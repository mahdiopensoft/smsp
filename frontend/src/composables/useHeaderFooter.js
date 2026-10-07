import { useRoute } from "vue-router";

// ==========================================
// المتغيرات الأساسية
// ==========================================

export const variables = [
  { name_ar: "اسم المستخدم", name_en: "user name" },
  { name_ar: "اسم المنظمة", name_en: "Organization name" },
  { name_ar: "شعار المنظمة", name_en: "Organization logo" },
  { name_ar: "البريد الالكتروني", name_en: "email" },
  { name_ar: "التاريخ الحالي", name_en: "Current date" },
  { name_ar: "الوقت الحالي", name_en: "Current time" },
  { name_ar: "التاريخ والوقت الحالي", name_en: "Current date and time" },
  { name_ar: "عنوان الشاشة", name_en: "Screen title" },
];

// ==========================================
// متغيرات الطالب (للتعميمات)
// ==========================================

export const studentVariables = [
  { name_ar: "اسم الطالب", name_en: "Student name", key: "student_name" },
  { name_ar: "رقم الطالب", name_en: "Student number", key: "student_number" },
  { name_ar: "الصف", name_en: "Grade", key: "grade_name" },
  { name_ar: "ولي الأمر", name_en: "Parent name", key: "parent_name" },
  { name_ar: "هاتف ولي الأمر", name_en: "Parent phone", key: "parent_phone" },
];

// ==========================================
// دالة استبدال المتغيرات
// ==========================================

function getVariableValue(key, variableObject = {}) {
  // يمكن ربط هذه القيم بـ Store حقيقي لاحقاً
  switch (key) {
    case "اسم المستخدم":
      return ""; // TODO: Get from auth store
    case "اسم المنظمة":
      return ""; // TODO: Get from settings
    case "شعار المنظمة":
      return ""; // TODO: Get from settings
    case "البريد الالكتروني":
      return ""; // TODO: Get from auth store
    case "التاريخ الحالي":
      return new Date().toLocaleDateString("ar-SA");
    case "الوقت الحالي":
      return new Date().toLocaleTimeString("ar-SA", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    case "التاريخ والوقت الحالي":
      return new Date().toLocaleString("ar-SA", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    case "عنوان الشاشة":
      try {
        const route = useRoute();
        return route.meta?.name_ar || "";
      } catch {
        return "";
      }

    // متغيرات الطالب
    case "اسم الطالب":
      return variableObject?.student_name || "";
    case "رقم الطالب":
      return variableObject?.student_number || "";
    case "الصف":
      return variableObject?.grade_name || "";
    case "ولي الأمر":
      return variableObject?.parent_name || "";
    case "هاتف ولي الأمر":
      return variableObject?.parent_phone || "";

    default:
      return variableObject[key];
  }
}

export const highlightVariables = (html, variableObject = {}) => {
  if (!html) return "";

  // إنشاء عنصر مؤقت للمعالجة
  const container = document.createElement("div");
  container.innerHTML = html;

  // 1. استبدال عناصر Quill المخصصة (ql-variable)
  const nodes = container.querySelectorAll(".ql-variable");
  nodes.forEach((node) => {
    const rawValue = node.getAttribute("data-name") || node.textContent || "";
    const cleanKey = rawValue.replace(/\{\{|\}\}/g, "").trim();
    const replaceVal = getVariableValue(cleanKey, variableObject);

    // إنشاء عنصر للاستبدال
    const wrapper = document.createElement("span");
    if (replaceVal !== undefined) {
      wrapper.innerHTML = replaceVal;
    } else {
      wrapper.textContent = rawValue; // إبقاء النص كما هو إذا لم يوجد متغير
      wrapper.style.color = "red"; // تمييز الخطأ
    }
    node.replaceWith(wrapper);
  });

  // 2. (احتياطي) استبدال أي نصوص {{ key }} مكتوبة يدوياً
  let processedHtml = container.innerHTML;
  processedHtml = processedHtml.replace(
    /\{\{\s*([^}]+)\s*\}\}/g,
    (match, key) => {
      const val = getVariableValue(key.trim(), variableObject);
      return val !== undefined ? val : match;
    },
  );

  return processedHtml;
};

// ==========================================
// توليد التعميمات لكل طالب
// ==========================================

export function generateAnnouncementsForStudents(
  templateHtml,
  students,
  gradeName,
) {
  return students.map((student) => {
    // تعيين القيم الافتراضية إذا لم تكن موجودة في كائن الطالب
    const studentData = {
      student_name: student.name || student.name_ar || "",
      student_number: student.academic_number || student.student_number || "",
      grade_name: gradeName || student.student_set__fk_branch_class__fk_class__name_ar || "",
      parent_name: student.fk_parent__name || student.parent_name || "",
      parent_phone: student.fk_parent__phone_number || student.phone || student.parent_phone || "",
      ...student, // دمج أي خصائص أخرى
    };

    return {
      student: student,
      content: highlightVariables(templateHtml, studentData),
    };
  });
}

export function colSize(count) {
  return Math.floor(12 / count);
}

export async function getVariables() {
  return {};
}
