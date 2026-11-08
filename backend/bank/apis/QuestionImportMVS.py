import json
from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.Answer import Answer
from bank.models.ImportSession import ImportSession
from bank.models.AuditLog import AuditLog
from bank.models.QuestionMetrics import QuestionMetrics
from bank.serializers.Question import QuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import pandas as pd


def _clean_str(val):
    if val is None or pd.isna(val):
        return ''
    s = str(val).strip()
    if s.lower() in ['nan', 'none', 'null']:
        return ''
    return s


def _parse_difficulty(val):
    s = _clean_str(val).lower()
    if s in ['1', 'سهل', 'easy']:
        return Question.DifficultyChoices.EASY
    if s in ['2', 'متوسط', 'medium']:
        return Question.DifficultyChoices.MEDIUM
    if s in ['3', 'صعب', 'hard']:
        return Question.DifficultyChoices.HARD
    return Question.DifficultyChoices.MEDIUM


def _parse_bloom(val):
    s = _clean_str(val).strip()
    valid_blooms = {
        'تذكر': Question.BloomChoices.REMEMBER,
        'فهم': Question.BloomChoices.UNDERSTAND,
        'تطبيق': Question.BloomChoices.APPLY,
        'تحليل': Question.BloomChoices.ANALYZE,
        'تقييم': Question.BloomChoices.EVALUATE,
        'ابتكار': Question.BloomChoices.CREATE,
    }
    for k, v in valid_blooms.items():
        if k in s:
            return v
    return Question.BloomChoices.APPLY


def _parse_mark(val, default=1.0):
    try:
        s = _clean_str(val)
        return float(s) if s else default
    except (ValueError, TypeError):
        return default


def _parse_time(val, default=1):
    try:
        s = _clean_str(val)
        return int(float(s)) if s else default
    except (ValueError, TypeError):
        return default


def _determine_question_type(raw_type, raw_correct, options):
    t = _clean_str(raw_type).lower()
    if any(k in t for k in ['اختيار واحد', 'single choice', 'single', 'واحد']):
        return Question.TypeChoices.SINGLE_CHOICE
    if any(k in t for k in ['متعدد', 'multiple choice', 'multiple', 'عدة خيارات', 'عدة إجابات', 'خيارات متعددة']):
        return Question.TypeChoices.MULTIPLE_CHOICE
    if any(k in t for k in ['صح وخطأ', 'صح او خطا', 'صح و خطأ', 'true/false', 'true_false', 'صواب']):
        return Question.TypeChoices.TRUE_FALSE
    if any(k in t for k in ['مقالي', 'essay', 'مقال']):
        return Question.TypeChoices.ESSAY

    # Auto-detection heuristics:
    ans_clean = _clean_str(raw_correct).lower()
    if ans_clean in ['صح', 'صواب', 'نعم', 'true', 'خطأ', 'خطا', 'لا', 'false']:
        return Question.TypeChoices.TRUE_FALSE

    if any(sep in ans_clean for sep in [',', ';', '،', ' و ']):
        return Question.TypeChoices.MULTIPLE_CHOICE

    if not options and len(ans_clean) > 2 and not ans_clean.isdigit():
        return Question.TypeChoices.ESSAY

    return Question.TypeChoices.SINGLE_CHOICE


def _parse_multiple_correct_indices(raw_correct, options):
    s = _clean_str(raw_correct).replace('،', ',').replace(';', ',').replace(' و ', ',')
    parts = [p.strip() for p in s.split(',') if p.strip()]
    letter_map = {'أ': 1, 'ا': 1, 'a': 1, 'ب': 2, 'b': 2, 'ج': 3, 'c': 3, 'د': 4, 'd': 4, 'هـ': 5, 'ه': 5, 'e': 5}
    correct_indices = set()
    for p in parts:
        p_lower = p.lower()
        if p_lower in letter_map:
            correct_indices.add(letter_map[p_lower])
        else:
            try:
                correct_indices.add(int(float(p)))
            except (ValueError, TypeError):
                matched = next((opt_num for opt_num, opt_val in options if opt_val.strip().lower() == p_lower), None)
                if matched:
                    correct_indices.add(matched)
    return correct_indices or {1}


def _parse_single_correct_index(raw_correct, options):
    s = _clean_str(raw_correct).lower()
    letter_map = {'أ': 1, 'ا': 1, 'a': 1, 'ب': 2, 'b': 2, 'ج': 3, 'c': 3, 'د': 4, 'd': 4, 'هـ': 5, 'ه': 5, 'e': 5}
    if s in letter_map:
        return letter_map[s]
    try:
        return int(float(s))
    except (ValueError, TypeError):
        matched = next((opt_num for opt_num, opt_val in options if opt_val.strip().lower() == s), 1)
        return matched


def _parse_true_false_val(raw_correct):
    s = _clean_str(raw_correct).lower()
    if s in ['صح', 'صواب', 'نعم', 'true', '1', 'أ', 'a']:
        return True
    if s in ['خطأ', 'خطا', 'لا', 'false', '2', 'ب', 'b']:
        return False
    return True


class QuestionImportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Excel/CSV Question Importing.
    Endpoint: /api/bank/question-import/
    Used by: QuestionImportView.vue
    Supports Universal Smart Templates: Single Choice, Multiple Choice, True/False, Essay.
    Accepts raw Excel/CSV file OR pre-validated 'questions' JSON list.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        return self._process_excel_import(request)

    @action(detail=False, methods=['post'], url_path='import-excel')
    def import_excel(self, request):
        return self._process_excel_import(request)

    def _process_excel_import(self, request):
        req_data = getattr(request, 'data', None)
        if req_data is None:
            req_data = getattr(request, 'POST', {})
        req_files = getattr(request, 'FILES', {})

        lesson_id = req_data.get('fk_lesson') or req_data.get('lesson')
        file = req_files.get('file') or req_data.get('file')
        questions_raw = req_data.get('questions')
        
        if not lesson_id:
            return Response(
                {"success": False, "message": "يجب تحديد الدرس الأكاديمي المطلوب ربط الأسئلة به"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not file and not questions_raw:
            return Response(
                {"success": False, "message": "يجب توفير ملف الإكسل أو قائمة الأسئلة المجهزة"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_by = request.user if request.user and request.user.is_authenticated else None
        user_display_name = "مستخدم النظام"
        if created_by:
            user_display_name = f"{created_by.first_name or ''} {created_by.last_name or ''}".strip() or created_by.username
        file_name = getattr(file, 'name', 'قائمة أسئلة جاهزة')
        institution_type = req_data.get('institution_type', 'school')

        # Standardized questions rows list: each dict has text, options, raw_correct, raw_type, mark, difficulty, bloom, time
        standardized_rows = []

        try:
            # 1. Check if prepared questions JSON was supplied
            if questions_raw:
                if isinstance(questions_raw, str):
                    try:
                        parsed_list = json.loads(questions_raw)
                    except Exception:
                        parsed_list = []
                elif isinstance(questions_raw, list):
                    parsed_list = questions_raw
                else:
                    parsed_list = []

                for item in parsed_list:
                    if not isinstance(item, dict):
                        continue
                    q_text = _clean_str(item.get('text'))
                    if not q_text:
                        continue
                    
                    opts = []
                    for opt_i in [1, 2, 3, 4]:
                        val = _clean_str(item.get(f'opt{opt_i}'))
                        if val:
                            opts.append((opt_i, val))
                    
                    standardized_rows.append({
                        'text': q_text,
                        'options': opts,
                        'raw_correct': _clean_str(item.get('answer')),
                        'raw_type': _clean_str(item.get('type')),
                        'mark': item.get('mark', 1.0),
                        'difficulty': item.get('difficulty', '2'),
                        'bloom': item.get('bloomLevel') or item.get('bloom', 'تطبيق'),
                        'time': item.get('time', 1),
                    })

            # 2. Otherwise read from Excel/CSV file
            elif file:
                df = pd.read_excel(file)
                if df.empty:
                    return Response(
                        {"success": False, "message": "ملف الإكسل فارغ ولا يحتوي على بيانات"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                headers = [str(c).strip() for c in df.columns]
                type_idx = None
                question_idx = None
                opt_indices = []
                answer_idx = None
                mark_idx = None
                difficulty_idx = None
                bloom_idx = None
                time_idx = None

                for idx, h in enumerate(headers):
                    h_lower = h.lower()
                    if 'نوع' in h_lower or 'type' in h_lower:
                        type_idx = idx
                    elif any(k in h_lower for k in ['نص السؤال', 'نص', 'السؤال', 'question', 'content']):
                        question_idx = idx
                    elif any(k in h_lower for k in ['الخيار', 'خيار', 'option', 'بديل']):
                        opt_indices.append(idx)
                    elif any(k in h_lower for k in ['صحيحة', 'إجابة', 'مرجعية', 'answer', 'correct']):
                        answer_idx = idx
                    elif any(k in h_lower for k in ['درجة', 'mark', 'score']):
                        mark_idx = idx
                    elif any(k in h_lower for k in ['صعوبة', 'difficulty']):
                        difficulty_idx = idx
                    elif any(k in h_lower for k in ['بلوم', 'bloom']):
                        bloom_idx = idx
                    elif any(k in h_lower for k in ['زمن', 'وقت', 'time', 'دقيقة']):
                        time_idx = idx

                total_cols = df.shape[1]
                if question_idx is None:
                    col0_header = headers[0].lower() if headers else ''
                    col0_val = _clean_str(df.iloc[0, 0]).lower() if len(df) > 0 else ''
                    is_first_col_type = (
                        'نوع' in col0_header or
                        col0_val in ['اختيار واحد', 'صح وخطأ', 'خيارات متعددة', 'مقالي', 'single choice', 'true/false']
                    )

                    if is_first_col_type:
                        type_idx = 0
                        question_idx = 1
                        opt_indices = [2, 3, 4, 5] if total_cols >= 6 else []
                        answer_idx = 6 if total_cols > 6 else (5 if total_cols == 6 else None)
                        mark_idx = 7 if total_cols > 7 else None
                        difficulty_idx = 8 if total_cols > 8 else None
                        bloom_idx = 9 if total_cols > 9 else None
                    else:
                        type_idx = None
                        question_idx = 0
                        opt_indices = [1, 2, 3, 4] if total_cols >= 5 else []
                        answer_idx = 5 if total_cols > 5 else (4 if total_cols == 5 else None)
                        mark_idx = 6 if total_cols > 6 else None
                        difficulty_idx = 7 if total_cols > 7 else None
                        bloom_idx = 8 if total_cols > 8 else None

                for index, row in df.iterrows():
                    q_text = ''
                    if question_idx is not None and question_idx < len(row):
                        q_text = _clean_str(row.iloc[question_idx])
                    if not q_text or q_text.startswith('نص السؤال') or q_text.startswith('نوع السؤال'):
                        continue

                    options = []
                    for order_num, col_i in enumerate(opt_indices, start=1):
                        if col_i < len(row):
                            opt_val = _clean_str(row.iloc[col_i])
                            if opt_val:
                                options.append((order_num, opt_val))

                    raw_correct = ''
                    if answer_idx is not None and answer_idx < len(row):
                        raw_correct = _clean_str(row.iloc[answer_idx])

                    raw_type = ''
                    if type_idx is not None and type_idx < len(row):
                        raw_type = _clean_str(row.iloc[type_idx])

                    standardized_rows.append({
                        'text': q_text,
                        'options': options,
                        'raw_correct': raw_correct,
                        'raw_type': raw_type,
                        'mark': row.iloc[mark_idx] if mark_idx is not None and mark_idx < len(row) else 1.0,
                        'difficulty': row.iloc[difficulty_idx] if difficulty_idx is not None and difficulty_idx < len(row) else '2',
                        'bloom': row.iloc[bloom_idx] if bloom_idx is not None and bloom_idx < len(row) else 'تطبيق',
                        'time': row.iloc[time_idx] if time_idx is not None and time_idx < len(row) else 1,
                    })

            if not standardized_rows:
                return Response(
                    {"success": False, "message": "لا توجد أسئلة صالحة للاستيراد"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            created_count = 0
            type_counts = {
                Question.TypeChoices.SINGLE_CHOICE: 0,
                Question.TypeChoices.MULTIPLE_CHOICE: 0,
                Question.TypeChoices.TRUE_FALSE: 0,
                Question.TypeChoices.ESSAY: 0,
            }
            all_answers_to_create = []
            created_questions = []

            with transaction.atomic():
                import_session = ImportSession.objects.create()

                for row_data in standardized_rows:
                    q_text = row_data['text']
                    options = row_data['options']
                    raw_correct = row_data['raw_correct']
                    raw_type = row_data['raw_type']

                    q_type = _determine_question_type(raw_type, raw_correct, options)
                    q_mark = _parse_mark(row_data.get('mark'), 1.0)
                    q_difficulty = _parse_difficulty(row_data.get('difficulty', '2'))
                    q_bloom = _parse_bloom(row_data.get('bloom', 'تطبيق'))
                    q_time = _parse_time(row_data.get('time', 1))

                    is_true_field = None
                    answer_text_field = None

                    if q_type == Question.TypeChoices.TRUE_FALSE:
                        truth_val = _parse_true_false_val(raw_correct)
                        is_true_field = truth_val
                        answer_text_field = 'صح' if truth_val else 'خطأ'
                    elif q_type == Question.TypeChoices.ESSAY:
                        answer_text_field = raw_correct

                    q = Question.objects.create(
                        content=q_text,
                        questionType=q_type,
                        difficulty=q_difficulty,
                        bloomLevel=q_bloom,
                        defaultMark=q_mark,
                        expected_time_minutes=q_time,
                        status=Question.StatusChoices.PENDING,
                        institution_type=institution_type,
                        lesson_id=lesson_id,
                        createdBy=created_by,
                        import_session=import_session,
                        isTrue=is_true_field,
                        answerText=answer_text_field
                    )
                    created_questions.append(q)
                    type_counts[q_type] = type_counts.get(q_type, 0) + 1
                    created_count += 1

                    used_orders = set()

                    if q_type == Question.TypeChoices.SINGLE_CHOICE:
                        correct_idx = _parse_single_correct_index(raw_correct, options)
                        for opt_num, opt_val in options:
                            order_val = opt_num
                            while order_val in used_orders:
                                order_val += 1
                            used_orders.add(order_val)
                            all_answers_to_create.append(Answer(
                                question=q,
                                text=opt_val,
                                isTrue=(opt_num == correct_idx),
                                order_index=order_val
                            ))

                    elif q_type == Question.TypeChoices.MULTIPLE_CHOICE:
                        correct_indices = _parse_multiple_correct_indices(raw_correct, options)
                        for opt_num, opt_val in options:
                            order_val = opt_num
                            while order_val in used_orders:
                                order_val += 1
                            used_orders.add(order_val)
                            all_answers_to_create.append(Answer(
                                question=q,
                                text=opt_val,
                                isTrue=(opt_num in correct_indices),
                                order_index=order_val
                            ))

                    elif q_type == Question.TypeChoices.TRUE_FALSE:
                        truth_val = (is_true_field is True)
                        if len(options) >= 2:
                            for opt_num, opt_val in options[:2]:
                                is_correct = truth_val if opt_num == 1 else (not truth_val)
                                all_answers_to_create.append(Answer(
                                    question=q,
                                    text=opt_val,
                                    isTrue=is_correct,
                                    order_index=opt_num
                                ))
                        else:
                            all_answers_to_create.append(Answer(
                                question=q,
                                text='صح',
                                isTrue=truth_val,
                                order_index=1
                            ))
                            all_answers_to_create.append(Answer(
                                question=q,
                                text='خطأ',
                                isTrue=not truth_val,
                                order_index=2
                            ))

                    elif q_type == Question.TypeChoices.ESSAY:
                        pass

                if all_answers_to_create:
                    Answer.objects.bulk_create(all_answers_to_create)

                if created_questions:
                    QuestionMetrics.objects.bulk_create([
                        QuestionMetrics(question=q) for q in created_questions
                    ])
                    AuditLog.objects.bulk_create([
                        AuditLog(
                            user=created_by,
                            action=AuditLog.ActionChoices.IMPORT,
                            resource_type='Question',
                            resource_id=str(q.id),
                            description=f"تم استيراد سؤال ({q.questionType}) من ملف إكسل ({file_name}) بواسطة {user_display_name}",
                            changes={
                                "source": "excel",
                                "file_name": file_name,
                                "type": q.questionType,
                                "mark": q.defaultMark,
                                "difficulty": q.difficulty
                            }
                        )
                        for q in created_questions
                    ])

            return Response({
                "success": True,
                "count": created_count,
                "type_breakdown": type_counts,
                "import_session_id": str(import_session.id) if created_questions else None,
                "message": f"تم استيراد {created_count} أسئلة بنجاح!"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"success": False, "message": f"فشل في استيراد الملف: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
