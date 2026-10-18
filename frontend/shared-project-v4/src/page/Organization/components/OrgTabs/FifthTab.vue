<template>
  <CustomDataTableAddWithField :headers="headersContact" :items="data.contact_set">
    <template v-slot:fields="{ item }">
      <auto-list
        name="ContactTypeChoices"
        v-model="item.type"
        :rules="[$required]"
        cols="3"
      />

      <custom-text-field
        v-model="item.branch_contact"
        :rules="[
          $required,
          () => {
            if (item.type === 1 || item.type === 3 || item.type === 4)
              return [$min_length(6), $max_length(14)];
            else if (item.type === 2) return [$email];
            else return [$max_length(200)];
          },
        ]"
        cols="3"
        :type="item.type == 1 || item.type == 3 || item.type == 4 ? 'number' : 'text'"
      />
    </template>
  </CustomDataTableAddWithField>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const data = defineModel();
const headersContact = computed(() => {
  return [
    {
      title: t("type_communication_method"),
      key: "type",
      nameList: "ContactTypeChoices",
    },

    {
      title: t("communication_method"),
      key: "branch_contact",
    },
  ];
});
</script>
