<script setup lang="ts">
import { computed } from 'vue';
import type { QrField } from '../types';
import { useQrSvg } from '../../composables/omr/useQrCode';

const props = defineProps<{ field: QrField; color?: string }>();

const value = computed(() => props.field.value);
const svg = useQrSvg({
  value,
  ecc: props.field.ecc ?? 'M',
  color: props.color ?? '#000',
});

const transform = computed(
  () => `translate(${props.field.rect.x} ${props.field.rect.y})`,
);

function wrap(inner: string, w: number, h: number) {
  if (!inner) return '';
  return inner.replace(
    /<svg([^>]*)>/,
    `<svg$1 preserveAspectRatio="xMidYMid meet" style="width:${w}mm;height:${h}mm;display:block;">`,
  );
}
</script>

<template>
  <g :transform="transform">
    <foreignObject :width="field.rect.width" :height="field.rect.height" x="0" y="0">
      <div
        xmlns="http://www.w3.org/1999/xhtml"
        style="width:100%;height:100%;"
        v-html="wrap(svg, field.rect.width, field.rect.height)"
      />
    </foreignObject>
  </g>
</template>

<script lang="ts">
export default { name: 'OmrQrCode' };
</script>
