<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/lessons/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-lessons" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteLessons',
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
