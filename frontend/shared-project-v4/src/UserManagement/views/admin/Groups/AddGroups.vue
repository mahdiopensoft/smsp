<template>
  <VForm ref="valid">
    <VRow>
      <fields
        :data="data"
        :fields="fieldsGroup"
        :attr="{
          name_ar: {
            disabled: data.id && data.for_manager,
          },
          name_en: {
            disabled: data.id && data.for_manager,
            null: false,
          },
          for_manager: {
            width: '2',
            update: () => changeForManager(),
            disabled: data.id,
            depend: isPlatFormSys,
          },
          company_level: {
            depend: data.for_manager,
            disabled: data.id,
            uodate: getPermissionsByFilter,
          },
        }"
      >
        <template v-slot="{ field }">
          <template v-if="field.name === 'company_level'">
            <auto-list
              v-if="data.for_manager"
              :name="field.name_list"
              v-model="data.company_level"
              :cols="3"
              @update:model-value="getPermissionsByFilter"
              :disabled="data.id"
              :rules="[$required]"
            />
          </template>
          <template v-if="field.name === 'fk_user_type'">
            <auto-list
              v-if="data.for_manager"
              :name="field.name_list"
              v-model="data.fk_user_type"
              :cols="3"
              @update:model-value="getPermissionsByFilter"
              :disabled="data.id"
              :rules="[$required]"
            />
            <span v-else></span>
          </template>
        </template>
      </fields>

      <custom-btn
        :type="props.fk_group > 0 ? 'update' : 'save'"
        class="mt-5"
        :click="saveData"
        width="100%"
        is_submit
      />
    </VRow>
  </VForm>
  <VCard elevation="0" :loading="loading" style="overflow: auto !important">
    <v-tabs v-model="tab">
      <v-tab
        v-for="sys in systems"
        :key="sys.id"
        :value="sys.id"
        color="primary"
        @click="tab = sys.id"
      >
        {{ sys.name_ar }}
      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item v-for="sys in systems" :key="sys.id" :value="sys.id">
        <template v-if="sys.id === tab && systems.length > 0">
          <VLazy>
            <VTable density="compact">
              <thead>
                <tr>
                  <th>
                    <v-checkbox-btn
                      :model-value="allState.checked"
                      :label="$t('screen_type')"
                      @update:modelValue="(val) => toggleAll(val)"
                      :indeterminate="allState.indeterminate"
                      style="min-width: 200px !important"
                      hide-details
                      color="primary"
                    />
                  </th>
                  <th v-for="(header, index) in headers" :key="index">
                    <v-checkbox-btn
                      :model-value="columnState(header.id).checked"
                      :indeterminate="columnState(header.id).indeterminate"
                      :label="header.name"
                      color="primary"
                      hide-details
                      class="ms-1 width-cell"
                      @update:modelValue="(val) => toggleColumn(header.id, val)"
                    />
                  </th>
                </tr>
              </thead>
              <tbody>
                <v-virtual-scroll renderless :items="permissionsBySystem">
                  <template v-slot:default="{ item, itemRef }">
                    <tr :ref="itemRef">
                      <td>
                        <v-checkbox-btn
                          :model-value="rowState(item.fk_screen).checked"
                          :label="item.custom_str"
                          color="primary"
                          :indeterminate="rowState(item.fk_screen).indeterminate"
                          @update:modelValue="(val) => toggleRow(item.fk_screen, val)"
                        ></v-checkbox-btn>
                      </td>

                      <td
                        v-for="(per, indexPer) in item.permissions"
                        :key="indexPer"
                        class="ps-5"
                      >
                        <VCheckbox
                          v-if="per.checked != null"
                          :model-value="
                            matrix[item.fk_default_system][item.fk_screen][
                              per.operation_type
                            ]
                          "
                          hide-details
                          @update:modelValue="
                            (val) => toggleCell(item.fk_screen, per.operation_type, val)
                          "
                        />
                      </td>
                    </tr>
                  </template>
                </v-virtual-scroll>
              </tbody>
            </VTable>
          </VLazy> </template
      ></v-tabs-window-item>
    </v-tabs-window>
  </VCard>
</template>
<script setup>
import api from "../../../../../plugins/axios-plugin";
import { state } from "@/../src/store/state";
import { ref, computed, reactive, watch } from "vue";
import { showSnackBar, alert } from "../../../../utils/Globals";

const props = defineProps({
  fk_group: { type: Number, default: 0 },
});

const emit = defineEmits(["update:modelValue"]);

// fields

const valid = ref(null);
const data = ref({});
const fieldsGroup = [
  {
    name: "name_ar",
    type: "CharField",
    null: false,
    label_ar: "Arabic Name",
    label_en: "Arabic Name",
    max_length: 50,

    icon: "abjad-arabic",

    width: "3",
  },
  {
    name: "name_en",
    type: "CharField",
    null: true,
    label_ar: "English Name",
    label_en: "English Name",
    max_length: 50,

    icon: "alpha-e",

    width: "3",
  },
  {
    name: "is_active",
    type: "BooleanField",
    null: false,
    label_ar: "نشط",
    label_en: "active",

    default: true,

    width: "1",
  },
  {
    name: "for_manager",
    type: "BooleanField",
    null: false,
    label_ar: "للمدراء",
    label_en: "For Managers",
    default: false,

    width: "1",
  },
  {
    name: "company_level",
    type: "IntegerField",
    null: false,
    label_ar: "مستوى الشركة",
    label_en: "مستوى الشركة",
    icon: "layers",
    name_list: "CompanyLevelChoices",
    width: "2",
  },
  {
    name: "fk_user_type",
    type: "ForeignKey",
    null: false,
    label_ar: "نوع المستخدم",
    label_en: "User type",
    icon: "account-convert-outline",
    name_list: "UserTypeForManager",
    width: "2",
  },
];
const isPlatFormSys = computed(() => {
  return state?.isPlatFormSys;
});
const changeForManager = () => {
  if (data.value.for_manager) {
    permissions.value = [];
    permissionsBySystem.value = [];

    systems.value = [];
  } else {
    getPermissions();
  }
  data.value.company_level = undefined;
  data.value.fk_user_type = undefined;
};

// system
const systems = ref([]);

// tab
const tab = ref(undefined);
const loading = ref(false);

// permissions

const headers = ref([
  {
    id: 1,
    name: "عرض",
  },
  {
    id: 2,
    name: "إضافة",
  },
  {
    id: 3,
    name: "تعديل",
  },
  {
    id: 4,
    name: "حذف",
  },
  {
    id: 5,
    name: "حذف إجباري",
  },
  {
    id: 6,
    name: "تصدير",
  },
  {
    id: 7,
    name: "استيراد",
  },
  {
    id: 8,
    name: "عرض المحذوفات",
  },
  {
    id: 9,
    name: "سجلات محذوفة",
  },

  {
    id: 11,
    name: "السجل",
  },
  {
    id: 12,
    name: "طباعة",
  },
  {
    id: 13,
    name: "رفع",
  },
  {
    id: 14,
    name: "مزامنة",
  },
  {
    id: 15,
    name: "حفظ اعدادات الطباعة",
  },
  {
    id: 16,
    name: "حذف اعدادات الطباعة",
  },
]);

const matrix = reactive({});
const columnCount = reactive({});
const rowCount = reactive({});

const totalRows = ref(null);
const totalColumns = headers.value.length;

const permissions = ref([]);
const permissionsBySystem = ref([]);

const getPermissions = async () => {
  try {
    loading.value = true;
    let params;
    if (!props.fk_group)
      params = {
        for_manager: data.value.for_manager,
        company_level: data.value.company_level,
        fk_user_type: data.value.fk_user_type,
      };
    const response = await api(
      `user-manager/groups/data-for-add/${
        props.fk_group > 0 ? "?pk=" + props.fk_group : ""
      }`,
      { params: params }
    );
    const res = response.data.data || response.data;
    systems.value = res.system_list;

    if (systems?.value.length > 0) tab.value = systems.value[0].id;
    if (props.fk_group) data.value = res?.group;

    permissions.value = buildMatrix(res.screens);
  } finally {
    loading.value = false;
  }
};
function buildMatrix(screens) {
  const resultScreen = new Array(screens.length);

  systems.value.forEach((s) => {
    columnCount[s.id] = {};

    headers.value.forEach((h) => (columnCount[s.id][h.id] = 0));
  });

  console.log(columnCount);

  screens.forEach((screen, index) => {
    // console.log(screen);
    if (!matrix[screen.fk_default_system]) matrix[screen.fk_default_system] = {};

    matrix[screen.fk_default_system][screen.fk_screen] = {};
    if (!rowCount[screen.fk_default_system]) rowCount[screen.fk_default_system] = {};

    rowCount[screen.fk_default_system][screen.fk_screen] = 0;
    const permissiomsMap = {};
    screen.permissions.forEach((p) => {
      permissiomsMap[p.operation_type] = p;

      matrix[screen.fk_default_system][screen.fk_screen][p.operation_type] = p.checked;

      if (p.checked) {
        // console.log(p.operation_type);
        try {
          columnCount[screen.fk_default_system][p.operation_type]++;
          rowCount[screen.fk_default_system][screen.fk_screen]++;
        } catch (error) {
          console.log(error);
        }
      }
    });

    //  2. بناء مصفوفة جديدة وترتيبها
    const sortedPermissions = new Array(headers.value.length);
    for (let k = 0; k < headers.value.length; k++) {
      const type = headers.value[k].id;

      sortedPermissions[k] = permissiomsMap[type] || {
        id: null,
        operation_type: type,
        checked: null,
      };
    }

    resultScreen[index] = {
      fk_screen: screen.fk_screen,
      custom_str: screen.custom_str,
      fk_default_system: screen.fk_default_system,
      fk_screen: screen.fk_screen,
      permissions: sortedPermissions,
    };
  });

  return resultScreen;
}
getPermissions();

const filterPermissionsBySystem = () => {
  const filterScreens = permissions.value.filter((f) => f.fk_default_system == tab.value);

  totalRows.value = filterScreens.length;

  permissionsBySystem.value = filterScreens;
};

const getPermissionsByFilter = async () => {
  if (data.value.company_level && data.value.fk_user_type) {
    await getPermissions();
    filterPermissionsBySystem();
  } else {
    permissions.value = [];
    permissionsBySystem.value = [];

    systems.value = [];
  }
};

// checked
// all
const allState = computed(() => {
  const totalChecked = Object.values(rowCount[tab.value]).reduce((a, b) => a + b, 0);
  const totalPossible = totalRows.value * totalColumns;

  return {
    checked: totalChecked === totalPossible,
    indeterminate: totalChecked < totalPossible && totalChecked != 0,
  };
});

function toggleAll(value) {
  headers.value.forEach((h) => {
    toggleColumn(h.id, value);
  });
}
// columns
function columnState(permId) {
  const checked = columnCount[tab.value][permId];

  return {
    checked: checked === totalRows.value,
    indeterminate: checked > 0 && checked < totalRows.value,
  };
}
function toggleColumn(permId, value) {
  permissionsBySystem.value.forEach((screen) => {
    toggleCell(screen.fk_screen, permId, value);
  });
}
// rows
function rowState(screenId) {
  const checked = rowCount[tab.value][screenId];

  return {
    checked: checked === totalColumns,
    indeterminate: checked > 0 && checked < totalColumns,
  };
}
function toggleRow(screenId, value) {
  headers.value.forEach((h) => {
    toggleCell(screenId, h.id, value);
  });
}
// cell
function toggleCell(screenId, permId, value) {
  const old = matrix[tab.value][screenId][permId];
  if (old === value) return;

  matrix[tab.value][screenId][permId] = value;
  if (value) {
    columnCount[tab.value][permId]++;
    rowCount[tab.value][screenId]++;
  } else {
    columnCount[tab.value][permId]--;
    rowCount[tab.value][screenId]--;
  }
}

watch(
  () => tab.value,
  (val) => {
    filterPermissionsBySystem();
  }
);

const saveData = async () => {
  const isValid = await valid.value.validate();

  if (!isValid.valid) return;

  let permScreen = [];

  permissions.value.forEach((screen) => {
    const perm = matrix[screen.fk_default_system][screen.fk_screen];
    screen.permissions.forEach((per) => {
      const typePer = perm[per.operation_type];
      if (typePer === true) {
        if (per.id) permScreen.push(per.id);
      }
    });
  });

  const dataPost = {
    name_ar: data.value.name_ar,
    name_en: data.value.name_en,
    is_active: data.value.is_active,
    for_manager: data.value.for_manager,
    group_screen_permissions: permScreen,
    company_level: data.value.company_level || null,
    fk_user_type: data.value.fk_user_type || null,
  };

  if (props.fk_group == 0) {
    await api.post("user-manager/groups/", dataPost);
    alert("add");
  } else {
    await api.put(`user-manager/groups/${props.fk_group}/`, dataPost);
    alert("update");
  }
  showSnackBar();

  emit("update:modelValue", false);
};
</script>
<style>
.width-cell {
  width: 100px;
}
</style>
