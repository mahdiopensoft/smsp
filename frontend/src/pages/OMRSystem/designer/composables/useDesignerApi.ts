import { ref } from 'vue'
import api from '@/services/omr/client.js'
import { getProfileById } from './useInstitutionProfiles'

export function useDesignerApi() {
  const savedTemplatesList = ref<any[]>([])
  const isLoadingTemplates = ref(false)
  const isSaving = ref(false)
  const linkedExam = ref<any | null>(null)

  const showToast = ref(false)
  const toastMsg = ref('')
  const toastType = ref<'success' | 'error'>('success')

  function notify(msg: string, type: 'success' | 'error' = 'success') {
    toastMsg.value = msg
    toastType.value = type
    showToast.value = true
  }

  function extractErrorMessage(e: any): string {
    if (e.response?.data) {
      const d = e.response.data
      if (typeof d === 'string') return d
      if (d.message) return d.message
      if (d.error) return d.error
      if (d.detail) return d.detail
      if (d.non_field_errors) {
        return Array.isArray(d.non_field_errors)
          ? d.non_field_errors.join(', ')
          : String(d.non_field_errors)
      }
      const firstKey = Object.keys(d)[0]
      if (firstKey && Array.isArray(d[firstKey])) {
        return `${firstKey}: ${d[firstKey].join(', ')}`
      }
    }
    return e.message || 'حدث خطأ غير متوقع'
  }

  async function fetchSavedTemplates() {
    isLoadingTemplates.value = true
    try {
      const resp = await api.get('/api/templates-engine/', { params: { all: true, page_size: 1000 } })
      if (resp.status === 200) {
        const raw = resp.data
        const list: any[] = Array.isArray(raw) ? raw : (raw.results || raw.data || [])
        savedTemplatesList.value = list.map((t: any) => {
          const td = t.template_data || {}
          const qMeta = td.questions?.metadata || td.metadata || {}
          const qLayout = td.questions?.layout || td.layout || {}
          return {
            ...t,
            total_mcq: t.total_mcq ?? qMeta.num_questions ?? 0,
            template_data: td.template_id ? td : {
              ...td,
              template_id: td.template_id || t.name,
              metadata: {
                num_questions: qMeta.num_questions ?? t.total_mcq ?? 0,
                columns_count: qLayout.columns_count ?? 4,
                choices_count: qLayout.choices_count ?? 4,
                academic_year: td.metadata?.academic_year || '',
              },
              header: td.header || {},
            },
          }
        })
      }
    } catch (e: any) {
      notify('فشل في جلب قائمة القوالب: ' + extractErrorMessage(e), 'error')
    } finally {
      isLoadingTemplates.value = false
    }
  }

  async function saveNewTemplate(formData: any, config: any, savedDbId: { value: any }) {
    isSaving.value = true
    try {
      config.template_name = formData.name.trim()
      config.version = formData.version?.trim() || '1.0'
      config.description = formData.description?.trim() || ''
      if (config.header) {
        config.header.exam_name = formData.subject_name?.trim() || formData.name.trim()
      }

      if (!config.paper) {
        config.paper = { size: 'A4', width_mm: 210, height_mm: 297, dpi: 300, orientation: 'portrait' }
      }

      const payload = {
        name: config.template_name,
        version: config.version,
        description: config.description,
        paper_width_mm: Number(config.paper.width_mm) || 210,
        paper_height_mm: Number(config.paper.height_mm) || 297,
        dpi: Number(config.paper.dpi) || 300,
        template_data: JSON.parse(JSON.stringify(config)),
      }

      const resp = await api.post('/api/templates-engine/', payload)
      if (resp.status === 201 || resp.status === 200) {
        const saved = resp.data?.data || resp.data
        savedDbId.value = saved.id
        config.template_name = saved.name || config.template_name
        config.version = saved.version || config.version
        notify(`تم حفظ وتوثيق القالب «${config.template_name}» (إصدار ${config.version}) بنجاح!`)
        await fetchSavedTemplates()
        return true
      }
    } catch (e: any) {
      notify('خطأ أثناء حفظ القالب: ' + extractErrorMessage(e), 'error')
      return false
    } finally {
      isSaving.value = false
    }
    return false
  }

  async function updateTemplate(config: any, templateId: number | string) {
    if (!templateId) return false
    isSaving.value = true
    try {
      if (!config.paper) {
        config.paper = { size: 'A4', width_mm: 210, height_mm: 297, dpi: 300, orientation: 'portrait' }
      }
      const payload = {
        name: config.template_name,
        version: config.version || '1.0',
        description: config.description || '',
        paper_width_mm: Number(config.paper.width_mm) || 210,
        paper_height_mm: Number(config.paper.height_mm) || 297,
        dpi: Number(config.paper.dpi) || 300,
        template_data: JSON.parse(JSON.stringify(config)),
      }
      try {
        await api.put(`/api/templates-engine/${templateId}/`, payload)
      } catch {
        await api.patch(`/api/templates-engine/${templateId}/`, payload)
      }
      notify(`تم تحديث وحفظ القالب «${config.template_name}» بنجاح!`)
      await fetchSavedTemplates()
      return true
    } catch (e: any) {
      notify('خطأ أثناء تحديث القالب: ' + extractErrorMessage(e), 'error')
      return false
    } finally {
      isSaving.value = false
    }
  }

  async function deleteTemplateById(id: number | string) {
    try {
      await api.delete(`/api/templates-engine/${id}/`)
      notify('تم حذف القالب بنجاح')
      await fetchSavedTemplates()
      return true
    } catch (e: any) {
      notify('خطأ أثناء حذف القالب: ' + extractErrorMessage(e), 'error')
      return false
    }
  }

  async function importExamSpecs(examId: string | number, config: any, savedDbId: { value: any }) {
    try {
      notify('جاري استيراد مواصفات الاختبار من المولد وبناء القالب ديناميكياً...', 'success')
      const resp = await api.get(`/api/omr/exam-linking/${examId}/`)
      if (resp.status === 200 && resp.data?.success) {
        const examData = resp.data.exam || {}
        const versions = resp.data.versions || []
        const students = resp.data.registered_students || []

        let questionsCount = examData.totalQuestions || 50
        let sections: any[] = []

        if (versions.length > 0 && versions[0].questions?.length) {
          questionsCount = versions[0].questions.length
          const qList = versions[0].questions
          let tfCount = 0
          let mcqCount = 0
          qList.forEach((q: any) => {
            const typeStr = String(q.questionType || '').toLowerCase()
            if (typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')) {
              tfCount++
            } else {
              mcqCount++
            }
          })

          if (tfCount > 0 && mcqCount > 0) {
            sections = [
              { id: 'sec1', title: 'القسم الأول: صح وخطأ', from_q: 1, to_q: tfCount, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
              { id: 'sec2', title: 'القسم الثاني: الاختيار من متعدد', from_q: tfCount + 1, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2, type: 'mcq' },
            ]
          } else if (tfCount > 0 && mcqCount === 0) {
            sections = [
              { id: 'sec1', title: 'أسئلة الصح والخطأ', from_q: 1, to_q: questionsCount, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
            ]
          } else {
            sections = [
              { id: 'sec1', title: 'أسئلة الاختيار من متعدد', from_q: 1, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2, type: 'mcq' },
            ]
          }
        } else {
          const half = Math.min(20, Math.floor(questionsCount / 2))
          sections = [
            { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: half, choices: ['صح', 'خطأ'], mark: 1, type: 'true_false' },
            { id: 'sec2', title: 'اختيار من متعدد', from_q: half + 1, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2, type: 'mcq' },
          ]
        }

        config.template_id = `EXAM_${examData.uniqueCode || examId}`
        config.template_name = `قالب ${examData.title || 'الاختبار'}`
        config.description = `قالب OMR مولد تلقائياً للاختبار: ${examData.title || ''} (${questionsCount} سؤالاً)`
        
        // Dynamically resolve institution profile (school, university, institute)
        const rawInstType = String(examData.institution_type || '').toLowerCase()
        const instType = rawInstType.includes('univ') || rawInstType.includes('جامع')
          ? 'university'
          : rawInstType.includes('inst') || rawInstType.includes('معهد') || rawInstType.includes('مهني') || rawInstType.includes('تقني')
          ? 'institute'
          : 'school'
        
        const prof = getProfileById(instType)
        config.institution_type = prof.id
        config.display_mode = (prof.id === 'university' && questionsCount > 100) ? 'university_180' : 'compact_a5'

        if (config.header) {
          config.header.institution_name = prof.defaults.institution_name
          config.header.sub_title = examData.center_name ? `${examData.center_name} — ${prof.defaults.sub_title}` : prof.defaults.sub_title
          config.header.exam_stage_title = examData.stage_name || prof.defaults.exam_stage_title
          config.header.exam_name = examData.subject_name || examData.title || prof.defaults.exam_name
          config.header.governorate = examData.governorate_name || examData.governorate || prof.defaults.governorate
          config.header.directorate = examData.directorate_name || examData.directorate || prof.defaults.directorate
          config.header.primary_color = prof.defaults.primary_color || config.header.primary_color

          if (students.length > 0) {
            config.header.student_name = students[0].student_name
            config.header.seat_number = students[0].seat_number
            config.header.center_name = students[0].school_name || prof.defaults.center_name
            config.header.serial_number = students[0].secret_number || '101'
          } else {
            config.header.student_name = '................................'
            config.header.seat_number = '418485'
            config.header.center_name = examData.directorate || prof.defaults.center_name
          }
        }

        if (config.metadata) {
          config.metadata.academic_year = examData.year_name || prof.defaults.academic_year
        }

        // Dynamically compute optimal columns and geometry for OpenCV AI accuracy
        const cols = questionsCount <= 30 ? 3 : (questionsCount <= 120 ? 4 : 5)
        config.questions.metadata.num_questions = questionsCount
        config.questions.sections = sections
        config.questions.layout.columns_count = cols
        config.questions.layout.choices_count = 4

        const rows = Math.ceil(questionsCount / cols)
        if (config.display_mode === 'compact_a5') {
          config.questions.layout.row_spacing_mm = Math.min(5.4, Math.max(3.8, Math.floor((78 / rows) * 10) / 10))
          config.questions.layout.bubble_radius_mm = Math.min(2.1, Math.max(1.5, Math.floor((config.questions.layout.row_spacing_mm * 0.42) * 10) / 10))
        } else {
          config.questions.layout.row_spacing_mm = Math.min(6.5, Math.max(4.0, Math.floor((175 / rows) * 10) / 10))
          config.questions.layout.bubble_radius_mm = Math.min(2.2, Math.max(1.6, Math.floor((config.questions.layout.row_spacing_mm * 0.42) * 10) / 10))
        }

        if (students.length > 0 && students[0].seat_number) {
          config.barcode.value = String(students[0].seat_number)
        } else {
          config.barcode.value = examData.uniqueCode || '41848501164148'
        }

        savedDbId.value = null
        linkedExam.value = examData
        notify(`تم استيراد مواصفات الاختبار «${examData.title}» وبناء القالب (${questionsCount} سؤالاً) ديناميكياً!`)
        return true
      }
    } catch (err: any) {
      notify('تعذر استيراد بيانات الاختبار إلى المصمم: ' + extractErrorMessage(err), 'error')
      return false
    }
    return false
  }

  return {
    savedTemplatesList,
    isLoadingTemplates,
    isSaving,
    linkedExam,
    showToast,
    toastMsg,
    toastType,
    notify,
    extractErrorMessage,
    fetchSavedTemplates,
    saveNewTemplate,
    updateTemplate,
    deleteTemplateById,
    importExamSpecs,
  }
}
