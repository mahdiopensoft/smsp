<template>
  <div v-if="selectedExam" class="main-card mb-4 pa-4 bg-surface border rounded-2xl elevation-2">
    <!-- السطر الأول: العنوان والهوية والاعتماد -->
    <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-1">
      <div class="d-flex align-center gap-3">
        <v-avatar color="primary" variant="tonal" size="44" class="rounded-xl flex-shrink-0">
          <v-icon size="24" color="primary">mdi-file-document-check-outline</v-icon>
        </v-avatar>
        <div>
          <div class="d-flex align-center gap-2 flex-wrap">
            <h2 class="text-subtitle-1 font-weight-black text-on-surface mb-0">
              {{ selectedExam.title }}
            </h2>
            <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
              معتمد للطباعة
            </v-chip>
          </div>
          <div class="d-flex align-center gap-2 text-caption text-medium-emphasis flex-wrap mt-1">
            <span class="font-mono font-weight-bold text-primary">{{ selectedExam.uniqueCode }}</span>
            <span>•</span>
            <span v-if="selectedExam.subject_name">المادة: <strong class="text-on-surface font-weight-bold">{{ selectedExam.subject_name }}</strong></span>
            <span>•</span>
            <span>العام الدراسي: <strong class="text-on-surface font-weight-bold">{{ selectedExam.year_name || '2025-2026' }}</strong></span>
            <template v-if="selectedSchoolName">
              <span>•</span>
              <span>المركز: <strong class="text-teal font-weight-bold">{{ selectedSchoolName }}</strong></span>
            </template>
          </div>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" prepend-icon="mdi-layers-outline">
          {{ versionsChipLabel }}
        </v-chip>
        <v-chip size="small" color="success" variant="tonal" class="font-weight-black" prepend-icon="mdi-account-group-outline">
          {{ examDetails?.registered_students?.length || selectedExam.registered_students_count || 0 }} طالب
        </v-chip>
        <v-btn
          size="small"
          variant="tonal"
          color="primary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-tune-vertical"
          :to="`/omr-template-builder?examId=${selectedExam.id}&mode=designer`"
          title="تخصيص وضبط القالب الهندسي في المصمم"
        >
          تخصيص القالب
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  selectedExam: any
  selectedSchoolName?: string
  versionsChipLabel?: string
  examDetails?: any
}>()
</script>
