<template>
  <QuillEditor :ref="props.refEditor" />
</template>

<script setup>
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css"; // استيراد ستايل Quill
import Quill from "quill";

const props = defineProps({
  refEditor: null,
});
</script>