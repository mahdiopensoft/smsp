import { nextTick } from 'vue'
import { escapeHtml, sanitizePrintNode } from '../../utils/omrPrint'

/**
 * دالة طباعة مستند HTML عبر iframe مخفي ومعزول
 */
export function printHtmlViaHiddenIframe(
  html: string,
  iframeId = 'omr-hardware-print-frame',
  onError?: (msg: string) => void
): void {
  const existingFrame = document.getElementById(iframeId)
  if (existingFrame) existingFrame.remove()

  const iframe = document.createElement('iframe')
  iframe.id = iframeId
  iframe.style.position = 'fixed'
  iframe.style.left = '-10000px'
  iframe.style.top = '-10000px'
  iframe.style.width = '1024px'
  iframe.style.height = '768px'
  iframe.style.border = '0'
  iframe.style.opacity = '0.01'
  iframe.style.pointerEvents = 'none'
  iframe.style.zIndex = '-9999'
  iframe.setAttribute('aria-hidden', 'true')
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (!doc) {
    console.error(`[OMR Direct Print] Failed to access print iframe document (${iframeId})`)
    onError?.('تعذر إنشاء بيئة الطباعة المعزولة للمستند.')
    return
  }

  doc.open()
  doc.write(html)
  doc.close()

  let triggered = false
  const cleanup = () => {
    setTimeout(() => {
      if (document.body.contains(iframe)) {
        iframe.remove()
      }
    }, 1500)
  }

  const triggerIframePrint = () => {
    if (triggered) return
    triggered = true
    try {
      iframe.contentWindow?.addEventListener('afterprint', cleanup)
      iframe.contentWindow?.focus()
      iframe.contentWindow?.print()
    } catch (err) {
      console.error(`[OMR Direct Print] Iframe print failed (${iframeId}):`, err)
      onError?.('حدث خطأ أثناء استدعاء نافذة الطباعة للمستند المعزول.')
      cleanup()
    }
  }

  iframe.onload = () => {
    setTimeout(triggerIframePrint, 250)
  }
  setTimeout(triggerIframePrint, 700)
}

/**
 * دالة التحقق الحقيقي من اكتمال رسم أوراق OMR والباركود في الحاوية قبل الطباعة
 */
export const waitForBatchStagingReady = async (
  expectedCount: number,
  isAudit: boolean,
  maxWaitMs = 5000
): Promise<Element[]> => {
  if (expectedCount <= 0) return []

  const startTime = performance.now()
  const selector = isAudit ? '.yemeni-audit-report-sheet' : 'svg.yemeni-ministry-sheet-svg'
  const fallbackSelector = isAudit ? '.yemeni-audit-report-sheet' : 'svg'

  while (performance.now() - startTime < maxWaitMs) {
    await nextTick()
    await new Promise(resolve => requestAnimationFrame(resolve))

    const stagingEl = document.getElementById('omr-registry-batch-staging')
    if (stagingEl) {
      let elements = Array.from(stagingEl.querySelectorAll(selector))
      if (!elements.length && !isAudit) {
        elements = Array.from(stagingEl.querySelectorAll(fallbackSelector))
      }

      if (elements.length >= expectedCount) {
        const allReady = elements.every(el => {
          if (isAudit) {
            return el.children && el.children.length > 0
          }
          return el.childNodes && el.childNodes.length > 5
        })

        if (allReady) {
          await new Promise(resolve => setTimeout(resolve, 60))
          return elements
        }
      }
    }

    await new Promise(resolve => setTimeout(resolve, 50))
  }

  const stagingEl = document.getElementById('omr-registry-batch-staging')
  if (stagingEl) {
    let elements = Array.from(stagingEl.querySelectorAll(selector))
    if (!elements.length && !isAudit) {
      elements = Array.from(stagingEl.querySelectorAll(fallbackSelector))
    }
    return elements
  }
  return []
}

export interface DirectPrintDispatchOptions {
  exam: any
  options: {
    manifest?: boolean
    roster?: boolean
    booklets?: boolean
    sheets?: boolean
  }
  realOmrElements?: Element[]
  examDetails?: any
  selectedSheetLayout?: string
  todayIso?: string
  onError?: (msg: string) => void
}

/**
 * دالة توليد وتنفيذ الطباعة المباشرة لحزمة الاختبار (إذن صرف، كشوف مناداة، كراسات، أوراق OMR)
 */
export function dispatchRealDirectPrint(params: DirectPrintDispatchOptions): void {
  const {
    exam,
    options,
    realOmrElements = [],
    examDetails,
    selectedSheetLayout = 'compact_a5',
    todayIso = new Date().toISOString().split('T')[0],
    onError,
  } = params

  if (!exam) return

  const safeOrderNum = escapeHtml(String(exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id || ''}`))
  const safeExamTitle = escapeHtml(String(exam.title || 'الاختبار العام'))
  const safeExamCode = escapeHtml(String(exam.uniqueCode || 'EXAM-CODE'))
  const safeSubjectName = escapeHtml(String(exam.subject_name || ''))
  const safePressName = escapeHtml(String(exam.press_name || 'المطبعة المركزية'))
  const safeOfficerName = escapeHtml(String(exam.responsible_officer || 'مسؤول الكنترول والامتحانات'))
  const safeSchedDate = escapeHtml(String(exam.scheduled_print_date || todayIso))
  const totalCount = Number(exam.total_registered || exam.total_students || 0) || 0
  const schoolsCount = Number(exam.schools_count || 1) || 1

  const students = examDetails?.registered_students || []

  let sectionsHtml = ''

  // 1. إذا تم تحديد إذن الصرف وأمر الطباعة A4
  if (options?.manifest) {
    sectionsHtml += `
      <div class="print-page manifest-page">
        <div class="header">
          <div class="header-badge">وثيقة رسمية معتمدة</div>
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>اللجنة العليا للاختبارات — الإدارة العامة للاختبارات والكنترول</h3>
          <h1 class="manifest-title">إذن صرف وأمر طباعة رسمي للاختبارات</h1>
          <div class="order-code">رقم أمر الطباعة: ${safeOrderNum}</div>
        </div>

        <table class="info-table">
          <tr>
            <td class="lbl">اسم الاختبار:</td>
            <td class="val"><strong>${safeExamTitle}</strong></td>
            <td class="lbl">المادة:</td>
            <td class="val">${safeSubjectName}</td>
          </tr>
          <tr>
            <td class="lbl">كود الاختبار:</td>
            <td class="val font-mono">${safeExamCode}</td>
            <td class="lbl">تاريخ التنفيذ المعتمد:</td>
            <td class="val font-mono">${safeSchedDate}</td>
          </tr>
          <tr>
            <td class="lbl">المطبعة المنفذة:</td>
            <td class="val">${safePressName}</td>
            <td class="lbl">المسؤول المعتمد:</td>
            <td class="val">${safeOfficerName}</td>
          </tr>
          <tr>
            <td class="lbl">إجمالي الطلاب المشمولين:</td>
            <td class="val"><strong>${totalCount} طالب</strong></td>
            <td class="lbl">عدد المراكز الامتحانية:</td>
            <td class="val">${schoolsCount} مركز</td>
          </tr>
        </table>

        <div class="section-title">بيان وتفويض صرف وثائق الاختبار للمطبعة</div>
        <table class="items-table">
          <thead>
            <tr>
              <th>م</th>
              <th>البيان والمستند</th>
              <th>المواصفة والمقاس</th>
              <th>الكمية المصرح بها</th>
              <th>حالة التجهيز</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>أوراق إجابة التصحيح الآلي (OMR) مشفرة ومؤمنة بالباركود</td>
              <td>A5 / A4 ورق أبيض 80 جرام مقاوم للحرارة</td>
              <td><strong>${totalCount} ورقة</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
            <tr>
              <td>2</td>
              <td>كراسات الأسئلة الامتحانية (النماذج المعتمدة)</td>
              <td>A4 / A3 مغلفة طباعة سرية عالية الدقة</td>
              <td><strong>${totalCount} كراسة</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
            <tr>
              <td>3</td>
              <td>كشوف المناداة ومحاضر فتح المظاريف للمراكز</td>
              <td>A4 كشوف جرد وتسليم رسمية</td>
              <td><strong>${schoolsCount} كشوف</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
          </tbody>
        </table>

        <div class="signatures-grid">
          <div class="sig-box">
            <div>عضو لجنة التحقق والاعتماد</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>التاريخ: ${safeSchedDate}</div>
          </div>
          <div class="sig-box">
            <div>المشرف المسؤول بالمطبعة</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>الختم الرسمي: ....................</div>
          </div>
          <div class="sig-box">
            <div>مدير عام الامتحانات والكنترول</div>
            <div class="sig-line">المصادقة: ...........................</div>
            <div>التاريخ: ${safeSchedDate}</div>
          </div>
        </div>
      </div>
    `
  }

  // 2. إذا تم تحديد كشوف المناداة ومحاضر المراكز
  if (options?.roster) {
    if (!students || students.length === 0) {
      sectionsHtml += `
        <div class="print-page">
          <div class="header">
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كشف تسليم واستلام وثائق الاختبار للمركز الامتحاني</h3>
            <div class="order-code">الاختبار: ${safeExamTitle} (${safeExamCode}) — المادة: ${safeSubjectName}</div>
          </div>
          <div style="border: 2px dashed #b71c1c; background: #fff8f8; color: #b71c1c; padding: 30px 20px; text-align: center; border-radius: 8px; margin: 40px auto; max-width: 650px;">
            <div style="font-size: 17px; font-weight: bold; margin-bottom: 8px;">تنبيه الرقابة والكنترول: لا تتوفر سجلات طلاب مقيدين</div>
            <p style="font-size: 13px; margin: 0; color: #374151; line-height: 1.6;">
              لا توجد بيانات طلاب مقيدين في قاعدة البيانات لهذا الاختبار (${safeExamCode}).
              <br>
              <strong>يمنع النظام بصورة قاطعة إصدار كشف مناداة رسمي أو توليد أرقام جلوس وسرية افتراضية</strong> لضمان سلامة الوثائق الامتحانية ومطابقتها للكنترول.
            </p>
          </div>
        </div>
      `
    } else {
      let studentRows = ''
      students.forEach((st: any, idx: number) => {
        studentRows += `
          <tr>
            <td style="text-align: center;">${idx + 1}</td>
            <td style="text-align: center; font-family: monospace; font-weight: bold;">${escapeHtml(String(st.seat_number ?? ''))}</td>
            <td style="text-align: center; font-family: monospace;">${escapeHtml(String(st.secret_number ?? ''))}</td>
            <td style="font-weight: bold;">${escapeHtml(String(st.student_name ?? ''))}</td>
            <td>${escapeHtml(String(st.school_name || 'المركز الرئيسي'))}</td>
            <td style="text-align: center; font-weight: bold;">نموذج ${escapeHtml(String(st.model_code || 'A'))}</td>
            <td style="min-width: 100px;"></td>
          </tr>
        `
      })

      sectionsHtml += `
        <div class="print-page">
          <div class="header">
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كشف تسليم واستلام وثائق الاختبار للمركز الامتحاني</h3>
            <div class="order-code">الاختبار: ${safeExamTitle} (${safeExamCode}) — المادة: ${safeSubjectName}</div>
          </div>
          <table class="items-table" style="font-size: 12px;">
            <thead>
              <tr>
                <th style="width: 30px;">م</th>
                <th style="width: 90px;">رقم الجلوس</th>
                <th style="width: 80px;">الرقم السري</th>
                <th>اسم الطالب</th>
                <th>المدرسة</th>
                <th style="width: 80px;">النموذج</th>
                <th style="width: 120px;">توقيع الاستلام</th>
              </tr>
            </thead>
            <tbody>
              ${studentRows}
            </tbody>
          </table>
        </div>
      `
    }
  }

  // 3. كراسات الأسئلة الامتحانية (إذا تم تحديدها)
  if (options?.booklets) {
    const models = examDetails?.question_models || [
      { model_code: 'A', questions_count: 50 },
      { model_code: 'B', questions_count: 50 },
      { model_code: 'C', questions_count: 50 },
      { model_code: 'D', questions_count: 50 },
    ]
    models.forEach((m: any) => {
      const safeModelCode = escapeHtml(String(m.model_code || 'A'))
      const safeQuestionsCount = Number(m.questions_count) || 50
      sectionsHtml += `
        <div class="print-page question-booklet-page">
          <div class="header">
            <div class="header-badge">سري للغاية — وثيقة امتحانية رسمية</div>
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كراسة الأسئلة الامتحانية المقننة — نموذج (${safeModelCode})</h3>
            <div class="order-code">المادة: ${safeSubjectName} | كود الاختبار: ${safeExamCode}</div>
          </div>
          <div style="border: 2px dashed #000; padding: 25px; text-align: center; margin: 40px 0; border-radius: 8px;">
            <h2 style="margin: 0 0 10px 0;">كراسة الأسئلة — نموذج (${safeModelCode})</h2>
            <p style="font-size: 14px; color: #444;">
              عدد الفقرات: <strong>${safeQuestionsCount} فقرة اختيار من متعدد</strong> | الزمن المحدد: <strong>ساعتان ونصف</strong>
            </p>
            <p style="font-size: 12px; color: #777; margin-top: 20px;">
              تعليمات: تأكد من تطابق نموذج كراسة الأسئلة (${safeModelCode}) مع النموذج المطبوع على ورقة إجابتك المخصصة.
            </p>
          </div>
        </div>
      `
    })
  }

  // 4. أوراق إجابة OMR الرسمية الحقيقية للنظام (SVGs الأصلية المعتمدة)
  if (options?.sheets && realOmrElements && realOmrElements.length > 0) {
    realOmrElements.forEach(el => {
      if (!el) return
      const cloned = el.cloneNode(true)
      if (cloned instanceof HTMLElement) {
        cloned.querySelectorAll('.d-print-none, button, .v-btn').forEach(b => b.remove())
        sanitizePrintNode(cloned)
      }
      sectionsHtml += `
        <div class="print-page omr-real-sheet-page">
          <div class="real-sheet-container">
            ${cloned instanceof HTMLElement ? cloned.outerHTML : ''}
          </div>
        </div>
      `
    })
  }

  // إذا لم يختر أي خيار محدد، نطبع حزمة الاختبار الأساسية
  if (!sectionsHtml) {
    sectionsHtml = `
      <div class="print-page">
        <div class="header">
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>أمر سحب وثائق الاختبار</h3>
          <h1>${safeExamTitle} (${safeExamCode})</h1>
        </div>
        <p style="text-align: center; font-size: 16px; margin-top: 30px;">
          المادة: ${safeSubjectName} | إجمالي المقيدين: ${totalCount} طالب | المطبعة: ${safePressName}
        </p>
      </div>
    `
  }

  const onlySheetsSelected = !!(options?.sheets && !options?.manifest && !options?.booklets && !options?.roster)
  const omrPageSize = selectedSheetLayout === 'full_a4' ? 'A4 portrait' : 'A5 landscape'

  const fullHtml = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <meta http-equiv="Content-Security-Policy" content="script-src 'none'; connect-src 'none'; style-src 'unsafe-inline'; img-src data: blob: 'self'; font-src data: 'self';">
      <title>أمر سحب وثائق الاختبار - ${safeExamTitle} (${safeExamCode})</title>
      <style>
        @page {
          size: ${onlySheetsSelected ? omrPageSize : 'A4 portrait'};
          margin: ${onlySheetsSelected ? '0' : '6mm 8mm'};
        }
        @page omr-page {
          size: ${omrPageSize};
          margin: 0;
        }
        *, *::before, *::after {
          box-sizing: border-box;
          -webkit-print-color-adjust: exact !important;
          print-color-adjust: exact !important;
        }
        body {
          font-family: 'Amiri', 'Traditional Arabic', 'Cairo', Tahoma, Arial, sans-serif;
          margin: 0;
          padding: 0;
          color: #000;
          background: #fff;
        }
        .print-page {
          page-break-after: always;
          break-after: page;
          padding: 6px;
          min-height: 270mm;
          box-sizing: border-box;
        }
        .print-page:last-child {
          page-break-after: auto;
          break-after: auto;
        }
        .header {
          text-align: center;
          border-bottom: 2px solid #000;
          padding-bottom: 8px;
          margin-bottom: 12px;
        }
        .header h2 { margin: 0 0 3px 0; font-size: 17px; font-weight: bold; }
        .header h3 { margin: 0 0 3px 0; font-size: 14px; font-weight: normal; color: #333; }
        .header-badge {
          display: inline-block;
          font-size: 11px;
          font-weight: bold;
          border: 1px solid #000;
          padding: 2px 8px;
          border-radius: 4px;
          margin-bottom: 4px;
        }
        .manifest-title {
          font-size: 19px;
          font-weight: 900;
          margin: 4px 0;
          text-decoration: underline;
        }
        .order-code {
          font-family: monospace;
          font-weight: bold;
          font-size: 13px;
          margin-top: 3px;
        }
        .info-table, .items-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 12px;
          font-size: 12px;
        }
        .info-table td {
          border: 1px solid #666;
          padding: 5px 8px;
        }
        .info-table .lbl {
          background: #f4f4f4;
          width: 18%;
          font-weight: bold;
        }
        .info-table .val {
          width: 32%;
        }
        .items-table th, .items-table td {
          border: 1px solid #000;
          padding: 5px 6px;
          text-align: center;
        }
        .items-table th {
          background: #f0f0f0;
          font-weight: bold;
        }
        .section-title {
          font-weight: bold;
          font-size: 13px;
          margin: 10px 0 5px 0;
        }
        .signatures-grid {
          display: flex;
          justify-content: space-between;
          margin-top: 30px;
          font-size: 11px;
          font-weight: bold;
          text-align: center;
        }
        .sig-box {
          width: 30%;
          border: 1px solid #aaa;
          padding: 8px;
          border-radius: 6px;
        }
        .sig-line {
          margin: 20px 0 6px 0;
        }
        .font-mono {
          font-family: monospace, monospace;
        }

        /* ── تنسيق ورقة OMR الحقيقية الأصلية ── */
        .omr-real-sheet-page {
          page: omr-page;
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 0;
          min-height: ${onlySheetsSelected ? '100vh' : 'auto'};
        }
        .real-sheet-container {
          width: 100%;
          max-width: 210mm;
          margin: auto;
        }
        .real-sheet-container svg {
          width: 100% !important;
          max-width: 210mm !important;
          height: auto !important;
          max-height: ${selectedSheetLayout === 'full_a4' ? '297mm' : '148.5mm'} !important;
          display: block !important;
          margin: auto !important;
        }
        .yemeni-audit-report-sheet {
          width: 100% !important;
          max-width: 100% !important;
          margin: 0 auto !important;
        }
      </style>
    </head>
    <body>
      ${sectionsHtml}
    </body>
    </html>
  `

  printHtmlViaHiddenIframe(fullHtml, 'omr-hardware-print-frame', onError)
}

export interface AuditRosterPrintOptions {
  exam: any
  students: any[]
  meta?: {
    centerName?: string
    directorateName?: string
    governorateName?: string
    stageTitle?: string
    examYear?: string
    subjectName?: string
  }
  onError?: (msg: string) => void
}

/**
 * دالة توليد وتنفيذ طباعة كشف تسليم واستلام الكنترول A4 landscape
 */
export function dispatchAuditRosterPrint(params: AuditRosterPrintOptions): void {
  const { exam = {}, students = [], meta = {}, onError } = params

  const center = escapeHtml(String(meta.centerName || exam.school_name || exam.center_name || exam.directorate || ''))
  const directorate = escapeHtml(String(meta.directorateName || exam.directorate || ''))
  const governorate = escapeHtml(String(meta.governorateName || exam.governorate || ''))
  const examTitle = escapeHtml(String(meta.stageTitle || exam.title || ''))
  const yearName = escapeHtml(String(meta.examYear || exam.year_name || ''))
  const subjectName = escapeHtml(String(meta.subjectName || exam.subject_name || ''))
  const examCode = escapeHtml(String(exam.uniqueCode || ''))
  const totalStudents = Number(students.length) || 0

  let rowsHtml = ''
  students.forEach((st: any, idx: number) => {
    rowsHtml += `
      <tr>
        <td style="text-align: center; font-weight: bold;">${idx + 1}</td>
        <td style="text-align: center; font-family: monospace; font-weight: bold; font-size: 14px;">${escapeHtml(String(st.seat_number ?? ''))}</td>
        <td style="text-align: center; font-family: monospace;">${escapeHtml(String(st.secret_number ?? ''))}</td>
        <td style="font-weight: bold; padding-right: 8px;">${escapeHtml(String(st.student_name ?? ''))}</td>
        <td>${escapeHtml(String(st.school_name || ''))}</td>
        <td style="text-align: center; font-weight: bold;">النموذج ${escapeHtml(String(st.model_code || 'A'))}</td>
        <td style="text-align: center;">${st.is_printed ? 'نعم' : 'لا'}</td>
        <td style="min-width: 120px;"></td>
      </tr>
    `
  })

  const html = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <meta http-equiv="Content-Security-Policy" content="script-src 'none'; connect-src 'none'; style-src 'unsafe-inline'; img-src data: blob: 'self'; font-src data: 'self';">
      <title>كشف تسليم واستلام الكنترول - ${examCode}</title>
      <style>
        @page { size: A4 landscape; margin: 10mm; }
        *, *::before, *::after { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        body { font-family: 'Amiri', 'Traditional Arabic', Tahoma, sans-serif; margin: 0; padding: 10px; color: #000; background: #fff; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 16px; }
        .header h2 { margin: 0 0 6px 0; font-size: 20px; }
        .header h3 { margin: 0 0 6px 0; font-size: 16px; font-weight: normal; }
        .meta-grid { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
        th, td { border: 1px solid #000; padding: 6px 4px; }
        th { background-color: #f0f0f0; }
        .footer { margin-top: 25px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }
      </style>
    </head>
    <body>
      <div class="header">
        <h2>الجمهورية اليمنية - وزارة التربية والتعليم</h2>
        <h3>قطاع المناهج والتوجيه - الإدارة العامة للاختبارات</h3>
        <h2>كشف تسليم واستلام أوراق إجابة التظليل (OMR)</h2>
      </div>
      <div class="meta-grid">
        <div>المحافظة: ${governorate} | المديرية: ${directorate}</div>
        <div>المركز / المدرسة: ${center}</div>
      </div>
      <div class="meta-grid">
        <div>المادة: ${subjectName} | المرحلة: ${examTitle}</div>
        <div>العام الدراسي: ${yearName} | إجمالي الطلاب: ${totalStudents}</div>
      </div>
      <table>
        <thead>
          <tr>
            <th style="width: 35px;">م</th>
            <th style="width: 85px;">رقم الجلوس</th>
            <th style="width: 75px;">الرقم السري</th>
            <th>اسم الطالب الرباعي</th>
            <th>المدرسة</th>
            <th style="width: 75px;">النموذج</th>
            <th style="width: 65px;">مطبوع</th>
            <th style="width: 140px;">توقيع المستلم / الملاحظات</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
      <div class="footer">
        <div>مسؤول الكنترول: .......................................</div>
        <div>رئيس المركز الامتحاني: .......................................</div>
        <div>تاريخ التسليم: ${escapeHtml(new Date().toLocaleDateString('ar-YE'))}</div>
      </div>
    </body>
    </html>
  `

  printHtmlViaHiddenIframe(html, 'roster-print-frame', onError)
}
