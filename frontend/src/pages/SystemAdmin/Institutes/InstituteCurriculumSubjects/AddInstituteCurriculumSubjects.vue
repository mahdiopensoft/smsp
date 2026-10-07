<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/curriculum-subjects/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-curriculum-subjects" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteCurriculumSubjects',
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
