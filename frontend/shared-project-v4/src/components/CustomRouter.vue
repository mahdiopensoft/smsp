<!-- added by samer -->
<template>

  <component :is="component" v-if="$route.name == name_path"  :route="route" :url="url"  :key="name_path"/>
  <router-view  :key="name_path"/>
</template>
<script>
export default {
  props: {
    component: {
      type: [Object, Function],
      required: true,
    },
    name_path: {
      type: [String],
      required: true,
    },
    route:String,
    url:String,
  },
};
</script>
