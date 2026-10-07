<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/education-systems/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-education-systems" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteEducationSystems',
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
