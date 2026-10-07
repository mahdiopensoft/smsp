<template>
  <fieldset
    v-bind="$attrs"
    class="border pa-2 mb-4 rounded-lg w-100"
    :class="{
      'disabled-row': $attrs?.disabled,
      'd-flex justify-center': $attrs?.placeholder,
    }"
    :style="{ height: $attrs?.placeholder ? '50vh' : '' }"
  >
    <legend class="px-2 ms-1" :class="$attrs?.label_class">
      <slot name="legend">
        <v-icon v-if="prependIcon" class="me-1">{{ prependIcon }}</v-icon>
        {{ label || $t("show_fields") }}
        <v-icon v-if="appendIcon" class="ms-1">{{ appendIcon }}</v-icon>
      </slot>
    </legend>
    <slot v-if="$attrs?.placeholder" name="placeholder">
      <div v-if="$attrs?.loading" class="d-flex justify-center align-center">
        <div class="text-center mb-5 mt-3">
          <v-progress-circular indeterminate="" color="primary" size="55">
          </v-progress-circular>
          <p class="mt-4 text-medium-emphasis">{{ $t("fetching_data") }}</p>
        </div>
      </div>
      <div
        v-else
        class="d-flex justify-center align-center"
        style="height: 100%"
      >
        <div class="text-center mb-5 mt-3">
          <v-icon size="55" color="grey-lighten-1">{{
            PHIcon ? PHIcon : "mdi-filter-variant"
          }}</v-icon>
          <p class="text-grey-lighten-1 mt-2">
            {{ PHText ? PHText : $t("please_fill_the_filter_fields") }}
          </p>
        </div>
      </div>
    </slot>
    <slot v-else>
      <v-row class="align-center">
        <slot name="fields"> </slot>
      </v-row>
    </slot>
  </fieldset>
</template>
<script>
export default {
  props: {
    label: { type: String, default: false },
    table: { type: Boolean, default: false },
    form_ref: String,

    prependIcon: String,
    appendIcon: String,

    PHIcon: String,
    PHText: String,
  },
  data() {
    return {};
  },
  async created() {},
  computed: {},
  methods: {},
};
</script>
