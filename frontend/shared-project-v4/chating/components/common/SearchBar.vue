<template>
  <v-text-field
    v-model="searchText"
    class="search-bar"
    density="compact"
    hide-details
    :placeholder="placeholder"
    rounded="lg"
    single-line
    variant="solo"
    :autofocus="autofocus"
    @keydown.down.prevent="$emit('next')"
    @keydown.up.prevent="$emit('prev')"
    @keyup.enter="onEnter"
    @update:model-value="onInput"
  >
    <template #prepend-inner>
      <v-icon color="secondary" size="20">mdi-magnify</v-icon>
    </template>

    <template v-if="searchText" #append-inner>
      <v-btn icon size="x-small" variant="text" @click="clear">
        <v-icon size="18">mdi-close</v-icon>
      </v-btn>
    </template>
  </v-text-field>
</template>

<script setup>
  import { ref, watch } from 'vue'

  const props = defineProps({
    modelValue: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: 'بحث...',
    },
    debounce: {
      type: Number,
      default: 300,
    },
    autofocus: {
      type: Boolean,
      default: false,
    },
  })

  const emit = defineEmits([
    'update:modelValue',
    'search',
    'enter',
    'prev',
    'next',
  ])

  const searchText = ref(props.modelValue)
  let debounceTimer = null

  // مزامنة مع v-model الخارجي
  watch(
    () => props.modelValue,
    val => {
      searchText.value = val
    },
  )

  // تأخير البحث
  function onInput (value) {
    if (debounceTimer) clearTimeout(debounceTimer)

    debounceTimer = setTimeout(() => {
      emit('update:modelValue', value)
      emit('search', value)
    }, props.debounce)
  }

  // الضغط على Enter
  function onEnter () {
    if (debounceTimer) clearTimeout(debounceTimer)
    emit('update:modelValue', searchText.value)
    emit('enter', searchText.value)
  }

  // مسح البحث
  function clear () {
    searchText.value = ''
    emit('update:modelValue', '')
    emit('search', '')
  }
</script>

<style scoped>
.search-bar {
  max-width: 100%;
}

.search-bar :deep(.v-field) {
  min-height: 36px;
}

.search-bar :deep(.v-field__input) {
  padding-top: 6px;
  padding-bottom: 6px;
  min-height: 36px;
}
</style>
