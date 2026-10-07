<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/semesters/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-semesters" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteSemesters',
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
