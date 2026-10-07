"""
svg_omr_engine.py — محرك OMR الموحد (v1)
==========================================
الإحداثيات مشتقة رياضياً من OmrSheetMultigraphics.vue.
هذا الملف هو المرجع الوحيد للإحداثيات — لا تُعدّل القيم يدوياً.

معادلات الاشتقاق:
  responses-section : translate(8, 88)
  عمود RTL col=1..4 : translate((4-col)*49, 0)
  bubble_y (مطلق)   : 88 + 6 + (row-1)*4.2 + 2.1 = 96.1 + (row-1)*4.2
  bubble_x (مطلق)   : col_abs_x + {A:4.5, B:13.5, C:22.5, D:31.5}
  نصف القطر         : r = 1.7 mm
"""

import math
import logging
import time
import numpy as np
import cv2

logger = logging.getLogger("omr.svg_engine")

DPI   = 300
SCALE = DPI / 25.4   # px/mm = 11.81102362...

# ── الشبكة الرأسية (Y) ──────────────────────────────────────────
START_Y = 96.1   # mm — مركز Q1  = 88(sec) + 6(header) + 2.1(cy_inner)
SPACING = 4.2    # mm — مسافة مركز لمركز بين صفين متتاليين
R_MM    = 1.7    # mm — نصف قطر الدائرة (r="1.7" في SVG)

# ── الأعمدة والخيارات (X مطلق بالمليمتر من يسار الورقة) ─────────
COL_GROUPS = [
    (  1,  45, {'A': 159.5, 'B': 168.5, 'C': 177.5, 'D': 186.5}),
    ( 46,  90, {'A': 110.5, 'B': 119.5, 'C': 128.5, 'D': 137.5}),
    ( 91, 135, {'A':  61.5, 'B':  70.5, 'C':  79.5, 'D':  88.5}),
    (136, 180, {'A':  12.5, 'B':  21.5, 'C':  30.5, 'D':  39.5}),
]
CHOICES = ['A', 'B', 'C', 'D']

# ── عتبات الكشف ─────────────────────────────────────────────────
DARK_THR     = 35     # بكسل أسفل هذه القيمة يُعدّ "داكناً"
TH_EMPTY     = 0.08   # أقل = فارغ تماماً
TH_HALF      = 0.25   # أقل = نصف تظليل
TH_FILLED    = 0.55   # فوق = مظلل كامل
SAMPLE_RATIO = 0.75   # نسبة القطر للفحص (يتجنب حافة الطباعة)


def bubble_center(q_id: int, choice: str, dpi: int = DPI):
    """إحداثيات مركز الدائرة بالبكسل (cx, cy, r)."""
    scale = dpi / 25.4
    for (qs, qe, xs) in COL_GROUPS:
        if qs <= q_id <= qe:
            row  = q_id - qs
            return (
                round(xs[choice] * scale),
                round((START_Y + row * SPACING) * scale),
                round(R_MM * scale),
            )
    raise ValueError(f"Q{q_id} خارج النطاق 1-180")


def analyze_bubble(gray: np.ndarray, cx: int, cy: int, r: int) -> dict:
    """تحليل دائرة واحدة وإرجاع حالتها."""
    inner_r = max(4, int(r * SAMPLE_RATIO))
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.circle(mask, (cx, cy), inner_r, 255, -1)
    pixels = gray[mask > 0]
    total  = len(pixels)
    if total == 0:
        return {'state': 'empty', 'fill_ratio': 0.0, 'mean_gray': 255.0}

    dark_px    = int(np.count_nonzero(pixels < DARK_THR))
    fill_ratio = dark_px / total
    mean_gray  = float(np.mean(pixels))

    if fill_ratio < TH_EMPTY:
        state = 'empty'
    elif fill_ratio < TH_HALF:
        # فحص خطوط الشطب
        y1 = max(0, cy - r); y2 = min(gray.shape[0], cy + r)
        x1 = max(0, cx - r); x2 = min(gray.shape[1], cx + r)
        roi = gray[y1:y2, x1:x2].copy()
        roi_mask = mask[y1:y2, x1:x2]
        roi[roi_mask == 0] = 255
        edges = cv2.Canny(roi, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, math.pi/180, 12,
                                minLineLength=int(r * 0.85), maxLineGap=3)
        state = 'crossed' if (lines is not None and len(lines) >= 2) else 'half_filled'
    elif fill_ratio < TH_FILLED:
        state = 'half_filled'
    else:
        state = 'filled'

    return {'state': state, 'fill_ratio': round(fill_ratio, 4), 'mean_gray': round(mean_gray, 1)}


def grade_sheet(image_path: str, answer_key: dict = None, dpi: int = DPI, use_ai: bool = True) -> dict:
    """
    تصحيح ورقة OMR كاملة.

    Args:
        image_path:  مسار الصورة (PNG/JPG، A4 @ 300 DPI)
        answer_key:  {1: 'A', 2: 'C', ...} — اختياري
        dpi:         دقة الصورة
        use_ai:      تفعيل AI verifier

    Returns:
        dict: answers, scores, questions, annotated_image (bytes)
    """
    t0 = time.time()

    # 1. قراءة الصورة
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"لا يمكن قراءة الصورة: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    logger.info(f"[SVG-OMR] {img.shape[1]}×{img.shape[0]}px @ {dpi}DPI")

    # ── Pass 1: OpenCV ────────────────────────────────────────────
    bubble_data = {}
    for q in range(1, 181):
        bubble_data[q] = {}
        for ch in CHOICES:
            cx, cy, r = bubble_center(q, ch, dpi)
            bubble_data[q][ch] = analyze_bubble(gray, cx, cy, r)

    # ── Pass 2: AI للحالات الغامضة ──────────────────────────────
    ai_used = 0
    if use_ai:
        try:
            from omr.providers.ai_verification import AIBubbleVerifier
            verifier = AIBubbleVerifier()
            uncertain = {'half_filled', 'crossed'}
            for q in range(1, 181):
                for ch in CHOICES:
                    if bubble_data[q][ch]['state'] in uncertain:
                        cx, cy, r = bubble_center(q, ch, dpi)
                        pad = int(r * 1.6)
                        y1 = max(0, cy - pad); y2 = min(gray.shape[0], cy + pad)
                        x1 = max(0, cx - pad); x2 = min(gray.shape[1], cx + pad)
                        pred = verifier.predict(gray[y1:y2, x1:x2])
                        if pred.get('label') != bubble_data[q][ch]['state']:
                            bubble_data[q][ch]['state'] = pred['label']
                            ai_used += 1
        except Exception as e:
            logger.warning(f"[SVG-OMR] AI غير متاح: {e}")

    # ── تحديد الإجابات والدرجات ───────────────────────────────────
    question_results = []
    total_correct = total_answered = 0
    score = 0.0

    for q in range(1, 181):
        states  = bubble_data[q]
        filled  = [ch for ch, d in states.items() if d['state'] == 'filled']
        half    = [ch for ch, d in states.items() if d['state'] == 'half_filled']
        crossed = [ch for ch, d in states.items() if d['state'] == 'crossed']
        effective = [ch for ch in (filled + half) if ch not in crossed]

        if len(effective) == 1:
            marked = effective[0]; mode = 'single'
        elif len(effective) > 1:
            marked = None; mode = 'double'
        elif crossed:
            marked = None; mode = 'crossed_only'
        else:
            marked = None; mode = 'empty'

        correct_ch = (answer_key or {}).get(q) or (answer_key or {}).get(str(q))
        is_correct = (marked == correct_ch) if (marked and correct_ch) else None
        marks = 1.0 if is_correct else 0.0

        if marked: total_answered += 1
        if is_correct: total_correct += 1; score += marks

        question_results.append({
            'q': q, 'marked': marked, 'mode': mode,
            'correct': correct_ch, 'is_correct': is_correct, 'marks': marks,
            'fill_ratios': {ch: states[ch]['fill_ratio'] for ch in CHOICES},
            'states':      {ch: states[ch]['state']      for ch in CHOICES},
        })

    # ── رسم الصورة المُعلَّقة ───────────────────────────────────
    annotated = _draw_annotated(img.copy(), question_results, dpi)
    _, buf = cv2.imencode('.png', annotated)

    elapsed_ms = (time.time() - t0) * 1000

    return {
        'total_questions': 180,
        'total_answered':  total_answered,
        'total_correct':   total_correct,
        'total_wrong':     total_answered - total_correct,
        'total_empty':     180 - total_answered,
        'score':           round(score, 2),
        'max_score':       180.0,
        'score_percent':   round(score / 180 * 100, 1),
        'ai_corrections':  ai_used,
        'processing_ms':   round(elapsed_ms, 1),
        'questions':       question_results,
        'annotated_image': buf.tobytes(),
        'answers':         {r['q']: r['marked'] for r in question_results},
    }


def _draw_annotated(img: np.ndarray, results: list, dpi: int) -> np.ndarray:
    """رسم النتائج على نسخة من الصورة."""
    for r in results:
        q = r['q']; marked = r['marked']
        correct = r['correct']; mode = r['mode']

        for ch in CHOICES:
            cx, cy, rr = bubble_center(q, ch, dpi)
            state = r['states'][ch]
            mk    = max(6, int(rr * 0.9))

            if state in ('filled', 'half_filled'):
                if mode == 'double':
                    cv2.circle(img, (cx, cy), mk, (0, 165, 255), 3)
                elif ch == marked:
                    if r['is_correct'] is True:
                        cv2.circle(img, (cx, cy), mk, (0, 210, 0), 3)
                    elif r['is_correct'] is False:
                        cv2.circle(img, (cx, cy), mk, (0, 0, 220), -1)
                        cv2.line(img, (cx-int(rr*.4), cy-int(rr*.4)), (cx+int(rr*.4), cy+int(rr*.4)), (255,255,255), 2)
                        cv2.line(img, (cx+int(rr*.4), cy-int(rr*.4)), (cx-int(rr*.4), cy+int(rr*.4)), (255,255,255), 2)
                    else:
                        cv2.circle(img, (cx, cy), mk, (255, 180, 0), 2)

            cv2.circle(img, (cx, cy), 2, (80, 80, 80), -1)

        if correct and marked and marked != correct and r['is_correct'] is False:
            cxc, cyc, rrc = bubble_center(q, correct, dpi)
            cv2.circle(img, (cxc, cyc), max(6, int(rrc * 0.9)), (0, 210, 0), 2)

    return img
ث