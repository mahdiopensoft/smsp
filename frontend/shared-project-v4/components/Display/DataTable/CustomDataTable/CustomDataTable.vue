<template>
  <!-- added by samer -->

  <VCard
    elevation="0"
    class="p-0 ma-0 border-sm mb-10"
    v-show="!delete_log_dialog && !log_dialog"
    :style="isEmptyReprort ? 'overflow:hidden !important' : 'overflow:unset !important'"
  >
    <slot name="note"></slot>

    <VCol v-if="!is_print" class="pa-0">
      <v-card class="hide-item" elevation="0" rounded="0">
        <div
          class="d-flex align-center px-4 py-3 custom-data-table-toolbar bg-surface border-b gap-2"
        >
          <template v-if="showTop">
            <!-- View Tools Group (Start Side) -->
            <div
              :class="[
                'd-flex align-center gap-1 flex-wrap flex-sm-nowrap flex-md-grow-0',
                search ? 'flex-grow-1' : 'flex-grow-0',
              ]"
            >
              <!-- Column Visibility (The Eye) -->
              <v-menu
                v-if="select_header"
                :close-on-content-click="false"
                transition="slide-y-transition"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="tonal"
                    color="primary"
                    size="small"
                    class="rounded-lg flex-shrink-0"
                    style="height: 38px; min-width: 38px"
                  >
                    <v-icon icon="mdi-eye-outline" size="20" />
                    <VTooltip activator="parent" location="top">{{
                      $i18n.locale == "ar" ? "إظهار/إخفاء الأعمدة" : "Toggle Columns"
                    }}</VTooltip>
                  </v-btn>
                </template>
                <v-card
                  elevation="24"
                  rounded="lg"
                  class="premium-menu-card border-thin mt-2 overflow-hidden"
                  style="min-width: 280px"
                >
                  <div
                    class="pa-4 border-b d-flex align-center"
                    style="background-color: rgba(var(--v-theme-primary), 0.08)"
                  >
                    <v-icon color="primary" class="me-3" size="22"
                      >mdi-view-column-outline</v-icon
                    >
                    <div>
                      <div
                        class="text-subtitle-2 font-weight-bold"
                        style="color: rgb(var(--v-theme-on-surface))"
                      >
                        {{ $i18n.locale == "ar" ? "إعدادات الأعمدة" : "Column Settings" }}
                      </div>
                      <div
                        class="text-caption"
                        style="color: rgba(var(--v-theme-on-surface), 0.6)"
                      >
                        {{
                          $i18n.locale == "ar"
                            ? "اختر الأعمدة التي تود عرضها"
                            : "Select columns to display"
                        }}
                      </div>
                    </div>
                  </div>

                  <v-card-text class="pa-2">
                    <v-list density="compact" class="bg-transparent pa-0">
                      <v-list-item
                        v-for="h in copy_headers"
                        :key="h.key"
                        class="premium-list-item"
                        :active="h.show"
                        active-color="primary"
                        :disabled="value.length > 0 && h.key == 'actions'"
                      >
                        <template v-slot:prepend>
                          <v-checkbox-btn
                            v-model="h.show"
                            color="primary"
                            density="compact"
                          ></v-checkbox-btn>
                        </template>
                        <v-list-item-title class="text-body-2 font-weight-medium">{{
                          h.title
                        }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-menu>

              <!-- Search -->
              <v-text-field
                v-if="search"
                v-model="params.search"
                prepend-inner-icon="mdi-magnify"
                :placeholder="$i18n.locale === 'ar' ? 'ابحث...' : 'Search...'"
                density="compact"
                variant="solo-filled"
                flat
                hide-details
                clearable
                class="modern-search-field flex-grow-1 flex-shrink-1"
                style="max-width: 100%; min-width: 140px"
                @input="!params.search ? ('pagination' in items ? fetchData() : '') : ''"
                @keyup.enter="fetchData()"
                type="search"
              />

              <!-- Filters -->
              <v-btn
                v-if="hasFilter"
                @click="filter_dialog = true"
                variant="tonal"
                :color="activeFilters ? 'primary' : 'secondary'"
                size="small"
                class="rounded-lg"
                style="height: 38px; min-width: 38px"
              >
                <VIcon size="20">{{
                  activeFilters ? "mdi-filter-check" : "mdi-filter-variant"
                }}</VIcon>
                <VTooltip activator="parent" location="top">
                  {{ $i18n.locale == "ar" ? "الفلترة المتقدمة" : "Advanced Filter" }}
                </VTooltip>
              </v-btn>

              <!-- Clear Filters -->
              <v-btn
                v-if="activeFilters"
                @click="resetFilters"
                variant="tonal"
                color="error"
                size="small"
                class="rounded-lg"
                style="height: 38px; min-width: 38px"
              >
                <VIcon size="20">mdi-filter-off-outline</VIcon>
                <VTooltip activator="parent" location="top">{{
                  $t("clear_filters") || "إلغاء الفلترة"
                }}</VTooltip>
              </v-btn>
            </div>

            <!-- Data Operations Group (Middle) -->
            <div
              :class="[
                'd-flex align-center gap-1 hide-item flex-wrap flex-md-nowrap flex-grow-1 flex-lg-grow-0',
                search ? 'ps-sm-2 border-sm-s' : '',
              ]"
            >
              <!-- Refresh -->
              <v-btn
                v-if="refresh"
                @click="fetchData"
                variant="tonal"
                color="secondary"
                size="small"
                class="rounded-lg flex-shrink-0"
                style="height: 38px; min-width: 38px"
              >
                <VIcon size="20">mdi-refresh</VIcon>
                <VTooltip activator="parent" location="top">{{
                  $t("refresh") || "تحديث"
                }}</VTooltip>
              </v-btn>

              <!-- Import Excel -->
              <v-btn
                v-if="imoprtExcel && hasImportPermission"
                @click="dialog_import_to_excel = true"
                variant="tonal"
                color="success"
                size="small"
                class="rounded-lg"
                style="height: 38px; min-width: 38px"
              >
                <VIcon size="20">mdi-file-import-outline</VIcon>
                <VTooltip activator="parent" location="top">{{
                  $i18n.locale == "ar" ? "استيراد إكسل" : "Import Excel"
                }}</VTooltip>
              </v-btn>

              <!-- Operations (Cog Menu) -->

              <TableGeneralActions
                v-if="showOperations"
                :hasImportExcel="imoprtExcel"
                :hasRestore="hasRestorePermission"
                :hasLog="hasLogPermission"
                :hasPrint="hasPrintPermission"
                :hasExportExcel="ExportToExcel"
                :hasDelete="hasDeletePermission && canSelectDelete"
                `1
                :selectedItems="value"
                :items="Array.isArray(items) ? items : items.results || []"
                :url="delItem"
                :headers="headers"
                :fields="fields"
                :label="label"
                :getData="fetchData"
                :deleteItem="deleteItem"
                :multipleMethodes="multipleMethodes"
                :addToActionsList="addToActionsList"
                @typePrint="handleTypePrint"
                @exportExcel="ExportExcel"
              />
            </div>

            <v-spacer></v-spacer>

            <!-- Primary Actions Group (End Side) -->
            <div
              class="d-flex align-center gap-2 flex-wrap justify-end flex-grow-1 flex-md-grow-0"
            >
              <!-- Extra Action Slot -->
              <slot name="header-actions"></slot>

              <!-- Create Button -->
              <custom-btn v-if="create && hasAddPermission" type="add" :click="create" />
              <!-- <v-btn
                v-if="create && hasAddPermission"
                @click="create"
                color="primary"
                size="small"
                class="rounded-lg font-weight-bold px-2 px-sm-4 shadow-sm flex-shrink-0"
                style="height: 38px; min-width: 38px"
              >
                <v-icon icon="mdi-plus" class="me-sm-1" />
                <span class="d-none d-sm-inline">{{
                  $i18n.locale == "ar" ? "إضافة جديد" : "Create New"
                }}</span>
                <v-tooltip activator="parent" location="top" v-if="$vuetify.display.xs">{{
                  $i18n.locale == "ar" ? "إضافة جديد" : "Create New"
                }}</v-tooltip>
              </v-btn> -->

              <!-- Create Button Slot or Default -->
            </div>
          </template>

          <v-spacer v-if="!showTop"></v-spacer>
          <slot name="action"></slot>

          <!-- Print Actions Always Visible -->
          <div class="d-flex align-center gap-2 flex-wrap justify-end">
            <!-- Print All Button -->
            <v-btn
              v-if="canPrintReport"
              @click="printReport(undefined, false)"
              variant="outlined"
              color="primary"
              size="small"
              class="rounded-lg px-2 px-sm-4 flex-shrink-0"
              style="height: 38px; min-width: 38px"
            >
              <v-icon icon="mdi-printer-outline" class="me-sm-1" />
              <span class="d-none d-sm-inline">{{
                $i18n.locale == "ar" ? "طباعة التقرير" : "Print Report"
              }}</span>
              <v-tooltip activator="parent" location="top" v-if="$vuetify.display.xs">{{
                $i18n.locale == "ar" ? "طباعة التقرير" : "Print Report"
              }}</v-tooltip>
            </v-btn>

            <!-- Print Empty Button -->
            <v-btn
              v-if="canPrintReportEmpty"
              @click="printReport(undefined, true)"
              variant="outlined"
              color="primary"
              size="small"
              class="rounded-lg px-2 px-sm-4 flex-shrink-0"
              style="height: 38px; min-width: 38px"
            >
              <v-icon icon="mdi-printer-outline" class="me-sm-1" />
              <span class="d-none d-sm-inline">{{
                $i18n.locale == "ar" ? "طباعة فارغة" : "Print Empty"
              }}</span>
              <v-tooltip activator="parent" location="top" v-if="$vuetify.display.xs">{{
                $i18n.locale == "ar" ? "طباعة فارغة" : "Print Empty"
              }}</v-tooltip>
            </v-btn>
          </div>
        </div>
      </v-card>
    </VCol>

    <v-card ref="report" elevation="0">
      <component
        v-model="value"
        v-model:sort-by="sortBy"
        :is="pagination ? 'VDataTableServer' : 'VDataTableVirtual'"
        id="vDataTable"
        :headers="visibleHeaders"
        :items="data"
        density="compact"
        :loading="loading || customLoading"
        :item-value="itemValue"
        :class="{
          'custom-data-table': true,
          'flex-grow-1': true,
          'class-numbering-child-2': numbering && !is_print && showSelect,
          'class-numbering-child-1':
            (numbering && !is_print && !showSelect) || (numbering && is_print),
        }"
        :show-select="showSelect && !is_print"
        :return-object="returnObject"
        :search="pagination ? '' : params.search"
        :height="height"
        :fixed-header="fixedHeader"
        @update:options="fetchData"
      >
        <!--  -->
        <template #no-data>
          <NotFound v-if="!error_in_fetch" />
          <template v-else>
            {{
              $i18n.locale == "ar"
                ? "فشل التحميل - إعادة المحاولة"
                : "Fetch Failed - Try Again"
            }}
            <VIcon
              icon="mdi-refresh"
              size="20"
              class="ms-2"
              color="primary"
              @click="fetchData()"
            />
          </template>
        </template>
        <template v-slot:loading>
          <v-skeleton-loader :type="`table-row-divider@${items?.results?.length || 4}`" />
        </template>
        <template #top>
          <div>
            <slot name="top" />
          </div>
        </template>

        <template v-slot:item="{ item, index }" v-if="customTable">
          <tr
            :style="{
              transition: 'background-color 0.2s',
              backgroundColor: item.new_colors
                ? 'rgba(var(--v-theme-primary), 0.05)'
                : '',
            }"
            :class="rowClass(item)"
          >
            <td class="ms-0 px-2" v-if="showSelect && !is_print">
              <v-checkbox-btn
                v-model="value"
                :value="returnObject ? item : item[itemValue]"
                :key="item[itemValue]"
                hide-details
                color="primary"
                density="compact"
              />
            </td>

            <td v-for="val in visibleHeaders" :key="val.key">
              <slot
                name="item-slot"
                :item="item"
                :key="val.key"
                :index="index"
                v-if="!isEmptyReprort"
              >
                <span
                  v-if="val.key === 'numbering' && numbering"
                  style="width: 20px !important"
                >
                  {{ index + 1 }}
                </span>
                <span v-if="val.type == 'object'">
                  {{ val.val.reduce((acc, key) => acc && acc[key], item[val.key]) }}
                </span>
                <v-chip-group v-else-if="Array.isArray(item[val.key])" density="compact">
                  <v-chip
                    v-for="(list, index) in item[val.key]"
                    :key="index"
                    size="small"
                  >
                    {{ list[val.title_list] || list }}
                  </v-chip>
                </v-chip-group>
                <v-dialog max-width="900" v-else-if="val.type == 'img'">
                  <template v-slot:activator="{ props: activatorProps }">
                    <VCard
                      v-if="item[val.key]"
                      height="50"
                      width="50"
                      v-bind="activatorProps"
                      class="border ma-1 pa-0"
                    >
                      <v-img
                        class="h-100 w-100"
                        :src="
                          val.has_url === true ? item[val.key] : base_url + item[val.key]
                        "
                        loading="lazy"
                      />
                    </VCard>
                    <v-icon v-else size="30" class="ms-2" color="secondary"
                      >mdi-image-multiple-outline</v-icon
                    >
                  </template>
                  <template v-slot:default="{ isActive }">
                    <v-card :title="val.title_img">
                      <template v-slot:append>
                        <dir :title="$i18n.locale == 'ar' ? 'إغلاق' : 'Close'">
                          <v-btn @click="isActive.value = false" icon size="20">
                            <v-icon color="error">mdi-close</v-icon>
                          </v-btn>
                        </dir>
                      </template>

                      <v-responsive class="mx-5 my-2 border-md border-dashed">
                        <v-img
                          :src="
                            val.has_url === true
                              ? item[val.key]
                              : base_url + item[val.key]
                          "
                          class="ma-1 rounded-lg"
                        />
                      </v-responsive>
                    </v-card>
                  </template>
                </v-dialog>
                <!-- صح وخطأ (Boolean Icons) -->
                <span v-else-if="typeof item[val.key] == 'boolean'">
                  <v-icon v-if="item[val.key] == true" color="success"
                    >mdi-check-circle</v-icon
                  >
                  <v-icon v-if="item[val.key] == false" color="error"
                    >mdi-close-circle</v-icon
                  >
                </span>
                <!-- ملف (File Download) -->
                <span v-else-if="val.type == 'file'">
                  <a
                    v-if="item[val.key]"
                    @click="viewInNewTab(item[val.key])"
                    class="cursor-pointer"
                  >
                    <v-icon size="20" color="primary">mdi-folder-arrow-down</v-icon>
                  </a>
                </span>
                <!-- الاجراءات (Row Actions) -->
                <span
                  v-else-if="val.key == 'actions' && actionList && !is_restore_screen"
                >
                  <v-menu
                    transition="slide-y-transition"
                    location="bottom end"
                    offset="8"
                  >
                    <template v-slot:activator="{ props }">
                      <custom-btn
                        v-bind="props"
                        is-icon
                        icon="dots-vertical"
                        color="secondary"
                        variant="text"
                        :label="$t('details')"
                        @click="copy_item = item"
                      />
                    </template>

                    <v-card
                      elevation="24"
                      rounded="lg"
                      class="premium-menu-card border-thin overflow-hidden"
                      style="min-width: 220px"
                    >
                      <div
                        class="pa-3 border-b d-flex align-center"
                        style="background-color: rgba(var(--v-theme-primary), 0.08)"
                      >
                        <v-icon color="primary" class="me-2" size="20"
                          >mdi-dots-horizontal-circle-outline</v-icon
                        >
                        <div
                          class="text-caption font-weight-bold"
                          style="color: rgb(var(--v-theme-on-surface))"
                        >
                          {{ $i18n.locale == "ar" ? "إجراءات السجل" : "Record Actions" }}
                        </div>
                      </div>

                      <v-card-text class="pa-1">
                        <v-list density="compact" class="bg-transparent pa-0">
                          <!-- Group: Operations -->
                          <template v-if="addToActionsList.length > 0">
                            <v-list-subheader class="modern-subheader px-2 mt-1 mb-1">
                              {{
                                $i18n.locale == "ar"
                                  ? "عمليات مخصصة"
                                  : "Custom Operations"
                              }}
                            </v-list-subheader>

                            <template v-for="(i, key) in addToActionsList" :key="key">
                              <v-list-item
                                @click="i['click'](false)"
                                class="premium-list-item"
                              >
                                <template v-slot:prepend>
                                  <v-icon size="18" color="primary" class="me-2"
                                    >mdi-cog-play-outline</v-icon
                                  >
                                </template>
                                <v-list-item-title
                                  class="text-caption font-weight-medium"
                                  style="color: rgba(var(--v-theme-on-surface), 0.7)"
                                >
                                  {{
                                    $i18n.locale == "ar" ? i["title_ar"] : i["title_en"]
                                  }}
                                </v-list-item-title>
                                <template v-slot:append>
                                  <v-btn
                                    icon="mdi-open-in-new"
                                    variant="text"
                                    size="x-small"
                                    color="grey-lighten-1"
                                    @click.stop="i['click'](true)"
                                  ></v-btn>
                                </template>
                              </v-list-item>
                            </template>
                          </template>

                          <!-- Group: Management -->
                          <v-list-subheader class="modern-subheader px-2 mt-1 mb-1">
                            {{
                              $i18n.locale == "ar" ? "إدارة السجل" : "Record Management"
                            }}
                          </v-list-subheader>

                          <v-list-item
                            v-if="edit_con(item) && editItem && hasEditPermission"
                            @click="edit(item)"
                            class="premium-list-item"
                          >
                            <template v-slot:prepend>
                              <v-icon size="18" color="primary" class="me-2"
                                >mdi-square-edit-outline</v-icon
                              >
                            </template>
                            <v-list-item-title
                              class="text-caption font-weight-medium"
                              style="color: rgba(var(--v-theme-on-surface), 0.7)"
                            >
                              {{ $i18n.locale == "ar" ? "تعديل" : "Edit" }}
                            </v-list-item-title>
                          </v-list-item>

                          <v-list-item
                            v-if="del_con(item) && delItem && hasDeletePermission"
                            @click="deleteItem(item.id)"
                            class="premium-list-item text-error"
                          >
                            <template v-slot:prepend>
                              <v-icon size="18" color="error" class="me-2"
                                >mdi-delete-outline</v-icon
                              >
                            </template>
                            <v-list-item-title class="text-caption font-weight-medium">
                              {{ $i18n.locale == "ar" ? "حذف السجل" : "Delete Record" }}
                            </v-list-item-title>
                          </v-list-item>
                          <v-dialog max-width="800">
                            <template v-slot:activator="{ props: activatorProps }">
                              <v-list-item
                                v-bind="activatorProps"
                                class="premium-list-item"
                              >
                                <template v-slot:prepend>
                                  <v-icon size="18" color="primary" class="me-2"
                                    >mdi-eye-outline</v-icon
                                  >
                                </template>
                                <v-list-item-title
                                  class="text-caption font-weight-medium"
                                  style="color: rgba(var(--v-theme-on-surface), 0.7)"
                                >
                                  {{ $i18n.locale == "ar" ? "التفاصيل" : "Details" }}
                                </v-list-item-title>
                              </v-list-item>
                            </template>
                            <template v-slot:default="{ isActive }">
                              <v-card rounded="xl" elevation="24" class="border-thin">
                                <v-toolbar
                                  density="comfortable"
                                  color="surface"
                                  flat
                                  class="border-b px-4"
                                >
                                  <v-icon color="primary" class="me-2"
                                    >mdi-eye-outline</v-icon
                                  >
                                  <v-toolbar-title class="text-h6 font-weight-bold">{{
                                    $i18n.locale == "ar"
                                      ? "تفاصيل السجل"
                                      : "Record Details"
                                  }}</v-toolbar-title>
                                  <v-spacer></v-spacer>
                                  <v-btn
                                    icon="mdi-close"
                                    variant="text"
                                    size="small"
                                    @click="isActive.value = false"
                                  ></v-btn>
                                </v-toolbar>
                                <v-card-text class="pa-0 overflow-auto">
                                  <v-table class="details-table">
                                    <thead>
                                      <tr
                                        style="
                                          background-color: rgba(
                                            var(--v-theme-on-surface),
                                            0.03
                                          );
                                        "
                                      >
                                        <th
                                          class="text-subtitle-2 font-weight-bold px-6 py-4"
                                        >
                                          {{ $i18n.locale == "ar" ? "العنوان" : "Title" }}
                                        </th>
                                        <th
                                          class="text-subtitle-2 font-weight-bold px-6 py-4"
                                        >
                                          {{ $i18n.locale == "ar" ? "البيانات" : "Data" }}
                                        </th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr
                                        v-for="val_data in visibleHeaders.filter(
                                          (e) => e.key != 'actions'
                                        )"
                                        :key="val_data.key"
                                        class="hover-bg-light"
                                      >
                                        <td
                                          class="text-body-2 font-weight-medium px-6 py-3"
                                          style="
                                            width: 30%;
                                            color: rgb(var(--v-theme-on-surface));
                                          "
                                        >
                                          {{ val_data.title }}
                                        </td>
                                        <td class="text-body-2 px-6 py-3">
                                          <span v-if="val_data.type == 'file'">
                                            <a
                                              v-if="item[val_data.key]"
                                              :href="base_url + item[val_data.key]"
                                              target="_blank"
                                            >
                                              <v-icon size="20" color="primary"
                                                >mdi-folder-arrow-down</v-icon
                                              >
                                            </a>
                                          </span>
                                          <span v-else>{{ item[val_data.key] }}</span>
                                        </td>
                                      </tr>
                                    </tbody>
                                  </v-table>
                                </v-card-text>
                                <v-divider></v-divider>
                                <v-card-actions
                                  class="pa-4"
                                  style="
                                    background-color: rgba(
                                      var(--v-theme-on-surface),
                                      0.02
                                    );
                                  "
                                >
                                  <v-spacer></v-spacer>
                                  <v-btn
                                    variant="tonal"
                                    color="primary"
                                    class="px-6 rounded-lg font-weight-bold"
                                    @click="isActive.value = false"
                                  >
                                    {{ $i18n.locale == "ar" ? "إغلاق" : "Close" }}
                                  </v-btn>
                                </v-card-actions>
                              </v-card>
                            </template>
                          </v-dialog>
                        </v-list>
                      </v-card-text>
                    </v-card>
                  </v-menu>
                </span>

                <!-- Case: Standalone Actions or Restore Screen -->
                <span
                  v-else-if="
                    (val.key == 'actions' && !actionList) ||
                    (val.key == 'actions' && is_restore_screen)
                  "
                >
                  <!-- Edit Button -->
                  <custom-btn
                    v-if="edit_con(item) && editItem && hasEditPermission"
                    type="update"
                    is-icon
                    @click="edit(item)"
                    class="me-1"
                  />

                  <!-- Delete Button -->
                  <custom-btn
                    v-if="
                      del_con(item) &&
                      delItem &&
                      hasDeletePermission &&
                      !is_restore_screen
                    "
                    type="del"
                    is-icon
                    @click="deleteItem(item.id)"
                    class="me-1"
                  />

                  <!-- Restore Button -->
                  <custom-btn
                    v-if="is_restore_screen"
                    type="restore"
                    is-icon
                    :label="$i18n.locale == 'ar' ? 'استعادة السجل' : 'Restore Record'"
                    @click="restoreItem(item.id)"
                    class="me-1"
                  />

                  <!-- Details Button & Dialog -->
                  <v-dialog max-width="800">
                    <template v-slot:activator="{ props: activatorProps }">
                      <custom-btn
                        v-bind="activatorProps"
                        type="show"
                        is-icon
                        :label="$i18n.locale == 'ar' ? 'تفاصيل السجل' : 'Record Details'"
                        class="me-1"
                        v-if="hasInfo"
                      />
                    </template>
                    <template v-slot:default="{ isActive }">
                      <v-card
                        rounded="xl"
                        elevation="12"
                        class="border-thin overflow-hidden"
                      >
                        <v-toolbar
                          density="compact"
                          color="surface"
                          flat
                          class="border-b px-4"
                        >
                          <v-icon color="primary" class="me-2"
                            >mdi-information-outline</v-icon
                          >
                          <v-toolbar-title class="text-h6 font-weight-bold">{{
                            $i18n.locale == "ar" ? "تفاصيل السجل" : "Record Details"
                          }}</v-toolbar-title>
                          <v-spacer></v-spacer>
                          <v-btn
                            icon="mdi-close"
                            variant="text"
                            size="small"
                            @click="isActive.value = false"
                          ></v-btn>
                        </v-toolbar>

                        <v-card-text class="pa-0 overflow-auto">
                          <v-table class="details-table">
                            <thead>
                              <tr
                                style="
                                  background-color: rgba(var(--v-theme-on-surface), 0.05);
                                "
                              >
                                <th
                                  class="text-subtitle-2 font-weight-bold px-6 py-4"
                                  style="color: rgb(var(--v-theme-on-surface))"
                                >
                                  {{ $i18n.locale == "ar" ? "العنوان" : "Title" }}
                                </th>
                                <th
                                  class="text-subtitle-2 font-weight-bold px-6 py-4"
                                  style="color: rgb(var(--v-theme-on-surface))"
                                >
                                  {{ $i18n.locale == "ar" ? "البيانات" : "Data" }}
                                </th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr
                                v-for="val_data in headers.filter(
                                  (e) => e.key != 'actions'
                                )"
                                :key="val_data.key"
                                class="hover-bg-light"
                              >
                                <td
                                  class="text-body-2 font-weight-medium px-6 py-3"
                                  style="
                                    width: 30%;
                                    color: rgba(var(--v-theme-on-surface), 0.7);
                                  "
                                >
                                  {{ val_data.title }}
                                </td>
                                <td
                                  class="text-body-2 px-6 py-3"
                                  style="color: rgb(var(--v-theme-on-surface))"
                                >
                                  <span v-if="val_data.type == 'file'">
                                    <a
                                      v-if="item[val_data.key]"
                                      :href="base_url + item[val_data.key]"
                                      target="_blank"
                                    >
                                      <v-icon size="20" color="primary"
                                        >mdi-folder-arrow-down</v-icon
                                      >
                                    </a>
                                  </span>
                                  <span v-else>{{ item[val_data.key] }}</span>
                                </td>
                              </tr>
                            </tbody>
                          </v-table>
                        </v-card-text>

                        <v-divider></v-divider>
                        <v-card-actions
                          class="pa-4"
                          style="background-color: rgba(var(--v-theme-on-surface), 0.05)"
                        >
                          <v-spacer></v-spacer>
                          <v-btn
                            variant="tonal"
                            color="primary"
                            class="px-6 rounded-lg font-weight-bold"
                            @click="isActive.value = false"
                          >
                            {{ $i18n.locale == "ar" ? "إغلاق" : "Close" }}
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </template>
                  </v-dialog>

                  <slot name="action-row" :item="item" />
                </span>

                <!-- <span v-else v-tooltip="item[val.key]?.length > 40 ? item[val.key] : ''"> -->
                <span v-else>
                  {{ item[val.key] }}
                  <v-tooltip activator="parent" location="top" open-delay="500">
                    {{ item[val.key] }}
                  </v-tooltip>
                </span>
              </slot>
            </td>
          </tr>
        </template>

        <template v-slot:item.actions="{ item }" v-if="!customTable">
          <span v-if="actionList && !is_restore_screen">
            <v-menu location="end" lazy>
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-cog"
                  color="info"
                  width="26"
                  height="26"
                  variant="text"
                  @click="copy_item = item"
                />
              </template>

              <v-list density="compact" class="py-0 cursor-auto rounded-lg pa-0 ma-0">
                <template v-for="(i, key) in addToActionsList" :key="key">
                  <v-list-item class="ma-0 pa-0">
                    <template v-slot:title>
                      <Custom-btn
                        variant="text"
                        @click="i['click'](false)"
                        :label="$i18n.locale == 'ar' ? i['title_ar'] : i['title_en']"
                      />
                    </template>

                    <template v-slot:append>
                      <VSheet>
                        <template v-slot:default>
                          <Custom-btn
                            icon="mdi-open-in-new"
                            elevation="0"
                            class="ma-0 pa-0"
                            @click="i['click'](true)"
                            width="20"
                          />
                          <v-tooltip activator="parent" location="top">{{
                            $i18n.locale == "ar" ? "فتح في تبويب جديد" : "Open in new tab"
                          }}</v-tooltip>
                        </template>
                      </VSheet>
                    </template>
                  </v-list-item>
                </template>

                <v-list-item
                  0.
                  v-if="edit_con(item) && editItem && hasEditPermission"
                  v-ripple
                  @click="edit(item)"
                >
                  {{ $i18n.locale == "ar" ? "تعديل" : "Edit" }}
                  <template v-slot:append>
                    <v-icon color="warning" icon="mdi-pencil-outline" />
                  </template>
                </v-list-item>
                <v-list-item
                  v-if="
                    del_con(item) && delItem && hasDeletePermission && !is_restore_screen
                  "
                  v-ripple
                  @click="deleteItem(item.id)"
                >
                  {{ $i18n.locale == "ar" ? "حذف" : "Delete" }}
                  <template v-slot:append>
                    <v-icon color="error" icon="mdi-trash-can-outline" />
                  </template>
                </v-list-item>
                <v-dialog max-width="800">
                  <template v-slot:activator="{ props: activatorProps }">
                    <v-list-item v-ripple v-bind="activatorProps">
                      {{ $i18n.locale == "ar" ? "تفاصيل" : "details" }}
                      <template v-slot:append>
                        <v-icon color="primary">mdi-information-outline</v-icon>
                      </template>
                    </v-list-item>
                  </template>
                  <template v-slot:default="{ isActive }">
                    <v-card>
                      <template v-slot:text>
                        <VCol>
                          <v-card id="table_report">
                            <VTable
                              density="compact"
                              style="background: rgba(var(--v-theme-primary), 0.05)"
                            >
                              <thead>
                                <tr>
                                  <th>
                                    <{{ $i18n.locale == "ar" ? "العنوان" : "Tilte" }}>
                                  </th>
                                  <th>
                                    {{ $i18n.locale == "ar" ? "البيانات" : "Data" }}
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr
                                  v-for="val_data in visibleHeaders.filter(
                                    (e) => e.key != 'actions'
                                  )"
                                  :key="val_data.key"
                                >
                                  <td>
                                    {{ val_data.title }}
                                  </td>
                                  <td>
                                    {{ item[val_data.key] }}
                                  </td>
                                </tr>
                              </tbody>
                            </VTable>
                          </v-card>
                        </VCol>
                      </template>

                      <v-card-actions>
                        <custom-btn
                          type="cancel"
                          @click="isActive.value = false"
                        ></custom-btn>
                      </v-card-actions>
                    </v-card>
                  </template>
                </v-dialog>
              </v-list>
            </v-menu>
          </span>
          <span v-else>
            <custom-btn
              v-if="edit_con(item) && editItem && hasEditPermission"
              type="update"
              isIcon
              elevation="0"
              color="transparent"
              icon-color="green"
              :click="() => edit(item)"
            />
            <custom-btn
              v-if="del_con(item) && delItem && hasDeletePermission && !is_restore_screen"
              type="del"
              isIcon
              elevation="0"
              color="transparent"
              icon-color="red"
              :click="() => deleteItem(item.id)"
            />
            <span>
              <v-dialog max-width="800">
                <template v-slot:activator="{ props: activatorProps }">
                  <v-btn
                    v-bind="activatorProps"
                    icon="mdi-information-outline"
                    color="primary"
                    width="26"
                    height="26"
                    variant="text"
                  />
                </template>
                <template v-slot:default="{ isActive }">
                  <v-card>
                    <template v-slot:text>
                      <VCol>
                        <v-card id="table_report">
                          <VTable>
                            <thead>
                              <tr>
                                <th>العنوان</th>
                                <th>البيانات</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr
                                v-for="val_data in visibleHeaders.filter(
                                  (e) => e.key != 'actions'
                                )"
                                :key="val_data.key"
                              >
                                <td>
                                  {{ val_data.title }}
                                </td>
                                <td>
                                  {{ item[val_data.key] }}
                                </td>
                              </tr>
                            </tbody>
                          </VTable>
                        </v-card>
                      </VCol>
                    </template>

                    <v-card-actions>
                      <custom-btn
                        type="cancel"
                        @click="isActive.value = false"
                      ></custom-btn>
                    </v-card-actions>
                  </v-card>
                </template>
              </v-dialog>
            </span>

            <custom-btn
              v-if="is_restore_screen"
              type="restore"
              isIcon
              elevation="0"
              color="transparent"
              icon-color="green"
              label="استعادة العنصر"
              @click="restoreItem(item.id)"
            />
          </span>
        </template>

        <template
          v-for="(slot, name) in $slots"
          :slot="name"
          v-slot:[name]="scope"
          :key="slot"
        >
          <slot v-if="!isEmptyReprort" :name="name" v-bind="scope"></slot>
        </template>

        <template v-slot:bottom>
          <v-sheet
            v-if="!is_print && items?.pagination"
            style="background: rgba(var(--v-theme-primary), 0.08) !important"
          >
            <v-row>
              <!-- Section: Data Metrics (Clean & Minimalist) -->
              <v-col cols="auto">
                <!-- Section: Data Metrics (Clean & Minimalist) -->
                <div class="d-flex align-center flex-wrap">
                  <!-- Entries Selector -->
                  <div class="d-flex align-center pe-4">
                    <span
                      class="text-caption font-weight-bold me-2"
                      style="
                        color: rgba(var(--v-theme-on-surface), 0.7);
                        font-size: 13px !important;
                      "
                      >{{ $i18n.locale == "ar" ? "عرض:" : "Show:" }}</span
                    >
                    <v-menu offset="4">
                      <template v-slot:activator="{ props }">
                        <div
                          v-bind="props"
                          class="cursor-pointer d-flex align-center text-caption font-weight-black"
                          style="
                            color: rgb(var(--v-theme-on-surface));
                            font-size: 13px !important;
                          "
                        >
                          {{ params.page_size }}
                          <v-icon size="14" class="ms-1 opacity-60"
                            >mdi-chevron-down</v-icon
                          >
                        </div>
                      </template>
                      <v-list density="compact" class="rounded-lg border-thin shadow-xl">
                        <v-list-item
                          v-for="item in listItemsPerPage"
                          :key="item.value"
                          @click="
                            params.page_size = item.value;
                            fetchData();
                          "
                          :active="params.page_size === item.value"
                          color="primary"
                        >
                          <v-list-item-title
                            class="text-caption font-weight-bold text-center"
                            style="font-size: 12px !important"
                            >{{ item.text }}</v-list-item-title
                          >
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </div>

                  <!-- Vertical Separator -->
                  <div
                    class="mx-2"
                    style="
                      height: 16px;
                      border-left: 1.5px solid rgba(var(--v-theme-on-surface), 0.12);
                    "
                  ></div>

                  <!-- Total Counter -->
                  <div class="d-flex align-center ps-4">
                    <v-icon size="16" color="primary" class="me-2"
                      >mdi-database-outline</v-icon
                    >
                    <span
                      class="text-caption font-weight-bold"
                      style="
                        color: rgb(var(--v-theme-on-surface));
                        font-size: 13px !important;
                      "
                    >
                      {{ $i18n.locale == "ar" ? "الإجمالي:" : "Total:" }}
                      <span
                        class="text-caption font-weight-black mx-1"
                        style="
                          color: rgb(var(--v-theme-primary));
                          font-size: 13px !important;
                        "
                        >{{ items?.pagination?.count || 0 }}</span
                      >
                      <span
                        class="text-caption font-weight-bold"
                        style="
                          color: rgba(var(--v-theme-on-surface), 0.5);
                          font-size: 13px !important;
                        "
                        >{{ $i18n.locale == "ar" ? "عناصر" : "items" }}</span
                      >
                    </span>
                  </div>
                </div>
              </v-col>
              <v-spacer />
              <v-col cols="auto" class="ma-0 pa-0">
                <v-pagination
                  v-if="'pagination' in items"
                  v-model="params.page"
                  :length="items?.pagination?.num_pages"
                  show-first-last-page
                  rounded="lg"
                  density="comfortable"
                  total-visible="5"
                  @update:model-value="fetchData"
                  active-color="primary"
                  class="overflow-auto"
                />
              </v-col>
            </v-row>
          </v-sheet>
        </template>
      </component>
    </v-card>
  </VCard>

  <!-- نافذه restore  -->
  <custom-dialog
    v-model="delete_log_dialog"
    :title="label ? label : $i18n.locale == 'ar' ? 'السجلات المحذوفة' : 'Deleted records'"
    class="mt-5"
    fullscreen
  >
    <VCard class="print">
      <restore-table
        :headers="headers"
        :url="delItem"
        :customTable="customTable"
        :getDataAfterRestore="fetchData"
      />
    </VCard>
  </custom-dialog>

  <!-- نافذة تاكيد استعادة العنصر -->
  <confirm-dialog v-model="restore_dialog" type="warning" :confirmBtn="restoreData"
    ><template v-slot:body>استرجاع العناصر المحذوفة</template>
  </confirm-dialog>

  <!-- تاكيد الحذف -->
  <confirm-deletion
    v-model="del_dialog"
    :url="delItem"
    :delRefresh="delRefresh"
    :delete-item="value.length > 0 ? value : delete_id"
    :getData="fetchData"
    :items="items"
    :selectItems="value"
    :itemValue="itemValue"
    :returnObject="returnObject"
  />

  <custom-dialog
    v-if="imoprtExcel"
    v-model="dialog_import_to_excel"
    title="استيراد من اكسل"
    height="auto"
    width="auto"
  >
    <template v-slot>
      <import-excel
        v-model="dialog_import_to_excel"
        @process-export="(data, status) => $emit('process-export', data, status)"
        :fields="fields_excel"
        :newDataToExcel="newDataToExcel"
        :newHeadersExcel="newHeadersExcel"
        :exclude_field_excel="exclude_field_excel"
        :fileExcel="fileExcel"
        :startRow="startRow"
        :startHeader="startHeader"
        :attr_field_excel="attr_field_excel"
        :loadinExportToExcel="loadinExportToExcel"
        :url="url || delItem"
        :auto-import-excel="autoImportExcel"
        :getData="getData"
        @close-imort-excel="dialog_import_to_excel = false"
      />
    </template>
  </custom-dialog>

  <!-- الفلتره -->

  <filter-table
    v-model="filter_dialog"
    :headers="headers"
    @apply-filters="applyFilters"
    :local-loading="local_loading"
    :active-filters-default="activeFilters"
    :loadingApplyFilters="loading"
  />
</template>
<script>
import shared from "external-components";

import { VDataTableServer } from "vuetify/components";
import { VDataTableVirtual } from "vuetify/components";
import { state } from "@/../src/store/state";
import _ from "lodash";
import NotFound from "../../../other/NotFound.vue";
import PreviewContentHtml from "../../../other/PreviewContentHtml.vue";
import { useHeaderFooterStore } from "../../../../src/stores/headerFooterStore";
import FilterTable from "./children/filterTable/FilterTable.vue";
export default {
  components: {
    VDataTableServer,
    VDataTableVirtual,
    NotFound,
    PreviewContentHtml,
    FilterTable,
  },
  props: {
    canPrintReportEmpty: { type: Boolean, default: false },
    canPrintReport: { type: Boolean, default: false },
    attr_field_excel: Object,
    select_header: {
      type: Boolean,
      default: true,
    },
    height: {
      type: String,
      default: "auto",
    },
    numbering: {
      type: Boolean,
      default: true,
    },
    showTop: {
      type: Boolean,
      default: true,
    },
    customLoading: {
      type: Boolean,
      default: false,
    },
    customTable: {
      type: Boolean,
      default: true,
    },
    modelValue: {
      type: Array,
      default: null,
    },
    pagination: {
      type: Boolean,
      default: true,
    },
    items: {
      type: Object,
      default() {
        return {
          results: [],
          pagination: {
            count: 0,
            current_page: 1,
            num_pages: 0,
          },
        };
      },
    },
    itemValue: {
      type: String,
      default() {
        return "id";
      },
    },

    showSelect: {
      type: Boolean,
      default() {
        return true;
      },
    },

    headers: {
      type: Array,
      required: true,
      default() {
        return [];
      },
    },

    actions: {
      type: Boolean,
      default() {
        return true;
      },
    },

    getData: { type: Function },

    create: {
      type: [Function, Boolean],
      default() {
        return false;
      },
    },
    delItem: {
      type: [Function, Boolean, String],
      default() {
        return false;
      },
    },

    editItem: {
      type: [Function, Boolean],
      default() {
        return false;
      },
    },
    hasInfo: {
      type: Boolean,
      default: true,
    },

    actionList: {
      type: [String, Boolean, Object, Array],
    },
    returnObject: {
      type: Boolean,
      default() {
        return false;
      },
    },
    search: {
      type: Boolean,
      default: true,
    },
    edit_con: {
      type: Function,
      default(item) {
        return true;
      },
    },
    del_con: {
      type: Function,
      default(item) {
        return true;
      },
    },
    restore: {
      type: Boolean,
      default: true,
    },

    is_restore_screen: {
      type: Boolean,
      default: false,
    },
    refresh: {
      type: Boolean,
      default: true,
    },
    log: {
      type: Boolean,
      default: true,
    },

    imoprtExcel: {
      type: Boolean,
      default: false,
    },

    fields_excel: {
      type: Array,
    },
    newDataToExcel: {
      type: Array,
      default: [],
    },
    newHeadersExcel: { type: Array },

    exclude_field_excel: { type: Array, default: [] },
    fileExcel: String,

    startRow: { type: Number },
    startHeader: { type: Number },
    ExportToExcel: { type: Boolean, default: true },
    delRefresh: { type: Boolean, default: false },
    loadinExportToExcel: { type: Boolean, default: false },
    perm_url: undefined,

    getDataAfterRestore: Function,
    hasFilter: { type: Boolean, default: true },
    logUrl: String,
    canSelectDelete: { type: Boolean, default: true },
    rowClass: { type: Function, default: (item) => "" },
    autoImportExcel: {
      type: Boolean,
      default: false,
    },
    fixedHeader: {
      type: Boolean,
      default: false,
    },
    url: String,
  },
  data() {
    return {
      base_url: this.setting.url_img,
      error_in_fetch: false,
      isEmptyReprort: false,
      sortBy: [],
      copy_headers: [],
      header_actions: {
        title: this.$i18n.locale === "ar" ? "الاجراءات" : "actions",
        key: "actions",
        sortable: false,
      },
      header_numbering: {
        title: "#",
        key: "numbering",
        sortable: false,
        class: "col-custom",
      },

      itemsPerPage: [],
      listItemsPerPage: [
        { id: 0, value: 10, text: "10" },
        { id: 1, value: 25, text: "25" },
        { id: 2, value: 50, text: "50" },
        { id: 3, value: 100, text: "100" },
        // { id: 4, value: 500, text: "500" },
      ],

      params: {
        page: 1,
        page_size: 10,
      },
      copy_item: {},
      alert_del: {},

      delete_id: undefined,

      restore_id: undefined,

      selectedRow: null,
      hoveredRow: null,

      loading: false,

      restore_dialog: false,

      del_dialog: false,
      success_del: false,

      is_print: false,

      del_loading: false,
      delete_log_dialog: false,
      log_dialog: false,
      dialog_import_to_excel: false,

      protected_records: false,
      message_protected_records: [],

      is_parent_select: undefined,

      title_snackbar: undefined,

      selectItem: [],

      route_name: undefined,

      custom_title: undefined,
      activeFilters: undefined,
      filter_dialog: false,
    };
  },
  created() {
    this.route_name = this.perm_url || this.$route.name;

    this.copy_headers = Array.isArray(this.headers) ? [...this.headers] : [];

    // if (this.actions)
    //   this.copy_headers.push({
    //     title: this.$t("actions"),
    //     key: "actions",
    //     sortable: false,
    //   });

    this.change_status_headers();
  },
  methods: {
    viewInNewTab(url) {
      if (!url) return;

      const newWindow = window.open("", "_blank");

      if (newWindow) {
        newWindow.opener = null;
        newWindow.location.href = this.base_url + url;
      } else {
        alert("الملف غير صحيح");
      }
    },

    resetPagination() {
      this.itemsPerPage = [];
      this.params = {
        page: 1,
        page_size: 10,
      };
    },

    ExportExcel(selected = undefined) {
      this.is_parent_select = selected;
      const title =
        this.$i18n.locale == "ar"
          ? this.$route?.matched?.find((e) => e.name == this.$route.name).props?.default
              ?.name_ar
          : this.$route?.matched?.find((e) => e.name == this.$route.name).props?.default
              ?.name_en;

      if (this.data && this.data.length > 0) {
        shared.ExportToExcel(
          this.visibleHeaders
            .filter((e) => e.type != "img" && e.key != "actions" && e.key != "numbering")
            .map((e) => {
              return { header: e.title, key: e.key };
            }),
          this.data,
          title || ""
        );
      } else this.$snack("empty");

      this.is_parent_select = undefined;
    },

    multipleMethodes(element) {
      // const item = this.copy_item;

      for (const select of this.selectItem) {
        var item = this.returnObject
          ? select
          : this.items.results.find((f) => f[this.itemValue] === select);
        const funAction = _.cloneDeep(this.actionList(item));
        var actionList = "auto" in funAction ? funAction.auto : funAction;

        this.$navigateTo({
          name: element.name,
          params: actionList,
          ar: actionList.ar,
          en: actionList.en || actionList.ar,
          blank: true,
        });
      }
    },

    change_status_headers() {
      this.copy_headers
        .filter((e) => e.show == undefined)
        .map((r) => {
          r.show = true;
        });
    },

    async fetchData() {
      this.selectItem = [];
      this.error_in_fetch = false;
      this.loading = true;

      this.params.sort_by = this.order_data();
      const params = {
        params: {
          ...this.params,
          filters: this.activeFilters,
          hasPagination: this.pagination && "pagination" in this.items,
        },
      };

      let sort_by = params.params.sort_by;

      if (sort_by) {
        if (sort_by.endsWith("__display")) {
          sort_by = sort_by.slice(0, -9);
        } else if (sort_by.endsWith("_display")) {
          sort_by = sort_by.slice(0, -8);
        }
      }

      params.params.sort_by = sort_by;

      this.getData
        ? await this.getData(params).catch((e) => {
            this.error_in_fetch = true;
          })
        : "";

      this.loading = false;
    },

    edit(data) {
      this.editItem(data);
    },
    // حذف العنصر
    deleteItem(id) {
      this.delete_id = id;
      this.del_dialog = true;
    },

    // printReport(parent_select = undefined) {
    //   state.print = true;
    //   this.is_print = true;
    //   this.is_parent_select = parent_select;

    //   setTimeout(() => {
    //     const printContent = this.$refs.report.$el.innerHTML;
    //     document.getElementById("printView").style.display = "block";
    //     document.getElementById("printView").innerHTML = printContent;
    //     document.getElementById("printView").style.backgroundColor = "white";
    //     document.getElementById("printView").style.height = "auto !important";
    //     document.getElementById("appViewId").style.display = "none";
    //     document.querySelectorAll(".v-table__wrapper").forEach((el) => {
    //       el.style.height = "auto";
    //     });

    //     setTimeout(() => {
    //       window.print();
    //       document.getElementById("printView").innerHTML = "";
    //       document.getElementById("printView").style.display = "none";
    //       document.getElementById("appViewId").style.display = "block";
    //       document.querySelectorAll(".v-table__wrapper").forEach((el) => {
    //         el.style.height = this.height;
    //       });

    //       this.is_print = false;
    //       state.print = false;

    //       this.is_parent_select = undefined;
    //     }, 500);
    //   }, 200);
    // },

    handleTypePrint(type) {
      let parent_select = undefined;
      if (type === "selected") parent_select = true;
      else if (type === "unselected") parent_select = false;

      this.printReport(parent_select);
    },

    async printReport(parent_select = undefined, isEmpty = false) {
      this.isEmptyReprort = isEmpty;
      state.print = true;

      const headerFooterStore = useHeaderFooterStore();
      await headerFooterStore.changeHeaderFooter({
        fk_screen: this.$route?.meta?.fk_screen,
      });

      if (!headerFooterStore.headerFooterData) {
        this.$snack("errorData", {
          message: "يرجى ربط الشاشة مع الرأس والتذييل",
        });
        return;
      }

      this.is_parent_select = parent_select;

      this.is_print = true;
      // إضافة تأخير بسيط جداً (Buffer) لضمان استقرار المتصفح
      await new Promise((resolve) => setTimeout(resolve, 200));
      const elementToPrint = this.$refs.report.$el.innerHTML;

      if (!elementToPrint) {
        console.error("العنصر موجود ولكن لا يحتوي على محتوى (innerHTML)");
        return;
      }

      // ننتظر قليلاً لضمان ظهور عنصر printView في الـ DOM
      await new Promise((resolve) => setTimeout(resolve, 300));

      const printView = document.getElementById("printView");
      if (!printView) {
        console.error("عنصر printView غير موجود في الـ DOM");
        state.print = false;
        this.is_print = false;
        return;
      }

      // نسخ المحتوى إلى حاوية الطباعة
      printView.innerHTML = elementToPrint;

      // --- الجزء الجديد: انتظار تحميل الصور ---
      const images = printView.querySelectorAll("img");
      const imagePromises = Array.from(images).map((img) => {
        if (img.complete) {
          return Promise.resolve(); // الصورة محملة مسبقاً
        }
        return new Promise((resolve) => {
          img.onload = resolve; // نجاح التحميل
          img.onerror = resolve; // حتى لو فشل التحميل، نكمل لكي لا تتعطل الطباعة
        });
      });

      try {
        // انتظار جميع الصور حتى تنتهي من التحميل

        await Promise.all(imagePromises);

        // إضافة تأخير بسيط جداً (Buffer) لضمان استقرار المتصفح
        await new Promise((resolve) => setTimeout(resolve, 200));

        // تشغيل أمر الطباعة
        window.print();
      } catch (err) {
        console.error("خطأ أثناء انتظار الصور:", err);
      } finally {
        // التنظيف وإعادة الحالة
        printView.innerHTML = "";
        this.isEmptyReprort = false;
        this.is_print = false;
        state.print = false;

        headerFooterStore.headerFooterData = {};

        this.is_parent_select = undefined;
      }
    },
    //  الترتيب
    order_data() {
      try {
        return this.sortBy[0].order == "desc"
          ? `-${this.sortBy[0].key}`
          : this.sortBy[0].key;
      } catch (error) {
        return "id";
      }
    },

    restoreItem(id) {
      this.restore_dialog = true;
      this.restore_id = id;
    },
    async restoreData() {
      try {
        this.restore_dialog = true;

        const data = [];
        data.push(this.restore_id);

        await this.$axios.patch(this.delItem + "restore" + "/", data);

        // this.$alert("del", {
        //   message:"البيانات المحذوفة",
        //   sub_message: response.data.deleted_objects.map((e) => e.name),
        // });
        this.selectItem = [];
        this.fetchData();
        this.getDataAfterRestore();
      } catch {
        this.items = {};
      } finally {
        this.restore_dialog = false;
        this.restore_id = undefined;
      }
    },

    async applyFilters(filters) {
      this.activeFilters = filters;

      await this.fetchData();
    },
    async resetFilters() {
      this.activeFilters = undefined;

      await this.fetchData();
    },
  },
  computed: {
    hasAddPermission() {
      return this.$perm("add", this.route_name);
    },
    hasEditPermission() {
      return this.$perm("edit", this.route_name);
    },
    hasDeletePermission() {
      return this.$perm("delete", this.route_name);
    },
    hasExportPermission() {
      return this.$perm("export", this.route_name);
    },
    hasImportPermission() {
      return this.$perm("import", this.route_name) && this.imoprtExcel;
    },
    hasPrintPermission() {
      return this.$perm("print", this.route_name);
    },
    hasRestorePermission() {
      return this.$perm("restore", this.route_name) && this.restore;
    },
    hasLogPermission() {
      return this.$perm("log", this.route_name) && this.log;
    },

    addToActionsList() {
      try {
        const item = this.copy_item || {};
        const actionResult =
          this.actionList && typeof this.actionList === "function"
            ? this.actionList(item)
            : this.actionList === true
            ? null
            : this.actionList;
        if (!actionResult) return [];

        const funAction = _.cloneDeep(actionResult);
        if (Array.isArray(funAction))
          return funAction.map((e) => ({ ...e, type: "list" }));
        else {
          var actionList = funAction && "auto" in funAction ? funAction.auto : funAction;
          if (!actionList) return [];

          var list_route = [];
          const matchedRoute = this.$route.matched.find(
            (e) => e.name === this.$route.name
          );

          if (matchedRoute && matchedRoute.children) {
            matchedRoute.children.forEach((e) => {
              if (e.type_of_screen != 1)
                list_route.push({
                  title_ar: e.props?.name_ar || e.name,
                  title_en: e.props?.name_en || e.name,
                  name: e.name,
                  click: (blank) => {
                    this.$navigateTo({
                      name: e.name,
                      params: actionList,
                      ar: actionList.ar,
                      en: actionList.en || actionList.ar,
                      blank: blank,
                      icon: e?.meta?.icon ?? "",
                    });
                  },
                });
            });
          }

          return funAction && "list" in funAction
            ? [
                ...(funAction.list || []).map((e) => ({ ...e, type: "list" })),
                ...list_route,
              ]
            : list_route;
        }
      } catch (error) {
        console.error("Error in addToActionsList:", error);
        return [];
      }
    },
    value: {
      get() {
        if (this.modelValue != null) return this.modelValue;
        else return this.selectItem;
      },
      set(value) {
        if (this.modelValue != null) this.$emit("update:modelValue", value);
        else this.selectItem = value;
      },
    },
    data() {
      if (this.pagination) {
        if (this.isEmptyReprort == true) {
          const obj_empty = {};
          let list_empty = [];

          this.visibleHeaders.map((e) => {
            obj_empty[e.key] = "";
          });

          for (let i = 0; i <= 20; i++) {
            list_empty.push(obj_empty);
          }

          return list_empty;
        } else if (this.is_parent_select == true) {
          return this.items?.results.filter((item) =>
            this.value.some((e) =>
              this.returnObject
                ? e[this.itemValue] === item[this.itemValue]
                : e === item[this.itemValue]
            )
          );
        } else if (this.is_parent_select == false)
          return this.items?.results.filter(
            (item) =>
              !this.value.some((e) =>
                this.returnObject
                  ? e[this.itemValue] === item[this.itemValue]
                  : e === item[this.itemValue]
              )
          );
        else return this.items?.results;
      } else {
        if (this.isEmptyReprort == true) {
          const obj_empty = {};
          let list_empty = [];

          this.visibleHeaders.map((e) => {
            obj_empty[e.key] = "";
          });

          for (let i = 0; i <= 20; i++) {
            list_empty.push(obj_empty);
          }

          return list_empty;
        } else if (this.is_parent_select == true) {
          return this.items?.filter((item) =>
            this.selectItem.includes(this.returnObject ? item : item[this.itemValue])
          );
        } else if (this.is_parent_select == false)
          return this.items.filter(
            (item) =>
              !this.selectItem.includes(this.returnObject ? item : item[this.itemValue])
          );
        else return this.items;
      }
    },
    paginate() {
      return this.items?.pagination;
    },
    visibleHeaders() {
      // header_numbering
      let headers = this.copy_headers.filter((header) => header.show);

      if (this.numbering) headers = [this.header_numbering, ...headers];

      if (this.is_print || this.selectItem.length > 0) {
        return headers;
      } else {
        if (this.actions) headers = [...headers, this.header_actions];
        return headers;
      }
    },
    showOperations() {
      return (
        this.imoprtExcel ||
        this.hasRestorePermission ||
        this.hasLogPermission ||
        this.canPrintReprort ||
        this.hasPrintPermission ||
        this.ExportToExcel
      );
    },
  },
  watch: {
    headers() {
      this.copy_headers = this.headers;
      this.change_status_headers();
    },
  },
};
</script>

<style scoped>
:deep(tr[style*="height: 0px"] td) {
  padding: 0 !important;
  border: none !important;
}
</style>
