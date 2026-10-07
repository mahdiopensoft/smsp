<template>
  <drawer :data="data" :getData="getData" click="api/academic/lessons/" :items="items">
    <template v-slot>
      <v-row>
        <fields
          :data="data"
          url="lessons"
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
  name: 'AddLessons',
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
