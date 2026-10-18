<template>
  <!-- added by samer -->
  <!-- فلترة ب المنظمات -->

  <template v-if="!show_in_edit && data.id"> </template>
  <template v-else>
    
    <auto-list    
      v-model="data.fk_organization__company_level"
      name="CompanyLevelChoices"
    />
    <auto-list    
      v-model="data.fk_branch"
      name="add_to_level"
      :rules="[$required]"
      :param="data.fk_organization__company_level"
    />
  </template>
</template>

<script>
export default {
  props: {
    data: { type: Object, required: true },
    show_in_edit: { type: Boolean, default: true }
  
  },
};
</script>
