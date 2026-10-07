<template>
  <v-dialog v-model="isOpen" max-width="800" persistent>
    <v-card class="glass-card">
      <v-toolbar color="error" class="px-4 text-white">
        <v-icon start>mdi-delete-restore</v-icon>
        <v-toolbar-title>{{ title }} - سلة المحذوفات</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-0">
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
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Restore Confirmation Dialog -->
  <v-dialog v-model="confirmDialog" max-width="400">
    <v-card class="glass-card pa-4">
      <v-card-title class="text-h6 font-weight-bold text-success d-flex align-center">
        <v-icon start color="success" class="me-2">mdi-alert-circle</v-icon>
        تأكيد الاسترجاع
      </v-card-title>
      <v-card-text class="pt-2 pb-4">
        هل أنت متأكد من استرجاع السجل "<strong>{{ itemToRestore?.[nameKey] }}</strong>"؟
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="confirmDialog = false">إلغاء</v-btn>
        <v-btn color="success" variant="tonal" @click="executeRestore">تأكيد واسترجاع</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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
