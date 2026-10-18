<template>
  <!-- added by samer -->

  <v-card elevation="0" color="transparent">
    <!-- Search Section -->

    <!-- Search -->
    <v-col :cols="12" class="pa-0 py-2 px-2">
      <v-text-field
        v-model="search"
        prepend-inner-icon="mdi-magnify"
        :placeholder="$i18n.locale === 'ar' ? 'ابحث...' : 'Search...'"
        density="compact"
        variant="solo-filled"
        flat
        hide-details
        clearable
        class="modern-search-field"
        type="search"
      >
        <!-- <template #append>
          <v-menu location="end" lazy :close-on-content-click="false">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-filter"
                color="info"
                width="26"
                height="26"
                variant="text"
              />
            </template>
            <v-card>
            
              <v-list density="compact">
                <v-list-item class="premium-list-item" active-color="primary">
                  <template v-slot:prepend>
                    <v-checkbox-btn color="primary" density="compact"></v-checkbox-btn>
                  </template>
                  <v-list-item-title class="text-body-2 font-weight-medium">
                    الكل
                  </v-list-item-title>
                </v-list-item>
                <v-divider />
                <v-list-item
                  v-for="(sys, index) in state?.systems"
                  :key="sys.key"
                  class="premium-list-item"
                  active-color="primary"
                >
                  <template v-slot:prepend>
                    <v-checkbox-btn
                      v-model="selected_system"
                      color="primary"
                      density="compact"
                      :value="sys.id"
                    ></v-checkbox-btn>
                  </template>
                  <v-list-item-title class="text-body-2 font-weight-medium">
                    {{ sys.name_ar }}</v-list-item-title
                  >
                </v-list-item>
              </v-list>
            </v-card>
          </v-menu>
        </template> -->
      </v-text-field>
    </v-col>

    <v-divider />

    <!-- <input
          v-model="search"
          type="text"
          :placeholder="$i18n.locale == 'ar' ? 'بحث سريع...' : 'Quick search...'"
          class="sidebar-search-input"
        /> -->

    <!-- Loading Skeleton -->

    <template v-if="loading">
      <div class="sidebar-skeleton">
        <v-skeleton-loader v-for="item in 7" :key="item" type="heading" />
      </div>
    </template>

    <!-- Navigation Tree (Search Mode) -->

    <v-list
      v-model:opened="open"
      v-else-if="search"
      density="compact"
      :slim="true"
      class="sidebar-nav sidebar-tree-sneat"
    >
      <template v-for="item in filterdItems" :key="item.id">
        <tree-node :node="item" :search="search" />
      </template>

      <!-- Empty Search State -->
      <div v-if="filterdItems.length === 0" class="sidebar-empty-state">
        <v-icon size="28" class="mb-2 text-warning">mdi-magnify-close</v-icon>
        <span> لا توجد نتائج مطابقة لـ </span>
        <span>" {{ search }}"</span>
      </div>
    </v-list>

    <!-- Navigation Tree (Default) -->
    <v-list v-else density="compact" :slim="true" class="sidebar-nav sidebar-tree-sneat">
      <template v-for="item in filterdItems" :key="item.id">
        <tree-node :node="item" :search="search" />
      </template>
    </v-list>
  </v-card>
</template>
<script setup>
import { ref, onMounted, computed, watch } from "vue";
import TreeNode from "./component/TreeNode.vue";
import { primaryStore } from "../../store/state";
import { state } from "@/store/state";

const props = defineProps({
  loading: Boolean,
});

const items = primaryStore.addedRoutes.filter((f) => f.screen_type !== 2);
let itemsTree = ref([]);
let selected_system = ref([]);
const search = ref("");
const searchInput = ref("");
const open = ref([]);
const searchInAllSys = ref(false);

function updateSearch() {
  if (!searchInput.value) search.value = "";
}
function buildItems(system) {
  if (Array.isArray(system)) {
    const filterItems = [...items.filter((f) => system.includes(f.fk_default_system))];
    return filterItems;
  } else {
    if (!system) return [];
    const filterItems = [...items.filter((f) => f.fk_default_system === system)];
    itemsTree.value = buildTree(filterItems);
  }
}
function buildTree(items) {
  const map = {};
  const tree = [];
  items.forEach((item) => {
    map[item.id] = { ...item, children: [] };
  });
  items.forEach((item) => {
    const node = map[item.id];
    const parendId = item.fk_parent_screen;
    if (parendId && map[parendId]) map[parendId].children.push(node);
    else tree.push(node);
  });

  return tree;
}
function onEnter() {
  search.value = searchInput.value;
}
function filterTree(nodes, keyword) {
  if (!keyword) return nodes;

  const k = keyword.toLowerCase();
  const result = [];
  for (const node of nodes) {
    const name = node.name?.toLowerCase();
    const isMatch = name?.includes(k);

    if (isMatch) {
      result.push({
        ...node,
        children: node.children || [],
      });
      continue;
    }

    let filteredChildren = [];

    if (node.children?.length) {
      filteredChildren = filterTree(node?.children, keyword);
    }

    if (filteredChildren.length) {
      result.push({ ...node, children: filteredChildren });
    }
  }

  return result;
}

const currentSystem = computed(() => {
  return state.current_system;
});
const filterdItems = computed(() => {
  let list = [];
  // if (search.value) {
  //   if (state.current_system) {
  //     const l = buildItems(state.current_system);
  //     console.log(l);
  //   }
  //   list = [];
  //   // list = filterTree(buildItems(state.current_system), search.value);
  //   // list = filterTree(buildItems(selected_system.value), search.value);

  //   open.value = [];
  //   list.forEach((e) => {
  //     if (e?.children?.length) {
  //       open.value.push(e.id);
  //     }
  //   });
  // } else {
  //   }

  list = filterTree(itemsTree.value, search.value);
  if (search.value) {
    open.value = [];
    list.forEach((e) => {
      if (e?.children?.length) {
        open.value.push(e.id);
      }
    });
  }

  return list;
});

watch(currentSystem, (val) => {
  buildItems(val);
});

onMounted(() => {
  if (state.current_system) {
    buildItems(state.current_system);
  }
});
</script>
<style scope>
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
}
</style>
