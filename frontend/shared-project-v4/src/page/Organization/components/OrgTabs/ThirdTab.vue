<template>
  <v-row class="pa-2">
    <v-col cols="12" md="10">
      <!-- :style="`pointer-events:${screenStatus.EDIT ? 'none' : ''};`" -->
      <v-row>
        <Fields :data="data" :fields="fields" />
        <v-col cols="12">
          <fieldset class="mb-5 border rounded pa-2">
            <legend class="mx-2 px-2">
              <span>{{ $t("user_info") }}</span>
            </legend>

            <v-row class="pa-2">
              <!--  disabled: data.id ? true : false -->
              <!-- username: { disabled: screenStatus.EDIT }, -->
              <Fields
                :data="data['manager_user']"
                :fields="fieldUser"
                :attr="{
                  first_name: {},
                  last_name: { disabled: screenStatus.EDIT },

                  fk_user_type: { disabled: screenStatus.EDIT },

                  password: {
                    depend: !screenStatus.EDIT,
                    rules: [$valid_pass],
                  },
                  groups: {
                    param: paramToGroup,
                  },
                }"
              />
              <OrgChangePass v-if="screenStatus.EDIT" :userId="data?.manager_user?.id" />

              <OrgActiveUser
                v-if="screenStatus.EDIT"
                :userId="data?.manager_user?.id"
                :active="data?.manager_user?.is_active"
                @changeActive="(val) => (data.manager_user.is_active = val)"
              />

              <OrgApprovedUser
                v-if="screenStatus.EDIT"
                :userId="data?.manager_user?.id"
                :is_approved="data?.manager_user?.is_approved"
                :approved_to="data?.manager_user?.approved_to"
                @changeApproved="
                  (is_approved, approved_to) => (
                    (data.manager_user.is_approved = is_approved),
                    (data.manager_user.approved_to = approved_to)
                  )
                "
              />
            </v-row>
          </fieldset>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="12" md="2" class="pa-2 justify-items-center">
      <CustomImage
        v-if="hasLevel(levels.COMPANY, levels.COLLEGE)"
        v-model="data.license_image"
        :title="$t('license_image')"
      />
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed } from "vue";
import api from "../../../../../plugins/axios-plugin";
import usersApi from "../../../../UserManagement/api/users";
import { alert, showAlert, showSnackBar } from "../../../../utils/Globals";
import OrgChangePass from "./OrgChangePass.vue";
import OrgActiveUser from "./OrgActiveUser.vue";
import OrgApprovedUser from "./OrgApprovedUser.vue";

const data = defineModel();

const props = defineProps({
  fields: {
    type: Array,
    default: [],
  },
  levels: {
    type: Object,
    default: {},
  },

  hasLevel: {
    type: Function,
    default: () => {},
  },
  screenStatus: { type: Object, default: {} },
});
const paramToGroup = computed(() => {
  if (data.value?.manager_user?.fk_user_type && data.value.company_level)
    return {
      fk_user_type: data.value.manager_user.fk_user_type,
      company_level: data.value.company_level,
    };
  else return undefined;
});

const fieldUser = [
  {
    name: "first_name",
    type: "CharField",
    null: false,
    label_ar: "الاسم الأول",
    label_en: "first name",
    max_length: 150,
    icon: "account",
    width: 3,
  },
  {
    name: "last_name",
    type: "CharField",
    null: true,
    label_ar: "الاسم الأخير",
    label_en: "last name",
    max_length: 150,
    icon: "account",

    width: 3,
  },
  {
    name: "username",
    type: "CharField",
    null: false,
    label_ar: "اسم المستخدم",
    label_en: "username",
    max_length: 150,
    icon: "account-circle",
    width: 3,
  },
  {
    name: "password",
    type: "password",
    null: false,
    label_ar: "كلمة المرور",
    label_en: "password",
    max_length: 128,
    icon: "lock",
    width: 3,
  },
  {
    name: "fk_user_type",
    type: "ForeignKey",
    null: false,
    label_ar: "نوع المستخدم",
    label_en: "User type",
    icon: "account-convert-outline",
    name_list: "UserType",
    width: 3,
  },
  {
    name: "groups",
    type: "ManyToManyField",
    null: false,
    label_ar: "المجموعات",
    label_en: "groups",
    max_length: null,
    default: null,
    icon: "account-group",
    group: null,
    name_list: "GroupesForManager",
    width: null,
    model: null,
  },
];

const formPass = ref(null);

const toggleActive = async () => {
  try {
    loadingActive.value = true;
    await usersApi.toggleActive(data?.value?.manager_user?.id);

    if (data?.value.manager_user) {
      data.value.manager_user.is_active = !data?.value.manager_user.is_active || false;
    }

    alert("success", {
      message: `تم ${
        data.value?.manager_user.is_active ? "تفعيل" : "إلغاء تفعيل"
      } المستخدم`,
    });
    showSnackBar();
  } finally {
    loadingActive.value = false;
  }
};
</script>
