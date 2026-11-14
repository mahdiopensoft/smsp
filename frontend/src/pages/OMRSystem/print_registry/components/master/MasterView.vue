<template>
  <div class="master-view-container">
    <!-- شريط التصفية الهيكلي الموحد بنمط students-master القياسي -->
    <MasterFiltersBar
      :filters="filters"
      :loading="loadingMaster"
      @apply="$emit('load-master-data')"
    />

    <!-- 4. تبويبات الاستعراض الهيكلي وسجل الطباعة المركزي (Master Tabs) -->
    <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1 bg-surface border">
      <div class="d-flex align-center flex-wrap gap-2 px-4 pt-3 border-b">
        <v-tabs
          :model-value="masterTab"
          @update:model-value="$emit('update:masterTab', $event)"
          color="primary"
          density="compact"
        >
          <v-tab v-if="institutionType === 'school' || institutionType === 'all'" value="offices" class="font-weight-bold">
            <v-icon start size="18">mdi-office-building-outline</v-icon>
            مكاتب التربية والتعليم ({{ filteredOfficesTable.length }})
          </v-tab>
          <v-tab v-if="institutionType === 'school' || institutionType === 'all'" value="directorates" class="font-weight-bold">
            <v-icon start size="18">mdi-map-marker-radius-outline</v-icon>
            إدارات التربية بالمديريات ({{ filteredDirectoratesTable.length }})
          </v-tab>
          <v-tab value="schools" class="font-weight-bold">
            <v-icon start size="18">{{ institutionType === 'university' ? 'mdi-domain' : (institutionType === 'institute' ? 'mdi-tools' : 'mdi-school-outline') }}</v-icon>
            {{ institutionType === 'university' ? 'الجامعات والكليات' : (institutionType === 'institute' ? 'المعاهد والمراكز' : (institutionType === 'all' ? 'المراكز التعليمية والامتحانية' : 'المراكز الامتحانية والمدارس')) }} ({{ filteredSchoolsTable.length }})
          </v-tab>
          <v-tab value="exams" class="font-weight-bold">
            <v-icon start size="18">mdi-file-document-check-outline</v-icon>
            الاختبارات المعتمدة للطباعة ({{ filteredMasterExamsTable.length }})
          </v-tab>
          <v-tab value="registry" class="font-weight-bold">
            <v-icon start size="18">mdi-history</v-icon>
            سجل الدفعات المطبوعة ({{ filteredBatchesTable.length }})
          </v-tab>
        </v-tabs>
      </div>

      <v-window :model-value="masterTab">
        <!-- 1. تبويب مكاتب التربية بالمحافظات -->
        <v-window-item value="offices" v-if="institutionType === 'school' || institutionType === 'all'">
          <MasterOfficesTab
            :items="officeMasterTableItems"
            :get-data="getOfficeMasterData"
            :headers="officeMasterHeaders"
            :loading="loadingMaster"
            :selected-rows="selectedOfficeMasterRows"
            @update:selected-rows="$emit('update:selectedOfficeMasterRows', $event)"
            :filtered-count="filteredOfficesTable.length"
            :filter-key="normalizeIds(selectedOfficeId).join('-')"
            @drill-down="$emit('drill-down-office', $event)"
            @open-studio="$emit('open-office-studio', $event)"
          />
        </v-window-item>

        <!-- 2. تبويب إدارات التربية بالمديريات -->
        <v-window-item value="directorates" v-if="institutionType === 'school' || institutionType === 'all'">
          <MasterDirectoratesTab
            :items="directorateMasterTableItems"
            :get-data="getDirectorateMasterData"
            :headers="directorateMasterHeaders"
            :loading="loadingMaster"
            :selected-rows="selectedDirectorateMasterRows"
            @update:selected-rows="$emit('update:selectedDirectorateMasterRows', $event)"
            :filtered-count="filteredDirectoratesTable.length"
            :filter-key="normalizeIds(selectedDirectorateId).join('-')"
            @drill-down="$emit('drill-down-directorate', $event)"
            @open-studio="$emit('open-directorate-studio', $event)"
          />
        </v-window-item>

        <!-- 3. تبويب المراكز الامتحانية والمدارس / الجامعات / المعاهد -->
        <v-window-item value="schools">
          <MasterSchoolsTab
            :items="schoolMasterTableItems"
            :get-data="getSchoolMasterData"
            :headers="schoolMasterHeaders"
            :loading="loadingMaster"
            :selected-rows="selectedSchoolMasterRows"
            @update:selected-rows="$emit('update:selectedSchoolMasterRows', $event)"
            :filtered-count="filteredSchoolsTable.length"
            :filter-key="normalizeIds(selectedSchoolId).join('-')"
            @open-exams-dialog="$emit('open-school-exams-dialog', $event)"
            @open-studio="$emit('open-school-studio', $event)"
          />
        </v-window-item>

        <!-- 4. تبويب الاختبارات المعتمدة للطباعة (مع التبويبات الفرعية الستة) -->
        <v-window-item value="exams">
          <MasterExamsTab
            :sub-tab="examSubTab"
            @update:sub-tab="$emit('update:examSubTab', $event)"
            :selected-rows="selectedExamMasterRows"
            @update:selected-rows="$emit('update:selectedExamMasterRows', $event)"
            :items="examMasterTableItems"
            :get-data="getExamMasterData"
            :headers="examMasterHeaders"
            :loading="loadingMaster"
            :pending-and-active-orders-count="pendingAndActiveOrdersCount"
            :scheduled-exams-count="scheduledExamsCount"
            :due-exams-count="dueExamsCount"
            :completed-exams-count="completedExamsCount"
            :cancelled-exams-count="cancelledExamsCount"
            :all-exams-count="allExamsCount"
            @direct-print="$emit('direct-print', $event)"
            @open-studio="$emit('open-exam-studio', $event)"
            @preview-manifest="$emit('preview-manifest', $event)"
            @approve-order="$emit('approve-order', $event)"
            @return-order="$emit('return-order', $event)"
            @advance-schedule="$emit('advance-schedule', $event)"
            @cancel-order="$emit('cancel-order', $event)"
            @view-history="$emit('view-history', $event)"
          />
        </v-window-item>

        <!-- 5. تبويب سجل الدفعات المطبوعة العام -->
        <v-window-item value="registry">
          <MasterBatchesTab
            :items="batchMasterTableItems"
            :get-data="getBatchMasterData"
            :headers="registryMasterHeaders"
            :loading="loadingBatches"
            :selected-rows="selectedBatchMasterRows"
            @update:selected-rows="$emit('update:selectedBatchMasterRows', $event)"
            @view-batch="$emit('view-batch', $event)"
          />
        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script setup lang="ts">
import MasterFiltersBar from './MasterFiltersBar.vue'
import MasterOfficesTab from './MasterOfficesTab.vue'
import MasterDirectoratesTab from './MasterDirectoratesTab.vue'
import MasterSchoolsTab from './MasterSchoolsTab.vue'
import MasterExamsTab from './MasterExamsTab.vue'
import MasterBatchesTab from './MasterBatchesTab.vue'

defineProps<{
  filters: any
  loadingMaster?: boolean
  masterTab: string
  institutionType: string
  filteredOfficesTable: any[]
  filteredDirectoratesTable: any[]
  filteredSchoolsTable: any[]
  filteredMasterExamsTable: any[]
  filteredBatchesTable: any[]
  officeMasterTableItems: any
  getOfficeMasterData: (params?: any) => Promise<any>
  officeMasterHeaders: any[]
  selectedOfficeMasterRows: any[]
  directorateMasterTableItems: any
  getDirectorateMasterData: (params?: any) => Promise<any>
  directorateMasterHeaders: any[]
  selectedDirectorateMasterRows: any[]
  schoolMasterTableItems: any
  getSchoolMasterData: (params?: any) => Promise<any>
  schoolMasterHeaders: any[]
  selectedSchoolMasterRows: any[]
  examSubTab: string
  selectedExamMasterRows: any[]
  examMasterTableItems: any
  getExamMasterData: (params?: any) => Promise<any>
  examMasterHeaders: any[]
  pendingAndActiveOrdersCount: number
  scheduledExamsCount: number
  dueExamsCount: number
  completedExamsCount: number
  cancelledExamsCount: number
  allExamsCount: number
  selectedBatchMasterRows: any[]
  batchMasterTableItems: any
  getBatchMasterData: (params?: any) => Promise<any>
  registryMasterHeaders: any[]
  loadingBatches?: boolean
  selectedOfficeId: any
  selectedDirectorateId: any
  selectedSchoolId: any
  normalizeIds: (val: any) => number[]
}>()

defineEmits<{
  (e: 'load-master-data'): void
  (e: 'update:masterTab', val: string): void
  (e: 'update:selectedOfficeMasterRows', val: any[]): void
  (e: 'update:selectedDirectorateMasterRows', val: any[]): void
  (e: 'update:selectedSchoolMasterRows', val: any[]): void
  (e: 'update:selectedExamMasterRows', val: any[]): void
  (e: 'update:selectedBatchMasterRows', val: any[]): void
  (e: 'update:examSubTab', val: string): void
  (e: 'drill-down-office', item: any): void
  (e: 'open-office-studio', item: any): void
  (e: 'drill-down-directorate', item: any): void
  (e: 'open-directorate-studio', item: any): void
  (e: 'open-school-exams-dialog', item: any): void
  (e: 'open-school-studio', item: any): void
  (e: 'direct-print', item: any): void
  (e: 'open-exam-studio', item: any): void
  (e: 'preview-manifest', item: any): void
  (e: 'approve-order', item: any): void
  (e: 'return-order', item: any): void
  (e: 'advance-schedule', item: any): void
  (e: 'cancel-order', item: any): void
  (e: 'view-history', item: any): void
  (e: 'view-batch', item: any): void
}>()
</script>
