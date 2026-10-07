<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/subjects/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-subjects" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteSubjects',
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
