<template>
  <div>
    <VRow>
      <custom-btn
        type="other"
        label="حفظ الصلاحيات كملف json"
        class="ma-5"
        :click="saveToJson"
      />
      <custom-btn
        type="other"
        label="مزامنه الصلاحيات المرتبطة"
        class="ma-5"
        :click="syncPermission"
      />
    </VRow>

    <v-tabs v-model="tab" bg-color="primary">
      <v-tab :value="0">الشاشات</v-tab>
      <v-tab :value="1">الانظمة</v-tab>
    </v-tabs>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item :value="0">
        <VCol>
          <VAutocomplete
            v-model="fk_default_system"
            :items="itemsSys"
            item-value="id"
            item-title="name_ar"
            prepend-inner-icon="mdi-open-in-app"
            density="compact"
            variant="outlined"
            class="mb-2"
            @update:modelValue="getData()"
          />

          <custom-btn
            v-if="fk_default_system"
            type="add"
            :click="
              () => (
                (dialog = true), (data.fk_default_system = fk_default_system), resetForm()
              )
            "
            width="100%"
          />
          <div style="overflow: scroll">
            <VTreeview
              v-model:actived="active"
              v-model:opened="open"
              :items="items.length > 0 ? items : []"
              item-title="name_ar"
              item-value="id"
              color="primary"
              activatable
            >
              <template v-slot:title="{ item }">
                <VLazy>
                  <VRow>
                    <VCol
                      cols="8"
                      class="treeview-title align-center justify-center row"
                      :style="item.children ? 'font-weight:bold' : ''"
                      @mouseover="hover_item = item.id"
                      @mouseleave="hover_item = null"
                      draggable="true"
                      @dragstart="onDragStart(item)"
                      @dragover.prevent
                      @drop="onDrop(item)"
                    >
                      <VIcon icon="mdi-drag" />
                      <span>{{ item.name_ar }}</span>
                      <VBtn
                        v-bind="activatorProps"
                        v-if="hover_item === item.id"
                        icon
                        @click.stop="
                          (data.fk_parent_screen = item.id),
                            (dialog = true),
                            (data.fk_default_system = fk_default_system),
                            resetForm()
                        "
                        size="20"
                        class="ms-4 mb-2"
                        v-tooltip="'إضافة'"
                      >
                        <VIcon size="15" icon="mdi-plus" />
                      </VBtn>

                      <VBtn
                        v-if="hover_item === item.id"
                        icon
                        size="20"
                        class="ms-4 mb-2"
                        @click.stop="editItem(item)"
                        v-tooltip="'تعديل'"
                      >
                        <VIcon size="15" icon="mdi-pencil" />
                      </VBtn>

                      <VBtn
                        v-if="hover_item === item.id"
                        icon
                        size="20"
                        class="ms-4 mb-2"
                        @click.stop="(del_dialog = true), (data.id = item.id)"
                        v-tooltip="'حذف'"
                      >
                        <VIcon size="15" icon="mdi-trash-can-outline" />
                      </VBtn>
                      <VBtn
                        v-if="hover_item === item.id && item.screen_type !== 3"
                        icon
                        size="20"
                        class="ms-4 mb-2"
                        @click.stop="openDialogPermssions(item)"
                        v-tooltip="'علاقات الشاشة'"
                      >
                        <VIcon size="15" icon="mdi-relation-one-or-many-to-many" />
                      </VBtn>
                    </VCol>
                    <VCol>
                      <VTextField
                        v-model="item.order_in_default_system"
                        hide-details
                        style="width: 100px; font-size: 5"
                        class="mb-5"
                        variant="outlined"
                      />
                    </VCol>
                    <VBtn @click="updateOrder(item.id, item.order_in_default_system)">
                      حفظ
                    </VBtn>
                  </VRow>
                </VLazy>
              </template>
            </VTreeview>
          </div>
        </VCol>
      </v-tabs-window-item>
      <v-tabs-window-item :value="1">
        <add-system v-model="drawer" :data="data_sys" :getData="getDataSys" />
        <custom-data-table
          :="{
            headers: headers_sys,
            items: itemsSys,
            getData: getDataSys,
            create: () => (drawer = true),
            delItem: 'screens/systems/',
            editItem: editItemSys,
            pagination: false,
          }"
        />
      </v-tabs-window-item>
    </v-tabs-window>
  </div>

  <v-dialog v-model="dialog">
    <v-card title="الشاشة">
      <VCardTitle>
        <!-- <pre dir="ltr">
          {{ dataPer }}</pre> -->
        <VBtn
          class="ms-4 mb-2"
          @click.stop="copyToClipboard(data)"
          text="نسخ الكل"
          append-icon="mdi-content-copy"
        >
        </VBtn>
        <v-expansion-panels>
          <v-expansion-panel title="اضافة JSON">
            <v-expansion-panel-text>
              <VCard>
                <VCardText>
                  <custom-text-note v-model="jsonData" :rows="10" />
                </VCardText>
                <VCardActions>
                  <custom-btn type="add" @click="saveData(jsonData)" />
                </VCardActions>
              </VCard> </v-expansion-panel-text></v-expansion-panel
        ></v-expansion-panels>

        <VForm ref="form_1">
          <!-- <VCheckbox v-model="data.is_active" label="نشط" />
          <custom-text-field
            v-model="data.name_ar"
            label="اسم الشاشة عربي"
            :rules="[$required]"
          />
          <custom-text-field
            v-model="data.name_en"
            label="اسم الشاشة انجليزي"
            :rules="[$required, $max_length(255)]"
          />

          <v-locale-provider>
            <custom-text-field
              v-model="data.route"
              label="اسم الرابط"
              :rules="[$max_length(255)]"
            />
            <custom-text-field
              v-model="data.path"
              label="الرابط"
              :rules="[$max_length(255)]"
            />
            <custom-text-field
              v-model="data.component"
              label="مسار الشاشة"
              :rules="[$max_length(255)]"
            />
          </v-locale-provider>
          <custom-text-field
            v-model="data.icon"
            label="الايقونة"
            :rules="[$max_length(100)]"
          />
          <custom-text-field
            v-model="data.back_end_link"
            label="back_end_link"
            :rules="[$max_length(255)]"
          />
          <custom-text-field
            v-model="data.view"
            label="view"
            :rules="[$max_length(200)]"
          />

          <auto-list v-model="data.fk_parent_screen" name="parent_screen" />

          <auto-list
            v-model="data.screen_type"
            name="ScreenTypeChoices"
            :rules="[$required]"
          />
          <VCol>
            <VAutocomplete
              v-model="data.type_of_screen"
              :items="items_type_of_screen"
              item-value="id"
              prepend-inner-icon="mdi-open-in-app"
              item-title="name"
              variant="outlined"
              density="compact"
              label="الظهور في الشاشة"
            />
          </VCol>
          <VCol>
            <VAutocomplete
              v-model="fk_default_system"
              :items="itemsSys"
              item-value="id"
              item-title="name_ar"
              prepend-inner-icon="mdi-open-in-app"
              density="compact"
              variant="outlined"
              class="mb-2"
              label="النظام"
            />
          </VCol>

          <custom-text-field
            v-model="data.order_in_default_system"
            label="الترتيب  في العرض"
            type="number"
            :rules="[$required]"
          /> -->

          <!-- <pre dir="ltr"> {{dataPer.permissions.id }}</pre> -->

          <VDivider />
          <v-row class="pt-5">
            <fields
              :data="data"
              :fields="fields"
              :attr="{
                fk_default_system: {
                  objects: itemsSys,
                  cols: 3,
                },
                name_ar: {
                  cols: 3,
                },
                name_en: {
                  cols: 3,
                },
                route: {
                  cols: 3,
                },
                path: {
                  cols: 3,
                },
                component: {
                  cols: 3,
                },
                back_end_link: {
                  cols: 3,
                },
                fk_parent_screen: {
                  cols: 3,
                },
                screen_type: {
                  cols: 3,
                },
                icon: {
                  cols: 3,
                },
                type_of_screen: {
                  cols: 3,
                },
                is_active: {
                  cols: 1,
                },
                is_report: {
                  cols: 1,
                },
                for_admin: {
                  cols: 1,
                },
                for_ministry: {
                  cols: 1,
                },
                for_governorate: {
                  cols: 1,
                },
                for_directorate: {
                  cols: 1,
                },
                for_region: {
                  cols: 1,
                },
                for_company: {
                  cols: 1,
                },
                for_college: {
                  cols: 1,
                },

                order_in_default_system: {
                  cols: 3,
                },
                view: {
                  cols: 3,
                },
              }"
            />
          </v-row>
          <v-expansion-panels>
            <v-expansion-panel title="التعليمات">
              <v-expansion-panel-text>
                <QuillEditor
                  v-model:content="data.json_notes"
                  toolbar="full"
                  content-type="html"
                  dense="compact"
                  style="height: 300px"
                /> </v-expansion-panel-text></v-expansion-panel
          ></v-expansion-panels>
          <v-expansion-panels>
            <!-- <v-expansion-panel title="الصلاحيات">
              <v-expansion-panel-text>
                <VRow>
                  <VCol cols="4">
                    <auto-list
                      v-model="dataPer.fk_screen_permission__operation_type"
                      name="OperationTypeChoices"
                      hide-details
                      return-object
                    />

                    <auto-list
                      v-model="
                        dataPer.fk_related_permission__fk_screen__fk_default_system
                      "
                      name="system"
                      hide-details
                      :objects="systems"
                      return-object
                    />

                    <auto-list
                      v-model="dataPer.fk_related_permission__fk_screen"
                      name="screen_by_system"
                      :param="
                        dataPer
                          ?.fk_related_permission__fk_screen__fk_default_system
                          ?.id
                      "
                      hide-details
                      return-object
                    />
                    <auto-list
                      v-model="dataPer.fk_related_permission"
                      name="permissionsByScreen"
                      :param="dataPer?.fk_related_permission__fk_screen?.id"
                      hide-details
                      return-object
                    />
                  </VCol>
                  <VCol cols="1">
                    <VBtn
                      icon="mdi-arrow-left-bold-circle-outline"
                      @click="
                        () => {
                          if (
                            dataPer.fk_screen_permission__operation_type &&
                            dataPer.fk_related_permission__fk_screen__fk_default_system &&
                            dataPer.fk_related_permission__fk_screen &&
                            dataPer.fk_related_permission
                          ) {
                            items_permissions.push({
                              fk_screen_permission__operation_type:
                                dataPer.fk_screen_permission__operation_type.id,
                              fk_screen_permission__operation_type__display:
                                dataPer.fk_screen_permission__operation_type
                                  .name,

                              fk_related_permission__fk_screen__fk_default_system:
                                dataPer
                                  .fk_related_permission__fk_screen__fk_default_system
                                  .id,
                              fk_related_permission__fk_screen__fk_default_system__name_ar:
                                dataPer
                                  .fk_related_permission__fk_screen__fk_default_system
                                  .name_ar,

                              fk_related_permission__fk_screen:
                                dataPer.fk_related_permission__fk_screen.id,
                              fk_related_permission__fk_screen__name_er:
                                dataPer.fk_related_permission__fk_screen
                                  .name_ar,

                              fk_related_permission:
                                dataPer.fk_related_permission.id,
                              fk_related_permission__operation_type__display:
                                dataPer.fk_related_permission
                                  .operation_type__display,
                            });
                            dataPer = {};
                          } else {
                            $alert('errorData', {
                              message: 'يجب ملئ جميع الحقول',
                            });
                          }
                        }
                      "
                    />
                  </VCol>
                  <VCol cols="7">
                    <v-data-table-virtual
                      :headers="headers_permissions"
                      :items="items_permissions"
                      height="400"
                      fixed-header
                    >
                      <template v-slot:item.actions="{ index }">
                        <VIcon
                          size="20"
                          icon="mdi-trash-can"
                          @click="items_permissions.splice(index, 1)"
                        />
                      </template>
                    </v-data-table-virtual>
                  </VCol>
                </VRow>
              </v-expansion-panel-text>
            </v-expansion-panel> -->
          </v-expansion-panels>
        </VForm>

        <fieldset
          class="border-dashed ma-2 ps-2"
          style="border: 1px solid rgba(0, 0, 0, 0.1)"
        >
          <legend class="text-primary">الحقول</legend>
          <custom-text-field
            v-model="data.json_fields.main_model"
            label="المودل الرئيسي"
          />
          <VForm ref="form_2">
            <VDataTableVirtual
              :group-by="groupBy"
              :headers="headers"
              :items="data.json_fields.fields"
            >
              <template v-slot:top>
                <custom-btn type="add" @click="addRowAfter(null)" />
              </template>

              <template v-slot:[`item.actions`]="{ item, index }">
                <VBtn
                  icon
                  @click="addRowAfter(index, item.group)"
                  size="20"
                  class="ms-4 mb-2"
                >
                  <VIcon size="15" icon="mdi-plus" />
                </VBtn>
                <VBtn icon @click="deleteRow(index)" size="20" class="ms-4 mb-2">
                  <VIcon size="15" icon="mdi-minus" />
                </VBtn>
              </template>

              <template v-slot:[`item.index`]="{ item }">
                <v-text-field v-model="item.index" @change="onIndexChange(item)" />
              </template>

              <template v-slot:[`item.name`]="{ item }">
                <custom-text-field v-model="item.name" :rules="[$required]" />
              </template>

              <template v-slot:[`item.icon`]="{ item }">
                <custom-text-field v-model="item.icon" />
              </template>
              <template v-slot:[`item.model`]="{ item }">
                <custom-text-field v-model="item.model" />
              </template>
              <template v-slot:[`item.width`]="{ item }">
                <custom-text-field v-model="item.width" />
              </template>
              <template v-slot:[`item.group`]="{ item }">
                <custom-text-field v-model="item.group" />
              </template>

              <template v-slot:[`item.name_list`]="{ item }">
                <custom-text-field v-model="item.name_list" />
              </template>
            </VDataTableVirtual>
          </VForm>
        </fieldset>
      </VCardTitle>

      <v-card-actions>
        <custom-btn type="add" :click="saveData" />
        <custom-btn v-if="data.id" type="update" :click="updateData" />

        <custom-btn type="cancel" :click="() => (dialog = false)" />
      </v-card-actions>
    </v-card>
  </v-dialog>

  <custom-dialog
    v-model="dialog_relation"
    title="علاقات الشاشات"
    width="1200"
    height="90svh"
  >
    <div class="align-end text-end">
      <VBtn
        class="ms-4 text-end"
        @click.stop="copyToClipboard(items_permissions)"
        text="نسخ الكل"
        variant="tonal"
        append-icon="mdi-content-copy"
      >
      </VBtn>
    </div>

    <VRow>
      <VCol cols="12" md="3" lg="4">
        <auto-list
          v-model="dataPer.fk_screen_permission__operation_type"
          name="OperationTypeChoices"
          hide-details
          return-object
        />

        <auto-list
          v-model="dataPer.fk_related_permission__fk_screen__fk_default_system"
          name="system"
          hide-details
          :objects="systems"
          return-object
        />

        <auto-list
          v-model="dataPer.fk_related_permission__fk_screen"
          name="screen_by_system"
          :param="dataPer?.fk_related_permission__fk_screen__fk_default_system?.id"
          hide-details
          return-object
        />
        <auto-list
          v-model="dataPer.fk_related_permission"
          name="permissionsByScreen"
          :param="dataPer?.fk_related_permission__fk_screen?.id"
          hide-details
          return-object
        />
      </VCol>
      <VCol cols="12" md="1" lg="1" align="center">
        <VBtn
          :icon="
            $vuetify.display.mobile
              ? 'mdi-arrow-down-bold-circle-outline'
              : 'mdi-arrow-left-bold-circle-outline'
          "
          @click="addToRelation(dataPer)"
        />
      </VCol>
      <VCol cols="12" md="7" lg="7">
        <v-expansion-panels density="compact">
          <v-expansion-panel title="اضافة JSON" density="compact">
            <v-expansion-panel-text>
              <custom-text-note v-model="jsonData" />
              <custom-btn
                type="add"
                @click="addToRelation(jsonData)"
              /> </v-expansion-panel-text></v-expansion-panel
        ></v-expansion-panels>

        <v-data-table-virtual
          :headers="headers_permissions"
          :items="items_permissions"
          height="100%"
        >
          <template v-slot:item.actions="{ item, index }">
            <VIcon
              size="20"
              icon="mdi-trash-can"
              color="red"
              @click="items_permissions.splice(index, 1)"
            />

            <VIcon
              size="20"
              icon="mdi-content-copy"
              color="green"
              @click="copyToClipboard(item)"
            />
          </template>
        </v-data-table-virtual>
      </VCol>
    </VRow>
    <VCardActions> </VCardActions>
    <template #actions>
      <custom-btn type="update" :click="updatePermssions" width="100%" />
    </template>
  </custom-dialog>
  <delete-dialog v-model="del_dialog" @confirmDelete="deleteData" />
  <VSnackbar v-model="copied" timeout="2000" color="grey-darken-4" location="top">
    تم نسخ التفاصيل الى الحافظة !
  </VSnackbar>
</template>
<script>
import AddSystem from "./AddSystem.vue";
import { QuillEditor } from "@vueup/vue-quill";

export default {
  components: { AddSystem, QuillEditor },

  data() {
    return {
      jsonData: undefined,
      tab: 0,
      expansion: false,
      copied: false,
      headers_permissions: [
        {
          title: "نوع الصلاحية",
          key: "fk_screen_permission__operation_type__display",
        },
        {
          title: "النظام",
          key: "fk_related_permission__fk_screen__fk_default_system__name_ar",
        },
        { title: "الشاشة", key: "fk_related_permission__fk_screen__name_er" },
        {
          title: "الصلاحية",
          key: "fk_related_permission",
        },
        {
          title: "الصلاحيات",
          key: "fk_related_permission__operation_type__display",
        },
        { title: "actions", key: "actions" },
      ],

      fk_default_system: undefined,

      data: {
        is_active: true,
        json_fields: {
          fields: [],
          main_model: "",
        },
      },
      data_sys: {},
      itemsSys: [],
      items: [],
      items_type_of_screen: [],

      dataPer: [],

      items_permissions: [],

      drawer: false,
      del_dialog: false,
      dialog_relation: false,

      url: "screens/systems/",

      groupBy: [
        {
          key: "group",
          order: "desc",
        },
      ],

      headers: [
        { title: "الرقم", key: "index", sortable: false },
        { title: "الاسم", key: "name", sortable: false },
        { title: "الأيقونة", key: "icon", sortable: false },
        { title: "model", key: "model", sortable: false },
        { title: "المجموعة", key: "group", sortable: false },
        { title: "العرض", key: "width", sortable: false },
        { title: "اسم ال Autocomplete ", key: "name_list", sortable: false },
        { title: "الإجراءات", key: "actions", sortable: false },
      ],

      draggedItem: null,

      systems: [],
      active: [],
      open: [],
      fields: [
        {
          name: "name_ar",
          type: "CharField",
          null: false,
          label_ar: "اسم الشاشة عربي",
          label_en: "Screen Name Arabic",
          max_length: 255,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "name_en",
          type: "CharField",
          null: false,
          label_ar: "اسم الشاشة انجليزي",
          label_en: "Screen Name English",
          max_length: 255,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "component",
          type: "CharField",
          null: true,
          label_ar: "اسم الشاشة Component",
          label_en: "Component",
          max_length: 255,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "fk_parent_screen",
          type: "ForeignKey",
          null: true,
          label_ar: "اسم الشاشة الأب",
          label_en: "Parent Screen",
          max_length: null,
          default: null,
          icon: null,
          group: null,
          name_list: "parent_screen",
          width: null,
          model: null,
        },
        {
          name: "screen_type",
          type: "PositiveSmallIntegerField",
          null: false,
          label_ar: "نوع الشاشة",
          label_en: "Screen Type",
          max_length: null,
          default: null,
          max_value: 32767,
          min_value: 0,
          icon: null,
          group: null,
          name_list: "ScreenTypeChoices",
          width: null,
          model: null,
        },
        {
          name: "route",
          type: "CharField",
          null: true,
          label_ar: "الروتر",
          label_en: "Route",
          max_length: 255,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "path",
          type: "CharField",
          null: true,
          label_ar: "المسار",
          label_en: "path",
          max_length: 255,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },

        {
          name: "back_end_link",
          type: "CharField",
          null: true,
          label_ar: "Backend Link",
          label_en: "Backend Link",
          max_length: 255,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },

        {
          name: "icon",
          type: "CharField",
          null: true,
          label_ar: "الايقونة",
          label_en: "Icon",
          max_length: 100,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "type_of_screen",
          type: "PositiveSmallIntegerField",
          null: true,
          label_ar: "نوع العرض",
          label_en: "Type Of Display",
          max_length: null,
          default: null,
          max_value: 32767,
          min_value: 0,
          icon: null,
          group: null,
          name_list: "TypeOfDisplayChoices",
          width: null,
          model: null,
        },
        {
          name: "fk_default_system",
          type: "ForeignKey",
          null: false,
          label_ar: "النظام الافتراضي",
          label_en: "Default System",
          max_length: null,
          default: null,
          icon: null,
          group: null,
          name_list: "System",
          width: null,
          model: null,
        },
        {
          name: "order_in_default_system",
          type: "PositiveSmallIntegerField",
          null: false,
          label_ar: "ترتيب الشاشة",
          label_en: "Order in Default System",
          max_length: null,
          default: null,
          max_value: 32767,
          min_value: 0,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "view",
          type: "CharField",
          null: true,
          label_ar: "استعراض",
          label_en: "View",
          max_length: 200,
          default: null,
          min_length: null,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "has_sync_push",
          type: "BooleanField",
          null: false,
          label_ar: "مزامنة البيانات مع البوابة",
          label_en: "مزامنة البيانات مع البوابة",
          max_length: null,
          default: true,
          icon: null,
          group: null,
          name_list: null,
          width: 1,
          model: null,
        },
        {
          name: "has_sync_pull",
          type: "BooleanField",
          null: false,
          label_ar: "جلب البيانات من البوابة",
          label_en: "جلب البيانات من البوابة",
          max_length: null,
          default: true,
          icon: null,
          group: null,
          name_list: null,
          width: 1,
          model: null,
        },
        {
          name: "is_active",
          type: "BooleanField",
          null: false,
          label_ar: "هل مفعل",
          label_en: "Is Active",
          max_length: null,
          default: true,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "is_report",
          type: "BooleanField",
          null: false,
          label_ar: "هل تقرير",
          label_en: "Is Report",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "for_admin",
          type: "BooleanField",
          null: false,
          label_ar: "أدارة عامة",
          label_en: "For Admin",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "for_ministry",
          type: "BooleanField",
          null: false,
          label_ar: "وزارة",
          label_en: "For Ministry",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "for_governorate",
          type: "BooleanField",
          null: false,
          label_ar: "محافظة",
          label_en: "For Governorate ",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "for_directorate",
          type: "BooleanField",
          null: false,
          label_ar: "مديرية",
          label_en: "For Directorate ",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "for_region",
          type: "BooleanField",
          null: false,
          label_ar: "منطقة",
          label_en: "For Region",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },

        {
          name: "for_company",
          type: "BooleanField",
          null: false,
          label_ar: "مدرسة",
          label_en: "For Company",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
        {
          name: "for_college",
          type: "BooleanField",
          null: false,
          label_ar: "فرع",
          label_en: "For college",
          max_length: null,
          default: false,
          icon: null,
          group: null,
          name_list: null,
          width: null,
          model: null,
        },
      ],
      permissions: [],
      permissionTypes: [
        { id: 1, label: "عرض", status: false, permissions: [] },
        { id: 2, label: "اضافة", status: false, permissions: [] },
        { id: 3, label: "تعديل", status: false, permissions: [] },
        { id: 4, label: "حذف", status: false, permissions: [] },
        { id: 5, label: "حذف اجباري", status: false, permissions: [] },
        { id: 6, label: "تصدير", status: false, permissions: [] },
        { id: 7, label: "استيراد", status: false, permissions: [] },
        { id: 8, label: "عرض المحذوفات", status: false, permissions: [] },
        { id: 9, label: "استعادة", status: false, permissions: [] },
      ],

      hover_item: undefined,

      dialog: false,
    };
  },
  created() {
    this.resetForm();
    this.getDataSys();
    this.getTypeOfScreen();
    this.getData();
    // this.getFields();
    this.getSystems();
    this.getPermissions();
  },
  methods: {
    addToRelation(item) {
      if (typeof item == "string") {
        const convertJson = JSON.parse(item);
        if (Array.isArray(convertJson))
          convertJson.forEach((e) => {
            this.addRealtion(e);
          });
        else if (typeof convertJson === "object") this.addRealtion(convertJson);
      } else {
        this.addRealtion(item);
      }
    },
    addRealtion(dataPer) {
      if (
        dataPer.fk_screen_permission__operation_type &&
        dataPer.fk_related_permission__fk_screen__fk_default_system &&
        dataPer.fk_related_permission__fk_screen &&
        dataPer.fk_related_permission
      ) {
        this.items_permissions.push({
          fk_screen_permission__operation_type:
            dataPer.fk_screen_permission__operation_type.id ||
            dataPer.fk_screen_permission__operation_type,

          fk_screen_permission__operation_type__display:
            dataPer.fk_screen_permission__operation_type.name ||
            dataPer.fk_screen_permission__operation_type__display,

          fk_related_permission__fk_screen__fk_default_system:
            dataPer.fk_related_permission__fk_screen__fk_default_system.id ||
            dataPer.fk_related_permission__fk_screen__fk_default_system,

          fk_related_permission__fk_screen__fk_default_system__name_ar:
            dataPer.fk_related_permission__fk_screen__fk_default_system.name_ar ||
            dataPer.fk_related_permission__fk_screen__fk_default_system__name_ar,

          fk_related_permission__fk_screen:
            dataPer.fk_related_permission__fk_screen.id ||
            dataPer.fk_related_permission__fk_screen,

          fk_related_permission__fk_screen__name_er:
            dataPer.fk_related_permission__fk_screen.name_ar ||
            dataPer.fk_related_permission__fk_screen__name_er,

          fk_related_permission:
            dataPer.fk_related_permission.id || dataPer.fk_related_permission,

          fk_related_permission__operation_type__display:
            dataPer.fk_related_permission.operation_type__display ||
            dataPer.fk_related_permission__operation_type__display,
        });

        this.dataPer = {};
        this.jsonData = undefined;
      } else {
        this.$alert("errorData", {
          message: "يجب ملئ جميع الحقول",
        });
      }
    },
    copyDataRelatedPermission(item) {
      this.data.related_screen_permission = [...item.related_screen_permission];
    },
    async syncPermission() {
      await this.$axios.post("screens/screen/sync-permissions/").then((e) => {
        this.$snack("add", { message: "تمت المزامنه بنجاح " });
      });
    },
    async saveToJson() {
      await this.$axios
        .post("screens/screen/save-related-permissions-json/")
        .then((e) => {
          this.$snack("add");
        });
    },
    async getFields() {
      await this.$axios(`${this.setting.url_field}screen-view/`).then((response) => {
        const res = response.data.data || response.data;
        this.fields = res;
      });
    },
    async getSystems() {
      await this.$axios(`screens/systems/all/`).then((response) => {
        const res = response.data.data || response.data;
        console.log(res, "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx");

        this.systems = res;
      });
    },
    async getPermissions() {
      await this.$axios(`screens/screen-permission/`).then((response) => {
        const res = response.data.data || response.data;
        this.permissions = res;
      });
    },

    onDragStart(item) {
      this.draggedItem = item;
    },
    onDrop(targetItem) {
      if (this.draggedItem && this.draggedItem !== targetItem) {
        this.movedItem(this.items, this.draggedItem, targetItem);
        this.draggedItem = null;
      }
    },
    movedItem(items, draggedItem, targetItem) {
      let draggedParent = null;
      let draggedIndex = null;
      const findAndRemoveItem = (items, parent = null) => {
        for (let i = 0; i < items.length; i++) {
          if (items[i].id === draggedItem.id) {
            draggedParent = parent;
            draggedIndex = i;
            return items.splice(i, 1)[0];
          }
          if (items[i].children) {
            const item = findAndRemoveItem(items[i].children, items[i]);
            if (item) return item;
          }
        }
      };
      const movedItem = findAndRemoveItem(items);

      if (movedItem) {
        // if (targetItem.children) {
        //   targetItem.children.push(movedItem);
        // } else {
        const parentArray = draggedParent ? draggedParent.children : items;
        const targetIndex = parentArray.findIndex((child) => child.id === targetItem.id);
        if (targetIndex !== -1) parentArray.splice(targetIndex, 0, movedItem);

        // }
      }
    },

    async updateIcon(id, icon) {
      await this.$axios
        .patch("screens/screen/" + id + "/", {
          icon: icon,
          fk_default_system: this.fk_default_system,
        })
        .then((e) => {
          this.$snack("update");
        });
    },

    async updateOrder(id, order) {
      await this.$axios
        .patch("screens/screen/" + id + "/", {
          order_in_default_system: order,
          fk_default_system: this.fk_default_system,
        })
        .then((e) => {
          this.$snack("update");
          this.getData();
        });
    },

    async getDataSys(params) {
      return await this.$axios(this.url, params).then((response) => {
        const res = response.data.data || response.data;
        this.itemsSys = res;
      });
    },
    getTypeOfScreen() {
      this.$axios(`${this.setting.url}choices/TypeOfDisplayChoices/`).then((response) => {
        const res = response.data.data || response.data;
        this.items_type_of_screen = res;
      });
    },
    editItem(data) {
      if (data.json_fields === null || !("json_fields" in data))
        data.json_fields = {
          fields: [],
          main_model: "",
        };

      this.data = { ...data };

      this.dialog = true;
    },
    deleteData() {
      this.$axios
        .delete("screens/screen/" + this.data.id + "/")
        .then((response) => this.getData());
    },
    editItemSys(data) {
      this.data_sys = { ...data };
      this.drawer = true;
    },
    resetForm() {
      this.dataPer = {};
      this.items_permissions = [];
      this.data = {
        is_active: true,
        json_fields: {
          main_model: null,
          fields: [],
        },
      };
    },
    async getData() {
      if (this.fk_default_system) {
        const filters = [{ field: "fk_default_system", value: this.fk_default_system }];

        const response = await this.$axios.post("screens/screen/filter/", {
          filters,
        });
        const res = response.data.data || response.data;
        this.items = this.buildTree(res);
      } else this.items = [];
      // const response = await this.$axios("screens/screen/");
    },
    buildTree(data, parentId = 0) {
      if (
        parentId === 0 &&
        data.filter((item) => item.fk_parent_screen === parentId).length === 0
      )
        parentId = null;

      return data
        .filter((item) => item.fk_parent_screen === parentId)
        .map((item) => ({
          ...item,
          children: this.buildTree(data, item.id),
        }));
    },
    openDialogPermssions(data) {
      this.data.id = data.id;
      this.items_permissions = [...data.related_screen_permission];

      this.dialog_relation = true;
    },
    async updatePermssions() {
      const list = this.groupPermissions(this.items_permissions);
      await this.$axios.patch("screens/screen/" + this.data.id + "/", {
        fk_default_system: this.fk_default_system,
        related_premssions: list,
      });
      this.getData();
      this.$alert("update");
    },

    async saveData(items) {
      try {
        if (!items) {
          const { valid } = await this.$refs.form_1.validate();
          if (!valid) return;
        }

        const data = items ? JSON.parse(items) : this.data;

        await this.$axios
          .post("screens/screen/", {
            ...data,
            fk_default_system: this.fk_default_system,
          })
          .then((e) => {
            this.getData();
            this.dialog = false;
            this.$alert("add");
          });
      } catch (error) {
        console.error("Error processing permissions:", error);
      }
    },
    async updateData() {
      const { valid } = await this.$refs.form_1.validate();
      if (valid) {
        const data = { ...this.data };

        delete data.related_screen_permission;

        await this.$axios
          .patch("screens/screen/" + this.data.id + "/", {
            ...data,
            fk_default_system: this.fk_default_system,
          })
          .then((e) => {
            this.getData();
            // this.dialog = false;
            this.$alert("update");
          });
      }
    },

    groupPermissions(permissions) {
      const grouped = {};

      permissions.forEach((p) => {
        const type = p.fk_screen_permission__operation_type;
        if (!grouped[type]) {
          grouped[type] = [];
        }
        grouped[type].push(p.fk_related_permission);
      });

      return Object.entries(grouped).map(([type, ids]) => ({
        type: Number(type),
        permissions: ids,
      }));
    },

    async addRowAfter(index, group = null) {
      const num = index === null ? 1 : index + 2;

      const newRow = {
        index: num,
        name: null,
        icon: null,
        group: group,
      };
      const { valid } = await this.$refs.form_2.validate();
      if (valid)
        if (index === null) {
          // إضافة صف جديد في البداية إذا لم يتم تحديد صف
          this.data.json_fields.fields.push(newRow);
        } else {
          // إضافة صف جديد بعد الصف المحدد
          this.data.json_fields.fields.splice(index + 1, 0, newRow);
        }
      this.reorderFields();
    },
    deleteRow(index) {
      this.data.json_fields.fields.splice(index, 1);
      this.reorderFields();
    },

    reorderFields() {
      // إعادة ترتيب الحقول وضبط `index`
      this.data.json_fields.fields.sort((a, b) => a.index - b.index);
      this.data.json_fields.fields.forEach((item, i) => {
        item.index = i + 1;
      });
    },

    onIndexChange(item) {
      // إعادة الترتيب عند تغيير `index`
      this.reorderFields();
    },

    copyToClipboard(item) {
      const text = JSON.stringify(item, null, 2);
      navigator.clipboard.writeText(text);
      this.copied = true;
    },
  },
  computed: {
    convertDataToJson() {
      return this.data;
    },
    headers_sys() {
      return [
        { title: this.$t("name_ar"), key: "name_ar" },
        { title: this.$t("name_en"), key: "name_en" },
        { title: this.$t("description"), key: "description" },
        { title: "هل هو رئيسي", key: "is_main" },
        { title: "الترتيب", key: "order" },
      ];
    },
  },
  watch: {
    dialog(value) {
      if (!value) this.resetForm();
    },
  },
};
</script>
