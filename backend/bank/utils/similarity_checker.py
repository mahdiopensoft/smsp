import re
import math
from collections import Counter
from django.utils.html import strip_tags

ARABIC_DIACRITICS = re.compile(r'[\u064B-\u0652\u0670\u0640]')
ARABIC_PUNCTUATIONS = re.compile(r'[،؛؟.,!?:;\"\'\(\)\[\]\{\}\\\/<>_\-\+=~`*&^%$#@|]')

ARABIC_STOPWORDS = {
    'من', 'إلى', 'عن', 'على', 'في', 'حتى', 'مع', 'هذا', 'هذه', 'هؤلاء', 'ذلك',
    'تلك', 'الذي', 'التي', 'الذين', 'اللاتي', 'اللواتي', 'هو', 'هي', 'هم', 'هن',
    'أنا', 'نحن', 'أنت', 'أنتم', 'ما', 'ماذا', 'لماذا', 'كيف', 'متى', 'أين',
    'هل', 'كم', 'أي', 'إذا', 'إن', 'أن', 'لكن', 'ثم', 'أو', 'أم', 'بل', 'لا',
    'لم', 'لن', 'ليس', 'غير', 'كل', 'بعض', 'كلما', 'بينما', 'حيث', 'فإن', 'وقد',
    'قد', 'كان', 'كانت', 'يكون', 'تكون', 'أحد', 'إحدى'
}

def normalize_arabic_text(text):
    if not text:
        return ""
    # Strip HTML tags
    text = strip_tags(text)
    # Remove diacritics & tatweel
    text = ARABIC_DIACRITICS.sub('', text)
    # Normalize Alef variants
    text = re.sub(r'[إأآٱ]', 'ا', text)
    # Normalize Teh Marbuta
    text = re.sub(r'ة', 'ه', text)
    # Normalize Yeh variants
    text = re.sub(r'ى', 'ي', text)
    # Remove punctuations and symbols
    text = ARABIC_PUNCTUATIONS.sub(' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def get_word_vector(text):
    clean_text = normalize_arabic_text(text)
    words = clean_text.split()
    filtered_words = [w for w in words if w not in ARABIC_STOPWORDS and len(w) > 1]
    return Counter(filtered_words)

def cosine_similarity(counter1, counter2):
    if not counter1 or not counter2:
        return 0.0
    
    intersection = set(counter1.keys()) & set(counter2.keys())
    numerator = sum(counter1[x] * counter2[x] for x in intersection)
    
    sum1 = sum(v ** 2 for v in counter1.values())
    sum2 = sum(v ** 2 for v in counter2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    return float(numerator) / denominator

def check_question_similarity(content_text, lesson_id=None, threshold=0.80, exclude_question_id=None):
    """
    Checks if a question's text is duplicate (>= threshold) compared to other questions in the same lesson.
    Returns:
        dict: {
            'is_duplicate': bool,
            'max_similarity': float (0-100),
            'matched_questions': list of dicts with id, content, similarity
        }
    """
    from bank.models.Question import Question

    new_vector = get_word_vector(content_text)
    if not new_vector:
        return {'is_duplicate': False, 'max_similarity': 0.0, 'matched_questions': []}

    qs = Question.objects.exclude(status='مرفوض')
    if lesson_id:
        qs = qs.filter(lesson_id=lesson_id)
    if exclude_question_id:
        qs = qs.exclude(id=exclude_question_id)

    matched = []
    max_sim = 0.0

    for q in qs.only('id', 'content', 'status')[:200]:
        q_vector = get_word_vector(q.content)
        sim = cosine_similarity(new_vector, q_vector)
        if sim >= 0.50:  # Report any high similarity >= 50%
            clean_snippet = strip_tags(q.content)[:80]
            matched.append({
                'id': q.id,
                'snippet': clean_snippet,
                'status': q.status,
                'similarity_percentage': round(sim * 100, 1)
            })
            if sim > max_sim:
                max_sim = sim

    matched.sort(key=lambda x: x['similarity_percentage'], reverse=True)
    is_duplicate = (max_sim >= threshold)

    return {
        'is_duplicate': is_duplicate,
        'max_similarity': round(max_sim * 100, 1),
        'matched_questions': matched[:5]
    }
