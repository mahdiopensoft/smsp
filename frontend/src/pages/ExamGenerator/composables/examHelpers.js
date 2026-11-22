/**
 * Shared Helpers & Enums for Exam Generator
 */

export const difficultyColor = (profile) => {
  const map = { 
    easy: 'success', 1: 'success', '1': 'success', 'سهل': 'success',
    medium: 'warning', 2: 'warning', '2': 'warning', 'متوسط': 'warning',
    hard: 'error', 3: 'error', '3': 'error', 'صعب': 'error',
    mixed: 'info', custom: 'deep-purple' 
  }
  return map[profile] || 'info'
}

export const difficultyLabel = (profile) => {
  const map = { 
    easy: 'سهل', 1: 'سهل', '1': 'سهل', 'سهل': 'سهل',
    medium: 'متوسط', 2: 'متوسط', '2': 'متوسط', 'متوسط': 'متوسط',
    hard: 'صعب', 3: 'صعب', '3': 'صعب', 'صعب': 'صعب',
    mixed: 'مختلط', custom: 'مخصص' 
  }
  return map[profile] || profile
}

export const questionTypeLabel = (type) => {
  if (!type) return 'اختيار من متعدد'
  const mapping = {
    'Single Choice': 'اختيار من متعدد',
    'single_choice': 'اختيار من متعدد',
    'mcq': 'اختيار من متعدد',
    'True/False': 'صح وخطأ',
    'true_false': 'صح وخطأ',
    'tf': 'صح وخطأ',
    'Multiple Choice': 'خيارات متعددة',
    'multiple_choice': 'خيارات متعددة',
    'Essay': 'مقالي',
    'essay': 'مقالي',
    'Fill in the Blanks': 'إكمال فراغات',
    'fill_blanks': 'إكمال فراغات',
    'Matching': 'مطابقة وتوصيل',
    'matching': 'مطابقة وتوصيل',
    'Ordering': 'إعادة ترتيب',
    'ordering': 'إعادة ترتيب',
  }
  return mapping[type] || type
}

export const questionTypeColor = (type) => {
  if (!type) return 'primary'
  if (type.includes('Single') || type.includes('mcq')) return 'primary'
  if (type.includes('True') || type.includes('tf')) return 'success'
  if (type.includes('Multiple')) return 'info'
  if (type.includes('Essay')) return 'warning'
  if (type.includes('Fill')) return 'deep-purple'
  if (type.includes('Matching')) return 'teal'
  if (type.includes('Ordering')) return 'cyan'
  return 'primary'
}

export const questionTypeIcon = (type) => {
  if (!type) return 'mdi-radiobox-marked'
  if (type.includes('Single') || type.includes('mcq')) return 'mdi-radiobox-marked'
  if (type.includes('True') || type.includes('tf')) return 'mdi-check-circle-outline'
  if (type.includes('Multiple')) return 'mdi-checkbox-multiple-marked-outline'
  if (type.includes('Essay')) return 'mdi-text-box-edit-outline'
  if (type.includes('Fill')) return 'mdi-form-textbox'
  if (type.includes('Matching')) return 'mdi-swap-horizontal-bold'
  if (type.includes('Ordering')) return 'mdi-sort-ascending'
  return 'mdi-help-circle-outline'
}

export const arabicOptionLetter = (idx) => ['أ', 'ب', 'ج', 'د', 'هـ', 'و'][idx] || (idx + 1)

export const isTF = (type) => {
  if (!type) return false
  const t = String(type).toLowerCase()
  return t.includes('true') || t.includes('tf') || t.includes('صح') || t.includes('صواب')
}

export const isOptionTrue = (q, idx) => {
  if (q && q.options && q.options.length > idx) {
    return Boolean(q.options[idx].isTrue)
  }
  return idx === 0 ? Boolean(q && q.isTrue) : !Boolean(q && q.isTrue)
}

export const calculateStagedTotalMarks = (model) => {
  if (!model || !model.questions) return 0
  const sum = model.questions.reduce((acc, q) => acc + (parseFloat(q.assignedMark) || 0), 0)
  return Math.round(sum * 100) / 100
}
