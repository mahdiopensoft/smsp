<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/special-tracks/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-special-tracks" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteSpecialTracks',
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
