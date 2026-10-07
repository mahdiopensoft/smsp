<template>
  <drawer :data="data" :getData="getData" click="api/academic/learning-outcomes/" :items="items">
    <template v-slot>
      <v-row>
        <fields
          :data="data"
          url="learning-outcomes"
          :attr="{
            unit: {
              param: data.subject,
            },
          }"
        />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddLearningOutcomes',
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
