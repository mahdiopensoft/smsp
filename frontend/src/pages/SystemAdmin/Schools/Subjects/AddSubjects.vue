<template>
  <drawer :data="data" :getData="getData" click="api/academic/subjects/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="subjects" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddSubjects',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  data() {
    return {};
  },
  created() { },
  methods: {},
};
</script>
