import { ref, computed } from 'vue'

export function usePrintRegistryFilters(options: { onFilterChange?: () => void } = {}) {
  const triggerChange = () => {
    if (options.onFilterChange) {
      options.onFilterChange()
    }
  }

  // ── Unified Tripartite Filters State ──
  const filterInstitutionType = ref<string>('school')
  const institutionType = ref<string>('school')
  const filterGovernorate = ref<any>(null)
  const filterDirectorate = ref<any>(null)
  const filterOrganization = ref<any>(null)

  // 🏫 School Filters (المرحلة، الصف والمسار، المادة)
  const filterStage = ref<any>(null)
  const filterClassTrack = ref<any>(null)
  const filterSubject = ref<any>(null)

  // 🎓 University Filters (الكلية، القسم، التخصص، المقرر)
  const filterCollege = ref<any>(null)
  const filterDepartment = ref<any>(null)
  const filterSpecialization = ref<any>(null)
  const filterSemesterSubject = ref<any>(null)

  // 🏢 Institute Filters (المجال المهني، نظام التعليم، التخصص، المادة)
  const filterInstituteField = ref<any>(null)
  const filterInstituteEducationSystem = ref<any>(null)
  const filterInstituteSpecialization = ref<any>(null)
  const filterInstituteSubject = ref<any>(null)

  const masterSearchQuery = ref<string>('')

  const getEffectiveInstitutionType = () => {
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      return filterInstitutionType.value
    }
    if (filterInstitutionType.value === 'all') {
      return undefined
    }
    if (institutionType.value && institutionType.value !== 'all') {
      return institutionType.value
    }
    return undefined
  }

  const isSchoolFilter = computed(() => {
    return !filterInstitutionType.value || filterInstitutionType.value === 'all' || filterInstitutionType.value === 'school'
  })

  const isOrgDisabled = computed(() => {
    if (isSchoolFilter.value) {
      return !filterGovernorate.value || !filterDirectorate.value
    }
    return !filterGovernorate.value
  })

  const orgFieldLabel = computed(() => {
    if (filterInstitutionType.value === 'university') return 'الجامعة / الكلية'
    if (filterInstitutionType.value === 'institute') return 'المعهد / مركز التدريب'
    return 'المدرسة / المركز الامتحاني'
  })

  const orgPlaceholder = computed(() => {
    if (isSchoolFilter.value) {
      if (!filterGovernorate.value) return 'اختر المحافظة أولاً'
      if (!filterDirectorate.value) return 'اختر المديرية أولاً'
      return 'المدرسة / المركز الامتحاني'
    }
    return filterGovernorate.value ? 'الجامعة / الكلية / المعهد' : 'اختر المحافظة أولاً'
  })

  const orgParam = computed(() => {
    const p: Record<string, any> = {}
    if (filterGovernorate.value) p.governorate = filterGovernorate.value
    if (filterDirectorate.value) p.directorate = filterDirectorate.value
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      p.institution_type = filterInstitutionType.value
    }
    return Object.keys(p).length > 0 ? p : null
  })

  const subjectFilterParam = computed(() => {
    const p: Record<string, any> = {}
    if (filterClassTrack.value) p.class_track = filterClassTrack.value
    if (filterStage.value) p.stage = filterStage.value
    return Object.keys(p).length > 0 ? p : null
  })

  const instituteSpecParam = computed(() => {
    const p: Record<string, any> = {}
    if (filterInstituteField.value) p.field = filterInstituteField.value
    if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
    return Object.keys(p).length ? p : null
  })

  const instituteSubjectParam = computed(() => {
    if (filterInstituteField.value) return { field: filterInstituteField.value }
    return null
  })

  // ── Change Handlers ──
  const onInstitutionTypeChange = () => {
    institutionType.value = filterInstitutionType.value
    filterGovernorate.value = null
    filterDirectorate.value = null
    filterOrganization.value = null
    filterStage.value = null
    filterClassTrack.value = null
    filterSubject.value = null
    filterCollege.value = null
    filterDepartment.value = null
    filterSpecialization.value = null
    filterSemesterSubject.value = null
    filterInstituteField.value = null
    filterInstituteEducationSystem.value = null
    filterInstituteSpecialization.value = null
    filterInstituteSubject.value = null
    triggerChange()
  }

  const onGovernorateChange = () => {
    filterDirectorate.value = null
    filterOrganization.value = null
    triggerChange()
  }

  const onDirectorateChange = () => {
    filterOrganization.value = null
    triggerChange()
  }

  const onOrganizationChange = () => {
    triggerChange()
  }

  const onStageChange = () => {
    filterClassTrack.value = null
    filterSubject.value = null
    triggerChange()
  }

  const onClassTrackChange = () => {
    filterSubject.value = null
    triggerChange()
  }

  const onCollegeChange = () => {
    filterDepartment.value = null
    filterSpecialization.value = null
    filterSemesterSubject.value = null
    triggerChange()
  }

  const onDepartmentChange = () => {
    filterSpecialization.value = null
    filterSemesterSubject.value = null
    triggerChange()
  }

  const onSpecializationChange = () => {
    filterSemesterSubject.value = null
    triggerChange()
  }

  const onInstituteFieldChange = () => {
    filterInstituteEducationSystem.value = null
    filterInstituteSpecialization.value = null
    filterInstituteSubject.value = null
    triggerChange()
  }

  const onInstituteEducationSystemChange = () => {
    filterInstituteSpecialization.value = null
    filterInstituteSubject.value = null
    triggerChange()
  }

  const resetUnifiedFilters = async () => {
    filterInstitutionType.value = 'all'
    institutionType.value = 'all'
    filterGovernorate.value = null
    filterDirectorate.value = null
    filterOrganization.value = null
    filterStage.value = null
    filterClassTrack.value = null
    filterSubject.value = null
    filterCollege.value = null
    filterDepartment.value = null
    filterSpecialization.value = null
    filterSemesterSubject.value = null
    filterInstituteField.value = null
    filterInstituteEducationSystem.value = null
    filterInstituteSpecialization.value = null
    filterInstituteSubject.value = null
    masterSearchQuery.value = ''
    triggerChange()
  }

  return {
    filterInstitutionType,
    institutionType,
    filterGovernorate,
    filterDirectorate,
    filterOrganization,
    filterStage,
    filterClassTrack,
    filterSubject,
    filterCollege,
    filterDepartment,
    filterSpecialization,
    filterSemesterSubject,
    filterInstituteField,
    filterInstituteEducationSystem,
    filterInstituteSpecialization,
    filterInstituteSubject,
    masterSearchQuery,
    getEffectiveInstitutionType,
    isSchoolFilter,
    isOrgDisabled,
    orgFieldLabel,
    orgPlaceholder,
    orgParam,
    subjectFilterParam,
    instituteSpecParam,
    instituteSubjectParam,
    onInstitutionTypeChange,
    onGovernorateChange,
    onDirectorateChange,
    onOrganizationChange,
    onStageChange,
    onClassTrackChange,
    onCollegeChange,
    onDepartmentChange,
    onSpecializationChange,
    onInstituteFieldChange,
    onInstituteEducationSystemChange,
    resetUnifiedFilters,
  }
}
