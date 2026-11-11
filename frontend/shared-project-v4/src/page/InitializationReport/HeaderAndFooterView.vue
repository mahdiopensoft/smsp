<template>
  <!-- samer alnggar -->
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      delItem: url,
      editItem,
      create: () => (dialog = true),
    }"
  >
    <template v-slot:item-slot="{ item, key, index }">
      <VIcon
        v-if="key == 'preview'"
        icon="mdi-eye"
        color="primary"
        @click="openPreview(item)"
      />
      <span v-else-if="key === 'is_main'">
        <VProgressLinear v-if="item.loading === true" indeterminate />
        <v-icon
          v-if="item?.is_main == true"
          color="success"
          @click="changeStatus(item, index)"
          >mdi-check-circle</v-icon
        >
        <v-icon
          v-if="item?.is_main == false"
          color="error"
          @click="changeStatus(item, index)"
          >mdi-close-circle</v-icon
        >
      </span>
    </template>
  </custom-data-table>

  <custom-dialog v-model="dialogPreview" title="معاينة" width="60%">
    <v-card
      class="pa-4 mt-4"
      dir="rtl"
      v-for="i in ['header', 'footer']"
      :key="i"
    >
      <v-card-title class="rtl-preview"
        >📄 المعاينة الحية لل {{ i }}</v-card-title
      >
      <v-divider></v-divider>
      <v-card-text class="rtl-preview">
        <preview-content-html :items="item[i]" />
        <v-row> </v-row>
      </v-card-text>
    </v-card>
  </custom-dialog>

  <custom-dialog
    v-model="dialog"
    width="100%"
    height="auto"
    title="اضافة رأس وتذييل"
  >
    <AddHeaderAndFooter v-model="dialog" :item="item" :getData="getData" />
  </custom-dialog>
</template>
<script setup>
import { computed, ref, watch } from "vue";
import api from "../../../plugins/axios-plugin";
import useNavigateTo from "../../composables/useNavigateTo";
import { alert, showSnackBar } from "../../utils/Globals";
import AddHeaderAndFooter from "./AddHeaderAndFooter.vue";
import { useRouter } from "vue-router";

const router = useRouter();
const items = ref({});
const item = ref({});

const url = "common/print-report-setting/";
const dialogPreview = ref(false);
const dialog = ref(false);

async function getData(
  params = { page: 1, perPage: 10, sort_by: "id", txt_search: "" }
) {
  const response = await api(url, params);
  items.value = response.data;
}

function editItem(data) {
  item.value = { ...data };

  dialog.value = true;
}

function openPreview(el) {
  item.value.header = JSON.parse(el.header);
  item.value.footer = JSON.parse(el.footer);
  dialogPreview.value = true;
}
async function changeStatus(item, index) {
  try {
    items.value.results[index].loading = true;
    await api.patch(url + item?.id + "/", {
      is_main: !item.is_main,
    });

    items.value.results[index].is_main = !item.is_main ?? false;
    alert("update");
    showSnackBar()
  } finally {
    items.value.results[index].loading = false;
  }
}

// computed
const headers = computed(() => {
  return [
    { title: "الفرع", key: "fk_branch__name_ar" },
    { title: "الاسم", key: "name" },
    { title: "العلامة المائية", key: "has_watermark" },
    { title: "الشعار", key: "logo" },
    { title: "الرئيسي ؟", key: "is_main" },
    { title: "معاينة", key: "preview" },
  ];
});

// watch
watch(
  () => dialog.value,
  (val) => {
    if (!val) item.value = {};
  }
);
</script>

<style>
/* دعم RTL للمحرر */
.rtl-editor .ql-editor {
  direction: rtl;
  text-align: right;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-size: 16px;
}

.rtl-editor .ql-container {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  background-color: #ffffff;
}

.rtl-editor .ql-toolbar {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  background-color: #f5f5f5;
}
</style>