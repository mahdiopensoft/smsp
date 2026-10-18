<template>
  <CustomDialog width="300" height="300" :title="$t('change_password')">
    <template #activator="slotProps">
      <custom-btn
        v-bind="slotProps.props"
        type="update"
        label="تغيير كلة المرور"
        class="mt-3"
        style="pointer-events: visible !important"
      />
    </template>

    <template v-slot>
      <VForm ref="formPass" @submit.prevent="changePassword">
        <custom-text-field
          v-model="password.new_password"
          icon="lock"
          type="password"
          :rules="[$required, $valid_pass]"
          :label="$t('new_pass')"
        >
        </custom-text-field>
      </VForm>
    </template>
    <template v-slot:actions>
      <custom-btn
        type="update"
        :label="$t('change')"
        :click="changePassword"
        width="100%"
        class="mb-1"
      />
    </template>
  </CustomDialog>
</template>
<script setup>
import { ref } from "vue";
import api from "../../../../../plugins/axios-plugin";
import { alert, showSnackBar } from "../../../../utils/Globals";

const props = defineProps({
  userId: Number,
});

const formPass = ref(null);
const password = ref({});
const loadingActive = ref(false);

const changePassword = async () => {
  const { valid } = await formPass.value.validate();
  if (!valid) return;

  await api
    .post(`user-manager/users/${props.userId}/admin-change-password/`, {
      new_password: password.value.new_password,
    })
    .then(() => {
      alert("update");
      showSnackBar();
      password.value = {};
    });
};
</script>
