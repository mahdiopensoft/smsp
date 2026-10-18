<template>
 
  <drawer
    :data="data"
    click="/user-manager/user-type/"
    :getData="getData"
    :items="items"
    :re_open="false"
  >
    <template v-slot="{ value }">
 
      <fields
        :data="data"
        url="user-type"
        :attr="{
          fk_parent_user_type: { refresh: value ,depend:!data.id,null:is_super_user},
          name_ar:{disabled:disabledField},
          name_en:{disabled: disabledField},
          description:{disabled:disabledField},
          is_active:{disabled:disabledField},
          
        }"
      />
      <auto-list v-model="data.screens" name="parent_screen" multiple />
    </template>
  </drawer>
</template>
<script>
import { state } from '@/store/state';
import { useAuthStore } from "../../../stores/auth";

export default {
  
  props: {
    data: Object,
    items: [Array, Object],
  },
  
  data() {
    return {
      is_super_user:state.is_super_user,
      authStore: useAuthStore(),
    }
  },
  computed:{
     disabledField(){
      return this.data.id &&  this.isPlatFormSys
     },
      isPlatFormSys() {
      return state?.isPlatFormSys || true;
    },
     
  }


};
</script>
