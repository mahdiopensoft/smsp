<template>
  <CustomDialog
    :model-value="modelValue"
    width="650"
    title="تقرير عجز الأسئلة المعتمدة"
    subTitle="نقص في بعض المستويات مقارنة بالمصفوفة المطلوبة"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <p class="text-body-2 text-medium-emphasis mb-3">
      يوجد نقص في رصيد الأسئلة المعتمدة المتوفرة ببنك الأسئلة للمادة المحددة مقارنة باحتياجات المصفوفة:
    </p>

    <v-table density="compact" class="rounded-xl border-subtle mb-4">
      <thead>
        <tr class="bg-surface-variant">
          <th class="font-weight-bold">المعيار المطلوب</th>
          <th class="font-weight-bold text-center">المطلوب</th>
          <th class="font-weight-bold text-center">المتوفر</th>
          <th class="font-weight-bold text-center">العجز</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="shortageReport?.mcq && shortageReport.mcq.missing > 0">
          <td><v-icon size="14" color="primary" class="me-1">mdi-radiobox-marked</v-icon> اختيار من متعدد (MCQ)</td>
          <td class="text-center">{{ shortageReport.mcq.required }}</td>
          <td class="text-center text-success font-weight-bold">{{ shortageReport.mcq.available }}</td>
          <td class="text-center text-error font-weight-bold">-{{ shortageReport.mcq.missing }}</td>
        </tr>
        <tr v-if="shortageReport?.tf && shortageReport.tf.missing > 0">
          <td><v-icon size="14" color="success" class="me-1">mdi-check-circle-outline</v-icon> صح وخطأ (True/False)</td>
          <td class="text-center">{{ shortageReport.tf.required }}</td>
          <td class="text-center text-success font-weight-bold">{{ shortageReport.tf.available }}</td>
          <td class="text-center text-error font-weight-bold">-{{ shortageReport.tf.missing }}</td>
        </tr>
        <tr v-if="shortageReport?.easy && shortageReport.easy.missing > 0">
          <td><v-icon size="14" color="success" class="me-1">mdi-speedometer-slow</v-icon> مستوى سهل</td>
          <td class="text-center">{{ shortageReport.easy.required }}</td>
          <td class="text-center text-success font-weight-bold">{{ shortageReport.easy.available }}</td>
          <td class="text-center text-error font-weight-bold">-{{ shortageReport.easy.missing }}</td>
        </tr>
        <tr v-if="shortageReport?.medium && shortageReport.medium.missing > 0">
          <td><v-icon size="14" color="warning" class="me-1">mdi-speedometer-medium</v-icon> مستوى متوسط</td>
          <td class="text-center">{{ shortageReport.medium.required }}</td>
          <td class="text-center text-success font-weight-bold">{{ shortageReport.medium.available }}</td>
          <td class="text-center text-error font-weight-bold">-{{ shortageReport.medium.missing }}</td>
        </tr>
        <tr v-if="shortageReport?.hard && shortageReport.hard.missing > 0">
          <td><v-icon size="14" color="error" class="me-1">mdi-speedometer</v-icon> مستوى صعب</td>
          <td class="text-center">{{ shortageReport.hard.required }}</td>
          <td class="text-center text-success font-weight-bold">{{ shortageReport.hard.available }}</td>
          <td class="text-center text-error font-weight-bold">-{{ shortageReport.hard.missing }}</td>
        </tr>
        <tr v-if="shortageReport?.totalMissing > 0" :style="'background: rgba(var(--v-theme-error), 0.08);'">
          <td class="font-weight-black text-error">إجمالي النقص العام للأسئلة</td>
          <td class="text-center font-weight-bold">{{ shortageReport.totalRequired }}</td>
          <td class="text-center font-weight-bold text-success">{{ shortageReport.totalAvailable }}</td>
          <td class="text-center font-weight-black text-error">-{{ shortageReport.totalMissing }}</td>
        </tr>
      </tbody>
    </v-table>

    <v-alert type="error" variant="tonal" density="compact" class="mb-4 rounded-xl">
      <v-icon start size="18">mdi-alert-octagon</v-icon>
      <strong>تنبيه وزاري ملزم:</strong> لا يمكن المتابعة أو توليد الاختبار طالما يوجد عجز في رصيد الأسئلة المعتمدة لضمان تحقيق الجودة والعدالة الامتحانية. يرجى تعديل نسب المصفوفة أو تغذية بنك الأسئلة بالأسئلة المطلوبة أولاً.
    </v-alert>

    <template #actions>
      <v-btn variant="text" color="medium-emphasis" class="font-weight-bold" @click="$emit('update:modelValue', false)">
        إغلاق
      </v-btn>
      <v-btn variant="tonal" color="primary" class="font-weight-bold rounded-lg" @click="$emit('goToMatrix')">
        <v-icon start size="16">mdi-cog-outline</v-icon>
        الرجوع للمصفوفة لتعديل النسب
      </v-btn>
      <v-btn variant="flat" color="info" class="font-weight-bold rounded-lg" @click="$emit('goToAddQuestion')">
        <v-icon start size="16">mdi-plus-circle-outline</v-icon>
        إضافة أسئلة بالبنك
      </v-btn>
    </template>
  </CustomDialog>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  shortageReport: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['update:modelValue', 'goToMatrix', 'goToAddQuestion'])
</script>
