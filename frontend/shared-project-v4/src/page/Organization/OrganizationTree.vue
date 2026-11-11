<template>
  <div>
    <VRow>
      <custom-btn
        v-if="
          !dialog &&
          $perm('add', 'organizations') &&
          isPlatFormSys &&
          !dialog_info &&
          $perm('add', 'organizations') &&
          isPlatFormSys
        "
        type="create"
        @click="
          (data_org.fk_organization = 0),
            (data_org.fk_parent_organization = 0),
            (data_org.company_level = 0);
          dialog = true;
        "
      />
      <VSpacer />
      <div class="me-5 mb-2">
        <table-general-actions
          v-if="
            !dialog &&
            $perm('restore', 'organizations') &&
            !dialog_info &&
            $perm('restore', 'organizations')
          "
          :url="url"
          :headers="headersLog"
          print="print"
          :hasPrint="true"
          :hasLog="true"
          :hasRestore="isPlatFormSys"
          :getData="getData"
        />
      </div>
    </VRow>
  </div>
  <organizationScreen
    v-if="dialog"
    v-model="dialog"
    :methodData="getData"
    :data_organization="data_org"
  >
    <template v-slot:action>
      <back-to
        v-if="dialog || dialog_info"
        @click="accept_cancel = true"
        class="me-5 mt-3"
      />
    </template>
  </organizationScreen>
  <organization-basic-data
    v-if="dialog_info"
    :id__organization="id__organization"
  >
    <template v-slot:action>
      <back-to
        v-if="dialog || dialog_info"
        @click="accept_cancel = true"
        class="ms-5 mt-1"
      />
    </template>
  </organization-basic-data>

  <VProgressLinear v-if="loading" indeterminate height="1" class="mt-10" />
  <VCard
    id="print"
    v-if="!dialog && items.length > 0 && !dialog_info && items.length > 0"
  >
    <custom-text-field
      v-model="search"
      icon="magnify"
      :label="$i18n.locale == 'ar' ? 'إبحث هنا' : 'ٍSearch her'"
      hide-details
    />
    <VTreeview
      v-model:actived="active"
      v-model:opened="open"
      :items="items.length > 0 ? items : []"
      item-title="name_ar"
      item-value="id"
      color="primary"
      activatable
      density="compact"
      indent-lines
      :search="search"
    >
      <template #no-data>
        <VLabel class="ps-5" text="لا يوجد بيانات" width="100%" />
      </template>
      <template v-slot:prepend="{ item }">
        <VIcon :icon="getIcon(item.company_level)" />
      </template>
      <template v-slot:title="{ item }">
        <VHover>
          <template v-slot:default="{ isHovering, props }">
            <VSheet>
              <VRow v-bind="props" align="center" class="ma-0 pa-0">
                <VCol
                  cols="8"
                  class="treeview-title align-center justify-center row ma-0 pa-0"
                  :style="item.children ? 'font-weight:bold' : ''"
                >
                  <span
                    :class="{
                      'font-weight-bold text-primary': item.isHeader,
                      'font-weight-medium':
                        !item.isHeader && item.company_level === 30,
                      'body-2': true,
                    }"
                    >{{ item.name_ar }}</span
                  >
                  <custom-btn
                    v-if="
                      isHovering &&
                      $perm('add', 'organizations') &&
                      item.company_level != 60 &&
                      isPlatFormSys &&
                      !item.isHeader
                    "
                    icon="plus"
                    is-icon
                    @click.stop="
                      (data_org.fk_organization = 0),
                        (data_org.fk_parent_organization = item.id ?? 0),
                        (data_org.company_level = item.company_level ?? 0),
                        (dialog = true)
                    "
                    size="20"
                    class="ms-4 mb-2"
                    color="primary"
                    label="إضافة"
                  />

                  <custom-btn
                    v-if="
                      isHovering &&
                      $perm('edit', 'organizations') &&
                      isPlatFormSys &&
                      !item.isHeader
                    "
                    icon="square-edit-outline"
                    is-icon
                    size="20"
                    class="ms-4 mb-2"
                    @click.stop="
                      (data_org.fk_organization = item.id),
                        (data_org.fk_parent_organization =
                          item.fk_parent_organization ?? 0),
                        (data_org.company_level = item.company_level ?? 0),
                        (dialog = true)
                    "
                    color="green"
                    label="تعديل"
                  />

                  <custom-btn
                    v-if="
                      isHovering &&
                      $perm('delete', 'organizations') &&
                      isPlatFormSys &&
                      !item.isHeader
                    "
                    icon="trash-can-outline"
                    is-icon
                    size="20"
                    class="ms-4 mb-2"
                    @click="
                      (delete_dialog = true), (id__organization = item.id)
                    "
                    color="red"
                    label="حذف"
                  />

                  <SelectErpOrg
                    :id__organization="item.id"
                    :show="isHovering && isPlatFormSys && !item.isHeader"
                  />

                  <custom-btn
                    v-if="isHovering && !item.isHeader"
                    icon="information-outline"
                    is-icon
                    size="20"
                    class="ms-4 mb-2"
                    color="primary"
                    label="معلومات"
                    @click="(dialog_info = true), (id__organization = item.id)"
                  />
                </VCol>
              </VRow>
            </VSheet>
          </template>
        </VHover>
      </template>
    </VTreeview>
  </VCard>
  <VCol class="mt-10" v-if="!dialog && items.length === 0">
    <VRow justify="center">
      <VIcon
        :icon="error.data ? 'mdi-refresh' : 'mdi-playlist-remove'"
        size="40"
        @click="handleError"
      />
    </VRow>
    <VRow justify="center">
      {{ error.data ? $t("try_again") : $t("not_found") }}
    </VRow>
  </VCol>

  <confirm-deletion
    v-model="delete_dialog"
    url="common/branch/"
    :delete-item="id__organization"
    :getData="getData"
    :delRefresh="true"
  />

  <confirm-dialog
    v-model="accept_cancel"
    :title="$t('confirm_exit')"
    icon="information"
    color="primary"
    :message="$t('are_you_sure_ignore_changes')"
    @confirm="(dialog = false), (dialog_info = false)"
  />
</template>
<script>
import OrganizationScreen from "./OrganizationScreen.vue";

import SelectErpOrg from "../../ErpSystem/component/SelectErpOrg.vue";
import OrganizationBasicData from "./OrganizationBasicData/OrganizationBasicData.vue";
import { state } from "@/../src/store/state";

export default {
  components: { OrganizationScreen, SelectErpOrg, OrganizationBasicData },
  data() {
    return {
      // acti,
      OrganizationBasicDatave: [],
      open: [],
      items: [],
      data: {},
      search: null,

      id__organization: undefined,

      loading: false,
      error: {
        data: false,
      },
      delete_dialog: false,
      dialog: false,
      dialog_info: false,
      accept_cancel: false,

      data_org: {},

      url: "common/branch/",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    handleError() {
      if (this.error.data) this.getData();
    },

    async getData() {
      try {
        this.loading = true;
        this.error.data = false;

        const response = await this.$axios(this.url);

        const res = response.data.data || response.data;
        const data = res;
        this.items = this.buildFastTree(data);
      } catch (error) {
        this.error.data = true;
      } finally {
        this.loading = false;
      }
    },
    buildFastTree(data) {
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
                  name_ar: "المديريات",
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
                  name_ar: "الجامعات",
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
    },
    getIcon(level) {
      switch (level) {
        case 10:
          return "mdi-shield-account";
        case 20:
          return "mdi-domain";
        case 30:
          return "mdi-city-variant";
        case 40:
          return "mdi-office-building-marker";
        case 50:
          return "mdi-school";
        case 60:
          return "mdi-source-branch";
      }
    },

    colorOrg(level) {
      switch (level) {
        case 1:
          return "yellow";

        case 2:
          return "primary";

        case 3:

        case 4:
      }
    },
  },
  computed: {
    isPlatFormSys() {
      // return state?.isSSO||false;
      return state?.isPlatFormSys || false;
    },

    headersLog() {
      return [
        { title: this.$t("name_ar"), key: "name_ar" },
        { title: this.$t("name_en"), key: "name_en" },
        { title: this.$t("level"), key: "company_level_display" },
      ];
    },
  },
};
</script>
