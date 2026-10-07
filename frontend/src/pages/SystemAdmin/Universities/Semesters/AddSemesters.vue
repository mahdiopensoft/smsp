<template>
  <drawer :data="data" :getData="getData" click="api/academic/semesters/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="semesters" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddSemesters',
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
