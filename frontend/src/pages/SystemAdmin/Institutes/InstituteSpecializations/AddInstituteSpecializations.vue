<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/specializations/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-specializations" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteSpecializations',
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
