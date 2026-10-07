import math
from django.db import transaction
from django.utils import timezone
from django.db.models import Avg, StdDev, Variance
from bank.models.Question import Question
from bank.models.QuestionMetrics import QuestionMetrics
from bank.models.DistractorAnalysis import DistractorAnalysis
from bank.models.Answer import Answer
from submissions.models.Submission import Submission

def calculate_exam_psychometrics(exam_id):
    """
    Computes psychometric metrics (p-value, Discrimination Index, Point-Biserial, Distractor Rates, KR-20)
    for an exam and updates the Question Bank metrics.
    """
    # 1. Fetch all student submissions for this exam
    submissions = list(Submission.objects.filter(exam_id=exam_id, is_graded=True))
    total_students = len(submissions)
    if total_students < 2:
        return {"error": "عدد الطلاب غير كافٍ لإجراء التحليل الإحصائي (الحد الأدنى 2)"}

    # Extract student scores
    student_scores = [float(s.score or 0.0) for s in submissions]
    mean_total_score = sum(student_scores) / total_students
    variance_total = sum((x - mean_total_score) ** 2 for x in student_scores) / total_students
    std_dev_total = math.sqrt(variance_total) if variance_total > 0 else 1.0

    # Sort submissions by score descending to get 27% upper and lower groups
    submissions.sort(key=lambda s: float(s.score or 0.0), reverse=True)
    group_size = max(1, int(round(0.27 * total_students)))
    upper_group = submissions[:group_size]
    lower_group = submissions[-group_size:]

    # Get all questions used in this exam
    from exams.models.ExamQuestionOrder import ExamQuestionOrder
    question_orders = ExamQuestionOrder.objects.filter(exam_id=exam_id).select_related('question')
    
    p_values_for_kr20 = []
    question_reports = []

    with transaction.atomic():
        for qo in question_orders:
            q = qo.question
            if not q:
                continue

            metrics, _ = QuestionMetrics.objects.get_or_create(question=q)

            # Analyze answers from all submissions for this question
            # In submissions, student_answers is typically stored as JSON {question_id: answer_id or text}
            correct_count = 0
            correct_scores = []
            incorrect_scores = []
            
            # For option analysis
            option_counts = {}  # {answer_id: {'total': int, 'upper': int, 'lower': int}}
            for opt in q.options.all():
                option_counts[opt.id] = {'total': 0, 'upper': 0, 'lower': 0}

            # Tally responses
            for sub in submissions:
                ans_map = sub.student_answers or {}
                selected_ans_id = ans_map.get(str(q.id)) or ans_map.get(q.id)
                score_val = float(sub.score or 0.0)

                # Check correctness
                is_correct = False
                if q.questionType in ['Single Choice', 'True/False']:
                    try:
                        chosen_opt = Answer.objects.filter(id=selected_ans_id, question=q).first()
                        if chosen_opt and chosen_opt.isTrue:
                            is_correct = True
                    except Exception:
                        pass
                elif q.questionType == 'Essay':
                    # If essay has score > 0
                    is_correct = (sub.score or 0) > 0

                if is_correct:
                    correct_count += 1
                    correct_scores.append(score_val)
                else:
                    incorrect_scores.append(score_val)

                # Option tally
                if selected_ans_id and int(selected_ans_id) in option_counts:
                    option_counts[int(selected_ans_id)]['total'] += 1

            # Upper vs lower group for Discrimination Index
            upper_correct = 0
            for sub in upper_group:
                ans_map = sub.student_answers or {}
                selected_ans_id = ans_map.get(str(q.id)) or ans_map.get(q.id)
                if selected_ans_id and int(selected_ans_id) in option_counts:
                    option_counts[int(selected_ans_id)]['upper'] += 1
                if q.options.filter(id=selected_ans_id, isTrue=True).exists():
                    upper_correct += 1

            lower_correct = 0
            for sub in lower_group:
                ans_map = sub.student_answers or {}
                selected_ans_id = ans_map.get(str(q.id)) or ans_map.get(q.id)
                if selected_ans_id and int(selected_ans_id) in option_counts:
                    option_counts[int(selected_ans_id)]['lower'] += 1
                if q.options.filter(id=selected_ans_id, isTrue=True).exists():
                    lower_correct += 1

            # 1. p-value (difficulty)
            p_val = round(correct_count / total_students, 3)
            p_values_for_kr20.append(p_val)

            # Cumulative difficulty update
            metrics.total_correct_answers += correct_count
            metrics.total_respondents += total_students
            metrics.actual_difficulty = round(metrics.total_correct_answers / metrics.total_respondents, 3)

            # 2. Discrimination Index D = P_upper - P_lower
            p_upper = upper_correct / len(upper_group)
            p_lower = lower_correct / len(lower_group)
            metrics.discrimination_index = round(p_upper - p_lower, 3)

            # 3. Point-Biserial Correlation rpb = (M1 - M0)/St * sqrt(p*q)
            m1 = sum(correct_scores) / len(correct_scores) if correct_scores else 0.0
            m0 = sum(incorrect_scores) / len(incorrect_scores) if incorrect_scores else 0.0
            q_val = 1.0 - p_val
            if std_dev_total > 0 and (p_val * q_val) > 0:
                metrics.point_biserial = round(((m1 - m0) / std_dev_total) * math.sqrt(p_val * q_val), 3)
            else:
                metrics.point_biserial = 0.0

            metrics.usage_count += 1
            metrics.last_used_at = timezone.now()
            metrics.last_calculated_at = timezone.now()
            metrics.save()

            # 4. Distractor Analysis Update
            for opt in q.options.all():
                d_stat = option_counts.get(opt.id, {'total': 0, 'upper': 0, 'lower': 0})
                da, _ = DistractorAnalysis.objects.get_or_create(answer=opt, question=q)
                da.selection_count += d_stat['total']
                da.selection_rate = round(d_stat['total'] / total_students, 3) if total_students else 0.0
                da.upper_group_rate = round(d_stat['upper'] / len(upper_group), 3) if upper_group else 0.0
                da.lower_group_rate = round(d_stat['lower'] / len(lower_group), 3) if lower_group else 0.0
                da.last_calculated_at = timezone.now()
                da.save()

            question_reports.append({
                'question_id': q.id,
                'p_value': p_val,
                'discrimination_index': metrics.discrimination_index,
                'point_biserial': metrics.point_biserial
            })

        # Calculate KR-20 Reliability for Exam
        K = len(p_values_for_kr20)
        kr20 = 0.0
        if K > 1 and variance_total > 0:
            sum_pq = sum(p * (1.0 - p) for p in p_values_for_kr20)
            kr20 = round((K / (K - 1)) * (1.0 - (sum_pq / variance_total)), 3)

    return {
        "success": True,
        "total_students": total_students,
        "questions_analyzed": len(question_reports),
        "kr20_reliability": kr20,
        "question_reports": question_reports
    }
