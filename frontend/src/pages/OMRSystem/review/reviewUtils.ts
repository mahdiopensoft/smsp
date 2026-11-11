/**
 * OMR Human Review Utility Functions
 * Centralized logic for question classification, answer formatting, and image resolution.
 */

export interface ReviewQuestion {
  id?: number | string
  question_number: number
  question_type?: string
  is_true_false?: boolean
  marked_choice?: string | null
  candidate_choice?: string | null
  final_marked_choice?: string | null
  correct_choice?: string | null
  is_correct?: boolean | null
  bubble_state?: string
  choice_confidences?: Record<string, number>
  final_confidence?: number
  decision_confidence?: number
  needs_review?: boolean
  review_priority?: string
  assigned_weight?: number | string
  marks_awarded?: number | string
  darkness_values?: Record<string, number>
  options?: string[]
  // Display mappings
  correct_choice_display?: string
  marked_choice_display?: string
  status?: string
  score?: string
  override?: string
}

export function normalizeChoice(choice: any): string {
  if (choice == null || choice === '') return ''
  const c = String(choice).trim().toUpperCase()
  const mapping: Record<string, string> = {
    '1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E',
    'أ': 'A', 'ا': 'A', 'ب': 'B', 'ج': 'C', 'د': 'D', 'هـ': 'E', 'ه': 'E',
    'صح': 'A', 'ص': 'A', 'T': 'A', 'TRUE': 'A', '✓': 'A',
    'خطأ': 'B', 'خ': 'B', 'F': 'B', 'FALSE': 'B', '✗': 'B',
  }
  return mapping[c] || c
}

export function isQuestionTrueFalse(q: any, totalQuestions: number = 50): boolean {
  if (!q) return false
  if (q.is_true_false === true || q.question_type === 'true_false' || q.question_type === 'صح وخطأ') {
    return true
  }
  if (q.is_true_false === false || q.question_type === 'mcq' || q.question_type === 'اختيارات') {
    return false
  }

  // Check confidences keys
  if (q.choice_confidences && typeof q.choice_confidences === 'object') {
    const keys = Object.keys(q.choice_confidences)
    if (keys.some(k => ['صح', 'خطأ', 'ص', 'خ'].includes(k))) return true
  }

  // Check marked_choice
  const m = String(q.marked_choice || '').trim()
  if (['صح', 'خطأ', 'ص', 'خ', 'TRUE', 'FALSE', 'T', 'F'].includes(m.toUpperCase())) {
    return true
  }

  // Check correct_choice
  const c = String(q.correct_choice || '').trim()
  if (['صح', 'خطأ', 'ص', 'خ', 'TRUE', 'FALSE', 'T', 'F'].includes(c.toUpperCase())) {
    return true
  }

  // Check options array
  if (Array.isArray(q.options) && q.options.length === 2) {
    if (q.options.some((opt: string) => ['صح', 'خطأ', 'ص', 'خ'].includes(opt))) return true
  }

  // Standard Yemeni ministerial exam convention (Q1 to Q20 is True/False)
  const qNum = Number(q.question_number || 0)
  const total = Number(totalQuestions || 50)
  if (total >= 20 && qNum >= 1 && qNum <= 20) {
    return true
  }

  return false
}

export function formatChoiceDisplay(choice: any, isTF: boolean, fallback: string = 'لم يُجب (فارغ)', options?: string[]): string {
  if (choice == null || choice === '' || choice === 'لم يُجب (فارغ)') {
    return fallback
  }
  const str = String(choice).trim()
  if (isTF) {
    const upper = str.toUpperCase()
    if (['A', '1', 'صح', 'ص', 'T', 'TRUE', '✓'].includes(upper)) return 'صح'
    if (['B', '2', 'خطأ', 'خ', 'F', 'FALSE', '✗'].includes(upper)) return 'خطأ'
    return str
  }

  // أسئلة الاختيارات المتعددة (MCQ)
  // إذا كانت خيارات النموذج أرقاماً (1, 2, 3, 4) كما في الاختبارات اليمنية
  // نقوم بمطابقة وعرض الأحرف والرموز بصيغة الخيار الرقمي الموحد لضمان التطابق التام بين العمودين
  const isNumericOptions = !options || options.length === 0 || options.some(opt => ['1', '2', '3', '4'].includes(opt))
  if (isNumericOptions) {
    const letterToNum: Record<string, string> = {
      'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5',
      'أ': '1', 'ب': '2', 'ج': '3', 'د': '4', 'هـ': '5', 'ه': '5',
    }
    const upper = str.toUpperCase()
    if (letterToNum[upper]) {
      return letterToNum[upper]
    }
  }

  return str
}

export function getQuestionOptions(q: any, totalQuestions: number = 50): string[] {
  if (!q) return ['1', '2', '3', '4']
  if (isQuestionTrueFalse(q, totalQuestions)) {
    return ['صح', 'خطأ']
  }
  if (Array.isArray(q.options) && q.options.length) {
    return q.options
  }
  // Default MCQ choices for Yemeni exams (1, 2, 3, 4)
  return ['1', '2', '3', '4']
}

export function fixImageUrl(url: any): string {
  if (!url || typeof url !== 'string') return ''
  const token = localStorage.getItem('token') || localStorage.getItem('access_token') || ''
  let cleanUrl = url
  if (url.startsWith('http://') || url.startsWith('https://')) {
    cleanUrl = url
  } else if (url.startsWith('/media/')) {
    cleanUrl = url
  } else if (url.startsWith('media/')) {
    cleanUrl = `/${url}`
  } else {
    cleanUrl = `/media/${url}`
  }
  if (token && cleanUrl.includes('/media/')) {
    cleanUrl = `${cleanUrl}${cleanUrl.includes('?') ? '&' : '?'}token=${token}`
  }
  return cleanUrl
}

export function resolveSheetImageUrl(sheet: any, imageMode: 'aligned' | 'original' = 'aligned'): string {
  if (!sheet) return ''
  let rawUrl = ''
  if (imageMode === 'aligned') {
    rawUrl = sheet.aligned_image || sheet.sheet_image || sheet.original_image || sheet.image_url || sheet.sheet_image_url || sheet.file || ''
  } else {
    rawUrl = sheet.original_image || sheet.sheet_image || sheet.aligned_image || sheet.image_url || sheet.sheet_image_url || sheet.file || ''
  }
  return fixImageUrl(rawUrl)
}

export function getStatusChip(q: any): { text: string; color: string; icon: string } {
  if (!q) return { text: 'لم يُجب (فارغ)', color: 'grey', icon: 'mdi-circle-outline' }
  if (q.bubble_state === 'ambiguous') {
    return { text: 'ملتبس', color: 'primary', icon: 'mdi-help-circle-outline' }
  }
  if (q.is_correct === true) {
    return { text: 'صحيحة', color: 'success', icon: 'mdi-check-circle-outline' }
  }
  if (q.is_correct === false && q.marked_choice && q.marked_choice !== 'لم يُجب (فارغ)') {
    return { text: 'خاطئة', color: 'error', icon: 'mdi-close-circle-outline' }
  }
  return { text: 'لم يُجب (فارغ)', color: 'grey', icon: 'mdi-circle-outline' }
}

export function enrichQuestion(q: any, totalQuestions: number = 50): ReviewQuestion {
  if (!q) return q
  const isTF = isQuestionTrueFalse(q, totalQuestions)
  q.is_true_false = isTF
  q.question_type = isTF ? 'صح وخطأ' : 'اختيارات'
  q.options = getQuestionOptions(q, totalQuestions)
  q.correct_choice_display = formatChoiceDisplay(q.correct_choice, isTF, 'لم تُحدد', q.options)
  q.marked_choice_display = formatChoiceDisplay(q.marked_choice, isTF, 'لم يُجب (فارغ)', q.options)

  // مطابقة منطقية حاسمة لمنع أي تعارض بين تظليل الطالب والإجابة النموذجية
  if (q.correct_choice && q.marked_choice && q.marked_choice !== 'لم يُجب (فارغ)') {
    const isMatch = normalizeChoice(q.marked_choice) === normalizeChoice(q.correct_choice)
    q.is_correct = isMatch
    const weight = Number(q.assigned_weight || 1.0)
    if (isMatch) {
      q.marks_awarded = (q.marks_awarded != null && Number(q.marks_awarded) > 0) ? q.marks_awarded : weight
    } else {
      q.marks_awarded = 0.0
    }
  }

  const statusInfo = getStatusChip(q)
  q.status = statusInfo.text
  q.score = q.is_correct
    ? (q.marks_awarded != null && Number(q.marks_awarded) > 0 ? Number(q.marks_awarded).toFixed(1).replace('.0', '') : '1.0')
    : '0.0'
  q.override = q.marked_choice ? `تظليل حالي: ${q.marked_choice_display}` : 'متاح للتعديل السريع'
  return q
}
