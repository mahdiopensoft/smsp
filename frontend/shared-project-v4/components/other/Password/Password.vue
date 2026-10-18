<template>
  <v-form v-model="isFormValid" @submit.prevent="changePassword">
    <div>
      <slot name="top"></slot>

      <v-text-field
        v-model="model.new_password"
        label="كلمة المرور"
        prepend-inner-icon="mdi-lock"
        :type="showPassword ? 'text' : 'password'"
        :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="showPassword = !showPassword"
        :rules="[$required]"
        variant="outlined"
        density="compact"
        clearable
      />

      <!-- قائمة التحقق الذكية (Validation Checklist) -->
      <v-expand-transition
        ><div v-if="model.new_password?.length > 0" class="password-rules mt-4 px-2">
          <div
            v-for="(rule, index) in passwordRules"
            :key="index"
            class="rule-item d-flex align-center mb-1 transition-swing"
            :class="
              rule.check(model.new_password) ? 'text-success' : 'text-grey-darken-1'
            "
          >
            <v-icon size="14" class="me-2">
              {{
                rule.check(model.new_password) ? "mdi-check-circle" : "mdi-circle-outline"
              }}
            </v-icon>

            <span class="text-caption font-weight-medium">
              {{ rule.label }}
            </span>
          </div>
        </div>
      </v-expand-transition>

      <custom-btn
        type="update"
        :is_submit="true"
        label="تغيير كلمة المرور"
        width="100%"
        :click="changePassword"
      >
      </custom-btn>
    </div>
  </v-form>
</template>
<script setup>
import { ref } from "vue";
import api from "../../../plugins/axios-plugin";
import { showSnackBar, alert } from "../../../src/utils/Globals";

const props = defineProps({
  id: Number,
});

const model = defineModel();

const emit = defineEmits(["update:modelValue"]);

const showPassword = ref(false);
// قواعد التحقق المتقدمة
const passwordRules = [
  { label: "على الأقل 8 أحرف", check: (p) => p.length >= 8 },
  {
    label: "حرف كبير (A) وحرف صغير (a)",
    check: (p) => /[A-Z]/.test(p) && /[a-z]/.test(p),
  },
  { label: "رقم واحد على الأقل (0-9)", check: (p) => /[0-9]/.test(p) },
  {
    label: "رمز خاص واحد (@, #, !...)",
    check: (p) => /[!@#$%^&*(),.?":{}|<>]/.test(p),
  },
  {
    label: "لا يحتوي على تكرار مفرط (مثل 111)",
    check: (p) => !/(.)\1\1/.test(p),
  },
  { label: "ليست أرقاماً فقط", check: (p) => /[a-zA-Z]/.test(p) },
  //   {
  //     label: "لا تشبه بيانات المستخدم (البريد)",
  //     check: (p) =>
  //       model.value ? !p.includes(model.value.split("@")[0]) : true,
  //   },
];

const isFormValid = ref(null);
const loading = ref(false);

const isPaswordValid = (pass) => {
  return passwordRules.every((rule) => rule.check(pass) === true);
};
const changePassword = async () => {
  if (!isFormValid.value) return;

  if (!isPaswordValid(model.value?.new_password)) {
    alert("errorData", { message: "يجب استيفاء كافة الشروط" });
    showSnackBar();
    return;
  }

  await api.post(`user-manager/users/${props.id}/admin-change-password/`, {
    ...model.value,
  });
  alert("update");
  showSnackBar();
};
</script>
<style scoped>
/* انميشن بسيط لتغير الحالة */
.transition-swing {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.password-rules {
  display: flex;
  flex-wrap: wrap;

  overflow-y: auto;
}

.rule-item {
  width: 100%;
}
</style>
