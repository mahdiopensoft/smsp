<template>
  <!-- added by samer -->
  <!-- فلترة ب الفرع -->

  <!-- <pre dir="ltr">{{ data }}</pre> -->
  <template v-if="!show_in_edit && data.id"> </template>
  <template v-else>
    <VCheckbox
      v-model="active_level"
      :label="$t('add_other_level')"
      class="ma-0 pa-0"
      hide-details
      @update:model-value="resetData"
    />
    <div v-show="active_level">
      <auto-list v-model="fk_organization__company_level" name="CompanyLevelChoices" />

      <auto-list
        v-model="data.fk_branch"
        name="add_to_level"
        :param="fk_organization__company_level"
      />
      <!-- :rules="[$required]" -->
    </div>
  </template>
</template>

<script>
export default {
  props: {
    data: { type: Object, required: true },
    modelValue: {
      type: [Number, String],
      default: null,
    },

    show_in_edit: { type: Boolean, default: true },
  },
  data() {
    return {
      active_level: false,
      fk_organization__company_level: null,
    };
  },

  mounted() {
    // this.data.fk_branch = null;
  },
  methods: {
    resetData() {
      // this.fk_organization__company_level = null;
      this.data.fk_branch = null;
    },
  },
};
</script>
