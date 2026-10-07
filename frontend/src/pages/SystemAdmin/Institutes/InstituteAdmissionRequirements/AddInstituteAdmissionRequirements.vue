<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/admission-requirements/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-admission-requirements" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteAdmissionRequirements',
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
