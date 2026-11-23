<template>
  <div class="master-view-container">
    <!-- ── شريط التصفية الهيكلي الموحد ── -->
    <ReviewMasterFilters
      :institution-type="institutionType"
      :sector-options="sectorOptions"
      :selected-office-id="selectedOfficeId"
      :selected-directorate-id="selectedDirectorateId"
      :selected-school-id="selectedSchoolId"
      :selected-subject-id="selectedSubjectId"
      :all-offices-list="allOfficesList"
      :offices-list="officesList"
      :directorates-options="directoratesOptions"
      :schools-options="schoolsOptions"
      :subjects-list="subjectsList"
      :loading-master="loadingMaster"
      @update:institution-type="$emit('update:institutionType', $event)"
      @update:selected-office-id="$emit('update:selectedOfficeId', $event)"
      @update:selected-directorate-id="$emit('update:selectedDirectorateId', $event)"
      @update:selected-school-id="$emit('update:selectedSchoolId', $event)"
      @update:selected-subject-id="$emit('update:selectedSubjectId', $event)"
      @refresh="$emit('refresh')"
      @reset="$emit('reset')"
    />

    <!-- ── تبويبات الاستعراض الهيكلي الأربعة ── -->
    <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1 bg-surface border">
      <div class="d-flex align-center flex-wrap gap-2 px-4 pt-3 border-b">
        <v-tabs v-model="currentTab" color="primary" density="compact">
          <v-tab v-if="institutionType === 'school'" value="offices" class="font-weight-bold">
            <v-icon start size="18">mdi-office-building-outline</v-icon>
            مكاتب التربية والتعليم ({{ filteredOffices.length }})
          </v-tab>
          <v-tab v-if="institutionType === 'school'" value="directorates" class="font-weight-bold">
            <v-icon start size="18">mdi-map-marker-radius-outline</v-icon>
            إدارات التربية بالمديريات ({{ filteredDirectorates.length }})
          </v-tab>
          <v-tab value="schools" class="font-weight-bold">
            <v-icon start size="18">{{ institutionType === 'university' ? 'mdi-domain' : (institutionType === 'institute' ? 'mdi-tools' : 'mdi-school-outline') }}</v-icon>
            {{ institutionType === 'university' ? 'الجامعات والكليات' : (institutionType === 'institute' ? 'المعاهد والمراكز' : 'المراكز الامتحانية والمدارس') }} ({{ filteredSchools.length }})
          </v-tab>
          <v-tab value="exams" class="font-weight-bold">
            <v-icon start size="18">mdi-file-document-check-outline</v-icon>
            الاختبارات الأكاديمية والتدقيق ({{ filteredExams.length }})
          </v-tab>
        </v-tabs>
      </div>

      <v-window v-model="currentTab">
        <!-- 1. تبويب مكاتب التربية بالمحافظات -->
        <v-window-item value="offices" v-if="institutionType === 'school'">
          <custom-data-table
            :items="officeTableItems"
            :getData="getOfficeData"
            :headers="officeMasterHeaders"
            :customLoading="loadingMaster"
            :hasFilter="false"
            :log="false"
            :restore="false"
            :numbering="true"
            :showSelect="false"
          
        :actionList="(item) => ([ { label: 'عرض المديريات', icon: 'arrow-down-right', color: 'primary', onClick: () => onDrillDownOffice(item) }, { label: 'عرض الاختبارات', icon: 'file-document-check-outline', color: 'indigo', onClick: () => onOpenOfficeExams(item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
            <template v-slot:item-slot="{ item, key }">
              <template v-if="key === 'office_name'">
                <div class="py-1" style="min-width: 200px;">
                  <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.office_name }}</div>
                  <div class="text-caption text-medium-emphasis">المحافظة: {{ item.governorate_name }}</div>
                </div>
              </template>
              <template v-else-if="key === 'scanned_count'">
                <span class="font-mono font-weight-bold text-body-2">{{ item.scanned_count ?? 0 }} ورقة</span>
              </template>
              <template v-else-if="key === 'needs_review_count'">
                <span class="font-mono font-weight-bold text-body-2" :class="(item.needs_review_count || 0) > 0 ? 'text-warning-darken-2' : 'text-success'">
                  {{ item.needs_review_count || 0 }} ورقة
                </span>
              </template>
              <template v-else-if="key === 'completed_count'">
                <span class="font-mono font-weight-bold text-body-2 text-success">{{ item.completed_count || 0 }} معتمدة</span>
              </template>
            </template>
          </custom-data-table>
        </v-window-item>

        <!-- 2. تبويب إدارات التربية بالمديريات -->
        <v-window-item value="directorates" v-if="institutionType === 'school'">
          <custom-data-table
            :items="directorateTableItems"
            :getData="getDirectorateData"
            :headers="directorateMasterHeaders"
            :customLoading="loadingMaster"
            :hasFilter="false"
            :log="false"
            :restore="false"
            :numbering="true"
            :showSelect="false"
          
        :actionList="(item) => ([ { label: 'عرض المدارس', icon: 'arrow-down-right', color: 'teal', onClick: () => onDrillDownDirectorate(item) }, { label: 'عرض الاختبارات', icon: 'file-document-check-outline', color: 'primary', onClick: () => onOpenDirectorateExams(item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
            <template v-slot:item-slot="{ item, key }">
              <template v-if="key === 'name'">
                <div class="py-1" style="min-width: 200px;">
                  <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.name }}</div>
                  <div class="text-caption text-medium-emphasis">{{ item.office_name }}</div>
                </div>
              </template>
              <template v-else-if="key === 'scanned_count'">
                <span class="font-mono font-weight-bold text-body-2">{{ item.scanned_count ?? 0 }} ورقة</span>
              </template>
              <template v-else-if="key === 'needs_review_count'">
                <span class="font-mono font-weight-bold text-body-2" :class="(item.needs_review_count || 0) > 0 ? 'text-warning-darken-2' : 'text-success'">
                  {{ item.needs_review_count || 0 }} ورقة
                </span>
              </template>
            </template>
          </custom-data-table>
        </v-window-item>

        <!-- 3. تبويب المدارس والمراكز -->
        <v-window-item value="schools">
          <custom-data-table
            :items="schoolTableItems"
            :getData="getSchoolData"
            :headers="schoolMasterHeaders"
            :customLoading="loadingMaster"
            :hasFilter="false"
            :log="false"
            :restore="false"
            :numbering="true"
            :showSelect="false"
          
        :actionList="(item) => ([ { label: 'عرض الاختبارات', icon: 'file-document-check-outline', color: 'primary', onClick: () => onOpenSchoolExams(item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
            <template v-slot:item-slot="{ item, key }">
              <template v-if="key === 'name'">
                <div class="py-1" style="min-width: 200px;">
                  <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.name }}</div>
                  <div class="text-caption text-medium-emphasis">{{ item.directorate_name || item.governorate_name || '' }}</div>
                </div>
              </template>
              <template v-else-if="key === 'scanned_count'">
                <span class="font-mono font-weight-bold text-body-2">{{ item.scanned_count ?? 0 }} ورقة</span>
              </template>
              <template v-else-if="key === 'needs_review_count'">
                <span class="font-mono font-weight-bold text-body-2" :class="(item.needs_review_count || 0) > 0 ? 'text-warning-darken-2' : 'text-success'">
                  {{ item.needs_review_count || 0 }} ورقة
                </span>
              </template>
            </template>
          </custom-data-table>
        </v-window-item>

        <!-- 4. تبويب الاختبارات الأكاديمية والتدقيق -->
        <v-window-item value="exams">
          <custom-data-table
            :items="examTableItems"
            :getData="getExamData"
            :headers="examMasterHeaders"
            :customLoading="loadingMaster"
            :hasFilter="false"
            :log="false"
            :restore="false"
            :numbering="true"
            :showSelect="false"
          
        :actionList="(item) => ([ { label: 'فحص وتدقيق أوراق الاختبار', icon: 'shield-search', color: 'primary', onClick: () => $emit('select-exam', item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
            <template v-slot:item-slot="{ item, key }">
              <template v-if="key === 'title' || key === 'exam_title'">
                <div class="py-1" style="min-width: 220px;">
                  <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.title }}</div>
                  <div class="text-caption text-medium-emphasis mt-0.5">
                    <span class="font-mono">{{ item.uniqueCode || item.code }}</span> • {{ item.subject_name }}
                  </div>
                </div>
              </template>
              <template v-else-if="key === 'total_scanned'">
                <span class="font-mono font-weight-bold text-body-2">{{ item.total_scanned || item.scanned_count || 0 }} ورقة</span>
              </template>
              <template v-else-if="key === 'needs_review_count'">
                <span class="font-mono font-weight-bold text-body-2" :class="(item.needs_review_count || 0) > 0 ? 'text-warning-darken-2' : 'text-success'">
                  {{ item.needs_review_count || 0 }} بحاجة لمراجعة
                </span>
              </template>
              <template v-else-if="key === 'completed_count'">
                <span class="font-mono font-weight-bold text-body-2 text-success">{{ item.completed_count || 0 }} معتمدة</span>
              </template>
            </template>
          </custom-data-table>
        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ReviewMasterFilters from './ReviewMasterFilters.vue'
import {
  officeMasterHeaders,
  directorateMasterHeaders,
  schoolMasterHeaders,
  examMasterHeaders,
  sliceForPagination,
} from './useReviewMaster'

const props = defineProps<{
  institutionType: string
  sectorOptions: any[]
  masterTab: string
  selectedOfficeId: any
  selectedDirectorateId: any
  selectedSchoolId: any
  selectedSubjectId: any
  allOfficesList: any[]
  officesList: any[]
  directoratesOptions: any[]
  schoolsOptions: any[]
  subjectsList: any[]
  loadingMaster: boolean
  filteredOfficesTable: any[]
  filteredDirectoratesTable: any[]
  filteredSchoolsTable: any[]
  filteredMasterExamsTable: any[]
}>()

const emit = defineEmits<{
  (e: 'update:institutionType', val: string): void
  (e: 'update:masterTab', val: string): void
  (e: 'update:selectedOfficeId', val: any): void
  (e: 'update:selectedDirectorateId', val: any): void
  (e: 'update:selectedSchoolId', val: any): void
  (e: 'update:selectedSubjectId', val: any): void
  (e: 'refresh'): void
  (e: 'reset'): void
  (e: 'select-exam', exam: any): void
}>()

const currentTab = computed({
  get: () => props.masterTab,
  set: (val) => emit('update:masterTab', val),
})

const officeTableItems = ref({ results: [], count: 0 })
const directorateTableItems = ref({ results: [], count: 0 })
const schoolTableItems = ref({ results: [], count: 0 })
const examTableItems = ref({ results: [], count: 0 })

const filteredOffices = computed(() => props.filteredOfficesTable || [])
const filteredDirectorates = computed(() => props.filteredDirectoratesTable || [])
const filteredSchools = computed(() => props.filteredSchoolsTable || [])
const filteredExams = computed(() => props.filteredMasterExamsTable || [])

function getOfficeData(params: any) {
  officeTableItems.value = sliceForPagination(filteredOffices.value, params)
  return officeTableItems.value
}

function getDirectorateData(params: any) {
  directorateTableItems.value = sliceForPagination(filteredDirectorates.value, params)
  return directorateTableItems.value
}

function getSchoolData(params: any) {
  schoolTableItems.value = sliceForPagination(filteredSchools.value, params)
  return schoolTableItems.value
}

function getExamData(params: any) {
  examTableItems.value = sliceForPagination(filteredExams.value, params)
  return examTableItems.value
}

function onDrillDownOffice(item: any) {
  emit('update:selectedOfficeId', [item.id])
  emit('update:selectedDirectorateId', null)
  emit('update:selectedSchoolId', null)
  emit('update:masterTab', 'directorates')
  emit('refresh')
}

function onOpenOfficeExams(item: any) {
  emit('update:selectedOfficeId', [item.id])
  emit('update:selectedDirectorateId', null)
  emit('update:selectedSchoolId', null)
  emit('update:masterTab', 'exams')
  emit('refresh')
}

function onDrillDownDirectorate(item: any) {
  emit('update:selectedDirectorateId', [item.id])
  emit('update:selectedSchoolId', null)
  emit('update:masterTab', 'schools')
  emit('refresh')
}

function onOpenDirectorateExams(item: any) {
  emit('update:selectedDirectorateId', [item.id])
  emit('update:selectedSchoolId', null)
  emit('update:masterTab', 'exams')
  emit('refresh')
}

function onOpenSchoolExams(item: any) {
  emit('update:selectedSchoolId', [item.id])
  emit('update:masterTab', 'exams')
  emit('refresh')
}
</script>
