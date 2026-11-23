<template>
    <custom-dialog
        :model-value="modelValue"
        :title="title"
        width="540"
        height="auto"
        persistent
        no-click-animation
        class="master-note-portal"
        @update:model-value="$emit('update:modelValue', $event)"
    >
        <!-- Status Context Track (Visual Clue) -->
        <div v-if="entry" class="status-context-rail pa-4 rounded-lg mb-6">
            <div class="rail-label mb-2">سياق الحركة الإدارية</div>
            <div class="d-flex align-center ga-3 flex-wrap">
                <div class="status-chip old">{{ entry.old_status_display }}</div>
                <v-icon icon="mdi-arrow-left-thin" size="20" color="slate-300"></v-icon>
                <div class="status-chip new">{{ entry.new_status_display }}</div>
            </div>
        </div>

        <!-- Documentation Area -->
        <div class="documentation-arena">
            <label class="arena-label d-block mb-2">نص الملاحظة</label>
            <v-textarea v-model="internalText" placeholder="أدخل تفاصيل الملاحظة المراد إضافتها لهذا الإجراء..."
                variant="outlined" rows="5" auto-grow hide-details color="primary"
                class="portal-textarea"></v-textarea>
        </div>

        <template #actions>
            <div class="d-flex align-center justify-space-between w-100">
                <v-btn variant="text" color="slate-500" class="px-6 font-weight-bold" height="44"
                    @click="$emit('update:modelValue', false)">
                    إلغاء الإجراء
                </v-btn>
                <v-btn color="primary" variant="tonal" class="px-8 rounded-lg font-weight-black" height="44"
                    :disabled="!internalText || !internalText.trim()" @click="save">
                    تأكيد وحفظ
                </v-btn>
            </div>
        </template>
    </custom-dialog>
</template>

<script>
export default {
    name: 'NoteModal',
    props: {
        modelValue: Boolean,
        note: { type: String, default: '' },
        title: { type: String, default: 'إضافة ملحوظة إدارية' },
        entry: { type: Object, default: null}
    },
    emits: ['update:modelValue', 'save'],
    data() {
        return { internalText: '' };
    },
    watch: {
        note: {
            immediate: true,
            handler(val) { this.internalText = val || ''; }
        },
        modelValue(val) {
            if (!val) this.internalText = this.note || '';
        }
    },
    methods: {
        save() {
            this.$emit('save', this.internalText);
            this.$emit('update:modelValue', false);
        }
    }
};
</script>

<style scoped>

.master-note-portal {
    font-family: 'Noto Sans Arabic', 'Plus Jakarta Sans', sans-serif;
}

.portal-surface {
    background: #ffffff;
    /* Zero Jitter Animations */
}

.portal-header {
    background: #ffffff;
}

.portal-icon-box {
    width: 48px;
    height: 48px;
    background: #f1f5f9;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #e2e8f0;
}

.portal-h3 {
    font-size: 1.2rem;
    font-weight: 900;
    color: #0f172a;
}

.portal-sub {
    font-size: 10px;
    font-weight: 800;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.status-context-rail {
    background: #f8fafc;
    border: 1px solid #f1f5f9;
}

.rail-label {
    font-size: 10px;
    font-weight: 800;
    color: #94a3b8;
}

.status-chip {
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
}

.status-chip.old {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #64748b;
}

.status-chip.new {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #2563eb;
}

.arena-label {
    font-size: 13px;
    font-weight: 800;
    color: #475569;
}

.portal-textarea :deep(.v-field__outline) {
    --v-field-border-opacity: 0.1;
    border-radius: 10px !important;
}

.arena-footer {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
}

.portal-sep {
    border-color: #f1f5f9 !important;
}

@media (max-width: 600px) {
    .master-note-portal :deep(.v-overlay__content) {
        margin: 12px !important;
        width: calc(100% - 24px) !important;
    }
}
</style>
