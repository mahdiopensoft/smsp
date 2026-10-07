export const rules = {
    required: (v) => {
        if (typeof v === 'string') return !!v.trim() || 'هذا الحقل مطلوب'
        if (Array.isArray(v)) return v.length > 0 || 'هذا الحقل مطلوب'
        return (v !== null && v !== undefined) || 'هذا الحقل مطلوب'
    },
    requiredWithMessage: (message) => (v) => {
        if (typeof v === 'string') return !!v.trim() || message
        if (Array.isArray(v)) return v.length > 0 || message
        return (v !== null && v !== undefined) || message
    },
    email: (v) => {
        if (!v) return true
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'البريد الإلكتروني غير صالح'
    },
    positive: (v) => {
        if (v === null || v === undefined || v === '') return true
        return Number(v) > 0 || 'يجب أن تكون القيمة أكبر من صفر'
    },
    minLength: (min) => (v) => {
        if (!v) return true
        return String(v).length >= min || `يجب أن يحتوي على الأقل على ${min} أحرف`
    },
    maxLength: (max) => (v) => {
        if (!v) return true
        return String(v).length <= max || `يجب أن يحتوي على الأكثر على ${max} أحرف`
    },
    matchPassword: (password) => (v) => {
        return v === password || 'كلمات المرور غير متطابقة'
    },
}
