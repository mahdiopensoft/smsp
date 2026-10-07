<template>
  <drawer :data="data" :getData="getData" click="api/academic/levels/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="levels" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddLevels',
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
