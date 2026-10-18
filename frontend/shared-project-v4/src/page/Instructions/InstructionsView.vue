<template>
  <VCol>
    <VRow v-for="(item, index) in data" :key="index">
      <auto-list name="parent_screen" cols="4" />
      <custom-text-field v-model="item.text" label="العنوان" cols="6" />

      <custom-text-field
        v-model="item.color"
        label="اللون"
        cols="2"
        @click="item.dialog = true"
      >
        <template v-slot:append-inner>
          <VCard :color="item.color" height="20" width="20" />
        </template>
      </custom-text-field>

      <CustomDialog
        v-model="item.dialog"
        class="text-center align-center"
        height="auto"
        width="auto"
      >
        <VColorPicker v-model="item.color" hide-inputs />
      </CustomDialog>
    </VRow>
    <VRow>
      <v-spacer />
      <VBtn
        v-if="data.length != 1"
        variant="text"
        color="red"
        icon="mdi-minus"
        class="me-5"
        @click="removeItem"
      />
      <VBtn
        variant="text"
        color="blue"
        icon="mdi-plus"
        class="me-5"
        @click="addItem"
      />
    </VRow>
    <custom-btn type="save" width="100%" />
  </VCol>
</template>
<script>
export default {
  data() {
    return {
      data: [{ text: null, color: null }],
    };
  },
  methods: {
    addItem() {
      this.data.push({ text: null, color: null });
    },
    removeItem() {
      if (this.data.length != 1) this.data.length = this.data.length - 1;
      //   this.data.splice(index,1);
    },
  },
};
</script>