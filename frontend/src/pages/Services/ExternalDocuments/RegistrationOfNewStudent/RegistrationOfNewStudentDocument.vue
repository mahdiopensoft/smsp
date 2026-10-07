<template>
  <!-- Main Title -->
  <div class="text-center mb-12 flex-grow-0">
    <div>
      مديرية: <strong>{{ output_data.district }}</strong>
    </div>
    <div class="mt-3 font-weight-bold">
      للعام الدراسي الجاري:
      <strong dir="ltr">{{ output_data.academic_year }}</strong>
    </div>
  </div>

  <!-- Certificate Body -->
  <div class="px-8 doc-body flex-grow-1" style="line-height: 2.4">
    <p class="text-justify">
      تشهد إدارة مدرسة
      <strong class="mx-2 px-2 pb-1 border-bottom-dotted">{{
        output_data.school_name
      }}</strong>
      بأن الطالب/ـة الموضحة بياناته أدناه قد استوفى كافة شروط القبول والتسجيل،
      وتم قيده رسمياً في سجلات المدرسة كطالب مستجد للعام الدراسي المذكور أعلاه.
    </p>

    <div
      class="mt-8 mb-8 pa-6"
      style="
        background-color: #fafafa;
        border: 2px solid #000;
        border-radius: 8px;
      "
    >
      <v-row>
        <v-col cols="12" md="8" class="py-2">
          الاسم الرباعي للطالب:
          <strong class="" style="border-bottom: 1px dotted #000">{{
            output_data.student_name
          }}</strong>
        </v-col>
        <v-col cols="12" md="4" class="py-2">
          الجنس:
          <strong>{{
            output_data.gender === 1
              ? "ذكر"
              : output_data.gender === 2
              ? "أنثى"
              : ""
          }}</strong>
        </v-col>
        <v-col cols="12" md="6" class="py-2">
          الرقم الوطني / الهوية:
          <strong>{{ output_data.identity_number }}</strong>
        </v-col>
        <v-col cols="12" md="6" class="py-2">
          تاريخ الميلاد:
          <strong dir="ltr">{{ output_data.date_of_birth }}</strong>
        </v-col>
        <v-col cols="12" md="6" class="py-2">
          الصف المسجل به: <strong>{{ output_data.enrolled_grade }}</strong>
        </v-col>
        <v-col cols="12" md="6" class="py-2">
          اسم ولي الأمر المفوّض:
          <strong>{{ output_data.guardian_name }}</strong>
        </v-col>
      </v-row>
    </div>

    <p class="text-justify mt-8">
      وقد أُعطي هذا الإشعار لولي الأمر كإثبات رسمي على قبول الطالب واكتمال
      إجراءاته الإدارية. نرجو من ولي الأمر مراجعة إدارة المدرسة في موعد أقصاه
      <strong dir="ltr">{{ output_data.attendance_deadline }}</strong> لمعرفة
      الجدول الدراسي واستلام الزي والكتب المدرسية.
    </p>
  </div>

  <!-- Footer Signatures -->
  <!-- <div class="flex-grow-0 pt-10 pb-6">
      <v-row class="text-center px-12 align-center">
        <v-col cols="4">
          <div class="font-weight-bold mb-8">مسؤول القبول والتسجيل</div>
          <div class="text-grey-darken-1">..............................</div>
          <div class="mt-2 font-weight-medium">
            {{ output_data.registrar_name }}
          </div>
        </v-col>
        <v-col cols="4" class="text-center position-relative">
          <div class="font-weight-bold mb-4">الختم الرسمي</div>
          <div class="mx-auto">ختم المدرسة الرسمي</div>
        </v-col>
        <v-col cols="4">
          <div class="font-weight-bold mb-8">مدير المدرسة / الوكيل</div>
          <div class="text-grey-darken-1">..............................</div>
          <div class="mt-2 font-weight-medium">
            {{ output_data.principal_name }}
          </div>
        </v-col>
      </v-row>
    </div> -->
</template>

<script>
export default {
  name: "RegistrationOfNewStudentDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
    };
  },
};
</script>

<style scoped>
.border-bottom-dotted {
  border-bottom: 2px dotted #000;
}
</style>
