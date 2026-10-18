<template>
  <v-switch
    :model-value="data?.is_active"
    color="primary"
    style="pointer-events: visible !important"
    true-icon="mdi-check"
    false-icon="mdi-close"
    hideDetails
    width="150"
    class="px-5"
    @change="toggleActive"
  >
    <template v-slot:label>
      {{ data?.is_active ? "مفعل" : "غير مفعل" }}
      <v-progress-circular v-if="loadingActive" indeterminate size="20" />
    </template>
  </v-switch>
</template>
<script setup>
import { ref, watch } from "vue";
import usersApi from "../../../../UserManagement/api/users";
import { alert, showSnackBar } from "../../../../utils/Globals";

const props = defineProps({
  userId: Number,
  active: Boolean,
});

const emit = defineEmits(["changeActive"]);
const data = ref({
  is_active: props.active,
});

const loadingActive = ref(false);

const toggleActive = async () => {
  try {
    loadingActive.value = true;
    await usersApi.toggleActive(props.userId);

    if (data?.value) {
      data.value.is_active = !data?.value.is_active || false;
    }

    emit("changeActive", data.value.is_active);

    alert("success", {
      message: `تم ${data.value?.is_active ? "تفعيل" : "إلغاء تفعيل"} المستخدم`,
    });
    showSnackBar();
  } finally {
    loadingActive.value = false;
  }
};

watch(
  () => props.active,
  (val) => {
    data.value.is_active = val;
  }
);
</script>
