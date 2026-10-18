<template>
  <drawer :data="data" click="screens/systems/" :getData="getData">
    <template v-slot>
      <custom-text-field
        v-model="data.name_ar"
        label="الاسم العربي"
        :rules="[this.$required]"
      />
      <custom-text-field
        v-model="data.name_en"
        label="الاسم الانجليزي"
        :rules="[this.$required]"
      />
      <VCheckbox v-model="data.is_main" label="هل هو رئيسي" />
      <custom-text-field v-model="data.description" label="الوصف" />
      <custom-text-field
        v-model="data.order"
        label="الترتيب"
        type="number"
        :rules="[this.$required]"
      />
      <custom-text-field v-model="data.icon" label="الايقونه" />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },
  data() {
    return {};
  },
};
</script>
