<template>
  <drawer :data="data" click="chat/contacts/rules/" :items="items" type="dialog" width="60%">
    <template v-slot>
      <v-row>
        <fields :data="data" url="contact-rules-view" :attr="{}" />
        <v-col cols="12">
        <json-field
          v-model="formattedQueryConfig"
          :label="$t('contact_rules.query_config')"
          :indentation="3"
          auto-grow
          variant="outlined"
          rows="10"
          :rules="[jsonRule]"
          hide-details="auto"
          class="font-monospace"
        >
        </json-field>
        </v-col>
      </v-row>
    </template>
  </drawer>
</template>
<script>

export default {
  props: {
    data: Object,
    items: [Array, Object],
  },
  data() {
    return {};
  },
  computed: {
    formattedQueryConfig: {
      get() {
        if (!this.data.query_config) return '';
        if (typeof this.data.query_config === 'object') {
          return JSON.stringify(this.data.query_config, null, 2);
        }
        return this.data.query_config;
      },
      set(value) {
        try {
          // محاولة تحويل النص إلى كائن JSON عند التعديل
          this.data.query_config = JSON.parse(value);
        } catch (e) {
          // إذا كان النص غير صالح كـ JSON، نحتفظ به كنص مؤقتاً
          this.data.query_config = value;
        }
      }
    }
  },
  created() {},

  methods: {
    jsonRule(v) {
      if (!v) return true;
      try {
        if (typeof v === 'string') {
          JSON.parse(v);
        }
        return true;
      } catch (e) {
        return 'صيغة JSON غير صحيحة';
      }
    }
  },
};
</script>
