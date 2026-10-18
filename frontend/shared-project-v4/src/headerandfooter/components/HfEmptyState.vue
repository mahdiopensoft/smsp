<template>
  <div class="hf-empty">
    <div class="hf-empty-inner">
      <div class="hf-empty-icon">
        <v-icon icon="mdi-page-layout-header-footer" size="64" color="primary" />
      </div>
      <div class="text-h6 font-weight-bold mb-2">لا يوجد قالب محدد</div>
      <div class="text-body-2 text-medium-emphasis mb-6">
        ابدأ بإنشاء قالب جديد لتصميم الهيدر والفوتر ودعم المتغيرات والصور
      </div>
      <v-btn
        prepend-icon="mdi-plus-circle"
        color="primary"
        variant="flat"
        rounded="xl"
        size="large"
        @click="$emit('open-create')"
      >
        إنشاء قالب جديد
      </v-btn>
    </div>
  </div>
</template>

<script setup>
defineEmits(['open-create'])
</script>
