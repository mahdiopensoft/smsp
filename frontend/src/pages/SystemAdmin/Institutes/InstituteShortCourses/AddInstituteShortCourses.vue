<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/short-courses/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-short-courses" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteShortCourses',
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
