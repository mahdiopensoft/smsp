/**
 * tooltip.js — نسخة مُحسَّنة بـ Event Delegation
 *
 * Fix #7 (tooltips/listeners):
 * قبل: 8 event listeners × N عنصر = آلاف المستمعين
 * بعد: مستمعان فقط (mouseover + mouseout) على document — بغض النظر عن عدد العناصر
 *
 * الطريقة: نخزّن نص الـ tooltip في data-tip و data-tip-pos،
 * ونقرأها عند تحريك الماوس عبر event.target.closest('[data-tip]')
 */

// ── عنصر الـ tooltip الوحيد في الصفحة ──
let _tip = null;
let _showTimer = null;
let _hideTimer = null;
let _delegationReady = false;

function _ensureTipEl() {
  if (!_tip) {
    _tip = document.createElement('div');
    _tip.setAttribute('role', 'tooltip');
    _tip.style.cssText = `
      position:fixed; z-index:99999; pointer-events:none;
      background:#1e293b; color:#f1f5f9; font-size:13px;
      padding:8px 14px; border-radius:8px; font-family:inherit;
      max-width:280px; line-height:1.5; text-align:center;
      box-shadow:0 8px 24px rgba(0,0,0,0.25);
      opacity:0; transition:opacity 0.15s ease;
      border:1px solid rgba(255,255,255,0.08); direction:rtl;
      will-change:opacity;
    `;
    document.body.appendChild(_tip);
  }
  return _tip;
}

function _position(el, pos) {
  const r = el.getBoundingClientRect(), g = 8;
  const map = {
    top:    { left: r.left + r.width / 2,  top: r.top - g,      transform: 'translate(-50%, -100%)' },
    bottom: { left: r.left + r.width / 2,  top: r.bottom + g,   transform: 'translate(-50%, 0)' },
    left:   { left: r.left - g,            top: r.top + r.height / 2, transform: 'translate(-100%, -50%)' },
    right:  { left: r.right + g,           top: r.top + r.height / 2, transform: 'translate(0, -50%)' },
  };
  return map[pos] || map.bottom;
}

function _show(el) {
  clearTimeout(_hideTimer);
  const text = el.dataset.tip;
  if (!text) return;
  _showTimer = setTimeout(() => {
    const tip = _ensureTipEl();
    tip.textContent = text;
    const p = _position(el, el.dataset.tipPos || 'bottom');
    tip.style.left = p.left + 'px';
    tip.style.top  = p.top  + 'px';
    tip.style.transform = p.transform;
    tip.style.opacity = '0';
    requestAnimationFrame(() => { tip.style.opacity = '1'; });
  }, Number(el.dataset.tipDelay) || 400);
}

function _hide() {
  clearTimeout(_showTimer);
  _hideTimer = setTimeout(() => {
    if (_tip) _tip.style.opacity = '0';
  }, 150);
}

// ── تثبيت المستمع المُفوَّض مرة واحدة فقط ──
function _setupDelegation() {
  if (_delegationReady) return;
  _delegationReady = true;

  document.addEventListener('mouseover', e => {
    const el = e.target.closest('[data-tip]');
    if (el) _show(el); else _hide();
  }, { passive: true });

  document.addEventListener('mouseout', e => {
    if (!e.relatedTarget?.closest?.('[data-tip]')) _hide();
  }, { passive: true });

  // دعم لوحة المفاتيح: focus/blur
  document.addEventListener('focusin', e => {
    const el = e.target.closest('[data-tip]');
    if (el) _show(el);
  }, { passive: true });

  document.addEventListener('focusout', e => {
    const el = e.target.closest('[data-tip]');
    if (el) _hide();
  }, { passive: true });
}

// ── الـ directive ──
export default {
  mounted(el, binding) {
    if (!binding.value) return;
    _setupDelegation();

    const text = typeof binding.value === 'string' ? binding.value : (binding.value?.text || '');
    el.dataset.tip = text;
    el.dataset.tipPos = binding.value?.position || 'bottom';
    if (binding.value?.delay) el.dataset.tipDelay = binding.value.delay;
    el.setAttribute('aria-label', text);
  },

  updated(el, binding) {
    if (binding.value === binding.oldValue) return;
    const text = typeof binding.value === 'string' ? binding.value : (binding.value?.text || '');
    el.dataset.tip = text;
    el.setAttribute('aria-label', text);
  },

  unmounted(el) {
    delete el.dataset.tip;
    delete el.dataset.tipPos;
    delete el.dataset.tipDelay;
  },
};
