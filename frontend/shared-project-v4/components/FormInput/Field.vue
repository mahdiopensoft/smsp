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
     @selectObject="(val, object) => $emit('selectObject', val, object)"
  />
</template>

  <script>
import CustomCheckBox from "./CustomCheckBox.vue";
  
export default {
  components: { CustomCheckBox },
  props: {
    field: { type: Object, required: {} },
    attr: { type: Object, default: () => ({}) },
    modelValue: {
      type: [Number, String],
      default: null,
    },
  },

  methods: {
    feature(attr) {
      return this.attr[attr];
    },
  },
  computed: {
    field_filter() {
      return {
        ...this.field,
        ...this.attr,
      };
    },
    value: {
      get() {
        if (this.field.type === "BooleanField" && this.modelValue === null) {
          this.value = this.attr["default"] || this.field.default;
        } else if (this.field.name_list && this.modelValue === null) {
          this.value = this.attr["default"] || this.field.default_val || null;
        } else if (this.modelValue === null && this.field.name_list === null) {
          this.value =
            this.field.default !=
            "<class 'django.db.models.fields.NOT_PROVIDED'>"
              ? this.attr["default"] || this.field.default || null
              : null;
          this.attr["default"] = null;
          this.field.default = null;
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
      const type = this.attr.type || this.field.type

      const is_list = this.field.name_list || this.field.items;
      return (
        {
          JSONField: "custom-text-note",
          CharField: is_list ? "auto-list" : "custom-text-field",
          IntegerField: is_list ? "auto-list" : "custom-text-field",
          DecimalField: "custom-text-field",
          PositiveSmallIntegerField: is_list
            ? "auto-list"
            : "custom-text-field",
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
          colorPicker:"color-picker",
        }[type] ??   'custom-text-field'
      );
    },
    generateFieldProps() {

      const isArabic = this.$i18n.locale === "ar";
      let field_filter = {...this.field_filter}
      field_filter.label =
        this.attr?.label ||
        (isArabic ? field_filter.label_ar : field_filter.label_en);

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
          
          if (field_filter.null === false)
            field_filter.required = true;
          break;
      }

      if (this.attr["items"]) field_filter.objects = this.attr["items"];

      var rules = this.attr["rules"]
        ? [...this.generateValidationRules, ...this.attr["rules"]]
        : this.generateValidationRules;

      field_filter.rules = rules;

      if (field_filter.width > 12)
        field_filter.width = field_filter.width;
      else if (field_filter.width <= 12) {
        field_filter.cols =
          this.attr["cols"] || field_filter.width || "12";
        field_filter.width = null;
      }
      if (field_filter.name_list)
        field_filter.name = field_filter.name_list;

      if (field_filter.items && field_filter.items?.length > 0) {
        field_filter.objects = field_filter.items;
      }

     
 
      return field_filter;
    },

    generateValidationRules() {
      var rules = [];

      if ("rules" in this.field) rules = this.field.rules;
      if ("null" in this.field_filter && !this.field_filter.null) {
        rules.push(this.$required);
      }
      if ("min_value" in this.field_filter && this.field_filter.min_value)
        rules.push(this.$min_value(this.field_filter.min_value));
      if ("max_value" in this.field_filter && this.field_filter.max_value)
        rules.push(this.$max_value(this.field_filter.max_value));
      if ("max_length" in this.field_filter && this.field_filter.max_length)
        rules.push(this.$max_length(this.field_filter.max_length));
      if (this.field_filter.type == "DecimalField"){
        rules.push(
          this.$decimal_valid(
            this.field_filter.max_digits,
            this.field_filter.decimal_places,
            this.$numeric
          )
        );
      }
      if (this.field_filter.type == "JSONField") rules.push(this.$validateJson);
      // if ("name" in this.field_filter) {
         
        // if (this.field_filter.name.endsWith("_en")) rules.push(this.$en);
        // if (this.field_filter.name.includes("phone")) {
        //   if (this.field_filter.rules) rules.push(this.field_filter.rules);

        //   rules.push(this.$min_length(6));
        //   rules.push(this.$max_length(14));

        //   this.field_filter.type = "number";
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
