import { ref, reactive } from 'vue'

export interface DesignerConfig {
  template_id: string
  template_name: string
  version: string
  description: string
  display_mode: 'compact_a5' | 'audit_a4' | 'university_180'
  institution_type?: 'school' | 'university' | 'institute' | string
  paper: {
    size: string
    width_mm: number
    height_mm: number
    dpi: number
    orientation: 'portrait' | 'landscape'
  }
  header: {
    institution_name: string
    sub_title: string
    exam_name: string
    governorate: string
    directorate: string
    center_name: string
    center_code: string
    envelope_no: string
    student_name: string
    seat_number: string
    serial_number: string
    primary_color: string
    model_code?: string
    exam_stage_title?: string
  }
  metadata: {
    academic_year: string
  }
  student_fields: {
    enabled: boolean
  }
  questions: {
    metadata: {
      num_questions: number
    }
    layout: {
      columns_count: number
      choices_count: number
      bubble_radius_mm: number
      row_spacing_mm: number
      bubble_type: string
      tf_bubble_type: string
      layout_direction: 'rtl' | 'ltr'
      questions_per_column?: number
    }
    sections: Array<{
      id: string
      title: string
      from_q: number
      to_q: number
      choices: string[]
      mark: number
      type?: 'true_false' | 'mcq'
    }>
  }
  barcode: {
    enabled: boolean
    value: string
    format: string
  }
  qr: {
    enabled: boolean
    value: string
    ecc: string
  }
  footer: {
    right_text: string
    center_logo: string
    left_text: string
    document_label: string
    show_simulated_handwriting: boolean
  }
  instructions: {
    rule1: string
    correct_label: string
    rule2: string
    rule3: string
    rule4: string
    show_simulated_handwriting: boolean
  }
  detection: {
    engine: string
    ai_verification: boolean
    thresholds: {
      filled_min: number
      empty_max: number
    }
    tolerance_mm: number
  }
}

export const DEFAULT_CONFIG = (): DesignerConfig => ({
  template_id: 'YEMEN_MINISTRY_50',
  template_name: 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (50 سؤال)',
  version: '1.0',
  description: 'قالب اختبار الشهادة الثانوية العامة المعتمد: 20 سؤال صح/خطأ + 30 سؤال اختيار من متعدد + بطاقة بيانات الطالب ودوائر الغياب.',
  display_mode: 'compact_a5',
  institution_type: 'school',
  paper: {
    size: 'A5',
    width_mm: 210,
    height_mm: 148.5,
    dpi: 300,
    orientation: 'landscape',
  },
  header: {
    institution_name: 'الجمهورية اليمنية — وزارة التربية والتعليم',
    sub_title: 'قطاع المناهج والتوجيه — لجان الاختبارات',
    exam_name: 'القرآن الكريم',
    governorate: 'أمانة العاصمة',
    directorate: 'معين',
    center_name: 'سالم قطن — معين',
    center_code: '164',
    envelope_no: '2',
    student_name: 'عمرو عبدالباسط عبدالله قائد الزمر',
    seat_number: '418485',
    serial_number: '148',
    primary_color: '#000000',
  },
  metadata: {
    academic_year: '1444هـ — 2022-2023م',
  },
  student_fields: {
    enabled: true,
  },
  questions: {
    metadata: {
      num_questions: 50,
    },
    layout: {
      columns_count: 4,
      choices_count: 4,
      bubble_radius_mm: 1.8,
      row_spacing_mm: 5.2,
      bubble_type: 'numbers',
      tf_bubble_type: 'arabic',
      layout_direction: 'rtl',
    },
    sections: [
      { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
      { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2, type: 'mcq' },
    ],
  },
  barcode: {
    enabled: true,
    value: '41848501164148',
    format: 'CODE128',
  },
  qr: {
    enabled: true,
    value: 'YE-MOE-1444-418485-SUB1',
    ecc: 'M',
  },
  footer: {
    right_text: '',
    center_logo: '',
    left_text: '',
    document_label: '',
    show_simulated_handwriting: false,
  },
  instructions: {
    rule1: '1- يجب أن يكون تظليل الدائرة بقلم جاف أسود أو أزرق بشكل كامل مثال:',
    correct_label: 'واجب',
    rule2: '2 - تأكد من تظليل إجاباتك في الأماكن المخصصة لها.',
    rule3: '3 - يمنع استخدام المصحح.',
    rule4: '4 - لن تقبل الإجابات مالم تسجل على هذه الورقة، اترك لنفسك وقتاً كافياً لنقل الإجابات.',
    show_simulated_handwriting: false,
  },
  detection: {
    engine: 'opencv_omr',
    ai_verification: true,
    thresholds: {
      filled_min: 55,
      empty_max: 28,
    },
    tolerance_mm: 1.0,
  },
})

export function useDesignerConfig() {
  const pageMode = ref<'library' | 'designer'>('library')
  const designerTab = ref<'layout' | 'student' | 'questions' | 'codes' | 'detection'>('layout')
  const savedDbId = ref<number | string | null>(null)
  const config = reactive<DesignerConfig>(DEFAULT_CONFIG())

  function createNewTemplate() {
    savedDbId.value = null
    Object.assign(config, DEFAULT_CONFIG())
  }

  function startNewDesignerTemplate() {
    createNewTemplate()
    pageMode.value = 'designer'
  }

  function applyPreset(presetId: string) {
    if (presetId === 'YEMEN_MINISTRY_40') {
      Object.assign(config, DEFAULT_CONFIG())
      config.template_id = 'YEMEN_MINISTRY_40'
      config.template_name = 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (40 سؤال)'
      config.questions.metadata.num_questions = 40
      config.questions.sections = [
        { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
        { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 40, choices: ['1', '2', '3', '4'], mark: 2, type: 'mcq' },
      ]
    } else if (presetId === 'YEMEN_MINISTRY_50') {
      Object.assign(config, DEFAULT_CONFIG())
    } else if (presetId === 'YEMEN_MINISTRY_60') {
      Object.assign(config, DEFAULT_CONFIG())
      config.template_id = 'YEMEN_MINISTRY_60'
      config.template_name = 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (60 سؤال)'
      config.questions.metadata.num_questions = 60
      config.questions.sections = [
        { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
        { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 60, choices: ['1', '2', '3', '4'], mark: 1.5, type: 'mcq' },
      ]
    } else if (presetId === 'YEMEN_UNIVERSITY_180') {
      config.template_id = 'YEMEN_UNIVERSITY_180'
      config.template_name = 'نموذج الجامعات اليمنية العام (180 سؤال - 4 أعمدة)'
      config.institution_type = 'university'
      config.questions.metadata.num_questions = 180
      config.questions.layout.columns_count = 4
      config.questions.layout.choices_count = 4
      config.questions.layout.bubble_radius_mm = 1.7
      config.questions.layout.row_spacing_mm = 4.2
      config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
      config.header.sub_title = 'جامعة صنعاء — الإدارة العامة للامتحانات والتقويم الآلي'
      config.header.primary_color = '#1976D2'
    } else if (presetId === 'YEMEN_UNIVERSITY_100') {
      config.template_id = 'YEMEN_UNIVERSITY_100'
      config.template_name = 'نموذج الكليات والأقسام الجامعية (100 سؤال متعدد)'
      config.institution_type = 'university'
      config.questions.metadata.num_questions = 100
      config.questions.layout.columns_count = 4
      config.questions.layout.choices_count = 4
      config.questions.layout.bubble_radius_mm = 1.75
      config.questions.layout.row_spacing_mm = 4.6
      config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
      config.header.sub_title = 'جامعة صنعاء — كلية الحاسوب وتكنولوجيا المعلومات'
      config.header.primary_color = '#1976D2'
    } else if (presetId === 'YEMEN_INSTITUTE_60') {
      config.template_id = 'YEMEN_INSTITUTE_60'
      config.template_name = 'نموذج المعاهد التقنية والمهنية (60 سؤال: 20 صح/خطأ + 40 متعدد)'
      config.institution_type = 'institute'
      config.display_mode = 'compact_a5'
      config.questions.metadata.num_questions = 60
      config.questions.sections = [
        { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
        { id: 'sec2', title: 'القسم الثاني: الاختيار من متعدد', from_q: 21, to_q: 60, choices: ['1', '2', '3', '4'], mark: 1.5, type: 'mcq' },
      ]
      config.questions.layout.columns_count = 4
      config.questions.layout.choices_count = 4
      config.questions.layout.bubble_radius_mm = 2.0
      config.questions.layout.row_spacing_mm = 4.8
      config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني'
      config.header.sub_title = 'المعهد التقني الصناعي — إدارة الاختبارات والتقويم الآلي'
      config.header.exam_stage_title = 'اختبارات الدبلوم التقني والتدريب المهني'
      config.header.primary_color = '#00796B'
    } else if (presetId === 'YEMEN_INSTITUTE_80') {
      config.template_id = 'YEMEN_INSTITUTE_80'
      config.template_name = 'نموذج الدبلوم التقني الشامل للمعاهد (80 سؤال)'
      config.institution_type = 'institute'
      config.display_mode = 'compact_a5'
      config.questions.metadata.num_questions = 80
      config.questions.sections = [
        { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
        { id: 'sec2', title: 'القسم الثاني: الاختيار من متعدد', from_q: 21, to_q: 80, choices: ['1', '2', '3', '4'], mark: 1, type: 'mcq' },
      ]
      config.questions.layout.columns_count = 4
      config.questions.layout.choices_count = 4
      config.questions.layout.bubble_radius_mm = 1.8
      config.questions.layout.row_spacing_mm = 4.2
      config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني'
      config.header.sub_title = 'المعهد التقني التجاري — كنترول الاختبارات'
      config.header.primary_color = '#00796B'
    } else if (presetId === 'GENERAL_100') {
      config.template_id = 'GENERAL_100'
      config.template_name = 'النموذج المعياري العام (100 سؤال)'
      config.questions.metadata.num_questions = 100
      config.questions.layout.columns_count = 4
      config.questions.layout.choices_count = 4
      config.questions.layout.bubble_radius_mm = 1.75
      config.questions.layout.row_spacing_mm = 4.6
    }
  }

  function loadSavedTemplateState(t: any) {
    if (!t) return
    savedDbId.value = t.id
    const defaults = DEFAULT_CONFIG()
    const td = t.template_data || {}

    Object.assign(config, defaults)
    if (td.institution_type) config.institution_type = td.institution_type
    else if (t.institution_type) config.institution_type = t.institution_type
    if (td.paper) Object.assign(config.paper, td.paper)
    if (td.header) Object.assign(config.header, td.header)
    if (td.metadata) Object.assign(config.metadata, td.metadata)
    if (td.student_fields) Object.assign(config.student_fields, td.student_fields)
    if (td.questions) {
      if (td.questions.metadata) Object.assign(config.questions.metadata, td.questions.metadata)
      if (td.questions.layout) Object.assign(config.questions.layout, td.questions.layout)
      if (td.questions.sections) config.questions.sections = JSON.parse(JSON.stringify(td.questions.sections))
    }
    if (td.barcode) Object.assign(config.barcode, td.barcode)
    if (td.qr) Object.assign(config.qr, td.qr)
    if (td.footer) Object.assign(config.footer, td.footer)
    if (td.instructions) Object.assign(config.instructions, td.instructions)
    if (td.display_mode) config.display_mode = td.display_mode

    config.template_id = td.template_id || t.template_id || (t.total_mcq === 50 ? 'YEMEN_MINISTRY_50' : 'CUSTOM')
    config.template_name = t.name || config.template_name
    config.version = t.version || '1.0'
    config.description = t.description || ''
    if (config.header) {
      config.header.exam_name = td.header?.exam_name || t.name
    }
  }

  return {
    pageMode,
    designerTab,
    savedDbId,
    config,
    createNewTemplate,
    startNewDesignerTemplate,
    applyPreset,
    loadSavedTemplateState,
  }
}
