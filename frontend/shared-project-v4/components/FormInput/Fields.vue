<template>
  <!-- Error State: Retry Button (original behavior preserved) -->

  <custom-btn v-if="is_error" type="refresh" is-icon @click="fetchFields" class="ma-2" />

  <!-- Loading State: Professional Skeleton -->
  <div class="fields-skeleton-wrapper" v-if="progress_circular">
    <div class="skeleton-row" v-for="row in 2" :key="row">
      <div class="skeleton-bar skeleton-bar--label"></div>
      <div class="skeleton-bar skeleton-bar--input"></div>
    </div>
  </div>

  <!-- Fields Loop (v-else tied to progress_circular — original logic) -->
  <template v-for="(field, index) in filter_fildes" :key="index" v-else>
    <slot :field="field">
      <!-- Grouped Fields — Ultra-Premium Group Card -->
      <template v-if="'groups' in field">
        <VCol cols="12" class="pb-2">
          <div class="fields-group-card">
            <!-- Animated Header -->
            <div class="fields-group-header px-4 py-2 d-flex align-center">
              <div class="fields-group-indicator me-3"></div>
              <span
                class="text-subtitle-2 font-weight-bold text-primary fields-group-title"
              >
                {{ $t(field.groups) }}
              </span>
            </div>
            <!-- Group Content -->
            <div class="fields-group-body">
              <VRow>
                <template
                  v-for="(field_group, index_group) in field.fields"
                  :key="index_group"
                >
                  <field
                    v-if="'name' in field_group && field_group.name != null"
                    v-model="data[field_group.name]"
                    :field="field_group"
                    :attr="attr[field_group.name]"
                    @keydown="
                      handleFieldKeydown(field_group.name, data[field_group.name])
                    "
                    @update="handleFieldUpdate(field_group.name, data[field_group.name])"
                  />
                </template>
                <slot :name="field.groups"></slot>
              </VRow>
            </div>
          </div>
        </VCol>
      </template>

      <!-- Standalone Fields -->
      <template v-else>
        <add-to-level
          v-if="field.name_list === 'add_to_level'"
          :show_in_edit="false"
          :data="data"
        />
        <add-to-level-no-check
          v-else-if="field.name_list === 'add_to_level_no_check'"
          :show_in_edit="false"
          :data="data"
        />
        <template v-else>
          <field
            v-if="'name' in field && field.name != null"
            v-model="data[field.name]"
            :field="field"
            :attr="attr[field.name]"
            @keydown="(event) => handleFieldKeydown(event, field.name, data[field.name])"
            :autofocus="!field.name_list && index === 0 ? true : false"
            @selectObject="(val, object) => handleSelectObject(field.name, val, object)"
            @update="(value) => handleFieldUpdate(field.name, value)"
            @item-show="(value) => itemShow(field.name, value)"
          />
          <!-- @update:model-value="attr[field.name][`update:modelValue`]?.(value)" -->
        </template>
      </template>
    </slot>
  </template>

  <!-- Import Excel Dialog -->
  <custom-dialog v-model="dialog_import" title="Import from Excel" height="auto">
    <template v-slot>
      <import-excel :fields="filter_fildes" />
    </template>
  </custom-dialog>
</template>

<script>
import ImportExcel from "../other/ImportExcel/ImportExcel.vue";
import Field from "./Field.vue";
import setting from "@/../settings";

export default {
  components: { Field, ImportExcel },
  props: {
    data: { type: Object, required: true },
    attr: { type: Object, default: () => ({}) },
    url: { type: String },
    fields: { type: Array },
    group: {
      type: [String, Boolean],
      default: false,
    },
    focus: {
      type: Boolean,
      default: false,
    },
    importExcel: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      fields_list: [],
      progress_circular: false,
      is_error: false,

      dialog_import: false,
    };
  },
  created() {
    if (this.url) this.fetchFields();
  },
  methods: {
    handleSelectObject(fieldName, val, object) {
      this.attr[fieldName]?.selectObject?.(val, object);
    },
    itemShow(fieldName, value) {
      this.attr[fieldName]?.itemShow?.(value);
    },
    async fetchFields() {
      this.is_error = false;

      this.progress_circular = true;
      await this.$axios(`${setting.url_field}${this.url}/`)
        .then((response) => {
          this.fields_list = response?.data?.data || response.data;
        })
        .catch((error) => {
          this.is_error = true;

          console.error("Error fetching fields:", error);
        });

      this.progress_circular = false;
    },
    handleFieldUpdate(fieldName, value) {
      this.attr[fieldName]?.update?.(value);
    },

    handleFieldKeydown(event, fieldName, value) {
      if (this.attr[fieldName] && "keydown" in this.attr[fieldName])
        this.attr[fieldName]?.keydown?.(event, value);
    },
    parseGroup(groupStr) {
      const tabMatch = groupStr.match(/t\('(.+?)'\)/);
      const grupMatch = groupStr.match(/g\('(.+?)'\)/);
      return {
        tab: tabMatch ? tabMatch[1] : null,
        subgrup: grupMatch ? grupMatch[1] : null,
      };
    },

    // formatData(fields) {
    //   const results = [];
    //   data.forEach((item) => {
    //     if(item.group)
    //     {
    //       const groupInfo = item.group.match(/t\('.*?)'\)g\('(.*?)'\)/);
    //     const tabName = groupInfo
    //       ? groupInfo[1]
    //       : item.group.match(/t\('(.*?)'\)/)[1];
    //     const groupName = groupInfo ? groupInfo[2] : null;

    //     let tab = results.find((t) => t.tab === tabName);
    //     if (!tab) {
    //       tab = { tab: tabName, group: [] };
    //       results.push(tab);
    //     }
    //     if (groupName) {
    //       let group = tab.group.find((g) => g[groupName]);
    //       if (!group) {
    //         group = { [groupName]: [] };
    //         tab.group.push(group);
    //       }
    //       group[groupName].push(item);
    //     } else {
    //       if (!tab.fields) tab.fields = [];

    //       tab.fields.push(item);
    //     }}
    //   });

    //   return results;
    // },
  },
  computed: {
    filter_fildes() {
      // return this.url ? this.fields_list : this.fields;

      const field_list = this.url ? this.fields_list : this.fields;

      if (this.group === true) {
        const groupingData = [];
        const groups = {};
        field_list.forEach((item) => {
          if (item.group) {
            if (!groups[item.group]) {
              groups[item.group] = {
                groups: item.group,
                fields: [],
              };
              groupingData.push(groups[item.group]);
            }
            groups[item.group].fields.push({
              ...item,
            });
          } else {
            groupingData.push({
              ...item,
            });
          }
        });
        return groupingData;
      } else if (typeof this.group === "string") {
        return this.fields_list.filter((e) => e.group === this.group);
      } else {
        return field_list;
      }
    },

    autofocus() {
      return this.focus;
    },
  },
};
</script>

<style scoped>
/* ═══════════════════════════════════════════════════
   ULTRA-PREMIUM GROUP CARD
═══════════════════════════════════════════════════ */
.fields-group-card {
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(
    180deg,
    rgb(var(--v-theme-surface)) 0%,
    rgba(var(--v-theme-surface), 0.98) 100%
  );
  box-shadow: 0 4px 18px -4px rgba(0, 0, 0, 0.02),
    0 2px 6px -2px rgba(var(--v-theme-primary), 0.03);
  margin-bottom: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fields-group-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.25) !important;
  box-shadow: 0 4px 20px -4px rgba(var(--v-theme-primary), 0.06);
}

/* Header with subtle gradient */
.fields-group-header {
  padding: 14px 20px !important;
  background-color: rgba(var(--v-theme-primary), 0.03);
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.05);
  position: relative;
  overflow: hidden;
}

/* Glowing Indicator Bar */
.fields-group-indicator {
  position: relative;
  width: 4px;
  height: 18px;
  border-radius: 8px;
  background: rgb(var(--v-theme-primary));
  margin-inline-end: 12px;
  flex-shrink: 0;
}

/* Group Title Typography */
.fields-group-title {
  font-family: "Tajawal", "Inter", sans-serif !important;
  font-size: 0.92rem !important;
  font-weight: 700 !important;
  color: rgb(var(--v-theme-primary)) !important;
  letter-spacing: 0.4px;
}

/* Group Body Spacing */
.fields-group-body {
  padding: 20px !important;
}

/* ═══════════════════════════════════════════════════
   SKELETON LOADING STATE
═══════════════════════════════════════════════════ */
.fields-skeleton-wrapper {
  padding: 8px 4px;
  width: 100%;
}

.skeleton-row {
  margin-bottom: 20px;
}

.skeleton-bar {
  background: linear-gradient(
    90deg,
    rgba(var(--v-theme-on-surface), 0.06) 25%,
    rgba(var(--v-theme-on-surface), 0.12) 50%,
    rgba(var(--v-theme-on-surface), 0.06) 75%
  );
  background-size: 200% 100%;
  border-radius: 6px;
  animation: skeleton-shimmer 1.6s infinite ease-in-out;
}

.skeleton-bar--label {
  height: 12px;
  width: 30%;
  margin-bottom: 8px;
}

.skeleton-bar--input {
  height: 44px;
  width: 100%;
  border-radius: 8px;
}

@keyframes skeleton-shimmer {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -200% 0;
  }
}
</style>
