import { ref, watchEffect, unref } from 'vue';
import QRCode from 'qrcode';

export function useQrSvg(opts) {
  const svg = ref('');
  watchEffect(async () => {
    try {
      const str = await QRCode.toString(unref(opts.value) || ' ', {
        type: 'svg',
        errorCorrectionLevel: opts.ecc ?? 'M',
        color: {
          dark: opts.color ?? '#000',
          light: opts.background ?? '#0000',
        },
        margin: opts.margin ?? 0,
      });
      svg.value = str
        .replace(/<\?xml.*?\?>/, '')
        .replace(/ (width|height)="[^"]*"/g, '');
    } catch (_) {
      svg.value = '';
    }
  });
  return svg;
}
