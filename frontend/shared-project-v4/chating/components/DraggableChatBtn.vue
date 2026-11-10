<template>
  <div
    v-show="!$route.path.includes('/chatting')"
    class="draggable-chat-container"
    ref="chatContainerRef"
    :style="{
      transform: `translate3d(${chatPos.x}px, ${chatPos.y}px, 0)`,
      cursor: isDraggingChat ? 'grabbing' : 'grab',
      transition: isDraggingChat ? 'none' : 'transform 0.1s ease'
    }"
    @mousedown.prevent="startChatDrag"
    @touchstart="startChatDrag"
  >
    <v-btn color="primary" icon="mdi-forum" size="large" elevation="8"
      class="draggable-chat-btn"
      :ripple="!isDraggingChat"
      @click.stop="handleChatClick(() => chatStore.toggleQuickChat())">
    </v-btn>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useChatStore } from "../store/chat";

const chatStore = useChatStore();

const chatPos = ref({ x: window.innerWidth - 80, y: window.innerHeight - 80 });
const chatContainerRef = ref(null);
const isDraggingChat = ref(false);
const chatDragOffset = ref({ x: 0, y: 0 });
let hasMoved = false;

const startChatDrag = (e) => {
  isDraggingChat.value = true;
  hasMoved = false;
  const clientX = e.clientX || (e.touches && e.touches[0].clientX);
  const clientY = e.clientY || (e.touches && e.touches[0].clientY);
  
  chatDragOffset.value.x = clientX - chatPos.value.x;
  chatDragOffset.value.y = clientY - chatPos.value.y;

  document.addEventListener('mousemove', onChatDrag);
  document.addEventListener('touchmove', onChatDrag, { passive: false });
  document.addEventListener('mouseup', stopChatDrag);
  document.addEventListener('touchend', stopChatDrag);
};

const onChatDrag = (e) => {
  if (!isDraggingChat.value) return;
  hasMoved = true;
  if(e.cancelable) e.preventDefault();
  
  const clientX = e.clientX || (e.touches && e.touches[0].clientX);
  const clientY = e.clientY || (e.touches && e.touches[0].clientY);

  let newX = clientX - chatDragOffset.value.x;
  let newY = clientY - chatDragOffset.value.y;

  newX = Math.max(0, Math.min(newX, window.innerWidth - 64));
  newY = Math.max(0, Math.min(newY, window.innerHeight - 64));

  if (chatContainerRef.value) {
    chatContainerRef.value.style.transform = `translate3d(${newX}px, ${newY}px, 0)`;
  }
  chatPos.value.x = newX;
  chatPos.value.y = newY;
};

const stopChatDrag = (e) => {
  isDraggingChat.value = false;
  document.removeEventListener('mousemove', onChatDrag);
  document.removeEventListener('touchmove', onChatDrag);
  document.removeEventListener('mouseup', stopChatDrag);
  document.removeEventListener('touchend', stopChatDrag);
};

const handleChatClick = (toggleAction) => {
  if (!hasMoved) {
    toggleAction();
  }
};

const handleResize = () => {
  chatPos.value.x = Math.min(chatPos.value.x, window.innerWidth - 64);
  chatPos.value.y = Math.min(chatPos.value.y, window.innerHeight - 64);
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.draggable-chat-container {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1010;
  touch-action: none;
  border-radius: 50%;
}
.draggable-chat-btn {
  width: 64px !important;
  height: 64px !important;
  pointer-events: auto;
}
</style>
