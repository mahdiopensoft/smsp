<template>
  <v-menu :close-on-content-click="false" width="350">
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props" class="mr-4">
        <!-- <v-badge :content="store.unreadCount" :model-value="store.unreadCount.length >0" color="error">
                    <v-icon>mdi-bell-outline</v-icon>
                </v-badge>
                 -->
      </v-btn>
    </template>
    <VCard>
      <v-textarea
        v-model="adminMessage"
        label="اكتب الرسالة هنا ........."
        variant="filled"
        auto-grow
      />
      <custom-btn
        color="indigo-darken-2"
        size="large"
        block
        @click="submitBroadcast"
        label=" بث التعميم لكل المستخمين "
      />
    </VCard>
  </v-menu>
</template>
<script setup>
import { ref, onMounted } from "vue";

const adminMessage = ref("");

const submitBroadcast = async () => {
  // if(!adminMessage.value)  return
  // await store.senNew(adminMessage.value)
  // adminMessage.value
};

const timeAgo = (data) => {
  return new Date(date).toLocaleTimeString();
};

onMounted(() => {
  // state.fetchAll()
  // state.connectWS()
});
</script>
