<template>
  <drawer :data="data" :getData="getData" click="api/academic/exam-periods/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="exam-periods" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddExamPeriods',
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
