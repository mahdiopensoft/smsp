<template>
  <drawer :data="data" :getData="getData" click="api/academic/study-systems/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="study-systems" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddStudySystems',
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
