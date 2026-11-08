<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="920px"
    scrollable
  >
    <v-card class="rounded-2xl overflow-hidden bg-surface elevation-12">
      <!-- ── شريط الإجراءات والتحكم العلوي (مخفي عند الطباعة) ── -->
      <div class="d-print-none px-5 py-3.5 d-flex align-center justify-space-between border-b bg-surface">
        <div class="d-flex align-center gap-2.5">
          <v-avatar color="primary" variant="tonal" size="38" rounded="lg">
            <v-icon size="20" color="primary">mdi-file-document-check-outline</v-icon>
          </v-avatar>
          <div>
            <div class="font-weight-black text-subtitle-2 text-high-emphasis">
              استمارة إذن الصرف وأمر الطباعة الرسمي
            </div>
            <div class="text-caption text-medium-emphasis">
              وثيقة معتمدة وموجهة للمطبعة المنفذة ومحضر استلام رسمي
            </div>
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            size="small"
            class="font-weight-bold px-4"
            prepend-icon="mdi-printer"
            @click="triggerPrint"
          >
            طباعة المستند (A4)
          </v-btn>

          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            density="comfortable"
            color="medium-emphasis"
            rounded="lg"
            @click="$emit('update:modelValue', false)"
          />
        </div>
      </div>

      <!-- ── مساحة المستند الرسمي القابل للطباعة ── -->
      <v-card-text class="pa-4 pa-sm-8 bg-grey-lighten-4 overflow-y-auto" style="max-height: 80vh;">
        <div id="printableManifest" class="official-manifest-sheet mx-auto bg-white pa-6 pa-sm-10 rounded-xl border elevation-2" dir="rtl">
          <!-- 1. ترويسة الوزارة واللجنة العليا للاختبارات -->
          <div class="manifest-header text-center pb-4 mb-4 border-b-2">
            <h3 class="ministry-title mb-1 font-weight-bold">الجمهورية اليمنية — وزارة التربية والتعليم</h3>
            <h4 class="committee-title mb-2 text-medium-emphasis">اللجنة العليا للاختبارات — الإدارة العامة للامتحانات والنظام والمراقبة</h4>
            <div class="manifest-headline py-1 px-4 d-inline-block rounded-lg my-2">
              إذن صرف وأمر طباعة رسمي للاختبارات العامة
            </div>
            <div class="order-code-badge mt-2 font-mono font-weight-black">
              رقم أمر الطباعة: {{ orderData.orderNumber }}
            </div>
          </div>

          <!-- 2. بطاقة بيانات الاختبار والجدولة الزمنية -->
          <div class="meta-section pa-3 rounded-lg mb-4 border">
            <v-row dense>
              <v-col cols="12" sm="6">
                <div class="meta-item mb-1.5">
                  <span class="meta-label">اسم الاختبار:</span>
                  <strong class="meta-value text-high-emphasis">{{ orderData.examTitle }}</strong>
                </div>
                <div class="meta-item mb-1.5">
                  <span class="meta-label">المرحلة / المادة:</span>
                  <span class="meta-value">{{ orderData.stageName }} — {{ orderData.subjectName }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">كود الاختبار:</span>
                  <span class="meta-value font-mono">{{ orderData.examCode }}</span>
                </div>
              </v-col>

              <v-col cols="12" sm="6">
                <div class="meta-item mb-1.5">
                  <span class="meta-label">المطبعة المنفذة:</span>
                  <strong class="meta-value text-primary">{{ orderData.facility }}</strong>
                </div>
                <div class="meta-item mb-1.5">
                  <span class="meta-label">موعد الطباعة المجدول:</span>
                  <span class="meta-value font-mono">{{ orderData.printDate || '—' }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">موعد الامتحان الفعلي:</span>
                  <span class="meta-value font-mono">{{ orderData.examDate || '—' }}</span>
                </div>
              </v-col>
            </v-row>
          </div>

          <!-- نطاق التنفيذ المعتمد -->
          <div class="scope-notice pa-2 px-3 rounded-lg mb-4 border text-caption">
            <strong>نطاق التنفيذ المعتمد:</strong>
            {{ orderData.scopeSummary }}
            ({{ orderData.schoolsCount }} مراكز امتحانية | {{ orderData.studentsCount }} طالباً مقيداً)
          </div>

          <!-- 3. جدول توزيع الطلاب على النماذج (توزيع آلي 100%) -->
          <div class="table-section mb-4">
            <h5 class="section-title mb-2 font-weight-black">
              1. جدول توزيع الطلاب على النماذج الامتحانية (توزيع متكافئ 100%)
            </h5>
            <table class="manifest-table">
              <thead>
                <tr>
                  <th style="width: 18%;">رمز النموذج</th>
                  <th style="width: 20%;">الطلاب المقيدون</th>
                  <th style="width: 18%;">كراسات الأسئلة</th>
                  <th style="width: 18%;">أوراق إجابة OMR</th>
                  <th style="width: 14%;">احتياط الطوارئ</th>
                  <th style="width: 12%;">نسبة التمثيل</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="v in orderData.versionsRows" :key="v.version_code">
                  <td class="text-center font-weight-bold">النموذج {{ v.version_code }}</td>
                  <td class="text-center font-mono">{{ v.student_count }}</td>
                  <td class="text-center font-mono">{{ v.booklets }}</td>
                  <td class="text-center font-mono">{{ v.sheets }}</td>
                  <td class="text-center font-mono" dir="ltr">+{{ v.reserve_quota }}</td>
                  <td class="text-center font-mono" dir="ltr">{{ v.percentage }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 4. جدول حصر الكميات المعتمدة للطباعة والصرف -->
          <div class="table-section mb-4">
            <h5 class="section-title mb-2 font-weight-black">
              2. حصر الكميات المعتمدة للطباعة والصرف
            </h5>
            <table class="manifest-table">
              <thead>
                <tr>
                  <th style="width: 40%;">المادة المطلوب طباعتها</th>
                  <th style="width: 20%;">الكمية الأساسية (للطلاب)</th>
                  <th style="width: 20%;">احتياط الطوارئ (عام)</th>
                  <th style="width: 20%;">إجمالي الكمية المعتمدة</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="m in orderData.materialsRows" :key="m.id">
                  <td class="font-weight-bold">{{ m.material_name }}</td>
                  <td class="text-center font-mono">{{ m.base_qty }}</td>
                  <td class="text-center font-mono" dir="ltr">+{{ m.reserve_qty }}</td>
                  <td class="text-center font-mono font-weight-bold text-primary">{{ m.total_qty }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="totals-row font-weight-black">
                  <td>الإجمالي العام المعتمد للصرف</td>
                  <td class="text-center font-mono">{{ orderData.baseTotal }}</td>
                  <td class="text-center font-mono" dir="ltr">+{{ orderData.reserveTotal }}</td>
                  <td class="text-center font-mono text-primary font-weight-black">{{ orderData.grandTotal }} ورقة/كراسة</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <!-- 5. توثيق تفويض الزيادة والاحتياط (إن وجد) -->
          <div v-if="orderData.hasSurplus" class="surplus-box pa-3 rounded-lg mb-4 border">
            <div class="d-flex align-center gap-1.5 font-weight-bold mb-1 text-caption text-warning-darken-3">
              <v-icon size="16" color="warning-darken-3">mdi-shield-check-outline</v-icon>
              <span>توثيق وتفويض الكمية الإضافية (احتياط طوارئ رسمي معتمد):</span>
            </div>
            <div class="text-caption mb-1">
              <strong>السبب المعتمد:</strong> {{ orderData.surplusReason || '—' }}
            </div>
            <div class="text-caption mb-1">
              <strong>رقم وتاريخ مذكرة الاعتماد:</strong> {{ orderData.surplusAuthDoc || '—' }}
            </div>
            <div v-if="orderData.notes" class="text-caption">
              <strong>توجيهات لجنة المطبعة:</strong> {{ orderData.notes }}
            </div>
          </div>

          <!-- 6. خانات التوقيع والاعتماد الرسمية الثلاثية -->
          <div class="signatures-grid mt-8 pt-4 border-t">
            <div class="sig-col text-center">
              <div class="sig-title font-weight-bold mb-8">مسؤول إعداد وتجهيز الطلب</div>
              <div class="sig-dots">التوقيع: ....................................</div>
            </div>
            <div class="sig-col text-center">
              <div class="sig-title font-weight-bold mb-8">رئيس لجنة النظام والمراقبة (الكنترول)</div>
              <div class="sig-dots">التوقيع والختم: ....................................</div>
            </div>
            <div class="sig-col text-center">
              <div class="sig-title font-weight-bold mb-8">مدير عام المطبعة السرية (الاستلام)</div>
              <div class="sig-dots">التوقيع والختم: ....................................</div>
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Boolean, default: false },
  orderData: {
    type: Object,
    default: () => ({
      orderNumber: '',
      examTitle: '',
      stageName: '',
      subjectName: '',
      examCode: '',
      facility: '',
      printDate: '',
      examDate: '',
      scopeSummary: '',
      schoolsCount: 0,
      studentsCount: 0,
      versionsRows: [],
      materialsRows: [],
      baseTotal: 0,
      reserveTotal: 0,
      grandTotal: 0,
      hasSurplus: false,
      surplusReason: '',
      surplusAuthDoc: '',
      notes: '',
    }),
  },
})

defineEmits(['update:modelValue'])

const triggerPrint = () => {
  const manifestEl = document.getElementById('printableManifest')
  if (!manifestEl) {
    window.print()
    return
  }

  const existingFrame = document.getElementById('manifest-print-frame')
  if (existingFrame) existingFrame.remove()

  const iframe = document.createElement('iframe')
  iframe.id = 'manifest-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (doc) {
    doc.open()
    doc.write(`
      <!DOCTYPE html>
      <html dir="rtl" lang="ar">
      <head>
        <meta charset="utf-8">
        <title>إذن صرف وأمر طباعة رسمي - ${props.orderData?.orderNumber || ''}</title>
        <style>
          @page { size: A4 portrait; margin: 10mm; }
          *, *::before, *::after { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
          body { font-family: 'Amiri', 'Traditional Arabic', 'Cairo', Tahoma, Arial, sans-serif; margin: 0; padding: 0; color: #000; background: #fff; }
          .d-print-none { display: none !important; }
          .official-manifest-sheet { width: 100% !important; max-width: 100% !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
          .border-b-2 { border-bottom: 2px solid #000; }
          .manifest-header { text-align: center; }
          .ministry-title { font-size: 16px; font-weight: bold; margin: 0 0 4px 0; }
          .committee-title { font-size: 13px; color: #444; margin: 0 0 6px 0; }
          .manifest-headline { font-size: 18px; font-weight: 900; border: 2px solid #000; display: inline-block; padding: 4px 16px; border-radius: 6px; margin: 6px 0; }
          .order-code-badge { font-family: monospace; font-size: 13px; font-weight: bold; margin-top: 6px; }
          table { width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 12px; }
          th, td { border: 1px solid #333; padding: 6px 8px; text-align: right; }
          th { background: #f0f0f0; font-weight: bold; text-align: center; }
          .font-mono { font-family: monospace; }
          .signatures-grid, .d-flex { display: flex; }
          .justify-space-between { justify-content: space-between; }
        </style>
      </head>
      <body>
        ${manifestEl.outerHTML}
      </body>
      </html>
    `)
    doc.close()

    setTimeout(() => {
      try {
        iframe.contentWindow?.focus()
        iframe.contentWindow?.print()
      } catch (err) {
        window.print()
      }
    }, 200)
  } else {
    window.print()
  }
}
</script>

<style scoped>
.official-manifest-sheet {
  max-width: 820px;
  color: #0f172a;
  font-family: inherit;
}

.border-b-2 {
  border-bottom: 2px solid #0f172a;
}

.ministry-title {
  font-size: 1.05rem;
  color: #0f172a;
}

.committee-title {
  font-size: 0.9rem;
}

.manifest-headline {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  font-weight: 800;
  font-size: 1.05rem;
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
}

.order-code-badge {
  font-size: 0.85rem;
  color: #475569;
}

.meta-section {
  background: #f8fafc;
  border-color: #e2e8f0 !important;
}

.meta-label {
  font-size: 0.8rem;
  color: #64748b;
  margin-inline-end: 6px;
}

.meta-value {
  font-size: 0.85rem;
}

.scope-notice {
  background: #f1f5f9;
  border-color: #cbd5e1 !important;
}

.section-title {
  font-size: 0.88rem;
  color: #1e293b;
}

.manifest-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.manifest-table th {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  padding: 8px 10px;
  font-weight: 800;
  color: #1e293b;
}

.manifest-table td {
  border: 1px solid #e2e8f0;
  padding: 8px 10px;
  vertical-align: middle;
}

.totals-row {
  background: #f8fafc;
  border-top: 2px solid #cbd5e1;
}

.surplus-box {
  background: #fffbeb;
  border-color: #fde68a !important;
}

.text-warning-darken-3 {
  color: #b45309 !important;
}

.signatures-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.sig-title {
  font-size: 0.82rem;
  color: #334155;
}

.sig-dots {
  font-size: 0.78rem;
  color: #94a3b8;
}

/* ══════════════════════════════════════════════════════
   PRINT STYLES (@media print)
══════════════════════════════════════════════════════ */
@media print {
  .d-print-none {
    display: none !important;
  }

  body * {
    visibility: hidden;
  }

  #printableManifest, #printableManifest * {
    visibility: visible;
  }

  #printableManifest {
    position: absolute;
    left: 0;
    top: 0;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 20px !important;
    border: none !important;
    box-shadow: none !important;
    background: #fff !important;
  }
}
</style>
