<template>
  <drawer :data="data" :getData="getData" click="api/academic/grading-systems/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="grading-systems" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddGradingSystems',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  data() {
    return {};
  },
};
</script>
