<template>

    <!-- Title -->
    <div class="text-center mb-8">
        <div>
          مكتب التربية والتعليم بمحافظة:
          <strong>{{ input_data.governorate }}</strong>
        </div>
        <div>
          مديرية: <strong>{{ input_data.district }}</strong>
        </div>
      <div class="text-subtitle-1">
        للعام الدراسي: <strong>{{ input_data.academic_year }}</strong>
      </div>
    </div>

    <!-- Body -->
    <div class="doc-body text-body-1" style="line-height: 2.2">
      <p>
        الأخ / مدير مدرسة
        <strong class="mx-2">{{ input_data.school_name }}</strong> المحترم،
      </p>
      <p class="mb-6">
        أتقدم إليكم بطلب تسجيل ابني/ابنتي في الصف الأول الأساسي بمدرستكم
        الموقرة، وأقر بأن جميع البيانات المدونة أدناه صحيحة.
      </p>

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
          أولاً: بيانات الطالب
        </v-card-title>
        <v-card-text class="pa-4 text-black text-body-1">
          <v-row>
            <v-col cols="12" sm="8" class="py-2">
              الاسم الرباعي واللقب:
              <strong>{{ input_data.student_name }}</strong>
            </v-col>
            <v-col cols="12" sm="4" class="py-2">
              الجنس:
              <strong>{{
                input_data.gender === 1
                  ? "ذكر"
                  : input_data.gender === 2
                  ? "أنثى"
                  : ""
              }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              تاريخ الميلاد:
              <strong dir="ltr">{{ input_data.date_of_birth }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              مكان الميلاد: <strong>{{ input_data.governorate }} - {{ input_data.district }}</strong>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-card
        variant="outlined"
        class="mb-8"
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
          ثانياً: بيانات ولي الأمر
        </v-card-title>
        <v-card-text class="pa-4 text-black text-body-1">
          <v-row>
            <v-col cols="12" sm="8" class="py-2">
              اسم ولي الأمر الرباعي:
              <strong>{{ input_data.guardian_name }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              رقم الهوية: <strong>{{ input_data.identity_number }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              نوع الهوية: <strong>{{ input_data.identity_type }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              الوظيفة الأساسية: <strong>{{ input_data.job }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              رقم الهاتف الموبايل:
              <strong dir="ltr">{{ input_data.phone_number }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              هاتف العمل / المنزل:
              <strong dir="ltr">{{ input_data.home_number }}</strong>
            </v-col>
            <v-col cols="12" sm="6" class="py-2">
              عنوان السكن الحالي مفصلاً:
              <strong>{{ input_data.address }}</strong>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <div class="mb-2 font-weight-bold">المرفقات والوثائق:</div>
      <ul class="ml-0 pl-6 pr-6 mb-8" style="list-style-type: square">
        <li>نسخة من شهادة الميلاد الأصلية (للمطابقة)</li>
        <li>نسخة من هوية/بطاقة ولي الأمر الشخصية</li>
        <li>عدد (4) صور شخصية حديثة للطالب مقاس 4x6 بخلفية بيضاء</li>
        <li>الشهادة الصحية أو كرت التطعيم المعتمد</li>
      </ul>
    </div>

    <!-- Signatures -->
    <!-- <v-row class="text-center mt-8 pt-6">
      <v-col cols="6">
        <div class="font-weight-bold mb-8">توقيع ولي الأمر</div>
        <div class="text-grey-darken-1">
          ........................................
        </div>
      </v-col>
      <v-col cols="6">
        <div class="font-weight-bold mb-8">اعتماد لجنة القبول والتسجيل</div>
        <div class="text-grey-darken-1">
          ........................................
        </div>
      </v-col>
    </v-row> -->
</template>

<script>
export default {
  name: "RegistrationOfNewStudentRequestForm",
  inject: ["context"],
  data() {
    return {
      input_data: this.context?.input_data ?? {},
    };
  },
};
</script>

<style scoped>
/* Formal styling overrides */
ul {
  padding-right: 25px; /* RTL list indentation */
}
</style>
