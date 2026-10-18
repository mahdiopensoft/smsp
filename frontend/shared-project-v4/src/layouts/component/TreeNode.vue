<!-- added by samer -->

<template>
  <VListGroup :value="node.id" v-if="hasChildren === true" no-action class="tree-node">
    <template v-slot:activator="{ props }">
      <VListItem
        v-bind="props"
        :prepend-icon="node.icon ? 'mdi-' + node.icon : 'mdi-apps'"
      >
        <span>
          {{ $i18n.locale == "ar" ? node.name_ar : node.name_en }}
          <!-- <span
            v-for="(part, i) in highlight(
              $i18n.locale == 'ar' ? node.name_ar : node.name_en
            )"
            :key="i"
            :class="{ highlight: part?.toLowerCase() === search?.toLowerCase() }"
            style="letter-spacing: normal !important"
          >
            {{ part }}
          </span> -->
        </span>
      </VListItem>
    </template>
    <div>
      <tree-node
        v-for="(child, index) in node.children || []"
        :key="index"
        :node="child"
        class="child-item"
        :search="search"
      />
    </div>
  </VListGroup>
  <template v-else-if="node.screen_type === 3 && node?.children?.length === 0"></template>
  <template v-else>
    <VListItem
      density="compact"
      :prepend-icon="node.icon ? 'mdi-' + node.icon : 'mdi-apps'"
      color="primary"
      :to="getSafeRoute(node.route)"
    >
      <span>
        {{ $i18n.locale == "ar" ? node.name_ar : node.name_en }}
        <!-- <span
          v-for="(part, i) in highlight(
            $i18n.locale == 'ar' ? node.name_ar : node.name_en
          )"
          :key="i"
          :class="{ highlight: part?.toLowerCase() === search?.toLowerCase() }"
          style="letter-spacing: normal !important"
        >
          {{ part }}
        </span> -->
      </span>
    </VListItem>
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
      default: "children",
    },
    search: {
      type: String,
      default: "",
    },
  },
  methods: {
    getSafeRoute(routeName) {
      try {
        if (this.$router.hasRoute(routeName)) return { name: routeName };
        else return { name: "NotFound" };
      } catch (error) {
        return { name: "NotFound" };
      }
    },

    highlight(text) {
      if (!this.search) return text;
      const regex = new RegExp(`(${this.search})`, "giu");
      return text?.split(regex);
    },
  },
  computed: {
    hasChildren() {
      return this.node[this.children_name] && this.node[this.children_name].length > 0;
    },
  },
};
</script>
<style>
.highlight {
  background: #ffeb3b !important;
  font-weight: bold;
  padding: 0 2px;
  border-radius: 3px;
}
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
