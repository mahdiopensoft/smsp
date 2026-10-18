<template>
  <v-locale-provider :rtl="true">
 
    <v-sheet>
      <VCol>
        <VForm ref="valid">
          <VRow justify="end">
            <custom-btn
              :type="props.item.id ? 'update' : 'save'"
              :click="saveContent"
            />
          </VRow>

          <VRow>
            <custom-text-field
              v-model="name_section"
              label="الاسم"
              :rules="[$required,$max_length(255)]"
              cols="3"

            />

            <custom-text-field
              v-model.number="number_row.header"
              type="number"
              min="1"
              max="12"
              label=" عدد الاعمد لرأس الصفحة  "
              variant="outlined"
              cols="3"
              :rules="[$max_value(12)]"
            />
            <custom-text-field
              v-model.number="number_row.footer"
              type="number"
              min="1"
              max="12"
              label="عدد الاعمد لذيل الصفحة  "
              variant="outlined"
              cols="3"
              :rules="[$max_value(12)]"
            />
          </VRow>
        </VForm>

        <v-row justify="center">
          <v-col cols="12">
            <v-card class="pa-3">
              <v-card-title>🔖 المتغيرات (اسحب وأفلت داخل المحرر)</v-card-title>
              <v-divider></v-divider>
              <v-row class="pa-2">
                <v-list-item
                  v-for="variable in variables"
                  :key="variable.name_ar"
                  :draggable="true"
                  @dragstart="onDragStart($event, variable.name_ar)"
                  style="cursor: grab; user-select: none"
                >
                  <v-chip class="ma-1" color="primary" label>
                    {{ variable.name_ar }}
                  </v-chip>
                </v-list-item>
              </v-row>
              <v-row class="pa-2">

                <v-list-item
                 v-for="(value,key) in dynamicVariables"
                  :key="key"
                  :draggable="true"
                  @dragstart="onDragStart($event, value.name_ar)"
                  style="cursor: grab; user-select: none"
                >
                  <v-chip class="ma-1" color="primary" label>
                    {{ value.name_ar }}
                  </v-chip>
                </v-list-item>

              </v-row>
            </v-card>

            <v-card class="pa-4">
              <v-card-text>
                <v-expansion-panels
                  v-for="i in ['header', 'footer']"
                  :key="i"
                  class="mt-2"
                >
                  <v-expansion-panel :title="i">
                    <v-expansion-panel-text>
                      <v-row>
                        <v-col
                          v-for="(n, index) in validCount(i)"
                          :key="index"
                          cols="12"
                          :md="colSize(i)"
                        >
                          <v-card class="pa-2" variant="outlined">
                            <div class="text-caption mb-2 text-grey">
                              محرر رقم {{ index + 1 }}
                            </div>

                            <div
                              class="editor-container rtl-editor"
                              @drop.prevent="onDrop($event, index, i)"
                              @dragover.prevent
                            >

                              <CustomQuillEditor
                                :refEditor="(el) => (editorRefs[i][index] = el)"
                                v-model:content="content[i][index]"
                                content-type="html"
                                theme="snow"
                                toolbar="minimal"
                                style="min-height: 200px"
                                placeholder="اكتب النص هنا أو اسحب متغير..."
                              />
                            </div>
                          </v-card>
                        </v-col>
                      </v-row> </v-expansion-panel-text></v-expansion-panel
                ></v-expansion-panels>
              </v-card-text>
            </v-card>

            <v-card
              class="pa-4 mt-4"
              dir="rtl"
              v-for="i in ['header', 'footer']"
              :key="i"
            >
              <v-card-title class="rtl-preview"
                >📄 المعاينة الحية لل {{ i }}</v-card-title
              >
              <v-divider></v-divider>
              <v-card-text class="rtl-preview">
                <preview-content-html :items="content[i]" :variables="dynamicVariables" />
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </VCol>
    </v-sheet>
  </v-locale-provider>
</template>

<script setup>
import { ref, onMounted, onBeforeUpdate, onBeforeMount } from "vue";
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css"; // استيراد ستايل Quill
import Quill from "quill";
import api from "../../../plugins/axios-plugin";

 import { alert, showAlert } from "../../utils/Globals";
import {useHeaderFooterStore} from "../../stores/headerFooterStore"

const emit = defineEmits(["update:modelValue"]);

 const props = defineProps({
  item: { type: Object, type: null },
  getData: Function,
});

// --- الحالة (State) ---
const headerFooterStore = useHeaderFooterStore();

let dynamicVariables =headerFooterStore.listVariables;
const variables = headerFooterStore.localVariables;

 

 
const valid = ref(null);
const name_section = ref(props?.item?.name);
const content = ref({ header: [], footer: [] });
// مصفوفة لتخزين مراجع المحررات
const editorRefs = ref({
  header: [],
  footer: [],
});

const copy_header = props?.item?.header
  ? JSON.parse(props?.item?.header)
  : null;
const copy_footer = props?.item?.footer
  ? JSON.parse(props?.item?.footer)
  : null;

if (copy_header) content.value.header = copy_header;
if (copy_footer) content.value.footer = copy_footer;

const number_row = ref({
  header: copy_header?.length || 1,
  footer: copy_footer?.length || 1,
});
const draggedVariable = ref(null);



// --- تأكد من تنظيف المراجع قبل التحديث ---
onBeforeUpdate(() => {
  editorRefs.value.header = [];
  editorRefs.value.footer = [];
});

function validCount(key) {
  const n = Number(number_row.value[key]);
  // السماح من 1 إلى 12 محرر
  return Number.isFinite(n) && n > 0 ? Math.min(n, 12) : 1;
}

function colSize(key) {
  const count = validCount(key);
  // إذا كان عدد المحررات 4 أو أقل، قم بتوزيعها بالتساوي على السطر
  if (count <= 4) {
    return Math.floor(12 / count);
  }
  // إذا زاد العدد عن 4، اجعل عرض العمود 3 (وهو ما يعني 4 أعمدة في الصف الواحد)
  // وباقي المحررات ستنتقل تلقائياً للسطر التالي
  return 3;
}

// --- تسجيل الـ Blot المخصص (مرة واحدة) ---
const Embed = Quill.import("blots/embed");

class VariableBlot extends Embed {
  static create(value) {
    const node = super.create();
    node.setAttribute("data-name", value);
    // العرض داخل المحرر
    node.innerText = value;
    // تنسيق الـ Chip داخل المحرر
    Object.assign(node.style, {
      display: "inline-block",
      backgroundColor: "#e3f2fd",
      color: "#1565c0",
      padding: "2px 6px",
      borderRadius: "12px",
      border: "1px solid #90caf9",
      fontSize: "0.9em",
      margin: "0 2px",
      cursor: "default",
      userSelect: "none",
      verticalAlign: "middle",
    });
    return node;
  }

  static value(node) {
    return node.getAttribute("data-name");
  }
}

VariableBlot.blotName = "variable";
VariableBlot.tagName = "span";
VariableBlot.className = "ql-variable";

// التسجيل الآمن لتجنب الأخطاء عند إعادة التحميل 
if (!Quill.imports["formats/variable"]) {
  Quill.register(VariableBlot);
}

// --- الدوال (Methods) ---

async function saveContent() {
  const isValid = await valid.value.validate();

  if (!isValid.valid) return;

  let url = "common/print-report-setting/";
  let type_request = "post";

  if (props?.item?.id) {
    url += `${props.item?.id}/`;
    type_request = "put";
  }

  await api[type_request](url, {
    name: name_section.value,
    header: JSON.stringify(content.value.header),
    footer: JSON.stringify(content.value.footer),
  });

  await props.getData();

  emit("update:modelValue", false);

  if (props.item?.id) {
    alert("update");
    showAlert();
  } else {
    alert("add");
    showAlert();
  }
}

function onDragStart(event, variableKey) {
  draggedVariable.value = variableKey;
  // تحسين السحب: تحديد شكل البيانات
  event.dataTransfer.effectAllowed = "copy";
  event.dataTransfer.setData("text/plain", `{{ ${variableKey} }}`);
}

function onDrop(event, index, key) {
  const editorComponent = editorRefs.value[key][index];
  if (!editorComponent || !draggedVariable.value) return;

  const quill = editorComponent.getQuill();

  // 1. تفعيل التركيز على المحرر لضمان عمل getSelection
  quill.focus();

  // 2. محاولة تحديد مكان المؤشر
  // ملاحظة: عند السحب والإفلات، المتصفح يعرف المكان، لكن Quill يحتاج لمساعدة لتحديد الـ Index الدقيق
  // الحل البسيط: الإدراج مكان المؤشر الحالي (الذي تم تفعيله بـ focus)
  // أو الإدراج في النهاية كحل احتياطي

  let range = quill.getSelection();
  let insertIndex = range ? range.index : quill.getLength();

  // الإدراج
  const varText = `{{ ${draggedVariable.value} }}`;
  quill.insertEmbed(insertIndex, "variable", varText);

  // وضع مسافة بعد المتغير وتحريك المؤشر
  quill.insertText(insertIndex + 1, " ");
  quill.setSelection(insertIndex + 2);

  // إعادة تعيين المتغير المسحوب
  draggedVariable.value = null;
}
 
</script>

<style>
/* دعم RTL للمحرر */
.rtl-editor .ql-editor {
  direction: rtl;
  text-align: right;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-size: 16px;
}

.rtl-editor .ql-container {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  background-color: #ffffff;
}

.rtl-editor .ql-toolbar {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  background-color: #f5f5f5;
}

/* تنسيق المعاينة */
.rtl-preview {
  direction: rtl;
  text-align: right;
}
</style>
