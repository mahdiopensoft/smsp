<template>
  <drawer :data="data" :getData="getData" click="api/academic/semester-subjects/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="semester-subjects" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddSemesterSubjects',
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
