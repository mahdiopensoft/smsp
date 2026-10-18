<template>
  <!-- added by samer -->
  <VCard
    ref="report"
    elevation="0"
    :loading="loading"
    class="p-0 ma-0 border-sm"
    :style="'overflow:unset !important'"
  >
    <VForm ref="form" @submit.prevent>
      <VDataTableVirtual
        id="vDataTable"
        v-model:selected="selectedItems"
        v-model:sort-by="sortBy"
        :headers="visibleHeaders"
        :items="data"
        density="compact"
        :loading="loading || customLoading"
        :item-value="itemValue"
        :class="{
          'custom-data-table': true,
          'flex-grow-1': true,
          'class-numbering-child-2': showIndex && showSelect && !is_print,
          'class-numbering-child-1':
            (showIndex && !showSelect && !is_print) || (showIndex && is_print),
          'mb-10': $vuetify.display.mobile,
        }"
        :search="search"
        height="auto"
        style="z-index: 10000 !important"
      >
        <!-- :style="`height:${height}`" -->
        <template #no-data>
          <template v-if="canAdd && !search">
            <VBtn
              @click="addRowAfter(index), (isEditing = true)"
              class="ma-5 float-start"
              color="primary"
              prepend-icon="mdi-plus"
              :text="$i18n.locale == 'ar' ? 'إضافة صف' : 'Addd Row'"
            >
            </VBtn>
          </template>
          <template v-else>
            <!-- {{ $t("not-found") }}
              {{ $i18n.locale == "ar" ? "لايوجد" : "Not Found" }} -->
            <NotFound />
          </template>
        </template>

        <template v-slot:loading>
          <v-skeleton-loader
            :type="`table-row-divider@${items?.results?.length || 10}`"
          />
        </template>

        <template v-slot:top>
          <!-- <table-header v-if="is_print" /> -->
          <div
            v-if="!is_print && showTop"
            class="d-flex align-center px-4 py-3 custom-data-table-toolbar bg-surface border-b gap-2 hide-item"
          >
            <!-- View Tools Group (Start Side) -->
            <div
              :class="[
                'd-flex align-center gap-1 flex-wrap flex-sm-nowrap flex-md-grow-0',
                'flex-grow-1',
              ]"
            >
              <!-- Column Visibility (The Eye) -->
              <v-menu
                v-if="top"
                :close-on-content-click="false"
                transition="slide-y-transition"
                :menu-props="{ zIndex: 10000 }"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="tonal"
                    color="primary"
                    size="small"
                    class="rounded-lg flex-shrink-0"
                    style="height: 38px; min-width: 38px; z-index: 10000 !important"
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
                  style="min-width: 280px; z-index: 10000 !important"
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
                        :disabled="
                          selectedItems.length > 0 && h.key == 'actions' ? true : false
                        "
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
                v-if="canSearch"
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                :placeholder="
                  $t('search-here') || ($i18n.locale === 'ar' ? 'ابحث...' : 'Search...')
                "
                density="compact"
                variant="solo-filled"
                flat
                hide-details
                clearable
                class="modern-search-field flex-grow-1 flex-shrink-1"
                style="max-width: 100%; min-width: 140px"
                @keydown.enter.prevent
                type="search"
              />
            </div>

            <!-- Data Operations Group (Middle) -->
            <div
              :class="[
                'd-flex align-center gap-1 hide-item flex-wrap flex-md-nowrap flex-grow-1 flex-lg-grow-0',
                search !== undefined ? 'ps-sm-2 border-sm-s' : '',
              ]"
            >
              <!-- Refresh -->
              <v-btn
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
              <!-- Print & Export Menu -->
              <v-menu
                :close-on-content-click="true"
                v-if="top"
                :menu-props="{ zIndex: 10000 }"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="tonal"
                    color="primary"
                    size="small"
                    class="rounded-lg flex-shrink-0"
                    style="height: 38px; min-width: 38px; z-index: 10000 !important"
                  >
                    <v-icon size="20">mdi-cog-sync-outline</v-icon>
                    <VTooltip activator="parent" location="top">{{
                      $i18n.locale == "ar" ? "العمليات العامة" : "General Operations"
                    }}</VTooltip>
                  </v-btn>
                </template>
                <v-card
                  elevation="24"
                  rounded="lg"
                  class="premium-menu-card border-thin mt-2 overflow-hidden"
                  style="min-width: 260px; z-index: 10000 !important"
                >
                  <div
                    class="pa-3 border-b d-flex align-center"
                    style="background-color: rgba(var(--v-theme-primary), 0.08)"
                  >
                    <v-icon color="primary" class="me-2" size="20"
                      >mdi-cog-sync-outline</v-icon
                    >
                    <div
                      class="text-caption font-weight-bold"
                      style="color: rgb(var(--v-theme-on-surface))"
                    >
                      {{
                        $i18n.locale == "ar" ? "العمليات العامة" : "General Operations"
                      }}
                    </div>
                  </div>
                  <v-card-text class="pa-1">
                    <v-list density="compact" class="bg-transparent pa-0">
                      <!-- Selected items group -->
                      <template v-if="selectedItems.length > 0">
                        <v-list-subheader class="modern-subheader px-2 mt-1 mb-1">
                          {{
                            $i18n.locale == "ar"
                              ? "العمليات على المحدد"
                              : "Selected Items"
                          }}
                          ({{ selectedItems.length }})
                        </v-list-subheader>

                        <v-list-item
                          v-ripple
                          @click="printReport(true)"
                          class="premium-list-item"
                        >
                          <template #prepend>
                            <v-icon color="secondary" size="18" class="me-2"
                              >mdi-printer-pos-check-outline</v-icon
                            >
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium">
                            {{ $t("print") }} {{ $t("specified") }}
                          </v-list-item-title>
                        </v-list-item>

                        <v-list-item
                          v-ripple
                          v-if="items?.length - selectedItems?.length > 0"
                          @click="printReport(false)"
                          class="premium-list-item"
                        >
                          <template #prepend>
                            <v-icon color="success" size="18" class="me-2"
                              >mdi-printer-pos-remove-outline</v-icon
                            >
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium">
                            {{ $t("print") }} {{ $t("not") }}
                            {{ $t("specified") }}
                          </v-list-item-title>
                        </v-list-item>

                        <v-list-item
                          v-ripple
                          @click="ExportExcel(true)"
                          class="premium-list-item"
                        >
                          <template #prepend>
                            <v-icon color="primary" size="18" class="me-2"
                              >mdi-file-excel-outline</v-icon
                            >
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium">
                            {{ $t("export_excel") }} {{ $t("specified") }}
                          </v-list-item-title>
                        </v-list-item>

                        <v-list-item
                          v-ripple
                          v-if="items?.length - selectedItems?.length > 0"
                          @click="ExportExcel(false)"
                          class="premium-list-item"
                        >
                          <template #prepend>
                            <v-icon color="secondary" size="18" class="me-2"
                              >mdi-file-excel-box</v-icon
                            >
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium">
                            {{ $t("export_excel") }} {{ $t("not") }}
                            {{ $t("specified") }}
                          </v-list-item-title>
                        </v-list-item>
                      </template>

                      <!-- All items group -->
                      <v-list-subheader class="modern-subheader px-2 mt-2 mb-1">
                        {{
                          $i18n.locale == "ar"
                            ? "تقارير وتصدير البيانات"
                            : "Reports & Exports"
                        }}
                      </v-list-subheader>

                      <v-list-item
                        v-ripple
                        @click="printReport"
                        class="premium-list-item"
                      >
                        <template #prepend>
                          <v-icon color="primary" size="18" class="me-2"
                            >mdi-printer-outline</v-icon
                          >
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium">
                          {{ $t("print") }} {{ $t("everyone") }}
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item
                        v-ripple
                        @click="ExportExcel"
                        class="premium-list-item"
                      >
                        <template #prepend>
                          <v-icon color="success" size="18" class="me-2"
                            >mdi-microsoft-excel</v-icon
                          >
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium">
                          {{ $t("export_excel") }} {{ $t("everyone") }}
                        </v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-menu>
            </div>

            <v-spacer></v-spacer>

            <!-- Primary Actions Group (End Side) -->
            <div
              class="d-flex align-center gap-2 flex-wrap justify-end flex-grow-1 flex-md-grow-0"
            >
              <slot name="action"></slot>

              <div v-if="!readOnly" class="d-flex align-center gap-2">
                <div v-if="!isEditing" class="d-flex align-center pa-0 ma-0">
                  <custom-btn type="update" @click="isEditing = true" />
                </div>
                <div v-else class="d-flex align-center gap-2 pa-0 ma-0">
                  <custom-btn
                    type="prev"
                    isIcon
                    @click="click ? (dialog_cancel = true) : (isEditing = false)"
                  />
                  <custom-btn
                    type="save"
                    v-if="click"
                    :click="async () => await methodeAction()"
                    :disabled="!isEditing"
                    class="ma-0"
                  />
                </div>
              </div>
            </div>
          </div>
          <VDivider />
        </template>

        <template v-slot:headers="{ columns }">
          <tr>
            <th
              v-if="showIndex && !loading && !customLoading && data?.length > 0"
              style="width: 10px !important"
              class="v-data-table__th"
            >
              #
            </th>
            <th v-if="showSelect && !is_print" class="v-data-table__th pa-0 ma-0">
              <VCheckbox
                :indeterminate="
                  selectedItems.length > 0 && selectedItems.length < data.length
                "
                :model-value="selectedItems.length === data.length"
                @update:model-value="toggleAll"
                hide-details
                density="compact"
              />
            </th>

            <template v-for="column in columns" :key="column.key">
              <th style="width: auto !important" class="v-data-table__th">
                <span v-if="'type' in column && column.type.name == 'check'">
                  <VCheckbox
                    v-if="!is_print"
                    v-model="column.check"
                    :label="column.title"
                    :model-value="items.every((e) => e[column.key])"
                    :indeterminate="
                      items.some((e) => e[column.key]) &&
                      !items.every((e) => e[column.key])
                    "
                    hide-details
                    @change="
                      checkAll(
                        column.check,
                        column.key,
                        column.type?.trueValue,
                        column?.type?.falseValue,
                        column?.type?.cond
                      )
                    "
                    min-width="max-content"
                  />
                  <template v-else>
                    {{ column.title }}
                  </template>
                </span>

                <span v-else>
                  {{ column.title }}
                </span>
              </th>
            </template>
            <th v-if="canAdd & !is_print" class="v-data-table__th">
              {{ $t("actions") }}
            </th>
          </tr>
        </template>

        <template v-slot:item="{ item, index }">
          <tr :class="{ 'disabled-row': !isEditing }" :key="index">
            <td v-if="showIndex" style="width: 10px !important">
              {{ index + 1 }}
            </td>
            <td class="pa-0" v-if="showSelect && !is_print" style="width: 30px">
              <VCheckbox
                v-if="!is_print"
                v-model="selectedItems"
                :value="item.id"
                hide-details
                density="compact"
                width="30"
              />
            </td>
            <td v-for="val in visibleHeaders" :key="val.key">
              <slot name="item" :item="item" :key="val.key">
                <template v-if="'field' in val">
                  <component :is="is_print ? 'v-sheet' : 'v-lazy'">
                    <field
                      :field="listDataChoices(val.field, item)"
                      v-model="item[val.key]"
                      @update:model-value="
                        (valueItem) => {
                          if (typeof val.field === 'function' && val.field().update) {
                            val.field(item).update();
                          } else if (typeof val.field === 'object' && val.field.update) {
                            val.field.update(item, index, valueItem);
                          }
                        }
                      "
                      :width="
                        typeof val.field === 'function' && val.field(item).width
                          ? val?.field(item)?.width
                          : typeof val.field === 'object' && val.field.width
                          ? val?.field?.width
                          : '250px'
                      "
                    />
                    <!-- :attr="{ resetIcon: false }" -->

                    <!-- :attr="{...val.field,add:false}" -->
                  </component>
                </template>
                <span v-else-if="typeof item[val.key] === 'boolean'">
                  <Checked :val="item[val.key]" />
                </span>
                <span v-else>
                  {{ item[val.key] }}
                </span>
              </slot>
            </td>
            <td v-if="canAdd & !is_print" style="width: 110px">
              <div class="d-flex align-center justify-center gap-1">
                <custom-btn
                  v-if="index === data.length - 1"
                  type="add"
                  isIcon
                  variant="tonal"
                  class="row-action-btn"
                  @click="addRowAfter(index)"
                />
                <custom-btn
                  v-if="canRemove"
                  type="del"
                  icon="mdi-minus"
                  isIcon
                  variant="tonal"
                  class="row-action-btn"
                  @click="deleteRow(index)"
                />
              </div>
            </td>
          </tr>
        </template>
      </VDataTableVirtual>
    </VForm>

    <VSheet>
      <slot name="bottom" />
    </VSheet>
  </VCard>

  <confirm-dialog
    v-model="dialog_cancel"
    type="warning"
    :confirmBtn="cancelEdit"
    message="هل تريد تجاهل التغيرات في البيانات  ؟"
  />
</template>
<script>
import shared from "external-components";

import { VCheckbox } from "vuetify/components";
import { state } from "@/../src/store/state";
import { VLazy } from "vuetify/components";
import { VSheet } from "vuetify/components";
import _ from "lodash";
import NotFound from "../../other/NotFound.vue";
import Checked from "../../other/Checked.vue";

export default {
  components: {
    VCheckbox,
    VLazy,
    VSheet,
    NotFound,
    Checked,
  },
  props: {
    readOnly: {
      type: Boolean,
      default: false,
    },
    itemValue: {
      type: String,
      default() {
        return "id";
      },
    },
    height: {
      type: String,
    },
    top: {
      type: Boolean,
      default: true,
    },

    showSelect: {
      type: Boolean,
      default() {
        return false;
      },
    },
    canAdd: {
      type: Boolean,
      default() {
        return false;
      },
    },
    canRemove: {
      type: Boolean,
      default() {
        return true;
      },
    },
    customLoading: {
      type: Boolean,
      default() {
        return false;
      },
    },
    items: Array,
    headers: {
      type: Array,
      required: true,
    },

    getData: Function,
    click: { type: [Function, Boolean], default: false },

    showTop: {
      type: Boolean,
      default() {
        return true;
      },
    },
    showIndex: {
      type: Boolean,
      default() {
        return false;
      },
    },
    canSearch: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      sortBy: [],
      copy_headers: [],
      selectedItems: [],

      params: {},

      selectedRow: null,

      loading: false,
      is_print: false,
      isEditing: false,
      dialog_cange_data: false,
      dialog_cancel: false,

      is_prent_select: undefined,
      search: undefined,
      copy_items: [],

      status_cahnge_items: false,
      autolist_data: {},
    };
  },
  created() {
    this.copy_headers = [...this.headers];
    this.change_status_headers();

    // if (this.getData()) this.fetchData();
  },
  methods: {
    listDataChoices(field_data, item) {
      let field = typeof field_data === "function" ? field_data(item) : field_data;
      return field;

      // if (field?.name_list) {
      //   const name_list = field.name_list;
      //   if (this.autolist_data[name_list]?.status) {
      //      field.objects = this.autolist_data[name_list].list;
      //   } else {
      //     this.autolist_data[name_list]={}
      //     this.autolist_data[name_list].status = true;
      //     this.autolist_data[name_list].list =[]

      //     this.autolist_data[name_list].list = await dataList()[
      //       name_list
      //     ].method();
      //     field.objects = this.autolist_data[name_list].list;
      //   }
      //   }

      return field;
    },
    async cancelEdit() {
      // this.items.splice(0, this.items.length);
      // const list = _.cloneDeep(this.copy_items);
      // list.forEach((e) => this.items.push(e));

      await this.getData();
      this.isEditing = false;
    },
    async methodeAction() {
      const { valid } = await this.$refs.form.validate();

      if (valid && this.click) {
        await this.click();

        this.copy_items.splice(0, this.copy_items.length);
        const list = _.cloneDeep(this.items);
        list.forEach((e) => this.copy_items.push(e));

        this.isEditing = false;
      }
    },
    handleFieldUpdate(method, val, index) {
      method(val, index);
      // this.attr[fieldName]?.update?.(value);
    },
    async addRowAfter(index) {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        var newRow = {};
        this.copy_headers.map(
          (e) => (newRow[e.key] = e?.field?.type === "BooleanField" ? false : null)
        );

        if (index === null) {
          // إضافة صف جديد في البداية إذا لم يتم تحديد صف
          this.items.push(newRow);
        } else {
          // إضافة صف جديد بعد الصف المحدد
          this.items.splice(index + 1, 0, newRow);
        }
      }
    },
    deleteRow(index) {
      this.items.splice(index, 1);
    },
    reorderFields() {
      // إعادة ترتيب الحقول وضبط `index`
      this.items.sort((a, b) => a.index - b.index);
      this.items.forEach((item, i) => {
        item.index = i + 1;
      });
    },
    toggleAll(value) {
      this.selectedItems = value ? this.data.map((item) => item.id) : [];
    },
    checkAll(val, head, true_value = true, false_value = false, condition = []) {
      if (val) condition.map((cond) => this.data.filter((item) => (item[cond] = false)));

      this.items.map((e) => (e[head] = val ? true_value : false_value));
    },
    ExportExcel(selected = undefined) {
      const title =
        this.$i18n.locale == "ar"
          ? this.$route?.matched?.find((e) => e.name == this.$route.name).props?.default
              ?.name_ar
          : this.$route?.matched?.find((e) => e.name == this.$route.name).props?.default
              ?.name_en;

      var items = [];

      if (selected === true)
        items = this.data.filter((e) => this.selectedItems.includes(e.id));
      else if (selected === false)
        items = this.data.filter((e) => !this.selectedItems.includes(e.id));
      else items = this.data;

      if (items.length > 0)
        shared.ExportToExcel(
          this.visibleHeaders
            .filter((e) => e.type != "img" && e.key != "actions")
            .map((e) => {
              return { header: e.title, key: e.key };
            }),
          items,
          title || ""
        );
      else this.$snack("empty");
    },

    change_status_headers() {
      this.copy_headers
        .filter((e) => e.show == undefined)
        .map((r) => {
          r.show = true;
        });
    },

    async fetchData() {
      try {
        this.loading = true;

        await this.getData().catch(() => {});

        // this.copy_items = _.cloneDeep(this.items);
      } finally {
        this.loading = false;
      }
    },

    // الطباعة
    printReport(parent_select = undefined) {
      this.is_print = true;
      this.is_prent_select = parent_select;
      state.print = true;
      setTimeout(() => {
        const printContent = this.$refs.report.$el.innerHTML;
        document.getElementById("printView").style.display = "block";
        document.getElementById("printView").innerHTML = printContent;
        document.getElementById("appViewId").style.display = "none";
        document.getElementById("vDataTable").style.height = "auto";
        window.print();
        document.getElementById("printView").innerHTML = "";
        document.getElementById("printView").style.display = "none";
        document.getElementById("appViewId").style.display = "block";
        document.getElementById("vDataTable").style.height = "78vh";
        this.is_print = false;
        this.is_prent_select = undefined;
        state.print = false;
      }, 100);
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
  },
  computed: {
    data() {
      if (this.items)
        if (this.items.length > 0 && !this.status_cahnge_items) {
          this.status_cahnge_items = true;
        }
      if (this.is_prent_select == true)
        return this.items.filter((item) => this.selectedItems.includes(item.id));
      if (this.is_prent_select == false)
        return this.items.filter((item) => !this.selectedItems.includes(item.id));
      else return this.items;
    },

    visibleHeaders() {
      if (this.is_print)
        return this.copy_headers.filter(
          (header) => header.show && header.key != "actions"
        );

      return this.copy_headers.filter((header) => header.show);
    },
  },
  watch: {
    status_cahnge_items(value) {
      if (value) {
        this.copy_items.splice(0, this.copy_items.length);
        const list = _.cloneDeep(this.items);
        list.forEach((e) => this.copy_items.push(e));
      }
    },
    headers() {
      this.copy_headers = this.headers;
      this.change_status_headers();
    },
    selectedItems(item) {
      if (item.length > 0) {
        const item = this.copy_headers.find((e) => e.key == "actions");
        if (item) item.show = false;
      } else {
        const item = this.copy_headers.find((e) => e.key == "actions");
        if (item) item.show = true;
      }
    },
  },
};
</script>
<style scoped>
.premium-list-item {
  transition: all 0.15s ease;
  margin: 2px 6px !important;
  border-radius: 6px !important;
  min-height: 34px !important;
  padding: 0 8px !important;
}
.premium-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05) !important;
}
.modern-subheader {
  font-size: 0.65rem !important;
  text-transform: uppercase;
  font-weight: 800;
  color: rgb(var(--v-theme-on-surface));
  display: flex;
  align-items: center;
}
.modern-subheader::after {
  content: "";
  flex: 1;
  height: 1px;
  background: rgba(var(--v-theme-on-surface), 0.05);
  margin-left: 8px;
}
.hover-row-bg {
  transition: background-color 0.2s ease-in-out !important;
}
.hover-row-bg:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.02) !important;
}
:deep(.v-data-table__wrapper) {
  overflow-x: auto !important;
}
:deep(.v-data-table-rows-no-data td) {
  width: 100% !important;
}
:deep(tr[style*="height: 0px"] td) {
  padding: 0 !important;
  border: none !important;
}
</style>
