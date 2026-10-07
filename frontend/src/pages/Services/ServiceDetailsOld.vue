<template>
  <v-card>
    <v-card-title class="py-2">
      <v-avatar size="40" color="primary" variant="tonal" class="ml-3">
        <v-icon>mdi-cog-outline</v-icon>
      </v-avatar>
      <span class="text-h6 font-weight-bold"> بيانات الخدمة</span>
      <v-divider class="mt-1"></v-divider>
    </v-card-title>
    <v-card-text>
      <v-list>
        <v-row>
          <v-col cols="12" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar color="primary" variant="tonal">
                  <v-icon> mdi-tag-outline </v-icon>
                </v-avatar>
              </template>
              <v-list-item-content>
                <v-list-item-title>اسم الخدمة</v-list-item-title>
                <v-list-item-subtitle>{{ service?.name }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar color="secondary" variant="tonal">
                  <v-icon> mdi-folder-open-outline </v-icon>
                </v-avatar>
              </template>

              <v-list-item-content>
                <v-list-item-title> التصنيف</v-list-item-title>
                <v-list-item-subtitle>{{
                  service?.category_name
                }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="4" sm="6">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar color="success" variant="tonal">
                  <v-icon> mdi-check-circle-outline </v-icon>
                </v-avatar>
              </template>
              <v-list-item-title> الحالة</v-list-item-title>
              <v-list-item-subtitle>{{
                service?.status ? "نشطة" : "غير نشطة"
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </v-list>
      <div>
        <fieldset class="border rounded pa-4">
          <legend class="px-4">وصف الخدمة</legend>
          <p>
            {{ service.description }}
          </p>
        </fieldset>
      </div>
    </v-card-text>
  </v-card>
  <v-sheet class="w-100 border rounded pa-4 pt-0 mt-2">
    <v-tabs
      v-model="tab"
      slider-color="primary"
      color="primary"
      class="border-b text-medium-emphasis"
      variant="solo"
    >
      <v-tab
        value="workflow"
        prepend-icon="mdi-sitemap"
        text="تعريفات سير العمل"
        class="elevation-2"
      >
      </v-tab>
      <v-tab
        value="templates"
        prepend-icon="mdi-form-select"
        text="نماذج الخدمة"
        class="elevation-2"
      >
      </v-tab>
      <v-tab
        value="permissions"
        prepend-icon="mdi-shield-account"
        text=" الصلاحيات الممنوحة"
        class="elevation-2"
      >
      </v-tab>
    </v-tabs>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item value="workflow">
        <v-card>

          <v-card-text>
            <v-timeline dense side="end" density="compact">
              <template v-for="(stage, index) in workflow_stages" :key="index">
                <v-timeline-item
                  size="small"
                  :dot-color="getStageStyle(stage.stage_type)?.color"
                  class="w-100"
                  truncate-line="both"
                >
                  <v-card
                    :class="`border-e-lg border-${
                      getStageStyle(stage.stage_type)?.color
                    } border-opacity-75`"
                  >
                    <v-card-title>
                      <div class="d-flex align-center">
                        <v-avatar
                          size="40"
                          variant="tonal"
                          :color="getStageStyle(stage.stage_type)?.color"
                          class="me-2"
                        >
                          <v-icon>mdi-sitemap</v-icon>
                        </v-avatar>
                        <div>
                          <div class="text-h6 font-weight-bold me-2">
                            {{ stage.name }}
                          </div>
                          <div class="text-caption">description</div>
                        </div>
                        <v-spacer> </v-spacer>
                        <v-chip>
                          {{ stage.is_private ? "خاصة" : "عامة" }}
                        </v-chip>
                        <v-chip
                          color="error"
                          class="ms-1"
                          v-if="stage?.is_final"
                        >
                          <v-icon size="small" left>mdi-flag-checkered</v-icon>
                          مرحلة نهائية
                        </v-chip>
                      </div>
                    </v-card-title>
                    <v-card-text>
                      {{ stage.description }}
                    </v-card-text>
                    <v-card-actions>
                      <v-chip :color="getStageStyle(stage.stage_type)?.color">
                        <v-icon class="me-1">
                          {{ getStageStyle(stage.stage_type)?.icon }}
                        </v-icon>
                        {{ stage.stage_type_display }}
                      </v-chip>
                    </v-card-actions>
                  </v-card>
                </v-timeline-item>
              </template>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-tabs-window-item>
      <v-tabs-window-item value="templates">
        <v-card>
          <v-card-text>
            <add-service-template v-model="drawer" :data="data" />
            <custom-data-table
              :="{
                headers,
                items: templates,
                getData: getServiceTemplates,
                create: () => (drawer = true),
                delItem: url,
                actionList,
                editItem,
                pagination: false,
                log: false,
                search: false,
                restore: false,
              }"
            />
            <custom-dialog v-model="preview_dialog">
              <v-container>
                <form-preview :fields="json_schema" />
              </v-container>
            </custom-dialog>
          </v-card-text>
        </v-card>

      </v-tabs-window-item>
      <v-tabs-window-item value="permissions">
        <v-card>

          <v-card-text>
            <custom-data-table
              :="{
                headers: permission_headers,
                items: service_permissions,
                getData: getServicePermissions,
                pagination: false,
                log: false,
                search: false,
                restore: false,
              }"
            />
          </v-card-text>
        </v-card>

      </v-tabs-window-item>
    </v-tabs-window>
  </v-sheet>
</template>
<script>
export default {
  data() {
    return {
      drawer: false,
      service_id: this.$route.params?.service_id,
      service: {},
      workflow_stages: [],
      service_permissions: [],
      preview_dialog: false,
      tab: "workflow",
      templates: [],
      json_schema: [],
      stage_styles: {
        1: {
          icon: "mdi-check-circle",
          color: "success",
        },
        2: {
          icon: "mdi-eye",
          color: "primary",
        },
        3: {
          icon: "mdi-bell-ring",
          color: "warning",
        },
        4: {
          icon: "mdi-auto-fiex",
          color: "",
        },
        defaults: {
          icon: "mdi-sitemap",
          color: "grey",
        },
      },
      url: "d-services/workflow/services/",
    };
  },
  async created() {
    await this.getServiceDetails();
    await this.getServiceWorkflowStages();
    await this.getServiceTemplates();
    await this.getServicePermissions();
  },
  methods: {
    // الحصول على بيانات الخدمة
    async getServiceDetails() {
      return await this.$axios(`${this.url}${this.service_id}/`).then(
        (response) => (this.service = response.data)
      );
    },
    // الحصول على مراحل سير العمل للخدمة
    async getServiceWorkflowStages() {
      return await this.$axios(
        `${this.url}${this.service_id}/workflow-stages/`
      ).then((response) => (this.workflow_stages = response.data));
    },
    // الحصول على  النماذج الخاصة بالخدمة
    async getServiceTemplates() {
      return await this.$axios(`${this.url}${this.service_id}/templates/`).then(
        (response) => (this.templates = response.data)
      );
    },
    // الحصول على  الصلاحيات الخاصة بالخدمة
    async getServicePermissions() {
      return await this.$axios(
        `${this.url}${this.service_id}/user-permissions/`
      ).then((response) => (this.service_permissions = response.data));
    },
    // الحصول على نمط تصميم المرحلة
    getStageStyle(stage) {
      return this.stage_styles[stage] || this.stage_styles.default;
    },

    actionList(item) {
      return [
        {
          title_ar: "معاينة",
          title_en: "Preview",
          click: () => {
            this.preview_dialog = true;
            this.json_schema = item.json_schema;
          },
        },
      ];
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("template_name"), key: "name" },
        { title: this.$t("template_type"), key: "template_type_name" },
        { title: this.$t("version"), key: "version", field: {} },
        { title: this.$t("is_active"), key: "is_active" },
      ];
    },
    permission_headers() {
      return [
        { title: this.$t("permission_name"), key: "permission_name" },
        { title: this.$t("action"), key: "action" },
        { title: this.$t("permission_type"), key: "permission_type" },
        { title: this.$t("is_active"), key: "is_active" },
      ];
    },
  },
};
</script>
