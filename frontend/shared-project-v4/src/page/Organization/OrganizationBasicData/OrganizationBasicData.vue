<template>
  <VRow v-if="loading">
    <VCol cols="12">
      <v-skeleton-loader :type="`text`" />
    </VCol>
    <VCol cols="12" lg="4" md="4" v-for="load in 5" :key="load">
      <v-skeleton-loader :type="`card`" />
    </VCol>
  </VRow>
  <VRow v-else-if="error.fields || error.data" style="place-content: center">
    <error-in-server @click="refreshData" />
  </VRow>
  <VForm ref="valid" v-else class="bg-surface px-4 py-4 rounded-lg border">
    <VCard elevation="0" color="transparent">
      <VCardText class="pa-0 mt-2">
        <v-card
          variant="outlined"
          class="mb-6 rounded-lg"
          style="
            background-color: rgba(var(--v-theme-primary), 0.04);
            border-color: rgba(var(--v-theme-primary), 0.1) !important;
          "
        >
          <v-card-text class="d-flex align-center flex-wrap gap-4 pa-4">
            <div class="d-flex align-center gap-4">
              <!-- Premium Image Frame -->
              <div
                class="d-flex align-center justify-center rounded-lg bg-surface"
                style="
                  width: 58px;
                  height: 58px;
                  border: 1px solid rgba(var(--v-theme-primary), 0.12);
                  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.05);
                  padding: 4px;
                "
              >
                <custom-image
                  v-model="data.logo"
                  height="50"
                  width="50"
                  :circle="false"
                  class="rounded-md"
                  variant="flat"
                  color="transparent"
                  style="
                    border: none !important;
                    outline: none !important;
                    box-shadow: none !important;
                  "
                  :canEdit="false"
                />
              </div>
              <div>
                <div class="text-h6 font-weight-bold text-primary">
                  {{
                    data.name_ar ||
                    ($i18n.locale === "ar" ? "البيانات الأساسية" : "Basic Information")
                  }}
                </div>
                <div class="text-caption text-medium-emphasis" v-if="data.branch_no">
                  {{ $i18n.locale === "ar" ? "رقم الفرع" : "Branch No" }}:
                  {{ data.branch_no }}
                </div>
              </div>
            </div>

            <VSpacer />

            <div class="d-flex align-center flex-wrap" style="gap: 8px">
              <OrgChangePass V :userId="data?.manager_user?.id" />

              <OrgActiveUser
                :userId="data?.manager_user?.id"
                :active="data?.manager_user?.is_active"
                @changeActive="(val) => (data.manager_user.is_active = val)"
              />

              <OrgApprovedUser
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

              <!-- Merged Back Button -->
              <div
                class="d-flex align-center justify-center"
                style="height: 40px; margin: 0 !important"
              >
                <back-to @click="$emit('close')" />
              </div>
            </div>
          </v-card-text>
        </v-card>

        <VRow>
          <template v-for="(item, index) in items" :key="index">
            <VCol
              cols="12"
              :lg="item.cols"
              :md="item.cols"
              draggable="true"
              @dragstart="onDragStart($event, index)"
              @dragover.prevent
              @drop="onDrop($event, index)"
            >
              <VCard
                class="rounded-lg mb-4"
                variant="outlined"
                style="border-color: rgba(var(--v-theme-primary), 0.1) !important"
              >
                <VCardTitle
                  class="px-5 py-4 d-flex align-center border-b"
                  style="
                    background-color: rgba(var(--v-theme-primary), 0.04);
                    border-bottom-color: rgba(var(--v-theme-primary), 0.05) !important;
                  "
                >
                  <VIcon color="primary" class="me-3" size="24">{{
                    "mdi-" + item.icon
                  }}</VIcon>
                  <span class="text-subtitle-1 font-weight-bold text-primary">
                    {{ getTabTitle(item.title) }}
                  </span>
                  <VSpacer />
                </VCardTitle>

                <VCardText class="pa-5">
                  <VRow>
                    <template v-for="(body, body_index) in item.body" :key="body_index">
                      <template
                        v-if="
                          Array.isArray(
                            body?.data?.reduce((acc, key) => acc?.[key], data)
                          )
                        "
                      >
                        <VCol :cols="body.cols">
                          <VCard
                            variant="outlined"
                            class="rounded-lg"
                            style="
                              border-color: rgba(var(--v-theme-primary), 0.1) !important;
                            "
                          >
                            <VCardText class="pa-4">
                              <div
                                class="text-subtitle-2 font-weight-bold mb-3 text-primary"
                              >
                                {{ $t(body.name) }}
                              </div>
                              <v-chip-group
                                v-if="
                                  body?.data?.reduce((acc, key) => acc?.[key], data)
                                    ?.length
                                "
                                class="mt-2"
                              >
                                <v-chip
                                  v-for="(el, index) in body?.data
                                    ?.reduce((acc, key) => acc?.[key], data)
                                    .map((item) => item.name_ar)"
                                  :key="index"
                                  color="primary"
                                  variant="tonal"
                                  size="small"
                                >
                                  {{ el }}
                                </v-chip>
                              </v-chip-group>
                              <div
                                class="py-4 text-medium-emphasis text-caption"
                                style="text-align: center"
                                v-else
                              >
                                {{
                                  $i18n.locale === "ar"
                                    ? "لايوجد مجموعات"
                                    : "No groups available"
                                }}
                              </div>
                            </VCardText>
                          </VCard>
                        </VCol>
                      </template>
                      <template v-else>
                        <custom-text-field
                          :model-value="
                            data[body.name] ||
                            body?.data?.reduce((acc, key) => acc?.[key], data)
                          "
                          :cols="body.cols"
                          :label="
                            fields?.[body.key || body.name]?.label_ar || $t(body.name)
                          "
                          readonly
                        />
                      </template>
                      <!-- :readonly="!body.edit" -->
                    </template>
                  </VRow>
                </VCardText>
              </VCard>

              <VCol v-if="index === items.length - 1" cols="12" class="mt-2 pa-0">
                <VCard
                  class="rounded-lg mb-4"
                  variant="outlined"
                  style="border-color: rgba(var(--v-theme-primary), 0.1) !important"
                >
                  <VCardTitle
                    class="px-5 py-4 d-flex align-center border-b"
                    style="
                      background-color: rgba(var(--v-theme-primary), 0.04);
                      border-bottom-color: rgba(var(--v-theme-primary), 0.05) !important;
                    "
                  >
                    <VIcon color="primary" class="me-3" size="24"
                      >mdi-map-marker-radius</VIcon
                    >
                    <span class="text-subtitle-1 font-weight-bold text-primary">
                      {{ $i18n.locale === "ar" ? "التواصل" : "Communication" }}
                    </span>
                  </VCardTitle>
                  <VCardText class="pa-0">
                    <v-table
                      v-if="data?.contact_set?.length"
                      class="custom-data-table"
                      density="comfortable"
                      style="
                        border: 1px solid rgba(var(--v-theme-primary), 0.1);
                        border-radius: 8px;
                        overflow: hidden;
                      "
                    >
                      <thead style="background-color: rgba(var(--v-theme-primary), 0.06)">
                        <tr>
                          <th
                            v-for="header in headers_contact"
                            :key="header.key"
                            class="text-start font-weight-bold"
                            style="color: rgb(var(--v-theme-primary))"
                          >
                            {{ header.title }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(item, index) in data.contact_set"
                          :key="index"
                          style="
                            border-bottom: 1px solid rgba(var(--v-theme-primary), 0.05) !important;
                          "
                        >
                          <td class="py-3">{{ item.type }}</td>
                          <td class="py-3 font-weight-medium">
                            {{ item.branch_contact }}
                          </td>
                        </tr>
                      </tbody>
                    </v-table>
                    <div v-else class="py-8 text-center text-medium-emphasis">
                      <v-icon size="40" class="mb-2" color="grey-lighten-1"
                        >mdi-card-account-phone-outline</v-icon
                      >
                      <br />
                      {{
                        $i18n.locale === "ar"
                          ? "لا توجد بيانات تواصل"
                          : "No contact data available"
                      }}
                    </div>

                    <!--                   
                    <custom-data-table-add-with-field
                      :headers="headers_contact"
                      :items="data.contact_set"
                    >
                      <template v-slot:fields="{ item }">
                        <auto-list
                          name="ContactTypeChoices"
                          v-model="item.type"
                          :rules="[$required]"
                          cols="3"
                        />

                        <custom-text-field
                          v-model="item.branch_contact"
                          :rules="[$required, ...validateContact(item.type)]"
                          cols="3"
                          :type="
                            item.type == 1 || item.type == 3 || item.type == 4
                              ? 'number'
                              : 'text'
                          "
                        />
                      </template>
                    </custom-data-table-add-with-field>  -->
                  </VCardText></VCard
                >
              </VCol>
            </VCol>
          </template>
        </VRow>
      </VCardText>
      <VCardActions>
        <VRow>
          <VSpacer />
          <custom-btn type="refresh" :click="getData" variant="flat" color="info" />
          <!-- <custom-btn type="update" :click="saveData" variant="flat" class="ms-5" /> -->
        </VRow>
      </VCardActions>
    </VCard>
  </VForm>
</template>
<script>
import OrgChangePass from "../components/OrgTabs/OrgChangePass.vue";
import OrgActiveUser from "../components/OrgTabs/OrgActiveUser.vue";
import OrgApprovedUser from "../components/OrgTabs/OrgApprovedUser.vue";

export default {
  components: { OrgChangePass, OrgActiveUser, OrgApprovedUser },
  props: {
    id__organization: Number,
  },
  data() {
    return {
      url: "common/branch/",

      data: { contact_set: [] },
      fields: {},
      error: {},

      loading: false,
      approve_dialog: false,

      password: {
        show: false,
        showPass: false,
      },

      items: [
        {
          title: "basic_information",
          cols: 8,
          icon: "office-building",
          body: [
            { name: "name_ar", cols: 6 },
            { name: "name_en", cols: 6 },
            { name: "branch_no", cols: 4 },
            { name: "company_level_display", cols: 4 },
            { name: "fk_country", cols: 4 },
            { name: "fk_governorate", cols: 4 },
            { name: "description", cols: 4 },
          ],
        },
        {
          title: "geographical_location",
          cols: 4,
          icon: "map",
          body: [
            {
              name:
                "fk_address__fk_region__fk_directorate__fk_governorate__fk_country__name_ar",
              key: "fk_address__fk_region__fk_directorate__fk_governorate__fk_country",
            },
            {
              name: "fk_address__fk_region__fk_directorate__fk_governorate__name_ar",
              key: "fk_address__fk_region__fk_directorate__fk_governorate",
              cols: 6,
            },
            {
              name: "fk_address__fk_region__fk_directorate__name_ar",
              key: "fk_address__fk_region__fk_directorate",
              cols: 6,
            },
            {
              name: "fk_address__fk_region__name_ar",
              key: "fk_address__fk_region",
              cols: 6,
            },
            { name: "fk_address__street", cols: 6 },
          ],
        },
        {
          title: "advanced_settings",
          cols: 6,
          edit: true,
          icon: "cog-outline",
          body: [
            { name: "default_user_name_for_employees", edit: true, cols: 4 },
            { name: "default_password_for_employees", edit: true, cols: 4 },
            { name: "default_user_name_for_students", edit: true, cols: 4 },
            { name: "default_password_for_students", edit: true, cols: 4 },
            { name: "academic_id_length", edit: true, cols: 4 },
            { name: "subject_code", edit: true, cols: 4 },
            { name: "student_type", edit: true, cols: 4 },
            { name: "branch_type", edit: true, cols: 4 },
            { name: "use_hijri_calendar", edit: true, cols: 4 },
            { name: "attendance_twice", edit: true, cols: 4 },
            { name: "number_of_levels", edit: true, cols: 4 },
            { name: "batch_code_for_college", edit: true, cols: 4 },
            { name: "batch_code_for_specialization", edit: true, cols: 4 },
            { name: "semester_code_for_batch", edit: true, cols: 4 },
            { name: "semester_code_for_specialization", edit: true, cols: 4 },
            {
              name: "batch_code_for_differentiation_batch",
              edit: true,
              cols: 4,
            },
            { name: "card_title", edit: true, cols: 4 },
            { name: "card_title_color", edit: true, cols: 4 },
            { name: "card_info_title", edit: true, cols: 4 },
            { name: "card_info_title_color", edit: true, cols: 4 },
            { name: "card_background_image", edit: true, cols: 4 },
          ],
        },
        {
          title: "license_administrator_information",
          cols: 6,
          icon: "information-outline",
          body: [
            {
              name: "first_name",
              data: ["manager_user", "first_name"],
              cols: 4,
            },
            { name: "last_name", data: ["manager_user", "last_name"], cols: 4 },
            { name: "username", data: ["manager_user", "username"], cols: 4 },
            // { name: "email", data: ["manager_user", "email"], cols: 4 },
            {
              name: "user_type",
              data: ["manager_user", "fk_user_type"],
              cols: 4,
            },
            {
              name: "groups",
              data: ["manager_user", "groups_list_as_object"],
              cols: 12,
            },
          ],
        },
      ],

      draggedIndex: null,
    };
  },
  created() {
    this.getData();
    this.getFields();
  },
  methods: {
    getTabTitle(title) {
      if (title === "basic_information")
        return this.$i18n.locale === "ar" ? "البيانات الأساسية" : "Basic Information";
      if (title === "geographical_location")
        return this.$i18n.locale === "ar" ? "الموقع الجغرافي" : "Geographical Location";
      if (title === "license_administrator_information")
        return this.$i18n.locale === "ar"
          ? "معلومات الترخيص والمدير"
          : "License & Administrator Info";
      if (title === "advanced_settings")
        return this.$i18n.locale === "ar" ? "إعدادات متقدمة" : "Advanced Settings";
      if (title === "communication")
        return this.$i18n.locale === "ar" ? "التواصل" : "Communication";
      return title;
    },
    onDragStart(event, index) {
      this.draggedIndex = index;

      event.dataTransfer.effectAllowed = "move";
    },
    onDrop(event, dropIndex) {
      const draggedItem = this.items[this.draggedIndex];

      this.items.splice(this.draggedIndex, 1);
      this.items.splice(dropIndex, 0, draggedItem);
      this.draggedIndex = null;
    },
    refreshData() {
      if (this.error.data) this.getData();
      if (this.error.fields) this.getFields();
    },
    async getData() {
      this.loading = true;
      this.error.data = false;
      this.$axios(this.url + this.id__organization + "/")
        .then((response) => {
          const res = response.data.data || response.data;
          this.data = res;
        })
        .catch(() => {
          this.error.data = true;
        })
        .finally(() => {
          setTimeout(() => {
            this.loading = false;
          }, 300);
        });
    },

    async saveData(onlyImg = false) {
      const { valid } = await this.$refs.valid.validate();

      if (!valid) return;

      const formData = new FormData();

      formData.append("data", JSON.stringify({}));

      // if (!onlyImg) {
      //   formData.append("data", JSON.stringify(this.data));
      // }
      if (typeof this.data.img !== "string")
        formData.append("logo", this.data.logo || null);

      await this.$axios.patch(`common/branch/${this.id__organization}/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      this.snack("update");
    },

    async getFields() {
      this.loading = true;
      this.error.fields = false;
      this.$axios(`${this.setting.url_field}organizations/`)
        .then((response) => {
          let data = {};
          const res = response.data.data || response.data;
          res.forEach((el) => {
            data[el.name] = el;
          });

          this.fields = data;
        })
        .catch(() => {
          this.error.fields = true;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    validateContact(value) {
      if (value === 1 || value === 3 || value === 4)
        return [this.$min_length(6), this.$max_length(14)];
      else if (value === 2) return [this.$email];
      else return [this.$max_length(200)];
    },
  },
  computed: {
    headers_contact() {
      let headers = [
        {
          title:
            this.$i18n.locale === "ar"
              ? "نوع وسيلة التواصل"
              : "Communication Method Type",
          key: "type",
        },
        {
          title: this.$i18n.locale === "ar" ? "وسيلة التواصل" : "Communication Method",
          key: "branch_contact",
        },
      ];

      return headers;
    },
  },
};
</script>
