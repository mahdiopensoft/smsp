<template>
  <drawer :data="data" :getData="getData" click="api/academic/institute-exam-periods/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-exam-periods" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteExamPeriods',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  data() {
    return {};
  },
  created() {},
  methods: {},
};
</script>
