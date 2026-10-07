<script setup lang="ts">
import { computed } from 'vue';
import type { OmrSheetConfig } from '../types';

const props = defineProps<{ config: OmrSheetConfig }>();

const corners = computed(() => {
  const { paper, safeMargin } = props.config;
  const s = 3.5; // mm — fiducial size
  const inset = Math.max(2, safeMargin - s - 1);
  return [
    { x: inset, y: inset },
    { x: paper.width - inset - s, y: inset },
    { x: inset, y: paper.height - inset - s },
    { x: paper.width - inset - s, y: paper.height - inset - s },
  ].map((p) => ({ ...p, s }));
});

const timing = computed(() => {
  const t = props.config.timingMarks;
  if (!t) return [];
  const { paper } = props.config;
  const marks: Array<{ x: number; y: number; w: number; h: number }> = [];
  const usableH = paper.height - t.topOffset - t.bottomOffset;
  const step = usableH / (t.count - 1);
  for (const edge of t.edges) {
    for (let i = 0; i < t.count; i++) {
      const y = t.topOffset + i * step - t.markHeight / 2;
      const x = edge === 'left' ? t.inset : paper.width - t.inset - t.markWidth;
      marks.push({ x, y, w: t.markWidth, h: t.markHeight });
    }
  }
  return marks;
});
</script>

<template>
  <g>
    <!-- corner fiducials -->
    <template v-if="config.cornerFiducials !== false">
      <rect
        v-for="(c, i) in corners"
        :key="`f-${i}`"
        :x="c.x"
        :y="c.y"
        :width="c.s"
        :height="c.s"
        fill="#000"
      />
    </template>

    <!-- timing marks -->
    <rect
      v-for="(m, i) in timing"
      :key="`t-${i}`"
      :x="m.x"
      :y="m.y"
      :width="m.w"
      :height="m.h"
      fill="#000"
    />
  </g>
</template>

<script lang="ts">
export default { name: 'OmrAlignmentMarks' };
</script>
