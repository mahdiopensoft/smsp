import { useRoute } from "vue-router";
import DOMPurify from "dompurify";
import { state } from "@/store/state";
import { useHeaderFooterStore } from "../stores/headerFooterStore";

export default function useHeaderFooter() {
  const profile = state?.profile
  const headerFooterStore = useHeaderFooterStore()
 
   
  const highlightVariables = (html) => {
    
    if (!html) return "";

    const config = {
      ALLOWED_TAGS: [
        "p",
        "br",
        "span",
        "img",
        "b",
        "strong",
        "i",
        "em",
        "ul",
        "li",
        
      ],
      ALLOWED_ATTR: [
        "style",
        "src",
        "width",
        "height",
        "class",
        "data-name",
        "alt",
      ],
      ADD_ATTR: ["target"],
    };

    const container = document.createElement("div");
    
    // تنظيف أولي
    container.innerHTML = DOMPurify.sanitize(html, config);
    
    const nodes = container.querySelectorAll(".ql-variable");
   
 
    nodes.forEach((node) => {
      
       const rawValue = node.getAttribute("data-name") || node.innerText;
      const cleanKey = rawValue.replace(/\{\{|\}\}/g, "").trim();
    

      const replaceVal = getVariableValue(cleanKey);
     
    

      const wrapper = document.createElement("span");

      if (replaceVal !== undefined && replaceVal !== "") {
        // التعديل هنا: إذا كان النص يحتوي على <img سنستخدم innerHTML مع تنظيفه
        // وإلا نستخدم textContent للأمان
        if (typeof replaceVal === "string" && replaceVal.includes("<img")) {
          wrapper.innerHTML = DOMPurify.sanitize(replaceVal, config);
        } else {
          wrapper.textContent = replaceVal;
        }
      } else {
        wrapper.textContent = rawValue;
        wrapper.style.color = "red";
        wrapper.style.fontWeight = "bold";
      }
      node.replaceWith(wrapper);
    });

    // استبدال النصوص {{ key }} يدوياً
    let processedHtml = container.innerHTML;
    
    processedHtml = processedHtml.replace(
      /\{\{\s*(.+?)\s*\}\}/g, // تعديل الـ Regex ليشمل المسافات بين الكلمات
      (match, key) => {
      
        
        const val = getVariableValue(key.trim());
         
        return val !== undefined && val !== "" ? val : match;
      }
    );
    

    // التنظيف النهائي هو الأهم
    return DOMPurify.sanitize(processedHtml, config);
  };

  function getVariableValue(key) {
    console.log(key);
    
   
   
    switch (key) {
      case "اسم المستخدم":    
        return profile?.username;
      case "اسم المنظمة":
        return profile?.first_name + " " + profile?.last_name;
      case "شعار المنظمة":
        const logo = new URL("@/assets/logo.png", import.meta.url).href;
        return `<img  src="${
          profile?.org_logo || logo
        }" style="vertical-align: middle; border-radius: 4px;" width="50" height="50""/>`;      
      case "البريد الالكتروني":
        return profile?.email;
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
        const route = useRoute();

        return route.meta?.name_ar || "";

      default:
        const variable = headerFooterStore.listVariables[key]
        if(variable.image){
          const logo =  variable.image
          console.log(logo);
          return `<img  src="${
            logo
          }" style="border-radius: 4px;" width="50" height="50""/>`;      
          
        }
    
         
        const code = headerFooterStore.customVariable[variable.name_code]
  
         
        if(code){
           
          return code;
          
        }
     
        return variable?.value_ar;
    }
  }

  function colSize(count) {
    return Math.floor(12 / count);
  }

  return { highlightVariables, colSize };
}
