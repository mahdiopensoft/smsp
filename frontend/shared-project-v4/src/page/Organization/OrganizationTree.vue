<template>
  <v-sheet v-if="showScreen.SCREEN">
    <OrganizationScreen :originData="originData" @back="back" />
  </v-sheet>
  <v-sheet v-show="showScreen.TREE">
    <v-col cols="12">
      <v-row>
        <v-col v-if="loading" cols="3" class="pa-0">
          <v-skeleton-loader type="heading@1" width="400" />
        </v-col>
        <CustomTextField
          v-else
          v-model="search"
          label="البحث"
          icon="magnify"
          color="primary"
          cols="3"
          hideDetails
          rounded
        />

        <VSpacer />

        <!-- Create Button -->

        <v-col cols="auto" v-if="loading" class="pa-0">
          <v-skeleton-loader type="actions" width="400" />
        </v-col>
        <v-col cols="auto" v-if="!loading">
          <CustomBtn
            v-if="$perm('add', 'organizations') && isPlatFormSys"
            type="create"
            @click="actionClick('new')"
          />
        </v-col>

        <v-col cols="auto" v-if="!loading">
          <TableGeneralActions
            :url="url"
            :headers="headersLog"
            print="print"
            :hasLog="true"
            :hasRestore="isPlatFormSys"
            :getData="getData"
          />
          <custom-btn
            type="print"
            isIcon
            variant="tonal"
            size="small"
            class="ms-2 rounded-lg"
            style="height: 38px; min-width: 38px"
            print="print"
          />
        </v-col>
      </v-row>
    </v-col>

    <v-card id="print" elevation="0" class="border rounded-lg">
      <v-skeleton-loader
        v-if="loading"
        type="list-item-two-line,list-item-two-line,list-item-two-line"
        width="400"
      />
      <ErrorInServer v-else-if="error" @click="getData" />
      <EmptyState
        v-else-if="items.length == 0"
        :description="$i18n.locale === 'ar' ? 'لا يوجد بيانات' : 'No data available'"
      />
      <OrgBuildTree
        v-if="!loading"
        :items="items"
        :search="search"
        :isPlatFormSys="isPlatFormSys"
        :getData="getData"
        @action-click="actionClick"
      />
    </v-card>
  </v-sheet>
  <v-sheet v-if="showScreen.DETAILS">
    <OrganizationBasicData
      :id__organization="currentId"
      @close="resetshowScreen(), (showScreen.TREE = true)"
    />
  </v-sheet>
</template>
<script setup>
import { ref, computed, watch, onMounted } from "vue";

import OrgBuildTree from "./components/OrgBuildTree.vue";
import OrganizationScreen from "./OrganizationScreen.vue";
import { useI18n } from "vue-i18n";
import { state } from "@/../src/store/state";
import api from "../../../plugins/axios-plugin";
import OrganizationBasicData from "./OrganizationBasicData/OrganizationBasicData.vue";

const { locale } = useI18n();

const url = "common/branch/";

const search = ref(null);
const items = ref([]);
const loading = ref(false);
const error = ref(false);
const showScreen = ref({
  TREE: true,
  SCREEN: false,
  DETAILS: false,
});

const resetshowScreen = () => {
  showScreen.value = {
    TREE: false,
    SCREEN: false,
    DETAILS: false,
  };
};
const originData = ref({});

const currentId = ref(null);

const getData = async () => {
  try {
    items.value = [];
    error.value = false;
    loading.value = true;

    const response = await api(url);
    items.value = buildFastTree(response.data?.data);
  } catch (err) {
    error.value = true;
  } finally {
    setTimeout(() => {
      loading.value = false;
    }, 500);
  }
};
const buildFastTree = (data) => {
  const tree = [];
  const map = {};
  for (const item of data) {
    map[item.id] = { ...item };
  }

  for (const item of data) {
    const node = map[item.id];
    const parentId = item.fk_parent_organization;
    if (parentId && map[parentId]) {
      const parent = map[parentId];
      if (parent.company_level === 30) {
        if (node.company_level === 40) {
          if (!parent._dirNode) {
            parent._dirNode = {
              id: `dir-${parent.id}`,
              name_ar: locale.value === "ar" ? "المديريات" : "Directorates",
              isHeader: true,
              children: [],
            };
            if (!parent.children) parent.children = [];
            parent.children.push(parent._dirNode);
          }

          parent._dirNode.children.push(node);
        } else if (node.company_level === 50) {
          if (!parent._uniNode) {
            parent._uniNode = {
              id: `uni-${parent.id}`,
              name_ar: locale.value === "ar" ? "الجامعات" : "Universities",
              isHeader: true,
              children: [],
            };
            if (!parent.children) parent.children = [];

            if (parent._uniNode) parent.children.push(parent._uniNode);
          }
          parent._uniNode.children.push(node);
        } else parent.children.push(node);
      } else {
        if (!parent.children) parent.children = [];
        parent.children.push(map[item.id]);
      }
    } else {
      tree.push(map[item.id]);
    }
  }

  return tree;
};

const isPlatFormSys = computed(() => {
  return state?.isPlatFormSys || false;
});

const headersLog = computed(() => {
  return [
    {
      title: locale.value === "ar" ? "الاسم بالعربي" : "Name (AR)",
      key: "name_ar",
    },
    {
      title: locale.value === "ar" ? "الاسم بالانجليزي" : "Name (EN)",
      key: "name_en",
    },
    {
      title: locale.value === "ar" ? "المستوى" : "Level",
      key: "company_level_display",
    },
  ];
});

const actionClick = (type, item) => {
  originData.value = {};
  switch (type) {
    case "new":
      originData.value.fk_organization = 0;
      originData.value.fk_parent_organization = 0;
      originData.value.company_level = 0;
      break;
    case "newChild":
      originData.value.fk_organization = 0;
      originData.value.fk_parent_organization = item.id ?? 0;
      originData.value.company_level = item.company_level ?? 0;

      originData.value.fk_country =
        item?.fk_country ||
        item?.fk_governorate__fk_country ||
        item?.fk_directorate__fk_governorate__fk_country;

      originData.value.fk_governorate =
        item?.fk_governorate || item?.fk_directorate__fk_governorate;

      originData.value.fk_directorate = item?.fk_directorate;

      originData.value.fk_address__fk_region__fk_directorate__fk_governorate__fk_country =
        item?.fk_address__fk_region__fk_directorate__fk_governorate__fk_country;

      originData.value.fk_address__fk_region__fk_directorate__fk_governorate =
        item?.fk_address__fk_region__fk_directorate__fk_governorate;

      originData.value.fk_address__fk_region__fk_directorate =
        item?.fk_address__fk_region__fk_directorate;

      originData.value.fk_address__fk_region = item?.fk_address__fk_region;

      break;
    case "edit":
      originData.value.fk_organization = item.id;
      originData.value.fk_parent_organization = item.fk_parent_organization ?? 0;
      originData.value.company_level = item.company_level ?? 0;
      break;

    case "details":
      currentId.value = item.id;

      resetshowScreen();

      showScreen.value.DETAILS = true;
      return;

      break;
  }
  resetshowScreen();
  showScreen.value.SCREEN = true;
};

const back = (type, element) => {
  originData.value = {};
  if (type === "update") {
    getData();
    // console.log(items.value);
    // console.log(element);
    // const itemIndex = items.value.findIndex((e) => (e.id = element.id));
    // const element = items.value[itemIndex];

    // console.log(items.value[itemIndex]);
    // console.log(element);
  } else if (type === "add") {
    getData();
  }
  resetshowScreen();
  showScreen.value.TREE = true;
};
onMounted(() => {
  getData();
});
</script>
