<template>
  <!-- <pre dir="ltr">
 {{attr}}
 </pre> -->

  <component
    ref="componentInput"
    v-model="value"
    v-if="shouldRenderField"
    :is="resolveComponent"
    v-bind="generateFieldProps"
    :print="print"
    class="field-input-ltr"
    @update:modelValue="onUpdate"
  />
</template>

<script>
import CustomCheckBox from "./CustomCheckBox.vue";
import { VChip } from "vuetify/components";

export default {
  components: { CustomCheckBox, VChip },
  props: {
    field: { type: Object, required: {} },
    attr: { type: Object, default: () => ({}) },
    modelValue: {
      type: [Number, String],
      default: null,
    },
  },
  mounted() {
    // console.count(`Field mounted : ${this.field.name}`);
    this.initializeDefaultValue();
  },

  methods: {
    onUpdate(value) {
      // console.log("field");
      this.$emit("update", value);
    },
    feature(attr) {
      return this.attr[attr];
    },
    initializeDefaultValue() {
      if (this.modelValue !== null && this.modelValue !== undefined) return;
      let defaultValue = null;
      if (this.field.type === "BooleanField") {
        defaultValue = this.attr.default ?? this.field.default;
      } else if (this.field.name_list) {
        defaultValue =
          this.attr["default"] === null
            ? null
            : this.attr["default"] ??
              this.field.default ??
              this.field.default_val ??
              null;
      } else if (
        this.field.default !== "<class 'django.db.models.fields.NOT_PROVIDED'>"
      ) {
        defaultValue = this.attr.default ?? this.field.default ?? null;
      }
      if (defaultValue !== null && defaultValue !== undefined) {
        this.$emit("update:modelValue", defaultValue);
      }
    },
  },
  computed: {
    value: {
      get() {
        if (this.modelValue == null) {
          if (this.field.type === "BooleanField") {
            this.value = this.attr["default"] ?? this.field.default;
          } else if (this.field.name_list) {
            this.value =
              this.attr["default"] === null
                ? null
                : this.attr["default"] ??
                  this.field.default ??
                  this.field.default_val ??
                  null;
          } else if (this.field.name_list == null) {
            this.value =
              this.field.default != "<class 'django.db.models.fields.NOT_PROVIDED'>"
                ? this.attr["default"] || this.field.default || null
                : null;
            this.attr["default"] = null;
            this.field.default = null;
          }
        }

        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    shouldRenderField() {
      if ("depend" in this.attr) return this.attr.depend;
      if ("depend" in this.field) return this.field.depend;

      return true;
    },
    resolveComponent() {
      const type = this.attr.type || this.field.type;

      const is_list = this.field.name_list || this.field.items;
      return (
        {
          JSONField: "custom-text-note",
          CharField: is_list ? "auto-list" : "custom-text-field",
          IntegerField: is_list ? "auto-list" : "custom-text-field",
          DecimalField: "custom-text-field",
          PositiveSmallIntegerField: is_list ? "auto-list" : "custom-text-field",
          PositiveBigIntegerField: "custom-text-field",
          number: "custom-text-field",
          PositiveIntegerField: "custom-text-field",
          FloatField: "custom-text-field",
          TextField: "custom-text-note",
          ForeignKey: "auto-list",
          OneToOneField: "auto-list",
          BooleanField: "custom-check-box",
          TimeField: "custom-text-field",
          DateField: "custom-date",
          DateTimeField: "custom-text-field",
          ImageField: "custom-img",
          FileField: "custom-file",
          ManyToManyField: "auto-list",
          colorPicker: "color-picker",
          chip: "v-chip",
        }[type] ?? "custom-text-field"
      );
    },
    generateFieldProps() {
      const isArabic = this.$i18n.locale === "ar";
      let field_filter = { ...this.field, ...this.attr };

      field_filter.label =
        this.attr?.label || (isArabic ? field_filter.label_ar : field_filter.label_en);

      if (this.field.isText) field_filter.variant = "text";

      switch (field_filter.type) {
        case "password":
          field_filter.type = "password";
          break;
        case "TimeField":
          field_filter.type = "time";
          break;
        case "PositiveSmallIntegerField":
        case "IntegerField":
        case "PositiveBigIntegerField":
        case "FloatField":
          field_filter.type = "number";
          break;
        case "DateField":
          field_filter.type = "date";
          break;
        case "DateTimeField":
          field_filter.type = "datetime-local";

          break;
        case "ManyToManyField":
          field_filter.multiple = true;
          break;
        case "ImageField":
          field_filter.width = "200";
          field_filter.height = "200";
          break;
        case "FileField":
          if (field_filter.null === false) field_filter.required = true;
          break;
      }

      if (this.attr["items"]) field_filter.objects = this.attr["items"];

      var rules = this.attr["rules"]
        ? [...this.generateValidationRules, ...this.attr["rules"]]
        : this.generateValidationRules;

      field_filter.rules = rules;

      if (field_filter.width > 12) field_filter.width = field_filter.width;
      else if (field_filter.width <= 12) {
        field_filter.cols = this.attr["cols"] || field_filter.width || "12";
        field_filter.width = null;
      }
      if (field_filter.name_list) field_filter.name = field_filter.name_list;

      if (field_filter.items && field_filter.items?.length > 0) {
        field_filter.objects = field_filter.items;
      }

      return field_filter;
    },

    generateValidationRules() {
      var rules = [];
      let field_filter = { ...this.field, ...this.attr };

      if ("rules" in this.field) rules = this.field.rules;
      if ("null" in field_filter && !field_filter.null) {
        rules.push(this.$required);
      }
      if ("min_value" in field_filter && field_filter.min_value)
        rules.push(this.$min_value(field_filter.min_value));
      if ("max_value" in field_filter && field_filter.max_value)
        rules.push(this.$max_value(field_filter.max_value));
      if ("max_length" in field_filter && field_filter.max_length)
        rules.push(this.$max_length(field_filter.max_length));
      if (field_filter.type == "DecimalField") {
        rules.push(
          this.$decimal_valid(
            field_filter.max_digits,
            field_filter.decimal_places,
            this.$numeric
          )
        );
      }
      if (field_filter.type == "JSONField") rules.push(this.$validateJson);
      // if ("name" in field_filter) {

      if (field_filter.name.endsWith("_en")) rules.push(this.$en);
      // if (field_filter.name.includes("phone")) {
      //   if (field_filter.rules) rules.push(field_filter.rules);

      //   rules.push(this.$min_length(6));
      //   rules.push(this.$max_length(14));

      //   field_filter.type = "number";
      // }
      // }

      return rules;
    },

    focusFirstElement() {
      this.$refs.componentInput.$el.querySelectorAll(button, [href], input);
    },
  },
};
</script>

<style scoped>
/*
 * field-input-ltr:
 * Ensures number, date, and code inputs always align
 * left (LTR) regardless of the page direction (RTL/LTR).
 * Applied globally to all field types rendered by Field.vue.
 */
.field-input-ltr {
  text-align: left !important;
}
</style>
