<template>
  <drawer
    :data="data"
    click="/user-manager/users/"
    :getData="getData"
    :files="['image_user']"
    :items="items"
  >
    <template v-slot>
      <add-to-level v-if="!data.id" :data="data" />
      <fields
        :data="data"
        url="users"
        :attr="{
          first_name: { rules: [$required] },
          last_name: { rules: [$required] },
          email: { rules: [$email, $max_length(255)] },
          fk_organization: {
            param: this.data.fk_organization__company_level,
            depend: data.active_level && !data.id,
          },
          fk_organization__company_level: {
            depend: data.active_level && !data.id,
          },
          groups: {
            rules: [$required],
          },
          image_user: {
            max_length: 10000,
          },
        }"
        ><template v-slot="{ field }">
          <VSheet v-if="field.name === 'password'">
            <custom-text-field
              v-if="!data.id"
              type="password"
              :rules="[$required, $valid_pass]"
              v-model="data.password"
              label=" كلمة المرور"
              autocomplete="new password"
            ></custom-text-field>
          </VSheet> </template
      ></fields>
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
    items: [Array, Object],
  },
};
</script>
