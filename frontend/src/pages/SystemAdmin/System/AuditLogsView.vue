<template>
  <div class="qb-audit-logs-page-v4">
    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات تصفية سجل الرقابة والتدقيق التاريخي" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Action Type Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterAction"
            :items="actionOptions"
            item-title="title"
            item-value="value"
            placeholder="نوع الإجراء"
            prepend-inner-icon="mdi-filter-variant"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Resource Type Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterResourceType"
            :items="resourceTypeOptions"
            item-title="title"
            item-value="value"
            placeholder="نوع الكيان المستهدف"
            prepend-inner-icon="mdi-database-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- User Filter -->
        <auto-list
          v-model="filterUser"
          name="User"
          placeholder="المستخدم المنفذ"
          cols="3"
          :add="false"
        />

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            placeholder="بحث بالوصف، المعرف، أو IP..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Date From -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="filterDateFrom"
            type="date"
            placeholder="من تاريخ"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Date To -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="filterDateTo"
            type="date"
            placeholder="إلى تاريخ"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="12" md="6" class="d-flex align-center justify-end gap-2">
          <custom-btn
            type="show"
            label="تصفية السجل"
            color="primary"
            class="font-weight-bold px-6 mb-6"
            :click="loadData"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ الفلاتر"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Custom Data Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table :headers="headers" :items="tableItems" :getData="getData" :customLoading="loading"
        class="bg-transparent" :hasFilter="false" :log="false" :restore="false">
        <template v-slot:item-slot="{ item, key }">
          <!-- Action Type -->
          <template v-if="key === 'action'">
            <v-chip size="small" :color="getActionColor(item.action)" variant="tonal"
              class="font-weight-bold text-white">
              <v-icon start size="14">{{ getActionIcon(item.action) }}</v-icon>
              {{ item.action }}
            </v-chip>
          </template>

          <!-- User -->
          <template v-else-if="key === 'user_name'">
            <div class="d-flex align-center gap-2">
              <v-avatar size="28" color="primary" variant="tonal">
                <span class="text-caption font-weight-black">{{ (item.user_name || 'U').charAt(0) }}</span>
              </v-avatar>
              <div>
                <div class="font-weight-bold text-body-2">{{ item.user_name || 'النظام' }}</div>
                <div v-if="item.ip_address" class="text-caption text-medium-emphasis">
                  IP: {{ item.ip_address }}
                </div>
              </div>
            </div>
          </template>

          <!-- Resource Type & ID -->
          <template v-else-if="key === 'resource_type'">
            <div class="d-flex align-center gap-2">
              <v-chip size="small" variant="tonal" color="indigo" class="font-weight-bold">
                {{ item.resource_type }}
              </v-chip>
              <span v-if="item.resource_id" class="text-caption text-medium-emphasis">#{{ item.resource_id }}</span>
            </div>
          </template>

          <!-- Description -->
          <template v-else-if="key === 'description'">
            <div class="text-body-2 font-weight-medium text-slate-700">
              {{ item.description }}
            </div>
          </template>

          <!-- Created At -->
          <template v-else-if="key === 'created_at'">
            <div class="text-caption font-weight-medium text-medium-emphasis" dir="ltr">
              {{ formatDate(item.created_at) }}
            </div>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <custom-btn is-icon icon="eye-outline" color="primary" variant="text" size="small"
              :click="() => openDetailsDialog(item)" />
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- Log Details Modal (CustomDialog Component) -->
    <CustomDialog v-model="detailsDialog" width="680" title="تفاصيل سجل العملية والتدقيق"
      :subTitle="selectedLog ? `عملية: ${selectedLog.action} • الكيان: ${selectedLog.resource_type} #${selectedLog.resource_id}` : ''">
      <div v-if="selectedLog">
        <v-row dense class="mb-4">
          <v-col cols="12" sm="6">
            <div class="text-caption text-medium-emphasis">المستخدم المنفذ:</div>
            <div class="text-body-2 font-weight-bold text-primary">{{ selectedLog.user_name || 'النظام' }}</div>
          </v-col>
          <v-col cols="12" sm="6">
            <div class="text-caption text-medium-emphasis">عنوان IP:</div>
            <div class="text-body-2 font-mono">{{ selectedLog.ip_address || 'غير محدد' }}</div>
          </v-col>
          <v-col cols="12" sm="6" class="mt-2">
            <div class="text-caption text-medium-emphasis">تاريخ ووقت التنفيذ:</div>
            <div class="text-body-2 font-medium" dir="ltr">{{ formatDate(selectedLog.created_at) }}</div>
          </v-col>
          <v-col cols="12" sm="6" class="mt-2">
            <div class="text-caption text-medium-emphasis">نوع الإجراء:</div>
            <v-chip size="small" :color="getActionColor(selectedLog.action)" variant="tonal"
              class="text-white font-weight-bold">
              {{ selectedLog.action }}
            </v-chip>
          </v-col>
        </v-row>

        <div class="pa-4 bg-slate-50 rounded-xl border mb-3">
          <div class="text-caption text-medium-emphasis mb-1 font-weight-bold">نص ووصف العملية:</div>
          <div class="text-body-2 font-weight-medium text-slate-800">{{ selectedLog.description }}</div>
        </div>

        <div v-if="selectedLog.changes"
          class="pa-4 bg-slate-900 rounded-xl text-white font-mono text-caption overflow-auto"
          style="max-height: 250px;">
          <div class="text-emerald-400 font-weight-bold mb-2">سجل التغييرات والحقول (JSON Payload / Diff):</div>
          <pre style="white-space: pre-wrap; word-break: break-all;">{{ JSON.stringify(selectedLog.changes, null, 2) }}
      </pre>
        </div>
      </div>

      <template #actions>
        <custom-btn type="cancel" :click="() => detailsDialog = false" variant="text" label="إغلاق"
          class="font-weight-bold ms-auto" />
      </template>
    </CustomDialog>
  </div>
</template>

<script>
import { bankService } from '@/services/bankService'

export default {
  name: 'AuditLogsView',

  data() {
    return {
      loading: false,

      // Data items
      tableItems: { results: [], pagination: {} },

      // Filters
      filterAction: null,
      filterResourceType: null,
      filterUser: null,
      filterDateFrom: '',
      filterDateTo: '',
      searchQuery: '',

      actionOptions: [
        { title: 'إنشاء', value: 'إنشاء' },
        { title: 'تعديل', value: 'تعديل' },
        { title: 'حذف', value: 'حذف' },
        { title: 'اعتماد', value: 'اعتماد' },
        { title: 'رفض', value: 'رفض' },
        { title: 'استيراد جماعي', value: 'استيراد جماعي' },
        { title: 'أرشفة', value: 'أرشفة' },
        { title: 'استعادة', value: 'استعادة' },
        { title: 'طباعة', value: 'طباعة' },
        { title: 'مزامنة', value: 'مزامنة' },
      ],

      resourceTypeOptions: [
        { title: 'كافة الكيانات', value: null },
        { title: 'الأسئلة (Question)', value: 'Question' },
        { title: 'الاختبارات ونماذج التوليد (Exam)', value: 'Exam' },
        { title: 'جداول الامتحانات (ExamSchedule)', value: 'ExamSchedule' },
        { title: 'استيراد الأسئلة (ImportSession)', value: 'Import' },
        { title: 'المناهج والدروس (Curriculum)', value: 'Curriculum' },
        { title: 'المستخدمين (User)', value: 'User' },
      ],

      // Dialog
      detailsDialog: false,
      selectedLog: null,

      headers: [
        { title: "نوع الإجراء", key: "action", sortable: true, width: "140px", align: "center" },
        { title: "المستخدم المنفذ", key: "user_name", sortable: true, width: "180px" },
        { title: "الكيان المستهدف", key: "resource_type", sortable: true, width: "180px" },
        { title: "تفاصيل العملية", key: "description", sortable: false },
        { title: "تاريخ ووقت التنفيذ", key: "created_at", sortable: true, width: "180px", align: "center" },
      ],
    }
  },

  methods: {
    async getData(params = {}) {
      this.loading = true
      try {
        const queryParams = {
          ...params,
          action: this.filterAction || undefined,
          resource_type: this.filterResourceType || undefined,
          user: this.filterUser || undefined,
          date_from: this.filterDateFrom || undefined,
          date_to: this.filterDateTo || undefined,
          search: this.searchQuery || undefined,
        }
        const res = await bankService.getAuditLogs(queryParams)
        const data = res.data || res
        if (Array.isArray(data)) {
          this.tableItems = {
            results: data,
            pagination: { count: data.length, total: data.length },
          }
        } else {
          this.tableItems = data
        }
      } catch (err) {
        console.error('Error fetching audit logs:', err)
      } finally {
        this.loading = false
      }
    },

    async loadData() {
      await this.getData()
    },

    openDetailsDialog(item) {
      this.selectedLog = item
      this.detailsDialog = true
    },

    resetFilters() {
      this.filterAction = null
      this.filterResourceType = null
      this.filterUser = null
      this.filterDateFrom = ''
      this.filterDateTo = ''
      this.searchQuery = ''
      this.loadData()
    },

    getActionColor(action) {
      const map = {
        'إنشاء': 'success',
        'تعديل': 'amber-darken-2',
        'حذف': 'error',
        'اعتماد': 'primary',
        'رفض': 'deep-orange',
        'أرشفة': 'grey-darken-2',
        'استعادة': 'teal',
        'استيراد جماعي': 'purple',
        'تصدير': 'cyan',
        'طباعة': 'indigo',
        'مزامنة': 'blue',
      }
      return map[action] || 'grey'
    },

    getActionIcon(action) {
      const map = {
        'إنشاء': 'mdi-plus-circle',
        'تعديل': 'mdi-pencil',
        'حذف': 'mdi-delete',
        'اعتماد': 'mdi-check-circle',
        'رفض': 'mdi-close-circle',
        'أرشفة': 'mdi-archive',
        'استعادة': 'mdi-restore',
        'استيراد جماعي': 'mdi-file-excel',
        'تصدير': 'mdi-download',
        'طباعة': 'mdi-printer',
        'مزامنة': 'mdi-sync',
      }
      return map[action] || 'mdi-information-outline'
    },

    formatDate(dateStr) {
      if (!dateStr) return '-'
      try {
        const d = new Date(dateStr)
        return d.toLocaleString('ar-EG', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        })
      } catch (e) {
        return dateStr
      }
    },
  },

  mounted() {
    this.loadData()
  },
}
</script>

<style scoped>
.main-card {
  background: white;
  border-color: rgba(0, 0, 0, 0.08) !important;
}
</style>
