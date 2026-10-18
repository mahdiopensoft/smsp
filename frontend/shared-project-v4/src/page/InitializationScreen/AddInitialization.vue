<template>
  <!-- added by samer -->

  <drawer :data="data" :click="url" :getData="getData" :items="items">
    <template v-slot>
      <fields :data="data" :url="route" :import-excel="true" />
    </template>
  </drawer>
</template>
<script>
import Drawer from "../../../components/Navigation/Drawer.vue";
export default {
  created() {
    try {
      this.url = this.$route.meta?.url;
    } catch (e) {
      console.log("Error in fetching route or URL", e);
    }
  },
  components: { Drawer },

  props: {
    data: Object,
    route: String,
    getData: Function,
    items: Array,
  },
  data() {
    return {
      url: "",
    };
  },
  methods: {
    flattenTree(nodes) {
      let result = {};
      for (const node of nodes) {
        const { children, ...rest } = node;

        result[rest.name] = rest;

        if (children) {
          Object.assign(result, this.flattenTree(children));
        }
      }
      return result;
    },
  },
};
</script>
