<template>
  <v-row class="pa-2">
    <Fields
      :data="data"
      :fields="fields"
      :attr="{
        default_password_for_students: {
          depend: companyUniOrColl,
          rules: [$valid_pass],
        },
        default_user_name_for_employees: {
          null: false,
        },
        default_password_for_employees: {
          null: false,
          rules: [$valid_pass],
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
