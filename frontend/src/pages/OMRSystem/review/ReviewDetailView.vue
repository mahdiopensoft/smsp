<template>
  <div class="detail-view-container">
    <!-- ── شريط المسار والرجوع ── -->
    <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
        <!-- زر العودة والمسار الأكاديمي -->
        <div class="d-flex align-center gap-3 flex-wrap">
          <v-btn
            color="primary"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-arrow-right"
            @click="$emit('return-to-master')"
          >
            العودة للهيكل الإداري
          </v-btn>

          <v-divider vertical class="mx-1" />

          <div class="d-flex align-center gap-2 flex-wrap text-caption font-weight-bold text-medium-emphasis">
            <span class="text-on-surface font-weight-black">
              {{ activeBreadcrumb?.institution_type_name || (institutionType === 'university' ? 'التعليم الجامعي' : (institutionType === 'institute' ? 'التعليم الفني' : 'التعليم العام')) }}
            </span>
            <template v-if="activeBreadcrumb?.office_name">
              <v-icon size="14">mdi-chevron-left</v-icon>
              <span class="text-primary font-weight-bold">{{ activeBreadcrumb.office_name }}</span>
            </template>
            <template v-if="activeBreadcrumb?.directorate_name || (detailFilterDirectorate && detailFilterDirectorate !== 'all')">
              <v-icon size="14">mdi-chevron-left</v-icon>
              <span class="text-teal font-weight-bold">
                {{ (detailFilterDirectorate && detailFilterDirectorate !== 'all') ? detailFilterDirectorate : activeBreadcrumb?.directorate_name }}
              </span>
            </template>
            <template v-if="activeBreadcrumb?.school_name">
              <v-icon size="14">mdi-chevron-left</v-icon>
              <span class="text-indigo font-weight-bold">
                {{ (detailFilterSchool && detailFilterSchool !== 'all') ? detailFilterSchool : activeBreadcrumb?.school_name }}
              </span>
            </template>
            <v-icon size="14">mdi-chevron-left</v-icon>
            <span class="text-primary font-weight-black">{{ activeBreadcrumb?.exam_title || activeExam?.title }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── كبسولات المؤشرات التفاعلية الموحدة لكشف أوراق الاختبار ── -->
    <div class="d-flex align-center gap-2 flex-wrap pa-3 bg-surface border rounded-xl mb-4 elevation-1">
      <span class="text-caption font-weight-black text-medium-emphasis me-1">تصفية المؤشرات:</span>
      <v-chip
        v-for="chip in metricFilterChips"
        :key="chip.key"
        color="teal"
        :variant="activeMetricFilter === chip.key ? 'flat' : 'tonal'"
        size="small"
        rounded="lg"
        class="font-weight-bold cursor-pointer transition-all"
        :class="{ 'elevation-2 text-white font-weight-black': activeMetricFilter === chip.key }"
        @click="toggleMetricFilter(chip.key)"
      >
        <v-icon v-if="activeMetricFilter === chip.key" start size="14">mdi-check</v-icon>
        <span>{{ chip.label }}: {{ chip.countText }}</span>
      </v-chip>
      <v-btn
        v-if="activeMetricFilter !== 'all'"
        size="x-small"
        variant="text"
        color="teal"
        class="font-weight-bold ms-1"
        prepend-icon="mdi-close-circle"
        @click="toggleMetricFilter('all')"
      >
        إلغاء التصفية
      </v-btn>
    </div>

    <!-- ── فلاتر فرعية سريعة لكشف أوراق الاختبار ── -->
    <filter-fields label="خيارات تصفية أوراق إجابة الطلاب" class="main-card border-0 pa-4 rounded-2xl mb-6 elevation-1">
      <v-row dense class="align-center">
        <!-- فلتر المديرية -->
        <v-col cols="12" sm="6" md="2" v-if="institutionType === 'school'">
          <v-autocomplete
            v-model="detailFilterDirectorate"
            :items="directoratesOptions"
            item-title="title"
            item-value="value"
            label="إدارة التربية (المديرية)"
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            clearable
            class="mb-2"
            prepend-inner-icon="mdi-map-marker-radius-outline"
            @update:model-value="emitFilterChange"
            @click:clear="clearDirectorate"
          />
        </v-col>

        <!-- فلتر المدرسة / الكلية / المعهد -->
        <v-col cols="12" sm="6" :md="institutionType === 'school' ? 3 : 4">
          <v-autocomplete
            v-model="detailFilterSchool"
            :items="schoolsOptions"
            item-title="title"
            item-value="value"
            :label="institutionType === 'university' ? 'الكلية / المركز' : (institutionType === 'institute' ? 'المعهد / المركز' : 'المدرسة / المركز الامتحاني')"
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            clearable
            class="mb-2"
            prepend-inner-icon="mdi-school-outline"
            @update:model-value="emitFilterChange"
            @click:clear="clearSchool"
          />
        </v-col>

        <!-- فلتر حالة المراجعة -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="detailFilterStatus"
            :items="statusOptions"
            item-title="title"
            item-value="value"
            label="حالة المراجعة"
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-2"
            prepend-inner-icon="mdi-list-status"
            @update:model-value="emitFilterChange"
          />
        </v-col>

        <!-- حقل البحث السريع بالاسم أو رقم الجلوس -->
        <v-col cols="12" sm="6" :md="institutionType === 'school' ? 3 : 4">
          <v-text-field
            v-model="searchQuery"
            label="اسم الطالب أو رقم الجلوس"
            placeholder="بحث برقم الجلوس أو اسم الطالب..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            rounded="lg"
            class="mb-2"
            hide-details
            @keyup.enter="emitFilterChange"
            @click:clear="clearSearch"
          />
        </v-col>

        <!-- أزرار الإجراءات -->
        <v-col cols="12" sm="12" md="2" class="d-flex align-center justify-end gap-2 mb-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            icon="mdi-filter"
            class="font-weight-bold px-4"
            :loading="loadingDetail"
            :click="emitFilterChange"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="إلغاء الفلترة"
            icon="mdi-filter-off"
            class="font-weight-bold"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ── جدول أوراق إجابة الطلاب لكشف الاختبار ── -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table
        v-bind="{
          items: detailTableItems,
          getData: getDetailData,
          headers: detailHeaders,
          customLoading: loadingDetail,
          hasFilter: false,
          search: false,
          numbering: true,
          actions: false,
          log: false,
          restore: false,
        }"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Student Info & Seat Number -->
          <template v-if="key === 'student_info'">
            <div class="d-flex align-center py-2" style="min-width: 240px;">
              <v-avatar
                color="primary"
                variant="tonal"
                size="42"
                class="me-3 rounded-lg flex-shrink-0 cursor-pointer border"
                @click="$emit('review-sheet', item)"
              >
                <v-img v-if="item.aligned_image || item.sheet_image" :src="fixImageUrl(item.aligned_image || item.sheet_image)" cover />
                <v-icon v-else size="22" color="primary">mdi-file-document-outline</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-bold text-body-2 text-on-surface cursor-pointer" @click="$emit('review-sheet', item)">
                  {{ item.student_name || ('ورقة #' + item.id) }}
                </div>
                <div v-if="item.seat_number" class="text-caption text-medium-emphasis mt-0.5">
                  رقم الجلوس: <span class="font-weight-bold text-on-surface ms-1">{{ item.seat_number }}</span>
                </div>
                <div v-if="item.school_name" class="text-caption text-primary mt-0.5">
                  {{ item.school_name }}
                </div>
              </div>
            </div>
          </template>

          <!-- Exam -->
          <template v-else-if="key === 'exam_title'">
            <div class="py-1">
              <div class="text-body-2 font-weight-medium text-truncate" style="max-width: 250px;">
                {{ item.exam_title || activeExam?.title || 'اختبار عام' }}
              </div>
            </div>
          </template>

          <!-- Confidence -->
          <template v-else-if="key === 'confidence'">
            <v-chip
              size="small"
              :color="item.confidence >= 0.85 ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              {{ Math.round((item.confidence || 0) * 100) }}%
            </v-chip>
          </template>

          <!-- Ambiguous questions -->
          <template v-else-if="key === 'ambiguous_count'">
            <v-chip
              v-if="item.ambiguous_count > 0"
              size="small"
              color="error"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              <v-icon start size="13">mdi-alert-circle-outline</v-icon>
              {{ item.ambiguous_count }} أسئلة
            </v-chip>
            <span v-else class="text-medium-emphasis text-caption">-</span>
          </template>

          <!-- Score -->
          <template v-else-if="key === 'score'">
            <div class="d-flex align-center justify-center font-weight-bold text-body-2" dir="ltr">
              <span>{{ item.mcq_score != null ? item.mcq_score : 0 }}</span>
              <span class="mx-1 text-medium-emphasis">/</span>
              <span>{{ item.mcq_max_score != null ? item.mcq_max_score : 0 }}</span>
            </div>
          </template>

          <!-- Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="small"
              :color="item.status === 'verified' ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              <v-icon start size="14">{{ item.status === 'verified' ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
              {{ item.status === 'verified' ? 'معتمد' : 'قيد التدقيق' }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <v-btn
                size="small"
                color="primary"
                variant="flat"
                class="font-weight-bold px-3"
                prepend-icon="mdi-shield-search"
                @click="$emit('review-sheet', item)"
              >
                تدقيق وتعديل
              </v-btn>
              <custom-btn
                v-if="item.status !== 'verified'"
                type="ok"
                is-icon
                label="اعتماد ومصادقة النتيجة"
                :click="() => $emit('approve-sheet', item)"
              />
              <custom-btn
                v-else
                type="done"
                is-icon
                label="تم الاعتماد مسبقاً"
                disabled
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { fixImageUrl } from './reviewUtils'

const props = defineProps<{
  institutionType: string
  activeExam: any
  activeBreadcrumb: any
  detailTableItems: any
  loadingDetail: boolean
  detailStats: any
  detailHeaders: any[]
  directoratesOptions: any[]
  schoolsOptions: any[]
  statusOptions: any[]
  getDetailData: Function
}>()

const emit = defineEmits<{
  (e: 'return-to-master'): void
  (e: 'review-sheet', sheet: any): void
  (e: 'approve-sheet', sheet: any): void
  (e: 'filter-change', filters: any): void
  (e: 'reset-filters'): void
}>()

const activeMetricFilter = ref('all')
const detailFilterDirectorate = ref('all')
const detailFilterSchool = ref('all')
const detailFilterStatus = ref('all')
const searchQuery = ref('')

const metricFilterChips = computed(() => {
  const s = props.detailStats || {}
  return [
    { key: 'all', label: 'كافة الأوراق', countText: `${s.totalSheets || 0}` },
    { key: 'pending', label: 'تتطلب تدقيق يدوي', countText: `${s.pendingReview || 0}` },
    { key: 'ambiguous', label: 'أوراق ملتبسة', countText: `${s.ambiguousSheets || 0}` },
    { key: 'verified', label: 'أوراق معتمدة', countText: `${s.verifiedSheets || 0}` },
  ]
})

function toggleMetricFilter(key: string) {
  activeMetricFilter.value = key
  emitFilterChange()
}

function emitFilterChange() {
  emit('filter-change', {
    metricFilter: activeMetricFilter.value,
    directorate: detailFilterDirectorate.value,
    school: detailFilterSchool.value,
    status: detailFilterStatus.value,
    search: searchQuery.value,
  })
}

function clearDirectorate() {
  detailFilterDirectorate.value = 'all'
  emitFilterChange()
}

function clearSchool() {
  detailFilterSchool.value = 'all'
  emitFilterChange()
}

function clearSearch() {
  searchQuery.value = ''
  emitFilterChange()
}

function resetFilters() {
  activeMetricFilter.value = 'all'
  detailFilterDirectorate.value = 'all'
  detailFilterSchool.value = 'all'
  detailFilterStatus.value = 'all'
  searchQuery.value = ''
  emit('reset-filters')
}
</script>
