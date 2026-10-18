<template>
  <v-switch
    :model-value="data?.is_approved"
    color="primary"
    style="pointer-events: visible !important"
    true-icon="mdi-check"
    false-icon="mdi-close"
    @update:modelValue="approveUser.show = true"
    hideDetails
  >
    <template v-slot:label>
      {{
        data?.is_approved ? `مصادق حتى تاريخ ${data?.approved_to ?? ""}` : "غير مصادق "
      }}
    </template>
  </v-switch>

  <custom-dialog
    v-if="!data.is_approved"
    v-model="approveUser.show"
    title="مصاقة المدير"
    width="500"
    height="auto"
    class="px-2"
  >
    <template v-slot>
      <custom-date
        v-model="data['approved_to']"
        label="تاريخ انتهاء الصلاحية"
        hideDetails="auto"
      />
    </template>
    <template v-slot:actions>
      <custom-btn type="save" width="95%" class="mx-2" :click="approveManager" />
    </template>
  </custom-dialog>

  <confirm-dialog
    v-if="data.is_approved"
    v-model="approveUser.show"
    title="تاكيد الغاء المصادقة"
    icon="information"
    color="primary"
    message="هلا انت متاكد من الغاء مصادفة المستخدم"
    :confirmBtn="approveManager"
  />
</template>
<script setup>
import { ref, watch } from "vue";
import api from "../../../../../plugins/axios-plugin";
import { alert, showSnackBar } from "../../../../utils/Globals";

const props = defineProps({
  userId: Number,
  is_approved: Boolean,
  approved_to: String,
});

const emit = defineEmits(["changeApproved"]);

const data = ref({
  is_approved: props.is_approved,
  approved_to: props.approved_to,
});

const approveUser = ref({
  show: false,
  loading: false,
});

const approveManager = async () => {
  try {
    approveUser.value.loading = true;
    const method = data.value?.is_approved ? "unapprove" : "approve";

    const response = await api.post(`user-manager/users/${props.userId}/${method}/ `, {
      approved_to: data.value?.["approved_to"],
    });

    approveUser.value.show = false;
    if (data.value) {
      data.value.is_approved = !data.value?.is_approved;
      if (method === "unapprove") {
        data.value.approved_to = null;
      }
    }

    alert("add", { message: response?.data?.message });
    showSnackBar();

    emit("changeApproved", data.value.is_approved, data.value.approved_to);
  } finally {
    approveUser.value.loading = false;
  }
};

watch(
  () => props.is_approved,
  (val) => {
    data.value.is_approved = val;
  }
);
watch(
  () => props.approved_to,
  (val) => {
    data.value.approved_to = val;
  }
);
</script>
