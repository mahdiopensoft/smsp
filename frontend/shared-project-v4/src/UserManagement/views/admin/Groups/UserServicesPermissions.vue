<template>
  <VForm ref="form" @submit.prevent="saveData">
    <VRow>
      <custom-btn
        :type="fk_user > 0 ? 'update' : 'save'"
        class="mt-5"
        :click="saveData"
        width="100%"
        is_submit
      />
      <custom-btn
        class="mt-2"
        :color="allChecked ? 'error' : 'primary'"
        :prepend-icon="allChecked ? 'mdi-cancel' : 'mdi-check'"
        @click="toggleAllPermissions"
        :label="allChecked ? 'الغاء تحديد الكل' : 'تحديد الكل'"
      >
      </custom-btn>
    </VRow>
  </VForm>
  <VCard :loading="loading" class="mt-2">
    <v-tabs v-model="tab" class="border text-medium-emphasis" variant="solo">
      <v-tab
        v-for="category in categories"
        :key="category.id"
        :value="category.id"
        color="primary"
        @click="tab = category.id"
      >
        {{ category.name }}
      </v-tab>
    </v-tabs>

    <VCardText>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          <template v-if="category.id === tab && categories.length > 0">
            <VLazy v-if="servicesByCategory?.length > 0">
              <VExpansionPanels multiple>
                <v-expansion-panel
                  v-for="service in servicesByCategory"
                  :key="service.id"
                >
                  <VExpansionPanelTitle>
                    <VCheckboxBtn
                      inline
                      hide-details
                      density
                      color="primary"
                      @click.stop
                      :model-value="isRowSelected(service.permissions)"
                      @click="toggleRow(service.permissions)"
                      :indeterminate="indeterminateRow(service.permissions)"
                      :disabled="service?.permissions.every(p=>p.disabled==true)"
                    />
                    <span class="ms-2">{{ service.name }}</span>
                    <v-chip density="compact" class="ms-2">
                      {{ service?.permissions?.length }} صلاحيات
                    </v-chip>
                    <v-chip
                      density="compact"
                      color="primary"
                      class="ms-2"
                      v-if="selectedPermissionsCount(service?.permissions)"
                    >
                      تم تحديد
                      {{ selectedPermissionsCount(service?.permissions) }}
                    </v-chip>
                  </VExpansionPanelTitle>
                  <VExpansionPanelText>
                    <template
                      v-for="(per, index) in service.permissions"
                      :key="index"
                      style="width: 70px !important"
                    >
                      <VLazy>
                        <VCheckbox
                          :model-value="true"
                          density
                          color="primary"
                          :disabled="per.disabled"
                          v-if="per.disabled"
                        >
                          <template v-slot:label>
                            <span class="ms-2">
                              {{ per.custom_perm_name }}
                            </span>
                            <span  class="px-2"
                              >* صلاحية موروثة من المجموعة</span
                            >
                          </template>
                        </VCheckbox>
                        <VCheckbox
                          v-bind="props"
                          v-model="per.checked"
                          density
                          color="primary"
                          v-else
                        >
                          <template v-slot:label>
                            <span class="ms-2">
                              {{ per.custom_perm_name }}
                            </span>
                          </template>
                        </VCheckbox>
                      </VLazy>
                    </template>
                  </VExpansionPanelText>
                </v-expansion-panel>
              </VExpansionPanels>

              <VTable fixed-header height="68vh" density="compact" v-if="false">
                <thead>
                  <tr>
                    <th>اسم الخدمة</th>
                    <th>الصلاحيات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="service in servicesByCategory" :key="service.id">
                    <td>
                      <VLazy>
                        <v-checkbox-btn
                          :style="`min-width: 200px !important;`"
                          hide-details
                          density
                          color="primary"
                        >
                          <!-- :model-value="isRowSelected(service)" -->
                          <!-- @click="toggleRow(service)" -->
                          <!-- :indeterminate="indeterminateRow(service)" -->
                          <template v-slot:label>
                            <span class="ms-2">
                              {{ service.name }}
                            </span>
                          </template>
                        </v-checkbox-btn>
                      </VLazy>
                    </td>
                    <td class="d-flex justify-space-between">
                      <template
                        v-for="(per, index) in service.permissions"
                        :key="index"
                        style="width: 70px !important"
                      >
                        <VLazy>
                          <VCheckbox
                            v-bind="props"
                            v-model="per.checked"
                            style="width: 70px !important"
                            :hint="per.custom_perm_name"
                            persistent-hint
                            density
                          />
                        </VLazy>
                      </template>
                    </td>
                  </tr>
                </tbody>
              </VTable>
            </VLazy>
            <VCard v-else class="text-center py-2">
              لا توجد خدمات تحت هذا التصنيف
            </VCard>
          </template>
        </v-tabs-window-item>
      </v-tabs-window>
    </VCardText>
  </VCard>
</template>
<script>
export default {
  data() {
    return {
      data: {},

      fk_user: this.$route?.params?.user_id,
      categories: [],
      permissions: [],
      services_by_category: [],
      tab: undefined,
      services: [],
      loading: false,
      user_data: {},
    };
  },

  async mounted() {
    await this.getUserServicePermissions();
    await this.getServiceCategories();
    // this.getOperationType();
    await this.getServicesPermissions();
  },

  methods: {
    selectedPermissionsCount(permissions) {
      if (!permissions) return 0;
      return permissions?.filter((perm) => perm.checked === true)?.length;
    },

    // جلب فئات الخدمات
    async getServiceCategories() {
      return await this.$axios("d-services/workflow/categories/all/").then(
        (response) => {
          this.categories = response.data;
          if (response.data.length > 0) this.tab = response.data[0].id;
        }
      );
    },

    // جلب الخدمات مع الصلاحيات
    async getServicesPermissions() {
      try {
        this.loading = true;
        const userPermissionsMap = new Map(
          this.user_data?.permissions?.map((perm) => [perm.id, perm.inherited])
        );
        this.$axios("d-services/workflow/services-permissions/").then(
          (resp) => {
            this.services = resp.data;
            this.services
              ?.flatMap((service) => service?.permissions)
              ?.forEach((perm) => {
                (perm.checked = userPermissionsMap.has(perm.id)),
                  (perm.disabled = userPermissionsMap.get(perm.id) == true);
              });
          }
        );
      } finally {
        this.loading = false;
      }
    },

    // تحديد الكل
    toggleAllPermissions() {
      const newValue = !this.allChecked;
      this.flatedPermissions.forEach((p) => {
        p.checked = newValue;
      });
    },
    indeterminateRow(permissions) {
      const values = permissions.map((item) => item?.checked);

      let hasTrue = false;
      let hasFalse = false;

      for (const val of values) {
        if (val !== null) {
          if (val) hasTrue = true;
          else if (!val) hasFalse = true;
          if (hasTrue && hasFalse) break;
        }
      }

      return values.length > 0 && hasTrue && hasFalse;
    },
    // تحديد الصف
    toggleRow(permissions) {
      const select = this.isRowSelected(permissions);
      permissions.forEach((e) => {
        if (e) e.checked = !select;
      });
    },
    isRowSelected(permissions) {
      return permissions.every((e) => e?.checked === true);
    },
    async getUserServicePermissions() {
      return await this.$axios(
        `d-services/permissions/user-services-permissions/${this.fk_user}/`
      ).then((response) => {
        this.user_data = response.data;
      });
    },
    async saveData() {
      return await this.$axios
        .post(
          `d-services/permissions/user-services-permissions/${this.fk_user}/`,
          {
            fk_user: this.fk_user,
            permissions: this.flatedPermissions
              ?.filter((perm) => perm.checked == true)
              ?.map((perm) => perm.id),
          }
        )
        .then((response) => {
          this.$snack("update", { message: response.data });
        });
    },
  },
  computed: {
    flatedPermissions() {
      return this.services?.flatMap((service) => service?.permissions) ?? [];
    },
    servicesByCategory() {
      return this.services?.filter(
        (service) => service.fk_category == this.tab
      );
    },

    // اختيار الكل
    allChecked() {
      return this.flatedPermissions?.every((p) => p.checked === true);
    },
  },
};
</script>
