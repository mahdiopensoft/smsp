<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/levels/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-levels" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteLevels',
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
