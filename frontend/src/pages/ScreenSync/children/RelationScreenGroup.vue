<template>
<VRow>
  
    <auto-list v-model="modelValue.fk_sync_group" name="SyncGroup" :rules="[$required]"/>
    <custom-text-field v-model="modelValue.order" type="number" :label="$t('order')"/>
    <custom-text-note v-model="modelValue.settings" :label="$t('settings')" type="number"/>
</VRow>
</template>
<script>
export default {
    props:{
        modelValue:{
            type:Boolean,
            required:true
        }
         
    },
    emits:['update:modelValue']
}
</script>