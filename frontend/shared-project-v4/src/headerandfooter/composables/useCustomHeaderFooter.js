import { ref, computed, reactive } from "vue";
import api from "../../../plugins/axios-plugin";
import { getRouter } from "../../router/routerInstance";
import setting from "@/../settings";


import { state } from "@/store/state";
// Clean SVG Data URLs for offline reliability
const SVG_LOGO = `https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRiyxPWk4T7mdaSvg78_15s1_esPrbvcR5df5BjcvhPEFar7VWnRYWa-SU&s=10`;
const SVG_AVATAR =
  `data:image/svg+xml;utf8,` +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" width="50" height="50"><circle cx="25" cy="25" r="24" fill="#0284c7"/><circle cx="25" cy="18" r="9" fill="#ffffff"/><path d="M10 42 C10 32 17 29 25 29 C33 29 40 32 40 42 Z" fill="#ffffff"/></svg>`
  );
 
const SVG_GENERIC_IMG =
  `data:image/svg+xml;utf8,` +
  encodeURIComponent(
    `<svg xmlns="http://www.w3س.org/2000/svg" viewBox="0 0 120 50" width="120" height="50"><rect width="120" height="50" rx="6" fill="#0d9488"/><path d="M15 38 L35 18 L55 38 L75 24 L95 38 Z" fill="#ffffff" opacity="0.4"/><circle cx="85" cy="16" r="6" fill="#fef08a"/><text x="60" y="44" fill="#ffffff" font-family="sans-serif" font-size="10" text-anchor="middle" font-weight="bold">IMAGE</text></svg>`
  );

export const sanitizeImgSrc = (src) => {
  if (!src || typeof src !== "string") return "";
  const trimmed = src.trim();
  if (trimmed.startsWith("data:image/svg+xml;utf8,<svg")) {
    return (
      "data:image/svg+xml;utf8," +
      encodeURIComponent(trimmed.substring("data:image/svg+xml;utf8,".length))
    );
  }
  return trimmed;
};

// 1. Static Variables (Tab 1) matching API schema:
// { id, name_ar, name_en, value_ar, value_en, name_code, image, icon }

const logo = new URL("@/assets/logo.png", import.meta.url).href;
 



 

export const STATIC_VARIABLES = [
  {
    id: 1,
    name_ar: "اسم المستخدم",
    name_en: "User Name",
    value_ar:'',
    value_en: '',
    name_code: "userName",
    image: "",
    icon: "mdi-account",
    key: "{{userName}}",
    label: "اسم المستخدم",
    value: '',
    color: "primary",
  },
  // {
    //   id: 2,
    //   name_ar:"اسم الكيان",
    //   name_en: "Company Name",
    //   value_ar: profile?.first_name + " " + profile?.last_name,
    //   value_en:  profile?.first_name + " " + profile?.last_name,
  //   name_code: "companyName",
  //   image: "",
  //   icon: "mdi-domain",
  //   key: "{{companyName}}",
  //   label:"اسم الكيان",
  //   value: profile?.first_name + " " + profile?.last_name,
  //   color: "success",
  // },
  {
    id: 3,
    name_ar: "الشعار",
    name_en: "Organization Logo",
    value_ar: "الشعار",
    value_en: "Organization Logo",
    name_code: "organizationLogo",
    image: logo,
    icon: "mdi-image-filter-frames",
    key: "{{organizationLogo}}",
    label: "الشعار",
    value: "الشعار",
    color: "indigo",
  },


  {
    id: 3,
    name_ar: "البريد الإلكتروني",
    name_en: "User Email",
    value_ar:"",
    value_en:"",
    name_code: "userEmail",
    image: "",
    icon: "mdi-email",
    key: "{{userEmail}}",
    label: "البريد الإلكتروني",
    value:"",
    color: "info",
  },


  {
    id: 4,
    name_ar: "التاريخ الحالي",
    name_en: "Current Date",
    value_ar:   '',
    value_en:   '',
    name_code: "date",
    image: "",
    icon: "mdi-calendar",
    key: "{{date}}",
    label: "التاريخ الحالي",
    value:  '',
    color: "warning",
  },
  {
    id: 5,
    name_ar: "الوقت الحالي",
    name_en: "Current Time",
    value_ar:'',
    value_en:'',
    name_code: "time",
    image: "",
    icon: "mdi-clock",
    key: "{{time}}",
    label: "الوقت الحالي",
    value: '',
    color: "error",
  },
    
  {
    id: 6,
    name_ar: "عنوان الصفحة",
    name_en: "Page Title",
    value_ar:'',
    value_en:'',
    name_code: "pageTitle",
    image: "",
    icon: "mdi-file-document",
    key: "{{pageTitle}}",
    label: "عنوان الصفحة",
    value:'',
    color: "purple",
  },
   
  // {
  //   id: 10,
  //   name_ar: "رقم الهاتف",
  //   name_en: "Phone Number",
  //   value_ar: "+966 55 123 4567",
  //   value_en: "+966 55 123 4567",
  //   name_code: "phone",
  //   image: "",
  //   icon: "mdi-phone",
  //   key: "{{phone}}",
  //   label: "رقم الهاتف",
  //   value: "+966 55 123 4567",
  //   color: "green",
  // },
  // Image Variables (have image data)
  // {
  //   id: 11,
  //   name_ar: "صورة عامة",
  //   name_en: "General Image",
  //   value_ar: "صورة",
  //   value_en: "Image",
  //   name_code: "image",
  //   image: SVG_GENERIC_IMG,
  //   icon: "mdi-image-outline",
  //   key: "{{image}}",
  //   label: "صورة عامة",
  //   value: "صورة",
  //   color: "deep-purple",
  // },
   
 
  // {
  //   id: 13,
  //   name_ar: "صورة المستخدم",
  //   name_en: "User Avatar",
  //   value_ar: "الصورة الشخصية",
  //   value_en: "User Avatar",
  //   name_code: "userAvatar",
  //   image: SVG_AVATAR,
  //   icon: "mdi-account-circle-outline",
  //   key: "{{userAvatar}}",
  //   label: "صورة المستخدم",
  //   value: "الصورة الشخصية",
  //   color: "cyan",
  // },
];

// Fallback Mock API Variables matching exact schema
export const DEFAULT_API_VARIABLES = [
  
];

// Backward compatibility export
export const AVAILABLE_VARIABLES = STATIC_VARIABLES;

const createDefaultCell = (cellIndex) => ({
  id: `cell-${Date.now()}-${cellIndex}`,
  content: "",
  style: {
    fontSize: "14",
    fontFamily: "Tajawal",
    fontWeight: "normal",
    fontStyle: "normal",
    textDecoration: "none",
    color: "#1a1a1a",
    textAlign: "center",
    backgroundColor: "transparent",
  },
});

const buildColumns = (count, existingCells = []) => {
  return Array.from({ length: count }, (_, i) => {
    return existingCells[i] || createDefaultCell(i);
  });
};

// ── Module-Level Reactive State (Pure Vue Composable, No Pinia) ──────
const templates = ref({ results: [] });
const activeTemplateId = ref(null);
const draftTemplate = ref(null);
const editingBackup = ref(null);

// ── Variables State ──────────────────────────────────────────────────
const staticVariables = ref([...STATIC_VARIABLES]);
const apiVariables = ref([...DEFAULT_API_VARIABLES]);
const variable = ref({});
const apiLoading = ref(false);
const apiError = ref(null);
const apiLoaded = ref(false);

export function useCustomHeaderFooter() {
  // Combined variables list for quick resolution
  const allVariables = computed(() => {
    return [...staticVariables.value, ...apiVariables.value];
  });

  const findTemplate = (id) => {
    if (draftTemplate.value && draftTemplate.value.id === id) {
      return draftTemplate.value;
    }
    return templates.value?.results.find((t) => t.id === id) || null;
  };

  const activeTemplate = computed(() => {
    if (
      draftTemplate.value &&
      draftTemplate.value.id === activeTemplateId.value
    ) {
      return draftTemplate.value;
    }

    return (
      templates.value?.results.find((t) => t.id === activeTemplateId.value) ||
      null
    );
  });

  // ── Fetch Environment Variables from API ────────────────────────────
  const fetchApiVariables = async () => {
    apiLoading.value = true;
    apiError.value = null;
    try {
      // Try fetching from the environment variables endpoint
      const response = await api(
        "common/environment-variables-r/all/",
        {},
        { skipInterceptor: true }
      );

      const rawData =
        response?.data?.data || response?.data?.results || response?.data || [];
      const items = Array.isArray(rawData)
        ? rawData
        : Array.isArray(rawData.items)
        ? rawData.items
        : [];

      if (items.length > 0) {
        apiVariables.value = items.map((item, idx) => {
          const rawCode =
            item.name_code ||
            item.code ||
            item.key ||
            item.name_en ||
            `var_${idx}`;
          const cleanCode = String(rawCode).replace(/[{}]/g, "").trim();
          const key = `{{${cleanCode}}}`;
          const nameAr = item.name_ar || item.title_ar || cleanCode;
          const nameEn = item.name_en || cleanCode;
          const valAr =
            item.value_ar !== undefined ? item.value_ar : item.value || "";
          const valEn =
            item.value_en !== undefined ? item.value_en : item.value || "";

          // Check if image data is present
          const imageVal =
            item.image ||
            (cleanCode.toLowerCase().includes("image") ||
            cleanCode.toLowerCase().includes("logo") ||
            cleanCode.toLowerCase().includes("stamp")
              ? SVG_GENERIC_IMG
              : "");
          const hasImage = !!imageVal;

          return {
            id: item.id || idx + 1,
            name_ar: nameAr,
            name_en: nameEn,
            value_ar: valAr,
            value_en: valEn,
            name_code: cleanCode,
            image: imageVal,
            icon:
              item.icon || (hasImage ? "mdi-image-outline" : "mdi-variable"),
            // Compatibility fields
            key,
            label: nameAr,
            value: valAr || valEn || cleanCode,
            color: hasImage
              ? "deep-purple"
              : idx % 2 === 0
              ? "primary"
              : "teal",
            raw: item,
          };
        });
      } else {
        // Fallback default variables if response is empty
        apiVariables.value = [...DEFAULT_API_VARIABLES];
      }
      apiLoaded.value = true;
    } catch (err) {
      console.warn(
        "Could not fetch from common/environment-variables-r, using rich default environment variables:",
        err
      );
      apiError.value = "تعذر الاتصال بـ API، تم تفعيل المتغيرات الافتراضية.";
      apiVariables.value = [...DEFAULT_API_VARIABLES];
      apiLoaded.value = true;
    } finally {
      apiLoading.value = false;
    }
  };

  // ── Templates API CRUD ───────────────────────────────────────────────

  /**
   * Map raw API item → internal template object
   */
  const mapApiItemToTemplate = (item) => {
    // Support both flat JSON and nested structure from API
    let data = item;

    if (typeof data.header === "string") {
      try {
        data.header = JSON.parse(data.header);
      } catch (e) {
        data.header = {};
      }
    }
    
    if (typeof data.footer === "string") {
      try {
        data.footer = JSON.parse(data.footer);
      } catch (e) {
        data.footer = {};
      }
    }
    
    const rawHeader =
    (data && typeof data.header === "object" && data.header) ||
    (item && typeof item.header === "object" && item.header) ||
    {};
     
    const headerCols = Number(rawHeader.columns || 3);
    const headerCells =
      Array.isArray(rawHeader.cells) && rawHeader.cells.length
        ? rawHeader.cells
        : buildColumns(headerCols);

    const rawFooter =
      (data && typeof data.footer === "object" && data.footer) ||
      (item && typeof item.footer === "object" && item.footer) ||
      {};
    const footerCols = Number(rawFooter.columns || 3);
    const footerCells =
      Array.isArray(rawFooter.cells) && rawFooter.cells.length
        ? rawFooter.cells
        : buildColumns(footerCols);

    return {
      id: item.id || item.pk || `tpl-${Date.now()}`,
      apiId: item.id || item.pk || null,
      name: data.name || item.name || "قالب",
      createdAt: item.created_at || item.createdAt || new Date().toISOString(),
      header: {
        columns: headerCols,
        cells: headerCells,
        backgroundColor: rawHeader.backgroundColor || "#ffffff",
        borderBottom:
          rawHeader.borderBottom !== undefined ? rawHeader.borderBottom : true,
        height: rawHeader.height || "60",
      },
      footer: {
        columns: footerCols,
        cells: footerCells,
        backgroundColor: rawFooter.backgroundColor || "#f8fafc",
        borderTop:
          rawFooter.borderTop !== undefined ? rawFooter.borderTop : true,
        height: rawFooter.height || "50",
      },
    };
  };

  /**
   * Map internal template → API payload
   */
  const mapTemplateToApiPayload = (tpl) => ({
    name: tpl.name,
    header: JSON.stringify(tpl.header),
    footer: JSON.stringify(tpl.footer),
    
  });

  /**
   * GET common/print-report-setting/ — جلب جميع القوالب
   */
  const fetchTemplatesFromApi = async () => {
    const response = await api("common/print-report-setting/");
    
    
    templates.value.pagination = response.data?.pagination

    templates.value.results = response.data?.results.map(mapApiItemToTemplate)

 
  };

  /**
   * POST common/print-report-setting/ — حفظ قالب جديد
   * Returns the saved template with server-assigned id.
   */
  const saveTemplateToApi = async (tpl) => {
    const payload = mapTemplateToApiPayload(tpl);
    const response = await api.post("common/print-report-setting/", payload);

    const saved = response?.data?.data || response?.data || {};
    const savedTpl = mapApiItemToTemplate({
      ...saved,
      ...(!saved.id ? { id: tpl.id } : {}),
    });
    // Replace the draft in local list with the server version
    const idx = templates.value?.results.findIndex((t) => t.id === tpl.id);
    if (idx !== -1) {
      templates.value.results[idx] = savedTpl;
    } else {
      templates.value?.results.push(savedTpl);
    }
    activeTemplateId.value = savedTpl.id;
    return savedTpl;
  };

  /**
   * PUT common/print-report-setting/{id}/ — تعديل قالب موجود
   */
  const updateTemplateInApi = async (tpl) => {
    const apiId = tpl.apiId || tpl.id;
    const payload = mapTemplateToApiPayload(tpl);
    const response = await api.put(
      `common/print-report-setting/${apiId}/`,
      payload
    );
    const updated = response?.data?.data || response?.data || {};
    const updatedTpl = mapApiItemToTemplate({ ...tpl, ...updated });
    const idx = templates.value?.results.findIndex((t) => t.id === tpl.id);
    if (idx !== -1) {
      templates.value.results[idx] = updatedTpl;
    }
    return updatedTpl;
  };

  /**
   * مسح جميع بيانات القوالب من الذاكرة (يُستدعى عند الخروج من الشاشة)
   */
  const clearTemplates = () => {
    templates.value = { results: [] };
    activeTemplateId.value = null;
    draftTemplate.value = null;
    editingBackup.value = null;
  };

  // ── Template Actions ─────────────────────────────────────────────────
  const createTemplate = ({ name, headerColumns, footerColumns }) => {
    const id = `tpl-${Date.now()}`;
    const tpl = {
      id,
      name,
      createdAt: new Date().toISOString(),
      header: {
        columns: headerColumns,
        cells: buildColumns(headerColumns),
        backgroundColor: "#ffffff",
        borderBottom: true,
        height: "60",
      },
      footer: {
        columns: footerColumns,
        cells: buildColumns(footerColumns),
        backgroundColor: "#ffffff",
        borderTop: true,
        height: "50",
      },
    };
    templates.value?.results.push(tpl);
    activeTemplateId.value = id;
    return id;
  };

  const duplicateTemplate = async (id) => {
    const original = templates.value?.results.find((t) => t.id === id);
    if (!original) return null;

    const copy = JSON.parse(JSON.stringify(original));
    if(copy.name.includes('(نسخة)')) {
      const newText = copy.name?.replace(/(\d+)\s*$/,(_,num)=>Number(num)+1)    
      if(newText){
        copy.name = newText
      }else {
        copy.name = `${copy.name}(نسخة) 1`
      }

    }

    else copy.name = `${copy.name}(نسخة) 1`;

  

    delete copy.id
    original.loading = true
    try{
    await saveTemplateToApi(copy)
    }finally{
    original.loading = false
    }

    // const newId = `tpl-${Date.now()}`;
    // copy.id = newId;
    // copy.createdAt = new Date().toISOString();
    // templates.value?.results.push(copy);
    // return newId;
  };

  const deleteTemplate = (id) => {
    templates.value.results = templates.value?.results.filter(
      (t) => t.id !== id
    );
    if (activeTemplateId.value === id) {
      activeTemplateId.value = templates.value?.results[0]?.id || null;
    }
  };

  const setActiveTemplate = (id) => {
    activeTemplateId.value = id;
  };

  const setHeaderColumns = (id, count) => {
    const tpl = findTemplate(id);
    if (!tpl) return;
    tpl.header.columns = count;
    tpl.header.cells = buildColumns(count, tpl.header.cells);
  };

  const setFooterColumns = (id, count) => {
    const tpl = findTemplate(id);
    if (!tpl) return;
    tpl.footer.columns = count;
    tpl.footer.cells = buildColumns(count, tpl.footer.cells);
  };

  const updateCellContent = (templateId, section, cellIndex, content) => {
    const tpl = findTemplate(templateId);
    if (!tpl || !tpl[section] || !tpl[section].cells[cellIndex]) return;
    tpl[section].cells[cellIndex] = {
      ...tpl[section].cells[cellIndex],
      content,
    };
  };

  const updateCellStyle = (
    templateId,
    section,
    cellIndex,
    styleKey,
    styleValue
  ) => {
    const tpl = findTemplate(templateId);
    if (!tpl || !tpl[section] || !tpl[section].cells[cellIndex]) return;
    tpl[section].cells[cellIndex].style = {
      ...tpl[section].cells[cellIndex].style,
      [styleKey]: styleValue,
    };
  };

  const updateSectionStyle = (templateId, section, key, value) => {
    const tpl = findTemplate(templateId);
    if (!tpl || !tpl[section]) return;
    tpl[section][key] = value;
  };

  // ── Draft & Edit Lifecycle ──────────────────────────────────────────
  const startNewTemplateDraft = ({ name, headerColumns, footerColumns }) => {
    const id = `tpl-${Date.now()}`;
    const tpl = {
      id,
      name,
      createdAt: new Date().toISOString(),
      header: {
        columns: headerColumns,
        cells: buildColumns(headerColumns),
        backgroundColor: "#ffffff",
        borderBottom: true,
        height: "60",
      },
      footer: {
        columns: footerColumns,
        cells: buildColumns(footerColumns),
        backgroundColor: "#ffffff",
        borderTop: true,
        height: "50",
      },
    };
    draftTemplate.value = tpl;
    editingBackup.value = null;
    activeTemplateId.value = id;
    return id;
  };

  const commitDraftTemplate = () => {
    if (!draftTemplate.value) return null;
    const savedTpl = JSON.parse(JSON.stringify(draftTemplate.value));
    templates.value?.results.push(savedTpl);
    draftTemplate.value = null;
    activeTemplateId.value = savedTpl.id;
    return savedTpl.id;
  };

  const cancelDraftTemplate = () => {
    draftTemplate.value = null;
    activeTemplateId.value = templates.value?.results[0]?.id || null;
  };

  const startEditTemplate = (id) => {
    const tpl = templates.value?.results.find(t=>t.id === id)
    if (!tpl) return;
    draftTemplate.value = null;
    
    editingBackup.value = JSON.parse(JSON.stringify(tpl));
   
   
    activeTemplateId.value = tpl.id;
  };

  const commitEditTemplate = () => {
    editingBackup.value = null;
  };

  const cancelEditTemplate = () => {
    if (editingBackup.value) {
      const idx = templates.value?.results.findIndex(
        (t) => t.id === editingBackup.value.id
      );
      if (idx !== -1) {
        templates.value.results[idx] = JSON.parse(
          JSON.stringify(editingBackup.value)
        );
      }
      editingBackup.value = null;
    }
  };

  // ── HTML Generation with Image Support ────────────────────────────────
  const generateHTMLForTemplate = (tpl, sampleData = {}) => {
    if (!tpl) return { header: "", footer: "" };

    const resolveVars = (text) => {
      if (!text) return "";
      let result = text;

      allVariables.value.forEach((val) => {    
        
        
        let v ={...val,...variable.value[val.name_code]}

        switch(v.name_code){
          case "organizationLogo":
             if(state.profile?.org_logo){
            v.image = setting.url_img +  state.profile?.org_logo 
            }
            break;
        }
                      

        const cleanKey = String(v.name_code || v.key || "")
          .replace(/[{}]/g, "")
          .trim();

        const customValue =
          sampleData[v.name_code] ||
          sampleData[cleanKey] ||
          sampleData[`{{${cleanKey}}}`] ||
          (v.key ? sampleData[v.key] : undefined);
     
        const rawImgSrc = v.image || (cleanKey === "image" && customValue ? customValue:null) || null
        const imgSrc = sanitizeImgSrc(rawImgSrc)

        const isImageVar = !!v.image || cleanKey === "image"              

        const tokenRegex = new RegExp(
          `\\{\\{${cleanKey}(?:\\|([^}]+))?\\}\\}`,
          "g"
        );

        if (isImageVar) {   
            result = result.replace(tokenRegex, (match, paramStr) => {
            let w = 80;
            let h = null;
            let shape = "default";
            let opacity = 100;
            let fit = "contain";

            const KNOWN_FITS = [
              "contain",
              "cover",
              "fill",
              "none",
              "scale-down",
            ];
            const KNOWN_SHAPES = [
              "default",
              "circle",
              "card",
              "squircle",
              "badge",
              "frame",
              "pill",
              "glow",
              "polaroid",
              "stamp-double",
              "shadow-3d",
              "glass",
            ];

        

           
          




            if (paramStr) {
              const parts = paramStr.split("|");
              let hasExplicitDims = false;
              let shapeSeen = false;
              let numCount = 0;
              for (let i = 0; i < parts.length; i++) {
                const p = parts[i].trim();
                if (!p) continue;
                if (
                  p.includes("x") &&
                  !isNaN(parseInt(p.split("x")[0])) &&
                  !isNaN(parseInt(p.split("x")[1]))
                ) {
                  const dimParts = p.split("x");
                  w = parseInt(dimParts[0]) || 80;
                  h = parseInt(dimParts[1]) || w;
                  hasExplicitDims = true;
                } else if (KNOWN_FITS.includes(p) || p.startsWith("fit:")) {
                  fit = p.replace("fit:", "");
                } else if (
                  p.startsWith("op") ||
                  p.endsWith("%") ||
                  p.startsWith("opacity:")
                ) {
                  const val = parseInt(p.replace(/[^0-9]/g, ""));
                  if (!isNaN(val) && val >= 5 && val <= 100) opacity = val;
                } else if (KNOWN_SHAPES.includes(p) || p.startsWith("shape:")) {
                  shape = p.replace("shape:", "");
                  shapeSeen = true;
                } else if (!isNaN(parseInt(p)) && String(parseInt(p)) === p) {
                  const num = parseInt(p);
                  if (hasExplicitDims || shapeSeen) {
                    if (num >= 5 && num <= 100) {
                      opacity = num;
                    }
                  } else {
                    numCount++;
                    if (numCount === 1) {
                      w = num;
                      h = num;
                    } else if (numCount === 2) {
                      h = num;
                    } else if (numCount >= 3 && num >= 5 && num <= 100) {
                      opacity = num;
                    }
                  }
                } else {
                  shape = p;
                  shapeSeen = true;
                }
              }
            }

            let shapeCSS = "border-radius: 6px !important;";
            if (shape === "circle") {
              shapeCSS =
                "border-radius: 50% !important; aspect-ratio: 1 / 1 !important; object-fit: cover !important;";
            } else if (shape === "card") {
              shapeCSS =
                "border-radius: 10px !important; background: #ffffff !important; box-shadow: 0 3px 10px rgba(0,0,0,0.12) !important; padding: 4px !important; border: 1px solid rgba(0,0,0,0.08) !important;";
            } else if (shape === "squircle") {
              shapeCSS = "border-radius: 24% !important;";
            } else if (shape === "badge") {
              shapeCSS =
                "border: 2px dashed #1976d2 !important; border-radius: 12px !important; padding: 4px !important; background: rgba(37,99,235,0.06) !important;";
            } else if (shape === "frame") {
              shapeCSS =
                "border: 2px solid #1976d2 !important; border-radius: 5px !important; padding: 3px !important; background: #ffffff !important; box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;";
            } else if (shape === "pill") {
              shapeCSS =
                "border-radius: 9999px !important; border: 1px solid rgba(0,0,0,0.08) !important; background: #ffffff !important; box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important; padding: 4px 10px !important;";
            } else if (shape === "glow") {
              shapeCSS =
                "border-radius: 10px !important; box-shadow: 0 0 14px rgba(37,99,235,0.45), 0 2px 8px rgba(0,0,0,0.1) !important; border: 1.5px solid rgba(37,99,235,0.5) !important; background: #ffffff !important; padding: 4px !important;";
            } else if (shape === "polaroid") {
              shapeCSS =
                "background: #ffffff !important; border-radius: 4px !important; padding: 4px 4px 14px 4px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.14) !important; border: 1px solid #e2e8f0 !important;";
            } else if (shape === "stamp-double") {
              shapeCSS =
                "border: 4px double #1976d2 !important; border-radius: 50% !important; padding: 4px !important; aspect-ratio: 1 / 1 !important; background: rgba(37,99,235,0.04) !important; box-shadow: 0 0 0 1.5px rgba(25,118,210,0.6) !important; object-fit: cover !important;";
            } else if (shape === "shadow-3d") {
              shapeCSS =
                "border-radius: 8px !important; background: #ffffff !important; box-shadow: 0 10px 22px -3px rgba(0,0,0,0.22), 0 4px 8px -2px rgba(0,0,0,0.12) !important; border: 1px solid rgba(0,0,0,0.08) !important; padding: 4px !important;";
            } else if (shape === "glass") {
              shapeCSS =
                "background: rgba(241,245,249,0.75) !important; border-radius: 12px !important; border: 1.5px solid rgba(203,213,225,0.8) !important; box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important; padding: 4px !important;";
            }

            if (opacity < 100) {
              shapeCSS += ` opacity: ${opacity / 100} !important;`;
            }
            if (fit) {
              shapeCSS += ` object-fit: ${fit} !important;`;
            }

            // Standard MDI image-off icon SVG (الأيقونة المشطوبة الدالة على عدم وجود صورة)
            const iconSize = Math.max(16, Math.min(32, Math.round(w * 0.35)));
            const noImgSvg =  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="${iconSize}" height="${iconSize}" fill="#94a3b8" style="display:block;"><path d="M21,19.22L5.13,3.35L3.85,4.63L5.47,6.25C5.18,6.77 5,7.36 5,8V19C5,20.1 5.9,21 7,21H19.77L20.22,21.46L21.5,20.18L21,19.22M7,19C6.45,19 6,18.55 6,18V8C6,7.74 6.09,7.5 6.24,7.31L17.93,19H7M21,8.41V16.8L19,14.8V8C19,7.45 18.55,7 18,7H11.2L9.2,5H18C19.1,5 20,5.9 20,7V8.41M13.88,11.47L11.75,9.34L13.14,7.95L15.64,10.45L13.88,11.47Z"/></svg>`;
            const heightStyle =
              shape === "circle" || shape === "stamp-double"
                ? `height: ${w}px !important;`
                : h
                ? `height: ${h}px !important;`
                : `min-height: ${Math.max(
                    40,
                    Math.round(w * 0.7)
                  )}px !important;`;

              
            const noImgPlaceholder = `<span class="hf-no-image-placeholder shape-${shape}" style="width: ${w}px !important; ${heightStyle} max-width: 100% !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; vertical-align: middle !important; margin: 3px !important; box-sizing: border-box !important; ${shapeCSS}" title="${
              v.label || "صورة"
            } — لا توجد صورة">${noImgSvg}</span>`;



          

            if (imgSrc) {
              
              const hiddenFallback =  `<span class="hf-no-image-placeholder shape-${shape}" style="display: none !important; width: ${w}px !important; ${heightStyle} max-width: 100% !important; align-items: center !important; justify-content: center !important; background: #f1f5f9 !important; border: 1.5px dashed #cbd5e1 !important; vertical-align: middle !important; margin: 3px !important; box-sizing: border-box !important; ${shapeCSS}" title="${
                v.label || "صورة"
              } — لا توجد صورة">${noImgSvg}</span>`;
              const imgHeight =
                shape === "circle" || shape === "stamp-double"
                  ? `${w}px`
                  : h
                  ? `${h}px`
                  : fit === "cover" || fit === "fill"
                  ? `${Math.max(40, Math.round(w * 0.75))}px`
                  : "auto";
              return `<img src="${imgSrc}" class="shape-${shape}" alt="${
                v.label || "صورة"
              }" style="width: ${w}px !important; max-width: 100% !important; height: ${imgHeight} !important; vertical-align: middle; display: inline-block; margin: 3px; box-sizing: border-box; ${shapeCSS}" onerror="this.style.display='none';if(this.nextElementSibling)this.nextElementSibling.style.setProperty('display','inline-flex','important');" />${hiddenFallback}`;
            } else {
              
              
              return noImgPlaceholder;
            }
          });
        } else {

          let textVal =
            customValue !== undefined
              ? customValue
              : v.value_ar !== undefined
              ? v.value_ar
              : v.value || v.value_en || "";

              const profile = state?.profile                  

              switch(v.name_code){
                case "userName":        

                  textVal = (profile?.first_name || "اسم المستخدم" )+ " " + (profile.last_name??"")
                  break;
                case "userEmail":
                  textVal =  profile.email || "email"
                  break;

                case "date":
                  textVal = new Date().toLocaleDateString("ar-SA")
                  break;
                case "time":
                  textVal = new Date().toLocaleTimeString("ar-SA", {
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: true,
                  })
                  break;
                  case "pageTitle":                 
                    const router = getRouter();                    
                    textVal =  router?.currentRoute?.value?.meta?.name_ar ?? "عنوان الصفحة";
                    break;
                  default:
                    break;
                  
              }
         
        

          result = result.replace(tokenRegex, textVal);
        }
      });

      return result;
    };

    const buildSectionHTML = (section) => {
      const colWidth = Math.floor(100 / section.columns);
   
      if(!section.cells) return ''
      const colsHTML = section.cells
        .map((cell) => {
          const s = cell.style;
          const fontSizeVal = parseInt(s.fontSize || 14);
          const cssStyle = [
            `font-size: ${fontSizeVal}px !important`,
            `font-family: ${s.fontFamily || "Tajawal"} !important`,
            `font-weight: ${s.fontWeight} !important`,
            `font-style: ${s.fontStyle} !important`,
            `text-decoration: ${s.textDecoration} !important`,
            `color: ${s.color} !important`,
            `text-align: ${s.textAlign} !important`,
            `background-color: ${
              s.backgroundColor === "transparent"
                ? "transparent"
                : s.backgroundColor
            } !important`,
            `width: ${colWidth}% !important`,
            "padding: 8px",
            "display: inline-block",
            "vertical-align: middle",
            "box-sizing: border-box",
            "white-space: pre-wrap !important",
            "word-break: break-word !important",
          ].join("; ");
          return `<span style="${cssStyle}">${resolveVars(
            cell.content
          )}</span>`;
        })
        .join("");

      const borderStyle = section.borderBottom
        ? "border-bottom: 1px solid #dee2e6;"
        : "";
      const borderTopStyle = section.borderTop
        ? "border-top: 1px solid #dee2e6;"
        : "";
      const sectionStyle = [
        `background-color: ${section.backgroundColor}`,
        `min-height: ${section.height}px`,
        "width: 100%",
        "display: block",
        "box-sizing: border-box",
        borderStyle,
        borderTopStyle,
      ]
        .filter(Boolean)
        .join("; ");

      return `<div style="${sectionStyle}">${colsHTML}</div>`;
    };

 
    const header =  typeof tpl.header === 'object' ? tpl.header : ""
    const footer =  typeof tpl.footer === 'object' ? tpl.footer : ""

 

    

    return {
      header: tpl.header ?buildSectionHTML(tpl.header):"",
      footer:tpl.footer? buildSectionHTML(tpl.footer):"",
    };
  };

  const generateHTML = (templateId, sampleData = {}) => {
    const tpl = findTemplate(templateId);
    return generateHTMLForTemplate(tpl, sampleData);
  };

  return reactive({
    templates,
    activeTemplateId,
    activeTemplate,
    draftTemplate,
    staticVariables,
    apiVariables,
    variable,
    allVariables,
    apiLoading,
    apiError,
    apiLoaded,

    fetchApiVariables,
    fetchTemplatesFromApi,
    saveTemplateToApi,
    updateTemplateInApi,
    clearTemplates,
    createTemplate,
    duplicateTemplate,
    deleteTemplate,
    setActiveTemplate,
    setHeaderColumns,
    setFooterColumns,
    updateCellContent,
    updateCellStyle,
    updateSectionStyle,
    generateHTML,
    generateHTMLForTemplate,
    startNewTemplateDraft,
    commitDraftTemplate,
    cancelDraftTemplate,
    startEditTemplate,
    commitEditTemplate,
    cancelEditTemplate,
  });
}

// Composable Alias
export const useCustomHeaderFooterStore = useCustomHeaderFooter;
