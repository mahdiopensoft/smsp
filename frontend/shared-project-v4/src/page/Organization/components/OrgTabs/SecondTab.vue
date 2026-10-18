<template>
  <v-row>
    <Fields
      :data="data"
      :fields="fields"
      :attr="{
        fk_address__fk_region__fk_directorate__fk_governorate__fk_country: {
          null: false,
        },
        fk_address__fk_region__fk_directorate__fk_governorate: {
          param:
            data.fk_address__fk_region__fk_directorate__fk_governorate__fk_country,
          null: false,
        },
        fk_address__fk_region__fk_directorate: {
          param: data.fk_address__fk_region__fk_directorate__fk_governorate,
          null: false,
        },
        fk_address__fk_region: {
          param: data.fk_address__fk_region__fk_directorate,
          null: false,
        },
        fk_address__street: {
          null: false,
        },
        
      }"
    />
  </v-row>
</template>

<script setup>
const props = defineProps({
  fields: {
    type: Array,
    default: [],
  },
 
});
const data = defineModel();
</script>
