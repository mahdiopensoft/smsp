<template>
  <drawer :data="data" :getData="getData" click="api/academic/specializations/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="specializations" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddSpecializations',
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
