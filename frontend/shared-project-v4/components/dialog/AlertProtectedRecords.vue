<template>
  <v-dialog
    v-model="value"
    transition="dialog-transition"
    dir="rtl"
    scrollable
    max-width="600"
  >
    <v-card class="message-card border-thin overflow-hidden" elevation="1">
      <!-- Header Section (Calmer Warning Style) -->
      <div 
        class="header-section d-flex align-start px-6 pt-6 pb-4 position-relative"
        style="background-color: rgba(var(--v-theme-warning), 0.08)"
      >
        <v-avatar
          color="warning"
          variant="tonal"
          size="46"
          class="me-4 flex-shrink-0 rounded-lg"
        >
          <v-icon size="26">mdi-alert-outline</v-icon>
        </v-avatar>
        
        <div class="d-flex flex-column flex-grow-1 pt-1">
          <v-card-title class="pa-0 text-subtitle-1 font-weight-bold line-height-1-2" color="warning">
            {{ $t("warning") }}
          </v-card-title>
          <div class="text-caption font-weight-regular mt-1" style="color: rgba(var(--v-theme-on-surface), 0.6)">
            {{ $t(messages) }}
          </div>
        </div>
      </div>

      <v-card-text class="px-6 py-6 custom-scrollbar" style="max-height: 60vh; overflow-y: auto;">
        
        <!-- Unified Calm Information Note -->
        <v-alert
          color="warning"
          variant="tonal"
          border="start"
          border-color="warning"
          class="mb-8 rounded-lg"
          density="compact"
        >
          <template v-slot:prepend>
            <v-icon size="22" class="me-3 mt-1">mdi-information-outline</v-icon>
          </template>
          <div class="text-body-2 font-weight-medium" style="color: rgb(var(--v-theme-warning)); line-height: 1.6;">
            <template v-if="$i18n.locale == 'ar'">
              لإتمام العملية وتخطي هذا التحذير، يمكنك استخدام خيار <strong class="font-weight-bold mx-1" style="color: rgb(var(--v-theme-on-surface))">"حذف إجباري"</strong> لحذف العنصر بشكل نهائي مع كافة ارتباطاته.
            </template>
            <template v-else>
              To bypass this warning, use <strong class="font-weight-bold mx-1" style="color: rgb(var(--v-theme-on-surface))">"Force Delete"</strong> to permanently remove the item and all linked data.
            </template>
          </div>
        </v-alert>

        <!-- Deleted Objects Section -->
        <template v-if="data_message.deleted_objects?.length > 0">
          <div class="d-flex align-center mb-3">
            <v-avatar size="28" color="grey-darken-3" variant="tonal" class="me-3 rounded-md">
              <v-icon size="16">mdi-check-all</v-icon>
            </v-avatar>
            <span class="text-body-2 font-weight-bold" style="color: rgba(var(--v-theme-on-surface), 0.7)">
              {{ $i18n.locale == 'ar' ? 'عناصر قابلة للحذف' : 'Removable Elements' }}
            </span>
          </div>
          
          <v-table class="clean-sneat-table mb-8 border rounded-lg" density="comfortable">
            <thead>
              <tr>
                <th class="text-start" style="width: 80px;"># ID</th>
                <th class="text-start">{{ $i18n.locale == 'ar' ? 'العنصر' : 'Element' }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in data_message?.deleted_objects" :key="index">
                <td class="text-caption font-weight-medium" style="color: rgba(var(--v-theme-on-surface), 0.5)">#{{ item.id }}</td>
                <td class="text-body-2 font-weight-bold" style="color: rgba(var(--v-theme-on-surface), 0.8)">{{ item.name }}</td>
              </tr>
            </tbody>
          </v-table>
        </template>

        <div class="d-flex align-center mb-4 mt-2">
          <v-avatar size="28" color="warning" variant="tonal" class="me-3 rounded-md">
            <v-icon size="16">mdi-link-variant-remove</v-icon>
          </v-avatar>
          <span class="text-body-2 font-weight-bold" color="warning">
            {{ $i18n.locale == 'ar' ? 'عناصر مرتبطة تمنع الحذف' : 'Linked Elements (Preventing Deletion)' }}
          </span>
        </div>

        <template v-if="data_message.related_dependencies?.length > 0">
          <div 
            v-for="(item, index) in data_message.related_dependencies" 
            :key="index"
            class="border rounded-lg mb-4 overflow-hidden bg-surface"
          >
            <!-- Module Title -->
            <div class="d-flex align-center px-4 py-3 border-b" style="background-color: rgba(var(--v-theme-on-surface), 0.04)">
              <v-icon color="grey-darken-3" size="18" class="me-3">mdi-database-outline</v-icon>
              <span class="text-subtitle-2 font-weight-bold" style="color: rgba(var(--v-theme-on-surface), 0.7)">
                {{ item.object_str }}
              </span>
              <v-spacer></v-spacer>
              <v-chip size="small" color="warning" variant="tonal" class="font-weight-medium px-3 text-caption">
                {{ item.count }} {{ $i18n.locale == 'ar' ? 'مرتبط' : 'Linked' }}
              </v-chip>
            </div>

            <!-- Details Tables -->
            <div class="pa-4 pb-2">
              <div 
                v-for="(sub_item, sub_index) in item?.details" 
                :key="sub_index"
                class="mb-4"
              >
                <div class="d-flex align-center mb-3">
                  <v-avatar size="24" color="grey-darken-1" variant="tonal" class="me-3 rounded-md">
                    <v-icon size="14">mdi-application-outline</v-icon>
                  </v-avatar>
                  <span class="text-subtitle-2 font-weight-bold" style="color: rgba(var(--v-theme-on-surface), 0.8)">
                    {{ sub_item.model }}
                  </span>
                </div>
                
                <v-table class="clean-sneat-table bg-surface" density="compact">
                  <thead>
                    <tr>
                      <th class="text-start" style="width: 80px;"># ID</th>
                      <th class="text-start">{{ $i18n.locale == 'ar' ? 'العنصر' : 'Element' }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(value, key) in sub_item.related_objects" :key="key">
                      <td class="text-caption font-weight-medium" style="color: rgba(var(--v-theme-on-surface), 0.5)">#{{ value.id }}</td>
                      <td class="text-body-2 font-weight-bold" style="color: rgba(var(--v-theme-on-surface), 0.8)">{{ value.object_str }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
            </div>
          </div>
        </template>
        
        <div v-else class="text-center rounded-lg py-8 border-dashed" style="background-color: rgba(var(--v-theme-on-surface), 0.04); border-width: 2px;">
          <v-icon color="secondary" size="36" class="mb-3 opacity-80">mdi-shield-check-outline</v-icon>
          <div class="text-body-2 font-weight-medium" style="color: rgba(var(--v-theme-on-surface), 0.7)">
            {{ $i18n.locale == 'ar' ? 'لا توجد بيانات مرتبطة تمنع الحذف' : 'No related dependencies preventing deletion' }}
          </div>
        </div>

      </v-card-text>

      <v-divider class="opacity-05" />

      <v-card-actions class="px-6 py-4 justify-end gap-3 bg-surface">
        <v-btn
          variant="text"
          color="grey-darken-1"
          class="font-weight-bold px-6 rounded-lg"
          @click="(value = false), (state.message_protected_records = []), message_protected_records=[]"
        >
          {{ $t("cancel") }}
        </v-btn>
        
        <slot name="actions"/>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { state } from "@/../src/store/state";
</script>
<script>
export default {
  props: {
    data_message: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
    messages: {
      type: String,
      default: "cannot-delete",
    },
    message_protected_records:{
      type:Array,
      default:[]
    },
  },
  data() {
    return {
      protected_records: false,
    };
  },
   
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
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
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.05);
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

.clean-sneat-table :deep(tbody tr:hover) {
  background-color: rgba(var(--v-theme-on-surface), 0.03);
  transition: background-color 0.2s ease;
}

.opacity-05 {
  opacity: 0.05;
}

.gap-3 {
  gap: 12px;
}

/* Premium Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.3);
}
</style>