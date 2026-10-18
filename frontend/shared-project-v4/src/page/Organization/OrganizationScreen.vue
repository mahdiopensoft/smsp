<template>
  <ErrorInServer
    v-if="error.data || error.fields"
    @click="() => (error.fields ? getFields() : getData())"
  />
  <v-sheet v-else>
    <v-col cols="12" class="pa-0">
      <v-row justify-center align-center>
        <v-col>
          <v-container
            class="formal-tabs-card"
            elevation="0"
            style="overflow: auto !important"
          >
            <v-skeleton-loader
              v-if="loading.mounted"
              type="table-row-divider@1"
              class="w-100"
            />

            <v-tabs
              v-else
              :model-value="currentTab"
              density
              hide-slider
              show-arrows
              align-tabs="start"
              class="formal-tabs-container"
              slider-transition="grow"
              @update:modelValue="(val) => nextTab(val)"
            >
              <v-tab
                v-for="(item, index) in tabs"
                :key="index"
                :value="index"
                class="formal-tab"
                :class="{ 'formal-tab--error': tabStatus[index] == false }"
                :ripple="false"
              >
                <v-icon start size="20" class="me-2" :color="item.error ? 'error' : ''">{{
                  item.icon
                }}</v-icon>
                <span
                  style="font-size: 11px !important"
                  :class="{ 'text-error': item.error }"
                  >{{ item.title }}</span
                >
              </v-tab>
            </v-tabs>
          </v-container>
        </v-col>
        <v-spacer />

        <v-skeleton-loader v-if="loading.mounted" type="button@2" width="200" />
        <v-col cols="auto" v-else>
          <div>
            <back-to @click="confirmBack = true" />
            <custom-btn
              :type="screenStatus.EDIT ? 'update' : 'save'"
              class="ms-2 align-self-center"
              :click="saveData"
            />
          </div>
        </v-col>
      </v-row>
    </v-col>
    <v-divider />

    <!-- loading  -->
    <v-row v-if="loading.mounted">
      <v-col cols="12" md="8">
        <v-row v-for="key in 3" :key="key">
          <v-col cols="3">
            <v-skeleton-loader type="text" />
          </v-col>
          <v-col cols="3">
            <v-skeleton-loader type="text" />
          </v-col>
          <v-col cols="3">
            <v-skeleton-loader type="text" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-skeleton-loader type="image" />
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="2">
        <v-skeleton-loader type="image" />
      </v-col>
    </v-row>

    <v-window v-else v-model="currentTab" class="pt-5" activeSlide>
      <v-window-item :value="0" eager>
        <v-form :ref="(el) => (formsRefs[0] = el)">
          <FirstTab
            v-model="data"
            :fields="filterFields.filter((e) => e.group === 'Information Basic')"
            :levels="levels"
            :hasLevel="hasLevel"
            :paramCompanyLevel="paramCompanyLevel"
            :paramLocation="paramLocation"
            :errorLevel="error.level"
            :originData="originData"
            @changeCompanyLevel="changeCompanyLevel"
          />
        </v-form>
      </v-window-item>
      <v-window-item :value="1" eager>
        <v-form :ref="(el) => (formsRefs[1] = el)">
          <SecondTab
            v-model="data"
            :fields="filterFields.filter((e) => e.group === 'Information Location')"
        /></v-form>
      </v-window-item>
      <v-window-item :value="2" eager>
        <v-form :ref="(el) => (formsRefs[2] = el)"
          ><ThirdTab
            v-model="data"
            :fields="filterFields.filter((e) => e.group === 'Information Boss & License')"
            :screenStatus="screenStatus"
        /></v-form>
      </v-window-item>
      <v-window-item :value="3" eager>
        <v-form :ref="(el) => (formsRefs[3] = el)"
          ><FourthTab
            v-model="data"
            :fields="filterFields.filter((e) => e.group === 'Settings Advanced')"
        /></v-form>
      </v-window-item>
      <v-window-item :value="4" eager>
        <v-form :ref="(el) => (formsRefs[4] = el)"><FifthTab v-model="data" /></v-form>
      </v-window-item>
    </v-window>
  </v-sheet>

  <confirm-dialog
    v-model="confirmBack"
    :title="$i18n.locale === 'ar' ? 'تأكيد الخروج' : 'Confirm Exit'"
    icon="information"
    color="primary"
    :message="
      $i18n.locale === 'ar'
        ? 'هل أنت متأكد من تجاهل التغييرات؟'
        : 'Are you sure you want to ignore changes?'
    "
    @confirm="$emit('back')"
  />
</template>
<script setup>
import { ref, computed, watch, reactive, onMounted } from "vue";

import setting from "@/../settings";

import { useI18n } from "vue-i18n";
import FirstTab from "./components/OrgTabs/FirstTab.vue";
import SecondTab from "./components/OrgTabs/SecondTab.vue";
import ThirdTab from "./components/OrgTabs/ThirdTab.vue";
import FourthTab from "./components/OrgTabs/FourthTab.vue";
import FifthTab from "./components/OrgTabs/FifthTab.vue";
import api from "../../../plugins/axios-plugin";
import merge from "lodash";
import { state } from "@/../src/store/state";
import { alert, showSnackBar } from "../../utils/Globals";
const { locale, t } = useI18n();

const props = defineProps({
  originData: {
    type: Object,
    default: () => {},
  },
});

const confirmBack = ref(false);
const screenStatus = ref({
  NEW: false,
  NEWCHILD: false,
  EDIT: false,
});

const emit = defineEmits(["back"]);

const levels = {
  ADMIN: 10,
  MINISTRY: 20,
  GOVERNORATE: 30,
  DIRECTORATE: 40,
  COMPANY: 50,
  COLLEGE: 60,
};

const isEdit = ref(false);
const loading = ref({
  fields: false,
  mounted: false,
  data: false,
});
const error = ref({
  fields: false,
  level: false,
});

// =============================== data =======================================//
const data = ref({
  contact_set: [],
  manager_user: {},
  service_set: [],
});
const getData = async () => {
  try {
    loading.value.data = true;
    error.value.data = false;
    let url = `common/branch/${props.originData.fk_organization}/`;
    const response = await api(url);
    const results = response.data.data || response.data;

    data.value = {
      ...results,
      fk_country:
        results.fk_country ||
        results.fk_governorate__fk_country ||
        results.fk_directorate__fk_governorate__fk_country,
      fk_governorate: results.fk_governorate || results.fk_directorate__fk_governorate,
    };
  } catch {
    error.value.data = true;
  } finally {
    loading.value.data = false;
  }
};

// =============================== tabs =======================================//
const currentTab = ref(0);
const tabs = computed(() => {
  return [
    {
      title: locale.value === "ar" ? "البيانات الأساسية" : "Basic Information",
      color: "primary",
      icon: "mdi-information-outline",
    },
    {
      title: locale.value === "ar" ? "الموقع الجغرافي" : "Geographical Location",
      color: "primary",
      icon: "mdi-map-marker-outline",
    },
    {
      title:
        locale.value === "ar"
          ? "معلومات الترخيص والمدير"
          : "License & Administrator Info",
      color: "primary",
      icon: "mdi-card-account-details-outline",
    },
    {
      title: locale.value === "ar" ? "إعدادات متقدمة" : "Advanced Settings",
      color: "primary",
      icon: "mdi-cog-outline",
    },
    {
      title: locale.value === "ar" ? "التواصل" : "Communication",
      color: "primary",
      icon: "mdi-phone-outline",
    },
  ];
});

const nextTab = async (val) => {
  const valid = await validateForm(currentTab.value);
  tabStatus.value[currentTab.value] = valid;
  currentTab.value = val;
};

// ============================== location  ========================================

const paramLocation = ref({});

const resetLoacation = () => {
  paramLocation.value = {
    fk_country: { depend: false },
    fk_governorate: { depend: false },
    fk_directorate: { depend: false },
    fk_region: { depend: false },
  };
};

const controlLocation = (requiredMap) => {
  resetLoacation();
  let address = [
    { name: "fk_country", depend: false },
    { name: "fk_governorate", depend: false },
    { name: "fk_directorate", depend: false },
    { name: "fk_region", depend: false },
  ];
  let addressObj = {};
  requiredMap?.forEach((required) => {
    const targetIndex = address.findIndex((item) => item.name === required);
    if (targetIndex === -1) return;

    address.forEach((item, index) => {
      const status = index <= targetIndex;
      addressObj[item.name] = {
        depend: status,
        null: !status,
      };
    });
  });

  paramLocation.value = { ...paramLocation.value, ...addressObj };
};

// ================= Company Level  ========================================

const paramCompanyLevel = computed(() => {
  return {
    company_level: props.originData?.company_level ?? 0,
    isEdit: screenStatus.value.EDIT,
  };
});

const nullMap = ref([]);

const changeCompanyLevel = async () => {
  try {
    error.value.level = false;
    resetLoacation();
    if (!data.value.company_level) return;

    const response = await api("common/branch/data-for-add/", {
      params: {
        company_level: data.value.company_level,
      },
    });

    const results = response.data.data || response.data;

    nullMap.value = results?.null_map;

    controlLocation(results?.required_map);

    addControlToField();
  } catch (err) {
    error.value.level = true;
  } finally {
  }
};
// ================= forms ========================================
const formsRefs = ref([]);
const tabStatus = ref({});

const registerForm = () => {
  formsRefs[currentTab.value] = null;
  tabStatus[currentTab.value] = null;
};

const validateForm = async (index) => {
  const { valid } = (await formsRefs.value[index]?.validate()) || {
    valid: false,
  };
  return valid;
};

const validateAllForms = async () => {
  tabStatus.value = {};

  let status = true;

  for (const [ind, form] of formsRefs.value.entries()) {
    const { valid } = await form.validate();

    tabStatus.value[ind] = valid || false;
    if (!valid && status) {
      currentTab.value = ind;
      status = false;
    }
  }

  return status;
};

// ================= fields ========================================
const fields = ref([]);

const getFields = async () => {
  try {
    loading.fields = true;
    error.value.fields = false;
    const response = await api(`${setting.url_field}organizations/`);
    const results = response.data.data || response.data;
    fields.value = results;
  } catch {
    error.value.fields = true;
  } finally {
    loading.fields = false;
  }
};

const filterFields = computed(() => {
  return fields.value;
});

const hasLevel = (...allowedLevels) => allowedLevels.includes(data.value.company_level);

const controlField = {
  // ========================= tab 1 ==================================
  name_ar: {
    readonly: [levels.GOVERNORATE, levels.DIRECTORATE],
  },
  name_en: {
    readonly: [levels.GOVERNORATE, levels.DIRECTORATE],
  },
  // fk_country: { depend: [levels.MINISTRY, levels.GOVERNORATE, levels.DIRECTORATE] },
  // fk_governorate: { depend: [levels.MINISTRY, levels.GOVERNORATE, levels.DIRECTORATE] },
  // fk_directorate: { depend: [levels.MINISTRY, levels.GOVERNORATE, levels.DIRECTORATE] },
  established_date: {
    depend: [levels.COMPANY, levels.COLLEGE],
  },
  // ========================= tab 2 ==================================
  coordinate: {
    depend: [levels.COMPANY, levels.COLLEGE],
  },
  coordinate_image: {
    depend: [levels.COMPANY, levels.COLLEGE],
  },

  // ========================= tab 3 ==================================
  license_number: { depend: [levels.COMPANY, levels.COLLEGE] },
  // ========================= tab 4 ==================================
  student_type: { depend: [levels.COMPANY, levels.COLLEGE] },
  default_user_name_for_students: { depend: [levels.COMPANY, levels.COLLEGE] },
  default_password_for_students: { depend: [levels.COMPANY, levels.COLLEGE] },
  card_background_image: { depend: [levels.COMPANY, levels.COLLEGE] },
  card_title: { depend: [levels.COMPANY, levels.COLLEGE] },
  card_title_color: { depend: [levels.COMPANY, levels.COLLEGE] },
  card_info_title: { depend: [levels.COMPANY, levels.COLLEGE] },
  card_info_title_color: { depend: [levels.COMPANY, levels.COLLEGE] },
  use_hijri_calendar: { depend: [levels.COMPANY, levels.COLLEGE] },
  attendance_twice: { depend: [levels.COMPANY, levels.COLLEGE] },
  batch_code_for_college: { depend: [levels.COMPANY, levels.COLLEGE] },
  batch_code_for_specialization: { depend: [levels.COMPANY, levels.COLLEGE] },
  semester_code_for_batch: { depend: [levels.COMPANY, levels.COLLEGE] },
  semester_code_for_specialization: {
    depend: [levels.COMPANY, levels.COLLEGE],
  },
  subject_code: { depend: [levels.COMPANY, levels.COLLEGE] },
  batch_code_for_differentiation_batch: {
    depend: [levels.COMPANY, levels.COLLEGE],
  },
  academic_id_length: { depend: [levels.COMPANY, levels.COLLEGE] },
  branch_type: { depend: [levels.COMPANY, levels.COLLEGE] },
  number_of_levels: { depend: [levels.COMPANY, levels.COLLEGE] },
};

const addControlToField = () => {
  fields.value.forEach((field) => {
    const element = controlField[field.name];
    if (element) {
      if (element.depend) {
        field.depend = element.depend?.includes(data.value.company_level || 0);
      } else if (element.readonly) {
        field.readonly = element.readonly.includes(data.value.company_level);
      }
    }
  });
};

const saveData = async () => {
  try {
    const valid = await validateAllForms();
    if (!valid) return;

    if (!("contact_set" in data.value) || data.value?.contact_set.length === 0) {
      alert("info", {
        message: t("at_least_one_contact_method_must_entered"),
      });
      showSnackBar();
      currentTab.value = 4;
      return;
    }

    let copyData = merge.cloneDeep(data.value);

    nullMap.value.forEach((item) => {
      copyData[item] = null;
    });

    copyData.fk_address = {
      fk_region: data.value?.fk_address__fk_region,
      street: data.value?.fk_address__street,
    };

    if (screenStatus.EDIT) copyData.fk_address.id = data.value.fk_address.id;

    const formData = new FormData();
    if (
      copyData.logo &&
      typeof copyData?.logo === "string" &&
      copyData.logo === undefined
    ) {
      delete copyData.logo;
    } else formData.append("logo", copyData.logo);

    if (copyData.coordinate_image && typeof copyData?.coordinate_image === "object")
      formData.append("coordinate_image", copyData.coordinate_image);
    else delete copyData.coordinate_image;

    if (copyData.license_image && typeof copyData?.license_image === "object")
      formData.append("license_image", copyData.license_image);
    else delete copyData.license_image;

    copyData.boss =
      copyData.manager_user.first_name + " " + copyData.manager_user.last_name;
    var profile = state.profile;

    if (profile.ip && this.copyData_org.fk_parent_organization === 0) {
      copyData.fk_parent_organization = profile.ip;
    }

    if (!copyData.fk_parent_organization)
      copyData.fk_parent_organization = state.organization_id;

    formData.append("data", JSON.stringify(copyData));
    formData.append("manager_user", JSON.stringify(copyData.manager_user));

    const response = screenStatus.value.EDIT
      ? await api.put(`common/branch/${props.originData.fk_organization}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
      : await api.post("common/branch/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

    alert(screenStatus.value.EDIT ? "update" : "add");
    showSnackBar();

    emit(
      "back",
      screenStatus.value.EDIT ? "update" : "add",
      response.data?.data || response.data.data
    );
  } catch (err) {
    console.log(err);
  }
};

onMounted(async () => {
  try {
    loading.value.mounted = true;

    await getFields();

    if (props.originData?.fk_organization > 0) {
      screenStatus.value.EDIT = true;
    } else if (
      props.originData?.fk_organization == 0 &&
      props.originData?.fk_parent_organization > 0
    ) {
      screenStatus.value.NEWCHILD = true;
    } else {
      screenStatus.value.NEW = true;
    }
    if (screenStatus.value.NEWCHILD) {
      data.value = { ...data.value, ...props.originData };
      if (props.originData.company_level === levels.MINISTRY) {
        data.value.fk_address__fk_region__fk_directorate__fk_governorate = null;
        data.value.fk_address__fk_region__fk_directorate = null;
        data.value.fk_address__fk_region = null;
      } else if (props.originData.company_level === levels.GOVERNORATE) {
        data.value.fk_address__fk_region__fk_directorate = null;
        data.value.fk_address__fk_region = null;
      } else if (props.originData.company_level === levels.DIRECTORATE) {
        data.value.fk_address__fk_region = null;
      }

      data.value.fk_parent_organization = props.originData.fk_parent_organization;
      data.value.company_level = Number(props.originData.company_level) + 10;
      await changeCompanyLevel();
    } else if (screenStatus.value.EDIT) {
      await getData();
      await changeCompanyLevel();
    }
  } finally {
    loading.value.mounted = false;
  }

  // if (screenStatus.value.NEW) {
  // data.value.type_of_main_system = undefined;
  // }
});
</script>

<style scoped>
/* ── Ultra Professional Segmented Tabs ── */
.formal-tabs-card {
  background: rgba(var(--v-theme-primary), 0.03) !important;
  border-radius: 12px !important;
  padding: 6px !important;
  display: inline-flex;
  border: 1px solid rgba(var(--v-theme-primary), 0.06) !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.01) !important;
}

.formal-tabs-container {
  border-bottom: none !important;
  background: transparent !important;
}

.formal-tab {
  text-transform: none !important;
  letter-spacing: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.75) !important;
  min-height: 42px !important;
  padding: 0 24px !important;
  border-radius: 6px !important;
  margin-inline-end: 4px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.formal-tab.v-tab--selected {
  color: rgb(var(--v-theme-primary)) !important;
  background: rgba(var(--v-theme-primary), 0.12) !important;
  font-weight: 600;
  box-shadow: none !important;
}

.formal-tab:hover:not(.v-tab--selected) {
  background: rgba(var(--v-theme-primary), 0.05) !important;
  color: rgba(var(--v-theme-primary), 0.9) !important;
}

/* ── Error State Tabs ── */
.formal-tab.formal-tab--error {
  color: rgb(var(--v-theme-error)) !important;
}

.formal-tab.formal-tab--error.v-tab--selected {
  color: rgb(var(--v-theme-error)) !important;
  background: rgba(var(--v-theme-error), 0.12) !important;
}

.formal-tab.formal-tab--error:hover:not(.v-tab--selected) {
  background: rgba(var(--v-theme-error), 0.06) !important;
  color: rgb(var(--v-theme-error)) !important;
}

/* ── Modern Tabs Transition Container ── */
.tabs-container {
  display: grid;
  width: 100%;
  position: relative;
}

.tab-item {
  grid-area: 1 / 1;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  z-index: 0;
  min-width: 0; /* Prevents grid blowout on mobile */
  transform: translateY(10px);
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.active-tab {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  z-index: 1;
  transform: translateY(0);
}
</style>
