/**
 * Image shape templates definition (قوالب أشكال الصور والشعارات)
 */
export const IMAGE_SHAPES = [
  { key: 'default', label: 'افتراضي قياسي', icon: 'mdi-crop-square', desc: 'زوايا ناعمة كلاسيكية' },
  { key: 'circle', label: 'دائري كامل', icon: 'mdi-circle-outline', desc: 'إطار دائري مستدير' },
  { key: 'card', label: 'بطاقة عائمة', icon: 'mdi-card-outline', desc: 'خلفية بيضاء بظل خفيف' },
  { key: 'squircle', label: 'كبسولة ناعمة', icon: 'mdi-square-rounded', desc: 'حواف مستديرة حديثة' },
  { key: 'badge', label: 'ختم رسمي', icon: 'mdi-seal', desc: 'إطار مسنن ومزدوج' },
  { key: 'frame', label: 'إطار كلاسيكي', icon: 'mdi-image-frame', desc: 'إطار بلون السمة' },
  { key: 'pill', label: 'كبسولة أفقية', icon: 'mdi-pill', desc: 'استدارة كاملة عريضة' },
  { key: 'glow', label: 'توهج مضيء', icon: 'mdi-shimmer', desc: 'ظل متوهج فاخر' },
  { key: 'polaroid', label: 'بولارويد', icon: 'mdi-camera-metering-spot', desc: 'إطار صور تذكارية' },
  { key: 'stamp-double', label: 'ختم وزاري مزدوج', icon: 'mdi-stamper', desc: 'إطار رسمي مزدوج' },
  { key: 'shadow-3d', label: 'بروز 3D فاخر', icon: 'mdi-cube-outline', desc: 'تأثير ظل عميق ثلاثي الأبعاد' },
  { key: 'glass', label: 'زجاجي شفاف', icon: 'mdi-blur', desc: 'مظهر زجاجي شفاف ناعم' },
]

/**
 * Parse token into base variable key, width, and shape
 * Examples:
 * - "{{organizationLogo}}" -> { baseKey: "{{organizationLogo}}", width: 80, shape: 'default' }
 * - "{{organizationLogo|140}}" -> { baseKey: "{{organizationLogo}}", width: 140, shape: 'default' }
 * - "{{organizationLogo|140|circle}}" -> { baseKey: "{{organizationLogo}}", width: 140, shape: 'circle' }
 * - "{{organizationLogo|circle}}" -> { baseKey: "{{organizationLogo}}", width: 80, shape: 'circle' }
 */
export const IMAGE_FITS = [
  { key: 'contain', label: 'احتواء (Contain)', icon: 'mdi-arrow-collapse-all', desc: 'عرض الصورة كاملة مع الحفاظ على نسبتها دون قص' },
  { key: 'cover', label: 'تغطية (Cover)', icon: 'mdi-crop', desc: 'ملء الإطار بالكامل وقص الحواف الزائدة' },
  { key: 'fill', label: 'تمدد (Fill)', icon: 'mdi-arrow-expand-all', desc: 'مط الصورة لتملأ كامل المساحة المحددة' },
  { key: 'none', label: 'أصلي (None)', icon: 'mdi-image-size-select-actual', desc: 'الحجم الفعلي دون أي تحجيم أو مط' },
  { key: 'scale-down', label: 'تصغير (Scale-down)', icon: 'mdi-arrow-collapse', desc: 'تصغير ذكي فقط إذا كانت أكبر من المساحة' },
]

export const parseToken = (token) => {
  const clean = token.replace(/[{}]/g, '')
  const parts = clean.split('|')
  const baseKey = '{{' + parts[0] + '}}'
  
  let width = 80
  let height = 80
  let shape = 'default'
  let opacity = 100
  let fit = 'contain'

  const KNOWN_FITS = ['contain', 'cover', 'fill', 'none', 'scale-down']
  const KNOWN_SHAPES = ['default', 'circle', 'card', 'squircle', 'badge', 'frame', 'pill', 'glow', 'polaroid', 'stamp-double', 'shadow-3d', 'glass']

  let hasExplicitDims = false
  let shapeSeen = false
  let numericDimCount = 0

  for (let i = 1; i < parts.length; i++) {
    const p = parts[i].trim()
    if (!p) continue

    // 1. Dimensions like 120x80 or 80x80
    if (p.includes('x') && !isNaN(parseInt(p.split('x')[0])) && !isNaN(parseInt(p.split('x')[1]))) {
      const dimParts = p.split('x')
      width = parseInt(dimParts[0]) || 80
      height = parseInt(dimParts[1]) || width
      hasExplicitDims = true
    }
    // 2. Fits
    else if (KNOWN_FITS.includes(p) || p.startsWith('fit:')) {
      fit = p.replace('fit:', '')
    }
    // 3. Opacity with explicit unit or prefix (e.g. 60%, op60, opacity:60)
    else if (p.startsWith('op') || p.endsWith('%') || p.startsWith('opacity:')) {
      const val = parseInt(p.replace(/[^0-9]/g, ''))
      if (!isNaN(val) && val >= 5 && val <= 100) opacity = val
    }
    // 4. Known Shapes
    else if (KNOWN_SHAPES.includes(p) || p.startsWith('shape:')) {
      shape = p.replace('shape:', '')
      shapeSeen = true
    }
    // 5. Bare numeric value: dimension vs opacity
    else if (!isNaN(parseInt(p)) && String(parseInt(p)) === p) {
      const num = parseInt(p)
      if (hasExplicitDims || shapeSeen) {
        // If dimensions were already set or we passed the shape parameter, this bare number is opacity!
        if (num >= 5 && num <= 100) {
          opacity = num
        }
      } else {
        numericDimCount++
        if (numericDimCount === 1) {
          width = num
          height = num
        } else if (numericDimCount === 2) {
          height = num
        } else if (numericDimCount >= 3 && num >= 5 && num <= 100) {
          opacity = num
        }
      }
    } else {
      shape = p
      shapeSeen = true
    }
  }

  return {
    baseKey,
    width: (width > 0 && width <= 600) ? width : 80,
    height: (height > 0 && height <= 600) ? height : width,
    shape: shape || 'default',
    opacity: (opacity >= 5 && opacity <= 100) ? opacity : 100,
    fit: KNOWN_FITS.includes(fit) ? fit : 'contain'
  }
}

/**
 * Generate chip HTML for a variable matching the exact design
 * In editor and canvas, all variables appear as consistent, elegant pill chips.
 * Image variables include a subtle edit button to customize shape and size.
 *
 * @param {string} varKey - e.g. "{{userName}}" or "{{organizationLogo|120|circle}}"
 * @param {Array} allVariables - list of available variable objects
 * @param {boolean} isEditor - whether rendering inside the interactive rich editor
 * @returns {string} HTML string
 */
export const createChipHTML = (varKey, allVariables = [], isEditor = false) => {
  const { baseKey, width, height, shape, opacity, fit } = parseToken(varKey)
  const cleanKey = baseKey.replace(/[{}]/g, '')
  const found = allVariables.find(v =>
    v.name_code === cleanKey ||
    v.key === baseKey ||
    v.key === cleanKey ||
    (v.name_code && `{{${v.name_code}}}` === baseKey)
  )
  const label = found?.name_ar || found?.label || cleanKey
  const hasImage = !!found?.image || (found?.icon && (found.icon.includes('image') || found.icon.includes('photo'))) || cleanKey.toLowerCase().includes('logo') || cleanKey.toLowerCase().includes('image') || cleanKey.toLowerCase().includes('stamp') || cleanKey.toLowerCase().includes('avatar')
  const imgSrc = found?.image || ''
  const iconName = found?.icon || (hasImage ? 'mdi-image-outline' : 'mdi-variable')

  const closeSvg = `<svg style="width:10px;height:10px;display:block;" viewBox="0 0 24 24"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/></svg>`
  const editSvg = `<svg style="width:10px;height:10px;display:block;" viewBox="0 0 24 24"><path fill="currentColor" d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.07,6.19L3,17.25Z"/></svg>`

  // 1. Image Variable Chip (Shows thumbnail if available, or image-off icon if no image)
  if (hasImage) {
    const editBtn = isEditor ? `<button type="button" class="hf-canvas-chip-edit" data-action="edit-image" title="تعديل قالب وحجم وأبعاد وشفافية وملاءمة الصورة">${editSvg}</button>` : ''
    const dimText = (width === height) ? `${width}px` : `${width}×${height}px`
    const customInfo = (width !== 80 || height !== 80 || shape !== 'default' || opacity !== 100 || fit !== 'contain') ? `<span class="hf-chip-size-tag">${dimText}${opacity < 100 ? ` / ${opacity}%` : ''}</span>` : ''

    const cleanSrc = (imgSrc && typeof imgSrc === 'string' && imgSrc.startsWith('data:image/svg+xml;utf8,<svg'))
      ? ('data:image/svg+xml;utf8,' + encodeURIComponent(imgSrc.substring('data:image/svg+xml;utf8,'.length)))
      : imgSrc

    const thumbHTML = cleanSrc
      ? `<img src="${cleanSrc}" class="hf-canvas-chip-thumb" style="opacity: ${opacity / 100}; object-fit: ${fit};" alt="thumb" onerror="this.style.display='none'" />`
      : `<i class="mdi mdi-image-off-outline me-1" style="font-size:13px;color:#94a3b8;vertical-align:middle;display:inline-flex;" title="لا توجد صورة"></i>`

    return `<span class="hf-canvas-chip is-image" contenteditable="false" data-token="${baseKey}" data-width="${width}" data-height="${height}" data-shape="${shape}" data-opacity="${opacity}" data-fit="${fit}" data-img="${cleanSrc}" title="${baseKey} (${label})">${thumbHTML}<span class="hf-canvas-chip-label">${label}</span>${customInfo}${editBtn}<button type="button" class="hf-canvas-chip-remove" data-action="delete-chip" title="حذف الصورة">${closeSvg}</button></span>&nbsp;`
  }

  // 2. Regular Text Variable Pill Chip
  const mediaHTML = `<i class="mdi ${iconName} me-1" style="font-size:12px;vertical-align:middle;display:inline-flex;color:${found?.color ? `var(--v-theme-${found.color})` : 'inherit'};"></i>`
  return `<span class="hf-canvas-chip" contenteditable="false" data-token="${baseKey}" title="${baseKey}">${mediaHTML}<span class="hf-canvas-chip-label">${label}</span><button type="button" class="hf-canvas-chip-remove" data-action="delete-chip" title="حذف المتغير">${closeSvg}</button></span>&nbsp;`
}

/**
 * Convert template string with {{var}} or {{var|width|shape}} to Rich Editor HTML
 * @param {string} content - raw template string
 * @param {Array} allVariables - list of variable objects
 * @returns {string} HTML string for contenteditable editor
 */
export const templateToEditorHTML = (content, allVariables = []) => {
  if (!content) return ''
  const regex = /(\{\{[^}]+?\}\})/g
  return content.replace(regex, (match) => {
    return createChipHTML(match, allVariables, true)
  })
}

/**
 * Render canvas cell HTML (consistent chip pills matching user request)
 * @param {string} content
 * @param {Array} allVariables
 * @returns {string}
 */
export const renderCanvasCellHTML = (content, allVariables = []) => {
  if (!content) return ''
  const regex = /(\{\{[^}]+?\}\})/g
  return content.replace(regex, (match) => {
    return createChipHTML(match, allVariables, false)
  })
}

/**
 * Convert Rich Editor DOM back to clean template string while PRESERVING HTML styling and encoded image dimensions/shapes/opacity/fit
 * @param {HTMLElement} el - the rich editor container element
 * @returns {string} template string with {{tokens}}
 */
export const editorHTMLToTemplate = (el) => {
  if (!el) return ''
  const clone = el.cloneNode(true)

  const chips = clone.querySelectorAll('.hf-canvas-chip, .hf-editor-chip')
  chips.forEach(chip => {
    const rawToken = chip.getAttribute('data-token')
    if (rawToken) {
      const cleanBase = '{{' + rawToken.replace(/[{}]/g, '').split('|')[0] + '}}'
      const width = parseInt(chip.getAttribute('data-width')) || 80
      const height = parseInt(chip.getAttribute('data-height')) || width
      const shape = chip.getAttribute('data-shape') || 'default'
      const opacity = parseInt(chip.getAttribute('data-opacity')) || 100
      const fit = chip.getAttribute('data-fit') || 'contain'
      let encodedToken = cleanBase
      if (shape !== 'default' || width !== 80 || height !== 80 || opacity !== 100 || fit !== 'contain') {
        const dimStr = (width === height) ? `${width}` : `${width}x${height}`
        encodedToken = cleanBase.replace('}}', `|${dimStr}|${shape}|${opacity}%|${fit}}}`)
      }
      const textNode = document.createTextNode(encodedToken)
      chip.parentNode.replaceChild(textNode, chip)
    } else {
      chip.remove()
    }
  })

  return clone.innerHTML
}

/**
 * Parse cell segments into plain text vs variables
 * @param {string} content
 * @param {Array} allVariables
 * @returns {Array} list of segment objects
 */
export const parseCellSegments = (content, allVariables = []) => {
  if (!content) return []
  const regex = /(\{\{[^}]+?\}\})/g
  const parts = content.split(regex)
  return parts.filter(p => p && p.length > 0).map(part => {
    if (part.startsWith('{{') && part.endsWith('}}')) {
      const { baseKey, width, shape } = parseToken(part)
      const foundVar = allVariables.find(v => v.key === baseKey)
      const cleanKey = baseKey.replace(/[{}]/g, '')
      return {
        isVar: true,
        key: baseKey,
        width,
        shape,
        label: foundVar?.label || cleanKey,
        image: foundVar?.image || null,
        icon: foundVar?.icon || (foundVar?.image ? 'mdi-image-outline' : 'mdi-variable'),
        color: foundVar?.color || (foundVar?.image ? 'indigo' : 'primary'),
      }
    }
    return {
      isVar: false,
      text: part,
    }
  })
}
