<template>
  <custom-dialog
    v-model="isOpen"
    :title="`${title} - سلة المحذوفات`"
    width="800"
    height="auto"
    persistent
  >
    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-center align-center py-10">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <!-- Empty State -->
    <div v-else-if="items.length === 0" class="d-flex flex-column align-center justify-center py-10 text-medium-emphasis">
      <v-icon size="64" class="mb-4" color="grey-lighten-1">mdi-delete-empty</v-icon>
      <div class="text-h6">سلة المحذوفات فارغة</div>
    </div>

    <!-- Data Table -->
    <v-table v-else hover class="bg-transparent">
      <thead>
        <tr>
          <th class="text-right">#</th>
          <th class="text-right">الاسم</th>
          <th class="text-right">تاريخ الحذف</th>
          <th class="text-center">إجراءات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td class="font-weight-medium">{{ item[nameKey] || 'بدون اسم' }}</td>
          <td dir="ltr" class="text-right">{{ formatDate(item.deleted_at) }}</td>
          <td class="text-center">
            <v-btn
              color="success"
              variant="text"
              size="small"
              prepend-icon="mdi-restore"
              @click="confirmRestore(item)"
              :loading="restoringId === item.id"
            >
              استرجاع
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </custom-dialog>

  <!-- Restore Confirmation Dialog -->
  <custom-dialog
    v-model="confirmDialog"
    title="تأكيد الاسترجاع"
    width="420"
    height="auto"
  >
    <p class="mb-0">
      هل أنت متأكد من استرجاع السجل "<strong>{{ itemToRestore?.[nameKey] }}</strong>"؟
    </p>
    <template #actions>
      <v-btn variant="text" @click="confirmDialog = false">إلغاء</v-btn>
      <v-btn color="success" variant="tonal" @click="executeRestore">تأكيد واسترجاع</v-btn>
    </template>
  </custom-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from 'vuetify'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  nameKey: {
    type: String,
    default: 'name'
  }
})

const emit = defineEmits(['update:modelValue', 'restore'])

// Theme styling
const theme = useTheme()
const isDark = computed(() => theme.global.current.value.dark)

// Dialog visibility
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const close = () => {
  isOpen.value = false
}

// Restore Confirmation Logic
const confirmDialog = ref(false)
const itemToRestore = ref(null)
const restoringId = ref(null)

const confirmRestore = (item) => {
  itemToRestore.value = item
  confirmDialog.value = true
}

const executeRestore = async () => {
  if (!itemToRestore.value) return
  
  const idToRestore = itemToRestore.value.id
  restoringId.value = idToRestore
  confirmDialog.value = false
  
  try {
    // Let parent handle the actual API call
    emit('restore', idToRestore)
  } finally {
    restoringId.value = null
    itemToRestore.value = null
  }
}

// Date formatter
const formatDate = (dateString) => {
  if (!dateString) return 'غير معروف'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ar-EG', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>

<style scoped>
.glass-card {
  background: var(--v-theme-surface);
  border: 1px solid rgba(128, 128, 128, 0.2);
}
</style>
