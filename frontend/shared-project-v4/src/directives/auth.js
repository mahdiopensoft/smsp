import { useAuthStore } from "../UserManagement/stores/auth";

/**
 * موجه الصلاحيات (Custom Directive)
 * الاستخدام: v-auth:action="'resource'"
 * مثال: v-auth:delete="'users'"
 */
export default {
  mounted(el, binding) {
    const authStore = useAuthStore();

    // binding.arg هو ما يأتي بعد النقطتين (:) -> مثال: delete
    const action = binding.arg;

    // binding.value هو القيمة الممررة للموجه -> مثال: 'users'
    const resource = binding.value;

    // التحقق من الصلاحية عبر الـ Store
    // ملاحظة: تأكد أن الدالة في الـ Store تسمى checkPermission وترتب المعاملات (action, resource)
    if (!authStore.checkPermission(action, resource)) {
      // إزالة العنصر من الـ DOM إذا لم تتوفر الصلاحية
      if (el.parentNode) {
        el.parentNode.removeChild(el);
      }
    }
  },
};
