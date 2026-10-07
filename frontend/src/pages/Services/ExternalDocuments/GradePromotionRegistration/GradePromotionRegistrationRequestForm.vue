<template>
  <!-- Title -->
  <div class="text-center mb-8">
    <div class="text-subtitle-1">
      للعام الدراسي الجديد:
      <strong dir="ltr">{{ input_data.academic_year_new }}</strong>
    </div>
  </div>

  <!-- Body text -->
  <div class="doc-body text-body-1" style="line-height: 2.2">
    <p>الأخ / مدير إدارة المدرسة المحترم،</p>
    <p class="mb-6">
      أتقدم إليكم بطلب تجديد قيد وترفيع ابني/ابنتي للصف الدراسي التالي، وذلك
      بناءً على نتيجته في العام المنصرم، متعهداً بالالتزام بكافة أنظمة المدرسة
      واستيفاء أي متطلبات مالية أو إدارية سابقة.
    </p>

    <!-- Student current status -->
    <v-card
      variant="outlined"
      class="mb-6"
      style="border: 1px solid #000 !important"
    >
      <v-card-title
        class="py-2 font-weight-bold"
        style="
          background-color: #f5f5f5;
          border-bottom: 1px solid #000;
          font-size: 1.1rem;
          color: #000;
        "
      >
        أولاً: البيانات الأكاديمية للطالب
      </v-card-title>
      <v-card-text class="pa-4 text-black text-body-1">
        <v-row>
          <v-col cols="12" sm="8" class="py-2">
            اسم الطالب الرباعي: <strong>{{ input_data.student_name }}</strong>
          </v-col>
          <v-col cols="12" sm="4" class="py-2">
            الرقم المدرسي: <strong>{{ input_data.student_school_id }}</strong>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            الصف الدراسي <strong>الحالي</strong>:
            <strong>{{ input_data.previous_grade }}</strong>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>

  <!-- Signatures -->
  <!-- <v-row class="text-center mt-6 pt-6 align-center">
      <v-col cols="6">
        <div class="font-weight-bold mb-4">مقدم الطلب (ولي الأمر)</div>
        <div class="mb-2">
          <strong>{{ input_data.guardian_name }}</strong>
        </div>
        <div class="text-grey-darken-1">
          التوقيع: ............................
        </div>
      </v-col>
      <v-col cols="6">
        <div class="font-weight-bold mb-8">
          اعتماد شؤون الطلاب (للاستخدام الإداري)
        </div>
        <div class="text-grey-darken-1">
          الختم / التوقيع: ............................
        </div>
      </v-col>
    </v-row> -->
</template>

<script>
export default {
  name: "GradePromotionRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>
