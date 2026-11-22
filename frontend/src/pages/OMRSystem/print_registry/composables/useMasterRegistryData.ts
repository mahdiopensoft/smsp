import { ref, computed, watch, type Ref } from 'vue'
import api from '@/services/omr/client.js'
import { gradebookAPI } from '@/services/omr/endpoints'
import { safeApiFetch, isRequestCanceled } from '../utils/safeApiFetch'

export interface UseMasterRegistryDataOptions {
  filters: any
  institutionType: Ref<string>
  getEffectiveInstitutionType: () => string
  selectedExamId?: Ref<any>
  batches?: Ref<any[]>
  examsList?: Ref<any[]>
  batchPrintNotification: Ref<{ show: boolean; message: string; color: string }>
  loadSavedPrintOrders: (force?: boolean) => Promise<any>
  getExamMasterData: (params?: any) => Promise<any>
}

export function useMasterRegistryData(options: UseMasterRegistryDataOptions) {
  const {
    filters,
    institutionType,
    getEffectiveInstitutionType,
    selectedExamId = ref(null),
    examsList = ref([]),
    batchPrintNotification,
    loadSavedPrintOrders,
    getExamMasterData,
  } = options

  const {
    filterGovernorate,
    filterDirectorate,
    filterOrganization,
    filterSubject,
    filterSemesterSubject,
    filterInstituteSubject,
    filterStage,
    filterClassTrack,
    filterCollege,
    filterDepartment,
    filterSpecialization,
    masterSearchQuery,
  } = filters

  const masterTab = ref('schools')
  const loadingMaster = ref(false)
  const masterDataStatus = ref<'idle' | 'loading' | 'success' | 'empty' | 'error'>('idle')
  const masterDataError = ref<any>(null)

  const allOfficesList = ref<any[]>([])
  const officesList = ref<any[]>([])
  const selectedOfficeId = ref<any>([])
  const selectedOfficeName = ref('')

  const directoratesList = ref<any[]>([])
  const selectedDirectorateId = ref<any>([])
  const selectedDirectorateName = ref('')

  const schoolsList = ref<any[]>([])
  const selectedSchoolId = ref<any>([])
  const selectedSchoolName = ref('')

  const selectedSubjectId = ref<any>(null)
  const selectedSubjectName = ref('')
  const subjectsList = ref<any[]>([])

  const masterExamsList = ref<any[]>([])
  const batches = options.batches || ref<any[]>([])
  const loadingBatches = ref(false)

  const schoolExamsDialog = ref(false)
  const selectedSchoolDialogItem = ref<any>(null)

  const sectorOptions = [
    { title: 'التعليم العام (المدرسي)', value: 'school', icon: 'mdi-school' },
    { title: 'التعليم الجامعي (كليات وجامعات)', value: 'university', icon: 'mdi-domain' },
    { title: 'التعليم الفني والمهني (معاهد)', value: 'institute', icon: 'mdi-tools' },
  ]

  // Master Table Headers
  const officeMasterHeaders = [
    { title: "مكتب التربية والتعليم (المحافظة)", key: "office_name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
    { title: "المديريات", key: "directorates_count", sortable: true, align: "center", width: "95px" },
    { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
    { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
    { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
    { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
    { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
    { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
    { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
  ]

  const directorateMasterHeaders = [
    { title: "إدارة التربية والتعليم (المديرية)", key: "name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
    { title: "المكتب التابع له", key: "office_name", sortable: true, align: "center", width: "180px" },
    { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
    { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
    { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
    { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
    { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
    { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
    { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
  ]

  const schoolMasterHeaders = [
    { title: "المدرسة / المركز الامتحاني", key: "name", sortable: true, align: "start", width: "320px", minWidth: "280px" },
    { title: "نوع المؤسسة", key: "institution_type", sortable: true, align: "center", width: "105px" },
    { title: "المحافظة والمديرية", key: "directorate_name", sortable: true, align: "center", width: "170px" },
    { title: "المادة الدراسية", key: "subject_name", sortable: true, align: "center", width: "160px" },
    { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "105px" },
    { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
    { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "115px" },
    { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "120px" },
    { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "115px" },
    { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "190px" },
  ]

  const schoolExamsHeaders = [
    { title: "رمز الاختبار", key: "code", sortable: true, align: "center", width: "135px" },
    { title: "عنوان الاختبار والمواصفات", key: "title", sortable: true, align: "start" },
    { title: "المادة الدراسية", key: "subject", sortable: true, align: "center", width: "120px" },
    { title: "طلاب المركز", key: "students_count", sortable: true, align: "center", width: "105px" },
    { title: "النماذج المخصصة للطلاب وتوزيعها", key: "versions", sortable: false, align: "center", width: "230px" },
    { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "110px" },
  ]

  const examMasterHeaders = [
    { title: "رمز الاختبار", key: "uniqueCode", sortable: true, align: "center", width: "125px" },
    { title: "عنوان الاختبار والمادة", key: "title", sortable: true, align: "start", width: "290px", minWidth: "240px" },
    { title: "المدارس المشاركة", key: "schools_count", sortable: true, align: "center", width: "115px" },
    { title: "المقيدون", key: "total_registered", sortable: true, align: "center", width: "95px" },
    { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "105px" },
    { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "115px" },
    { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
    { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "140px" },
  ]

  const registryMasterHeaders = [
    { title: "رقم الدفعة", key: "batch_id", sortable: true, align: "center", width: "170px" },
    { title: "عنوان الاختبار", key: "exam_title", sortable: true, align: "start", width: "300px", minWidth: "260px" },
    { title: "عدد الأوراق", key: "total_sheets", sortable: true, align: "center", width: "110px" },
    { title: "تاريخ الطباعة", key: "printed_at", sortable: true, align: "center", width: "160px" },
    { title: "المسؤول", key: "printed_by_name", sortable: true, align: "center", width: "140px" },
    { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "120px" },
  ]

  // Master KPI Computeds
  const kpiTotalPrinted = computed(() => {
    return masterExamsList.value.reduce((acc, e) => acc + (Number(e.printed_count) || 0), 0)
  })

  const kpiTotalRegistered = computed(() => {
    return masterExamsList.value.reduce((acc, e) => acc + (Number(e.total_registered || e.total_students) || 0), 0)
  })

  const kpiPrintRate = computed(() => {
    if (!kpiTotalRegistered.value) return 0
    return Math.round((kpiTotalPrinted.value / kpiTotalRegistered.value) * 1000) / 10
  })

  const kpiSchoolsCount = computed(() => {
    return schoolsList.value.length
  })

  const kpiExamsCount = computed(() => {
    return masterExamsList.value.length
  })

  const normalizeIds = (val: any): number[] => {
    if (!val) return []
    if (Array.isArray(val)) {
      return val.map(x => {
        if (typeof x === 'object' && x !== null) {
          return Number(x.id ?? x.value ?? x.raw?.id)
        }
        return Number(x)
      }).filter(n => !isNaN(n) && n > 0)
    }
    if (typeof val === 'object' && val !== null) {
      const id = Number(val.id ?? val.value ?? val.raw?.id)
      return (!isNaN(id) && id > 0) ? [id] : []
    }
    if (typeof val === 'string' && val.includes(',')) {
      return val.split(',').map(s => Number(s.trim())).filter(n => !isNaN(n) && n > 0)
    }
    const num = Number(val)
    return (!isNaN(num) && num > 0) ? [num] : []
  }

  // Autocomplete Options
  const directoratesOptions = computed(() => {
    const officeIds = normalizeIds(selectedOfficeId.value)
    if (officeIds.length > 0) {
      const oObjs = (officesList.value || []).filter(o => 
        officeIds.includes(Number(o.id)) ||
        officeIds.includes(Number(o.core_org_id)) ||
        officeIds.includes(Number(o.office_id)) ||
        officeIds.includes(Number(o.governorate_id)) ||
        officeIds.includes(Number(o.fk_governorate_id))
      )
      const allOffIds = [...officeIds, ...oObjs.map(o => Number(o.id)), ...oObjs.map(o => Number(o.office_id)), ...oObjs.map(o => Number(o.governorate_id)), ...oObjs.map(o => Number(o.fk_governorate_id))].filter(Boolean)
      return (directoratesList.value || []).filter(d => 
        allOffIds.includes(Number(d.office_id)) ||
        allOffIds.includes(Number(d.governorate_id)) ||
        allOffIds.includes(Number(d.fk_governorate_id))
      )
    }
    return directoratesList.value || []
  })

  const schoolsOptions = computed(() => {
    let list = schoolsList.value || []
    const effType = getEffectiveInstitutionType()
    if (effType) {
      list = list.filter(s => !s.institution_type || s.institution_type === effType)
    }
    const dirIds = normalizeIds(selectedDirectorateId.value)
    const officeIds = normalizeIds(selectedOfficeId.value)

    if (dirIds.length > 0) {
      const dObjs = (directoratesList.value || []).filter(d => 
        dirIds.includes(Number(d.id)) ||
        dirIds.includes(Number(d.directorate_id)) ||
        dirIds.includes(Number(d.fk_directorate_id))
      )
      const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
      const allDirIds = [...dirIds, ...dObjs.map(d => Number(d.id)), ...dObjs.map(d => Number(d.directorate_id)), ...dObjs.map(d => Number(d.fk_directorate_id))].filter(Boolean)
      list = list.filter(s => 
        allDirIds.includes(Number(s.directorate_id)) ||
        allDirIds.includes(Number(s.fk_directorate_id)) ||
        dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
      )
    } else if (officeIds.length > 0) {
      const oObjs = (officesList.value || []).filter(o => 
        officeIds.includes(Number(o.id)) ||
        officeIds.includes(Number(o.core_org_id)) ||
        officeIds.includes(Number(o.office_id)) ||
        officeIds.includes(Number(o.governorate_id)) ||
        officeIds.includes(Number(o.fk_governorate_id))
      )
      const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
      const allOffIds = [...officeIds, ...oObjs.map(o => Number(o.id)), ...oObjs.map(o => Number(o.office_id)), ...oObjs.map(o => Number(o.governorate_id)), ...oObjs.map(o => Number(o.fk_governorate_id))].filter(Boolean)
      list = list.filter(s => 
        allOffIds.includes(Number(s.office_id)) ||
        allOffIds.includes(Number(s.governorate_id)) ||
        allOffIds.includes(Number(s.fk_governorate_id)) ||
        oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
      )
    }
    return list
  })

  // Unified Objects for <auto-list> integration
  const sectorOptionsObjects = computed(() => {
    return (sectorOptions || []).map(opt => ({
      id: opt.value,
      value: opt.value,
      name: opt.title,
      title: opt.title,
    }))
  })

  const officesObjects = computed(() => {
    return (officesList.value || []).map(o => ({
      id: o.id,
      value: o.id,
      name: o.office_name || o.name_ar || o.name,
      title: o.office_name || o.name_ar || o.name,
    }))
  })

  const directoratesObjectsFormatted = computed(() => {
    return (directoratesOptions.value || []).map(d => ({
      id: d.id,
      value: d.id,
      name: d.name || d.name_ar,
      title: d.name || d.name_ar,
    }))
  })

  const schoolsObjectsFormatted = computed(() => {
    return (schoolsOptions.value || []).map(s => ({
      id: s.id,
      value: s.id,
      name: s.name || s.school_name || s.name_ar,
      title: s.name || s.school_name || s.name_ar,
    }))
  })

  const examsObjectsFormatted = computed(() => {
    return (examsList.value || []).map(e => ({
      id: e.id,
      value: e.id,
      name: `${e.title || e.name || 'اختبار'} (${e.subject_name || 'عام'} - ${e.uniqueCode || ''})`,
      title: `${e.title || e.name || 'اختبار'} (${e.subject_name || 'عام'} - ${e.uniqueCode || ''})`,
    }))
  })

  // Filtered Master Tables Computeds
  const filteredOfficesTable = computed(() => {
    let list = officesList.value || []
    const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)
    if (effGov.length > 0) {
      list = list.filter(o => 
        effGov.includes(Number(o.id)) || 
        effGov.includes(Number(o.governorate_id)) || 
        effGov.includes(Number(o.fk_governorate_id))
      )
    }
    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
    if (effSubj) {
      list = list.filter(o => (o.exams_count || 0) > 0)
    }
    if (masterSearchQuery.value) {
      const q = masterSearchQuery.value.toLowerCase().trim()
      list = list.filter(o => 
        (o.office_name && o.office_name.toLowerCase().includes(q)) ||
        (o.governorate_name && o.governorate_name.toLowerCase().includes(q))
      )
    }
    return list
  })

  const filteredDirectoratesTable = computed(() => {
    let list = directoratesList.value || []
    const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)
    if (effGov.length > 0) {
      list = list.filter(d => 
        effGov.includes(Number(d.office_id)) || 
        effGov.includes(Number(d.governorate_id)) ||
        effGov.includes(Number(d.fk_governorate_id))
      )
    }
    const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
    if (effDir.length > 0) {
      list = list.filter(d => 
        effDir.includes(Number(d.id)) || 
        effDir.includes(Number(d.directorate_id)) || 
        effDir.includes(Number(d.fk_directorate_id))
      )
    }
    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
    if (effSubj) {
      list = list.filter(d => (d.exams_count || 0) > 0)
    }
    if (masterSearchQuery.value) {
      const q = masterSearchQuery.value.toLowerCase().trim()
      list = list.filter(d => 
        (d.name && d.name.toLowerCase().includes(q)) ||
        (d.office_name && d.office_name.toLowerCase().includes(q))
      )
    }
    return list
  })

  const filteredSchoolsTable = computed(() => {
    let list = schoolsList.value || []
    const effType = getEffectiveInstitutionType()
    if (effType) {
      list = list.filter(s => !s.institution_type || s.institution_type === effType)
    }
    const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
    const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)

    if (effDir.length > 0) {
      const dObjs = (directoratesList.value || []).filter(d => 
        effDir.includes(Number(d.id)) || 
        effDir.includes(Number(d.directorate_id)) || 
        effDir.includes(Number(d.fk_directorate_id))
      )
      const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
      list = list.filter(s => 
        effDir.includes(Number(s.directorate_id)) ||
        effDir.includes(Number(s.fk_directorate_id)) ||
        dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
      )
    } else if (effGov.length > 0) {
      const oObjs = (officesList.value || []).filter(o => 
        effGov.includes(Number(o.id)) || 
        effGov.includes(Number(o.governorate_id)) || 
        effGov.includes(Number(o.fk_governorate_id))
      )
      const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
      list = list.filter(s => 
        effGov.includes(Number(s.office_id)) || 
        effGov.includes(Number(s.governorate_id)) || 
        effGov.includes(Number(s.fk_governorate_id)) ||
        oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
      )
    }
    const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
    if (effOrg.length > 0) {
      list = list.filter(s => effOrg.includes(Number(s.id)) || effOrg.includes(Number(s.organization_id)))
    }
    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
    if (effSubj) {
      const sObj = subjectsList.value.find(s => Number(s.id) === Number(effSubj))
      const sName = sObj?.name?.trim() || sObj?.name_ar?.trim()
      list = list.filter(s => {
        if (!sName) return true
        if (s.subjects && Array.isArray(s.subjects)) {
          return s.subjects.some(sub => sub === sName || sub.includes(sName))
        }
        return s.subject_name === sName || (s.subject_name && s.subject_name.includes(sName))
      })
    }
    if (masterSearchQuery.value) {
      const q = masterSearchQuery.value.toLowerCase().trim()
      list = list.filter(s => 
        (s.name && s.name.toLowerCase().includes(q)) ||
        (s.directorate_name && s.directorate_name.toLowerCase().includes(q)) ||
        (s.governorate_name && s.governorate_name.toLowerCase().includes(q)) ||
        (s.subject_name && s.subject_name.toLowerCase().includes(q))
      )
    }
    return list
  })

  const filteredMasterExamsTable = computed(() => {
    let list = masterExamsList.value || []
    const effType = getEffectiveInstitutionType()
    if (effType) {
      list = list.filter(e => !e.institution_type || e.institution_type === effType)
    }
    const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
    const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
    const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)

    if (effOrg.length > 0) {
      list = list.filter(e => 
        effOrg.includes(Number(e.school_id)) || 
        effOrg.includes(Number(e.school)) || 
        effOrg.includes(Number(e.organization_id)) ||
        (e.schools && Array.isArray(e.schools) && e.schools.some(sId => effOrg.includes(Number(sId)))) ||
        !e.school_id
      )
    } else if (effDir.length > 0) {
      list = list.filter(e => effDir.includes(Number(e.directorate_id)) || effDir.includes(Number(e.directorate)))
    } else if (effGov.length > 0) {
      list = list.filter(e => effGov.includes(Number(e.governorate_id)) || effGov.includes(Number(e.office_id)) || effGov.includes(Number(e.governorate)))
    }

    if (filterStage.value) {
      list = list.filter(e => Number(e.stage_id) === Number(filterStage.value) || Number(e.stage) === Number(filterStage.value) || !e.stage_id)
    }
    if (filterClassTrack.value) {
      list = list.filter(e => Number(e.class_track_id) === Number(filterClassTrack.value) || Number(e.class_track) === Number(filterClassTrack.value))
    }

    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
    if (effSubj) {
      const sObj = subjectsList.value.find(s => Number(s.id) === Number(effSubj))
      const sName = sObj?.name?.trim() || sObj?.name_ar?.trim()
      list = list.filter(e => 
        Number(e.subject_id) === Number(effSubj) || 
        Number(e.subject) === Number(effSubj) ||
        (sName && e.subject_name && (e.subject_name === sName || e.subject_name.includes(sName)))
      )
    }
    if (masterSearchQuery.value) {
      const q = masterSearchQuery.value.toLowerCase().trim()
      list = list.filter(e => 
        (e.title && e.title.toLowerCase().includes(q)) ||
        (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
        (e.subject_name && e.subject_name.toLowerCase().includes(q)) ||
        (e.order_number && e.order_number.toLowerCase().includes(q))
      )
    }
    return list
  })

  const filteredBatchesTable = computed(() => {
    let list = batches.value || []
    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
    if (effSubj) {
      const sObj = subjectsList.value.find(s => Number(s.id) === Number(effSubj))
      const sName = sObj?.name?.trim() || sObj?.name_ar?.trim()
      list = list.filter(b => 
        Number(b.subject_id) === Number(effSubj) ||
        (sName && b.subject_name && (b.subject_name === sName || b.subject_name.includes(sName)))
      )
    }
    if (masterSearchQuery.value) {
      const q = masterSearchQuery.value.toLowerCase().trim()
      list = list.filter(b => 
        (b.batch_id && b.batch_id.toLowerCase().includes(q)) ||
        (b.exam_title && b.exam_title.toLowerCase().includes(q)) ||
        (b.exam_code && b.exam_code.toLowerCase().includes(q)) ||
        (b.subject_name && b.subject_name.toLowerCase().includes(q))
      )
    }
    return list
  })

  // Master Tables Selection State
  const selectedOfficeMasterRows = ref<any[]>([])
  const selectedDirectorateMasterRows = ref<any[]>([])
  const selectedSchoolMasterRows = ref<any[]>([])
  const selectedExamMasterRows = ref<any[]>([])
  const selectedBatchMasterRows = ref<any[]>([])

  // Master Tables Reactive State for custom-data-table
  const officeMasterTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
  })

  const getOfficeMasterData = async (params: any = {}) => {
    const p = params?.params || params || {}
    const page = p.page || 1
    const pageSize = p.page_size || 20
    const all = filteredOfficesTable.value || []
    const start = (page - 1) * pageSize
    officeMasterTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: all.length,
      pagination: {
        count: all.length,
        total: all.length,
        num_pages: Math.ceil(all.length / pageSize) || 1,
        current_page: page,
      },
    }
    return officeMasterTableItems.value
  }

  const directorateMasterTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
  })

  const getDirectorateMasterData = async (params: any = {}) => {
    const p = params?.params || params || {}
    const page = p.page || 1
    const pageSize = p.page_size || 20
    const all = filteredDirectoratesTable.value || []
    const start = (page - 1) * pageSize
    directorateMasterTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: all.length,
      pagination: {
        count: all.length,
        total: all.length,
        num_pages: Math.ceil(all.length / pageSize) || 1,
        current_page: page,
      },
    }
    return directorateMasterTableItems.value
  }

  const schoolMasterTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
  })

  const getSchoolMasterData = async (params: any = {}) => {
    const p = params?.params || params || {}
    const page = p.page || 1
    const pageSize = p.page_size || 20
    const all = filteredSchoolsTable.value || []
    const start = (page - 1) * pageSize
    schoolMasterTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: all.length,
      pagination: {
        count: all.length,
        total: all.length,
        num_pages: Math.ceil(all.length / pageSize) || 1,
        current_page: page,
      },
    }
    return schoolMasterTableItems.value
  }

  const schoolExamsPage = ref(1)
  const schoolExamsPageSize = ref(10)
  const schoolExamsTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
  })

  const getSchoolExamsData = async (params: any = {}) => {
    const p = params?.params || params || {}
    const page = Number(p.page) || schoolExamsPage.value || 1
    const pageSize = Number(p.page_size) || schoolExamsPageSize.value || 10
    schoolExamsPage.value = page
    schoolExamsPageSize.value = pageSize

    const all = selectedSchoolDialogItem.value?.exams || []
    const total = all.length
    const numPages = Math.ceil(total / pageSize) || 1
    const validPage = Math.min(Math.max(1, page), numPages)
    const start = (validPage - 1) * pageSize

    schoolExamsTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: total,
      pagination: {
        count: total,
        total: total,
        num_pages: numPages,
        current_page: validPage,
      },
    }
    return schoolExamsTableItems.value
  }

  const batchMasterTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
  })

  const getBatchMasterData = async (params: any = {}) => {
    const p = params?.params || params || {}
    const page = p.page || 1
    const pageSize = p.page_size || 20
    const all = filteredBatchesTable.value || []
    const start = (page - 1) * pageSize
    batchMasterTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: all.length,
      pagination: {
        count: all.length,
        total: all.length,
        num_pages: Math.ceil(all.length / pageSize) || 1,
        current_page: page,
      },
    }
    return batchMasterTableItems.value
  }

  // Load Subjects
  const loadSubjects = async () => {
    try {
      const res = await safeApiFetch('loadSubjects:gradebook', () => gradebookAPI.getSubjects())
      if (res.status === 'success' && res.data.length > 0) {
        subjectsList.value = res.data
        return
      }
      const acRes = await safeApiFetch('loadSubjects:academic', () => api.get('/api/academic/subjects/', { skipInterceptor: true }))
      if (acRes.status === 'success' && acRes.data.length > 0) {
        subjectsList.value = acRes.data
      } else if (res.status === 'error' && acRes.status === 'error') {
        console.warn('[OMR Registry] تعذر تحميل قائمة المواد من كلا المصدرين (gradebook & academic).')
      }
    } catch (err) {
      console.error('[OMR Registry API Error] فشل في loadSubjects:', err)
    }
  }

  let masterDataRequestId = 0
  let masterDataAbortController: AbortController | null = null

  const loadMasterData = async () => {
    if (masterDataAbortController) {
      masterDataAbortController.abort()
    }
    masterDataAbortController = new AbortController()
    const signal = masterDataAbortController.signal
    const currentRequestId = ++masterDataRequestId

    loadingMaster.value = true
    masterDataStatus.value = 'loading'
    masterDataError.value = null

    try {
      const effGov = filterGovernorate.value || (normalizeIds(selectedOfficeId.value)[0] || undefined)
      const effDir = filterDirectorate.value || (normalizeIds(selectedDirectorateId.value)[0] || undefined)
      const effOrg = filterOrganization.value || (normalizeIds(selectedSchoolId.value)[0] || undefined)
      const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value || undefined
      const effType = getEffectiveInstitutionType()

      const baseParams: any = {
        institution_type: effType,
        subject: effSubj,
        governorate: effGov,
      }
      const officeParams: any = { ...baseParams }
      if (effGov) {
        officeParams.office_id = effGov
        officeParams.governorate_id = effGov
      }

      const dirParams: any = { ...officeParams }
      if (effDir) {
        dirParams.directorate_id = effDir
      }

      const schoolParams: any = { ...dirParams }
      if (effOrg) {
        schoolParams.school_id = effOrg
        schoolParams.organization_id = effOrg
      }
      if (filterStage.value) schoolParams.stage = filterStage.value
      if (filterClassTrack.value) schoolParams.class_track = filterClassTrack.value
      if (filterCollege.value) schoolParams.college = filterCollege.value
      if (filterDepartment.value) schoolParams.department = filterDepartment.value
      if (filterSpecialization.value) schoolParams.specialization = filterSpecialization.value

      const [allOfficesRes, officesRes, directoratesRes, schoolsRes, examsRes] = await Promise.all([
        (!allOfficesList.value || !allOfficesList.value.length)
          ? safeApiFetch('loadMasterData:allOffices', () => gradebookAPI.getByOffice(baseParams, { signal }), baseParams)
          : Promise.resolve({ status: 'success', data: allOfficesList.value, count: allOfficesList.value.length, isEmpty: allOfficesList.value.length === 0, error: null } as any),
        safeApiFetch('loadMasterData:offices', () => gradebookAPI.getByOffice(officeParams, { signal }), officeParams),
        safeApiFetch('loadMasterData:directorates', () => gradebookAPI.getByDirectorate(dirParams, { signal }), dirParams),
        safeApiFetch('loadMasterData:schools', () => gradebookAPI.getBySchool(schoolParams, { signal }), schoolParams),
        safeApiFetch('loadMasterData:exams', () => gradebookAPI.list(schoolParams, { signal }), schoolParams),
      ])

      if (currentRequestId !== masterDataRequestId) {
        return
      }

      if (
        allOfficesRes.status === 'canceled' ||
        officesRes.status === 'canceled' ||
        directoratesRes.status === 'canceled' ||
        schoolsRes.status === 'canceled' ||
        examsRes.status === 'canceled'
      ) {
        return
      }

      const failures = [
        { name: 'مكاتب المحافظات', res: officesRes },
        { name: 'إدارات المديريات', res: directoratesRes },
        { name: 'المراكز الامتحانية والمدارس', res: schoolsRes },
        { name: 'الاختبارات المعتمدة', res: examsRes },
      ].filter(item => item.res.status === 'error')

      if (failures.length > 0) {
        masterDataStatus.value = 'error'
        const failedNames = failures.map(f => f.name).join('، ')
        masterDataError.value = {
          message: `تعذر جلب بيانات: ${failedNames}`,
          failedServices: failures.map(f => f.name),
          errors: failures.map(f => f.res.error),
        }
        batchPrintNotification.value = {
          show: true,
          color: 'error',
          message: `تعذر تحميل بعض بيانات الهيكل الإداري (${failedNames}). يرجى مراجعة الاتصال أو إعادة المحاولة.`,
        }
      } else {
        masterDataError.value = null
      }

      if (allOfficesRes.status === 'success' && (!allOfficesList.value || !allOfficesList.value.length)) {
        allOfficesList.value = allOfficesRes.data || []
      }
      if (officesRes.status === 'success') {
        officesList.value = officesRes.data || []
      }
      if (directoratesRes.status === 'success') {
        directoratesList.value = directoratesRes.data || []
      }
      if (schoolsRes.status === 'success') {
        schoolsList.value = schoolsRes.data || []
      }
      if (examsRes.status === 'success') {
        masterExamsList.value = examsRes.data || []
      }

      const totalCount = (officesList.value?.length || 0) + (schoolsList.value?.length || 0) + (masterExamsList.value?.length || 0)
      if (failures.length === 0) {
        masterDataStatus.value = totalCount === 0 ? 'empty' : 'success'
      }

      await loadSavedPrintOrders(true)

      if (currentRequestId === masterDataRequestId) {
        getOfficeMasterData()
        getDirectorateMasterData()
        getSchoolMasterData()
        getExamMasterData()
        getBatchMasterData()
      }
    } catch (err: any) {
      if (!isRequestCanceled(err)) {
        masterDataStatus.value = 'error'
        masterDataError.value = {
          message: 'حدث خطأ غير متوقع أثناء جلب بيانات الهيكل الإداري',
          error: err?.message || err,
        }
        console.error('[OMR Registry API Error] خطأ غير متوقع في loadMasterData:', err)
      }
    } finally {
      if (currentRequestId === masterDataRequestId) {
        loadingMaster.value = false
      }
    }
  }

  // Drill down helpers
  const drillDownToOffice = (office: any) => {
    selectedOfficeId.value = office.id
    selectedOfficeName.value = office.office_name
    masterTab.value = 'directorates'
  }

  const drillDownToDirectorate = (dir: any) => {
    selectedDirectorateId.value = dir.id
    selectedDirectorateName.value = dir.name
    if (dir.office_id && !selectedOfficeId.value) {
      selectedOfficeId.value = dir.office_id
      selectedOfficeName.value = dir.office_name
    }
    masterTab.value = 'schools'
  }

  const openSchoolExamsDialog = (item: any) => {
    selectedSchoolDialogItem.value = item
    schoolExamsDialog.value = true
    getSchoolExamsData()
  }

  const onSchoolFilterChange = (schoolId: any) => {
    selectedSchoolId.value = schoolId || []
    loadMasterData()
  }

  // Watchers to synchronize tables
  watch(filteredOfficesTable, () => {
    getOfficeMasterData()
  }, { immediate: true })

  watch(filteredDirectoratesTable, () => {
    getDirectorateMasterData()
  }, { immediate: true })

  watch(filteredSchoolsTable, () => {
    getSchoolMasterData()
  }, { immediate: true })

  watch(filteredBatchesTable, () => {
    getBatchMasterData()
  }, { immediate: true })

  watch(masterTab, (tab) => {
    if (tab === 'offices') getOfficeMasterData()
    else if (tab === 'directorates') getDirectorateMasterData()
    else if (tab === 'schools') getSchoolMasterData()
    else if (tab === 'exams') getExamMasterData()
    else if (tab === 'registry') getBatchMasterData()
  })

  return {
    masterTab,
    loadingMaster,
    masterDataStatus,
    masterDataError,
    allOfficesList,
    officesList,
    selectedOfficeId,
    selectedOfficeName,
    directoratesList,
    selectedDirectorateId,
    selectedDirectorateName,
    schoolsList,
    selectedSchoolId,
    selectedSchoolName,
    selectedSubjectId,
    selectedSubjectName,
    subjectsList,
    masterExamsList,
    batches,
    loadingBatches,
    schoolExamsDialog,
    selectedSchoolDialogItem,
    sectorOptions,
    officeMasterHeaders,
    directorateMasterHeaders,
    schoolMasterHeaders,
    schoolExamsHeaders,
    examMasterHeaders,
    registryMasterHeaders,
    kpiTotalPrinted,
    kpiTotalRegistered,
    kpiPrintRate,
    kpiSchoolsCount,
    kpiExamsCount,
    normalizeIds,
    directoratesOptions,
    schoolsOptions,
    sectorOptionsObjects,
    officesObjects,
    directoratesObjectsFormatted,
    schoolsObjectsFormatted,
    examsObjectsFormatted,
    filteredOfficesTable,
    filteredDirectoratesTable,
    filteredSchoolsTable,
    filteredMasterExamsTable,
    filteredBatchesTable,
    selectedOfficeMasterRows,
    selectedDirectorateMasterRows,
    selectedSchoolMasterRows,
    selectedExamMasterRows,
    selectedBatchMasterRows,
    officeMasterTableItems,
    getOfficeMasterData,
    directorateMasterTableItems,
    getDirectorateMasterData,
    schoolMasterTableItems,
    getSchoolMasterData,
    schoolExamsPage,
    schoolExamsPageSize,
    schoolExamsTableItems,
    getSchoolExamsData,
    batchMasterTableItems,
    getBatchMasterData,
    loadSubjects,
    loadMasterData,
    drillDownToOffice,
    drillDownToDirectorate,
    openSchoolExamsDialog,
    onSchoolFilterChange,
  }
}
