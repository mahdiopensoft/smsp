<template>
  <VRow v-if="loading">
    <VCol cols="12">
      <v-skeleton-loader :type="`text`" />
    </VCol>
    <VCol cols="12" lg="4" md="4" v-for="load in 5" :key="load">
      <v-skeleton-loader :type="`card`" />
    </VCol>
  </VRow>
  <VRow v-else-if="error.fields || error.data">
    <error-in-server @click="refreshData" />
  </VRow>
  <VForm ref="valid" v-else>
    <VCard elevation="0">
      <VCardText>
        <VRow class="ms-5">
          <custom-image
            v-model="data.license_image"
            width="70"
            height="70"
            :canEdit="false"
          />
          <VSpacer />

          <custom-btn
            type="update"
            label="تغيير كلة المرور"
            class="mt-3"
            @click="password.show = true"
            style="pointer-events: visible !important"
          />
          <custom-btn
            label="مصادقة المدير"
            @click="approve_dialog = true"
            class="mt-3 ms-5"
            style="pointer-events: visible !important"
          />
          <slot name="action" />
        </VRow>

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
                class="rounded-xl border-grey-lighten-2"
                variant="outlined"
              >
                <VCardTitle class="pa-5 d-flex align-center">
                  <VIcon color="primary" class="ml-3" size="28">{{
                    "mdi-" + item.icon
                  }}</VIcon>
                  <span class="font-weight-bold">
                    {{ $t(item.title) }}
                  </span>
                  <VSpacer />
                  <!-- <VChip
                    size="small"
                    variant="flat"
                    :color="item.edit ? 'secondary' : 'primary'"
                    append-icon="mdi-information-outline"
                  >
                    {{ item.edit ? "قابل للتعديل" : "غير قابل للتعديل" }}
                  </VChip> -->
                </VCardTitle>
                <VDivider class="border-opacity-20" />

                <VCardText>
                  <VRow>
                    <template
                      v-for="(body, body_index) in item.body"
                      :key="body_index"
                    >
                      <template
                        v-if="
                          Array.isArray(
                            body?.data?.reduce((acc, key) => acc?.[key], data)
                          )
                        "
                      >
                        <VCol :cols="body.cols">
                          <VCard elevation="1" rounded="xl">
                            <VCardText>
                              <h3 class="text-title-large mt-0 mb-2">
                                {{ $t(body.name) }}
                              </h3>
                              <VDivider />

                              <v-chip-group
                                v-if="
                                  body?.data?.reduce(
                                    (acc, key) => acc?.[key],
                                    data
                                  )?.length
                                "
                              >
                                <v-chip
                                  v-for="(el, index) in body?.data
                                    ?.reduce((acc, key) => acc?.[key], data)
                                    .map((item) => item.name_ar)"
                                  :key="index"
                                >
                                  {{ el }}
                                </v-chip>
                              </v-chip-group>
                              <div
                                class="pa-5"
                                style="text-align: center"
                                v-else
                              >
                                <VLabel>لايوجد مجموعات</VLabel>
                              </div>
                            </VCardText>
                          </VCard>
                        </VCol>
                        <!-- <custom-text-field
                          :model-value="
                            body?.data
                              ?.reduce((acc, key) => acc?.[key], data)
                              .map((item) => item.name_ar)
                              .join(', ')
                          "
                          :label="$t(body.name)"
                          :cols="body.cols"
                        /> -->
                      </template>
                      <template v-else>
                        <custom-text-field
                          :model-value="
                            data[body.name] ||
                            body?.data?.reduce((acc, key) => acc?.[key], data)
                          "
                          :cols="body.cols"
                          :label="
                            fields?.[body.key || body.name]?.label_ar ||
                            $t(body.name)
                          "
                          readonly
                        />
                      </template>
                      <!-- :readonly="!body.edit" -->
                    </template>
                  </VRow>
                </VCardText>
              </VCard>

              <VCol
                v-if="index === items.length - 1"
                cols="12"
                class="mt-5 pa-0"
              >
                <VCard class="rounded-xl border-opacity-20" variant="outlined">
                  <VCardTitle class="pa-5 d-flex align-center">
                    <VIcon color="primary" class="ml-3" size="28"
                      >mdi-map-marker-radius</VIcon
                    >
                    <span class="font-weight-bold">
                      {{ $t("communication") }}
                    </span>
                    <VSpacer />
                  </VCardTitle>
                  <VDivider class="border-opacity-20" />
                  <VCardText class="text-center">
                    <v-table v-if="data?.contact_set?.length">
                      <thead class="bg-header custom-data-table">
                        <tr>
                          <td v-for="header in headers_contact" :key="header">
                            {{ header.title }}
                          </td>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(item, index) in data.contact_set"
                          :key="index"
                        >
                          <td>{{ item.type }}</td>
                          <td>{{ item.branch_contact }}</td>
                        </tr>
                      </tbody>
                      <tr></tr>
                    </v-table>
                    <Vlabel v-else> لايوجد بيانات </Vlabel>

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
      <!-- <VCardActions>
        <VRow>
          <VSpacer />
          <custom-btn type="refresh" :click="getData" variant="flat" />
          <custom-btn
            type="update"
            :click="saveData"
            variant="flat"
            class="ms-5"
          />
        </VRow>
      </VCardActions> -->
    </VCard>
  </VForm>

  <custom-dialog
    v-model="password.show"
    width="300"
    height="auto"
    title="تغيير كلمة المرور"
  >
    <template v-slot>
      <password v-model="password.data" :id="data?.manager_user?.id" />
    </template>
  </custom-dialog>

  <custom-dialog
    v-model="approve_dialog"
    title="مصاقة المدير"
    height="170"
    width="500"
    class="px-2"
  >
    <template v-slot>
      <custom-date
        v-model="data['manager_user']['approved_to']"
        label="تاريخ انتهاء الصلاحية"
      />
      <custom-btn
        type="save"
        width="95%"
        class="mx-2"
        :click="approveManager"
      />
    </template>
  </custom-dialog>
</template>
 <script>
export default {
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
        data: {},
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
              name: "fk_address__fk_region__fk_directorate__fk_governorate__fk_country__name_ar",
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

    async saveData() {
      const { valid } = await this.$refs.valid.validate();

      if (!valid) return;

      const formData = new FormData();

      formData.append("data", JSON.stringify(this.data));
      if (typeof this.data.img !== "string")
        formData.append("img", this.data.img || null);

      await this.$axios.patch("common/branch/me/", formData);
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

    async changePassword() {
      const { valid } = await this.$refs.form_password.validate();
      if (!valid) return;

      await this.$axios
        .post(
          `user-manager/users/${this.data?.manager_user?.id}/admin-change-password/`,
          {
            new_password: this.password.new_password,
          }
        )
        .then(() => {
          this.$snack("update");

          this.password = {
            show: false,
            showPass: false,
          };
        });
    },
    async approveManager() {
      await this.$axios
        .post(`user-manager/users/${this.data.manager_user.id}/approve/ `, {
          approved_to: this.data["manager_user"]["approved_to"],
        })
        .then((e) => {
          this.$alert("add", { message: e.data });
        });
    },
  },
  computed: {
    headers_contact() {
      let headers = [
        {
          title: this.$t("type_communication_method"),
          key: "type",
        },
        {
          title: this.$t("communication_method"),
          key: "branch_contact",
        },
      ];

      return headers;
    },
  },
  watch: {
    "password.show"(val) {
      if (!val) {
        this.password.data = {};
      }
    },
  },
};
</script>
