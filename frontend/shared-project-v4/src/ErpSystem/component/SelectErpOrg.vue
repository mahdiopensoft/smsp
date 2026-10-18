<template>
  <!-- :click="async () => await openDialogErpOrg(item.id)" -->

  <custom-btn
    v-if="show"
    icon="list-status "
    is-icon
    size="20"
    class="ms-4 mb-2"
    label="اختيار نظام لنظام ال ERP"
    @click="openDialogErpOrg"
    variant="tonal"
  />
  <custom-dialog
    v-model="dialogErpOrg"
    title="تخطيط موارد المؤسسات"
    width="400"
    height="auto"
  >
    <VCard>
      <VCardText>
        <VForm ref="form">
          <VRow>
            <auto-list name="" :rules="[$required]" />
            <custom-text-field
              v-model="erpOrg.erp_domain"
              label="الرابط"
              :rules="[$required]"
            />
            <custom-text-field
              v-model="erpOrg.erp_db"
              label="قاعدة البيانات"
              :rules="[$required]"
            />
          </VRow>
        </VForm>
      </VCardText>
      <VCardActions>
        <VRow>
          <VSpacer />

          <custom-btn type="cancel" class="me-3" @click="dialogErpOrg = false" />
          <custom-btn type="save" :click="saveErpSystem" v-if="isSuperUser" />
        </VRow>
      </VCardActions>
    </VCard>
  </custom-dialog>
</template>
<script setup>
import { ref, computed } from "vue";
import api from "../../../plugins/axios-plugin";
import { alert, showAlert } from "../../utils/Globals";
import { state } from "@/../src/store/state";

const props = defineProps({
  id__organization: Number,
  show: Boolean,
});

const form = ref(null);
const dialogErpOrg = ref(false);
const erpOrg = ref({});
const url = "common/branch/erp-config/";
// ERP
const openDialogErpOrg = async (id) => {
  props.id__organization = id;
  const response = await api(url, {
    params: {
      fk_organization: props.id__organization,
    },
  });
  erpOrg.value = response?.data?.data;

  dialogErpOrg.value = true;
};

const saveErpSystem = async () => {
  const { valid } = await form.value.validate();

  if (!valid) return;

  await api.patch(url + props.id__organization + "/", erpOrg.value);
  alert("add");
  showAlert();
};

const isSuperUser = computed(() => {
  return state?.is_super_user;
});
</script>
