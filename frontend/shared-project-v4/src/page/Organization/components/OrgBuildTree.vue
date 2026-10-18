<template>
  <VTreeview
    v-if="items.length > 0"
    v-model:actived="active"
    v-model:opened="open"
    :items="items.length > 0 ? items : []"
    item-title="name_ar"
    item-value="id"
    color="primary"
    activatable
    density="comfortable"
    indent-lines
    expand-icon="mdi-chevron-down"
    collapse-icon="mdi-chevron-left"
    class="premium-treeview bg-surface rounded-lg"
    :search="search"
  >
    <template #no-data>
      <EmptyState
        :description="$i18n.locale === 'ar' ? 'لا يوجد بيانات' : 'No data available'"
      />
    </template>
    <template v-slot:prepend="{ item }">
      <VIcon
        :icon="getIcon(item.company_level)"
        color="primary"
        class="me-2"
        size="large"
      />
    </template>
    <template v-slot:title="{ item }">
      <VHover>
        <template v-slot:default="{ isHovering, props }">
          <div
            v-bind="props"
            class="d-flex align-center justify-space-between w-100 py-1"
          >
            <!-- Node Title -->
            <div class="d-flex align-center text-truncate pe-4">
              <span
                class="text-truncate overflow-auto"
                :class="{
                  'font-weight-bold text-primary text-subtitle-1': item.isHeader,
                  'font-weight-bold text-high-emphasis text-body-1':
                    !item.isHeader && item.company_level === 30,
                  'font-weight-medium text-high-emphasis text-body-1':
                    !item.isHeader && item.company_level !== 30,
                }"
                style="letter-spacing: 0.2px"
                >{{ item.name_ar }}</span
              >

              <div
                class="tree-actions-container d-flex align-center gap-1 ms-1"
                :class="{ 'actions-visible': isHovering }"
                v-if="!item.isHeader && !$vuetify.display.mobile"
              >
                <custom-btn
                  v-if="
                    $perm('add', 'organizations') &&
                    item.company_level != 60 &&
                    isPlatFormSys
                  "
                  icon="plus"
                  isIcon
                  size="small"
                  color="success"
                  variant="tonal"
                  class="rounded-pill premium-action-btn ms-1"
                  :label="$t('add')"
                  @click.stop="$emit('action-click', 'newChild', item)"
                />

                <custom-btn
                  v-if="$perm('edit', 'organizations') && isPlatFormSys"
                  icon="square-edit-outline"
                  isIcon
                  size="small"
                  color="warning"
                  variant="tonal"
                  class="rounded-pill premium-action-btn ms-1"
                  :label="$t('update')"
                  @click.stop="$emit('action-click', 'edit', item)"
                />

                <custom-btn
                  v-if="$perm('delete', 'organizations') && isPlatFormSys"
                  icon="trash-can-outline"
                  isIcon
                  size="small"
                  color="error"
                  variant="tonal"
                  class="rounded-pill premium-action-btn ms-1"
                  :label="$t('delelte')"
                  @click.stop="(delDialog = true), (deleteId = item.id)"
                />

                <v-divider vertical />
                <custom-btn
                  icon="information-outline"
                  is-icon
                  size="small"
                  color="info"
                  variant="tonal"
                  class="rounded-pill ms-3 premium-info-btn"
                  @click.stop="$emit('action-click', 'details', item)"
                  :label="$t('details')"
                />
              </div>
              <v-menu
                location="bottom end"
                v-if="$vuetify.display.mobile"
                :close-on-content-click="false"
              >
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon
                    size="small"
                    density="compact"
                    variant="text"
                  >
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>

                <v-list class="cursor-pointer" density="compact">
                  <v-list-item
                    v-if="!item.isHeader"
                    append-icon="mdi-information-outline"
                    @click.stop="$emit('action-click', 'details', item)"
                  >
                    {{ $t("details") }}
                  </v-list-item>
                  <v-list-item
                    append-icon="mdi-plus"
                    v-if="
                      $perm('add', 'organizations') &&
                      item.company_level != 60 &&
                      isPlatFormSys
                    "
                    @click.stop="$emit('action-click', 'newChild', item)"
                  >
                    {{ $t("add") }}
                  </v-list-item>

                  <v-list-item
                    append-icon="mdi-square-edit-outline"
                    v-if="$perm('edit', 'organizations') && isPlatFormSys"
                    @click.stop="$emit('action-click', 'edit', item)"
                  >
                    {{ $t("update") }}
                  </v-list-item>

                  <v-list-item
                    v-if="$perm('delete', 'organizations') && isPlatFormSys"
                    append-icon="mdi-trash-can-outline"
                    @click.stop="(delDialog = true), (deleteId = item.id)"
                  >
                    {{ $t("delelte") }}
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </div>
        </template>
      </VHover>
    </template>
  </VTreeview>

  <confirm-deletion
    v-model="delDialog"
    url="common/branch/"
    :delRefresh="true"
    :delete-item="deleteId"
    :getData="getData"
    :returnObject="true"
    :items="[]"
  />
</template>
<script setup>
import { ref } from "vue";

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  search: {
    type: String,
    default: null,
  },
  isPlatFormSys: {
    type: Boolean,
    default: false,
  },
  getData: Function,
});

const delDialog = ref(false);
const deleteId = ref(null);
const active = ref([]);
const open = ref([]);
const getIcon = (level) => {
  if (level === undefined) return "mdi-folder-table-outline"; // Icon for Header nodes
  switch (level) {
    case 10:
      return "mdi-shield-account";
    case 20:
      return "mdi-domain";
    case 30:
      return "mdi-city-variant";
    case 40:
      return "mdi-office-building-marker";
    case 50:
      return "mdi-school";
    case 60:
      return "mdi-source-branch";
    default:
      return "mdi-folder-outline"; // Fallback icon
  }
};
</script>

<style scoped>
/* Premium Treeview UI/UX - Formal & Clean */
.premium-treeview {
  padding: 12px 16px;
}

/* Row Layout */
.premium-treeview :deep(.v-list-item) {
  min-height: 44px !important;
  border-radius: 4px !important;
  margin-bottom: 2px;
}

/* Professional Hover State */
.premium-treeview :deep(.v-list-item:hover) {
  background-color: rgba(var(--v-theme-on-surface), 0.04) !important;
}

/* Active Selected State */
.premium-treeview :deep(.v-list-item--active) {
  background-color: rgba(var(--v-theme-primary), 0.08) !important;
}

/* Formal Indent Lines */
.premium-treeview :deep(.v-treeview-group__children) {
  border-inline-start: 1px solid rgba(var(--v-theme-on-surface), 0.15) !important;
  margin-inline-start: 18px;
  padding-inline-start: 12px;
}

/* Expand/Collapse Icons */
.premium-treeview :deep(.v-list-group__header .v-list-item__append .v-icon),
.premium-treeview :deep(.v-list-group__header .v-list-item__prepend .v-icon) {
  color: rgba(var(--v-theme-on-surface), 0.5);
  font-size: 1.4rem;
}

.premium-treeview :deep(.v-list-group__header:hover .v-list-item__append .v-icon),
.premium-treeview :deep(.v-list-group__header:hover .v-list-item__prepend .v-icon) {
  color: rgba(var(--v-theme-on-surface), 0.75);
}

/* Action Buttons Animation */
.tree-actions-container {
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
  pointer-events: none;
}

.tree-actions-container.actions-visible {
  opacity: 1;
  pointer-events: auto;
}

.premium-action-btn {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.premium-action-btn:hover {
  transform: scale(1.1);
}

.premium-separator {
  width: 2px;
  height: 22px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(var(--v-theme-on-surface), 0.2),
    transparent
  );
  border-radius: 2px;
  margin: 0 6px;
}

.premium-info-btn {
  box-shadow: 0 2px 6px rgba(var(--v-theme-info), 0.2) !important;
}
</style>
