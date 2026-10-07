<template>
  <drawer :data="data" :getData="getData" click="api/academic/class-tracks/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="class-tracks" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddClassTracks',
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
