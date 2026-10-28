<template>
  <div class="qb-human-review-v4 pa-4 pa-md-6">
    <!-- 1. MASTER VIEW: الهيكل الإداري ومراجعة أوراق الاختبارات -->
    <ReviewMasterView
      v-if="currentView === 'master'"
      v-model:institution-type="institutionType"
      v-model:master-tab="masterTab"
      v-model:selected-office-id="selectedOfficeId"
      v-model:selected-directorate-id="selectedDirectorateId"
      v-model:selected-school-id="selectedSchoolId"
      v-model:selected-subject-id="selectedSubjectId"
      :sector-options="sectorOptions"
      :all-offices-list="allOfficesList"
      :offices-list="officesList"
      :directorates-options="directoratesOptions"
      :schools-options="schoolsOptions"
      :subjects-list="subjectsList"
      :loading-master="loadingMaster"
      :filtered-offices-table="filteredOfficesTable"
      :filtered-directorates-table="filteredDirectoratesTable"
      :filtered-schools-table="filteredSchoolsTable"
      :filtered-master-exams-table="filteredMasterExamsTable"
      @refresh="refreshMasterData"
      @reset="resetHierarchyFilters"
      @select-exam="openExamReviewDetail"
    />

    <!-- 2. DETAIL VIEW: كشف فحص وتدقيق أوراق الطلاب التفصيلي -->
    <ReviewDetailView
      v-else
      :institution-type="institutionType"
      :active-exam="activeExam"
      :active-breadcrumb="activeBreadcrumb"
      :detail-table-items="detailTableItems"
      :loading-detail="loadingDetail"
      :detail-stats="detailStats"
      :detail-headers="detailHeaders"
      :directorates-options="detailDirectoratesOptions"
      :schools-options="detailSchoolsOptions"
      :status-options="statusOptions"
      :get-detail-data="getDetailData"
      @return-to-master="returnToMaster"
      @review-sheet="openReviewModal"
      @approve-sheet="approveSheet"
      @filter-change="handleDetailFilterChange"
      @reset-filters="resetDetailFilters"
    />

    <!-- 3. REVIEW MODAL: نافذة المراجعة والتدقيق المتقدمة -->
    <ReviewAuditDialog
      v-model="reviewDialog"
      :active-review-sheet="activeReviewSheet"
      :has-prev-sheet="hasPrevSheet"
      :has-next-sheet="hasNextSheet"
      :approving-loading="approvingLoading"
      :overriding-loading="overridingLoading"
      @prev-sheet="prevSheet"
      @next-sheet="nextSheet"
      @approve-sheet="approveActiveSheet"
      @override-question="handleOverrideQuestion"
    />
  </div>
</template>

<script>
import { humanReviewAPI, verificationAPI } from '@/services/omr/endpoints.js'
import api from '@/services/api'
import ReviewMasterView from './review/ReviewMasterView.vue'
import ReviewDetailView from './review/ReviewDetailView.vue'
import ReviewAuditDialog from './review/ReviewAuditDialog.vue'
import { detailHeaders } from './review/useReviewMaster'

export default {
  name: 'OMRHumanReviewView',
  components: { ReviewMasterView, ReviewDetailView, ReviewAuditDialog },

  data() {
    return {
      currentView: 'master',
      institutionType: 'school',
      masterTab: 'exams',
      selectedOfficeId: null,
      selectedDirectorateId: null,
      selectedSchoolId: null,
      selectedSubjectId: null,
      allOfficesList: [],
      officesList: [],
      directoratesList: [],
      schoolsList: [],
      subjectsList: [],
      examsList: [],
      educationalOrgs: [],
      loadingMaster: false,
      detailHeaders,

      sectorOptions: [
        { title: 'التعليم العام (مدرسي)', value: 'school', icon: 'mdi-school' },
        { title: 'التعليم الجامعي (أكاديمي)', value: 'university', icon: 'mdi-domain' },
        { title: 'التعليم الفني والمهني (معاهد)', value: 'institute', icon: 'mdi-tools' },
      ],

      // Detail State
      activeExam: null,
      selectedExamId: null,
      loadingDetail: false,
      detailSheets: [],
      detailStats: { pendingReview: 0, ambiguousSheets: 0, verifiedSheets: 0, totalSheets: 0 },
      detailPagination: { count: 0, current_page: 1, num_pages: 1, page_size: 10 },
      detailActiveMetricFilter: 'all',
      detailFilterDirectorate: 'all',
      detailFilterSchool: 'all',
      detailFilterStatus: 'all',
      detailSearchQuery: '',
      availableDirectoratesForExam: [],
      availableSchoolsForExam: [],

      activeBreadcrumb: { institution_type_name: 'التعليم العام', office_name: '', directorate_name: '', school_name: '', exam_title: '' },
      statusOptions: [
        { title: 'كافة الحالات', value: 'all' },
        { title: 'تتطلب تدقيق يدوي', value: 'pending' },
        { title: 'معتمدة ومحققة', value: 'verified' },
      ],

      // Dialog State
      reviewDialog: false,
      activeReviewSheet: null,
      currentSheetIndex: 0,
      overridingLoading: '',
      approvingLoading: false,
    }
  },

  computed: {
    directoratesOptions() {
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      return officeIds.length > 0 ? (this.directoratesList || []).filter(d => officeIds.includes(Number(d.office_id))) : (this.directoratesList || [])
    },

    schoolsOptions() {
      let list = this.schoolsList || []
      if (this.institutionType !== 'all') list = list.filter(s => !s.institution_type || s.institution_type === this.institutionType)
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      if (dirIds.length > 0) return list.filter(s => dirIds.includes(Number(s.directorate_id)))
      if (officeIds.length > 0) return list.filter(s => officeIds.includes(Number(s.office_id)))
      return list
    },

    filteredOfficesTable() {
      const selIds = this.normalizeIds(this.selectedOfficeId)
      return selIds.length > 0 ? (this.officesList || []).filter(o => selIds.includes(Number(o.id))) : (this.officesList || [])
    },

    filteredDirectoratesTable() {
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      return officeIds.length > 0 ? (this.directoratesList || []).filter(d => officeIds.includes(Number(d.office_id))) : (this.directoratesList || [])
    },

    filteredSchoolsTable() { return this.schoolsOptions || [] },
    filteredMasterExamsTable() { return this.examsList || [] },

    detailDirectoratesOptions() {
      const dirs = (this.availableDirectoratesForExam || [])
        .map(d => typeof d === 'string' ? d : (d.value !== 'all' ? (d.value || d.title) : null))
        .filter(d => d && d !== 'all')
      return [{ title: 'كافة المديريات (الكل)', value: 'all' }, ...dirs.map(d => ({ title: d, value: d }))]
    },

    detailSchoolsOptions() {
      const schools = (this.availableSchoolsForExam || [])
        .map(s => typeof s === 'string' ? s : (s.value !== 'all' ? (s.value || s.title) : null))
        .filter(s => s && s !== 'all')
      return [{ title: 'كافة المدارس والمراكز (الكل)', value: 'all' }, ...schools.map(s => ({ title: s, value: s }))]
    },

    detailTableItems() {
      return { results: this.detailSheets, count: this.detailPagination.count || this.detailSheets.length, pagination: this.detailPagination }
    },

    hasPrevSheet() { return this.currentSheetIndex > 0 },
    hasNextSheet() { return this.currentSheetIndex < this.detailSheets.length - 1 },
  },

  async mounted() {
    await this.loadEducationalHierarchy()
    await this.refreshMasterData()

    const examParam = this.$route?.query?.exam
    if (examParam) {
      const exObj = (this.examsList || []).find(e => String(e.id) === String(examParam))
      if (exObj) {
        this.openExamReviewDetail(exObj)
      } else {
        this.selectedExamId = Number(examParam)
        this.currentView = 'detail'
        this.fetchDetailSchools()
        this.fetchDetailSheets()
      }
    }
  },

  methods: {
    normalizeIds(val) {
      if (!val) return []
      if (Array.isArray(val)) {
        return val.map(x => (typeof x === 'object' && x !== null) ? Number(x.id ?? x.value ?? x.raw?.id) : Number(x)).filter(n => !isNaN(n) && n > 0)
      }
      const num = Number(typeof val === 'object' && val !== null ? (val.id ?? val.value) : val)
      return (!isNaN(num) && num > 0) ? [num] : []
    },

    async loadEducationalHierarchy() {
      try {
        const res = await api.get('/api/exams/distributions/educational-hierarchy/')
        this.educationalOrgs = res.data?.data || []
      } catch (err) {
        console.error('Error fetching educational hierarchy:', err)
      }
    },

    async refreshMasterData() {
      this.loadingMaster = true
      try {
        const officeIds = this.normalizeIds(this.selectedOfficeId)
        const dirIds = this.normalizeIds(this.selectedDirectorateId)
        const schoolIds = this.normalizeIds(this.selectedSchoolId)

        const baseParams = {
          institution_type: this.institutionType !== 'all' ? this.institutionType : undefined,
          subject: this.selectedSubjectId || undefined,
        }
        const officeParams = { ...baseParams }
        if (officeIds.length > 0) officeParams.office_id = officeIds.join(',')

        const dirParams = { ...officeParams }
        if (dirIds.length > 0) dirParams.directorate_id = dirIds.join(',')

        const schoolParams = { ...dirParams }
        if (schoolIds.length > 0) schoolParams.school_id = schoolIds.join(',')

        const [allOfficesRes, officesRes, directoratesRes, schoolsRes, examsRes] = await Promise.all([
          (!this.allOfficesList || !this.allOfficesList.length)
            ? verificationAPI.getByOffice(baseParams).catch(() => ({ data: { results: [] } }))
            : Promise.resolve({ data: { results: this.allOfficesList } }),
          verificationAPI.getByOffice(officeParams).catch(() => ({ data: { results: [] } })),
          verificationAPI.getByDirectorate(dirParams).catch(() => ({ data: { results: [] } })),
          verificationAPI.getBySchool(schoolParams).catch(() => ({ data: { results: [] } })),
          verificationAPI.list(schoolParams).catch(() => ({ data: { results: [] } }))
        ])
        if (!this.allOfficesList || !this.allOfficesList.length) {
          this.allOfficesList = allOfficesRes.data?.results || []
        }
        this.officesList = officesRes.data?.results || []
        this.directoratesList = directoratesRes.data?.results || []
        this.schoolsList = schoolsRes.data?.results || []
        this.examsList = examsRes.data?.results || []
      } catch (err) {
        console.error('Error refreshing master data:', err)
      } finally {
        this.loadingMaster = false
      }
    },

    resetHierarchyFilters() {
      this.institutionType = 'school'
      this.selectedOfficeId = null
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.selectedSubjectId = null
      this.masterTab = 'exams'
      this.refreshMasterData()
    },

    async openExamReviewDetail(exam) {
      this.activeExam = exam
      this.selectedExamId = exam.id
      this.detailActiveMetricFilter = 'all'
      this.detailFilterStatus = 'all'
      this.detailSearchQuery = ''
      this.detailFilterDirectorate = 'all'
      this.detailFilterSchool = 'all'

      this.activeBreadcrumb = {
        institution_type_name: this.institutionType === 'university' ? 'التعليم الجامعي' : (this.institutionType === 'institute' ? 'التعليم الفني' : 'التعليم العام'),
        office_name: exam.governorate_name || exam.office_name || '',
        directorate_name: 'كافة المديريات',
        school_name: exam.schools_count === 1 ? (exam.school_name || '') : (exam.schools_count > 1 ? `كافة المدارس (${exam.schools_count})` : ''),
        exam_title: exam.title,
      }
      this.currentView = 'detail'
      await this.fetchDetailSchools()
      await this.fetchDetailSheets()
    },

    async fetchDetailSchools() {
      try {
        const res = await verificationAPI.retrieve(this.selectedExamId, { page_size: 1 })
        const filterOpts = res.data?.filter_options || {}
        this.availableDirectoratesForExam = filterOpts.directorates || []
        this.availableSchoolsForExam = filterOpts.schools || []
      } catch (e) {
        this.availableDirectoratesForExam = []
        this.availableSchoolsForExam = []
      }
    },

    returnToMaster() {
      this.currentView = 'master'
      this.activeExam = null
      this.refreshMasterData()
    },

    handleDetailFilterChange(filters) {
      this.detailActiveMetricFilter = filters.metricFilter
      this.detailFilterDirectorate = filters.directorate
      this.detailFilterSchool = filters.school
      this.detailFilterStatus = filters.status
      this.detailSearchQuery = filters.search
      this.fetchDetailSheets()
    },

    resetDetailFilters() {
      this.detailFilterDirectorate = 'all'
      this.detailFilterSchool = 'all'
      this.detailFilterStatus = 'all'
      this.detailActiveMetricFilter = 'all'
      this.detailSearchQuery = ''
      this.fetchDetailSheets()
    },

    async getDetailData(params = {}) {
      return await this.fetchDetailSheets(params)
    },

    async fetchDetailSheets(params = {}) {
      this.loadingDetail = true
      try {
        const p = params?.params || params || {}
        const pageNum = Number(p.page) || this.detailPagination.current_page || 1
        const pageSizeNum = Number(p.page_size) || this.detailPagination.page_size || 10

        const queryParams = {
          page: pageNum,
          page_size: pageSizeNum,
          exam: this.selectedExamId || undefined,
          directorate: (this.detailFilterDirectorate && this.detailFilterDirectorate !== 'all') ? this.detailFilterDirectorate : undefined,
          school: (this.detailFilterSchool && this.detailFilterSchool !== 'all') ? this.detailFilterSchool : undefined,
          status: (this.detailFilterStatus && this.detailFilterStatus !== 'all') ? this.detailFilterStatus : undefined,
          metric_filter: (this.detailActiveMetricFilter && this.detailActiveMetricFilter !== 'all') ? this.detailActiveMetricFilter : undefined,
          search: p.search || this.detailSearchQuery || undefined,
        }

        const [statsRes, listRes] = await Promise.all([
          humanReviewAPI.getStats(queryParams),
          humanReviewAPI.list(queryParams)
        ])

        this.detailStats = statsRes?.data || {}
        const results = listRes?.data?.results || listRes?.data || []
        this.detailSheets = Array.isArray(results) ? results : []

        if (listRes?.data?.pagination) {
          this.detailPagination = listRes.data.pagination
        } else {
          this.detailPagination = {
            count: this.detailSheets.length,
            total: this.detailSheets.length,
            current_page: pageNum,
            num_pages: Math.ceil(this.detailSheets.length / pageSizeNum) || 1,
            page_size: pageSizeNum,
          }
        }
        return this.detailTableItems
      } catch (err) {
        console.error('Failed to load human review detail data', err)
        return { results: [], count: 0 }
      } finally {
        this.loadingDetail = false
      }
    },

    async approveSheet(sheet) {
      try {
        await humanReviewAPI.approveReview(sheet.id)
        this.$alert?.('success', { message: 'تم اعتماد ومصادقة النتيجة بنجاح' })
        await this.fetchDetailSheets()
      } catch (err) {
        this.$alert?.('errorData', { message: 'فشل اعتماد الورقة' })
        console.error(err)
      }
    },

    openReviewModal(sheet) {
      const idx = this.detailSheets.findIndex(s => s.id === sheet.id)
      this.currentSheetIndex = idx >= 0 ? idx : 0
      this.activeReviewSheet = { ...sheet }
      this.reviewDialog = true
    },

    prevSheet() {
      if (this.hasPrevSheet) {
        this.currentSheetIndex -= 1
        this.activeReviewSheet = { ...this.detailSheets[this.currentSheetIndex] }
      }
    },

    nextSheet() {
      if (this.hasNextSheet) {
        this.currentSheetIndex += 1
        this.activeReviewSheet = { ...this.detailSheets[this.currentSheetIndex] }
      }
    },

    async handleOverrideQuestion({ question, choice }) {
      if (!this.activeReviewSheet) return
      this.overridingLoading = `${question.question_number}-${choice}`
      try {
        const res = await humanReviewAPI.overrideQuestion(this.activeReviewSheet.id, {
          question_number: question.question_number,
          marked_choice: choice
        })
        const updated = res.data?.sheet || res.data?.data || res.data
        if (updated) {
          this.activeReviewSheet = { ...this.activeReviewSheet, ...updated }
          const idx = this.detailSheets.findIndex(s => s.id === this.activeReviewSheet.id)
          if (idx !== -1) {
            this.detailSheets[idx] = { ...this.detailSheets[idx], ...updated }
          }
        }
        this.$alert?.('success', { message: 'تم تعديل الإجابة وتوثيق التدقيق بنجاح' })
      } catch (err) {
        this.$alert?.('errorData', { message: 'فشل تعديل الإجابة' })
        console.error(err)
      } finally {
        this.overridingLoading = ''
      }
    },

    async approveActiveSheet(sheet) {
      this.approvingLoading = true
      try {
        await humanReviewAPI.approveReview(sheet.id)
        this.$alert?.('success', { message: 'تم اعتماد ومصادقة النتيجة بنجاح' })
        if (this.hasNextSheet) {
          this.nextSheet()
        } else {
          this.reviewDialog = false
        }
        await this.fetchDetailSheets()
      } catch (err) {
        this.$alert?.('errorData', { message: 'فشل اعتماد الورقة' })
        console.error(err)
      } finally {
        this.approvingLoading = false
      }
    },
  }
}
</script>

<style scoped>
.qb-human-review-v4 {
  background-color: rgb(var(--v-theme-background));
  min-height: 100vh;
}
</style>
