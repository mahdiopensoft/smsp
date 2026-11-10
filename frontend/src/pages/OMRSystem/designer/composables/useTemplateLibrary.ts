import { ref, computed, watch } from 'vue'

export function useTemplateLibrary(props: { templates: any[] }) {
  const viewMode = ref<'table' | 'cards'>('table')
  const searchQuery = ref('')
  const tableSearch = ref('')
  const filterCategory = ref('all')
  const filterQuestions = ref('all')
  const filterActive = ref<any>('all')

  const showDeleteDialog = ref(false)
  const templateToDelete = ref<any>(null)
  const isDeleting = ref(false)

  const categoryOptions = [
    { id: 'all', name: 'كافة الأنواع (الكل)', text: 'كافة الأنواع (الكل)', value: 'all', title: 'كافة الأنواع (الكل)' },
    { id: 'ministry', name: 'وزارة التربية والتعليم (المدارس)', text: 'وزارة التربية والتعليم (المدارس)', value: 'ministry', title: 'وزارة التربية والتعليم (المدارس)' },
    { id: 'university', name: 'الجامعات والتعليم العالي', text: 'الجامعات والتعليم العالي', value: 'university', title: 'الجامعات والتعليم العالي' },
    { id: 'institute', name: 'المعاهد والتدريب المهني', text: 'المعاهد والتدريب المهني', value: 'institute', title: 'المعاهد والتدريب المهني' },
    { id: 'custom', name: 'قوالب مخصصة', text: 'قوالب مخصصة', value: 'custom', title: 'قوالب مخصصة' },
  ]

  const questionCountOptions = [
    { id: 'all', name: 'كافة السعات', text: 'كافة السعات', value: 'all', title: 'كافة السعات' },
    { id: 20, name: '20 سؤال (سريع)', text: '20 سؤال (سريع)', value: 20, title: '20 سؤال (سريع)' },
    { id: 40, name: '40 سؤال (معياري)', text: '40 سؤال (معياري)', value: 40, title: '40 سؤال (معياري)' },
    { id: 50, name: '50 سؤال (وزاري رسمي)', text: '50 سؤال (وزاري رسمي)', value: 50, title: '50 سؤال (وزاري رسمي)' },
    { id: 60, name: '60 سؤال (فصلي)', text: '60 سؤال (فصلي)', value: 60, title: '60 سؤال (فصلي)' },
    { id: 100, name: '100 سؤال (نصف سنوي)', text: '100 سؤال (نصف سنوي)', value: 100, title: '100 سؤال (نصف سنوي)' },
    { id: 180, name: '180 سؤال (جامعي شامل)', text: '180 سؤال (جامعي شامل)', value: 180, title: '180 سؤال (جامعي شامل)' },
  ]

  const activeOptions = [
    { id: 'all', name: 'كافة الحالات (الكل)', text: 'كافة الحالات (الكل)', value: 'all', title: 'كافة الحالات (الكل)' },
    { id: true, name: 'مفعل', text: 'مفعل', value: true, title: 'مفعل' },
    { id: false, name: 'غير مفعل', text: 'غير مفعل', value: false, title: 'غير مفعل' },
  ]

  const headers = computed(() => [
    { title: '#', key: 'id', sortable: true, align: 'center', width: '70px' },
    { title: 'اسم القالب والنموذج', key: 'name', sortable: true },
    { title: 'نوع القالب / المؤسسة', key: 'category', sortable: true },
    { title: 'عدد الأسئلة', key: 'total_mcq', sortable: true, align: 'center' },
    { title: 'التخطيط (أعمدة / خيارات)', key: 'layout', sortable: false, align: 'center' },
    { title: 'المقاس', key: 'paper_size', sortable: false, align: 'center' },
    { title: 'الإصدار', key: 'version', sortable: true, align: 'center' },
    { title: 'الحالة', key: 'is_active', sortable: true, align: 'center' },
  ])

  function getQuestionsCount(item: any) {
    return (
      item?.total_mcq ??
      item?.template_data?.questions?.metadata?.num_questions ??
      item?.template_data?.metadata?.num_questions ??
      0
    )
  }

  function getColumnsCount(item: any) {
    return (
      item?.template_data?.questions?.layout?.columns_count ??
      item?.template_data?.metadata?.columns_count ??
      item?.template_data?.layout?.columns_count ??
      4
    )
  }

  function getChoicesCount(item: any) {
    return (
      item?.template_data?.questions?.layout?.choices_count ??
      item?.template_data?.metadata?.choices_count ??
      item?.template_data?.layout?.choices_count ??
      4
    )
  }

  function getPaperSize(item: any) {
    return (
      item?.template_data?.paper?.size ||
      item?.template_data?.metadata?.paper_size ||
      (getQuestionsCount(item) > 100 ? 'A3' : (getQuestionsCount(item) <= 40 ? 'A5' : 'A4'))
    )
  }

  function getCategoryLabel(item: any) {
    const name = item?.name || ''
    const tId = item?.template_data?.template_id || ''
    const inst = item?.institution_type || item?.template_data?.institution_type || ''
    const q = getQuestionsCount(item)

    if (inst === 'institute' || name.includes('المعاهد') || name.includes('معهد') || name.includes('التعليم الفني') || name.includes('التدريب') || tId.includes('INSTITUTE')) {
      return 'المعاهد والتدريب المهني'
    }
    if (inst === 'university' || q === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')) {
      return 'الجامعات والتعليم العالي'
    }
    if (name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tId === 'YEMEN_MINISTRY_50' || q === 50) {
      return 'وزارة التربية والتعليم'
    }
    return 'قالب مخصص'
  }

  function getCategoryColor(item: any) {
    const name = item?.name || ''
    const tId = item?.template_data?.template_id || ''
    const inst = item?.institution_type || item?.template_data?.institution_type || ''
    const q = getQuestionsCount(item)

    if (inst === 'institute' || name.includes('المعاهد') || name.includes('معهد') || name.includes('التعليم الفني') || name.includes('التدريب') || tId.includes('INSTITUTE')) {
      return 'teal'
    }
    if (inst === 'university' || q === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')) {
      return 'indigo'
    }
    if (name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tId === 'YEMEN_MINISTRY_50' || q === 50) {
      return 'primary'
    }
    return 'secondary'
  }

  function getCategoryIcon(item: any) {
    const name = item?.name || ''
    const tId = item?.template_data?.template_id || ''
    const inst = item?.institution_type || item?.template_data?.institution_type || ''
    const q = getQuestionsCount(item)

    if (inst === 'institute' || name.includes('المعاهد') || name.includes('معهد') || name.includes('التعليم الفني') || name.includes('التدريب') || tId.includes('INSTITUTE')) {
      return 'mdi-certificate-outline'
    }
    if (inst === 'university' || q === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')) {
      return 'mdi-domain'
    }
    if (name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tId === 'YEMEN_MINISTRY_50' || q === 50) {
      return 'mdi-school-outline'
    }
    return 'mdi-tune-variant'
  }

  const filteredTemplates = computed(() => {
    let list = props.templates || []

    if (filterCategory.value === 'ministry') {
      list = list.filter((t) => {
        const name = t.name || ''
        const tid = t.template_data?.template_id || ''
        const q = getQuestionsCount(t)
        return name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tid === 'YEMEN_MINISTRY_50' || tid.includes('YEMEN_MINISTRY') || q === 50
      })
    } else if (filterCategory.value === 'university') {
      list = list.filter((t) => {
        const q = getQuestionsCount(t)
        return q === 180 || t.name?.includes('الجامعات') || t.name?.includes('التعليم العالي')
      })
    } else if (filterCategory.value === 'institute') {
      list = list.filter((t) => {
        const name = t.name || ''
        const tid = t.template_data?.template_id || ''
        const inst = t.institution_type || t.template_data?.institution_type || ''
        return inst === 'institute' || name.includes('المعاهد') || name.includes('معهد') || name.includes('التعليم الفني') || name.includes('التدريب') || tid.includes('INSTITUTE')
      })
    } else if (filterCategory.value === 'custom') {
      list = list.filter((t) => {
        const q = getQuestionsCount(t)
        const name = t.name || ''
        return q !== 50 && q !== 180 && !name.includes('معهد') && !name.includes('التربية') && !name.includes('الجامعات')
      })
    }

    if (filterQuestions.value && filterQuestions.value !== 'all') {
      const targetQ = Number(filterQuestions.value)
      list = list.filter((t) => getQuestionsCount(t) === targetQ)
    }

    if (filterActive.value !== null && filterActive.value !== undefined && filterActive.value !== 'all') {
      const targetActive = filterActive.value === true || filterActive.value === 'true'
      list = list.filter((t) => {
        const active = t.is_active !== false
        return active === targetActive
      })
    }

    const effectiveSearch = (tableSearch.value || searchQuery.value || '').toLowerCase().trim()
    if (effectiveSearch) {
      list = list.filter((t) =>
        (t.name && t.name.toLowerCase().includes(effectiveSearch)) ||
        (t.description && t.description.toLowerCase().includes(effectiveSearch)) ||
        (String(t.id).includes(effectiveSearch)) ||
        (t.template_data?.template_id && t.template_data.template_id.toLowerCase().includes(effectiveSearch)) ||
        (t.template_data?.header?.exam_name && t.template_data.header.exam_name.toLowerCase().includes(effectiveSearch)) ||
        (t.subject_name && t.subject_name.toLowerCase().includes(effectiveSearch))
      )
    }

    return list
  })

  const libraryPage = ref(1)
  const libraryPageSize = ref(10)
  const libraryTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: {
      count: 0,
      total: 0,
      num_pages: 1,
      current_page: 1,
    },
  })

  async function getData(params: any = {}) {
    const p = params?.params || params || {}
    const page = Number(p.page) || libraryPage.value || 1
    const pageSize = Number(p.page_size) || libraryPageSize.value || 10
    libraryPage.value = page
    libraryPageSize.value = pageSize

    if (p.search !== undefined) {
      tableSearch.value = String(p.search).trim()
    }

    const all = filteredTemplates.value || []
    const total = all.length
    const numPages = Math.ceil(total / pageSize) || 1
    const validPage = Math.min(Math.max(1, page), numPages)
    const start = (validPage - 1) * pageSize

    libraryTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: total,
      pagination: {
        count: total,
        total: total,
        num_pages: numPages,
        current_page: validPage,
      },
    }
    return libraryTableItems.value
  }

  watch(filteredTemplates, () => {
    libraryPage.value = 1
    getData({ page: 1, page_size: libraryPageSize.value })
  }, { immediate: true })

  const tableItems = computed(() => libraryTableItems.value)

  function applyFilters() {}

  function resetFilters() {
    searchQuery.value = ''
    tableSearch.value = ''
    filterCategory.value = 'all'
    filterQuestions.value = 'all'
    filterActive.value = 'all'
  }

  function confirmDeleteTemplate(t: any) {
    templateToDelete.value = t
    showDeleteDialog.value = true
  }

  return {
    viewMode,
    searchQuery,
    filterCategory,
    filterQuestions,
    filterActive,
    showDeleteDialog,
    templateToDelete,
    isDeleting,
    categoryOptions,
    questionCountOptions,
    activeOptions,
    headers,
    filteredTemplates,
    tableItems,
    getData,
    applyFilters,
    resetFilters,
    getQuestionsCount,
    getColumnsCount,
    getChoicesCount,
    getPaperSize,
    getCategoryLabel,
    getCategoryColor,
    getCategoryIcon,
    confirmDeleteTemplate,
  }
}
