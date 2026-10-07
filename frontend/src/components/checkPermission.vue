<template>
  <button v-if="userPermissions.CanMakePay">الدفع</button>
</template>


<script>
import { ref } from "vue";
import { onMounted } from "vue";

const userPermissions = ref({
  CanMakePay: false,
});
onMounted(async () => {
  const response = await axios.get("api/");
  userPermissions.CanMakePay = response.data.permissions;
});
</script>
