<template>
  <drawer :data="data" :getData="getData" click="api/academic/educational-levels/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="educational-levels" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddEducationalLevels',
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
