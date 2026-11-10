<template>
  <div class="import-excel-root">
    <v-card class="import-card d-flex flex-column" :loading="loading" elevation="0">

      <!-- ── Professional Header ── -->
      <div class="import-header">
        <div class="import-header__brand">
          <div class="import-header__icon">
            <v-icon size="20" color="primary">mdi-microsoft-excel</v-icon>
          </div>
          <div>
            <div class="import-header__title">استيراد بيانات Excel</div>
            <div class="import-header__subtitle">اتبع الخطوات لاستيراد البيانات بشكل صحيح</div>
          </div>
        </div>

        <div class="steps-track">
          <template v-for="(s, i) in [
            { label: 'تحميل القالب', icon: 'mdi-download-outline' },
            { label: 'تعبئة الملف', icon: 'mdi-table-edit' },
            { label: 'رفع ومعالجة', icon: 'mdi-upload-outline' }
          ]" :key="i">
            <div v-if="i > 0" class="steps-track__line" :class="{ 'steps-track__line--done': step > i }" />
            <div class="steps-track__step">
              <div class="steps-track__bubble"
                :class="{
                  'steps-track__bubble--active': step === i + 1,
                  'steps-track__bubble--done': step > i + 1,
                  'steps-track__bubble--pending': step < i + 1
                }">
                <v-icon v-if="step > i + 1" size="14" color="white">mdi-check</v-icon>
                <v-icon v-else size="14" :color="step === i + 1 ? 'white' : 'grey-lighten-1'">{{ s.icon }}</v-icon>
              </div>
              <div class="steps-track__label"
                :class="{
                  'steps-track__label--active': step === i + 1,
                  'steps-track__label--done': step > i + 1
                }">
                {{ s.label }}
              </div>
            </div>
          </template>
        </div>
      </div>

      <v-divider class="import-header-divider" />

      <!-- ── Content ── -->
      <div class="import-content flex-grow-1">

        <!-- Step 1 -->
        <div v-if="step === 1" class="step-pane">
          <div class="step-empty-state">
            <div class="step-icon-wrap">
              <v-icon size="52" color="primary">mdi-microsoft-excel</v-icon>
            </div>
            <h3 class="step-title">تحميل قالب Excel</h3>
            <p class="step-description">اضغط على الزر أدناه للحصول على قالب Excel الجاهز مع الأعمدة المطلوبة.</p>
            <v-btn v-if="!error" color="primary" variant="flat" size="large"
              prepend-icon="mdi-download-outline" class="import-btn-primary"
              @click="downloadTemplate" :disabled="loading">
              تحميل القالب
            </v-btn>
            <div v-if="error" class="error-state-block">
              <v-icon color="error" size="28">mdi-alert-circle-outline</v-icon>
              <span class="error-state-text">حدث خطأ أثناء التحميل</span>
              <v-btn variant="tonal" color="error" size="small" prepend-icon="mdi-refresh" @click="initialData()">إعادة المحاولة</v-btn>
            </div>
          </div>
        </div>

        <!-- Step 2: Field Rules -->
        <div v-if="step === 2" class="step-pane step-pane--rules">
          <div v-if="error" class="error-state-block">
            <v-icon color="error" size="36">mdi-alert-circle-outline</v-icon>
            <span class="error-state-text">فشل تحميل قواعد الحقول</span>
            <v-btn variant="tonal" color="error" size="small" prepend-icon="mdi-refresh" @click="initialData()">إعادة المحاولة</v-btn>
          </div>
          <template v-else>
            <div class="s2-header">
              <div class="s2-header__icon"><v-icon size="18" color="primary">mdi-table-check</v-icon></div>
              <div>
                <div class="s2-header__title">قواعد تعبئة البيانات</div>
                <div class="s2-header__sub">راجع كل حقل قبل تعبئة الملف — الحقول المميزة بـ * إلزامية</div>
              </div>
              <v-chip size="small" color="primary" variant="tonal" class="ms-auto">{{ items.length }} حقل</v-chip>
            </div>

            <div class="fields-grid">
              <div v-for="(item, index) in items" :key="index" class="field-rule-card"
                :class="item.rules.some(r => r === 'لايمكن ان يكون فارغاََ') ? 'field-rule-card--req' : 'field-rule-card--opt'">
                <div class="field-rule-card__top-bar" />
                <div class="field-rule-card__head">
                  <span class="field-rule-card__num">{{ index + 1 }}</span>
                  <span class="field-rule-card__name">{{ item.name }}</span>
                  <v-chip v-if="item.rules.some(r => r === 'لايمكن ان يكون فارغاََ')" size="x-small" color="error" variant="tonal">
                    <v-icon start size="9">mdi-asterisk</v-icon>مطلوب
                  </v-chip>
                  <v-chip v-else size="x-small" color="grey" variant="tonal">اختياري</v-chip>
                </div>
                <div class="field-rule-card__body">
                  <template v-for="(rule, ri) in item.rules" :key="ri">
                    <div v-if="typeof rule === 'object'" class="rule-line">
                      <auto-list v-model="data_list[item.field]" :name="rule.name_list"
                        :param="item.param ? data_list[item.param] : undefined" />
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
            <div class="s2-header__icon"><v-icon size="18" color="primary">mdi-upload-outline</v-icon></div>
            <div>
              <div class="s2-header__title">رفع الملف المكتمل</div>
              <div class="s2-header__sub">اختر ملف Excel الذي قمت بتعبئته لمعالجته</div>
            </div>
          </div>

          <div class="upload-dropzone" :class="{ 'upload-dropzone--active': uploadedFile }">
            <div class="upload-dropzone__icon-wrap" :class="uploadedFile ? 'upload-dropzone__icon-wrap--ok' : ''">
              <v-icon size="40" :color="uploadedFile ? 'success' : 'primary'">
                {{ uploadedFile ? 'mdi-check-circle-outline' : 'mdi-cloud-upload-outline' }}
              </v-icon>
            </div>
            <div class="upload-dropzone__texts">
              <div class="upload-dropzone__main">{{ uploadedFile ? 'تم اختيار الملف بنجاح' : 'اسحب الملف هنا أو اضغط للاختيار' }}</div>
              <div class="upload-dropzone__sub">الصيغ المدعومة: .xlsx, .xls فقط</div>
            </div>
            <v-file-input v-model="uploadedFile" accept=".xlsx,.xls" variant="outlined"
              density="comfortable" prepend-icon="mdi-file-excel-outline"
              :label="uploadedFile ? 'تغيير الملف' : 'اختر ملفاً'" clearable
              hide-details="auto" class="upload-dropzone__input" />
          </div>

          <div v-if="errors_validata.length > 0" class="val-errors">
            <div class="val-errors__head">
              <div class="val-errors__head-left">
                <v-icon color="error" size="16">mdi-alert-circle</v-icon>
                <span class="val-errors__title">أخطاء التحقق</span>
              </div>
              <v-chip size="small" color="error" variant="tonal">{{ errors_validata.length }} خطأ</v-chip>
            </div>
            <div class="val-errors__list">
              <div v-for="(item, index) in errors_validata" :key="index" class="val-errors__row">
                <span class="val-errors__num">{{ index + 1 }}</span>
                <span class="val-errors__msg">{{ item }}</span>
              </div>
            </div>
          </div>

          <div v-if="uploadedFile && errors_validata.length === 0 && !loading" class="upload-ready">
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
          <v-btn v-if="step > 1" variant="tonal" color="primary"
            prepend-icon="mdi-chevron-right" class="import-btn-nav" @click="step--">السابق</v-btn>
        </div>
        <div class="import-footer__dots">
          <span v-for="s in 3" :key="s" class="import-footer__dot"
            :class="{ 'import-footer__dot--active': step === s, 'import-footer__dot--done': step > s }" />
        </div>
        <div>
          <v-btn v-if="step < 3" color="primary" variant="flat"
            append-icon="mdi-chevron-left" class="import-btn-nav" @click="step++">التالي</v-btn>
          <v-btn v-if="step === 3 && !error" color="success" variant="flat"
            prepend-icon="mdi-check" :disabled="!uploadedFile || loading"
            :loading="loadinExportToExcel" class="import-btn-submit" @click="processFile">معالجة الملف</v-btn>
        </div>
      </div>

    </v-card>
  </div>
</template>

<script>
import i18n from "@/plugins/i18n";
import * as XLSX from "xlsx";
import ExcelJs from "exceljs";

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
    exclude_field_excel: { type: Array, default: [] },
    fileExcel: String,
    startRow: { type: Number, default: 1 },
    attr_field_excel: Object,
    loadinExportToExcel: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      uploadedFile: null,
      is_arabic: i18n.global.locale === "ar",

      dialog_name_list: false,
      step: 1,
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
    };
  },

  async created() {
    this.initialData();
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
            const res = response.data.data || response.data

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

        if (this.exclude_field_excel.length > 0)
          this.fields_items = this.fields_items.filter(
            (item) => !this.exclude_field_excel.includes(item.name)
          );
      } catch (e) {
        this.error = true;
      } finally {
        this.loading = false;
      }
      this.generatedTextValid();
    },

    generatedTextValid() {
      let list = [];

      this.fields_items
        .filter((f) => f.depend != false)
        .map((field) => {
          list.push({
            name: field.label_ar,
            rules: this.generatedValid(field, this.is_arabic),
            field: field.name,
            param: field.param,
          });
        });

      this.items = list;
    },

    async downloadTemplate() {
     
      new Promise(async (resolve, reject) => {
        const headers = [...this.fields_items, ...this.newHeadersExcel];

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
         
          worksheet.columns = headers.filter((f) => f.depend !=  false).map((h) => {
            console.log( h['null'] );
            const header  = h['null']  === false ?   h.label_ar +  "*"  : h.label_ar
            return {
            header:header,
            key: h.name,
          }
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
    async processFile() {
      this.errors_validata = [];
      if (!this.uploadedFile) return;

      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        let errors = [];

        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: "array" });
          const sheetName = workbook.SheetNames[0];
          const sheet = workbook.Sheets[sheetName];
          const field_items = this.fields_items.filter(
            (f) => f.depend != false
          );
          const keys = [...field_items, ...this.newHeadersExcel];

          let origin_header = keys.map((e) => e.label_ar);

          const headerInFile = XLSX.utils.sheet_to_json(sheet, {
            header: 1,
            range: this.startRow - 1,
          })[0];

          let isValid = true
          for(const i in origin_header){
            
          
            if((headerInFile[i]  === origin_header[i] + "*")  || (headerInFile[i]  === origin_header[i])) {                                          
              isValid = true
              }    else {
                isValid = false

                break
              }                    
            
          }
         
            

       

          if (!isValid) {
            let error_header = [];

        

            origin_header.forEach((h, i) => {                 
              if(!(h === headerInFile[i])){       
                error_header.push(h)                              
              }
            });

                      

            this.$alert("errorData", {
              title: "الترويسة غير متطابقة",
              message: {
                "الاعمدة الغير مطابقة":error_header

              },
            });
            return;
          }

          const json = XLSX.utils.sheet_to_json(sheet, {
            header: keys.map((e) => e.name),
            range: this.startRow,
            raw: false,
          });

          json.forEach((row, rowIndex) => {
            let rowErrors = [];
            

            this.fields_items.forEach((field) => {
              
              let infoError = `الصف ${
                rowIndex + 1 + this.startRow
              }: الحقل "${field.label_ar}"`;
              let value;
              if (field.type === "DateField") {
                if (row[field.name]) {
                  const date = new Date(row[field.name]);
                  row[field.name] = `${date.getFullYear()}-${
                    date.getMonth() + 1
                  }-${date.getDate()}`;
                }
              }

              value = row[field.name];
              if(value === undefined)
                row[field.name] = null
               
            

              if (
                !field.null &&
                (value === "" || value === undefined || value === null)
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
                if (value !== "" && value !== undefined && value != null) {
                  if (field.type === "CharField") {
                    if (typeof String(value) !== "string")
                      rowErrors.push(`${infoError}  يجب ان يكون نص`);

                    if (field.name.endsWith("_ar")) {
                      const valid =
                        /^[\u0621-\u064A '0-9+ '-.,@#$%^&*()_+=!*?]+$/.test(
                          value
                        );
                      if (!valid)
                        rowErrors.push(
                          `${infoError} يجب أن تكون أحرف عربية فقط`
                        );
                    } else if (field.name.endsWith("_en")) {
                      const valid =
                        /^[a-zA-Z' '0-9+  '-.,@#$%^&*()_+=!*?]+$/.test(value);
                      if (!valid)
                        rowErrors.push(
                          `${infoError} يجب أن تكون أحرف إنجليزية فقط`
                        );
                    }
                    // if (this.field.name.endsWith("_en")) rules.push(this.$en);
                  } else if (
                    field.type === "BooleanField" &&
                    !(
                      value === true ||
                      value === false ||
                      value === 1 ||
                      value === 0 ||
                      value === "true" ||
                      value === "false"
                    )
                  ) {
                    rowErrors.push(`${infoError}  يجب ان يكون قيمة منطقية`);
                  }

                  if (field.type === "DecimalField") {
                    // const regex = new RegExp(`^\\d{1,${max_digits}}$|^\\d{1,${max_digits - decimal_places}}(\\.\\d{1,${decimal_places}})?$`)
                    // if (!regex.test(String(value)?.replace(/[^0-9.]/g, '')) && value) {
                    //   return t(
                    //     `يجب إدخال رقم صحيح بحد أقصى ${max_digits} أرقام و ${decimal_places} بعد الفاصلة`,
                    //     `Must enter a valid number with up to ${max_digits} digits and ${decimal_places} decimals`
                    //   )
                    // }
                  }

                  if (
                    field.type === "IntegerField" ||
                    field.type === "DecimalField" ||
                    field.type === "PositiveSmallIntegerField"
                  ) {
                    if (isNaN(Number(value)))
                      rowErrors.push(`${infoError}  يجب ان يكون عدد`);
                    const num = Number(value);

                    if (field.max_value != undefined && num > field.max_value)
                      rowErrors.push(
                        `${infoError}  اكبر من المسموح (${field.max_value})`
                      );
                    if (field.min_value != undefined && num < field.min_value)
                      rowErrors.push(
                        `${infoError}  أصغر من المسموح (${field.min_value})`
                      );
                  }

                  if (field.max_length && value.length > field.max_length)
                    rowErrors.push(
                      `${infoError}  يتجاوز الحد الاقصى (${field.max_length})`
                    );
                  if (field.min_length && value.length < field.min_length)
                    rowErrors.push(
                      `${infoError}  اقل من الحد الأدنى (${field.min_length})`
                    );
                }
              } else {
                // if (value) {
                //   if (!this.items_list_name[field.name][value.trim()]) {
                //     rowErrors.push(
                //       `${infoError}  القيمة "${value}" ليست ضمن القيم المسموحة`
                //     );
                //   } else {
                //     row[field.name] =
                //       this.items_list_name[field.name][value.trim()];
                //   }
                // }
              }
            });

            if (rowErrors.length > 0) {
              errors.push(...rowErrors);
            }
          });

          this.errors_validata = errors;

          // let r = this.value_model;

          if (errors.length > 0) this.$emit("process-export", [], true);
          else this.$emit("process-export", json, false);
        };

        reader.onerror = reject;
        reader.readAsArrayBuffer(this.uploadedFile);
      });
    },

    generatedValid(field, is_arabic = true) {
      let list = [];

      if ("null" in field && !field.null)
        list.push(
          is_arabic ? "لايمكن ان يكون فارغاََ" : "This field is required"
        );

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
            `${
              is_arabic ? "أقل قيمة يمكن قبولها" : "Minimum acceptable value"
            }   ${field.min_value}`
          );

        if ("max_value" in field && field.max_value)
          list.push(
            `${
              is_arabic ? "اكبر قيمة يمكن قبولها" : "Maximum acceptable value"
            }  ${field.max_value}`
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
  },
};
</script>

<style scoped>
/* ══════════════════════════════════════════════════════
   ImportExcel — Enterprise Design System (v2)
   All values use CSS Design Tokens
══════════════════════════════════════════════════════ */

.import-excel-root { font-family: 'Tajawal', sans-serif; }

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
.steps-track__line--done { background: rgb(var(--v-theme-primary)); }

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
.steps-track__bubble--done { background: rgb(var(--v-theme-primary)); }
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
.steps-track__label--active { color: rgb(var(--v-theme-primary)); font-weight: 700; }
.steps-track__label--done  { color: rgba(var(--v-theme-primary), 0.6); }

.import-header-divider { opacity: 0.06; }

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
.step-title { font-size: 1.15rem; font-weight: 700; color: rgb(var(--v-theme-on-surface)); margin: 0; }
.step-description { font-size: 0.9rem; color: rgba(var(--v-theme-on-surface), 0.6); max-width: 360px; line-height: 1.6; margin: 0; }
.import-btn-primary { border-radius: var(--radius-lg) !important; min-width: 160px; }

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
.error-state-text { font-size: 0.9rem; color: rgb(var(--v-theme-error)); font-weight: 500; }

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
.s2-header__title { font-size: 0.9rem; font-weight: 700; color: rgb(var(--v-theme-on-surface)); }
.s2-header__sub { font-size: 0.78rem; color: rgba(var(--v-theme-on-surface), 0.55); }

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
.field-rule-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
.field-rule-card--req { border-color: rgba(var(--v-theme-error), 0.15); }
.field-rule-card__top-bar { height: 3px; }
.field-rule-card--req .field-rule-card__top-bar { background: rgb(var(--v-theme-error)); }
.field-rule-card--opt .field-rule-card__top-bar { background: rgba(var(--v-theme-on-surface), 0.1); }

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
.field-rule-card__name { font-size: 0.82rem; font-weight: 700; color: rgb(var(--v-theme-on-surface)); flex: 1; }
.field-rule-card__body { padding: var(--space-sm); display: flex; flex-direction: column; gap: 4px; }
.rule-line {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.78rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  line-height: 1.4;
}

/* ══ Step 3: Upload Dropzone ══ */
.step-pane--upload { gap: var(--space-lg); }

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
.upload-dropzone__icon-wrap--ok { background: rgba(var(--v-theme-success), 0.07); }
.upload-dropzone__texts { text-align: center; }
.upload-dropzone__main { font-size: 0.9rem; font-weight: 600; color: rgb(var(--v-theme-on-surface)); }
.upload-dropzone__sub { font-size: 0.78rem; color: rgba(var(--v-theme-on-surface), 0.4); margin-top: 4px; }
.upload-dropzone__input { width: 100%; }

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
.val-errors__head-left { display: flex; align-items: center; gap: var(--space-xs); }
.val-errors__title { font-size: 0.85rem; font-weight: 700; color: rgb(var(--v-theme-error)); }
.val-errors__list { max-height: 160px; overflow-y: auto; }
.val-errors__row {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-md);
  border-bottom: 1px solid rgba(var(--v-theme-error), 0.05);
  font-size: 0.82rem;
}
.val-errors__row:last-child { border-bottom: none; }
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
.val-errors__msg { color: rgba(var(--v-theme-on-surface), 0.75); line-height: 1.5; }

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
.upload-ready__title { font-size: 0.875rem; font-weight: 700; color: rgb(var(--v-theme-success)); }
.upload-ready__sub { font-size: 0.78rem; color: rgba(var(--v-theme-success), 0.7); }

/* ══ Footer ══ */
.import-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  background: rgb(var(--v-theme-surface));
}
.import-footer__dots { display: flex; gap: 6px; align-items: center; }
.import-footer__dot {
  width: 7px;
  height: 7px;
  border-radius: var(--radius-full);
  background: rgba(var(--v-theme-on-surface), 0.15);
  transition: all 0.25s ease;
}
.import-footer__dot--active { width: 20px; background: rgb(var(--v-theme-primary)); }
.import-footer__dot--done   { background: rgba(var(--v-theme-primary), 0.4); }

.import-btn-nav    { border-radius: var(--radius-lg) !important; }
.import-btn-submit { border-radius: var(--radius-lg) !important; min-width: 140px; }

/* ══ Scrollbar ══ */
.val-errors__list::-webkit-scrollbar,
.fields-grid::-webkit-scrollbar { width: 4px; }
.val-errors__list::-webkit-scrollbar-track,
.fields-grid::-webkit-scrollbar-track { background: transparent; }
.val-errors__list::-webkit-scrollbar-thumb,
.fields-grid::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: var(--radius-full);
}
</style>
