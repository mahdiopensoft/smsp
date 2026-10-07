<template>
  <drawer :data="data" :getData="getData" click="api/academic/university-courses/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="university-courses" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddUniversityCourses',
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
