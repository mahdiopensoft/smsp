<template>
  <drawer :data="data" :getData="getData" click="api/academic/educational-stages/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="educational-stages" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddEducationalStages',
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
