import { computed, unref } from 'vue';
import JsBarcode from 'jsbarcode';

export function useBarcodeSvg(opts) {
  return computed(() => {
    const svgNs = 'http://www.w3.org/2000/svg';
    const svg = typeof document !== 'undefined'
      ? document.createElementNS(svgNs, 'svg')
      : null;
    if (!svg) return '';
    try {
      JsBarcode(svg, unref(opts.value) || ' ', {
        format: opts.format ?? 'CODE128',
        displayValue: opts.displayValue ?? false,
        lineColor: opts.color ?? '#000',
        background: opts.background ?? 'transparent',
        height: opts.height ?? 40,
        fontSize: opts.fontSize ?? 12,
        margin: opts.margin ?? 0,
      });
    } catch (_) {
      return '';
    }
    return svg.outerHTML;
  });
}
