<template>
  <!-- added by samer -->

  <v-skeleton-loader v-if="loading" :type="`table-row-divider@4`" />

  <v-card style="padding-top: 0 !important" elevation="0" v-else>
    <VCardTitle>
      <VRow>
        <v-tabs v-model="steps" stacked density="compact">
          <v-tab
            v-for="(item, key) in items"
            :key="key"
            :value="key"
            density="compact"
            slider-color="primary"
            @click="nextTab(key)"
            class="pa-0 ma-0"
          >
            <custom-tab
              :title="item.name"
              :is_current="key === step"
              :error="item.error"
              :index="key + 1"
            />
          </v-tab>
        </v-tabs>
        <VSpacer />
        <slot name="action"/>
        <custom-btn
          :type="isEdit ? 'update' : 'save'"
          class="align-self-center me-2"
          :click="saveData"
        />
      </VRow>
    </VCardTitle>

    <v-window v-model="steps" class="pt-5" activeSlide>
      <v-window-item :value="0" eager>
        <v-form ref="form_1">
          <VRow>
            <VCol cols="12" md="8">
              <VRow class="pa-2">
                <fields
                  :data="data"
                  :fields="
                    fields.filter((e) => e.group === 'Information Basic')
                  "
                  :attr="{
                    name_ar: {
                      readonly: !companyMin && !companyUni && !companyColl,
                    },
                    name_en: {
                      
                      readonly: !companyMin && !companyUni && !companyColl,
                      
                    },
                    established_date: {
                      depend: companyUniOrColl,
                    },
                    url: {
                      depend: data.id,
                    },

                    fk_parent_organization: {
                      param: data.company_level,
                      depend:
                        data_org.fk_parent_organization == 0 && fk_brunch == 0,
                    },
                    type_of_main_system: {
                      param: data.company_level,
                    },

                    ...filterAttr,
                  }"
                >
                  <template v-slot="{ field }">
                    <template v-if="field.name === 'company_level'">
                      <auto-list
                        v-model="data.company_level"
                        name="CompanyLevelFilterChoices"
                        cols="4"
                        :param="paramCompanyLevel"
                        :disabled="
                          data_org.fk_organization != 0 ||
                          (data_org.fk_parent_organization != 0 &&
                            data_org.company_level != 30)
                        "
                        @update:modelValue="getFilterField"
                      >
                        <template v-slot:append-inner>
                          <VIcon
                            icon="mdi-refresh"
                            @click="getFilterField"
                            v-if="error_location"
                          />
                        </template>
                      </auto-list>
                    </template>
                    <template v-if="field.name === 'fk_country'">
                      <auto-list
                        v-if="filterAttr?.fk_country?.depend || false"
                        v-model="data.fk_country"
                        name="Country"
                        cols="4"
                        label="الدولة"
                      />
                    </template>
                    <template v-if="field.name === 'fk_governorate'">
                      <auto-list
                        v-if="filterAttr?.fk_governorate?.depend || false"
                        v-model="data.fk_governorate"
                        name="Governorate"
                        cols="4"
                        label="المحافظة"
                        :param="data.fk_country"
                        @selectObject="changeGov"
                      />
                    </template>
                    <template v-if="field.name === 'fk_directorate'">
                      <auto-list
                        v-if="filterAttr?.fk_directorate?.depend || false"
                        v-model="data.fk_directorate"
                        name="Directorate"
                        cols="4"
                        label="المديرية"
                        :param="data.fk_governorate"
                        @selectObject="changeDir"
                      />
                    </template> </template
                ></fields>
              </VRow>
            </VCol>
            <VCol cols="12" md="4" class="pa-2 justify-items-center">
              
              <CustomImage
                v-model="data.logo"
                :title="$t('logo')"
                v-if="companyUniOrColl"

              />
            </VCol>
          </VRow>
        </v-form>
      </v-window-item>
      <v-window-item :value="1" eager>
        <v-form ref="form_2">
          <VRow>
            <fields
              :data="data"
              :fields="fields.filter((e) => e.group === 'Information Location')"
              :attr="{
                fk_address__fk_region__fk_directorate__fk_governorate__fk_country:
                  {
                    null: false,
                  },
                fk_address__fk_region__fk_directorate__fk_governorate: {
                  param:
                    data.fk_address__fk_region__fk_directorate__fk_governorate__fk_country,
                  null: false,
                },
                fk_address__fk_region__fk_directorate: {
                  param:
                    data.fk_address__fk_region__fk_directorate__fk_governorate,
                  null: false,
                },
                fk_address__fk_region: {
                  param: data.fk_address__fk_region__fk_directorate,
                   null: false,
                },
                coordinate: {
                  depend: companyUniOrColl,
                },
                coordinate_image: {
                  depend: companyUniOrColl,
                },
              }"
            />
          </VRow>
        </v-form>
      </v-window-item>
      <v-window-item :value="2" eager>
        <v-form ref="form_3">
          <VRow class="pa-2">
            <VCol cols="12" md="10">
              <VRow :style="`pointer-events:${isEdit ? 'none' : ''};`">
                <fields
                  :data="data"
                  :fields="
                    fields.filter(
                      (e) => e.group === 'Information Boss & License'
                    )
                  "
                  :attr="{
                    license_number: {
                      depend: companyUniOrColl,
                    },
                  }"
                />
                <VCol cols="12">
                  <fieldset class="mb-5 border rounded pa-2">
                    <legend class="mx-2 px-2">
                      <span>{{ $t("user_info") }}</span>
                    </legend>

                    <VRow class="pa-2">
                      <!--  disabled: data.id ? true : false -->
                      <fields
                        :data="data['manager_user']"
                        :fields="field_user"
                        :attr="{
                          first_name: {},
                          last_name: { disabled: data.id ? true : false },
                          username: { disabled: data.id ? true : false },

                          fk_user_type: { disabled: data.id ? true : false },

                          password: {
                            depend: isEdit ? false : true,
                          },
                          groups: {
                            param: param_to_group,
                          },
                        }"
                      />

                      <custom-btn
                        v-if="isEdit"
                        type="update"
                        label="تغيير كلة المرور"
                        class="mt-3"
                        @click="dialog_change_password = true"
                        style="pointer-events: visible !important"
                      />
                      <custom-btn
                        v-if="isEdit"
                        label="مصادقة المدير"
                        @click="dialog_approve_user = true"
                        class="mt-3 ms-5"
                        style="pointer-events: visible !important"
                      />
                    </VRow>
                  </fieldset>
                </VCol>
              </VRow>
              <custom-dialog
                v-model="dialog_approve_user"
                title="مصاقة المدير"
        
                width="500"
                height="300"
                class="px-2"
              >
                <template v-slot>
                  <custom-date
                    v-model="data['manager_user']['approved_to']"
                    label="تاريخ انتهاء الصلاحية"
                  />
                </template>
                <template v-slot:actions>
                  <custom-btn
                    type="save"
                    width="95%"
                    class="mx-2"
                    :click="approveManager"
                  />

                </template>

              </custom-dialog>
            </VCol>
            <VCol cols="12" md="2" class="pa-2 justify-items-center">
            
              <CustomImage
                v-if="companyUniOrColl"
                v-model="data.license_image"
                :title="$t('license_image')"
              />
            </VCol>
          </VRow>
        </v-form>
      </v-window-item>
      <v-window-item :value="3" eager>
        <v-form ref="form_4">
          <VRow class="pa-2">
            <fields
              :data="data"
              :fields="fields.filter((e) => e.group === 'Settings Advanced')"
              :attr="{
                student_type: {
                  depend: companyUniOrColl,
                },
                default_password_for_employees: {
                  depend: companyUniOrColl,
                },
                default_user_name_for_employees: {
                  depend: companyUniOrColl,
                },

                card_background_image: {
                  depend: companyUniOrColl,
                },
                card_title: {
                  depend: companyUniOrColl,
                },
                card_title_color: {
                  depend: companyUniOrColl,
                },
                card_info_title: {
                  depend: companyUniOrColl,
                },
                card_info_title_color: {
                  depend: companyUniOrColl,
                },
                use_hijri_calendar: {
                  depend: companyUniOrColl,
                },
                attendance_twice: {
                  depend: companyUniOrColl,
                },
                batch_code_for_college: {
                  depend: companyUniOrColl,
                },
                batch_code_for_specialization: {
                  depend: companyUniOrColl,
                },
                semester_code_for_batch: {
                  depend: companyUniOrColl,
                },
                semester_code_for_specialization: {
                  depend: companyUniOrColl,
                },
                subject_code: {
                  depend: companyUniOrColl,
                },
                batch_code_for_differentiation_batch: {
                  depend: companyUniOrColl,
                },
                default_password_for_students: {
                  depend: companyUniOrColl,
                },
                default_user_name_for_students: {
                  depend: companyUniOrColl,
                },
                academic_id_length: {
                  depend: companyUniOrColl,
                },
              }"
            />
          </VRow>
        </v-form>
      </v-window-item>
      <v-window-item :value="4" eager>
        <v-form ref="form_5">
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
          </custom-data-table-add-with-field>
        </v-form>
      </v-window-item>
    </v-window>

    <template v-slot:actions>
      <div v-if="step != 2 && !isEdit">
        <custom-btn
          type="reset"
          :label="$t('reset_current_page')"
          width="200"
          :click="() => resetForm(false)"
        />
        <custom-btn
          class="ms-2"
          type="reset"
          :label="$t('reset_all_pages')"
          :click="() => resetForm(true)"
        />
      </div>
    </template>
  </v-card>
  <custom-dialog
    v-model="dialog_change_password"
    width="300"
    height="300"
    :title="$t('change_password')"
  >
    <template v-slot>
      <VForm ref="form_password" @submit.prevent="changePassword">
        <custom-text-field
          v-model="password.new_password"
          icon="lock"
          :type="`${showPass ? 'text' : 'password'}`"
          :rules="[$required, $min_value(8)]"
          :label="$t('new_pass')"
        >
          <template v-slot:append-inner>
            <VIcon
              :icon="`${showPass ? 'mdi-eye-off' : 'mdi-eye'}`"
              @click="showPass = !showPass"
            />
          </template>
        </custom-text-field>
      </VForm>
    </template>
    <template v-slot:actions>
      <custom-btn
        type="update"
        :label="$t('change')"
        :click="changePassword"
        width="100%"
        class="mb-1"
      />
    </template>
  </custom-dialog>
</template>


<script>
import merge from "lodash";
import Field from "../../../components/FormInput/Field.vue";
import { state } from "@/../src/store/state";
import api from "../../../plugins/axios-plugin";

export default {
  components: { Field },
  props: {
    data_organization: {
      type: Object,
      default: () => {},
    },

    methodData: Function,
    modelValue: {
      type: [Object, String],
      default: null,
    },
  },
  data() {
    return {
      data_org: {},
      isEdit: false,
      approved_to: undefined,

      data: {},
      dialog_approve_user: false,

      contact_data: {},

      fk_brunch: state.organization_id || 0,

      password: {},
      error: {
        fields: false,
      },

      null_map: [],

      filter_attr: {},

      fields: [],

      validList: ["form_1", "form_2", "form_3", "form_4", "form_5"],

      field_user: [
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
          type: "CharField",
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
      ],

      step: 0,
      steps: 0,

      loading: false,

      dialog_change_password: false,
      showPass: false,
    };
  },
  async created() {
    try {
      this.loading = true;
      this.resetData();
      this.data_org = { ...this.data_organization };
 

      if (
        this.data_org.fk_parent_organization > 0 &&
        this.data_org.fk_organization == 0
      ) {
        this.data.fk_parent_organization = this.data_org.fk_parent_organization;
        this.data.company_level = Number(this.data_org.company_level) + 10;
      }
      await this.getFields();

      if (this.data_organization.fk_organization > 0) {
        this.isEdit = true;
        await this.getData();
      }
      await this.getFilterField(false);
    } finally {
      this.loading = false;
    }
  },

  methods: {
    // جلب حقول الشاشة
    async getFields() {
      this.error.fields = false;
      await this.$axios(`${this.setting.url_field}organizations/`)
        .then((response) => {
          const res = response.data.data || response.data;
          this.fields = res;
        })
        .catch(() => {
          this.error.fields = true;
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
    async getFilterField(reset = true) {
      if (!this.data.company_level) return;

      if (reset) {
        this.data.name_ar = "";
        this.data.name_en = "";

        this.data.fk_country = null;
        this.data.fk_governorate = null;
        this.data.fk_directorate = null;
        this.data.fk_region = null;
      }
      if (!this.data.company_level) return;
      try {
        // this.loading = true;
        this.error_location = false;

        await api("common/branch/data-for-add/", {
          params: {
            company_level: this.data.company_level,
          },
        })
          .then((e) => {
            let data = e?.data?.data;
            this.null_map = data?.null_map;

            let filter_attr = [
              { name: "fk_country", depend: false },
              { name: "fk_governorate", depend: false },
              { name: "fk_directorate", depend: false },
              { name: "fk_region", depend: false },
            ];
            data?.required_map?.forEach((required) => {
              const index = filter_attr.findIndex((e) => e.name === required);
              const itemsBeforIndex = filter_attr.slice(0, index);
              if (typeof index === "number") {
                filter_attr[index].depend = true;
                filter_attr[index].null = false;
              }
              if (itemsBeforIndex) {
                itemsBeforIndex.forEach((e) => {
                  e.depend = true;
                });
              }
            });

            let convertFilterToObj = {};

            filter_attr.forEach((e) => {
              convertFilterToObj[e.name] = {
                depend: e.depend || false,
                null: e.null ?? true,
              };
            });

            this.filter_attr = convertFilterToObj;
          })
          .catch((error) => {
            this.error_location = true;
          });
      } finally {
        // this.loading = false;
      }
    },

    changeGov(item, select) {
      
      this.data.name_ar = "";
      this.data.name_en = "";
      if (this.companyGov) {
        this.data.name_ar = "مكتب محافظة " + (select?.name || "");
        this.data.name_en = "Governorate office " + (select?.name_en || "");
      }
    },
    changeDir(item, select) {
      this.data.name_ar = "";
      this.data.name_en = "";

      if (this.companyDir) {
        
        this.data.name_ar = "مكتب مديرية " + (select?.name_ar || "");
        this.data.name_en = "Directorate office " + (select?.name_en || "");
      }
    },
    changeRegionData(item, select) {
      // let string_name = {};
      //     if (this.companyGov) {
      //       string_name.name_ar = "مكتب محافظة " + (select?.name_ar||'');
      //       string_name.name_en = "";
      //     } else if (this.companyDir) {
      //       string_name.name_ar = "مكتب مديرية " + (select?.name_ar||'');
      //       string_name.name_en = "";
      //     } else if (this.companyUni) {
      //       string_name.name_ar = "جامعة ";
      //       string_name.name_en = "";
      //     } else if (this.companyColl) {
      //       string_name.name_ar = "فرع ";
      //       string_name.name_en = "";
      //     }
      //     this.data.name_ar = string_name.name_ar;
      //     this.data.name_en = string_name.name_en;
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
          this.dialog_change_password = false;
          this.password = {};
        });
    },
    resetData() {
      this.data = {
        contact_set: [],
        manager_user: {},
        service_set: [],
      };
    },
    keyTab(event) {
      event.preventDefault();
      if (!event.shiftKey) this.tabTo();
    },
    tabTo() {
      this.step++;
      this.steps++;
    },

    resetForm(all) {
      if (all) {
        for (let i = 0; i < this.validList.length; i++) {
          const v = this.validList[i];
          this.$refs[v].reset();
        }
      } else {
        const v = this.validList[this.step];
        this.$refs[v].reset();
      }
    },

    async nextTab(key) {
      let index = this.step;
      const data = this.validList[index];
      const { valid } = await this.$refs[data].validate();
      if (!valid) {
        this.items[index].error = true;
      }
      if (valid)
        if (this.step <= 7) {
          this.items[index].color = "green";
        }
      this.step = key;
    },
    async getData() {
      try {
        this.loading = true;
        let url = `common/branch/${this.data_org.fk_organization}/`;

        if (this.$route.name === "basic-data") url = "common/branch/retrieve/";
        await this.$axios(url).then((response) => {
          const res = response.data.data || response.data;
          this.data = {
            ...res,
            fk_country:
              res.fk_country ||
              res.fk_governorate__fk_country ||
              res.fk_directorate__fk_governorate__fk_country,
            fk_governorate:
              res.fk_governorate || res.fk_directorate__fk_governorate,
          };
        });
        
      } finally {
        this.loading = false;
      }
    },
    async saveData() {
      for (let i = 0; i < this.validList.length; i++) {
        try {
          const v = this.validList[i];
          const { valid } = await this.$refs[v].validate();

          if (valid) this.items[i].error = false;
          else {
            this.step = i;
            this.steps = i;
            this.items[i].error = true;
            return;
          }
        } catch (error) {
          this.items[i].error = true;
        }
      }

      if (this.items.filter((e) => e.error == true).length > 0) return;

      if (!("contact_set" in this.data) || this.data.contact_set.length === 0) {
        this.$alert("info", {
          message: this.$t("at_least_one_contact_method_must_entered"),
        });
        this.step = 4;
        this.steps = 4;
        return;
      }
      let data = merge.cloneDeep(this.data);

      this.null_map.forEach((item) => {
        data[item] = null;
      });

      data.fk_address = {
        fk_region: data.fk_address__fk_region,
        street: data.fk_address__street,
      };
      if (this.isEdit) data.fk_address.id = this.data.fk_address.id;

      const formData = new FormData();

      if (data.logo && typeof data?.logo === "object")
        formData.append("logo", data.logo);
      else delete data.logo;

      if (data.coordinate_image && typeof data?.coordinate_image === "object")
        formData.append("coordinate_image", data.coordinate_image);
      else delete data.coordinate_image;

      if (data.license_image && typeof data?.license_image === "object")
        formData.append("license_image", data.license_image);
      else delete data.license_image;

      data.boss =
        data.manager_user.first_name + " " + data.manager_user.last_name;
      var profile = state.profile;

      if (profile.ip && this.data_org.fk_parent_organization === 0) {
        data.fk_parent_organization = profile.ip;
      }

      if (!data.fk_parent_organization)
        data.fk_parent_organization = state.organization_id;

      formData.append("data", JSON.stringify(data));
      formData.append("manager_user", JSON.stringify(this.data.manager_user));

      this.isEdit
        ? await this.$axios.put(
            `common/branch/${this.data_org.fk_organization}/`,
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )
        : await this.$axios.post("common/branch/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });

      this.$snack(this.isEdit ? "update" : "add");
      this.resetForm(true);
      this.resetData();

      this.methodData();
      this.$emit("update:modelValue", false);
    },
  },
  computed: {
    items() {
      return [
        { name: this.$t("basic_information"), color: "primary" },
        {
          name: this.$t("geographical_location"),
          color: "primary",
        },
        {
          name: this.$t("license_administrator_information"),
          color: "primary",
        },
        {
          name: this.$t("advanced_settings"),
          color: "primary",
        },
        {
          name: this.$t("communication"),
          color: "primary",
        },
      ];
    },

    param_to_group() {
      if (this.data?.manager_user?.fk_user_type && this.data.company_level)
        return {
          fk_user_type: this.data.manager_user.fk_user_type,
          company_level: this.data.company_level,
        };
      else return undefined;
    },
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
    filterAttr() {
      let dataReq = {
        fk_governorate: {
          param: this.data.fk_country,
        },
        fk_directorate: {
          param: this.data.fk_governorate,
        },
        fk_region: {
          param: this.data.fk_directorate,
        },
      };

      Object.entries(this.filter_attr).forEach(([key, val]) => {
        dataReq[key] = {
          ...val,
          ...dataReq[key],
        };
      });

      return dataReq;
    },

    companyAdmin() {
      return this.data.company_level == 10;
    },
    companyMin() {
      return this.data.company_level == 20;
    },
    companyGov() {
      return this.data.company_level == 30;
    },

    companyDir() {
      return this.data.company_level == 40;
    },
    companyUni() {
      return this.data.company_level == 50;
    },
    companyColl() {
      return this.data.company_level == 60;
    },

    companyUniOrColl() {
      return this.data.company_level == 50 || this.data.company_level == 60;
    },
    paramCompanyLevel() {
      return {
        company_level: this.data_org.company_level,
        isEdit: this.data_org.fk_organization != 0,
      };
    },
  },
};
</script>