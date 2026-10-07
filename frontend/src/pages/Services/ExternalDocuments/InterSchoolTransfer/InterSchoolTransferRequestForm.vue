<template>
  <v-container
    class="formal-doc pa-8"
    style="
      background-color: white;
      color: black;
      max-width: 210mm;
      margin: auto;
      border: 1px solid #ccc;
      font-family: &quot;Tajawal&quot;, &quot;Cairo&quot;, sans-serif;
    "
  >
    <!-- Document Header -->
    <v-row class="mb-4 align-center">
      <v-col cols="4" class="text-center">
        <div class="font-weight-bold">الجمهورية اليمنية</div>
        <div class="font-weight-bold">وزارة التربية والتعليم</div>
        <div>
          إدارة التربية والتعليم م/
          <strong>{{ input_data.governorate }}</strong>
        </div>
      </v-col>
      <v-col cols="4" class="text-center">
        <v-img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Emblem_of_Yemen.svg/1200px-Emblem_of_Yemen.svg.png"
          max-height="80"
          contain
        ></v-img>
      </v-col>
      <v-col cols="4" class="text-left">
        <div class="d-flex justify-end mb-2">
          <span class="ml-2">تاريخ الطلب:</span>
          <strong dir="ltr">{{ input_data.issue_date }}</strong>
        </div>
        <div class="d-flex justify-end">
          <span class="ml-2">الرقم المرجعي:</span>
          <strong dir="ltr">{{ input_data.request_number }}</strong>
        </div>
      </v-col>
    </v-row>

    <v-divider
      class="mb-6 border-opacity-100"
      color="black"
      thickness="2"
    ></v-divider>

    <!-- Document Title -->
    <div class="text-center mb-8">
      <h2 class="text-decoration-underline font-weight-bold pb-2">
        استمارة طلب نقل طالب بين المدارس
      </h2>
      <div class="text-subtitle-1">
        للعام الدراسي: <strong dir="ltr">{{ input_data.academic_year }}</strong>
      </div>
    </div>

    <!-- Main Content -->
    <div class="doc-body text-body-1" style="line-height: 2.2">
      <p>
        الإخوة / <strong>إدارة شؤون الطلاب بمكتب التربية المحترمين</strong>،
      </p>
      <p class="mb-6">
        أتقدم إليكم بطلب نقل ابني/ابنتي الموضحة بياناته أدناه من مدرسته الحالية
        إلى المدرسة المقترحة، وذلك للأسباب المذكورة في هذا الطلب، مع التعهدي
        بتوفير كافة الوثائق المطلوبة وبراءة الذمة من المدرسة السابقة فور
        الموافقة.
      </p>

      <!-- Student & Transfer Details -->
      <v-card
        variant="outlined"
        class="mb-6"
        style="border: 1px solid #000 !important"
      >
        <v-card-title
          class="py-2 font-weight-bold text-center"
          style="
            background-color: #f5f5f5;
            border-bottom: 1px solid #000;
            font-size: 1.1rem;
            color: #000;
          "
        >
          البيانات الأساسية للنقل
        </v-card-title>
        <v-card-text class="pa-4 text-black text-body-1">
          <v-row>
            <v-col cols="12" md="7" class="py-2">
              اسم الطالب الرباعي: <strong>{{ input_data.student_name }}</strong>
            </v-col>
            <v-col cols="12" md="5" class="py-2">
              الرقم الوطني / الهوية:
              <strong>{{ input_data.student_id }}</strong>
            </v-col>
            <v-col cols="12" md="6" class="py-2">
              الصف الدراسي الحالي:
              <strong>{{ input_data.current_grade }}</strong>
            </v-col>
            <v-col cols="12" md="6" class="py-2">
              اسم ولي الأمر: <strong>{{ input_data.guardian_name }}</strong>
            </v-col>
            <v-col cols="12" class="py-2">
              سبب النقل: <strong>{{ input_data.transfer_reason_text }}</strong>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Schools Details -->
      <v-row class="mb-6 mx-0">
        <!-- Current School -->
        <v-col cols="12" md="6" class="pl-md-3 px-0 pb-0">
          <v-card
            variant="outlined"
            class="h-100"
            style="border: 1px solid #000 !important"
          >
            <v-card-title
              class="py-2 font-weight-bold"
              style="
                background-color: #ffebee;
                border-bottom: 1px solid #000;
                font-size: 1rem;
                color: #000;
              "
            >
              المدرسة الحالية (المنقول منها)
            </v-card-title>
            <v-card-text class="pa-4 text-black text-body-1">
              <div class="mb-2">
                المدرسة: <strong>{{ input_data.current_school_name }}</strong>
              </div>
              <div class="mb-2">
                المديرية: <strong>{{ input_data.current_district }}</strong>
              </div>
              <div class="mb-2 d-flex align-center">
                موقف العهد والرسوم:
                <v-icon
                  :color="input_data.cleared_from_current ? 'success' : 'error'"
                  class="mx-2"
                  size="small"
                >
                  {{
                    input_data.cleared_from_current
                      ? "mdi-check-circle"
                      : "mdi-close-circle"
                  }}
                </v-icon>
                <strong>{{
                  input_data.cleared_from_current
                    ? "تمت التصفية (براءة ذمة)"
                    : "غير مصفر"
                }}</strong>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Target School -->
        <v-col cols="12" md="6" class="pr-md-3 px-0 pb-0 mt-4 mt-md-0">
          <v-card
            variant="outlined"
            class="h-100"
            style="border: 1px solid #000 !important"
          >
            <v-card-title
              class="py-2 font-weight-bold"
              style="
                background-color: #e8f5e9;
                border-bottom: 1px solid #000;
                font-size: 1rem;
                color: #000;
              "
            >
              المدرسة المطلوبة (المنقول إليها)
            </v-card-title>
            <v-card-text class="pa-4 text-black text-body-1">
              <div class="mb-2">
                المدرسة: <strong>{{ input_data.target_school_name }}</strong>
              </div>
              <div class="mb-2">
                المديرية: <strong>{{ input_data.target_district }}</strong>
              </div>
              <div class="mb-2">
                المنطقة التعليمية:
                <strong>{{ input_data.target_education_office }}</strong>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <div class="mb-2 mt-4 font-weight-bold">إقرار:</div>
      <p class="text-justify indent text-body-2 mb-8">
        أقر أنا ولي أمر الطالب المذكور أعلاه بصحة جميع البيانات، وأتحمل
        المسؤولية القانونية في حال ثبوت العكس. كما أعلم بأن عملية النقل غير
        مكتملة إلا بعد اعتماد المدرستين وإدارة التربية واستلام وثيقة النقل
        الرسمية.
      </p>
    </div>

    <!-- Signatures -->
    <v-row class="text-center mt-4 align-end pb-4">
      <v-col cols="4">
        <div class="font-weight-bold mb-8">توقيع ولي الأمر</div>
        <div class="text-grey-darken-1">..............................</div>
      </v-col>
      <v-col cols="4">
        <div class="font-weight-bold mb-8">موافق، المدرسة الحالية</div>
        <div class="text-grey-darken-1">
          الختم / التوقيع: ....................
        </div>
      </v-col>
      <v-col cols="4">
        <div class="font-weight-bold mb-8">موافق، المدرسة المطلوبة</div>
        <div class="text-grey-darken-1">
          الختم / التوقيع: ....................
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "InterSchoolTransferRequestForm",
  inject: {
    context: {
      default: () => ({}),
    },
  },
  data() {
    return {
      input_data: {},
    };
  },
  created() {
    const parentData = this.context?.input_data;
    const hasData = parentData && Object.keys(parentData).length > 0;

    if (hasData) {
      this.input_data = parentData;
    } else {
      // Mock Transfer Form Data
      this.input_data = {
        issue_date: "2024-08-10",
        request_number: "TRN-24-5501",
        academic_year: "2024 / 2025",
        governorate: "الأمانة",

        student_name: "علي سالم علي الحرازي",
        student_id: "0185994488",
        current_grade: "الصف الخامس الأساسي",
        guardian_name: "سالم علي الحرازي",
        transfer_reason_text: "تغيير سكن العائلة",

        current_school_name: "مدرسة عمر بن عبدالعزيز",
        current_district: "الوحدة",
        cleared_from_current: true,

        target_school_name: "مدرسة النهضة للتعليم الأساسي والثانوي",
        target_district: "السبعين",
        target_education_office: "مكتب التربية - منطقة السبعين",
      };
    }
  },
};
</script>

<style scoped>
.formal-doc {
  direction: rtl;
}

.indent {
  text-indent: 30px;
}

@media print {
  .formal-doc {
    border: none !important;
    box-shadow: none !important;
    max-width: 100% !important;
  }
}
</style>
