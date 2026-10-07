<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/curricula/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-curricula" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteCurricula',
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
