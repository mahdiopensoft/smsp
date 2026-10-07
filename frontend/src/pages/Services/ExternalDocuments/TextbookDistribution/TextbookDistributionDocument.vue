<template>

    <!-- Main Title -->
    <div class="text-center mb-10 flex-grow-0">
      <div class="mt-2 text-subtitle-1">
        إخلاء عهدة مخزنية (مطبوعات) للعام
        <strong dir="ltr">{{ output_data.academic_year }}</strong> - فصل دراسي
        ({{ output_data.semester }})
      </div>
    </div>

    <!-- Document Body -->
    <div class="px-6 doc-body text-h6 flex-grow-1" style="line-height: 2.2">
      <p class="text-justify indent mb-6">
        تم صرف وتسليم المقررات المدرسية للطالب الموضحة بياناته أدناه، وذلك بعد
        التحقق من استيفائه لشروط التسجيل وبراءة الذمة المالية والمخزنية الخاصة
        بالأعوام المنصرمة.
      </p>

      <!-- Student Card -->
      <div
        class="mb-6 pa-5"
        style="border: 1px dashed #000; border-radius: 4px"
      >
        <v-row class="mx-0">
          <v-col cols="12" md="8" class="py-1">
            مستلم العهدة (الطالب/ة):
            <strong>{{ output_data.student_name }}</strong>
          </v-col>
          <v-col cols="12" md="4" class="py-1">
            الرقم المدرسي:
            <strong dir="ltr">{{ output_data.academic_number }}</strong>
          </v-col>
          <v-col cols="12" md="6" class="py-1">
            الصف المسجل به: <strong>{{ output_data.fk_branch_class }}</strong>
          </v-col>
          <v-col cols="12" md="6" class="py-1">
            الشعبة: <strong>{{ output_data.fk_division_name }}</strong>
          </v-col>
        </v-row>
      </div>

      <!-- Items Table -->
      <div class="mb-8 font-weight-bold">بيان الأصناف المنصرفة:</div>
      <table class="items-table w-100 mb-8 text-body-1">
        <thead>
          <tr>
            <th width="10%">م</th>
            <th width="50%">اسم الكتاب / المقرر</th>
            <th width="10%">الكمية</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in output_data.items_received" :key="index">
            <td class="text-center font-weight-bold">{{ index + 1 }}</td>
            <td class="font-weight-medium">{{ item.book_name }}</td>
            <td class="text-center">{{ item.quantity }}</td>
          </tr>
        </tbody>
      </table>

      <p class="text-justify text-body-2 font-weight-bold mt-8">
        * إقرار استلام: أقر أنا الموقع أدناه باستلام جميع الكتب الموضحة أعلاه
        وهي في حالة سليمة، وأتعهد بالمحافظة عليها من التمزق والتلف، وإعادتها فور
        طلب المدرسة أو بنهاية العام الدراسي كشرط قانوني لإخلاء العهدة.
      </p>
    </div>

    <!-- Footer Signatures -->
    <!-- <div class="flex-grow-0 pt-6 pb-6 px-12">
      <v-row class="text-center align-center font-weight-bold mx-0">
        <v-col cols="4" class="px-1 text-center">
          <div class="mb-8">إقرار المستلم</div>
          <div class="text-grey-darken-1 mb-2">
            الاسم: ..............................
          </div>
          <div class="text-grey-darken-1">
            التوقيع: ..............................
          </div>
        </v-col>

        <v-col cols="4" class="px-1 text-center position-relative">
          <div class="stamp-circle mx-auto">
            أمين<br />المخازن<br />Education Store
          </div>
        </v-col>

        <v-col cols="4" class="px-1 text-center">
          <div class="mb-8">أمين المكتبة / المخزن</div>
          <div class="text-grey-darken-1 mb-2">
            ..............................
          </div>
          <div>{{ output_data.store_keeper_name }}</div>
        </v-col>
      </v-row>
    </div> -->
</template>

<script>
export default {
  name: "TextbookDistributionDocument",
  inject: ["context"],
  data() {
    return {
      output_data: this.context?.output_data ?? {},
    };
  },
};
</script>

<style scoped>
.indent {
  text-indent: 40px;
}

.box-numbering {
  border: 1px solid #000;
  padding: 4px 10px;
  background-color: #fce4ec; /* optional light highlight */
}

.items-table {
  border-collapse: collapse;
}

.items-table th,
.items-table td {
  border: 1px solid #000;
  padding: 8px 12px;
}

.items-table th {
  background-color: #e0e0e0;
  color: #000;
}

.stamp-circle {
  width: 90px;
  height: 90px;
  border: 4px solid #1565c0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1565c0;
  font-weight: 900;
  font-size: 0.85rem;
  opacity: 0.8;
  transform: rotate(15deg);
  text-align: center;
  line-height: 1.2;
}
</style>
