<template>
  <drawer :data="data" :getData="getData" click="api/academic/tracks/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="tracks" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddTracks',
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
