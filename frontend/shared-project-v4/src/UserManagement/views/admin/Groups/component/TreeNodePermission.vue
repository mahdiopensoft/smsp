<template>
  <!-- <pre dir="ltr">{{ parent }}</pre> -->
 
  <VHover>
    <template v-slot:default="{ isHovering, props }" >
      <tr
        v-bind="props"
        :style="{
          transition: 'background-color 0.2s',
        }"
        :class="[{
          'selected-row': isHovering,
        } ,'children-per']"

      >
        <td style="border-bottom: unset" >
          <VListItem

            @click="toggle"
            :title="node.name_ar"
            density="compact"
            color="primary"
            dense
            :style="`width: 329px; padding-right: ${level * 30}px !important;`"
            class="node-per"
            
          >
            <template #append>
              <VSpacer />
              <VIcon>
                {{
                  hasChildren
                    ? isOpen
                      ? "mdi-chevron-up"
                      : "mdi-chevron-down"
                    : ""
                }}
              </VIcon>
            </template>
          </VListItem>
        </td>
        <td>
          <VCheckbox-btn
            v-model="node.status"
            @change="toogleParent(node)"
            style="width: 100px !important"
            :disabled="parent &&  !parent.status"
          />
        </td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
        <td><VCheckbox hide-details style="width: 100px !important" /></td>
      </tr>
    </template>
  </VHover>
 


   <template  v-if="isOpen">
    <tree-node-permission     
        v-for="child in node.children" 
        :key="child.id" 
        :node="child"
        :parent="node"
        :level="level + 1"          
        />
        </template>
      
        
    
 
     
 <!-- <VDivider /> -->
</template>
<script>
export default {
  props: {
    node: Object,
    parent: Object,
    level: Number,
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    hasChildren() {
      return this.node.children && this.node.children.length > 0;
    },
  },
  methods: {
    toogleParent(data) {        
      if (data.children && data.children.length > 0)
        data.children.map((e) => {
          if (!data.status) e.status = false;
          if(data.children.length>0) this.toogleParent(e)
        });
    },
    toggle() {
      if (this.hasChildren) this.isOpen = !this.isOpen;
    },
  },
};
</script>
<style scoped>
.toggle-icon {
  cursor: pointer;
  display: inline-block;
  width: 20px;
  text-align: center;
}
.tree-node{
    position: relative;
    padding-right: 20px;
    
}
.tree-node::before{
    content: "";
    position: absolute;
    top:20px;
    right: 0;
    width: 20px;
    height: 2px;
    background: #000;
}
.node-per{     
    padding: 5px 10px;
    position: relative;
    z-index: 1;
}
.children-per{
    margin-top: 10px;
    border-right: 2px solid #000;
    padding-right: 10px;
}
</style>