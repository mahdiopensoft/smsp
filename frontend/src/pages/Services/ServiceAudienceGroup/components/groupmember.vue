<template>
ممممم
  <custom-dialog
    v-model="dialog"
    :title="$t('group_member') + '   ( ' + title + ' ) '"
    width="auto"
    min-width="1700"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <v-form ref="form">
        <filter-fields :label="$t('filter_fields')">
          <template #fields>
            <fields
              :data="filter"
              :fields="
                $filter_fields({
                  hideDetails: true,
                  null: true,
                })
              "
              :attr="{}"
            >
            </fields>
            <!-- :param="$state.organization_id" -->
            <!-- name="CollegeForBatch" -->
            <auto-list
              v-model="filter.fk_college"
              name="College"
              cols="2"
              :add="false"
              :rules="[$required]"
            />
            <auto-list
              v-model="filter.fk_specialization"
              name="SpecializationForCollege"
              :param="filter.fk_college"
              cols="2"
              :rules="[$required]"
              :add="false"
            />
            <auto-list
              v-model="filter.fk_batch"
              name="BatchBySpecialization"
              cols="2"
              :param="filter.fk_specialization"
              :add="false"
              :rules="[$required]"
            />
            <auto-list
              v-model="filter.fk_student__student_status"
              name="StudentStatusChoiceWithOutRegister"
              cols="2"
              :add="false"
            />
            <!-- <v-col> -->
            <custom-btn type="filter" :click="getData"  />
            <!-- </v-col> -->
          </template>
        </filter-fields>
      </v-form>
      <custom-data-table-with-save
        :="{
          headers: headers,
          getData: getData,
          items: items,
          top: false,
        }"
        :click="
          is_data
            ? null
            : $perm('add', 'service-audience-group') ||
              $perm('edit', 'service-audience-group')
            ? save
            : null
        "
      ></custom-data-table-with-save>
      <!-- :canAdd="is_details ? null : true" -->
    </div>
  </custom-dialog>
</template>

<script>
export default {
  props: {
    modelValue: Boolean,
    group: Object,
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
      filter: {},
      loading: false,
      items: [],
      url: "d-services/group-members/",
    };
  },
  computed: {
    is_data() {
      this.items.length > 0;
    },
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
    title() {
      return this.group?.name_ar || "";
    },
    headers() {
      return [
        {
          title: this.$t("student"),
          key: "fk_user",
          // field: {
          //   name: "fk_user",
          //   type: "CharField",
          //   multiple: true,
          //   name_list: "AllStudents",
          //   rules: [this.$duplicate(this?.items.map((e) => e.fk_user))],
          //   icon: "text",
          //   null: false,
          //   cols: 5,
          //   max_length: 255,
          //   width: "500",
          // },
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
            name: "description",
            type: "TextField",
            icon: "number",
            null: true,
            width: "400",
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
      if (!this.group?.id) return;
      try {
        const { valid } = await this.$refs.form.validate();
        if (valid) {
          this.loading = true;
          await this.$axios
            .post(`${this.url}` + "filter/", {
              filters: [{ field: "fk_group", value: this.group.id }],
            })
            .then((response) => {
              this.items = response.data.data ?? [];
            });
        }
      } finally {
        this.loading = false;
      }
    },
    async save() {
      return await this.$axios
        .post(this.url, {
          fk_group: this.group?.id,
          services_conditions: this.items,
        })
        .then((res) => {
          this.$snack("add", { message: res.data.message });
        });
    },
  },
  watch: {
    dialog(val) {
      if (val) {
        this.getData();
      }
    },
    "group.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getData();
        }
      },
      immediate: true,
    },
  },
};
</script>
