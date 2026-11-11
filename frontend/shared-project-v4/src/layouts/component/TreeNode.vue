<!-- added by samer -->

<template>
  <!-- Expandable Group Node -->
  <VListGroup v-if="hasChildren === true" no-action class="tree-node">
    <template v-slot:activator="{ props }">
      <VListItem
        v-bind="props"
        :title="$i18n.locale == 'ar' ? node.name_ar : node.name_en"
        :prepend-icon="node.icon ? 'mdi-' + node.icon : 'mdi-apps'"
      />
    </template>
    <div>
      <tree-node
        v-for="(child, index) in node.children_for_sidebar"
        :key="index"
        :node="child"
        class="child-item"
      />
    </div>
  </VListGroup>

  <!-- Empty Group — hidden -->
  <template
    v-else-if="node.screen_type === 3 && node.children_for_sidebar.length === 0"
  ></template>

  <!-- Leaf Node (Single Link) -->
  <template v-else>
    <VListItem
      :title="$i18n.locale == 'ar' ? node.name_ar : node.name_en"
      density="compact"
      :prepend-icon="node.icon ? 'mdi-' + node.icon : 'mdi-apps'"
      color="primary"
      :to="getSafeRoute(node.route)"
    />
      
      
  </template>
</template>
<script>
export default {
  props: {
    node: {
      type: Object,
      required: true,
    },
    children_name: {
      type: String,
      default: "children_for_sidebar",
    },
  },
  methods: {
    getSafeRoute(routeName){
      if(routeName && this.$router.hasRoute(routeName)) return {name:routeName}
      else return ""
    },
    navigatTo(node){
      console.log(node);
    }
  },
  computed: {
    hasChildren() {
      return (
        this.node[this.children_name] &&
        this.node[this.children_name].length > 0
      );
      if (this.node)
        if ("children_for_sidebar" in this.node)
          return this.node.children_for_sidebar.length > 0;
        else return false;
    },
  },
};
</script>
<style>
/* TreeNode — Ultra-Clean Hierarchy */
.tree-node {
  position: relative;
}

/* No messy lines, just clean spatial hierarchy with hover hints */
.child-item {
  font-size: var(--font-size-sm);
  border-inline-start: 2px solid transparent !important;
  padding-inline-start: var(--space-sm);
  margin-inline-start: var(--space-xs);
  transition: border-color 0.2s ease, background 0.2s ease !important;
}

.child-item:hover {
  border-inline-start-color: rgba(var(--v-border-color), 0.15) !important;
}

.child-item.v-list-item--active {
  border-inline-start-color: rgb(var(--v-theme-primary)) !important;
}
</style>
