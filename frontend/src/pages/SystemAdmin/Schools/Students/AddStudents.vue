<template>
  <drawer :data="data" :getData="getData" click="api/academic/students/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="students" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddStudents',
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
