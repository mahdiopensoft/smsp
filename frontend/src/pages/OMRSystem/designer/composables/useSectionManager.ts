import { computed } from 'vue'

export function useSectionManager(props: { config: any }) {
  function ensureSections() {
    if (!props.config.questions.sections || !Array.isArray(props.config.questions.sections) || props.config.questions.sections.length === 0) {
      props.config.questions.sections = [
        { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
        { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2 },
      ]
    }
  }

  const sectionsList = computed(() => {
    ensureSections()
    return props.config.questions.sections
  })

  function getSectionCount(sec: any): number {
    if (!sec) return 0
    const from = sec.from_q || 1
    const to = sec.to_q || from
    return Math.max(1, to - from + 1)
  }

  const totalQuestionsCount = computed(() => {
    ensureSections()
    const secs = props.config.questions.sections
    if (!secs || secs.length === 0) return 50
    const lastSec = secs[secs.length - 1]
    return lastSec.to_q || 50
  })

  const totalExamMarks = computed(() => {
    ensureSections()
    let sum = 0
    for (const sec of props.config.questions.sections) {
      const count = getSectionCount(sec)
      const mark = sec.mark || 1
      sum += count * mark
    }
    return sum
  })

  const tfCount = computed(() => {
    ensureSections()
    return props.config.questions.sections
      .filter((s: any) => s.type === 'true_false')
      .reduce((sum: number, s: any) => sum + getSectionCount(s), 0)
  })

  const mcqCount = computed(() => {
    ensureSections()
    return props.config.questions.sections
      .filter((s: any) => s.type === 'mcq')
      .reduce((sum: number, s: any) => sum + getSectionCount(s), 0)
  })

  const tfSection = computed(() => {
    ensureSections()
    return props.config.questions.sections.find((s: any) => s.type === 'true_false')
  })

  const mcqSection = computed(() => {
    ensureSections()
    return props.config.questions.sections.find((s: any) => s.type === 'mcq')
  })

  const isYemeniPreset = computed(() => {
    return totalQuestionsCount.value === 50 && tfCount.value === 20 && mcqCount.value === 30
  })

  const hasDuplicateSectionTypes = computed(() => {
    ensureSections()
    const types = props.config.questions.sections.map((s: any) => s.type)
    return new Set(types).size !== types.length
  })

  function recalculateRanges() {
    ensureSections()
    let currentQ = 1
    for (const sec of props.config.questions.sections) {
      const count = getSectionCount(sec)
      sec.from_q = currentQ
      sec.to_q = currentQ + count - 1
      currentQ = sec.to_q + 1
    }
    props.config.questions.metadata.num_questions = currentQ - 1
  }

  function updateSectionCount(idx: number, newCount: number) {
    ensureSections()
    const sec = props.config.questions.sections[idx]
    if (!sec) return
    const count = Math.max(1, Math.min(200, isNaN(newCount) ? 1 : newCount))
    sec.to_q = (sec.from_q || 1) + count - 1
    recalculateRanges()
  }

  function onSectionTypeChange(idx: number, newType: string) {
    ensureSections()
    const sec = props.config.questions.sections[idx]
    if (!sec) return
    sec.type = newType
    if (newType === 'true_false') {
      sec.choices = ['صح', 'خطأ']
      sec.mark = sec.mark || 1
    } else {
      sec.choices = ['1', '2', '3', '4']
      sec.mark = sec.mark || 2
    }
  }

  function adjustTfCount(delta: number) {
    ensureSections()
    const newCount = Math.max(0, tfCount.value + delta)
    setTfCount(newCount)
  }

  function setTfCount(val: number) {
    ensureSections()
    const target = Math.max(0, Math.min(100, isNaN(val) ? 0 : val))
    const tfSecs = props.config.questions.sections.filter((s: any) => s.type === 'true_false')
    if (tfSecs.length === 0) {
      if (target > 0) {
        props.config.questions.sections.unshift({
          id: `sec_tf_${Date.now()}`,
          title: 'أسئلة الصواب والخطأ',
          type: 'true_false',
          from_q: 1,
          to_q: target,
          choices: ['صح', 'خطأ'],
          mark: 1,
        })
      }
    } else if (tfSecs.length === 1) {
      const idx = props.config.questions.sections.indexOf(tfSecs[0])
      if (target === 0 && props.config.questions.sections.length > 1) {
        removeSection(idx)
        return
      }
      updateSectionCount(idx, Math.max(1, target))
      return
    } else {
      tfSecs[0].to_q = (tfSecs[0].from_q || 1) + Math.max(1, target) - 1
      for (let i = 1; i < tfSecs.length; i++) {
        const idx = props.config.questions.sections.indexOf(tfSecs[i])
        props.config.questions.sections.splice(idx, 1)
      }
    }
    recalculateRanges()
  }

  function adjustMcqCount(delta: number) {
    ensureSections()
    const newCount = Math.max(0, mcqCount.value + delta)
    setMcqCount(newCount)
  }

  function setMcqCount(val: number) {
    ensureSections()
    const target = Math.max(0, Math.min(200, isNaN(val) ? 0 : val))
    const mcqSecs = props.config.questions.sections.filter((s: any) => s.type === 'mcq')
    if (mcqSecs.length === 0) {
      if (target > 0) {
        props.config.questions.sections.push({
          id: `sec_mcq_${Date.now()}`,
          title: 'أسئلة الاختيار من متعدد',
          type: 'mcq',
          from_q: 1,
          to_q: target,
          choices: ['1', '2', '3', '4'],
          mark: 2,
        })
      }
    } else if (mcqSecs.length === 1) {
      const idx = props.config.questions.sections.indexOf(mcqSecs[0])
      if (target === 0 && props.config.questions.sections.length > 1) {
        removeSection(idx)
        return
      }
      updateSectionCount(idx, Math.max(1, target))
      return
    } else {
      mcqSecs[0].to_q = (mcqSecs[0].from_q || 1) + Math.max(1, target) - 1
      for (let i = 1; i < mcqSecs.length; i++) {
        const idx = props.config.questions.sections.indexOf(mcqSecs[i])
        props.config.questions.sections.splice(idx, 1)
      }
    }
    recalculateRanges()
  }

  function addNewSection() {
    ensureSections()
    const lastSec = props.config.questions.sections[props.config.questions.sections.length - 1]
    const nextStart = lastSec ? ((lastSec.to_q || 1) + 1) : 1
    props.config.questions.sections.push({
      id: `sec_${Date.now()}`,
      title: `القسم ${props.config.questions.sections.length + 1}: أسئلة اختيار من متعدد`,
      type: 'mcq',
      from_q: nextStart,
      to_q: nextStart + 9,
      choices: ['1', '2', '3', '4'],
      mark: 1,
    })
    recalculateRanges()
  }

  function removeSection(idx: number) {
    ensureSections()
    if (props.config.questions.sections.length <= 1) return
    props.config.questions.sections.splice(idx, 1)
    recalculateRanges()
  }

  function moveSection(idx: number, direction: 'up' | 'down') {
    ensureSections()
    const targetIdx = direction === 'up' ? idx - 1 : idx + 1
    if (targetIdx < 0 || targetIdx >= props.config.questions.sections.length) return
    const item = props.config.questions.sections.splice(idx, 1)[0]
    props.config.questions.sections.splice(targetIdx, 0, item)
    recalculateRanges()
  }

  function mergeToStandardTwoSections() {
    ensureSections()
    const totalTf = tfCount.value
    const totalMcq = mcqCount.value
    const newSections: any[] = []

    if (totalTf > 0) {
      newSections.push({
        id: 'sec_tf',
        title: 'أسئلة الصواب والخطأ',
        type: 'true_false',
        from_q: 1,
        to_q: totalTf,
        choices: ['صح', 'خطأ'],
        mark: 1,
      })
    }

    if (totalMcq > 0) {
      const startMcq = totalTf + 1
      newSections.push({
        id: 'sec_mcq',
        title: 'أسئلة الاختيار من متعدد',
        type: 'mcq',
        from_q: startMcq,
        to_q: startMcq + totalMcq - 1,
        choices: ['1', '2', '3', '4'],
        mark: 2,
      })
    }

    props.config.questions.sections = newSections
    recalculateRanges()
  }

  function applyMinistry40() {
    props.config.template_id = 'YEMEN_MINISTRY_40'
    props.config.template_name = 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (40 سؤال)'
    props.config.display_mode = 'compact_a5'
    if (!props.config.paper) props.config.paper = {}
    props.config.paper.size = 'A5'
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 148.5
    props.config.paper.orientation = 'landscape'
    props.config.questions.metadata.num_questions = 40
    props.config.questions.sections = [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 40, choices: ['1', '2', '3', '4'], mark: 2 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.tf_bubble_type = 'arabic'
    props.config.questions.layout.row_spacing_mm = 5.2
    props.config.questions.layout.bubble_radius_mm = 2.1
  }

  function applyYemeniMinistry50() {
    props.config.template_id = 'YEMEN_MINISTRY_50'
    props.config.template_name = 'نموذج اختبار الشهادة الثانوية العامة — وزارة التربية والتعليم (50 سؤال)'
    props.config.display_mode = 'compact_a5'
    if (!props.config.paper) props.config.paper = {}
    props.config.paper.size = 'A5'
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 148.5
    props.config.paper.orientation = 'landscape'
    props.config.questions.metadata.num_questions = 50
    props.config.questions.sections = [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.tf_bubble_type = 'arabic'
    props.config.questions.layout.row_spacing_mm = 5.2
    props.config.questions.layout.bubble_radius_mm = 2.1
  }

  function applyMinistry60() {
    props.config.template_id = 'YEMEN_MINISTRY_60'
    props.config.template_name = 'نموذج اختبار (60 سؤال: 20 صح/خطأ + 40 متعدد)'
    props.config.questions.metadata.num_questions = 60
    props.config.questions.sections = [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 60, choices: ['1', '2', '3', '4'], mark: 1.5 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.tf_bubble_type = 'arabic'
    props.config.questions.layout.row_spacing_mm = 4.8
    props.config.questions.layout.bubble_radius_mm = 2.0
  }

  function applyInstitute60() {
    props.config.template_id = 'YEMEN_INSTITUTE_60'
    props.config.template_name = 'نموذج المعاهد التقنية والمهنية (60 سؤال: 20 صح/خطأ + 40 متعدد)'
    props.config.institution_type = 'institute'
    props.config.display_mode = 'compact_a5'
    if (!props.config.paper) props.config.paper = {}
    props.config.paper.size = 'A5'
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 148.5
    props.config.paper.orientation = 'landscape'
    props.config.questions.metadata.num_questions = 60
    props.config.questions.sections = [
      { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'القسم الثاني: الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 60, choices: ['1', '2', '3', '4'], mark: 1.5 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.tf_bubble_type = 'arabic'
    props.config.questions.layout.row_spacing_mm = 4.8
    props.config.questions.layout.bubble_radius_mm = 2.0
    props.config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني'
    props.config.header.sub_title = 'المعهد التقني الصناعي — إدارة الاختبارات والتقويم الآلي'
    props.config.header.exam_stage_title = 'اختبارات الدبلوم التقني والتدريب المهني'
    props.config.header.primary_color = '#00796B'
  }

  function applyInstitute80() {
    props.config.template_id = 'YEMEN_INSTITUTE_80'
    props.config.template_name = 'نموذج الدبلوم التقني الشامل للمعاهد (80 سؤال)'
    props.config.institution_type = 'institute'
    props.config.display_mode = 'compact_a5'
    if (!props.config.paper) props.config.paper = {}
    props.config.paper.size = 'A5'
    props.config.paper.width_mm = 210
    props.config.paper.height_mm = 148.5
    props.config.paper.orientation = 'landscape'
    props.config.questions.metadata.num_questions = 80
    props.config.questions.sections = [
      { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'القسم الثاني: الاختيار من متعدد', type: 'mcq', from_q: 21, to_q: 80, choices: ['1', '2', '3', '4'], mark: 1 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.tf_bubble_type = 'arabic'
    props.config.questions.layout.row_spacing_mm = 4.2
    props.config.questions.layout.bubble_radius_mm = 1.8
    props.config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني'
    props.config.header.sub_title = 'المعهد التقني التجاري — كنترول الاختبارات'
    props.config.header.primary_color = '#00796B'
  }

  function applyUniversity180() {
    props.config.template_id = 'YEMEN_UNIVERSITY_180'
    props.config.template_name = 'نموذج الجامعات اليمنية العام (180 سؤال - 4 أعمدة)'
    props.config.questions.metadata.num_questions = 180
    props.config.questions.sections = [
      { id: 'sec1', title: 'أسئلة الاختبار الشامل', type: 'mcq', from_q: 1, to_q: 180, choices: ['1', '2', '3', '4'], mark: 1 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.row_spacing_mm = 4.2
    props.config.questions.layout.bubble_radius_mm = 1.7
  }

  function applyGeneral100() {
    props.config.template_id = 'GENERAL_100'
    props.config.template_name = 'النموذج المعياري العام (100 سؤال)'
    props.config.questions.metadata.num_questions = 100
    props.config.questions.sections = [
      { id: 'sec1', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 1, to_q: 100, choices: ['1', '2', '3', '4'], mark: 1 },
    ]
    props.config.questions.layout.columns_count = 4
    props.config.questions.layout.choices_count = 4
    props.config.questions.layout.bubble_type = 'numbers'
    props.config.questions.layout.row_spacing_mm = 4.6
    props.config.questions.layout.bubble_radius_mm = 1.75
  }

  function autoFitRowSpacing() {
    const total = totalQuestionsCount.value
    const cols = props.config.questions.layout.columns_count || 4
    const rows = Math.ceil(total / cols)
    const availableH = 175
    const optimal = Math.max(3.8, Math.min(6.0, Math.floor((availableH / rows) * 10) / 10))
    props.config.questions.layout.row_spacing_mm = optimal
  }

  return {
    sectionsList,
    totalQuestionsCount,
    totalExamMarks,
    tfCount,
    mcqCount,
    tfSection,
    mcqSection,
    isYemeniPreset,
    hasDuplicateSectionTypes,
    getSectionCount,
    updateSectionCount,
    onSectionTypeChange,
    adjustTfCount,
    setTfCount,
    adjustMcqCount,
    setMcqCount,
    addNewSection,
    removeSection,
    moveSection,
    mergeToStandardTwoSections,
    applyMinistry40,
    applyYemeniMinistry50,
    applyMinistry60,
    applyInstitute60,
    applyInstitute80,
    applyUniversity180,
    applyGeneral100,
    autoFitRowSpacing,
  }
}
