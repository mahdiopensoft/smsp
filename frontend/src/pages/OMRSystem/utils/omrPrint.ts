/**
 * Utility for printing OMR sheets and reports cleanly and with high fidelity.
 * Uses an isolated iframe with direct @page CSS rules to avoid parent CSS contamination
 * and prevent unwanted blank pages or layout truncation.
 */
export async function printOmrElement(
  targetEl: SVGGraphicsElement | HTMLElement | null,
  options: { title?: string; isA5?: boolean } = {}
): Promise<void> {
  if (!targetEl) {
    console.warn('printOmrElement: Target element not found, falling back to window.print()')
    window.print()
    return
  }

  // 1. Clone element so we don't modify DOM
  const cloned = targetEl.cloneNode(true) as SVGGraphicsElement | HTMLElement

  if (cloned instanceof SVGElement) {
    cloned.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    cloned.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
  } else if (cloned instanceof HTMLElement) {
    // Remove action bars, buttons, and print-hidden elements completely from DOM
    cloned.querySelectorAll('.d-print-none, .report-action-bar, button, .v-btn').forEach(el => el.remove())
  }

  // 2. Convert all relative/absolute <image> hrefs to inline Base64 data URLs
  const images = Array.from(cloned.querySelectorAll('image'))
  for (const imgEl of images) {
    const href = imgEl.getAttribute('href') || imgEl.getAttribute('xlink:href') || ''
    if (href && !href.startsWith('data:')) {
      try {
        const fullUrl = href.startsWith('http') ? href : `${window.location.origin}${href}`
        const resp = await fetch(fullUrl)
        if (resp.ok) {
          const blob = await resp.blob()
          const b64 = await new Promise<string>((resolve, reject) => {
            const reader = new FileReader()
            reader.onloadend = () => resolve(reader.result as string)
            reader.onerror = reject
            reader.readAsDataURL(blob)
          })
          imgEl.setAttribute('href', b64)
          imgEl.removeAttribute('xlink:href')
        }
      } catch (e) {
        console.warn('Could not inline image for print:', href, e)
      }
    }
  }

  // 3. Determine orientation and page size
  const isSvg = targetEl instanceof SVGElement
  let isA5 = options.isA5
  if (isA5 === undefined && isSvg) {
    const vb = (targetEl as SVGElement).getAttribute('viewBox') || '0 0 210 148.5'
    const parts = vb.trim().split(/[\s,]+/).map(Number)
    const vbWidth = parts[2] || 210
    const vbHeight = parts[3] || 148.5
    isA5 = vbWidth > vbHeight
  }
  const pageSize = isA5 ? 'A5 landscape' : 'A4 portrait'

  // 4. Create isolated iframe
  const iframe = document.createElement('iframe')
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document
  if (!doc) return

  const headStyles = isSvg
    ? `
      @page {
        size: ${pageSize};
        margin: 0;
      }
      *, *::before, *::after {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      html, body {
        margin: 0;
        padding: 0;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: #ffffff !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Cairo', Arial, Tahoma, sans-serif;
      }
      svg {
        width: 100%;
        height: 100%;
        max-width: 100vw;
        max-height: 100vh;
        display: block;
        margin: auto;
      }
    `
    : `
      @page {
        size: A4 portrait;
        margin: 3mm 5mm !important;
      }
      *, *::before, *::after {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      html, body {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        background: #ffffff !important;
        font-family: 'Cairo', 'Segoe UI', Tahoma, Arial, sans-serif;
        color: #000;
        direction: rtl;
      }
      .d-print-none, .report-action-bar, button, .v-btn {
        display: none !important;
      }
      .yemeni-audit-report-sheet {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto !important;
        padding: 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      table {
        border-collapse: collapse;
        width: 100% !important;
      }
      .table-header-official td {
        border: 1px solid #000 !important;
        padding: 1.5px 2.5px !important;
        font-size: 0.72rem !important;
        line-height: 1.15 !important;
      }
      .table-header-official,
      .table-audit,
      .table-audit tr,
      .table-header-official tr {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .border-dark {
        border-color: #000 !important;
      }
      .exam-sheet-frame {
        width: 100% !important;
        aspect-ratio: 210 / 148.5 !important;
        height: auto !important;
        max-height: 142mm !important;
        border: 1px solid #000 !important;
        box-sizing: border-box !important;
        margin-bottom: 2px !important;
        background: #fff !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .sheet-slot-wrapper {
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .sheet-slot-wrapper svg {
        width: 100% !important;
        height: 100% !important;
        max-width: 100% !important;
        max-height: 100% !important;
        display: block !important;
        margin: 0 auto !important;
      }
      .sheet-image-unified {
        width: 100% !important;
        height: 100% !important;
        max-width: 100% !important;
        max-height: 142mm !important;
        display: block !important;
        margin: 0 auto !important;
        padding: 0 !important;
        object-fit: contain !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .table-header-official {
        border-collapse: collapse !important;
        width: 100% !important;
        table-layout: fixed !important;
      }
      .table-header-official td {
        border: 1px solid #000 !important;
        padding: 1.5px 3px !important;
        font-size: 0.74rem !important;
        line-height: 1.15 !important;
      }
      .table-audit {
        font-family: Tahoma, 'Segoe UI', Arial, sans-serif !important;
        border-collapse: collapse !important;
        width: 100% !important;
        table-layout: fixed !important;
      }
      .table-audit th {
        border: 1px solid #000 !important;
        padding: 1.5px 0.5px !important;
        font-size: 0.54rem !important;
        line-height: 1.12 !important;
        font-weight: 700 !important;
        white-space: normal !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        hyphens: none !important;
        vertical-align: middle !important;
        text-align: center !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
        letter-spacing: normal !important;
      }
      .table-audit td {
        border: 1px solid #000 !important;
        padding: 1px 1px !important;
        font-size: 0.65rem !important;
        line-height: 1.10 !important;
        white-space: nowrap !important;
        vertical-align: middle !important;
        text-align: center !important;
        box-sizing: border-box !important;
      }
      .audit-matrix-grid {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 3px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .matrix-column {
        min-width: 0 !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        box-sizing: border-box !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .notes-box {
        flex-grow: 1 !important;
        min-height: 38px !important;
        padding: 2px 4px !important;
        font-size: 0.68rem !important;
        box-sizing: border-box !important;
        border: 1px solid #000 !important;
        overflow: hidden !important;
      }
      .bg-grey-lighten-4 { background-color: #f5f5f5 !important; }
      .bg-grey-lighten-5 { background-color: #fafafa !important; }
      .bg-red-lighten-5 { background-color: #ffebee !important; }
      .text-error { color: #d32f2f !important; }
      .text-success { color: #2e7d32 !important; }
      .text-center { text-align: center !important; }
      .text-end { text-align: left !important; }
      .d-flex { display: flex !important; }
      .flex-column { flex-direction: column !important; }
      .gap-1 { gap: 3px !important; }
      .gap-2 { gap: 6px !important; }
      .flex-grow-1 { flex-grow: 1 !important; }
      .w-100 { width: 100% !important; }
      .border { border: 1px solid #000 !important; }
      .border-b { border-bottom: 1px solid #000 !important; }
      .font-weight-bold { font-weight: 700 !important; }
      .font-weight-black { font-weight: 900 !important; }
      .font-mono { font-family: monospace, sans-serif !important; }
    `

  const docStyles = Array.from(document.querySelectorAll('style, link[rel="stylesheet"]'))
    .map(el => el.outerHTML)
    .join('\n')

  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
      <head>
        <meta charset="utf-8">
        <title>${options.title || 'وثيقة التصحيح OMR'}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
        ${docStyles}
        <style>${headStyles}</style>
      </head>
      <body>
        ${cloned.outerHTML}
      </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    iframe.contentWindow?.focus()
    iframe.contentWindow?.print()
    setTimeout(() => {
      if (document.body.contains(iframe)) {
        document.body.removeChild(iframe)
      }
    }, 3000)
  }, 400)
}

/**
 * Utility for printing multiple OMR sheets in a single print job.
 * Wraps each sheet in a dedicated print page with page-break-after.
 */
export async function printOmrBatch(
  elements: Array<SVGGraphicsElement | HTMLElement>,
  options: { title?: string; isA5?: boolean } = {}
): Promise<void> {
  if (!elements || elements.length === 0) return

  const isA5 = options.isA5 !== undefined ? options.isA5 : true
  const pageSize = isA5 ? 'A5 landscape' : 'A4 portrait'

  const iframe = document.createElement('iframe')
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document
  if (!doc) return

  const headStyles = isA5
    ? `
      @page {
        size: A5 landscape;
        margin: 0;
      }
      *, *::before, *::after {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      html, body {
        margin: 0;
        padding: 0;
        background: #ffffff !important;
        font-family: 'Cairo', Arial, Tahoma, sans-serif;
      }
      .sheet-print-page {
        width: 100vw;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        page-break-after: always;
        break-after: page;
        overflow: hidden;
        box-sizing: border-box;
      }
      .sheet-print-page:last-child {
        page-break-after: auto;
        break-after: auto;
      }
      .sheet-print-page svg {
        width: 100%;
        height: 100%;
        max-width: 100vw;
        max-height: 100vh;
        display: block;
        margin: auto;
      }
    `
    : `
      @page {
        size: A4 portrait;
        margin: 3mm 5mm !important;
      }
      *, *::before, *::after {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      html, body {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        background: #ffffff !important;
        font-family: 'Cairo', 'Segoe UI', Tahoma, Arial, sans-serif;
        color: #000;
        direction: rtl;
      }
      .sheet-print-page {
        width: 100% !important;
        min-height: 100vh;
        page-break-after: always;
        break-after: page;
        box-sizing: border-box;
        display: block;
      }
      .sheet-print-page:last-child {
        page-break-after: auto;
        break-after: auto;
      }
      .d-print-none, .report-action-bar, button, .v-btn {
        display: none !important;
      }
      .yemeni-audit-report-sheet {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto !important;
        padding: 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      table {
        border-collapse: collapse;
        width: 100% !important;
      }
      .table-header-official td {
        border: 1px solid #000 !important;
        padding: 1.5px 2.5px !important;
        font-size: 0.72rem !important;
        line-height: 1.15 !important;
      }
      .table-header-official,
      .table-audit,
      .table-audit tr,
      .table-header-official tr {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .border-dark {
        border-color: #000 !important;
      }
      .exam-sheet-frame {
        width: 100% !important;
        aspect-ratio: 210 / 148.5 !important;
        height: auto !important;
        max-height: 142mm !important;
        border: 1px solid #000 !important;
        box-sizing: border-box !important;
        margin-bottom: 2px !important;
        background: #fff !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .sheet-slot-wrapper {
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .sheet-slot-wrapper svg {
        width: 100% !important;
        height: 100% !important;
        max-width: 100% !important;
        max-height: 100% !important;
        display: block !important;
        margin: 0 auto !important;
      }
      .table-audit th {
        border: 1px solid #000 !important;
        padding: 1.5px 0.5px !important;
        font-size: 0.54rem !important;
        line-height: 1.12 !important;
        font-weight: 700 !important;
        white-space: normal !important;
        text-align: center !important;
      }
      .table-audit td {
        border: 1px solid #000 !important;
        padding: 1px 1px !important;
        font-size: 0.65rem !important;
        line-height: 1.10 !important;
        white-space: nowrap !important;
        text-align: center !important;
      }
      .audit-matrix-grid {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 3px !important;
        width: 100% !important;
      }
      .bg-grey-lighten-4 { background-color: #f5f5f5 !important; }
      .bg-grey-lighten-5 { background-color: #fafafa !important; }
      .text-success { color: #2e7d32 !important; }
      .text-center { text-align: center !important; }
      .text-end { text-align: left !important; }
      .d-flex { display: flex !important; }
      .flex-column { flex-direction: column !important; }
      .w-100 { width: 100% !important; }
      .border { border: 1px solid #000 !important; }
      .border-b { border-bottom: 1px solid #000 !important; }
      .font-weight-bold { font-weight: 700 !important; }
      .font-weight-black { font-weight: 900 !important; }
      .font-mono { font-family: monospace, sans-serif !important; }
    `

  const docStyles = Array.from(document.querySelectorAll('style, link[rel="stylesheet"]'))
    .map(el => el.outerHTML)
    .join('\n')

  let pagesHtml = ''
  for (const el of elements) {
    const cloned = el.cloneNode(true) as SVGGraphicsElement | HTMLElement
    if (cloned instanceof SVGElement) {
      cloned.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
      cloned.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
    } else if (cloned instanceof HTMLElement) {
      cloned.querySelectorAll('.d-print-none, .report-action-bar, button, .v-btn').forEach(b => b.remove())
    }
    pagesHtml += `<div class="sheet-print-page">${cloned.outerHTML}</div>`
  }

  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
      <head>
        <meta charset="utf-8">
        <title>${options.title || 'طباعة أوراق التظليل دفعة واحدة'}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
        ${docStyles}
        <style>${headStyles}</style>
      </head>
      <body>
        ${pagesHtml}
      </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    iframe.contentWindow?.focus()
    iframe.contentWindow?.print()
    setTimeout(() => {
      if (document.body.contains(iframe)) {
        document.body.removeChild(iframe)
      }
    }, 4000)
  }, 500)
}

/**
 * Print Official Yemeni Question Paper (A3 Landscape spread or A4 portrait)
 * Clones target element, inlines images as Base64, and prints in an isolated iframe.
 */
export async function printOfficialQuestionPaper(
  targetEl: HTMLElement | null,
  options: { title?: string; isA3?: boolean } = {}
): Promise<void> {
  if (!targetEl) {
    console.warn('printOfficialQuestionPaper: Target element not found, falling back to window.print()')
    window.print()
    return
  }

  const isA3 = options.isA3 === true
  const cloned = targetEl.cloneNode(true) as HTMLElement
  cloned.querySelectorAll('.d-print-none, .action-bar, button, .v-btn').forEach(el => el.remove())

  // Inline images (emblem, student photo, diagrams)
  const images = Array.from(cloned.querySelectorAll('img'))
  for (const imgEl of images) {
    const src = imgEl.getAttribute('src') || ''
    if (src && !src.startsWith('data:')) {
      try {
        const fullUrl = src.startsWith('http') ? src : `${window.location.origin}${src}`
        const resp = await fetch(fullUrl)
        if (resp.ok) {
          const blob = await resp.blob()
          const b64 = await new Promise<string>((resolve, reject) => {
            const reader = new FileReader()
            reader.onloadend = () => resolve(reader.result as string)
            reader.onerror = reject
            reader.readAsDataURL(blob)
          })
          imgEl.setAttribute('src', b64)
        }
      } catch (e) {
        console.warn('Could not inline image for official question paper:', src, e)
      }
    }
  }

  const iframe = document.createElement('iframe')
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document
  if (!doc) return

  const pageSize = isA3 ? 'A3 landscape' : 'A4 portrait'
  const isDocLtr = (cloned.getAttribute('dir') || '').toLowerCase() === 'ltr'
  const headStyles = `
    @page {
      size: ${pageSize};
      margin: 6mm 8mm !important;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    html, body {
      margin: 0 !important;
      padding: 0 !important;
      width: 100% !important;
      background: #ffffff !important;
      font-family: 'Tajawal', 'Cairo', Tahoma, Arial, sans-serif !important;
      color: #000;
      direction: ${isDocLtr ? 'ltr' : 'rtl'};
    }
    .d-print-none, .action-bar, button, .v-btn {
      display: none !important;
    }
    .yemeni-official-question-paper {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
    }
    .a4-pages-wrapper {
      gap: 0 !important;
      display: block !important;
      width: 100% !important;
    }
    .a4-sheet-page {
      width: 100% !important;
      min-height: 0 !important;
      height: auto !important;
      padding: 4mm 6mm !important;
      margin: 0 !important;
      border: none !important;
      box-shadow: none !important;
      page-break-after: always !important;
      break-after: page !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
    }
    .a4-sheet-page:last-child {
      page-break-after: auto !important;
      break-after: auto !important;
    }
    .a4-page-footer {
      font-size: 0.68rem !important;
      border-top: 1px solid #000000 !important;
      padding-top: 3px !important;
      margin-top: 6px !important;
    }
    .reading-passage-box {
      border: 1px solid #000000 !important;
      margin-bottom: 3px !important;
    }
    .passage-text-content {
      font-size: 0.74rem !important;
      line-height: 1.35 !important;
      background: #ffffff !important;
      padding: 4px 6px !important;
      font-weight: 600 !important;
      border-top: 1px solid #000000 !important;
    }
    .exam-sheet-frame {
      width: 100% !important;
      display: grid !important;
      grid-template-columns: ${isA3 ? '1fr 1fr' : '1fr'} !important;
      gap: 8mm !important;
    }
    table {
      border-collapse: collapse !important;
    }
    .official-header-box {
      width: 100% !important;
      margin: 0 auto 4px auto !important;
      border: 1.5px solid #000000 !important;
      background-color: #ffffff !important;
      font-family: 'Arial', 'Simplified Arabic', Tahoma, sans-serif !important;
      color: #000000 !important;
      box-sizing: border-box !important;
    }
    .table-top-section {
      width: 100% !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      background-color: #ffffff !important;
    }
    .table-top-section td {
      border: 1px solid #000000 !important;
      padding: 2px 2px !important;
      text-align: center !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      font-size: 0.68rem !important;
      line-height: 1.15 !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }
    .student-photo-cell {
      width: 17.5% !important;
      padding: 2px !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
    }
    .student-photo-frame {
      width: 82px !important;
      height: 100px !important;
      border: 1px solid #000000 !important;
      margin: 0 auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #fafafa !important;
      overflow: hidden !important;
      box-sizing: border-box !important;
    }
    .student-photo-img {
      width: 100% !important;
      height: 100% !important;
      object-fit: cover !important;
      display: block !important;
    }
    .photo-placeholder {
      font-size: 0.70rem !important;
      font-weight: 800 !important;
      color: #222 !important;
      text-align: center !important;
      width: 100% !important;
      height: 100% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .emblem-cell {
      width: 19.0% !important;
      padding: 2px 2px !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
    }
    .republic-logo {
      width: 44px !important;
      height: auto !important;
      max-height: 32px !important;
      object-fit: contain !important;
      display: block !important;
      margin: 0 auto 2px auto !important;
    }
    .table-bottom-bar {
      width: 100% !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      border-top: 1px solid #000000 !important;
      background-color: #ffffff !important;
    }
    .table-bottom-bar td {
      border: 1px solid #000000 !important;
      padding: 2px 2px !important;
      text-align: center !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      font-size: 0.76rem !important;
      line-height: 1.15 !important;
      white-space: nowrap !important;
      box-sizing: border-box !important;
    }
    .table-tf {
      border: 1px solid #000 !important;
      font-size: 0.74rem !important;
      width: 100% !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      background-color: #ffffff !important;
    }
    .table-tf td {
      border: 1px solid #000 !important;
      padding: 1.5px 3px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
    }
    .table-mcq-continuous {
      border: 1px solid #000 !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      width: 100% !important;
      background-color: #ffffff !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .table-mcq-continuous td {
      border: 1px solid #000 !important;
      padding: 1px 2px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
    }
    .table-mcq-question {
      border: 1px solid #000 !important;
      border-collapse: collapse !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      margin-bottom: 2px !important;
      table-layout: fixed !important;
      width: 100% !important;
      background-color: #ffffff !important;
    }
    .table-mcq-question td {
      border: 1px solid #000 !important;
      padding: 1px 2px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
    }
    .q-num-cell {
      font-family: monospace, sans-serif !important;
      font-weight: 900 !important;
      font-size: 0.82rem !important;
      background: #ffffff !important;
      text-align: center !important;
    }
    .q-stem-cell {
      font-size: 0.76rem !important;
      line-height: 1.25 !important;
      font-weight: 700 !important;
    }
    .opt-num-cell {
      font-family: monospace, sans-serif !important;
      font-weight: 900 !important;
      font-size: 0.74rem !important;
      background: #ffffff !important;
      text-align: center !important;
    }
    .opt-text-cell {
      font-size: 0.72rem !important;
      font-weight: 700 !important;
      text-align: center !important;
      white-space: nowrap !important;
      overflow: hidden !important;
      text-overflow: ellipsis !important;
    }
    .instruction-banner {
      font-size: 0.70rem !important;
      font-weight: 800 !important;
      border: 1px solid #000 !important;
      border-bottom: 0 !important;
      padding: 2.5px 4px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      line-height: 1.2 !important;
    }
    .student-photo-frame {
      width: 100% !important;
      height: 100% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      padding: 2px !important;
      background: #ffffff !important;
      margin: 0 auto !important;
    }
    .student-photo-img {
      width: 95px !important;
      height: 112px !important;
      border: 1px solid #000 !important;
      object-fit: cover !important;
      display: block !important;
      margin: 0 auto !important;
    }
    .photo-placeholder {
      width: 95px !important;
      height: 112px !important;
      border: 1px dashed #666 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #fafafa !important;
      margin: 0 auto !important;
    }
    .republic-logo {
      width: 48px !important;
      height: auto !important;
      max-height: 36px !important;
      object-fit: contain !important;
      display: block !important;
      margin: 0 auto 2px auto !important;
    }
    .secret-press-ribbon {
      font-size: 0.68rem !important;
      border-bottom: 1px solid #000 !important;
      padding-bottom: 2px !important;
      margin-bottom: 4px !important;
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      font-weight: 800 !important;
    }
    .exam-paper-end-banner {
      font-size: 0.76rem !important;
      font-weight: 900 !important;
      border: 1px solid #000 !important;
      padding: 3px 6px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      text-align: center !important;
      margin-top: 6px !important;
    }
    .bg-grey-lighten-4, .bg-grey-lighten-5 { background-color: #ffffff !important; }
    .text-center { text-align: center !important; }
    .text-start { text-align: start !important; }
    .text-end { text-align: end !important; }
    .font-weight-bold { font-weight: 700 !important; }
    .font-weight-black { font-weight: 900 !important; }
    .font-mono { font-family: monospace, sans-serif !important; }
  `

  const docStyles = Array.from(document.querySelectorAll('style, link[rel="stylesheet"]'))
    .map(el => el.outerHTML)
    .join('\n')

  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html dir="${isDocLtr ? 'ltr' : 'rtl'}" lang="${isDocLtr ? 'en' : 'ar'}">
      <head>
        <meta charset="utf-8">
        <title>${options.title || 'ورقة_الأسئلة_الرسمية'}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
        ${docStyles}
        <style>${headStyles}</style>
      </head>
      <body>
        ${cloned.outerHTML}
      </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    iframe.contentWindow?.focus()
    iframe.contentWindow?.print()
    setTimeout(() => {
      if (document.body.contains(iframe)) {
        document.body.removeChild(iframe)
      }
    }, 4000)
  }, 500)
}

export interface ExamPackageOptions {
  title?: string
  examTitle: string
  subjectName: string
  stageName?: string
  yearName?: string
  governorate?: string
  directorate?: string
  centerName?: string
  centerCode?: string | number
  dayName?: string
  examDate?: string
  envelopeNo?: string | number
  versionCode: string
  studentName?: string
  seatNumber?: string
  secretNumber?: string | number
  studentPhoto?: string
  schoolName?: string
  institutionType?: string
  readingPassage?: string
  totalMarks?: number
  timeAllowed?: string
  tfMark?: number
  mcqMark?: number
  isA3?: boolean
  questions: Array<{
    id?: number | string
    orderIndex: number
    content: string
    questionType?: string
    assignedMark?: number
    image?: string
    figure?: string
    options?: Array<{
      id?: number | string
      letter?: string
      arabic_letter?: string
      text: string
      isTrue?: boolean
    }>
  }>
  omrElement?: HTMLElement | SVGGraphicsElement | null
  mode?: 'package' | 'questions_only'
  isA5?: boolean
}

/**
 * Print Questions Booklet along with OMR Answer Sheet in a single unified print job.
 * Formats the question paper using the authentic Yemeni Ministry of Education layout.
 * Default is A3 Landscape (single large sheet with 2 columns), strictly matching official ministerial standards.
 */
export async function printExamPackage(options: ExamPackageOptions): Promise<void> {
  const totalQuestions = (options.questions || []).length
  // Only use A3 if explicitly requested AND the exam has more than 18 questions!
  // Short exams (<= 18 questions) MUST default to standard A4 single page.
  const isA3 = options.isA3 === true && totalQuestions > 18
  const iframe = document.createElement('iframe')
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document
  if (!doc) return

  // Convert Republic Eagle logo to inline Base64
  let eagleBase64 = '/yemen_eagle_official.png'
  try {
    const fullUrl = `${window.location.origin}/yemen_eagle_official.png`
    const resp = await fetch(fullUrl)
    if (resp.ok) {
      const blob = await resp.blob()
      eagleBase64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result as string)
        reader.onerror = reject
        reader.readAsDataURL(blob)
      })
    }
  } catch (e) {
    console.warn('Could not inline eagle logo:', e)
  }

  // Detect if exam is English
  const isEnglish = (options.subjectName || '').toLowerCase().includes('english') ||
                    (options.subjectName || '').includes('إنجليز') ||
                    (options.subjectName || '').includes('انجليز') ||
                    (options.questions || []).some(q => (q.content || '').match(/[a-zA-Z]{5,}/))

  // Filter True/False vs MCQ Questions
  const tfQuestions = (options.questions || []).filter(q => {
    const t = String(q.questionType || '').toLowerCase()
    return t.includes('true') || t.includes('false') || t.includes('صح') || t.includes('خطأ')
  })
  const mcqQuestions = (options.questions || []).filter(q => {
    const t = String(q.questionType || '').toLowerCase()
    return !(t.includes('true') || t.includes('false') || t.includes('صح') || t.includes('خطأ'))
  })

  // Helper: Format Math & Option Content cleanly without RTL inversion
  const formatCellContent = (text: string) => {
    if (!text) return ''
    let clean = text.replace(/^<p>/i, '').replace(/<\/p>$/i, '').trim()
    const hasArabic = /[\u0600-\u06FF]/.test(clean)
    const hasMathOrLatin = /[a-zA-Z0-9^=+\-*/_()\\%π]/.test(clean)
    if (!hasArabic && hasMathOrLatin) {
      return `<span dir="ltr" style="unicode-bidi: isolate; display: inline-block; direction: ltr;">${clean}</span>`
    }
    return `<span dir="auto" style="unicode-bidi: isolate; display: inline-block;">${clean}</span>`
  }

  // Helper: Format True/False Table
  const renderTfTable = (questions: typeof tfQuestions) => {
    if (!questions || questions.length === 0) return ''
    const rows = questions.map(q => `
      <tr class="tf-row">
        <td class="q-index-cell text-center font-weight-black font-mono" style="width: 26px; border: 1px solid #000;">${q.orderIndex}</td>
        <td class="q-paren-cell text-center font-mono font-weight-bold" dir="ltr" style="width: 38px; min-width: 38px; border: 1px solid #000; white-space: nowrap !important; word-break: keep-all !important; letter-spacing: 0;">(&nbsp;&nbsp;&nbsp;)</td>
        <td class="q-text-cell pe-2 ps-2 py-1 font-weight-bold" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${q.content}</td>
      </tr>
    `).join('')
    return `
      <table class="table-tf w-100" dir="${isEnglish ? 'ltr' : 'rtl'}">
        <colgroup>
          <col style="width: 26px;">
          <col style="width: 38px;">
          <col style="width: auto;">
        </colgroup>
        <tbody>
          ${rows}
        </tbody>
      </table>
    `
  }

  // Helper: Format Continuous MCQ Table
  const renderContinuousMcqTable = (questions: typeof mcqQuestions) => {
    if (!questions || questions.length === 0) return ''
    const tables = questions.map(q => {
      const rawOpts = (q.options && q.options.length > 0) ? q.options : []
      const opts = rawOpts.slice(0, 4).map(o => (typeof o === 'object' ? (o.text || '') : String(o || '')))
      while (opts.length < 4) opts.push('')

      const hasDiagram = !!(q.image || q.figure)
      const stemContent = hasDiagram
        ? `<div style="display: flex; align-items: center; justify-content: space-between; width: 100%;"><span>${q.content}</span><img src="${q.image || q.figure}" alt="رسم توضيحي" style="max-height: 75px; max-width: 140px; object-fit: contain; margin-inline-start: 6px;" /></div>`
        : `<span>${q.content}</span>`

      const maxLen = Math.max(...opts.map(o => (o || '').length))

      if (maxLen > 30) {
        // Two-column layout (2 rows of 2 options: 50% width each)
        return `
          <table class="table-mcq-continuous w-100 mb-1" dir="${isEnglish ? 'ltr' : 'rtl'}">
            <colgroup>
              <col style="width: 26px;">
              <col style="width: 20px;"><col style="width: calc(50% - 33px);">
              <col style="width: 20px;"><col style="width: calc(50% - 33px);">
            </colgroup>
            <tbody>
              <tr class="q-stem-row">
                <td rowspan="3" class="q-num-cell text-center font-weight-black font-mono" style="width: 26px; border: 1px solid #000;">${q.orderIndex}</td>
                <td colspan="4" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${stemContent}</td>
              </tr>
              <tr class="q-options-row">
                <td class="opt-num-cell font-mono font-weight-black text-center" style="width: 20px; border: 1px solid #000;">1</td>
                <td class="opt-text-cell font-weight-bold pe-2 ps-2 py-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${formatCellContent(opts[0])}</td>
                <td class="opt-num-cell font-mono font-weight-black text-center" style="width: 20px; border: 1px solid #000;">2</td>
                <td class="opt-text-cell font-weight-bold pe-2 ps-2 py-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${formatCellContent(opts[1])}</td>
              </tr>
              <tr class="q-options-row">
                <td class="opt-num-cell font-mono font-weight-black text-center" style="width: 20px; border: 1px solid #000;">3</td>
                <td class="opt-text-cell font-weight-bold pe-2 ps-2 py-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${formatCellContent(opts[2])}</td>
                <td class="opt-num-cell font-mono font-weight-black text-center" style="width: 20px; border: 1px solid #000;">4</td>
                <td class="opt-text-cell font-weight-bold pe-2 ps-2 py-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${formatCellContent(opts[3])}</td>
              </tr>
            </tbody>
          </table>
        `
      }

      // Standard single-row 4 options (25% each)
      return `
        <table class="table-mcq-continuous w-100 mb-1" dir="${isEnglish ? 'ltr' : 'rtl'}">
          <colgroup>
            <col style="width: 26px;">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
          </colgroup>
          <tbody>
            <tr class="q-stem-row">
              <td rowspan="2" class="q-num-cell text-center font-weight-black font-mono" style="width: 26px; border: 1px solid #000;">${q.orderIndex}</td>
              <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'right'};">${stemContent}</td>
            </tr>
            <tr class="q-options-row text-center">
              <td class="opt-num-cell font-mono font-weight-black" style="width: 20px; border: 1px solid #000;">1</td>
              <td class="opt-text-cell font-weight-bold pe-1 ps-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'center'};">${formatCellContent(opts[0])}</td>
              <td class="opt-num-cell font-mono font-weight-black" style="width: 20px; border: 1px solid #000;">2</td>
              <td class="opt-text-cell font-weight-bold pe-1 ps-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'center'};">${formatCellContent(opts[1])}</td>
              <td class="opt-num-cell font-mono font-weight-black" style="width: 20px; border: 1px solid #000;">3</td>
              <td class="opt-text-cell font-weight-bold pe-1 ps-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'center'};">${formatCellContent(opts[2])}</td>
              <td class="opt-num-cell font-mono font-weight-black" style="width: 20px; border: 1px solid #000;">4</td>
              <td class="opt-text-cell font-weight-bold pe-1 ps-1" style="border: 1px solid #000; text-align: ${isEnglish ? 'left' : 'center'};">${formatCellContent(opts[3])}</td>
            </tr>
          </tbody>
        </table>
      `
    }).join('')

    return tables
  }

  const formatAcademicYear = (val?: string | number) => {
    const str = String(val || '').trim()
    if (!str || str === '1' || str === '0' || str.length < 4) {
      return '1445هـ - 2024-2023م'
    }
    return str
  }

  const formatTimeLine1 = () => {
    const t = options.timeAllowed || ''
    if (!t || t.includes('8:30') || t.includes('ثلاث ساعات')) {
      return isEnglish ? 'Three hours from 8:30 AM to' : 'ثلاث ساعات من الساعة 8:30 صباحاً وحتى'
    }
    if (t.includes('وحتى')) {
      return t.split('وحتى')[0].trim() + (isEnglish ? ' to' : ' وحتى')
    }
    return t
  }

  const formatTimeLine2 = () => {
    const t = options.timeAllowed || ''
    const d = options.examDate || '1445/11/10هـ - 2024/5/18م'
    if (t.includes('وحتى')) {
      const afterUntil = t.split('وحتى')[1].trim()
      if (d.includes(afterUntil)) return d
      return `${afterUntil} - ${d}`
    }
    if (d.includes('11:30')) return d
    return `11:30 - ${d}`
  }

  const formatStageLine1 = () => {
    let st = (options.stageName || 'اختبار الشهادة الثانوية العامة (المراكز الفرعية-علمي)').trim()
    st = st.replace(/\s*للعام\s*الدراسي.*$/, '').trim()
    const rawYr = String(options.yearName || '').trim()
    const yr = (!rawYr || rawYr === '1' || rawYr === '0' || rawYr.length < 4) ? '1445هـ - 2024-2023م' : rawYr

    const hijriMatch = yr.match(/(\d{4}\s*هـ?)/)
    const hijriStr = hijriMatch ? hijriMatch[1].replace('ه', '') + 'هـ' : '1445هـ'
    if (isEnglish) {
      return `${st} Academic Year ${hijriStr}`
    }
    return `${st} للعام الدراسي ${hijriStr}`
  }

  const formatStageLine2 = () => {
    const rawYr = String(options.yearName || '').trim()
    const yr = (!rawYr || rawYr === '1' || rawYr === '0' || rawYr.length < 4) ? '1445هـ - 2024-2023م' : rawYr
    const gregMatch = yr.match(/(\d{4}\s*[-/]\s*\d{4}\s*م?)/)
    if (gregMatch) {
      let g = gregMatch[1].trim()
      if (!g.endsWith('م')) g += 'م'
      if (!g.startsWith('-')) g = '-' + g
      return g
    }
    return '-2024-2023م'
  }

  // Exact Official Header Box (two-table architecture: Rows 1-5 Top Section + Row 6 Bottom Student Bar)
  const headerTableHtml = `
    <div class="official-header-box mb-1" dir="${isEnglish ? 'ltr' : 'rtl'}">
      <!-- Top Section: Rows 1 to 5 -->
      <table class="table-top-section w-100">
        <colgroup>
          <col style="width: 17.5%;">
          <col style="width: 7.5%;">
          <col style="width: 35.0%;">
          <col style="width: 9.0%;">
          <col style="width: 12.0%;">
          <col style="width: 19.0%;">
        </colgroup>
        <tbody>
          <!-- Row 1: Student Photo (Rows 1 to 5) + Governorate & Directorate + Republic Emblem (Rows 1 to 5) -->
          <tr>
            <!-- Student Photo Box (spans rows 1 to 5) -->
            <td rowspan="5" class="student-photo-cell">
              <div class="student-photo-frame">
                ${options.studentPhoto ? `<img src="${options.studentPhoto}" alt="صورة الطالب" class="student-photo-img" />` : `<div class="photo-placeholder">صورة شخصية</div>`}
              </div>
            </td>

            <!-- Governorate & Directorate -->
            <td class="font-weight-bold" style="font-size: 0.68rem;">المحافظة</td>
            <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${options.governorate || '................'}</td>
            <td class="font-weight-bold" style="font-size: 0.68rem;">المديرية</td>
            <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${options.directorate || '................'}</td>

            <!-- Republic Emblem Logo & Text (spans rows 1 to 5) -->
            <td rowspan="5" class="emblem-cell">
              <img src="${eagleBase64}" alt="شعار الجمهورية" class="republic-logo" />
              ${isEnglish ? `
                <div class="emblem-text-block text-center font-weight-black" style="line-height: 1.15;">
                  <div style="font-size: 0.60rem; font-weight: 800;">Republic of Yemen</div>
                  <div style="font-size: 0.54rem; font-weight: 800;">${options.institutionType === 'institute' ? 'Ministry of Technical Education' : (options.institutionType === 'university' ? 'Ministry of Higher Education' : 'Ministry of Education')}</div>
                  <div style="font-size: 0.50rem; font-weight: 800;">Supreme Exam Committee</div>
                  <div style="font-size: 0.56rem; font-weight: 900; margin-top: 1px;">Secret Press</div>
                </div>
              ` : `
                <div class="emblem-text-block text-center font-weight-black" style="line-height: 1.2;">
                  <div style="font-size: 0.78rem; font-weight: 900;">الجمهورية اليمنية</div>
                  <div style="font-size: 0.64rem; font-weight: 800; line-height: 1.15;">${
                    options.institutionType === 'institute'
                      ? 'وزارة التعليم الفني والتدريب المهني'
                      : (options.institutionType === 'university'
                        ? 'وزارة التعليم العالي والبحث العلمي'
                        : 'وزارة التربية والتعليم')
                  }</div>
                  <div style="font-size: 0.60rem; font-weight: 800; line-height: 1.15;">${
                    options.institutionType === 'institute'
                      ? 'الإدارة العامة للاختبارات والمقاييس'
                      : (options.institutionType === 'university'
                        ? 'نيابة شؤون الطلاب — الكنترول المركزي'
                        : 'اللجنة العليا للإختبارات')
                  }</div>
                  <div style="font-size: 0.64rem; font-weight: 900; margin-top: 1px;">لجنة المطبعة السرية المركزية</div>
                </div>
              `}
            </td>
          </tr>

          <!-- Row 2: Center & Center Code -->
          <tr>
            <td class="font-weight-bold" style="font-size: 0.68rem;">المركز</td>
            <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${options.centerName || options.schoolName || '................'}</td>
            <td class="font-weight-bold" style="font-size: 0.68rem;">رقمه</td>
            <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">${options.centerCode || '....'}</td>
          </tr>

          <!-- Row 3: Time, Day, Date (Exact match to real ministerial layout) -->
          <tr>
            <td class="font-weight-bold" style="font-size: 0.68rem;">الزمن</td>
            <td class="font-weight-bold time-cell" style="padding: 1px 2px; line-height: 1.2;">
              <div style="font-size: 0.58rem; white-space: nowrap;">${formatTimeLine1()}</div>
              <div style="font-size: 0.54rem; margin-top: 1px; white-space: nowrap;">${formatTimeLine2()}</div>
            </td>
            <td class="font-weight-bold" style="font-size: 0.68rem;">اليوم</td>
            <td class="font-weight-bold" style="font-size: 0.68rem; white-space: nowrap;">${options.dayName || 'السبت'}</td>
          </tr>

          <!-- Row 4: Stage Title & Academic Year (colspan 4) -->
          <tr>
            <td colspan="4" class="font-weight-black stage-year-cell" style="padding: 2px 2px; text-align: center; overflow: hidden; line-height: 1.25;">
              <div style="font-size: 0.60rem; white-space: nowrap; letter-spacing: -0.2px;">${formatStageLine1()}</div>
              <div style="font-size: 0.58rem; margin-top: 1px;">${formatStageLine2()}</div>
            </td>
          </tr>

          <!-- Row 5: Subject & Envelope No -->
          <tr>
            <td class="font-weight-bold" style="font-size: 0.68rem;">اسم المادة</td>
            <td class="font-weight-black" style="font-size: 0.84rem;">${isEnglish ? (options.subjectName || 'English') : (options.subjectName || '')}</td>
            <td class="font-weight-bold" style="font-size: 0.68rem;">رقم مظروف</td>
            <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">${options.envelopeNo || '1'}</td>
          </tr>
        </tbody>
      </table>

      <!-- Row 6: Exact Match to Original (Bottom Student Info Bar) -->
      <table class="table-bottom-bar w-100">
        <colgroup>
          <col style="width: 10.5%;">
          <col style="width: 46.5%;">
          <col style="width: 9.5%;">
          <col style="width: 16.5%;">
          <col style="width: 8.5%;">
          <col style="width: 8.5%;">
        </colgroup>
        <tbody>
          <tr>
            <td class="font-weight-black" style="font-size: 0.78rem;">الاسم</td>
            <td class="font-weight-black" style="font-size: 0.82rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${options.studentName || '...................................................'}
            </td>
            <td class="font-weight-black" style="font-size: 0.70rem;">رقم الجلوس</td>
            <td class="font-weight-black font-mono" style="font-size: 0.85rem;">${options.seatNumber || '................'}</td>
            <td class="font-weight-black" style="font-size: 0.70rem;">مسلسل</td>
            <td class="font-weight-black font-mono" style="font-size: 0.85rem;">${options.secretNumber || '................'}</td>
          </tr>
        </tbody>
      </table>
    </div>
  `

  const readingPassageHtml = (isEnglish && options.readingPassage) ? `
    <div class="reading-passage-box mb-1" dir="ltr">
      <div class="instruction-banner text-start ps-2 py-1 font-weight-bold">
        Part two: A) Read the following passage then choose the best answer to the questions below: (${options.mcqMark || 2}) points each
      </div>
      <div class="passage-text-content p-2 bg-white" style="border: 1px solid #000; font-size: 0.74rem; line-height: 1.35; text-align: left;">
        ${options.readingPassage}
      </div>
    </div>
  ` : ''

  const tfInstructionText = isEnglish
    ? `Read the following questions, and on the answer sheet, darken the number that matches the correct alternative.<br>Part One: Mark (T/True) for the true statements and (F/False) for the false ones. (${options.tfMark || 1}) point each`
    : `أولاً: ظلل في ورقة الإجابة الدائرة التي تحتوي على الحرف (ص) للإجابة الصحيحة والحرف (خ) للإجابة الخطأ بحسب رقم الفقرة لكل مما يأتي: ${options.tfMark || 1} درجة لكل فقرة.`

  const mcqInstructionText = isEnglish
    ? `Part two: Choose the best alternative: (${options.mcqMark || 2}) points each`
    : `ثانياً: لكل فقرة مما يأتي أربع إجابات واحدة فقط منها صحيحة، اختر الإجابة الصحيحة ثم ظلل في ورقة الإجابة الدائرة بحسب الاختيار ورقم الفقرة: ${options.mcqMark || 2} درجات لكل فقرة.`

  const secretPressRibbonHtml = isEnglish ? `
    <div class="secret-press-ribbon d-flex justify-space-between align-center mb-1 pb-1" dir="ltr">
      <span>${options.institutionType === 'institute' ? 'Ministry of Technical Education' : (options.institutionType === 'university' ? 'Ministry of Higher Education' : 'Ministry of Education')} • Secret Press</span>
      <span class="font-mono">Multiple Choice Questions (Continued) • Form (${options.versionCode || '1'})</span>
    </div>
  ` : `
    <div class="secret-press-ribbon d-flex justify-space-between align-center mb-1 pb-1" dir="rtl">
      <span>${
        options.institutionType === 'institute'
          ? 'وزارة التعليم الفني والتدريب المهني • لجنة الامتحانات المركزية'
          : (options.institutionType === 'university'
            ? 'وزارة التعليم العالي والبحث العلمي • الكنترول المركزي'
            : 'لجنة المطبعة السرية المركزية • وزارة التربية والتعليم')
      }</span>
      <span class="font-mono">تابع أسئلة الاختيار من متعدد • النموذج (${options.versionCode || '1'})</span>
    </div>
  `

  const endBannerText = isEnglish
    ? `*** End of Form (${options.versionCode || '1'}) Questions — Best wishes for success ***`
    : `*** انتهت أسئلة النموذج (${options.versionCode || '1'}) — مع تمنياتنا لجميع الطلاب بالتوفيق والنجاح ***`

  // Dynamic Multi-page splitting logic
  // Short exams (<= 18 questions without reading passage) fit cleanly on 1 single page!
  const hasSecondPage = totalQuestions > 18 || (!!readingPassageHtml && totalQuestions > 12)
  let col1Capacity = mcqQuestions.length
  if (hasSecondPage) {
    if (tfQuestions.length >= 12) {
      col1Capacity = readingPassageHtml ? 6 : 10
    } else {
      col1Capacity = Math.ceil(mcqQuestions.length * 0.42)
    }
  }

  const col1McqList = hasSecondPage ? mcqQuestions.slice(0, col1Capacity) : mcqQuestions
  const col2McqList = hasSecondPage ? mcqQuestions.slice(col1Capacity) : []

  // Questions Booklet HTML
  let questionsBookletHtml = ''
  if (isA3 && hasSecondPage) {
    // Two-Column Layout for A3 Landscape (Single large sheet)
    questionsBookletHtml = `
      <div class="exam-package-page questions-booklet-page">
        <div class="exam-sheet-frame columns-two" dir="${isEnglish ? 'ltr' : 'rtl'}">
          <!-- ── COLUMN 1: HEADER + TF + MCQ PART 1 ─────────── -->
          <div class="sheet-column column-first">
            <div class="header-box-wrapper mb-1">
              ${headerTableHtml}
            </div>

            ${tfQuestions.length > 0 ? `
              <div class="tf-section-wrapper mb-1">
                <div class="instruction-banner ${isEnglish ? 'text-start ps-2' : 'text-center'} py-1 font-weight-bold">
                  ${tfInstructionText}
                </div>
                ${renderTfTable(tfQuestions)}
              </div>
            ` : ''}

            ${readingPassageHtml}

            ${col1McqList.length > 0 ? `
              <div class="mcq-section-wrapper">
                <div class="instruction-banner ${isEnglish ? 'text-start ps-2' : 'text-center'} py-1 font-weight-bold">
                  ${mcqInstructionText}
                </div>
                ${renderContinuousMcqTable(col1McqList)}
              </div>
            ` : ''}
          </div>

          <!-- ── COLUMN 2: MCQ CONTINUATION + DIAGRAMS ───────── -->
          <div class="sheet-column column-second">
            ${secretPressRibbonHtml}

            ${renderContinuousMcqTable(col2McqList)}

            <div class="exam-paper-end-banner text-center font-weight-black">
              ${endBannerText}
            </div>
          </div>
        </div>
      </div>
    `
  } else {
    // A4 Mode: 2 distinct consecutive pages or 1 single page if short quiz
    if (hasSecondPage) {
      questionsBookletHtml = `
        <div class="exam-package-page questions-booklet-page a4-page-1">
          <div class="a4-sheet-page sheet-page-1" dir="${isEnglish ? 'ltr' : 'rtl'}">
            <div class="page-content-wrapper">
              <div class="header-box-wrapper mb-1">
                ${headerTableHtml}
              </div>

              ${tfQuestions.length > 0 ? `
                <div class="tf-section-wrapper mb-1">
                  <div class="instruction-banner ${isEnglish ? 'text-start ps-2' : 'text-center'} py-1 font-weight-bold">
                    ${tfInstructionText}
                  </div>
                  ${renderTfTable(tfQuestions)}
                </div>
              ` : ''}

              ${readingPassageHtml}

              ${col1McqList.length > 0 ? `
                <div class="mcq-section-wrapper">
                  <div class="instruction-banner ${isEnglish ? 'text-start ps-2' : 'text-center'} py-1 font-weight-bold">
                    ${mcqInstructionText}
                  </div>
                  ${renderContinuousMcqTable(col1McqList)}
                </div>
              ` : ''}
            </div>

            <div class="a4-page-footer d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
              <span>${isEnglish ? 'English' : options.subjectName} • ${isEnglish ? 'Form' : 'النموذج'} (${options.versionCode || '1'})</span>
              <span>${isEnglish ? 'Page 1 of 2 (Turn over)' : 'الصفحة 1 من 2 (يتبع في الصفحة التالية)'}</span>
            </div>
          </div>
        </div>

        <div class="exam-package-page questions-booklet-page a4-page-2">
          <div class="a4-sheet-page sheet-page-2" dir="${isEnglish ? 'ltr' : 'rtl'}">
            <div class="page-content-wrapper">
              ${secretPressRibbonHtml}

              <div class="mcq-section-wrapper">
                ${renderContinuousMcqTable(col2McqList)}
              </div>

              <div class="exam-paper-end-banner text-center font-weight-black">
                ${endBannerText}
              </div>
            </div>

            <div class="a4-page-footer d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
              <span>${isEnglish ? 'English' : options.subjectName} • ${isEnglish ? 'Form' : 'النموذج'} (${options.versionCode || '1'})</span>
              <span>${isEnglish ? 'Page 2 of 2' : 'الصفحة 2 من 2'}</span>
            </div>
          </div>
        </div>
      `
    } else {
      questionsBookletHtml = `
        <div class="exam-package-page questions-booklet-page a4-page-1">
          <div class="a4-sheet-page sheet-page-1" dir="${isEnglish ? 'ltr' : 'rtl'}">
            <div class="page-content-wrapper">
              <div class="header-box-wrapper mb-1">
                ${headerTableHtml}
              </div>

              ${tfQuestions.length > 0 ? `
                <div class="tf-section-wrapper mb-1">
                  <div class="instruction-banner ${isEnglish ? 'text-start ps-2' : 'text-center'} py-1 font-weight-bold">
                    ${tfInstructionText}
                  </div>
                  ${renderTfTable(tfQuestions)}
                </div>
              ` : ''}

              ${mcqQuestions.length > 0 ? `
                <div class="mcq-section-wrapper">
                  <div class="instruction-banner ${isEnglish ? 'text-start ps-2' : 'text-center'} py-1 font-weight-bold">
                    ${mcqInstructionText}
                  </div>
                  ${renderContinuousMcqTable(mcqQuestions)}
                </div>
              ` : ''}

              <div class="exam-paper-end-banner text-center font-weight-black">
                ${endBannerText}
              </div>
            </div>

            <div class="a4-page-footer d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
              <span>${isEnglish ? 'English' : options.subjectName} • ${isEnglish ? 'Form' : 'النموذج'} (${options.versionCode || '1'})</span>
              <span>${isEnglish ? 'Page 1 of 1' : 'الصفحة 1 من 1'}</span>
            </div>
          </div>
        </div>
      `
    }
  }

  let omrPageHtml = ''
  if (options.mode !== 'questions_only' && options.omrElement) {
    const cloned = options.omrElement.cloneNode(true) as HTMLElement | SVGGraphicsElement
    if (cloned instanceof SVGElement) {
      cloned.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
      cloned.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
    } else if (cloned instanceof HTMLElement) {
      cloned.querySelectorAll('.d-print-none, .report-action-bar, button, .v-btn').forEach(b => b.remove())
    }

    // Inlining all images in cloned SVG/HTML so that the Eagle logo and other assets are guaranteed to appear
    const images = Array.from(cloned.querySelectorAll('image'))
    for (const imgEl of images) {
      const href = imgEl.getAttribute('href') || imgEl.getAttribute('xlink:href') || ''
      if (href.includes('eagle') && eagleBase64.startsWith('data:')) {
        imgEl.setAttribute('href', eagleBase64)
        imgEl.setAttribute('xlink:href', eagleBase64)
      } else if (href && !href.startsWith('data:')) {
        try {
          const fullUrl = href.startsWith('http') ? href : `${window.location.origin}${href}`
          const resp = await fetch(fullUrl)
          if (resp.ok) {
            const blob = await resp.blob()
            const b64 = await new Promise<string>((resolve, reject) => {
              const reader = new FileReader()
              reader.onloadend = () => resolve(reader.result as string)
              reader.onerror = reject
              reader.readAsDataURL(blob)
            })
            imgEl.setAttribute('href', b64)
            imgEl.setAttribute('xlink:href', b64)
          }
        } catch (e) {
          console.warn('Could not inline image for print:', href, e)
        }
      }
    }
    const htmlImgs = Array.from(cloned.querySelectorAll('img'))
    for (const imgEl of htmlImgs) {
      const src = imgEl.getAttribute('src') || ''
      if (src.includes('eagle') && eagleBase64.startsWith('data:')) {
        imgEl.setAttribute('src', eagleBase64)
      }
    }

    omrPageHtml = `
      <div class="exam-package-page omr-attachment-page">
        ${cloned.outerHTML}
      </div>
    `
  }

  const headStyles = `
    @page {
      size: ${isA3 ? 'A3 landscape' : 'A4 portrait'};
      margin: 6mm 8mm !important;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    html, body {
      margin: 0 !important;
      padding: 0 !important;
      width: 100% !important;
      background: #ffffff !important;
      font-family: 'Tajawal', 'Cairo', Tahoma, Arial, sans-serif !important;
      color: #000 !important;
      direction: ${isEnglish ? 'ltr' : 'rtl'};
    }
    .exam-package-page {
      width: 100% !important;
      box-sizing: border-box;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .exam-package-page:not(:last-child) {
      page-break-after: always !important;
      break-after: page !important;
    }
    .exam-package-page:last-child {
      page-break-after: auto !important;
      break-after: auto !important;
    }
    .a4-sheet-page {
      width: 100% !important;
      min-height: 0 !important;
      height: auto !important;
      padding: 4mm 6mm !important;
      margin: 0 !important;
      border: none !important;
      box-shadow: none !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
    }
    .a4-page-footer {
      font-size: 0.68rem !important;
      border-top: 1px solid #000000 !important;
      padding-top: 3px !important;
      margin-top: 6px !important;
    }
    .reading-passage-box {
      border: 1px solid #000000 !important;
      margin-bottom: 3px !important;
    }
    .passage-text-content {
      font-size: 0.74rem !important;
      line-height: 1.35 !important;
      background: #ffffff !important;
      padding: 4px 6px !important;
      font-weight: 600 !important;
      border-top: 1px solid #000000 !important;
    }
    table {
      border-collapse: collapse !important;
    }
    .exam-sheet-frame {
      width: 100% !important;
    }
    .columns-two {
      display: grid !important;
      grid-template-columns: 1fr 1fr !important;
      gap: 8mm !important;
      width: 100% !important;
    }
    .official-header-box {
      width: 100% !important;
      margin: 0 auto 4px auto !important;
      border: 1.5px solid #000000 !important;
      background-color: #ffffff !important;
      font-family: 'Arial', 'Simplified Arabic', Tahoma, sans-serif !important;
      color: #000000 !important;
      box-sizing: border-box !important;
    }
    .table-top-section {
      width: 100% !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      background-color: #ffffff !important;
    }
    .table-top-section td {
      border: 1px solid #000000 !important;
      padding: 2px 2px !important;
      text-align: center !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      font-size: 0.68rem !important;
      line-height: 1.15 !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }
    .student-photo-cell {
      width: 17.5% !important;
      padding: 2px !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
    }
    .student-photo-frame {
      width: 82px !important;
      height: 100px !important;
      border: 1px solid #000000 !important;
      margin: 0 auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #fafafa !important;
      overflow: hidden !important;
      box-sizing: border-box !important;
    }
    .student-photo-img {
      width: 100% !important;
      height: 100% !important;
      object-fit: cover !important;
      display: block !important;
    }
    .photo-placeholder {
      font-size: 0.70rem !important;
      font-weight: 800 !important;
      color: #222 !important;
      text-align: center !important;
      width: 100% !important;
      height: 100% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .emblem-cell {
      width: 19.0% !important;
      padding: 2px 2px !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
    }
    .republic-logo {
      width: 44px !important;
      height: auto !important;
      max-height: 32px !important;
      object-fit: contain !important;
      display: block !important;
      margin: 0 auto 2px auto !important;
    }
    .table-bottom-bar {
      width: 100% !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      border-top: 1px solid #000000 !important;
      background-color: #ffffff !important;
    }
    .table-bottom-bar td {
      border: 1px solid #000000 !important;
      padding: 2px 2px !important;
      text-align: center !important;
      vertical-align: middle !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      font-size: 0.76rem !important;
      line-height: 1.15 !important;
      white-space: nowrap !important;
      box-sizing: border-box !important;
    }
    .table-tf {
      border: 1px solid #000 !important;
      font-size: 0.74rem !important;
      width: 100% !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      background-color: #ffffff !important;
      margin-bottom: 4px;
    }
    .table-tf td {
      border: 1px solid #000 !important;
      padding: 1.5px 3px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
    }
    .q-paren-cell {
      white-space: nowrap !important;
      word-break: keep-all !important;
      direction: ltr !important;
      text-align: center !important;
      letter-spacing: 0 !important;
      font-family: monospace, sans-serif !important;
      font-size: 0.85rem !important;
      font-weight: 900 !important;
    }
    .q-text-cell {
      unicode-bidi: plaintext !important;
    }
    .table-mcq-continuous {
      border: 1px solid #000 !important;
      border-collapse: collapse !important;
      table-layout: fixed !important;
      width: 100% !important;
      background-color: #ffffff !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      margin-bottom: 4px;
    }
    .table-mcq-continuous td {
      border: 1px solid #000 !important;
      padding: 1px 2px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
    }
    .q-num-cell {
      font-family: monospace, sans-serif !important;
      font-weight: 900 !important;
      font-size: 0.82rem !important;
      background: #ffffff !important;
      text-align: center !important;
    }
    .q-stem-cell {
      font-size: 0.75rem !important;
      line-height: 1.25 !important;
      font-weight: 700 !important;
      unicode-bidi: plaintext !important;
    }
    .opt-num-cell {
      font-family: monospace, sans-serif !important;
      font-weight: 900 !important;
      font-size: 0.74rem !important;
      background: #ffffff !important;
      text-align: center !important;
    }
    .opt-text-cell {
      font-size: 0.70rem !important;
      font-weight: 700 !important;
      text-align: center !important;
      white-space: nowrap !important;
      overflow: hidden !important;
      text-overflow: ellipsis !important;
      unicode-bidi: plaintext !important;
    }
    .instruction-banner {
      font-size: 0.70rem !important;
      font-weight: 800 !important;
      border: 1px solid #000 !important;
      border-bottom: 0 !important;
      padding: 2.5px 4px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      line-height: 1.2 !important;
    }
    .secret-press-ribbon {
      font-size: 0.68rem !important;
      border-bottom: 1px solid #000 !important;
      padding-bottom: 2px !important;
      margin-bottom: 4px !important;
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      font-weight: 800 !important;
    }
    .exam-paper-end-banner {
      font-size: 0.76rem !important;
      font-weight: 900 !important;
      border: 1px solid #000 !important;
      padding: 3px 6px !important;
      background-color: #ffffff !important;
      color: #000000 !important;
      text-align: center !important;
      margin-top: 6px !important;
    }
    .omr-attachment-page {
      width: 100% !important;
      display: block;
      margin: 0 !important;
      padding: 0 !important;
      max-height: 282mm !important;
      overflow: hidden !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      page-break-after: avoid !important;
      break-after: avoid !important;
    }
    .omr-attachment-page .yemeni-audit-report-sheet {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 auto !important;
      padding: 0 !important;
    }
    .omr-attachment-page svg {
      width: 100% !important;
      height: auto !important;
      max-width: 100% !important;
      max-height: 280mm !important;
      display: block !important;
      margin: auto !important;
    }
    .table-header-official td {
      border: 1px solid #000 !important;
      padding: 1.5px 2.5px !important;
      font-size: 0.72rem !important;
      line-height: 1.15 !important;
    }
    .table-audit th {
      border: 1px solid #000 !important;
      padding: 1.5px 0.5px !important;
      font-size: 0.54rem !important;
      line-height: 1.12 !important;
      font-weight: 700 !important;
      text-align: center !important;
    }
    .table-audit td {
      border: 1px solid #000 !important;
      padding: 1px 1px !important;
      font-size: 0.65rem !important;
      line-height: 1.10 !important;
      text-align: center !important;
    }
    .audit-matrix-grid {
      display: grid !important;
      grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
      gap: 3px !important;
      width: 100% !important;
    }
    .d-print-none, .report-action-bar, button, .v-btn {
      display: none !important;
    }
    .bg-grey-lighten-4, .bg-grey-lighten-5 { background-color: #ffffff !important; }
    .text-center { text-align: center !important; }
    .text-start { text-align: start !important; }
    .text-end { text-align: end !important; }
    .font-weight-bold { font-weight: 700 !important; }
    .font-weight-black { font-weight: 900 !important; }
    .font-mono { font-family: monospace, sans-serif !important; }
  `

  const docStyles = Array.from(document.querySelectorAll('style, link[rel="stylesheet"]'))
    .map(el => el.outerHTML)
    .join('\n')

  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html dir="${isEnglish ? 'ltr' : 'rtl'}" lang="${isEnglish ? 'en' : 'ar'}">
      <head>
        <meta charset="utf-8">
        <base href="${window.location.origin}/">
        <title>${options.title || `حزمة_اختبار_${options.subjectName}_النموذج_${options.versionCode}`}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
        ${docStyles}
        <style>${headStyles}</style>
      </head>
      <body>
        ${questionsBookletHtml}
        ${omrPageHtml}
      </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    iframe.contentWindow?.focus()
    iframe.contentWindow?.print()
    setTimeout(() => {
      if (document.body.contains(iframe)) {
        document.body.removeChild(iframe)
      }
    }, 4000)
  }, 500)
}
