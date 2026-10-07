<script setup lang="ts">
import { computed } from 'vue';
import type { BarcodeField } from '../types';
import { useBarcodeSvg } from '../../composables/omr/useBarcode';

const props = defineProps<{
  field: BarcodeField;
  color?: string;
}>();

const value = computed(() => props.field.value);
const svg = useBarcodeSvg({
  value,
  format: props.field.format ?? 'CODE128',
  displayValue: props.field.displayValue ?? false,
  color: props.color ?? '#000',
});

const transform = computed(() => {
  const { x, y, width, height } = props.field.rect;
  const rot = props.field.rotate ?? 0;
  if (rot === 90) {
    // rotate around top-left of a box, then translate into place
    return `translate(${x + width} ${y}) rotate(90)`;
  }
  return `translate(${x} ${y})`;
});

const boxW = computed(() =>
  (props.field.rotate ?? 0) === 90 ? props.field.rect.height : props.field.rect.width,
);
const boxH = computed(() =>
  (props.field.rotate ?? 0) === 90 ? props.field.rect.width : props.field.rect.height,
);
</script>

<template>
  <g :transform="transform">
    <foreignObject :width="boxW" :height="boxH" x="0" y="0">
      <div
        xmlns="http://www.w3.org/1999/xhtml"
        style="width:100%;height:100%;display:flex;align-items:stretch;justify-content:stretch;"
        v-html="svgWrapper(svg, boxW, boxH)"
      />
    </foreignObject>
  </g>
</template>

<script lang="ts">
// helper kept outside setup so it's callable from the template scope
function svgWrapper(svg: string, w: number, h: number) {
  if (!svg) return '';
  // Ensure the injected barcode fills the box; jsbarcode emits its own viewBox.
  return svg.replace(
    /<svg([^>]*)>/,
    `<svg$1 preserveAspectRatio="none" style="width:${w}mm;height:${h}mm;display:block;">`,
  );
}
export default { name: 'OmrBarcode' };
</script>
