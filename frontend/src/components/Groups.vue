<template>
  <filter-fields :label="$t('semester_group')">
    <template #fields>
      <v-form ref="form_group">
        <v-row>
          <v-col class="pa-0" cols="12">
            <v-row class="align-center">
              <fields
                :data="$attrs.filters"
                :fields="
                  this.$filter_fields({
                    null: false,
                    width: 4,
                    disabled: $attrs?.filters?.index,
                    hideDetails: true,
                    returnObject: true,
                  })
                "
                :attr="{
                  fk_college: {
                    depend: true,
                    update: (val) => {
                      if (val) {
                        $attrs.filters.college_display = val?.name_ar;
                        $attrs.filters.fk_college = val?.id;
                      }
                    },
                  },
                  fk_specialization: {
                    depend: true,
                    param: $attrs?.filters.fk_college,
                    update: (val) => {
                      if (val) {
                        $attrs.filters.specialization_display = val?.name_ar;
                        $attrs.filters.fk_specialization = val?.id;
                      }
                    },
                  },
                  fk_batch: {
                    depend: true,
                    param: $attrs?.filters.fk_specialization,
                    update: (val) => {
                      if (val) {
                        $attrs.filters.batch_no = val?.fk_academic_year__year_m;
                        $attrs.filters.fk_batch = val?.id;
                      }
                    },
                  },
                  fk_level: {
                    depend: true,
                    param: $attrs?.filters.fk_batch,
                    update: (val) => {
                      if (val) {
                        $attrs.filters.level_display = val?.level_display;
                        $attrs.filters.fk_level = val?.id;
                      }
                    },
                  },
                  fk_semester: {
                    depend: true,
                    param: $attrs?.filters.fk_level,
                    update: (val) => {
                      if (val) {
                        $attrs.filters.semester_display = val?.semester_display;
                        $attrs.filters.fk_semester = val?.id;
                        setFkGroupData(
                          $attrs?.data?.groups?.find(
                            (item) => item?.fk_semester == val?.id
                          )?.fk_group
                        );
                      }
                    },
                  },
                }"
              >
                <template v-slot="{ field }">
                  <v-col cols="12" v-if="field?.name == 'fk_group'">
                    <filter-fields
                      class="border-dashed"
                      style="margin-bottom: 0 !important"
                      :label="$t('groups')"
                      :disabled="!$attrs?.filters?.fk_semester"
                    >
                      <template #fields>
                        <fields
                          :data="$attrs.filters"
                          :fields="
                            this.$filter_fields({
                              null: false,
                              width: 8,
                              hideDetails: true,
                              returnObject: true,
                            })
                          "
                          :attr="{
                            fk_group: {
                              depend: true,
                              param: $attrs?.filters.fk_semester,
                              multiple: true,
                              update: (val) => {
                                if (Array?.isArray(val)) {
                                  console.log(val);
                                  $attrs.filters.fk_group__name_ar = val?.map(
                                    (item) => item?.fk_grouping__name_ar
                                  );
                                  $attrs.filters.fk_group = val?.map(
                                    (item) => item?.id
                                  );
                                }
                              },
                            },
                          }"
                        ></fields>
                        <v-col class="pa-0">
                          <custom-btn
                            :type="$attrs?.filters?.index ? 'update' : 'add'"
                            :click="
                              () =>
                                $attrs?.filters?.index
                                  ? editToTable(
                                      $attrs?.data?.groups,
                                      { ...$attrs?.filters },
                                      $attrs?.filters?.index - 1
                                    )
                                  : addToTable(
                                      $attrs?.data?.groups,
                                      $attrs?.filters
                                    )
                            "
                            class="mt-1"
                          />
                        </v-col>
                      </template>
                    </filter-fields>
                  </v-col>
                </template>
              </fields>
            </v-row>
          </v-col>
          <v-col cols="12">
            <CustomDataTableAddWithField
              :headers="headers_groups"
              :withFields="false"
              :items="$attrs?.data?.groups || []"
            >
              <template #item.fk_group__name_ar="{ item }">
                <v-chip-group density="compact">
                  <v-chip
                    v-for="(list, index) in item?.fk_group__name_ar"
                    :key="index"
                    size="small"
                  >
                    {{ list }}
                  </v-chip>
                </v-chip-group>
              </template>
              <template #item.actions="{ item, index }">
                <span>
                  <custom-btn
                    :type="$attrs?.filters?.index != index + 1 ? 'update' : ''"
                    isIcon
                    :icon="$attrs?.filters?.index != index + 1 ? '' : 'close'"
                    elevation="0"
                    color="transparent"
                    :iconColor="
                      $attrs?.filters?.index != index + 1 ? 'green' : 'grey'
                    "
                    :click="
                      () =>
                        $attrs?.filters?.index != index + 1
                          ? editFromTable(item, index + 1)
                          : resetData(this.$attrs.filters)
                    "
                  />
                  <custom-btn
                    type="del"
                    isIcon
                    elevation="0"
                    color="transparent"
                    icon_color="red"
                    :click="() => removeFromTable(index)"
                    iconColor="red"
                  />
                </span>
              </template>
            </CustomDataTableAddWithField>
          </v-col>
        </v-row>
      </v-form>
    </template>
  </filter-fields>
</template>
<script>
export default {
  data() {
    return {
      //   filters: {
      //     fk_college: 8,
      //     fk_specialization: 11,
      //     fk_batch: 112,
      //     fk_level: 94,
      //     fk_semester: 217,
      //     fk_group: [300, 301, 302, 303],
      //     college_display: "كلية الطب",
      //     specialization_display: "طب بيطري",
      //     batch_no: "2022-2023",
      //     level_display: "المستوى الاول",
      //     semester_display: "الفصل الأول",
      //     fk_group__name_ar: [
      //       "المجموعة",
      //       "المجموعة 2",
      //       "المجموعة 3",
      //       "المجموعة عملي 1",
      //     ],
      //   },

      drawer: false,
    };
  },

  computed: {
    headers_groups() {
      let headers = [
        {
          title: this.$t("college"),
          key: "college_display",
        },
        {
          title: this.$t("specialization"),
          key: "specialization_display",
        },
        {
          title: this.$t("batch"),
          key: "batch_no",
        },
        {
          title: this.$t("level"),
          key: "level_display",
        },
        {
          title: this.$t("semester"),
          key: "semester_display",
        },
        {
          title: this.$t("group"),
          key: "fk_group__name_ar",
          chips: true,
        },
      ];

      return headers;
    },
  },
  methods: {
    async addToTable(
      main_array,
      new_obj,
      keys_to_merge = ["fk_group", "fk_group__name_ar"]
    ) {
      if (new_obj?.id || (await this.$validate(this.$refs["form_group"]))) {
        const match_index = main_array?.findIndex(
          (item) => item?.fk_semester == new_obj?.fk_semester
        );
        console.log(main_array, "ssssssssssssssss");
        if (match_index > -1) {
          const existing_object = main_array[match_index];

          keys_to_merge?.forEach((key) => {
            const existing_value = existing_object[key];
            const new_value = new_obj[key];
            if (Array?.isArray(existing_value) && Array?.isArray(new_value)) {
              const combined_values = new Set([
                ...existing_value,
                ...new_value,
              ]);
              console.log(combined_values, "______________");
              existing_object[key] = Array.from(combined_values);
            }
          });
        } else {
          main_array?.push({ ...new_obj });
        }
      }
    },
    removeFromTable(index) {
      this.$attrs?.data?.groups.splice(index, 1);
    },
    editFromTable(item, index) {
      Object.assign(this.$attrs.filters, { ...item, index });

      this.setFkGroupData(item?.fk_group);
    },
    editToTable(table_data, edited_data, index) {
      table_data[index] = edited_data;
      this.resetData(this.$attrs?.filters);
    },
    setFkGroupData(data) {
      setTimeout(() => {
        this.$attrs.filters.fk_group = data;
      }, 50);
    },

    resetData(data) {
      Object.keys(data).forEach((key) => {
        delete data[key];
      });
    },
  },

  watch: {
    "$attrs.data.id": {
      handler(newVal, oldVal) {
        if (newVal) {
          const groups = [...this.$attrs?.data?.groups];
          this.resetData(this.$attrs?.filters);
          Object.assign(this.$attrs.data, { ...this.$attrs.data, groups: [] });
          groups?.forEach((element) => {
            this.addToTable(this.$attrs?.data?.groups, {
              ...element,
              fk_group: [element?.id],
              fk_group__name_ar: [element?.fk_group__name_ar],
            });
          });
        }
      },
      immediate: true,
    },
  },
};
</script>
