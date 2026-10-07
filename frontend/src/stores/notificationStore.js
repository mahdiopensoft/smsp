
import { ref } from 'vue'

const show = ref(false)
const mode = ref('snackbar')
const message = ref('')
const type = ref('info')
const title = ref('')
const timeout = ref(4000)

const confirmText = ref('تأكيد')
const cancelText = ref('إلغاء')
const showCancel = ref(false)

let onConfirmCb = null
let onCancelCb = null

export function useNotificationStore() {
    return {
        show, mode, message, type, title, timeout, confirmText, cancelText, showCancel,
        open(options) {
            mode.value = options.mode || 'snackbar'
            message.value = options.message || ''
            type.value = options.type || 'info'
            title.value = options.title || ''
            timeout.value = options.timeout !== undefined ? options.timeout : (mode.value === 'dialog' ? -1 : 4000)
            confirmText.value = options.confirmText || 'حسناً'
            cancelText.value = options.cancelText || 'إلغاء'
            showCancel.value = options.showCancel || false
            onConfirmCb = options.onConfirm || null
            onCancelCb = options.onCancel || null
            show.value = true
        },
        close() { show.value = false; if (onCancelCb) onCancelCb() },
        confirm() { show.value = false; if (onConfirmCb) onConfirmCb() },
        showSuccess(msg, customTitle = 'نجاح', isDialog = false) { this.open({ mode: isDialog ? 'dialog' : 'snackbar', message: msg, type: 'success', title: customTitle }) },
        showError(msg, customTitle = 'خطأ', isDialog = false) { this.open({ mode: isDialog ? 'dialog' : 'snackbar', message: msg, type: 'error', title: customTitle, timeout: 6000 }) },
        showWarning(msg, customTitle = 'تنبيه', isDialog = false) { this.open({ mode: isDialog ? 'dialog' : 'snackbar', message: msg, type: 'warning', title: customTitle, timeout: 5000 }) },
        showInfo(msg, customTitle = 'معلومة', isDialog = false) { this.open({ mode: isDialog ? 'dialog' : 'snackbar', message: msg, type: 'info', title: customTitle }) },
        promptConfirm(msg, t = 'تأكيد الإجراء', confirmBtn = 'تأكيد', cancelBtn = 'إلغاء') {
            return new Promise((resolve) => {
                this.open({ mode: 'dialog', title: t, message: msg, type: 'warning', showCancel: true, confirmText: confirmBtn, cancelText: cancelBtn, onConfirm: () => resolve(true), onCancel: () => resolve(false) })
            })
        },
        promptInfo(msg, t = 'تنبيه', btnText = 'حسناً', ty = 'info') {
            return new Promise((resolve) => {
                this.open({ mode: 'dialog', title: t, message: msg, type: ty, showCancel: false, confirmText: btnText, onConfirm: () => resolve(true), onCancel: () => resolve(true) })
            })
        }
    }
}
