# 📘 دليل المبرمج لاستخدام وتكامل الهيدر والفوتر (Developer Integration Guide)

يقدم هذا الدليل شرحاً عملياً وشاملاً للمبرمجين حول كيفية استخدام وتكامل وحدة **الهيدر والفوتر (Header & Footer)** في شاشات وتقارير النظام، وتوليد كود الطباعة، وتمرير البيانات المخصصة، واستخدام المكونات الجاهزة.

---

## 📑 الفهرس

1. [تضمين شاشة المحرر في النظام (Full Builder View)](#1-تضمين-شاشة-المحرر-في-النظام)
2. [استخدام نافذة اختيار القالب في شاشة أو تقرير (`HfTemplateSelectDialog`)](#2-استخدام-نافذة-اختيار-القالب-في-التقارير)
3. [توليد كود الـ HTML برمجياً للطباعة والـ PDF](#3-توليد-كود-الـ-html-برمجياً-للطباعة-والـ-pdf)
4. [تمرير بيانات ديناميكية مخصصة للتقرير (Dynamic Injection)](#4-تمرير-بيانات-ديناميكية-مخصصة-للتقرير)
5. [استرجاع القالب المخصص لشاشة معينة (Screen Assignment)](#5-استرجاع-القالب-المخصص-لشاشة-معينة)
6. [تنسيق صفحة الطباعة والـ CSS للتقارير (Print Styles)](#6-تنسيق-صفحة-الطباعة-والـ-css-للتقارير)
7. [إضافة وتوسيع المتغيرات (Custom Variables)](#7-إضافة-وتوسيع-المتغيرات)
8. [أمثلة عملية كاملة (Practical Examples)](#8-أمثلة-عملية-كاملة)

---

## 1. تضمين شاشة المحرر في النظام

إذا كنت تريد إضافة شاشة إدارة وتصميم الهيدر والفوتر كصفحة كاملة في تطبيقك:

### أ) عبر مسارات التوجيه (Vue Router):
```javascript
// router/index.js
{
  path: '/settings/header-footer-builder',
  name: 'HeaderFooterBuilder',
  component: () => import('@/headerandfooter/HeaderFooterBuilder.vue'),
  meta: {
    title: 'إدارة الهيدر والفوتر',
    requiresAuth: true
  }
}
```

### ب) كتضمين مباشر في صفحة إعدادات:
```vue
<template>
  <div class="settings-page">
    <HeaderFooterBuilder />
  </div>
</template>

<script setup>
import HeaderFooterBuilder from '@/headerandfooter/HeaderFooterBuilder.vue'
</script>
```

---

## 2. استخدام نافذة اختيار القالب في التقارير

يتيح مكون `HfTemplateSelectDialog` للمستخدم اختيار قالب هيدر وفوتر معين للتقرير الحالي مع عرض معاينة مباشرة قبل الاعتماد.

```vue
<template>
  <div>
    <!-- زر فتح نافذة الاختيار -->
    <v-btn
      color="primary"
      variant="tonal"
      prepend-icon="mdi-page-layout-header-footer"
      @click="isSelectOpen = true"
    >
      تخصيص ترويسة التقرير
    </v-btn>

    <!-- نافذة الاختيار والمعاينة -->
    <HfTemplateSelectDialog
      v-model="isSelectOpen"
      :initial-template-id="currentTemplateId"
      @confirm="onTemplateConfirmed"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HfTemplateSelectDialog from '@/headerandfooter/components/HfTemplateSelectDialog.vue'

const isSelectOpen = ref(false)
const currentTemplateId = ref('tpl-default')

// الدالة التي تستقبل القالب المختار وكود الـ HTML المولد
const onTemplateConfirmed = ({ templateId, template, html }) => {
  currentTemplateId.value = templateId
  console.log('معرف القالب:', templateId)
  console.log('اسم القالب:', template.name)
  console.log('كود الهيدر:', html.header)
  console.log('كود الفوتر:', html.footer)
}
</script>
```

---

## 3. توليد كود الـ HTML برمجياً للطباعة والـ PDF

يمكنك استخدام المتجر `useHeaderFooterStore` لتوليد كود الـ HTML النقي المجهز للطباعة لأي قالب:

```javascript
import { useHeaderFooterStore } from '@/headerandfooter/stores/useHeaderFooterStore'

const hfStore = useHeaderFooterStore()

// 1. توليد كود الـ HTML للقالب النشط
const activeHtml = hfStore.generateHTML(hfStore.activeTemplateId)
console.log(activeHtml.header) // كود الـ HTML للهيدر
console.log(activeHtml.footer) // كود الـ HTML للفوتر

// 2. أو توليد كود الـ HTML باستخدام كائن القالب مباشرة
const template = hfStore.templates[0]
const customHtml = hfStore.generateHTMLForTemplate(template)
```

---

## 4. تمرير بيانات ديناميكية مخصصة للتقرير

عند طباعة تقرير أو فاتورة، قد تحتاج لتمرير بيانات خاصة بتلك الفاتورة تحديداً (مثل: رقم الفاتورة، اسم العميل، التاريخ، الشعار المخصص) لاستبدال المتغيرات:

```javascript
import { useHeaderFooterStore } from '@/headerandfooter/stores/useHeaderFooterStore'

const hfStore = useHeaderFooterStore()

// كائن البيانات المخصصة للتقرير الحالي
const invoiceData = {
  '{{reportNo}}': 'INV-2026-8899',
  '{{pageTitle}}': 'فاتورة مبيعات ضريبية',
  '{{userName}}': 'أحمد المنصور',
  '{{branch_name}}': 'فرع جدة - طريق الملك عبدالعزيز',
  '{{tax_number}}': '310998877600003',
  '{{date}}': '2026/09/07',
  '{{time}}': '10:30 ص',
  // يمكن أيضاً تمرير صورة مخصصة (URL أو Base64)
  '{{organizationLogo}}': 'https://example.com/custom-logo.png'
}

// توليد الـ HTML مع دمج البيانات المخصصة
const reportHtml = hfStore.generateHTML(templateId, invoiceData)
```

---

## 5. استرجاع القالب المخصص لشاشة معينة

إذا قام المستخدم بتخصيص قالب لشاشة معينة (عبر شاشة `HfAssignScreenDialog`):

```javascript
// استرجاع تخصيصات الشاشات المحفوظة من التخزين المحلي
export const getAssignedTemplateForScreen = (screenId) => {
  try {
    const raw = localStorage.getItem('hf_screen_assignments')
    const assignments = raw ? JSON.parse(raw) : {}
    return assignments[screenId] || null // يرجع templateId المخصص لهذه الشاشة
  } catch (e) {
    console.error('Error loading template assignment:', e)
    return null
  }
}

// مثال الاستخدام داخل شاشة فاتورة المبيعات:
const screenTemplateId = getAssignedTemplateForScreen('sales-invoice')
```

---

## 6. تنسيق صفحة الطباعة والـ CSS للتقارير

لضمان ظهور الهيدر في أعلى كل ورقة مطبوعة والفوتر في أسفلها بشكل سليم:

```html
<!-- هيكل صفحة التقرير أو الفاتورة -->
<div class="print-page-container">
  <!-- 1. الهيدر المولد -->
  <header class="report-header" v-html="reportHtml.header" />

  <!-- 2. محتوى التقرير الأساسي (الجداول والبيانات) -->
  <main class="report-body">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>اسم الصنف</th>
          <th>الكمية</th>
          <th>السعر</th>
          <th>الإجمالي</th>
        </tr>
      </thead>
      <tbody>
        <!-- بيانات الأصناف -->
      </tbody>
    </table>
  </main>

  <!-- 3. الفوتر المولد -->
  <footer class="report-footer" v-html="reportHtml.footer" />
</div>
```

### تنسيقات الـ CSS الموصى بها للطباعة (`@media print`):
```css
 

  body {
    background: #ffffff !important;
    color: #000000 !important;
  }

  .print-page-container {
    width: 100%;
    margin: 0;
    padding: 0;
  }

  .report-header {
    width: 100%;
    margin-bottom: 8mm;
  }

  .report-footer {
    width: 100%;
    margin-top: 8mm;
  }

  /* منع انقسام الجداول داخل الصفحة */
  table, tr, td {
    page-break-inside: avoid;
  }
}
```

---

## 7. إضافة وتوسيع المتغيرات

### أ) إضافة متغير ثابت جديد في المتجر:
افتح الملف [`src/headerandfooter/stores/useHeaderFooterStore.js`](file:///c:/Users/samer/Desktop/vuetifyCore/src/headerandfooter/stores/useHeaderFooterStore.js) وأضف المتغير إلى مصفوفة `STATIC_VARIABLES`:
```javascript
{
  key: '{{customField}}',
  label: 'الحقل المخصص',
  icon: 'mdi-star-outline',
  color: 'purple',
  value: 'القيمة الافتراضية'
}
```

### ب) وسوم الصور المتقدمة (Image Tokens):
تدعم وسوم الصور التنسيق التالي تلقائياً:
`{{variableKey|width|height|shape|opacity|objectFit}}`

* **أمثلة على الأشكال (`shape`)**:
  - `default`: عادي مع حواف ناعمة.
  - `stamp-double`: ختم وزاري مزدوج بلون رسمي.
  - `circle`: دائري منتظم.
  - `badge`: شارة ووسام رسمي.
  - `frame`: إطار ذهبي ملكي.
  - `glow`: توهج نيون حديث.
  - `squircle`: زوايا فائقة النعومة.
* **ملاءمة الصورة (`objectFit`)**: `contain`, `cover`, `fill`, `none`, `scale-down`.

---

## 8. أمثلة عملية كاملة

### مثال: صفحة تقرير كاملة متكاملة مع الهيدر والفوتر والطباعة

```vue
<template>
  <div class="sales-report-page pa-6" dir="rtl">
    <!-- شريط التحكم العلوي -->
    <div class="d-flex align-center justify-space-between mb-4 no-print">
      <h2 class="text-h6 font-weight-bold">تقرير المبيعات اليومية</h2>
      <div class="d-flex ga-2">
        <v-btn
          color="primary"
          variant="tonal"
          prepend-icon="mdi-page-layout-header-footer"
          @click="selectDialog = true"
        >
          تغيير ترويسة التقرير
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-printer"
          @click="printReport"
        >
          طباعة التقرير
        </v-btn>
      </div>
    </div>

    <!-- ورقة التقرير المطبوعة -->
    <v-card class="report-paper pa-6 elevation-1">
      <!-- ترويسة التقرير (الهيدر) -->
      <div v-html="renderedHtml.header" class="mb-4" />

      <!-- بيانات التقرير -->
      <div class="report-content my-6">
        <v-table density="compact" class="border">
          <thead>
            <tr>
              <th>#</th>
              <th>البيان</th>
              <th>الفرع</th>
              <th>المبلغ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in 5" :key="i">
              <td>{{ i }}</td>
              <td>مبيعات نقدية - نقطة بيع {{ i }}</td>
              <td>الفرع الرئيسي</td>
              <td>{{ (i * 1250).toLocaleString() }} ر.س</td>
            </tr>
          </tbody>
        </v-table>
      </div>

      <!-- تذييل التقرير (الفوتر) -->
      <div v-html="renderedHtml.footer" class="mt-4" />
    </v-card>

    <!-- نافذة اختيار القالب -->
    <HfTemplateSelectDialog
      v-model="selectDialog"
      :initial-template-id="activeTemplateId"
      @confirm="onTemplateSelected"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useHeaderFooterStore } from '@/headerandfooter/stores/useHeaderFooterStore'
import HfTemplateSelectDialog from '@/headerandfooter/components/HfTemplateSelectDialog.vue'

const hfStore = useHeaderFooterStore()
const selectDialog = ref(false)
const activeTemplateId = ref(null)

onMounted(async () => {
  await hfStore.fetchApiVariables()
  if (hfStore.templates.length > 0) {
    activeTemplateId.value = hfStore.templates[0].id
  }
})

// توليد الـ HTML مع حقن البيانات اللحظية
const renderedHtml = computed(() => {
  const dynamicSample = {
    '{{pageTitle}}': 'تقرير المبيعات اليومية',
    '{{date}}': new Date().toLocaleDateString('ar-SA'),
    '{{reportNo}}': 'RPT-2026-901'
  }
  return hfStore.generateHTML(activeTemplateId.value, dynamicSample)
})

const onTemplateSelected = ({ templateId }) => {
  activeTemplateId.value = templateId
}

const printReport = () => {
  window.print()
}
</script>

<style scoped>
.report-paper {
  background: #ffffff;
  min-height: 800px;
  max-width: 900px;
  margin: 0 auto;
}

@media print {
  .no-print {
    display: none !important;
  }
  .report-paper {
    box-shadow: none !important;
    padding: 0 !important;
  }
}
</style>
```

---

> 💡 **نصيحة للمطورين**: يمكنك دائماً مراجعة ملف [`README.md`](file:///c:/Users/samer/Desktop/vuetifyCore/src/headerandfooter/README.md) للاطلاع على الوصف البنيوي لكافة ملفات ومكونات النظام.
