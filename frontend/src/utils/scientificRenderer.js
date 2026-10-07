/**
 * Scientific & Mathematical Markup Renderer
 * Supports LaTeX, KaTeX, Chemistry equations, Physics notation, Greek alphabet,
 * Markdown tables, and Syntax-highlighted code blocks.
 */

export function ensureKaTeXLoaded() {
  if (typeof window === 'undefined') return
  if (window.katex) return

  if (!document.getElementById('katex-css')) {
    const link = document.createElement('link')
    link.id = 'katex-css'
    link.rel = 'stylesheet'
    link.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css'
    document.head.appendChild(link)
  }

  if (!document.getElementById('katex-js')) {
    const script = document.createElement('script')
    script.id = 'katex-js'
    script.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'
    script.async = true
    document.head.appendChild(script)
  }
}

export function parseScientificMarkup(raw) {
  if (!raw || typeof raw !== 'string') return ''

  let html = raw

  // 1. Parse Code Blocks ```lang ... ```
  html = html.replace(/```([a-zA-Z0-9_]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<div class="code-block-wrapper my-3 rounded-lg overflow-hidden border-subtle">
      <div class="code-block-header px-3 py-1 bg-surface-variant d-flex justify-space-between align-center font-mono text-caption">
        <span class="text-uppercase font-weight-bold text-primary">${lang || 'code'}</span>
        <span>كود برمجي</span>
      </div>
      <pre class="pa-3 ma-0 text-ltr font-mono" style="background: rgba(0,0,0,0.85); color: #e2e8f0; overflow-x: auto; font-size: 0.88rem; direction: ltr; text-align: left;"><code>${escapeHtml(code.trim())}</code></pre>
    </div>`
  })

  // 2. Parse Inline Code `...`
  html = html.replace(/`([^`]+)`/g, (match, code) => {
    return `<code class="px-1 py-0.5 rounded font-mono text-primary bg-surface-variant font-weight-bold" style="direction: ltr; display: inline-block;">${escapeHtml(code)}</code>`
  })

  // 3. Parse Markdown Tables
  html = html.replace(/(?:^|\n)(\|.+?\|\n\|[-:| ]+?\|\n(?:\|.+?\|\n?)+)/g, (match, tableText) => {
    return renderMarkdownTable(tableText)
  })

  // 4. Render Math & Chemistry Formulas ($$...$$ and $...$)
  // Display Math ($$...$$)
  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (match, tex) => {
    return renderTex(tex.trim(), true)
  })

  // Inline Math ($...$)
  html = html.replace(/\$([^\$\n]+?)\$/g, (match, tex) => {
    return renderTex(tex.trim(), false)
  })

  // 5. Line Breaks
  html = html.replace(/\n/g, '<br>')

  return html
}

function renderTex(tex, displayMode) {
  // Option A: Use KaTeX if available
  if (typeof window !== 'undefined' && window.katex) {
    try {
      return window.katex.renderToString(tex, {
        displayMode: displayMode,
        throwOnError: false
      })
    } catch (e) {
      // Fallback
    }
  }

  // Option B: Built-in Resilient Fallback Math Engine (Pure HTML + CSS)
  return fallbackMathRenderer(tex, displayMode)
}

function fallbackMathRenderer(tex, displayMode) {
  let res = tex

  // Chemistry arrows
  res = res.replace(/\\rightarrow/g, ' &rarr; ')
  res = res.replace(/\\rightleftharpoons/g, ' &#8652; ')
  res = res.replace(/\\xrightarrow\{\\Delta\}/g, ' <span class="math-arrow-cond">&Delta;&rarr;</span> ')
  res = res.replace(/\\xrightarrow\{([^}]+)\}/g, ' <span class="math-arrow-cond"><sup>$1</sup>&rarr;</span> ')
  res = res.replace(/\\uparrow/g, ' &uarr; ')
  res = res.replace(/\\downarrow/g, ' &darr; ')

  // Fractions: \frac{num}{den}
  res = res.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '<span class="inline-fraction"><span class="numerator">$1</span><span class="fraction-bar"></span><span class="denominator">$2</span></span>')

  // Roots: \sqrt[n]{x} and \sqrt{x}
  res = res.replace(/\\sqrt\[([^\]]+)\]\{([^}]+)\}/g, '<span class="math-root"><sup>$1</sup>&radic;<span class="root-overbar">$2</span></span>')
  res = res.replace(/\\sqrt\{([^}]+)\}/g, '<span class="math-root">&radic;<span class="root-overbar">$1</span></span>')

  // Superscript & Subscript: x^{2} and x_{1}
  res = res.replace(/\^{([^}]+)\}/g, '<sup>$1</sup>')
  res = res.replace(/\^([0-9a-zA-Z+-]+)/g, '<sup>$1</sup>')
  res = res.replace(/_\{([^}]+)\}/g, '<sub>$1</sub>')
  res = res.replace(/_([0-9a-zA-Z+-]+)/g, '<sub>$1</sub>')

  // Integrals & Summations
  res = res.replace(/\\int/g, '<span class="math-big-symbol">&int;</span>')
  res = res.replace(/\\iint/g, '<span class="math-big-symbol">&int;&int;</span>')
  res = res.replace(/\\oint/g, '<span class="math-big-symbol">&#8750;</span>')
  res = res.replace(/\\sum/g, '<span class="math-big-symbol">&sum;</span>')
  res = res.replace(/\\prod/g, '<span class="math-big-symbol">&prod;</span>')
  res = res.replace(/\\lim/g, '<span class="math-op">lim</span>')

  // Greek letters
  const greekMap = {
    '\\alpha': '&alpha;', '\\beta': '&beta;', '\\gamma': '&gamma;', '\\delta': '&delta;',
    '\\epsilon': '&epsilon;', '\\theta': '&theta;', '\\lambda': '&lambda;', '\\mu': '&mu;',
    '\\nu': '&nu;', '\\pi': '&pi;', '\\rho': '&rho;', '\\sigma': '&sigma;', '\\tau': '&tau;',
    '\\phi': '&phi;', '\\omega': '&omega;', '\\Delta': '&Delta;', '\\Theta': '&Theta;',
    '\\Lambda': '&Lambda;', '\\Sigma': '&Sigma;', '\\Omega': '&Omega;', '\\infty': '&infin;',
    '\\pm': '&plusmn;', '\\times': '&times;', '\\div': '&divide;', '\\ne': '&ne;',
    '\\le': '&le;', '\\ge': '&ge;', '\\approx': '&asymp;', '\\in': '&isin;', '\\notin': '&notin;',
    '\\subset': '&sub;', '\\cup': '&cup;', '\\cap': '&cap;', '\\emptyset': '&empty;',
    '\\land': '&and;', '\\lor': '&or;', '\\neg': '&not;', '\\oplus': '&oplus;',
    '\\implies': '&rArr;', '\\iff': '&hArr;', '\\forall': '&forall;', '\\exists': '&exist;',
    '\\nabla': '&nabla;', '\\circ': '&deg;'
  }
  for (const [key, val] of Object.entries(greekMap)) {
    res = res.replaceAll(key, val)
  }

  // Text inside math \text{...}
  res = res.replace(/\\text\{([^}]+)\}/g, '<span class="math-text">$1</span>')
  res = res.replace(/\\mathbb\{R\}/g, '<span class="font-weight-bold font-serif">&#8477;</span>')
  res = res.replace(/\\mathbb\{Z\}/g, '<span class="font-weight-bold font-serif">&#8484;</span>')
  res = res.replace(/\\mathbb\{N\}/g, '<span class="font-weight-bold font-serif">&#8469;</span>')
  res = res.replace(/\\mathbb\{C\}/g, '<span class="font-weight-bold font-serif">&#8450;</span>')

  // Vectors: \vec{v}
  res = res.replace(/\\vec\{([^}]+)\}/g, '<span class="math-vec">$1&#8407;</span>')

  // Matrices: \begin{pmatrix} ... \end{pmatrix}
  res = res.replace(/\\begin\{pmatrix\}([\s\S]+?)\\end\{pmatrix\}/g, (match, inner) => {
    const rows = inner.split('\\\\').map(r => r.split('&').map(c => c.trim()))
    let matrixHtml = '<span class="inline-matrix pmatrix"><span class="matrix-bracket left">(</span><table class="matrix-table">'
    rows.forEach(r => {
      matrixHtml += '<tr>'
      r.forEach(c => { matrixHtml += `<td>${fallbackMathRenderer(c, false)}</td>` })
      matrixHtml += '</tr>'
    })
    matrixHtml += '</table><span class="matrix-bracket right">)</span></span>'
    return matrixHtml
  })

  // Determinants: \begin{vmatrix} ... \end{vmatrix}
  res = res.replace(/\\begin\{vmatrix\}([\s\S]+?)\\end\{vmatrix\}/g, (match, inner) => {
    const rows = inner.split('\\\\').map(r => r.split('&').map(c => c.trim()))
    let matrixHtml = '<span class="inline-matrix vmatrix"><span class="matrix-bracket bar">|</span><table class="matrix-table">'
    rows.forEach(r => {
      matrixHtml += '<tr>'
      r.forEach(c => { matrixHtml += `<td>${fallbackMathRenderer(c, false)}</td>` })
      matrixHtml += '</tr>'
    })
    matrixHtml += '</table><span class="matrix-bracket bar">|</span></span>'
    return matrixHtml
  })

  // Clean remaining braces
  res = res.replace(/\\left\(/g, '(').replace(/\\right\)/g, ')')
  res = res.replace(/\\left\[/g, '[').replace(/\\right\]/g, ']')
  res = res.replace(/\\left\|/g, '|').replace(/\\right\|/g, '|')
  res = res.replace(/\\\,/g, ' ')

  const wrapClass = displayMode ? 'math-display-block my-2 text-center' : 'math-inline'
  return `<span class="${wrapClass} text-ltr" style="direction: ltr; display: ${displayMode ? 'block' : 'inline-flex'}; align-items: center;">${res}</span>`
}

function renderMarkdownTable(tableText) {
  const lines = tableText.trim().split('\n')
  if (lines.length < 2) return tableText

  const headerCells = lines[0].split('|').filter(c => c.trim().length > 0).map(c => c.trim())
  const rows = lines.slice(2).map(line => {
    return line.split('|').filter(c => c.trim().length > 0).map(c => c.trim())
  })

  let html = `<div class="my-3 overflow-x-auto"><table class="scientific-table w-100 rounded-lg border-subtle"><thead><tr class="bg-surface-variant">`
  headerCells.forEach(h => {
    html += `<th class="pa-2 text-center font-weight-bold border-subtle">${parseScientificMarkup(h)}</th>`
  })
  html += `</tr></thead><tbody>`

  rows.forEach(r => {
    html += `<tr>`
    r.forEach(c => {
      html += `<td class="pa-2 text-center border-subtle">${parseScientificMarkup(c)}</td>`
    })
    html += `</tr>`
  })

  html += `</tbody></table></div>`
  return html
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}
