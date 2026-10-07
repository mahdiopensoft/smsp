<template>

    <!-- Main Title -->
    <div class="text-center mb-10 flex-grow-0">
      <div class="mt-2 text-subtitle-1 font-weight-bold">
        نظام الزي الموحد - العام
        <strong dir="ltr">{{ output_data.academic_year }}</strong>
      </div>
    </div>

    <!-- Document Body -->
    <div class="px-6 doc-body text-h6 flex-grow-1" style="line-height: 2.2">
      <p class="text-justify indent mb-6">
        تم في هذا اليوم تسليم قطع الزي المدرسي للطالب الموضحة هويته أدناه، من
        المخزن الإداري للمدرسة. وتعتبر هذه الوثيقة إخلاء طرف للمخزن وإبراء ذمة
        مالية بقيمة الزي المنصرف.
      </p>

      <!-- Student Card -->
      <div
        class="mb-6 pa-5"
        style="
          border: 1px dotted #000;
          border-radius: 4px;
          background-color: #fafafa;
        "
      >
        <v-row class="mx-0">
          <v-col cols="12" md="8" class="py-1">
            اسم الطالب المستلم:
            <strong class="text-h6 border-bottom-dotted">{{
              output_data.student_name
            }}</strong>
          </v-col>
          <v-col cols="12" md="4" class="py-1">
            الجنس: <strong>{{ output_data.gender }}</strong>
          </v-col>
          <v-col cols="12" md="5" class="py-1">
            الصف المسجل به: <strong>{{ output_data.fk_branch_class }}</strong>
          </v-col>
          <v-col cols="12" md="7" class="py-1 text-primary font-weight-bold">
            نوع الزي المنصرف:
            <strong>{{ output_data.gender_uniform_type }}</strong>
          </v-col>
        </v-row>
      </div>

      <!-- Items Delivered Table -->
      <div class="mb-4 mt-6 font-weight-bold">
        تفاصيل الأصناف المُسَلَّمة الفِعليَّة:
      </div>
      <table class="items-table w-100 mb-8 text-body-1">
        <thead>
          <tr>
            <th width="10%">م</th>
            <th width="35%">اسم الزي</th>
            <th width="20%">اللون</th>
            <th width="15%">المقاس</th>
            <th width="10%">الكمية</th>
            <th width="10%">السعر</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="text-center font-weight-bold">{{ 1 }}</td>
            <td class="font-weight-medium">{{ output_data.uniform_name }}</td>
            <td class="text-center" dir="ltr">{{ output_data.color }}</td>
            <td class="text-center font-weight-bold" dir="ltr">
              {{ output_data.size }}
            </td>
            <td class="text-center">{{ output_data.quantity }}</td>
            <td class="text-center" dir="ltr">
              {{ output_data.is_paid }}
            </td>
          </tr>
          <!-- Empty rows for padding if few items -->
          <tr
            v-if="
              output_data.delivered_items &&
              output_data.delivered_items.length < 4
            "
          >
            <td>&nbsp;</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>

      <p
        class="text-justify text-body-2 font-weight-bold mt-6"
        style="line-height: 1.8"
      >
        يقر المستلم المذكور أدناه بأنه قد استلم الزي بحالة ممتازة وجديدة وذات
        جودة مطابقة للمواصفات، وأنه على علم بسياسة الاستبدال خلال (<strong
          dir="ltr"
          >3</strong
        >) أيام فقط.
      </p>
    </div>

    <!-- Footer Signatures -->
    <!-- <div class="flex-grow-0 pt-6 pb-6 px-12">
      <v-row class="text-center align-center font-weight-bold mx-0">
        <v-col cols="4" class="px-1 text-center">
          <div class="mb-8">توقيع المستلم للعهد (ولي الأمر)</div>
          <div class="text-grey-darken-1 mb-2">
            الاسم: ..............................
          </div>
          <div class="text-grey-darken-1">
            التوقيع: ..............................
          </div>
        </v-col>

        <v-col cols="4" class="px-1 text-center position-relative">
          <div class="stamp-circle mx-auto">
            صُرِف<br />مخازن<br />الزي والقرطاسية
          </div>
        </v-col>

        <v-col cols="4" class="px-1 text-center">
          <div class="mb-8">أمين المخزن (المُسَلِّم)</div>
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
  name: "SchoolUniformDistributionDocument",
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

.indent {
  text-indent: 40px;
}

.box-numbering {
  border: 1px solid #000;
  padding: 4px 10px;
  background-color: #f1f8e9; /* optional light highlight */
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
  background-color: #bbdefb;
  color: #000;
}

.stamp-circle {
  width: 90px;
  height: 90px;
  border: 4px dashed #0277bd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0277bd;
  font-weight: 900;
  font-size: 0.85rem;
  opacity: 0.9;
  transform: rotate(-10deg);
  text-align: center;
  line-height: 1.2;
}
</style>
