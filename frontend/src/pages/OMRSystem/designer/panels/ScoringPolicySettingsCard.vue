<template>
  <div class="scoring-policy-settings">
    <!-- Header Banner -->
    <div class="pa-4 rounded-xl border bg-surface mb-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
          <v-icon color="indigo" size="20">mdi-scale-balance</v-icon>
          سياسات التصحيح الأكاديمي واحتساب الدرجات
        </label>
        <v-chip size="x-small" color="indigo" variant="flat" class="font-weight-bold">
          مربوط بمحرك الدرجات
        </v-chip>
      </div>
      <p class="text-caption text-medium-emphasis mb-0">
        تحدد هذه القواعد كيف يتعامل النظام آلياً مع حالات التردد والتظليل المتعدد، الشطب، والدرجات السالبة.
      </p>
    </div>

    <!-- Case 1: Multiple Choices Marked (One Correct + One Wrong) -->
    <v-card variant="outlined" class="rounded-xl pa-4 mb-4 bg-surface">
      <div class="d-flex align-center gap-2 mb-2">
        <v-icon color="warning" size="20">mdi-checkbox-multiple-marked-outline</v-icon>
        <strong class="text-body-2 font-weight-bold">تظليل خيارين أحدهما صحيح والآخر خاطئ:</strong>
      </div>
      <span class="text-caption text-medium-emphasis d-block mb-3">
        عندما يظلل الطالب دائرتين في سؤال مفرد وتكون إحداهما هي الإجابة الصحيحة:
      </span>

      <v-radio-group v-model="scoring.multi_one_correct_policy" hide-details density="compact">
        <v-radio value="ZERO" color="error" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-error">إلغاء وتصفير السؤال (صفر) — [اللائحة الوزارية القياسية]</strong>
              <div class="text-caption text-medium-emphasis">يُعتبر السؤال ملغياً لمنع التخمين أو التذاكي.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="PARTIAL_50" color="primary" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-primary">منح نصف الدرجة (50%) للطالب</strong>
              <div class="text-caption text-medium-emphasis">مراعاة تردد الطالب ومنحه نصف علامة السؤال مع إحالة الورقة للكنترول للتأكيد.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="FLAG_REVIEW" color="amber-darken-3" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-amber-darken-3">تجميد الدرجة وإحالة السؤال للتدقيق البشري</strong>
              <div class="text-caption text-medium-emphasis">عرض صورة الفقاعتين أمام رئيس الكنترول للبت فيها يدوياً.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="SPLIT_PENALTY" color="secondary">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold">احتساب الدرجة مع خصم عقوبة الخطأ</strong>
              <div class="text-caption text-medium-emphasis">منح درجة الصواب مخصوماً منها نسبة عقوبة الخطأ.</div>
            </div>
          </template>
        </v-radio>
      </v-radio-group>
    </v-card>

    <!-- Case 2: Both Marked Choices are Wrong -->
    <v-card variant="outlined" class="rounded-xl pa-4 mb-4 bg-surface">
      <div class="d-flex align-center gap-2 mb-2">
        <v-icon color="error" size="20">mdi-close-octagon-outline</v-icon>
        <strong class="text-body-2 font-weight-bold">تظليل خيارين كلاهما خاطئ:</strong>
      </div>
      <span class="text-caption text-medium-emphasis d-block mb-3">
        عندما يظلل الطالب خيارين وليس أحدهما صحيحاً إطلاقاً:
      </span>

      <v-radio-group v-model="scoring.multi_both_wrong_policy" hide-details density="compact">
        <v-radio value="ZERO" color="grey-darken-2" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold">صفر فقط (0.00) بدون خصم سالب إضافي</strong>
              <div class="text-caption text-medium-emphasis">لا درجات ولا عقوبة سالبة مضاعفة.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="APPLY_PENALTY" color="warning" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-warning">تطبيق خصم الخطأ العادي</strong>
              <div class="text-caption text-medium-emphasis">يخصم عليه نسبة الإجابة الخاطئة المحددة أدناه.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="DOUBLE_PENALTY" color="error" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-error">عقوبة مضاعفة (عقوبة التحايل والتخمين)</strong>
              <div class="text-caption text-medium-emphasis">خصم مضاعف عن كلا الخيارين الخاطئين لردع التخمين العشوائي.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="FLAG_REVIEW" color="amber-darken-3">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-amber-darken-3">تحويل للتدقيق لكشف شبهة التخمين الشامل</strong>
              <div class="text-caption text-medium-emphasis">تنبيه لجان الكنترول بوجود نمط تظليل غير منضبط.</div>
            </div>
          </template>
        </v-radio>
      </v-radio-group>
    </v-card>

    <!-- Case 3: Crossed-Out Choice (الشطب بالقلم) -->
    <v-card variant="outlined" class="rounded-xl pa-4 mb-4 bg-surface">
      <div class="d-flex align-center gap-2 mb-2">
        <v-icon color="teal" size="20">mdi-close-box-outline</v-icon>
        <strong class="text-body-2 font-weight-bold">شطب خيار بالقلم (X) وتظليل خيار بديل:</strong>
      </div>
      <span class="text-caption text-medium-emphasis d-block mb-3">
        عندما يشطب الطالب على إجابة ويظلل إجابة أخرى في نفس السؤال:
      </span>

      <v-radio-group v-model="scoring.crossed_choice_policy" hide-details density="compact">
        <v-radio value="ACCEPT_FILLED" color="success" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-success">اعتماد المظلل وتجاهل المشطوب آلياً بالذكاء الاصطناعي</strong>
              <div class="text-caption text-medium-emphasis">يتعرف YOLO/CNN على الشطب ويلغي الدائرة المشطوبة ويعتمد البديل فوراً.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="FLAG_REVIEW" color="amber-darken-3" class="mb-2">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-amber-darken-3">إرسال صورة الشطب للكنترول للتحقق البشري</strong>
              <div class="text-caption text-medium-emphasis">إظهار الدائرة المشطوبة والمظللة للمصحح لاعتماد نية الطالب يدوياً.</div>
            </div>
          </template>
        </v-radio>
        <v-radio value="DISQUALIFY" color="error">
          <template #label>
            <div>
              <strong class="text-caption font-weight-bold text-error">إلغاء السؤال وتصفيره (حظر الشطب باللائحة)</strong>
              <div class="text-caption text-medium-emphasis">معاملة أي شطب كمخالفة لقواعد التظليل بالورقة.</div>
            </div>
          </template>
        </v-radio>
      </v-radio-group>
    </v-card>

    <!-- Case 4: Negative Marking Ratio -->
    <v-card variant="outlined" class="rounded-xl pa-4 mb-4 bg-surface">
      <div class="d-flex justify-space-between align-center mb-2">
        <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
          <v-icon color="purple" size="20">mdi-minus-circle-outline</v-icon>
          عقوبة الإجابة الخاطئة (الدرجات السالبة / التخمين)
        </label>
        <v-chip size="x-small" :color="scoring.wrong_answer_penalty > 0 ? 'error' : 'grey'" class="font-weight-black">
          {{ scoring.wrong_answer_penalty > 0 ? `خصم ${(scoring.wrong_answer_penalty * 100).toFixed(0)}%` : 'بدون خصم' }}
        </v-chip>
      </div>

      <div class="d-flex gap-2 flex-wrap mb-3">
        <v-btn
          size="x-small"
          :variant="scoring.wrong_answer_penalty === 0.0 ? 'flat' : 'outlined'"
          :color="scoring.wrong_answer_penalty === 0.0 ? 'primary' : 'default'"
          class="font-weight-bold"
          @click="scoring.wrong_answer_penalty = 0.0"
        >
          بدون خصم (0%)
        </v-btn>
        <v-btn
          size="x-small"
          :variant="scoring.wrong_answer_penalty === 0.25 ? 'flat' : 'outlined'"
          :color="scoring.wrong_answer_penalty === 0.25 ? 'error' : 'default'"
          class="font-weight-bold"
          @click="scoring.wrong_answer_penalty = 0.25"
        >
          خصم ربع درجة (25%)
        </v-btn>
        <v-btn
          size="x-small"
          :variant="scoring.wrong_answer_penalty === 0.33 ? 'flat' : 'outlined'"
          :color="scoring.wrong_answer_penalty === 0.33 ? 'error' : 'default'"
          class="font-weight-bold"
          @click="scoring.wrong_answer_penalty = 0.33"
        >
          خصم ثلث درجة (33%)
        </v-btn>
        <v-btn
          size="x-small"
          :variant="scoring.wrong_answer_penalty === 0.50 ? 'flat' : 'outlined'"
          :color="scoring.wrong_answer_penalty === 0.50 ? 'error' : 'default'"
          class="font-weight-bold"
          @click="scoring.wrong_answer_penalty = 0.50"
        >
          خصم نصف درجة (50%)
        </v-btn>
      </div>

      <!-- Floor mode toggle -->
      <div v-if="scoring.wrong_answer_penalty > 0" class="pa-3 rounded-lg bg-grey-lighten-4 mt-2">
        <div class="text-caption font-weight-bold mb-1">الحد الأدنى لدرجة السؤال عند الخصم:</div>
        <v-radio-group v-model="scoring.score_floor_mode" hide-details density="compact">
          <v-radio value="PER_QUESTION_ZERO" color="primary">
            <template #label>
              <span class="text-caption">درجة السؤال لا تقل عن صفر (حماية: لا تصبح سالبة لكل سؤال).</span>
            </template>
          </v-radio>
          <v-radio value="ALLOW_NEGATIVE" color="error">
            <template #label>
              <span class="text-caption">السماح بالدرجة السالبة لتخصم من المجموع الكلي للاختبار.</span>
            </template>
          </v-radio>
        </v-radio-group>
      </div>
    </v-card>

    <!-- Case 5: Faint / Half-filled Marks -->
    <v-card variant="outlined" class="rounded-xl pa-4 mb-4 bg-surface">
      <div class="d-flex align-center gap-2 mb-2">
        <v-icon color="blue-grey" size="20">mdi-circle-half-full</v-icon>
        <strong class="text-body-2 font-weight-bold">التظليل الباهت أو المتردد (Faint / Half-filled):</strong>
      </div>
      <v-radio-group v-model="scoring.half_filled_policy" hide-details density="compact">
        <v-radio value="FLAG_REVIEW" color="primary" class="mb-2">
          <template #label>
            <span class="text-caption font-weight-bold">إحالة للتدقيق البشري لضمان عدم ظلم الطالب في حال ضعف قلمه.</span>
          </template>
        </v-radio>
        <v-radio value="REJECT_EMPTY" color="grey-darken-2">
          <template #label>
            <span class="text-caption">اعتباره فارغاً وغير معتمد تلقائياً.</span>
          </template>
        </v-radio>
      </v-radio-group>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  config: any
}>()

// Initialize nested omr_config and scoring structure safely
if (!props.config.omr_config) {
  props.config.omr_config = {}
}
if (!props.config.omr_config.scoring) {
  props.config.omr_config.scoring = {
    wrong_answer_penalty: 0.0,
    score_floor_mode: 'PER_QUESTION_ZERO',
    multi_one_correct_policy: 'ZERO',
    multi_both_wrong_policy: 'ZERO',
    crossed_choice_policy: 'ACCEPT_FILLED',
    erased_choice_policy: 'ACCEPT_FILLED',
    blank_answer_penalty: 0.0,
    half_filled_policy: 'FLAG_REVIEW',
  }
}

const scoring = computed(() => props.config.omr_config.scoring)
</script>
