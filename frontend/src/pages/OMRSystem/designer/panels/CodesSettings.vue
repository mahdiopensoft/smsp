<template>
  <div class="codes-settings">
    <!-- 1D Linear Barcode Settings -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">الباركود الخطي (1D Linear Barcode)</label>
        <v-switch
          v-model="config.barcode.enabled"
          color="primary"
          hide-details
          density="compact"
        />
      </div>
      <template v-if="config.barcode.enabled">
        <p class="text-caption text-medium-emphasis mb-3">
          يُطبع في أسفل الورقة لربط رقم الجلوس وكود القالب آلياً بماسح الباركود السريع.
        </p>
        <v-text-field
          v-model="config.barcode.value"
          label="قيمة الباركود المشفرة"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-select
          v-model="config.barcode.format"
          :items="['CODE128', 'CODE39', 'EAN13']"
          label="صيغة التشفير (Encoding)"
          variant="outlined"
          density="compact"
          rounded="lg"
          hide-details
        />
      </template>
    </div>

    <!-- 2D QR Code Settings -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">رمز الاستجابة السريعة (2D QR Code)</label>
        <v-switch
          v-model="config.qr.enabled"
          color="primary"
          hide-details
          density="compact"
        />
      </div>
      <template v-if="config.qr.enabled">
        <p class="text-caption text-medium-emphasis mb-3">
          يحتوي على بصمة التحقق الرقمية للامتحان والطالب لمنع التزوير أو تبديل الأوراق.
        </p>
        <v-text-field
          v-model="config.qr.value"
          label="البيانات المشفرة بالـ QR"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-select
          v-model="config.qr.ecc"
          :items="['L', 'M', 'Q', 'H']"
          label="مستوى تصحيح الأخطاء (Error Correction)"
          variant="outlined"
          density="compact"
          rounded="lg"
          hide-details
        />
      </template>
    </div>

    <!-- Shading Instructions & Rules Settings -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">تعليمات وتنبيهات تظليل ورقة الإجابة (Ministry Instructions & Rules)</label>
        <v-icon color="primary" size="20">mdi-format-list-checks</v-icon>
      </div>
      <p class="text-caption text-medium-emphasis mb-3">
        تخصيص قواعد وتنبيهات التظليل المطبوعة في صندوق التعليمات أسفل ورقة الإجابة.
      </p>

      <v-text-field
        v-model="config.instructions.rule1"
        label="التعليمة 1: تظليل الدائرة كاملاً بالقلم الجاف (Rule 1)"
        placeholder="1- يجب أن يكون تظليل الدائرة بقلم جاف أسود أو أزرق بشكل كامل مثال:"
        variant="outlined"
        density="compact"
        rounded="lg"
        class="mb-3"
        hide-details
      />

      <v-text-field
        v-model="config.instructions.correct_label"
        label="كلمة توضيح النموذج الصحيح (Correct Label)"
        placeholder="واجب"
        variant="outlined"
        density="compact"
        rounded="lg"
        class="mb-3"
        hide-details
      />

      <v-text-field
        v-model="config.instructions.rule2"
        label="التعليمة 2: التأكد من مكان التظليل (Rule 2)"
        placeholder="2 - تأكد من تظليل إجاباتك في الأماكن المخصصة لها."
        variant="outlined"
        density="compact"
        rounded="lg"
        class="mb-3"
        hide-details
      />

      <v-text-field
        v-model="config.instructions.rule3"
        label="التعليمة 3: منع المصحح (Rule 3)"
        placeholder="3 - يمنع استخدام المصحح."
        variant="outlined"
        density="compact"
        rounded="lg"
        class="mb-3"
        hide-details
      />

      <v-text-field
        v-model="config.instructions.rule4"
        label="التعليمة 4: عدم قبول الإجابات مالم تسجل (Rule 4)"
        placeholder="4 - لن تقبل الإجابات مالم تسجل على هذه الورقة، اترك لنفسك وقتاً كافياً لنقل الإجابات."
        variant="outlined"
        density="compact"
        rounded="lg"
        class="mb-3"
        hide-details
      />

      <v-divider class="my-3" />

      <div class="d-flex align-center justify-space-between">
        <div>
          <div class="text-caption font-weight-bold">محاكاة خط يد الطالب في خانة الاسم</div>
          <div class="text-caption text-medium-emphasis">
            عند التعطيل، تبقى الخانة فارغة تماماً ليقوم الطالب بكتابة اسمه يدوياً بالقلم.
          </div>
        </div>
        <v-switch
          v-model="config.instructions.show_simulated_handwriting"
          color="primary"
          hide-details
          density="compact"
        />
      </div>
    </div>

    <!-- Fiducial Markers -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold">علامات المحاذاة البصرية (Optical Fiducials)</label>
        <v-chip size="x-small" color="success" variant="flat" class="font-weight-bold">4 زوايا إجبارية</v-chip>
      </div>
      <p class="text-caption text-medium-emphasis mb-0">
        أربع مربعات سوداء صلبة مطبوعة في الأركان الأربعة للورقة مع منطقة أمان بيضاء معزولة (Quiet Zones)، يعتمد عليها محرك OpenCV في الكشف وتصحيح زاوية الميلان والانحراف المنظوري (Perspective Transform) بدقة 100%.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  config: any
}>()

if (!props.config.instructions) {
  props.config.instructions = {
    rule1: '1- يجب أن يكون تظليل الدائرة بقلم جاف أسود أو أزرق بشكل كامل مثال:',
    correct_label: 'واجب',
    rule2: '2 - تأكد من تظليل إجاباتك في الأماكن المخصصة لها.',
    rule3: '3 - يمنع استخدام المصحح.',
    rule4: '4 - لن تقبل الإجابات مالم تسجل على هذه الورقة، اترك لنفسك وقتاً كافياً لنقل الإجابات.',
    show_simulated_handwriting: false,
  }
}
</script>
