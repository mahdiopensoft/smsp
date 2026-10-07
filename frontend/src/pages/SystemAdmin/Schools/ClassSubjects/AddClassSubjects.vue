<template>
  <drawer :data="data" :getData="getData" click="api/academic/class-subjects/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="class-subjects" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddClassSubjects',
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
