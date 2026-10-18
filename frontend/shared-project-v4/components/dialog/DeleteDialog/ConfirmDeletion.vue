<template>
  <!-- Confirmation Dialog -->
  <v-dialog v-model="value" max-width="500" transition="dialog-transition">
    <template v-slot:activator="{ props: activatorProps }">
      <slot name="activator" :props="activatorProps" />
    </template>
    <template v-slot:default="{ isActive }">
      <v-card class="message-card border-thin error overflow-hidden" elevation="1">
        <!-- Header Section (Alert Style) -->
        <div
          class="header-section d-flex align-start px-6 pt-6 pb-4 position-relative"
          style="background-color: rgba(var(--v-theme-error), 0.08)"
        >
          <v-avatar
            color="error"
            variant="tonal"
            size="46"
            class="me-4 flex-shrink-0 rounded-lg"
          >
            <v-icon size="26">mdi-alert-circle-outline</v-icon>
          </v-avatar>

          <div class="d-flex flex-column flex-grow-1 pt-1">
            <v-card-title class="pa-0 text-h6 font-weight-bold line-height-1-2">
              {{ $t("warning") }}
            </v-card-title>
          </div>
        </div>

        <v-card-text
          class="px-6 py-6 text-body-1"
          style="color: rgba(var(--v-theme-on-surface), 0.7)"
        >
          <div class="mb-2">
            {{
              $i18n.locale == "ar"
                ? "في حالة تم الحذف سيتم نقل السجل الى المحذوفات"
                : "if deleted , the record will be moved to the Recycle Bin"
            }}
          </div>
          <div class="font-weight-medium text-error">
            {{
              $i18n.locale == "ar"
                ? "يتضمن ذلك جميع البيانات المرتبطة."
                : "This includes all associated data."
            }}
          </div>
        </v-card-text>

        <v-divider class="opacity-05" />

        <v-card-actions class="px-6 py-4 justify-end gap-3">
          <!-- Cancel Button (Standard Neutral Style) -->
          <v-btn
            color="grey-darken-1"
            variant="text"
            class="font-weight-bold"
            @click="value = false"
          >
            {{ $i18n.locale == "ar" ? "تراجع" : "Cancel" }}
          </v-btn>

          <!-- Delete Button (High Emphasis / Danger) -->
          <v-btn
            v-if="!is_restore_screen"
            color="error"
            variant="flat"
            class="px-8 font-weight-bold rounded-lg"
            @click="deleteData(false)"
            :loading="del_loading"
            height="40"
          >
            {{ $i18n.locale == "ar" ? "نعم، احذف" : "Yes, Delete" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>

  <!-- Protected Records Alert -->
  <alert-protected-records
    v-model="protected_records"
    :data_message="message_protected_records"
  >
    <template v-slot:actions>
      <v-btn
        variant="flat"
        color="error"
        class="font-weight-bold px-6 rounded-lg"
        :loading="del_loading"
        @click="deleteData(true)"
      >
        {{ $i18n.locale == "ar" ? "حذف إجباري" : "Force Delete" }}
      </v-btn>
    </template>
  </alert-protected-records>

  <!-- Success/Summary Dialog -->
  <v-dialog v-model="success_del" max-width="500" transition="dialog-transition">
    <v-card class="message-card border-thin success overflow-hidden" elevation="1">
      <!-- Success Header -->
      <div
        class="header-section d-flex align-start px-6 pt-6 pb-4 position-relative"
        style="background-color: rgba(var(--v-theme-success), 0.08)"
      >
        <v-avatar
          color="success"
          variant="tonal"
          size="46"
          class="me-4 flex-shrink-0 rounded-lg"
        >
          <v-icon size="26">mdi-check-circle-outline</v-icon>
        </v-avatar>

        <div class="d-flex flex-column flex-grow-1 pt-1">
          <v-card-title class="pa-0 text-h6 font-weight-bold line-height-1-2">
            {{ alert_del.message }}
          </v-card-title>
        </div>
      </div>

      <v-card-text class="px-6 py-4">
        <div class="results-container mt-2">
          <!-- Deleted Objects -->
          <template v-if="alert_del.deleted_objects?.length > 0">
            <p class="text-overline font-weight-black text-success mb-2">
              {{ $i18n.locale == "ar" ? "العناصر المحذوفة" : "Deleted Elements" }}
            </p>
            <v-table class="clean-sneat-table mb-4 border rounded-lg">
              <thead>
                <tr>
                  <th class="text-left"># ID</th>
                  <th class="text-left">
                    {{ $i18n.locale == "ar" ? "الاسم" : "Name" }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, key) in alert_del.deleted_objects" :key="key">
                  <td class="text-caption font-weight-bold">#{{ item.id }}</td>
                  <td class="text-body-2">{{ item.name }}</td>
                </tr>
              </tbody>
            </v-table>
          </template>

          <!-- Invalid IDs -->
          <template v-if="alert_del?.invalid_ids?.length > 0">
            <p class="text-overline font-weight-black text-error mb-2">
              {{ $i18n.locale == "ar" ? "فشل الحذف" : "Deletion Failed" }}
            </p>
            <v-table class="clean-sneat-table mb-4 border rounded-lg">
              <thead>
                <tr>
                  <th>IDX</th>
                  <th>REASON</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, key) in alert_del.invalid_ids" :key="key">
                  <td>{{ key }}</td>
                  <td class="text-error text-caption">{{ value }}</td>
                </tr>
              </tbody>
            </v-table>
          </template>

          <!-- Related Dependencies -->
          <template v-if="alert_del?.related_dependencies?.length > 0">
            <p class="text-overline font-weight-black text-warning mb-2">
              {{ $i18n.locale == "ar" ? "بيانات مرتبطة" : "Linked Data" }}
            </p>
            <v-table class="clean-sneat-table border rounded-lg">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>DEPENDENCY</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, key) in alert_del?.related_dependencies" :key="key">
                  <td>{{ item.id }}</td>
                  <td>{{ item.name }}</td>
                </tr>
              </tbody>
            </v-table>
          </template>
        </div>
      </v-card-text>

      <v-divider class="opacity-05" />

      <v-card-actions class="px-6 py-4 justify-end">
        <v-btn
          color="primary"
          variant="flat"
          class="px-10 font-weight-bold rounded-lg"
          @click="success_del = false"
          height="40"
        >
          {{ $i18n.locale == "ar" ? "حسناً" : "Okay" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "confirm-deletion",
  props: {
    modelValue: {
      type: Boolean,
      default: null,
    },
    url: {
      type: [String, Function],
    },

    customUrl: {
      type: String,
    },

    deleteItem: {
      type: [Number, Array],
    },
    getData: {
      type: Function,
    },
    items: [Array, Object],
    selectItems: {
      type: Array,
      default: [],
    },
    delRefresh: {
      type: Boolean,
      default: false,
    },
    itemValue: {
      type: String,
      default() {
        return "id";
      },
    },
    returnObject: {
      type: Boolean,
      default() {
        return false;
      },
    },
  },
  data() {
    return {
      localValue: false,
      del_loading: false,
      protected_records: false,
      success_del: false,

      message_protected_records: [],

      refreshData: false,

      alert_del: {},
    };
  },

  methods: {
    fixedItemDelete() {
      if (typeof this.deleteItem === "object") {
        if (this.returnObject) {
          return this.deleteItem.map((e) => e[this.itemValue]);
        } else {
          return [...this.deleteItem];
        }
      } else return [this.deleteItem];
    },
    async deleteData(force_delete) {
      const extera_url = force_delete ? "force-delete" : "bulk_delete";
      let url = this.customUrl ?? this.url + extera_url;

      try {
        this.del_loading = true;
        var data = this.fixedItemDelete();

        if (typeof this.customUrl == "string" || typeof this.url == "string") {
          await this.$axios
            .delete(url + "/", {
              data: data,
            })
            .then((response) => {
              this.success_del = true;
              const data = response?.data?.data;
              if (data)
                this.alert_del = {
                  message: data?.message,
                  deleted_objects: data?.deleted_objects,
                  related_dependencies: data?.related_dependencies,
                  invalid_ids: data?.invalid_ids,
                };
              else {
                this.alert_del = {
                  message: "تم حذف  العناصر بنجاح",
                };
              }

              if (this.items) this.deletFromItems(data?.deleted_objects);
              if (this.delRefresh) this.getData();

              this.message_protected_records = [];
              this.protected_records = false;
            })
            .catch((error) => {
              if (error.status === 409) {
                this.protected_records = true;

                const message = error.response.data.data;

                this.message_protected_records = message;

                if (this.items) {
                  if (message?.deleted_objects.length > 0)
                    this.deletFromItems(message.deleted_objects);
                } else {
                  this.getData();
                }

                // state.protected_records = false;
                // state.message_protected_records = [];
              }
            });
        } else if (typeof this.url === "function") {
          await this.url(data);
        }
      } finally {
        this.del_loading = false;
        this.value = false;
      }
    },
    deletFromItems(deleteItem) {
      let items =
        typeof this.items === "object" && "results" in this.items
          ? this.items.results
          : this.items;
      let pagination =
        typeof this.items === "object" && "pagination" in this.items
          ? this.items.pagination
          : undefined;
      if (typeof deleteItem === "object") {
        deleteItem.map((item) => {
          let element = typeof item === "object" ? item[this.itemValue] : item;
          const indexItem = items.findIndex((el) => el[this.itemValue] == element);
          if (indexItem >= 0) items.splice(indexItem, 1);
          if (this.returnObject) {
            const indexSelectItems = this.selectItems.findIndex(
              (el) => el[this.itemValue] == element
            );

            this.selectItems.splice(indexSelectItems, 1);
          } else {
            const indexSelectItems = this.selectItems.findIndex((el) => el == element);

            this.selectItems.splice(indexSelectItems, 1);
          }
        });
      } else {
        const index = items.findIndex((item) => item[this.itemValue] === deleteItem);
        items.splice(index, 1);
      }

      if (pagination) {
        if ("count" in pagination) pagination.count -= 1;

        let totalPages = Math.ceil(pagination.count / pagination.page_size);

        if (pagination.current_page > totalPages) {
          pagination.current_page = totalPages;
          this.getData();
        }
        if (pagination.current_page < 1) {
          pagination.current_page = 1;
        }

        if (pagination.num_pages > totalPages) {
          pagination.num_pages = totalPages;
        }
      }
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue !== null ? this.modelValue : this.localValue;
      },
      set(value) {
        if (this.modelValue !== null) {
          this.$emit("update:modelValue", value);
        } else {
          this.localValue = value;
        }
      },
    },
  },
};
</script>

<style scoped>
.message-card {
  border-radius: 8px !important;
}

.header-section {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.05);
}

.line-height-1-2 {
  line-height: 1.2 !important;
}

/* Sneat Style Clean Table */
.clean-sneat-table {
  background: transparent !important;
}

.clean-sneat-table :deep(thead) {
  background-color: rgba(var(--v-theme-on-surface), 0.02);
}

.clean-sneat-table :deep(th) {
  height: 40px !important;
  color: rgba(var(--v-theme-on-surface), 0.6) !important;
  text-transform: uppercase;
  font-size: 0.75rem !important;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.05) !important;
}

.clean-sneat-table :deep(td) {
  height: 44px !important;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.03) !important;
}

.clean-sneat-table :deep(tr:last-child td) {
  border-bottom: none !important;
}

.opacity-05 {
  opacity: 0.05;
}

/* Animations */
.dialog-transition-enter-active,
.dialog-transition-leave-active {
  transition: transform 0.3s ease-out, opacity 0.3s;
}

.dialog-transition-enter-from,
.dialog-transition-leave-to {
  transform: scale(0.9) translateY(20px);
  opacity: 0;
}
</style>
