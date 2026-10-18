<template>
  <div class="import-excel-root">
    <v-card class="import-card d-flex flex-column" :loading="loading" elevation="0">
      <!-- ── Professional Header ── -->
      <div v-if="!isImportOnly" class="import-header">
        <div class="import-header__brand">
          <div class="import-header__icon">
            <v-icon size="20" color="primary">mdi-microsoft-excel</v-icon>
          </div>
          <div>
            <div class="import-header__title">استيراد بيانات Excel</div>
            <div class="import-header__subtitle">
              اتبع الخطوات لاستيراد البيانات بشكل صحيح
            </div>
          </div>
        </div>

        <div class="steps-track">
          <template
            v-for="(s, i) in [
              { label: 'تحميل القالب', icon: 'mdi-download-outline' },
              { label: 'تعبئة الملف', icon: 'mdi-table-edit' },
              { label: 'رفع ومعالجة', icon: 'mdi-upload-outline' },
            ]"
            :key="i"
          >
            <div
              v-if="i > 0"
              class="steps-track__line"
              :class="{ 'steps-track__line--done': step > i }"
            />
            <div class="steps-track__step">
              <div
                class="steps-track__bubble"
                :class="{
                  'steps-track__bubble--active': step === i + 1,
                  'steps-track__bubble--done': step > i + 1,
                  'steps-track__bubble--pending': step < i + 1,
                }"
              >
                <v-icon v-if="step > i + 1" size="14" color="white">mdi-check</v-icon>
                <v-icon
                  v-else
                  size="14"
                  :color="step === i + 1 ? 'white' : 'grey-lighten-1'"
                  >{{ s.icon }}</v-icon
                >
              </div>
              <div
                class="steps-track__label"
                :class="{
                  'steps-track__label--active': step === i + 1,
                  'steps-track__label--done': step > i + 1,
                }"
              >
                {{ s.label }}
              </div>
            </div>
          </template>
        </div>
      </div>

      <v-divider v-if="!isImportOnly" class="import-header-divider" />

      <!-- ── Content ── -->
      <div class="import-content flex-grow-1">
        <!-- Step 1 -->
        <div v-if="step === 1" class="step-pane">
          <div class="step-empty-state">
            <div class="step-icon-wrap">
              <v-icon size="52" color="primary">mdi-microsoft-excel</v-icon>
            </div>
            <h3 class="step-title">تحميل قالب Excel</h3>
            <p class="step-description">
              اضغط على الزر أدناه للحصول على قالب Excel الجاهز مع الأعمدة المطلوبة.
            </p>
            <v-btn
              v-if="!error"
              color="primary"
              variant="flat"
              size="large"
              prepend-icon="mdi-download-outline"
              class="import-btn-primary"
              @click="downloadTemplate"
              :disabled="loading"
            >
              تحميل القالب
            </v-btn>
            <div v-if="error" class="error-state-block">
              <v-icon color="error" size="28">mdi-alert-circle-outline</v-icon>
              <span class="error-state-text">حدث خطأ أثناء التحميل</span>
              <v-btn
                variant="tonal"
                color="error"
                size="small"
                prepend-icon="mdi-refresh"
                @click="initialData()"
                >إعادة المحاولة</v-btn
              >
            </div>
          </div>
        </div>

        <!-- Step 2: Field Rules -->
        <div v-if="step === 2" class="step-pane step-pane--rules">
          <div v-if="error" class="error-state-block">
            <v-icon color="error" size="36">mdi-alert-circle-outline</v-icon>
            <span class="error-state-text">فشل تحميل قواعد الحقول</span>
            <v-btn
              variant="tonal"
              color="error"
              size="small"
              prepend-icon="mdi-refresh"
              @click="initialData()"
              >إعادة المحاولة</v-btn
            >
          </div>
          <template v-else>
            <div class="s2-header">
              <div class="s2-header__icon">
                <v-icon size="18" color="primary">mdi-table-check</v-icon>
              </div>
              <div>
                <div class="s2-header__title">قواعد تعبئة البيانات</div>
                <div class="s2-header__sub">
                  راجع كل حقل قبل تعبئة الملف — الحقول المميزة بـ * إلزامية
                </div>
              </div>
              <v-chip size="small" color="primary" variant="tonal" class="ms-auto"
                >{{ items.length }} حقل</v-chip
              >
            </div>

            <div class="fields-grid">
              <div
                v-for="(item, index) in items"
                :key="index"
                class="field-rule-card"
                :class="
                  item.rules.some((r) => r === 'لايمكن ان يكون فارغاََ')
                    ? 'field-rule-card--req'
                    : 'field-rule-card--opt'
                "
              >
                <div class="field-rule-card__top-bar" />
                <div class="field-rule-card__head">
                  <span class="field-rule-card__num">{{ index + 1 }}</span>
                  <span class="field-rule-card__name">{{ item?.field?.label_ar }}</span>
                  <v-chip
                    v-if="item.rules.some((r) => r === 'لايمكن ان يكون فارغاََ')"
                    size="x-small"
                    color="error"
                    variant="tonal"
                  >
                    <v-icon start size="9">mdi-asterisk</v-icon>مطلوب
                  </v-chip>
                  <v-chip v-else size="x-small" color="grey" variant="tonal"
                    >اختياري</v-chip
                  >
                </div>
                <div class="field-rule-card__body">
                  <template v-for="(rule, ri) in item.rules" :key="ri">
                    <div v-if="typeof rule === 'object'" class="rule-line">
                      <auto-list
                        v-model="data_list[item?.field?.name]"
                        :name="rule.name_list"
                        :param="
                          item?.field?.param ? data_list[item?.field?.param] : undefined
                        "
                      />
                    </div>
                    <div v-else-if="rule !== 'لايمكن ان يكون فارغاََ'" class="rule-line">
                      <v-icon size="12" color="grey-lighten-1">mdi-circle-small</v-icon>
                      <span>{{ rule }}</span>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Step 3: Upload & Validate -->
        <div v-if="step === 3" class="step-pane step-pane--upload">
          <div class="s2-header">
            <div class="s2-header__icon">
              <v-icon size="18" color="primary">mdi-upload-outline</v-icon>
            </div>
            <div>
              <div class="s2-header__title">رفع الملف المكتمل</div>
              <div class="s2-header__sub">اختر ملف Excel الذي قمت بتعبئته لمعالجته</div>
            </div>
          </div>

          <div
            class="upload-dropzone"
            :class="{ 'upload-dropzone--active': uploadedFile }"
          >
            <div
              class="upload-dropzone__icon-wrap"
              :class="uploadedFile ? 'upload-dropzone__icon-wrap--ok' : ''"
            >
              <v-icon size="40" :color="uploadedFile ? 'success' : 'primary'">
                {{
                  uploadedFile ? "mdi-check-circle-outline" : "mdi-cloud-upload-outline"
                }}
              </v-icon>
            </div>
            <div class="upload-dropzone__texts">
              <div class="upload-dropzone__main">
                {{
                  uploadedFile
                    ? "تم اختيار الملف بنجاح"
                    : "اسحب الملف هنا أو اضغط للاختيار"
                }}
              </div>
              <div class="upload-dropzone__sub">الصيغ المدعومة: .xlsx, .xls فقط</div>
            </div>
            <v-file-input
              v-model="uploadedFile"
              accept=".xlsx,.xls"
              variant="outlined"
              density="comfortable"
              prepend-icon="mdi-file-excel-outline"
              :label="uploadedFile ? 'تغيير الملف' : 'اختر ملفاً'"
              clearable
              hide-details="auto"
              class="upload-dropzone__input"
            />
          </div>

          <div v-if="errors_validata.length > 0" class="val-errors">
            <div class="val-errors__head">
              <div class="val-errors__head-left">
                <v-icon color="error" size="16">mdi-alert-circle</v-icon>
                <span class="val-errors__title">أخطاء التحقق</span>
              </div>
              <v-chip size="small" color="error" variant="tonal"
                >{{ errors_validata.length }} خطأ</v-chip
              >
            </div>
            <div class="val-errors__list">
              <div
                v-for="(item, index) in errors_validata"
                :key="index"
                class="val-errors__row"
              >
                <span class="val-errors__num">{{ index + 1 }}</span>
                <span class="val-errors__msg">{{ item }}</span>
              </div>
            </div>
          </div>

          <div
            v-if="uploadedFile && errors_validata.length === 0 && !loading"
            class="upload-ready"
          >
            <v-icon color="success" size="22">mdi-check-circle</v-icon>
            <div>
              <div class="upload-ready__title">الملف جاهز للمعالجة</div>
              <div class="upload-ready__sub">اضغط "معالجة الملف" للمتابعة</div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Footer ── -->
      <div class="import-footer">
        <div>
          <v-btn
            v-if="step > 1 && !isImportOnly"
            variant="tonal"
            color="primary"
            prepend-icon="mdi-chevron-right"
            class="import-btn-nav"
            @click="step--"
            >السابق</v-btn
          >
        </div>
        <div v-if="!isImportOnly" class="import-footer__dots">
          <span
            v-for="s in 3"
            :key="s"
            class="import-footer__dot"
            :class="{
              'import-footer__dot--active': step === s,
              'import-footer__dot--done': step > s,
            }"
          />
        </div>
        <div>
          <v-btn
            v-if="step < 3"
            color="primary"
            variant="flat"
            append-icon="mdi-chevron-left"
            class="import-btn-nav"
            @click="step++"
            >التالي</v-btn
          >

          <v-btn
            v-if="step === 3 && !error"
            color="primary"
            variant="flat"
            rounded="0"
            prepend-icon="mdi-check"
            :disabled="!uploadedFile || loading"
            :loading="loadinExportToExcel"
            @click.stop="() => processFile()"
            style="border-radius: 0 !important"
            >معالجة الملف
          </v-btn>
          <v-menu v-if="step === 3 && !error && !isImportOnly" location="top">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                color="primary"
                :rounded="0"
                elevation="0"
                :disabled="!uploadedFile || loading"
                style="
                  border-radius: 0 !important;
                  margin: 0px 1px;
                  height: 38px !important;
                "
                icon="mdi-chevron-up"
                width="20"
              >
              </v-btn>
            </template>
            <v-list
              class="cursor-pointer"
              density="compact"
              @click="dialogProcessColumn.show = true"
            >
              <v-list-item append-icon="mdi-format-list-group-plus">
                اصلاح الاعمدة قبل المعالجة
              </v-list-item>
              <!-- <v-list-item :title="$t('custom_date_range')" value="custom">
            </v-list-item> -->
            </v-list>
          </v-menu>
        </div>
      </div>
    </v-card>
  </div>
  <custom-dialog
    v-model="dialogProcessColumn.show"
    title="معالجة الاعمدة"
    width="1500"
    height="1000"
  >
    <v-row>
      <custom-text-field
        v-model="dialogProcessColumn.startRow"
        cols="3"
        label="تبداء البيانات في الاكسل من السطر رقم : "
        type="number"
      />
      <v-spacer />
      <custom-btn
        type="export"
        label="تصدير القالب الى ملف JSON"
        @click="exportSettingsToFile"
      />

      <custom-btn
        type="imports"
        label="استيراد القالب من ملف JSON"
        class="ms-5"
        @click="$refs.fileInput.click()"
      >
      </custom-btn>
      <input
        ref="fileInput"
        type="file"
        accept=".json"
        class="d-none"
        @change="importSettingsFromFile"
      />
    </v-row>
    <notes
      :items="[
        'تتيح لك هذه الشاشة ربط ومعالجة الأعمدة غير المتطابقة بين ملف Excel والنظام لضمان استيراد البيانات بشكل صحيح',
        'مثال في ملف الأكسل اسم العمود الطاب بينما في النظام اسم الطالب تستخدم هذه الشاشة لربط  الطالب بالعمود اسم الطالب ',
        'اي قيمة في في حقل الاكسل تطابق النص الموجود في حقل (القيمة من الاكسل) سيتم استبدالها الياَ الى القيمة الموجودة في حقل (تبد دائماَ الى القيمة )',
        'يمكنك ادخال عدة قيم للمطابقة بالفصل بينها بفاصلة (,) مثال (فيمة 1 , قيمة 2) ومن ثم عملها بنفس الترتيب في حقل (تبدل دائما الى القيمة)',
      ]"
    />

    <v-data-table-virtual
      density
      :headers="[
        { title: 'الحقل الاساسي', key: 'origin_col' },
        { title: 'الحقل من الاكسل', key: 'excel_col' },
        {
          title: 'معالجة الحقل',
          key: 'process_col',
          align: 'center',
          colspan: 2,
          children: [
            { title: 'القيمة من الاكسل', key: 'excel_val', align: 'center' },
            {
              title: 'تبدل دائماً الى القيمة',
              key: 'alternative_val',
              align: 'center',
            },
          ],
        },
        { title: 'القيمة الافتراضية للعمود بالكامل', key: 'default_val' },
      ]"
      :items="dialogProcessColumn.fields"
      class="header-table"
    >
      <template v-slot:item.origin_col="{ item, index }">
        <div
          :class="`${
            item.rules.some((r) => r === 'لايمكن ان يكون فارغاََ')
              ? 'field-rule-card--req'
              : 'field-rule-card--opt'
          } mt-2`"
          style="width: 200px"
        >
          <div class="field-rule-card__head">
            <span class="field-rule-card__num">{{ index + 1 }}</span>
            <span class="field-rule-card__name">{{
              item.field.name_list == "add_to_level" ? "الفرع" : item?.field?.label_ar
            }}</span>
            <v-chip
              v-if="item.rules.some((r) => r === 'لايمكن ان يكون فارغاََ')"
              size="x-small"
              color="error"
              variant="tonal"
            >
              <v-icon start size="9">mdi-asterisk</v-icon>مطلوب
            </v-chip>
            <v-chip v-else size="x-small" color="grey" variant="tonal">اختياري</v-chip>
          </div>
        </div>
      </template>
      <template v-slot:item.excel_col="{ item, index }">
        <VAutocomplete
          :model-value="dialogProcessColumn.fields[index].field.alternativeField"
          :items="headersInFile"
          variant="outlined"
          density="compact"
          hide-details
          clearable
          return-object
          @update:model-value="(val) => handleUpdateHeadersInFile(val, index)"
          width="200"
        />
      </template>
      <template v-slot:item.excel_val="{ item }">
        <custom-text-field
          v-model="item.field.origin_data"
          hide-details
          width="150"
          clearable
          :disabled="item.field.default_val ? item?.field?.default_val?.trim?.() : false"
        />
      </template>
      <template v-slot:item.alternative_val="{ item }">
        <auto-list
          v-if="item.field.name_list === 'add_to_level'"
          v-model="item.field.alternativeData"
          name="add_to_level"
          hide-details
          width="200"
          :disabled="item.field.default_val ? item?.field?.default_val?.trim?.() : false"
        />
        <field
          v-else
          v-model="item.field.alternativeData"
          :field="item.field"
          hideDetails
          :disabled="item.field.default_val ? item?.field?.default_val?.trim?.() : false"
          width="200"
        />
      </template>
      <template v-slot:item.default_val="{ item }">
        <auto-list
          v-if="item.field.name_list === 'add_to_level'"
          v-model="item.field.default_val"
          name="add_to_level"
          hide-details
          width="200"
        />
        <field
          v-model="item.field.default_val"
          :field="item.field"
          hideDetails
          width="200"
        />
      </template>
    </v-data-table-virtual>

    <table-drawer
      :headers="fullHeaders.map((e) => ({ title: e.label_ar, key: e.name }))"
      :items="{ results: dataInFile }"
    />

    <template #actions>
      <v-row>
        <v-spacer />

        <v-btn
          v-if="step === 3 && !error"
          color="primary"
          variant="flat"
          rounded="0"
          prepend-icon="mdi-check"
          :disabled="!uploadedFile || loading"
          :loading="loadinExportToExcel"
          @click.stop="() => processFile(false, true)"
          style="border-radius: 0 !important"
          >معالجة الملف
        </v-btn>
      </v-row>
    </template>
  </custom-dialog>
</template>

<script>
import i18n from "@/plugins/i18n";
import * as XLSX from "xlsx";
import ExcelJs from "exceljs";
import _ from "lodash";
export default {
  props: {
    fields: { type: [Array, String] },
    modelValue: {
      type: Boolean,
      default: false,
    },
    newDataToExcel: { type: Array },
    hideFieldExcel: { type: Array },
    newHeadersExcel: { type: Array, default: [] },

    fileExcel: String,
    startHeader: { type: Number, default: 1 },
    startRow: { type: Number, default: 2 },
    attr_field_excel: Object,
    loadinExportToExcel: {
      type: Boolean,
      default: false,
    },
    getData: { type: Function },
    autoImportExcel: {
      type: Boolean,
      default: false,
    },
    url: String,
    isImportOnly: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      uploadedFile: null,
      is_arabic: i18n.global.locale === "ar",

      dialog_name_list: false,
      step: this.isImportOnly ? 3 : 1,
      data_list: {},

      list_name: [],

      name_list: null,
      field_name: null,

      items: [],
      fields_items: [],

      // items_list_name: {},

      errors_validata: [],

      loading: false,
      error: false,

      dialogProcessColumn: { show: false },
      headersInFile: [],
      dataInFile: [],
    };
  },

  async created() {
    if (!this.isImportOnly) {
      this.initialData();
    }
  },
  methods: {
    async initialData() {
      // if (!this.fields) {
      //   this.$alert("errorData", { message: "لايوجد حقول" });
      //   return;
      // }
      try {
        this.error = false;
        this.loading = true;

        if (
          typeof this.fields === "String" ||
          typeof this.fields === "string" ||
          !this.fields
        ) {
          const url = this.fields || this.$route.name;
          await this.$axios(`${this.setting.url_field}${url}/`).then((response) => {
            const res = response.data.data || response.data;

            this.fields_items = res.map((field) => {
              let custom_field = field;

              if (this.attr_field_excel && this.attr_field_excel[field.name]) {
                custom_field = {
                  ...field,
                  ...this.attr_field_excel[field.name],
                };
              }

              return custom_field;
            });
          });
        } else {
          this.fields_items = [...this.fields];
        }
      } catch (e) {
        this.error = true;
      } finally {
        this.loading = false;
      }
      this.generatedTextValid();
    },

    generatedTextValid() {
      let list = [];

      this.fullHeaders.map((field) => {
        list.push({
          field: { ...field },
          rules: this.generatedValid(field, this.is_arabic),
        });
      });

      this.items = list;
    },

    async downloadTemplate() {
      new Promise(async (resolve, reject) => {
        const headers = this.fullHeaders;

        const workbook = new ExcelJs.Workbook();
        let worksheet;
        if (!this.fileExcel) {
          worksheet = workbook.addWorksheet("template", {
            views: [{ rightToLeft: true }],
          });
          worksheet.getRow(1).eachCell((cell) => {
            cell.fill = {
              type: "pattern",
              pattern: "solid",
              fgColor: { argb: "FFD9D9D9" },
            };
            cell.font = {
              bold: true,
              color: { argb: "FF000000" },
            };
          });

          worksheet.columns = headers
            .filter((f) => f.depend != false)
            .map((h) => {
              const header = h["null"] === false ? h.label_ar + "*" : h.label_ar;
              return {
                header: header,
                key: h.name,
              };
            });
          worksheet.eachRow((row) => {
            row.values.forEach((value, col) => {
              const column = worksheet.getColumn(col);
              const cell = value ? value.length : 0;

              if (cell > column.width) {
                column.width = cell + 2;
              }
            });
            row.eachCell((cell) => {
              cell.alignment = { horizontal: "right", vertical: "right" };
              cell.border = {
                top: { style: "thin" },
                left: { style: "thin" },
                right: { style: "thin" },
                bottom: { style: "thin" },
              };
            });
          });
        } else {
          const response = await fetch(this.fileExcel);
          const arrayBuffer = await response.arrayBuffer();
          await workbook.xlsx.load(arrayBuffer);
          worksheet = workbook.worksheets[0];
        }

        /////////////////////////////student ////////////////////////////

        // worksheet.addRow([]);
        // worksheet.getRow(1).height = 20;
        // worksheet.addRow(headers_label);
        // worksheet.getRow(2).height = 30;

        // worksheet.getRow(2).eachCell((cell) => {
        //   cell.fill = {
        //     type: "pattern",
        //     pattern: "solid",
        //     fgColor: { argb: "FFD9D9D9" },
        //   };
        //   cell.font = {
        //     bold: true,
        //     color: { argb: "FF000000" },
        //   };
        //   cell.height = 30;
        // });
        /////////////////////////////////////////////////////

        if (this.newDataToExcel) {
          this.newDataToExcel.forEach((row) => {
            const values = headers.map((h) => row[h.name]);
            worksheet.addRow(values);
          });
        }
        // const field_hide = headers.filter((f) => f.depend === false);
        // field_hide.forEach((colKey) => {
        //   const col = worksheet.columns.find((c) => c.key === colKey.name);
        //   if (col) col.hidden = true;
        // });

        const file_name = prompt(i18n.global.t("enter_file_name"));

        if (file_name) {
          workbook.xlsx.writeBuffer().then((buffer) => {
            const data = new Blob([buffer], {
              type: "application/octet-stream",
            });
            saveAs(data, file_name + ".xlsx");
          });

          resolve();
          this.$snack("add", { message: "تم تحميل الملف بنجاح" });
        }
      });
    },
    async processFile(fetch_headers_in_file = false, alternativeMethode = false) {
      if (this.isImportOnly) {
        this.$emit("process-export", this.uploadedFile);
        return;
      }
      this.errors_validata = [];
      if (!this.uploadedFile) return;

      return new Promise(async (resolve, reject) => {
        try {
          const reader = new FileReader();
          let errors = [];

          reader.onload = (e) => {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: "array" });
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];

            const keys = alternativeMethode
              ? this.dialogProcessColumn?.fields.map((e) => ({
                  ...e.field,
                }))
              : this.fullHeaders;

            let origin_header = keys.map((e) => e.alternativeField || e.label_ar);
            console.log(this.startHeader);

            const headerFromExcel = XLSX.utils.sheet_to_json(sheet, {
              header: 1,
              range: this.startHeader - 1,
            })[0];
            console.log(headerFromExcel);
            let headerInFile = {};
            headerFromExcel.forEach((e) => {
              headerInFile[e] = e;
            });

            if (fetch_headers_in_file) {
              this.headersInFile = headerFromExcel.map((e) => {
                if (e.endsWith("*")) {
                  return e.slice(0, -1);
                } else {
                  return e;
                }
              });
              return;
            }

            let error_header = [];
            for (const item of origin_header) {
              if ((item + "*", headerInFile[item + "*"] || item == headerInFile[item])) {
              } else {
                error_header.push(item);
              }
            }

            if (error_header.length) {
              this.$alert("errorData", {
                title: "الترويسة غير متطابقة",
                message: {
                  "الاعمدة الغير موجودة": error_header,
                },
              });
              return;
            }

            const json = XLSX.utils.sheet_to_json(sheet, {
              header: headerFromExcel.map((e) => e),
              range: alternativeMethode
                ? this.dialogProcessColumn.startRow - 1 || this.startRow - 1
                : this.startRow - 1,
              raw: false,
            });

            let dataJson = [];
            json.forEach((row, rowIndex) => {
              let rowErrors = [];
              let value = {};

              keys.forEach((field) => {
                const field_name = field.alternativeField || field.label_ar;

                value[field.name] = row[field_name] || row[field_name + "*"] || null;

                var currentField = value[field.name];

                let infoError = `الصف ${rowIndex + 1 + this.startRow}: الحقل "${
                  field.label_ar
                }"`;

                if (field?.default_val) {
                  value[field.name] = field?.default_val || null;
                } else if (field.origin_data || field.alternativeData) {
                  const altVal = (field.alternativeData || "")
                    .split(",")
                    .map((item) => item.trim());
                  (field.origin_data || "").split(",").forEach((item, index) => {
                    if (currentField == item) {
                      value[field.name] = altVal[index];
                    }
                  });
                }

                // if (field.origin_data || field.alternativeData) {
                //   const altValues = (field.alternativeData || "")
                //     .split(",")
                //     .map((item) => item.trim());
                //   console.log(altValues);
                //   (field.origin_data || "").split(",").forEach((item) => {
                //     if (currentField === field.origin_data) {
                //       console.log(item.trim());
                //     }
                //   });
                // }

                // if (currentField == field.origin_data) {
                //   const altValues = (field.alternativeData || "")
                //     .split(",")
                //     .map((item) => item.trim());
                //   console.log(field.origin_data);

                //   const originValues = (field.origin_data || "").split(",").map((item) => {
                //     return item.trim();

                //     // if (item.trim() == currentField) {
                //     //   value[field.name] = altValues[index];
                //     //   // return;
                //     // }
                //   });

                // (value[field.name] || "").split(",").forEach((item, ind ex) => {
                //   if (altValues[index] === item) {
                //     currentField = altValues[index];
                //   }
                // });
                // }

                if (
                  !field.null &&
                  (currentField === "" ||
                    currentField === undefined ||
                    currentField === null)
                ) {
                  rowErrors.push(`${infoError}  مطلوب`);
                  return;
                }

                if (
                  field.name_list === null ||
                  field.name_list === "" ||
                  !field.name_list ||
                  field.name_list === undefined
                ) {
                  if (
                    currentField !== "" &&
                    currentField !== undefined &&
                    currentField != null
                  ) {
                    if (field.type === "DateField") {
                      if (currentField) {
                        const date = new Date(currentField);
                        currentField = `${date.getFullYear()}-${
                          date.getMonth() + 1
                        }-${date.getDate()}`;
                      }
                    } else if (
                      field.type === "BooleanField" &&
                      !(
                        currentField == true ||
                        currentField == false ||
                        currentField == 1 ||
                        currentField == 0 ||
                        currentField == "true" ||
                        currentField == "TRUE" ||
                        currentField == "FALSE"
                      )
                    ) {
                      rowErrors.push(`${infoError}  يجب ان يكون قيمة منطقية`);
                    } else if (field.type === "DecimalField") {
                      // const regex = new RegExp(`^\\d{1,${max_digits}}$|^\\d{1,${max_digits - decimal_places}}(\\.\\d{1,${decimal_places}})?$`)
                      // if (!regex.test(String(value)?.replace(/[^0-9.]/g, '')) && value) {
                      //   return t(
                      //     `يجب إدخال رقم صحيح بحد أقصى ${max_digits} أرقام و ${decimal_places} بعد الفاصلة`,
                      //     `Must enter a valid number with up to ${max_digits} digits and ${decimal_places} decimals`
                      //   )
                      // }
                    } else if (
                      field.type === "IntegerField" ||
                      field.type === "DecimalField" ||
                      field.type === "PositiveSmallIntegerField"
                    ) {
                      if (isNaN(Number(currentField)))
                        rowErrors.push(`${infoError}  يجب ان يكون عدد`);
                      const num = Number(currentField);

                      if (field.max_value != undefined && num > field.max_value)
                        rowErrors.push(
                          `${infoError}  اكبر من المسموح (${field.max_value})`
                        );
                      if (field.min_value != undefined && num < field.min_value)
                        rowErrors.push(
                          `${infoError}  أصغر من المسموح (${field.min_value})`
                        );
                    }

                    if (field.max_length && currentField.length > field.max_length)
                      rowErrors.push(
                        `${infoError}  يتجاوز الحد الاقصى (${field.max_length})`
                      );
                    if (field.min_length && currentField.length < field.min_length)
                      rowErrors.push(
                        `${infoError}  اقل من الحد الأدنى (${field.min_length})`
                      );
                  }
                }
              });

              dataJson.push(value);
              if (rowErrors.length > 0) {
                errors.push(...rowErrors);
              }
            });

            // for (let index = 0; index <= 2000000; index++) {
            //   this.dataInFile.push(...dataJson);
            // }

            this.dataInFile = [...dataJson];

            this.errors_validata = errors;

            // let r = this.value_model;

            if (errors.length > 0) this.$emit("process-export", [], true);
            else {
              if (this.autoImportExcel) {
                try {
                  // this.loading = true;
                  this.$axios.post(this.url, this.dataInFile).then((ele) => {
                    this.$snack("add");
                    if (this.getData) {
                      this.getData();
                    }
                    this.$emit("closeImortExcel");
                  });
                } finally {
                  // this.loading = false;
                }
              } else {
                this.$emit("process-export", this.dataInFile, false);
              }
            }
          };

          reader.onerror = reject;
          reader.readAsArrayBuffer(this.uploadedFile);
        } catch (error) {
          this.$alert("errorData", { message: error });
        }
      });
    },

    generatedValid(field, is_arabic = true) {
      let list = [];

      if ("null" in field && !field.null)
        list.push(is_arabic ? "لايمكن ان يكون فارغاََ" : "This field is required");

      if (
        field.name_list === null ||
        field.name_list === "" ||
        field.name_list === undefined ||
        !field.name_list
      ) {
        switch (field.type) {
          case "CharField":
            list.push(is_arabic ? "نصوص , ارقام , رموز" : "");
            break;
          case "TextField":
            list.push(is_arabic ? "نصوص , ارقام , رموز" : "");
            break;
          case "PositiveSmallIntegerField":
            list.push(is_arabic ? "ارقام موجبة" : "");
            break;

          case "DateField":
            list.push(is_arabic ? "تاريخ مثال (YYYY-MM-DD)" : "");

            break;
          case "DecimalField":
            list.push(
              is_arabic
                ? `يجب إدخال رقم صحيح بحد أقصى ${field.max_digits} أرقام و ${field.decimal_places} بعد الفاصلة`
                : `Must enter a valid number with up to ${field.max_digits} digits and ${field.decimal_places} decimals`
            );
            break;

          case "TimeField":
            list.push("يجب ادخال وقت مثال" + " 08:01:15");
            break;
          case "BooleanField":
            list.push("يجب ان تكون قيمة منطقية true , false");
            break;
        }

        if ("min_length" in field && field.min_length)
          list.push(
            `${is_arabic ? "أقل عدد من المحارف" : "Min characters"}    ${
              field.min_length
            }`
          );

        if ("max_length" in field && field.max_length)
          list.push(
            `${is_arabic ? "اقصى عدد من المحارف" : "Max characters"}    ${
              field.max_length
            }`
          );

        if ("min_value" in field && field.min_value)
          list.push(
            `${is_arabic ? "أقل قيمة يمكن قبولها" : "Minimum acceptable value"}   ${
              field.min_value
            }`
          );

        if ("max_value" in field && field.max_value)
          list.push(
            `${is_arabic ? "اكبر قيمة يمكن قبولها" : "Maximum acceptable value"}  ${
              field.max_value
            }`
          );
      } else {
        list.push({ name_list: field.name_list });
      }

      return list;
    },

    async copyText(text) {
      try {
        await navigator.clipboard.writeText(text);
        this.$snack("add", { message: "تم النسخ" });
      } catch (err) {
        console.log("فشل النسخ");
      }
    },

    handleUpdateHeadersInFile(val, index) {
      const alternativeF = this.dialogProcessColumn?.fields[index]?.field;
      if (alternativeF) {
        alternativeF.alternativeField = val;
      }
    },

    exportSettingsToFile() {
      const dataStr =
        "data:text/json;charset=utf-8," +
        encodeURIComponent(
          JSON.stringify(
            {
              fields: this.dialogProcessColumn?.fields,
              startRow: this.dialogProcessColumn.startRow,
            },
            null,
            2
          )
        );
      const file_name = prompt("اجخل اسم الملف");
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `${file_name}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    },
    importSettingsFromFile(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const parsedConfig = JSON.parse(e.target.result);

          if (parsedConfig) {
            this.dialogProcessColumn.fields = parsedConfig.fields;
            this.dialogProcessColumn.startRow = parsedConfig.startRow;
            this.$snack("add", { message: "تم استرجاع القالب بنجاح" });
          } else {
            this.$snack("errorData", { message: "تنسيق الملف غير صحيح ." });
          }
        } catch (err) {
          this.$alert("errorData", {
            message: "حدث خطاء أثناء قراءة الملف , تأكد من اختيار ملف JSON صالح .",
          });
        }
      };

      reader.readAsText(file);
      event.target.value = "";
    },
  },

  computed: {
    value_model: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    fullHeaders() {
      return [
        ...this.fields_items.filter((f) => f.depend != false),
        ...this.newHeadersExcel,
      ];
    },
  },
  watch: {
    "dialogProcessColumn.show"(val) {
      if (val) {
        this.processFile(true);
        this.dialogProcessColumn.fields = _.cloneDeep(this.items);
        this.dialogProcessColumn.startRow = this.startRow;
      } else {
        this.dialogProcessColumn.fields = [];
        this.headerInFile = [];
        this.dialogProcessColumn.startRow = null;
      }
    },
  },
};
</script>

<style scoped>
.header-table :deep(th) {
  background-color: rgb(var(--v-theme-surface)) !important;
  background-image: linear-gradient(
    rgba(var(--v-theme-primary), 0.08),
    rgba(var(--v-theme-primary), 0.08)
  ) !important;

  font-weight: bold;
}
/* ══════════════════════════════════════════════════════
   ImportExcel — Enterprise Design System (v2)
   All values use CSS Design Tokens
══════════════════════════════════════════════════════ */

.import-excel-root {
  font-family: "Tajawal", sans-serif;
}

.import-card {
  border-radius: var(--radius-xl) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08) !important;
  min-height: 540px;
  overflow: hidden;
}

/* ══ Professional Header ══ */
.import-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-lg);
  gap: var(--space-lg);
  flex-wrap: wrap;
}

.import-header__brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.import-header__icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  background: rgba(var(--v-theme-primary), 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.import-header__title {
  font-size: 0.95rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  line-height: 1.3;
}

.import-header__subtitle {
  font-size: 0.75rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
  margin-top: 1px;
}

/* Steps Track */
.steps-track {
  display: flex;
  align-items: center;
}

.steps-track__step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.steps-track__line {
  width: 48px;
  height: 2px;
  background: rgba(var(--v-theme-on-surface), 0.12);
  margin-bottom: 18px;
  transition: background 0.3s ease;
}
.steps-track__line--done {
  background: rgb(var(--v-theme-primary));
}

.steps-track__bubble {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}
.steps-track__bubble--active {
  background: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 4px rgba(var(--v-theme-primary), 0.15);
}
.steps-track__bubble--done {
  background: rgb(var(--v-theme-primary));
}
.steps-track__bubble--pending {
  background: rgba(var(--v-theme-on-surface), 0.07);
  border: 1.5px solid rgba(var(--v-theme-on-surface), 0.15);
}

.steps-track__label {
  font-size: 0.7rem;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.4);
  white-space: nowrap;
  transition: color 0.2s ease;
}
.steps-track__label--active {
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
}
.steps-track__label--done {
  color: rgba(var(--v-theme-primary), 0.6);
}

.import-header-divider {
  opacity: 0.06;
}

/* ══ Content ══ */
.import-content {
  padding: var(--space-lg);
  overflow-y: auto;
}

.step-pane {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  min-height: 320px;
}

/* ══ Step 1: Empty State ══ */
.step-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  min-height: 300px;
  text-align: center;
}
.step-icon-wrap {
  width: 88px;
  height: 88px;
  border-radius: var(--radius-xl);
  background: rgba(var(--v-theme-primary), 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
}
.step-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  margin: 0;
}
.step-description {
  font-size: 0.9rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  max-width: 360px;
  line-height: 1.6;
  margin: 0;
}
.import-btn-primary {
  border-radius: var(--radius-lg) !important;
  min-width: 160px;
}

.error-state-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xl);
  border-radius: var(--radius-lg);
  background: rgba(var(--v-theme-error), 0.04);
  border: 1px solid rgba(var(--v-theme-error), 0.12);
}
.error-state-text {
  font-size: 0.9rem;
  color: rgb(var(--v-theme-error));
  font-weight: 500;
}

/* ══ Step 2: Section Header ══ */
.s2-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: rgba(var(--v-theme-primary), 0.04);
  border-radius: var(--radius-md);
  border-inline-start: 3px solid rgb(var(--v-theme-primary));
  margin-bottom: var(--space-md);
}
.s2-header__icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: rgba(var(--v-theme-primary), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.s2-header__title {
  font-size: 0.9rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
}
.s2-header__sub {
  font-size: 0.78rem;
  color: rgba(var(--v-theme-on-surface), 0.55);
}

/* ══ Step 2: Field Cards Grid ══ */
.fields-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-sm);
  overflow-y: auto;
  max-height: 300px;
}
.field-rule-card {
  border-radius: var(--radius-lg);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  background: rgb(var(--v-theme-surface));
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}
.field-rule-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}
.field-rule-card--req {
  border-color: rgba(var(--v-theme-error), 0.15);
}
.field-rule-card__top-bar {
  height: 3px;
}
.field-rule-card--req .field-rule-card__top-bar {
  background: rgb(var(--v-theme-error));
}
.field-rule-card--opt .field-rule-card__top-bar {
  background: rgba(var(--v-theme-on-surface), 0.1);
}

.field-rule-card__head {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm);
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.05);
  flex-wrap: wrap;
}
.field-rule-card__num {
  width: 20px;
  height: 20px;
  border-radius: var(--radius-full);
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  font-size: 0.68rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.field-rule-card__name {
  font-size: 0.82rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  flex: 1;
}
.field-rule-card__body {
  padding: var(--space-sm);
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.rule-line {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.78rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  line-height: 1.4;
}

/* ══ Step 3: Upload Dropzone ══ */
.step-pane--upload {
  gap: var(--space-lg);
}

.upload-dropzone {
  border: 2px dashed rgba(var(--v-theme-primary), 0.3);
  border-radius: var(--radius-xl);
  background: rgba(var(--v-theme-primary), 0.04);
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  transition: all 0.2s ease;
}
.upload-dropzone--active {
  border-color: rgba(var(--v-theme-success), 0.35);
  background: rgba(var(--v-theme-success), 0.02);
}
.upload-dropzone__icon-wrap {
  width: 68px;
  height: 68px;
  border-radius: var(--radius-full);
  background: rgba(var(--v-theme-primary), 0.07);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}
.upload-dropzone__icon-wrap--ok {
  background: rgba(var(--v-theme-success), 0.07);
}
.upload-dropzone__texts {
  text-align: center;
}
.upload-dropzone__main {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface));
}
.upload-dropzone__sub {
  font-size: 0.78rem;
  color: rgba(var(--v-theme-on-surface), 0.4);
  margin-top: 4px;
}
.upload-dropzone__input {
  width: 100%;
}

/* ══ Validation Errors ══ */
.val-errors {
  border-radius: var(--radius-lg);
  border: 1px solid rgba(var(--v-theme-error), 0.2);
  background: rgba(var(--v-theme-error), 0.02);
  overflow: hidden;
}
.val-errors__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-sm) var(--space-md);
  background: rgba(var(--v-theme-error), 0.05);
  border-bottom: 1px solid rgba(var(--v-theme-error), 0.1);
}
.val-errors__head-left {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}
.val-errors__title {
  font-size: 0.85rem;
  font-weight: 700;
  color: rgb(var(--v-theme-error));
}
.val-errors__list {
  max-height: 160px;
  overflow-y: auto;
}
.val-errors__row {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-md);
  border-bottom: 1px solid rgba(var(--v-theme-error), 0.05);
  font-size: 0.82rem;
}
.val-errors__row:last-child {
  border-bottom: none;
}
.val-errors__num {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border-radius: var(--radius-full);
  background: rgba(var(--v-theme-error), 0.1);
  color: rgb(var(--v-theme-error));
  font-size: 0.68rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.val-errors__msg {
  color: rgba(var(--v-theme-on-surface), 0.75);
  line-height: 1.5;
}

/* ══ Upload Ready State ══ */
.upload-ready {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: rgba(var(--v-theme-success), 0.06);
  border-radius: var(--radius-md);
  border: 1px solid rgba(var(--v-theme-success), 0.15);
}
.upload-ready__title {
  font-size: 0.875rem;
  font-weight: 700;
  color: rgb(var(--v-theme-success));
}
.upload-ready__sub {
  font-size: 0.78rem;
  color: rgba(var(--v-theme-success), 0.7);
}

/* ══ Footer ══ */
.import-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  background: rgb(var(--v-theme-surface));
}
.import-footer__dots {
  display: flex;
  gap: 6px;
  align-items: center;
}
.import-footer__dot {
  width: 7px;
  height: 7px;
  border-radius: var(--radius-full);
  background: rgba(var(--v-theme-on-surface), 0.15);
  transition: all 0.25s ease;
}
.import-footer__dot--active {
  width: 20px;
  background: rgb(var(--v-theme-primary));
}
.import-footer__dot--done {
  background: rgba(var(--v-theme-primary), 0.4);
}

.import-btn-nav {
  border-radius: var(--radius-lg) !important;
}
.import-btn-submit {
  border-radius: var(--radius-lg) !important;
  min-width: 140px;
}

/* ══ Scrollbar ══ */
.val-errors__list::-webkit-scrollbar,
.fields-grid::-webkit-scrollbar {
  width: 4px;
}
.val-errors__list::-webkit-scrollbar-track,
.fields-grid::-webkit-scrollbar-track {
  background: transparent;
}
.val-errors__list::-webkit-scrollbar-thumb,
.fields-grid::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: var(--radius-full);
}
</style>
