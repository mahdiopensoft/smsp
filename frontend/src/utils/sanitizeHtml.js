import DOMPurify from 'dompurify'

/**
 * Sanitize HTML strings before rendering via v-html while preserving
 * rich-text formatting, KaTeX/MathML notation, SVG graphics, and RTL attributes.
 */
export function sanitizeHtml(dirty) {
  if (dirty == null || dirty === '') return ''
  return DOMPurify.sanitize(String(dirty), {
    USE_PROFILES: { html: true, mathMl: true, svg: true },
    ADD_ATTR: ['target', 'dir', 'style', 'class', 'colspan', 'rowspan'],
    FORBID_TAGS: ['script', 'iframe', 'object', 'embed', 'form', 'base', 'meta'],
    FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover', 'onfocus', 'onblur'],
  })
}
