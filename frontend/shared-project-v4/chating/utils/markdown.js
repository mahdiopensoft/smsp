import hljs from 'highlight.js'
import MarkdownIt from 'markdown-it'
import 'highlight.js/styles/github-dark.css' // أو أي ستايل آخر تفضله

// تكوين Markdown-it
const md = new MarkdownIt({
  html: false, // تعطيل HTML للأمان
  xhtmlOut: false, // استخدام '/' لإغلاق العلامات الفردية (<br />).
  breaks: true, // تحويل \n إلى <br>
  langPrefix: 'hljs language-', // بادئة CSS لكتل الكود
  linkify: true, // تحويل الروابط النصية إلى روابط قابلة للنقر
  typographer: true, // تحسين الطباعة (مثل الاستبدالات الذكية)
  quotes: '“”‘’',

  // دالة التظليل للكود
  highlight (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>'
          + hljs.highlight(str, { language: lang, ignoreIllegals: true }).value
          + '</code></pre>'
      } catch {}
    }

    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  },
})

// تخصيص فتح الروابط في تبويب جديد
const defaultRender = md.renderer.rules.link_open || function (tokens, idx, options, env, self) {
  return self.renderToken(tokens, idx, options)
}

md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  // إضافة target="_blank"
  const aIndex = tokens[idx].attrIndex('target')

  if (aIndex < 0) {
    tokens[idx].attrPush(['target', '_blank'])
  } else {
    tokens[idx].attrs[aIndex][1] = '_blank'
  }

  // إضافة rel="noopener noreferrer" للأمان
  const relIndex = tokens[idx].attrIndex('rel')
  if (relIndex < 0) {
    tokens[idx].attrPush(['rel', 'noopener noreferrer'])
  } else {
    tokens[idx].attrs[relIndex][1] = 'noopener noreferrer'
  }

  return defaultRender(tokens, idx, options, env, self)
}

export function renderMarkdown (text) {
  if (!text) {
    return ''
  }
  return md.render(text)
}
