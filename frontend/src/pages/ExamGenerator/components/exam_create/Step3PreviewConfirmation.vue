<template>
  <div>
    <div class="d-flex align-center justify-space-between mb-6 flex-wrap gap-2">
      <div>
        <h3 class="text-h5 font-weight-black mb-1 d-flex align-center gap-2">
          <v-icon color="success">mdi-clipboard-check-outline</v-icon>
          المعاينة والتأكيد
        </h3>
        <span class="text-body-2 text-medium-emphasis">مراجعة تفاصيل ورقة الاختبار ومطابقة المواصفات قبل بدء التوليد</span>
      </div>
    </div>

    <!-- 4 Executive KPI Certification Cards -->
    <v-row dense class="mb-5">
      <!-- KPI Card 1: Academic Scope -->
      <v-col cols="12" sm="6" md="3">
        <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-caption font-weight-bold text-medium-emphasis">المقرر والتصنيف</span>
            <v-avatar size="34" color="primary" variant="tonal" class="rounded-lg">
              <v-icon size="18">mdi-school</v-icon>
            </v-avatar>
          </div>
          <div class="kpi-title font-weight-black text-truncate mb-1" :title="exam.title || 'اختبار بدون عنوان'">
            {{ exam.title || 'اختبار بدون عنوان' }}
          </div>
          <div class="d-flex align-center gap-1 mb-2">
            <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
              {{ exam.institution_type === 'school' ? 'تعليم مدرسي' : exam.institution_type === 'university' ? 'تعليم جامعي' : 'تعليم مهني' }}
            </v-chip>
          </div>
          <span class="text-caption text-medium-emphasis d-block">السنة الدراسية والفترة معتمدة</span>
        </div>
      </v-col>

      <!-- KPI Card 2: Exam Capacity -->
      <v-col cols="12" sm="6" md="3">
        <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-caption font-weight-bold text-medium-emphasis">سعة الاختبار ورصيد الأسئلة</span>
            <v-avatar size="34" color="info" variant="tonal" class="rounded-lg">
              <v-icon size="18">mdi-file-document-check</v-icon>
            </v-avatar>
          </div>
          <div class="kpi-metric font-weight-black text-info mb-1">
            {{ exam.questionsCount }} <span class="text-caption font-weight-bold text-medium-emphasis">سؤال معتمد</span>
          </div>
          <div class="d-flex align-center gap-1 mb-2">
            <v-chip size="x-small" :color="exam.exclude_previously_used ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
              <v-icon start size="12">mdi-shield-check</v-icon>
              {{ exam.exclude_previously_used ? 'مكافحة التكرار نشطة' : 'السماح بالتكرار' }}
            </v-chip>
          </div>
          <span class="text-caption text-medium-emphasis d-block">بلوم: {{ bloomEnabled ? 'مفعّل' : 'معطّل' }}</span>
        </div>
      </v-col>

      <!-- KPI Card 3: Models System -->
      <v-col cols="12" sm="6" md="3">
        <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-caption font-weight-bold text-medium-emphasis">منظومة النماذج التوليدية</span>
            <v-avatar size="34" color="warning" variant="tonal" class="rounded-lg">
              <v-icon size="18">mdi-layers-triple</v-icon>
            </v-avatar>
          </div>
          <div class="kpi-metric font-weight-black text-warning mb-1">
            {{ totalModelsCount }} <span class="text-caption font-weight-bold text-medium-emphasis">نماذج فرعية</span>
          </div>
          <div class="d-flex align-center gap-1 mb-2">
            <v-chip size="x-small" :color="modelsMode === 'advanced' ? 'warning' : 'success'" variant="tonal" class="font-weight-bold">
              {{ modelsMode === 'advanced' ? 'نمط متقدم ومناطقي' : 'نمط موحد قياسي' }}
            </v-chip>
          </div>
          <span class="text-caption text-medium-emphasis d-block">
            {{ modelsMode === 'advanced' ? `${modelGroups.length} مجموعات صعوبة` : 'نماذج بنفس الأسئلة' }}
          </span>
        </div>
      </v-col>

      <!-- KPI Card 4: Geographic Scope -->
      <v-col cols="12" sm="6" md="3">
        <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-caption font-weight-bold text-medium-emphasis">النطاق والانتشار الجغرافي</span>
            <v-avatar size="34" color="deep-purple" variant="tonal" class="rounded-lg">
              <v-icon size="18">mdi-map-marker-radius</v-icon>
            </v-avatar>
          </div>
          <div class="kpi-metric font-weight-black text-deep-purple mb-1">
            <span v-if="modelsMode === 'uniform' || isAllGroupsAllRegions">كافة المناطق</span>
            <span v-else>{{ totalUniqueAssignedTargetsCount }} <span class="text-caption font-weight-bold text-medium-emphasis">منطقة مخصصة</span></span>
          </div>
          <div class="d-flex align-center gap-1 mb-2">
            <v-chip size="x-small" color="deep-purple" variant="tonal" class="font-weight-bold">
              {{ modelsMode === 'advanced' ? 'توزيع مناطقي بالمجموعات' : 'شامل عام' }}
            </v-chip>
          </div>
          <span class="text-caption text-medium-emphasis d-block">تغطية النماذج حسب المجموعات</span>
        </div>
      </v-col>
    </v-row>

    <!-- Model Groups Summary (Advanced Mode) -->
    <div v-if="modelsMode === 'advanced'" class="section-group-card pa-5 rounded-2xl mb-5">
      <h4 class="text-subtitle-1 font-weight-black mb-3 d-flex align-center gap-2">
        <v-icon size="20" color="warning">mdi-file-multiple-outline</v-icon>
        شهادة اعتماد مجموعات النماذج والتوزيع المناطقي:
      </h4>
      <v-table density="compact" class="executive-table rounded-xl border-subtle">
        <thead>
          <tr class="table-header-row">
            <th class="font-weight-bold">المجموعة</th>
            <th class="font-weight-bold">النماذج الفرعية</th>
            <th class="font-weight-bold">تنوع الأسئلة</th>
            <th class="font-weight-bold">ملف الصعوبة</th>
            <th class="font-weight-bold">أوزان الصعوبة (سهل / متوسط / صعب)</th>
            <th class="font-weight-bold">المناطق المخصصة</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(group, gIdx) in modelGroups" :key="gIdx">
            <td class="font-weight-bold">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</td>
            <td>
              <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold font-mono">
                {{ getGroupVersionCodes(gIdx) }} ({{ group.count }} نماذج)
              </v-chip>
            </td>
            <td>
              <v-chip
                size="x-small"
                :color="(group.questions_variation || 'same_scrambled') === 'different_questions' ? 'secondary' : 'primary'"
                variant="tonal"
                class="font-weight-bold"
              >
                <v-icon start size="14">
                  {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'mdi-layers-triple' : 'mdi-shuffle-variant' }}
                </v-icon>
                {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'أسئلة مستقلة' : 'نفس الأسئلة (خلط)' }}
              </v-chip>
            </td>
            <td>
              <v-chip size="x-small" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="font-weight-bold">
                {{ difficultyLabel(group.difficulty_profile) }}
              </v-chip>
            </td>
            <td class="text-caption">
              <span class="text-success font-weight-bold">{{ group.difficulty_distribution?.easy }}%</span> /
              <span class="text-warning font-weight-bold">{{ group.difficulty_distribution?.medium }}%</span> /
              <span class="text-error font-weight-bold">{{ group.difficulty_distribution?.hard }}%</span>
            </td>
            <td class="text-caption">
              <span v-if="group.target_ids && group.target_ids.length > 0" class="font-weight-bold text-primary">
                {{ getGroupTargetNames(group) }}
              </span>
              <span v-else-if="(group.scope_level || 'all') === 'all'" class="text-success font-weight-bold">
                كافة المناطق (عام)
              </span>
              <span v-else class="text-medium-emphasis">غير مخصص</span>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Distribution Summary Mini-Widgets -->
    <v-row dense>
      <v-col cols="12" md="4">
        <div class="section-group-card pa-4 rounded-2xl h-100">
          <div class="d-flex align-center justify-space-between mb-3">
            <h4 class="text-subtitle-2 font-weight-bold mb-0 d-flex align-center gap-2">
              <v-icon size="18" color="primary">mdi-book-open-page-variant</v-icon>
              توزيع الوحدات المعتمدة
            </h4>
            <v-chip size="x-small" :color="modelsMode === 'advanced' ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
              {{ modelsMode === 'advanced' ? 'حسب المجموعات' : 'موحد' }}
            </v-chip>
          </div>

          <template v-if="modelsMode === 'uniform'">
            <div
              v-for="unit in (blueprint?.units || []).filter(u => u.percentage > 0)"
              :key="unit.id"
              class="d-flex align-center justify-space-between py-1 border-b-subtle"
            >
              <span class="text-caption font-weight-bold text-truncate" style="max-width: 70%;">{{ unit.name }}</span>
              <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">{{ unit.percentage }}%</v-chip>
            </div>
          </template>
          <template v-else>
            <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="py-2 border-b-subtle">
              <div class="d-flex justify-space-between text-caption font-weight-bold mb-1">
                <span class="text-primary">{{ group.name || ('المجموعة ' + (gIdx + 1)) }} ({{ group.count }} نماذج)</span>
                <v-chip size="x-small" :color="getGroupUnitsTotal(group) === 100 ? 'success' : 'warning'" variant="tonal">
                  {{ getGroupUnitsTotal(group) }}%
                </v-chip>
              </div>
              <div
                v-for="unit in (group.units && group.units.length > 0 ? group.units : blueprint?.units || []).filter(u => u.percentage > 0)"
                :key="unit.id"
                class="d-flex align-center justify-space-between py-0-5 text-caption"
              >
                <span class="text-truncate text-medium-emphasis" style="max-width: 70%;">{{ unit.name }}</span>
                <span class="font-weight-bold">{{ unit.percentage }}%</span>
              </div>
            </div>
          </template>
        </div>
      </v-col>

      <v-col cols="12" md="4">
        <div class="section-group-card pa-4 rounded-2xl h-100">
          <div class="d-flex align-center justify-space-between mb-3">
            <h4 class="text-subtitle-2 font-weight-bold mb-0 d-flex align-center gap-2">
              <v-icon size="18" color="warning">mdi-speedometer</v-icon>
              توزيع الصعوبة المعتمد
            </h4>
            <v-chip size="x-small" :color="modelsMode === 'advanced' ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
              {{ modelsMode === 'advanced' ? 'متقدم' : 'موحد' }}
            </v-chip>
          </div>
          <template v-if="modelsMode === 'uniform'">
            <div
              v-for="level in (blueprint?.difficulty || [])"
              :key="level.name"
              class="d-flex align-center justify-space-between py-1 border-b-subtle"
            >
              <span class="text-caption font-weight-bold">{{ level.name }}</span>
              <v-chip size="x-small" :color="level.color" variant="tonal" class="font-weight-bold">
                {{ Math.round((Number(exam.questionsCount) || 0) * (level.percentage || 0) / 100) }} ({{ level.percentage }}%)
              </v-chip>
            </div>
          </template>
          <template v-else>
            <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="py-2 border-b-subtle">
              <div class="d-flex justify-space-between text-caption font-weight-bold mb-1">
                <span>{{ group.name || ('المجموعة ' + (gIdx + 1)) }} ({{ difficultyLabel(group.difficulty_profile) }})</span>
                <v-chip size="x-small" color="primary" variant="tonal">{{ group.count }} نماذج</v-chip>
              </div>
              <div class="d-flex gap-1">
                <v-chip size="x-small" color="success" variant="tonal">سهل {{ group.difficulty_distribution?.easy }}%</v-chip>
                <v-chip size="x-small" color="warning" variant="tonal">متوسط {{ group.difficulty_distribution?.medium }}%</v-chip>
                <v-chip size="x-small" color="error" variant="tonal">صعب {{ group.difficulty_distribution?.hard }}%</v-chip>
              </div>
            </div>
          </template>
        </div>
      </v-col>

      <v-col cols="12" md="4">
        <div class="section-group-card pa-4 rounded-2xl h-100">
          <h4 class="text-subtitle-2 font-weight-bold mb-3 d-flex align-center gap-2">
            <v-icon size="18" color="info">mdi-shape</v-icon>
            توزيع أنواع الأسئلة
          </h4>
          <div v-if="modelsMode === 'advanced'">
            <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="mb-2 pb-1 border-b-subtle">
              <span class="text-caption font-weight-black text-primary d-block mb-1">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</span>
              <div
                v-for="type in (group.types || []).filter(t => (t.percentage || 0) > 0)"
                :key="type.name"
                class="d-flex align-center justify-space-between py-0.5 text-caption"
              >
                <span class="text-caption">{{ type.shortName || type.name }}</span>
                <v-chip size="x-small" :color="type.color" variant="tonal" class="font-weight-bold">
                  {{ Math.round((Number(exam.questionsCount) || 0) * (type.percentage || 0) / 100) }} ({{ type.percentage }}%)
                </v-chip>
              </div>
            </div>
          </div>
          <div v-else>
            <div
              v-for="type in ((blueprint?.types || []).filter(t => (t.percentage || 0) > 0))"
              :key="type.name"
              class="d-flex align-center justify-space-between py-1 border-b-subtle"
            >
              <span class="text-caption font-weight-bold">{{ type.shortName || type.name }}</span>
              <v-chip size="x-small" :color="type.color" variant="tonal" class="font-weight-bold">
                {{ Math.round((Number(exam.questionsCount) || 0) * (type.percentage || 0) / 100) }} ({{ type.percentage }}%)
              </v-chip>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Call to Action Banner to Step 4 -->
    <div
      class="mt-6 pa-5 rounded-2xl border-subtle d-flex align-center justify-space-between flex-wrap gap-4"
      style="background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%); border: 1.5px solid rgba(var(--v-theme-primary), 0.2);"
    >
      <div class="d-flex align-center gap-3">
        <v-avatar size="48" color="primary" variant="tonal" class="rounded-xl">
          <v-icon size="26" color="primary">mdi-file-document-edit-outline</v-icon>
        </v-avatar>
        <div>
          <h4 class="text-subtitle-1 font-weight-black mb-0 text-high-emphasis">
            المرحلة الرابعة: مسودة استعراض وضبط نماذج الاختبار
          </h4>
          <p class="text-caption text-medium-emphasis mb-0 mt-0.5">
            سيتم سحب الأسئلة من البنك وعرض كافة النماذج في بيئة تفاعلية تتيح لك مراجعة الأسئلة واستبدالها أو إنشاء أسئلة جديدة قبل الاعتماد النهائي.
          </p>
        </div>
      </div>
      <v-btn
        color="primary"
        size="large"
        class="font-weight-black rounded-xl px-6 elevation-2"
        prepend-icon="mdi-arrow-left"
        :loading="stagingLoading"
        @click="$emit('nextStep')"
      >
        الانتقال لمسودة واستعراض النماذج
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { difficultyColor, difficultyLabel } from '../../composables/examHelpers'

defineProps({
  exam: {
    type: Object,
    required: true
  },
  bloomEnabled: {
    type: Boolean,
    default: false
  },
  modelsMode: {
    type: String,
    default: 'uniform'
  },
  totalModelsCount: {
    type: Number,
    default: 1
  },
  modelGroups: {
    type: Array,
    default: () => []
  },
  isAllGroupsAllRegions: {
    type: Boolean,
    default: false
  },
  totalUniqueAssignedTargetsCount: {
    type: Number,
    default: 0
  },
  blueprint: {
    type: Object,
    default: () => ({})
  },
  stagingLoading: {
    type: Boolean,
    default: false
  },
  getGroupVersionCodes: {
    type: Function,
    required: true
  },
  getGroupTargetNames: {
    type: Function,
    required: true
  },
  getGroupUnitsTotal: {
    type: Function,
    required: true
  }
})

defineEmits(['nextStep'])
</script>
