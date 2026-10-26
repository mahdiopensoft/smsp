<template>
  <v-card
    v-if="exam"
    class="pa-4 pa-md-5 rounded-2xl mb-6 elevation-1 border bg-surface"
    style="border-right: 6px solid rgb(var(--v-theme-primary)) !important;"
  >
    <div class="d-flex align-center justify-space-between flex-wrap gap-4">
      <div class="d-flex align-center">
        <v-avatar color="primary" variant="tonal" size="48" class="me-3 rounded-xl flex-shrink-0">
          <v-icon size="26">mdi-check-decagram-outline</v-icon>
        </v-avatar>
        <div>
          <div class="d-flex align-center gap-2 flex-wrap mb-1">
            <span class="text-h6 font-weight-black text-on-surface">
              تم استيراد وضبط قالب الاختبار: {{ exam.title }}
            </span>
            <v-chip color="success" size="small" variant="flat" class="font-weight-bold">
              <v-icon start size="14">mdi-check-circle</v-icon>
              جاهز للاعتماد والطباعة
            </v-chip>
          </div>
          <div class="text-caption text-medium-emphasis d-flex align-center gap-3 flex-wrap">
            <span>المادة: <strong class="text-on-surface">{{ exam.subject_name || 'عام' }}</strong></span>
            <span>• الرمز: <strong class="font-mono text-on-surface">{{ exam.uniqueCode }}</strong></span>
            <span>• عدد الأسئلة: <strong class="text-primary">{{ questionsCount }} سؤالاً</strong></span>
            <span>• النموذج المعتمد: <strong class="text-primary">{{ displayMode === 'compact_a5' ? 'ورقة الطالب A5 (الوزارية)' : 'الورقة الشاملة A4' }}</strong></span>
          </div>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-arrow-right"
          title="الرجوع إلى شاشة استلام الاختبارات"
          @click="$emit('back-to-exam')"
        >
          العودة للاختبار
        </v-btn>

        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-printer-check"
          title="الانتقال إلى سجل الطباعة وتوليد أوراق الطلاب"
          @click="$emit('go-to-print')"
        >
          اعتماد وتوجيه للطباعة
        </v-btn>

        <v-btn
          color="success"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-scanner"
          title="الانتقال مباشرة لمختبر المسح الضوئي والتصحيح"
          @click="$emit('go-to-scanner')"
        >
          الانتقال للتصحيح الضوئي
        </v-btn>
      </div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  exam: any
  questionsCount: number
  displayMode: string
}>()

defineEmits<{
  (e: 'back-to-exam'): void
  (e: 'go-to-print'): void
  (e: 'go-to-scanner'): void
}>()
</script>
