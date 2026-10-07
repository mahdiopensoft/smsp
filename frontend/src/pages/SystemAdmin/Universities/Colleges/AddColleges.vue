<template>
  <drawer :data="data" :getData="getData" click="api/academic/colleges/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="colleges" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddColleges',
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
