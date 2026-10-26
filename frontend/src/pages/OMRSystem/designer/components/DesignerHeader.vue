<template>
  <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
    <div class="d-flex align-center">
      <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
        <v-icon size="24">{{ pageMode === 'library' ? 'mdi-folder-multiple-outline' : 'mdi-tune-vertical' }}</v-icon>
      </v-avatar>
      <div>
        <h1 class="text-h5 font-weight-black text-on-surface mb-0">
          {{ pageMode === 'library' ? 'مكتبة قوالب التصحيح المعيارية' : 'مصمم القوالب الهندسية المعيارية' }}
        </h1>
        <p class="text-caption text-medium-emphasis mb-0">
          {{ pageMode === 'library' ? 'استعراض وإدارة قوالب الامتحانات المعتمدة واستخدامها المباشر في التصحيح' : 'إنشاء وتخصيص وتوثيق أوراق الإجابة بدقة مليمترية معتمدة' }}
        </p>
      </div>
    </div>

    <div class="d-flex align-center gap-2 flex-wrap">
      <v-btn
        v-if="pageMode === 'designer'"
        variant="tonal"
        color="secondary"
        rounded="lg"
        class="font-weight-bold"
        prepend-icon="mdi-arrow-right"
        @click="$emit('switch-mode', 'library')"
      >
        العودة لمكتبة القوالب
      </v-btn>

      <v-btn
        v-if="pageMode === 'library'"
        color="primary"
        rounded="lg"
        class="font-weight-bold px-5"
        prepend-icon="mdi-plus"
        @click="$emit('create-new')"
      >
        تصميم قالب جديد
      </v-btn>

      <template v-if="pageMode === 'designer'">
        <v-btn
          variant="tonal"
          color="primary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-database-import-outline"
          @click="$emit('open-import')"
        >
          استيراد من اختبار
        </v-btn>

        <v-btn
          variant="outlined"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-refresh"
          @click="$emit('reset')"
        >
          إعادة تعيين
        </v-btn>

        <v-btn
          v-if="savedDbId"
          color="success"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-content-save-check"
          :loading="isSaving"
          @click="$emit('update')"
        >
          حفظ التعديلات
        </v-btn>

        <v-btn
          color="primary"
          rounded="lg"
          class="font-weight-bold px-5"
          prepend-icon="mdi-content-save-plus"
          :loading="isSaving"
          @click="$emit('open-save-modal')"
        >
          حفظ كقالب جديد
        </v-btn>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  pageMode: 'library' | 'designer'
  savedDbId: number | string | null
  isSaving: boolean
}>()

defineEmits<{
  (e: 'switch-mode', mode: 'library' | 'designer'): void
  (e: 'create-new'): void
  (e: 'open-import'): void
  (e: 'reset'): void
  (e: 'update'): void
  (e: 'open-save-modal'): void
}>()
</script>
