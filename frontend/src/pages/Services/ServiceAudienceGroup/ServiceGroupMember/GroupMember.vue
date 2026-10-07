<template>
  <custom-dialog
    v-model="dialog"
    :title="$t('group_member')"
    width="auto"
    min-width="1700"
    ><v-form ref="form">
      <filter-fields :label="$t('filter_fields')">
        <template #fields>
          <auto-list
            v-if="super_user"
            v-model="filter.fk_governorate"
            name="OrgGovernorate"
            cols="2"
            :add="false"
            :rules="[$required]"
          />
            <auto-list
            v-if="super_user"
            v-model="filter.fk_directorate"
            name="OrgDirectorate"
            cols="2"
            :add="false"
            :rules="[$required]"
          />
            <auto-list
            v-if="super_user"
            v-model="filter.fk_school"
            name="OrgSchoolByDirectorate"
            cols="2"
            :add="false"
            :rules="[$required]"
          />
          <custom-btn type="filter" class ="mb-5":click="getData"  />
        </template>
      </filter-fields>
    </v-form>
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <custom-data-table-with-save
        :="{
          headers,
          getData,
          items,
          top: false,
        }"
        v-if="can_update_or_add"
        :canSearch="false"
        :click="saveData"
      >
        <template v-slot:action>
          <div class="d-flex">
            <custom-btn
              :disabled="click"
              icon="account-multiple-check-outline"
              color="primary"
              cols="2"
              @click="selectAllActive"
            ></custom-btn>
          </div>
        </template>
      </custom-data-table-with-save>
    </div>
  </custom-dialog>
</template>

<script>
import { state } from "@/store/state";
export default {
  props: {
    modelValue: Boolean,
    fk_group: Number,
    embedded: {
      type: Boolean,
      default: false,
    },
    is_details: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      items: [],
      items_send: ["fk_user", "full_name_ar", "is_active", "notes"],
      filter: {},
      url: "d-services/",
      url_students: "student-affairs/student/",
    };
  },
  computed: {
    super_user() {
      return state.is_super_user;
    },
    collage_param() {
      if (this.super_user) {
        return this.filter.fk_org;
      } else {
        return state.organization_id;
      }
    },
    can_update_or_add() {
      return this.items.length;
    },
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
    headers() {
      return [
        {
          title: this.$t("student"),
          key: "full_name_ar",
        },
        {
          title: this.$t("is_active"),
          key: "is_active",
          field: {
            name: "is_active",
            type: "BooleanField",
            null: false,
            width: "4",
          },
        },
        {
          title: this.$t("notes"),
          key: "notes",
          field: {
            name: "notes",
            type: "TextField",
            icon: "number",
            rows: 1,
            null: true,
            height: "10",
            width: "600",
            attributes: {
              dir: "rtl",
            },
          },
        },
      ];
    },
  },
  methods: {
    async getData() {
      if (!this.fk_group) return;
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;
      this.loading = true;
      try {
        const filterMappings = {
          fk_section: this.filter?.fk_section,
          fk_branch_class: this.filter?.fk_branch_class,
        };

        const filters = Object.entries(filterMappings)
          .filter(([_, value]) => value !== null && value !== undefined && value !== "")
          .map(([field, value]) => ({ field, value }));
        if (filters.length === 0) {
          this.loading = false;
          return;
        }

        const response = await this.$axios.post(this.url_students + "filter/", {
          filters,
        });
        const data = response?.data?.data || response?.data;
        this.items = data.map((item) => {
          if (!("is_active" in item)) item.is_active = false;
          if (!("notes" in item)) item.notes = "";
          return item;
        });
      } catch (err) {
        console.log(err);
        this.items = {};
      } finally {
        this.loading = false;
      }
    },
    selectAllActive() {
      const allActive =
        this.items.length > 0 && this.items.every((item) => item.is_active);
      this.items.forEach((item) => {
        item.is_active = !allActive;
      });
    },
    async saveData() {
      const payload = this.items.map((item) => {
        const newObj = {};
        this.items_send.forEach((col) => {
          if (col in item) {
            newObj[col] = item[col];
          }
        });
        return newObj;
      });
      return await this.$axios
        .post(this.url + `audience-groups/${this.fk_group}/add-members/`, {
          students: payload,
        })
        .then((res) => {
          this.$snack("add", { message: res.data.message });
        });
    },
  },
};
</script>
