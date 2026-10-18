// composables/useNavigateTo.js
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
// import { useDialogStore } from "../store/dialog";
import { alert ,showAlert} from "../utils/Globals";

export default function useNavigateTo() {
  const { locale } = useI18n();
  const router = useRouter();
  // const dialog = useDialogStore();

  const navigateTo = async (param) => {
   
    // 1. التعامل مع Breadcrumbs
    try {
      const local_breadcrumbs =
        JSON.parse(localStorage.getItem("breadcrumbs")) || [];
      local_breadcrumbs.push({
        name: param.name,
        title: param.ar,
        title_en: param.en,
      });
      localStorage.setItem("breadcrumbs", JSON.stringify(local_breadcrumbs));
    } catch (e) {
      console.error("Error parsing breadcrumbs:", e);
    }

    // 2. منطق التنقل (Navigation Logic)
    if (param.blank) {
      // فتح في نافذة جديدة
      const routeData = router.resolve({
        name: param.name,
        params: param.params,
      });

      // نستخدم href بدلاً من path لضمان دعم hash mode و history mode بشكل صحيح
      const newTab = window.open(routeData.href, "_blank");

      // التحقق من مانع النوافذ المنبثقة (Popup Blocker)
      if (!newTab || newTab.closed || typeof newTab.closed === "undefined") {
        const isAr = locale.value === "ar";

        alert("", {
          title: isAr ? "حظر النوافذ" : "Blocked window",
          message: isAr
            ? "تم حظر النوافذ المنبثقة في متصفحك. يرجى تمكينها من الإعدادات لإكمال العملية..."
            : "Pop-ups have been blocked in your browser. Please enable them in your settings...",
          icon: "window-restore",
        });
        showAlert()
      }
    } else {
      // التنقل العادي داخل نفس الصفحة
      router.push({
        name: param.name,
        params: param.params,
        query: param?.query,
      });
    }
  };

  return {
    navigateTo,
  };
}
