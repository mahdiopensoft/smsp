<template>
  <drawer :data="data" :getData="getData" click="api/academic/school-sections/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="school-sections" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddSchoolSections',
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
