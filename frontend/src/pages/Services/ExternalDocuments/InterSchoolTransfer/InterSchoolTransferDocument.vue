<template>

    <!-- Main Title -->
    <div class="text-center mb-10 flex-grow-0">
      <div class="mt-2 text-subtitle-1">
        وثيقة نهائية مخصصة لتسليم ملف الطالب
      </div>
    </div>

    <!-- Document Body -->
    <div class="px-8 doc-body text-h6 flex-grow-1" style="line-height: 2.2">
      <p>
        الأخ مكرم مدير مدرسة /
        <strong class="mx-2 px-2 pb-1 border-bottom-dotted">{{
          output_data.target_school_name
        }}</strong>
        المحترم،
      </p>

      <p class="text-justify indent mt-6">
        تحية طيِّبة وبعد،،<br />
        بناءً على الطلب المقدم من ولي أمر الطالب، وإشارةً إلى موافقة إدارة
        المدرسة السابقة باستيفاء كافة الرسوم والالتزامات الأكاديمية، نفيدكم بأنه لا مانع لدينا من الجانب الإداري والفني من الموافقة على
        نقل ملف الطالب الموضحة بياناته أدناه إلى مدرستكم:
      </p>

      <div
        class="mt-8 mb-6 pa-6"
        style="
          background-color: #fafafa;
          border: 2px solid #000;
          border-radius: 8px;
        "
      >
        <v-row>
          <v-col cols="12" md="7" class="py-2">
            الاسم الكامل:
            <strong class="text-h6" style="border-bottom: 1px dotted #000">{{
              output_data.student_name
            }}</strong>
          </v-col>
          <v-col cols="12" md="5" class="py-2">
            الرقم المدرسي الشامل:
            <strong>{{ output_data.student_global_id }}</strong>
          </v-col>
          <v-col cols="12" md="6" class="py-2">
            المدرسة المنتقل منها:
            <strong>{{ output_data.source_school_name }}</strong>
          </v-col>
          <v-col cols="12" md="6" class="py-2">
            الصف الدراسي الحالي:
            <strong>{{ output_data.current_grade }}</strong>
          </v-col>
        </v-row>
      </div>

      <p class="text-justify mt-6 text-body-1 font-weight-bold">
        وعليه، نأمل منكم استلام ملف الطالب الورقي، واعتماد تسجيله رسمياً في
        كشوفات مدرستكم.
        <br /><br />
        وتقبلوا خالص التحية والتقدير،،،
      </p>
    </div>

    <!-- Signatures -->
    <!-- <div class="flex-grow-0 pt-10 pb-6 px-8">
      <v-row class="text-center align-center font-weight-bold mx-0">
        <v-col cols="4" class="px-1 text-center border-right">
          <div class="mb-8">المدير المنقول منه الطالب</div>
          <div class="text-grey-darken-1 mb-2">
            ..............................
          </div>
          <div>{{ output_data.source_school_principal }}</div>
        </v-col>

        <v-col cols="4" class="px-1 text-center position-relative">
          <div class="mb-4">مدير إدارة التربية / قسم الانتقالات</div>
          <div class="stamp-circle mx-auto">
            إدارة<br />التربية<br />والتعليم
          </div>
        </v-col>

        <v-col cols="4" class="px-1 text-center border-left">
          <div class="mb-8">المدير المنتهى إليه (للاعتماد)</div>
          <div class="text-grey-darken-1 mb-2">
            ..............................
          </div>
          <div>{{ output_data.target_school_principal }}</div>
        </v-col>
      </v-row>
    </div> -->
</template>

<script>
export default {
  name: "InterSchoolTransferDocument",
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

.border-right {
  border-right: 1px dotted #ccc;
}
.border-left {
  border-left: 1px dotted #ccc;
}

.stamp-circle {
  width: 90px;
  height: 90px;
  border: 4px double #b71c1c;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #b71c1c;
  font-weight: 900;
  font-size: 0.9rem;
  opacity: 0.8;
  transform: rotate(-5deg);
  text-align: center;
  line-height: 1.2;
}

@media print {
  .formal-doc {
    box-shadow: none !important;
    border: 1px double #000 !important;
  }
  .bg-grey-lighten-4 {
    background-color: transparent !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .stamp-circle {
    color: #b71c1c !important;
    border-color: #b71c1c !important;
  }
  .border-right,
  .border-left {
    border-color: transparent !important;
  }
}
</style>
