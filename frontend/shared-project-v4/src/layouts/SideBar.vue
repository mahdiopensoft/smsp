<template>
  <!-- added by samer -->

  <v-card class="h-100" elevation="0" color="transparent">
    <!-- Search Section -->
    <div class="sidebar-search-container">
      <div class="sidebar-search-wrapper">
        <v-icon size="18" class="search-icon">mdi-magnify</v-icon>
        <input 
          v-model="search" 
          type="text" 
          :placeholder="$i18n.locale == 'ar' ? 'بحث سريع...' : 'Quick search...'"
          class="sidebar-search-input"
        >

      </div>
    </div>

    <!-- Loading Skeleton -->
    <template v-if="loading">
      <div class="sidebar-skeleton">
        <v-skeleton-loader v-for="item in 7" :key="item" type="heading" />
      </div>
    </template>

    <!-- Navigation Tree (Search Mode) -->
    <v-list
      v-else-if="search"
      v-model:opened="open"
      density="compact"
      :slim="true"
      nav
      aria-label="قائمة التنقل الرئيسية"
      role="navigation"
      class="sidebar-nav sidebar-tree-sneat"
    >
      <template v-for="item in filterItems" :key="item.id">
        <tree-node :node="item" />
      </template>

      <!-- Empty Search State -->
      <div v-if="filterItems.length === 0" class="sidebar-empty-state">
        <v-icon size="28" class="mb-2" style="opacity: 0.25">mdi-magnify-close</v-icon>
        <span class="text-caption" style="opacity: 0.4">لا توجد نتائج</span>
      </div>
    </v-list>

    <!-- Navigation Tree (Default) -->
    <v-list
      v-else
      v-model:opened="open"
      density="compact"
      :slim="true"
      nav
      aria-label="قائمة التنقل الرئيسية"
      role="navigation"
      class="sidebar-nav sidebar-tree-sneat"
    >
      <template v-for="item in filterItems" :key="item.id">
        <tree-node :node="item" />
      </template>
    </v-list>
  </v-card>
</template>
<script>
import TreeNode from "./component/TreeNode.vue";

export default {
  name: "SideBar",
  components: { TreeNode },
  props: {
    items: {
      type: Array,
    },
    loading: false,
  },
  data() {
    return {
      itemss: [],
      search: undefined,
      open: [],
      selectedList: [],
    };
  },

  methods: {
    filtereItems(item, search) {
      
      if (item.name_ar.includes(search)) return true;
      if (item.children && item.children.length)
        return item.children.some((child) => this.filtereItems(child, search));
      return false;
    },
  },
  computed: {
    filterItems() {
      if (this.search) {
        const filterNode = (node) =>  {
          const nameMatch = node.name_ar.includes(this.search)
          if(node.children_for_sidebar){
            const filterChildren = node.children_for_sidebar.map(filterNode).filter(Boolean)
            if(filterChildren.length >0 || nameMatch){
              return {...node,children_for_sidebar:filterChildren};
            }
          }
          return nameMatch ?{...node}:null
        }
        return this.items.map(group=>{
          const result =  filterNode(group)
          return result
        }).filter(Boolean)


      } else {
        return this.items;
      }
    },
  },
};
</script>
<style>
/* Clean Hierarchy */
.sidebar-tree-sneat .v-list-group {
  position: relative;
}
.sidebar-tree-sneat .tree-child {
  position: relative;
  padding-inline-start: var(--space-xl);
}

/* Empty search state */
.sidebar-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  color: rgba(var(--v-theme-on-surface), 0.4);
}
</style>
