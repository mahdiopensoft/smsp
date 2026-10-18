import { defineAsyncComponent, h } from "vue";
import settings from "@/../settings";
import CustomRouter from "../components/CustomRouter.vue";
import InitializationView from "../page/InitializationScreen/InitializationView.vue";
import api from "../../plugins/axios-plugin";
import { primaryStore } from "../../store/state";

const pageLoadingComponent = {
  template: `<div style="display:flex;align-items:center;justify-content:center;height:200px;opacity:5;">
  <span>جاري التحميل .......</span>
  </div>`,
};

const pageErrorComponent = {
  template: `<div style="display:flex;align-items:center;justify-content:center;height:200px;color:red;">
  <span>فشل تحميل الصفحة . يرحى تحديث المتصفح</span>
  </div>`,
};

export default async function dynamicRoutes(modules = []) {
  const pages = import.meta.glob("../page/**/*.vue");

  const userPage = import.meta.glob("../UserManagement/**/*.vue");
  const chatPage = import.meta.glob("../../chating/pages/**/*.vue");

  const allPages = { ...modules, ...pages, ...userPage, ...chatPage };
  // const allPages = { ...modules, ...pages,...userPage };

  let page = {};

  for (const [filePath, resolver] of Object.entries(allPages)) {
    const fileName = filePath
      .split("/")
      .pop()
      .replace(/\.\w+$/, "");
    page[fileName] = defineAsyncComponent({
      loader: resolver,
      loadingComponent: pageLoadingComponent,
      errorComponent: pageErrorComponent,
      delay: 200,
      timeout: 15000,
    });
  }

  function buildNestedRoutes(items, parentId = 0) {
    // إذا كنا في الجذر (parentId === 0) ولم توجد عناصر تحمل fk_parent_screen = 0،
    // نعتبر الجذر هو null
    const effectiveParentId =
      parentId === 0 && !items.some((item) => item.fk_parent_screen === 0)
        ? null
        : parentId;

    return items
      .filter((item) => item.fk_parent_screen === effectiveParentId)
      .map((item) => createRoute(item, items));
  }

  function createRoute(item, items) {
    if (item.json_notes) {
      if (!primaryStore.notes_screen[item.route]) {
        primaryStore.notes_screen[item.route] = {};
      }
      primaryStore.notes_screen[item.route].notes = item.json_notes;
      primaryStore.notes_screen[item.route].functions = item.screen_functions;
    }

    // محاولة جلب الكمبوننت المسجّل، أو الوقوع إلى DashBoard
    const component = page[item.component] ?? page.DashBoard;
    let path = item.path || item.route;
    if (settings.multiple_company) {
      // إذا كان هناك مسار متعدد الشركات، نضيف الشركة إلى المسار
      path = `/:company/${path}`;
    }
    const sharedMeta = {
      requiresAuth: true,
      system: item.fk_default_system,
      json_notes: item.json_notes,
      fk_screen: item.id,
      name_ar: item?.name_ar,
      name_en: item?.name_en,
      icon: item?.icon,
    };
    const baseRoute = {
      path,
      name: item.route,
      type_of_screen: item.type_of_screen,
    };


  

    // بناء المسارات الفرعية بشكلٍ متكرر
    const children = buildNestedRoutes(items, item.id);

    if (children.length) {
      // إذا كان هناك مسارات فرعية
      return { 
        ...baseRoute,
        component:CustomRouter,
        children,
        props:{
          component,
          name_ar:item.name_ar,
          name_en:item.name_en,
          name_path:item.route,
          id:item.id
        },
        meta:{
          ...sharedMeta,
          fk_print_report_setting_id:item.fk_print_report_setting_id
        }
      };
    }

    // مسار نهائي (بدون أطفال)
    // حالة خاصة: لا يوجد component لكن يوجد back_end_link
    if (!item.component && item.back_end_link) {
      return { 
        ...baseRoute,
        component:CustomRouter,
   
        props:{
          component:InitializationView,
          name_ar:item.name_ar,
          name_en:item.name_en,
          url:item.back_end_link,
          route:item.route,
          name_path:item.route,
          id:item.id
        },
        meta:{
          ...sharedMeta,
          route:item.route,
          name_path:item.route,
          url:item.back_end_link
        }
      };
    }

    // الحالة الافتراضية: مسار مباشر إلى الكمبوننت
    return {
      ...baseRoute,
      component,
      props:{
        name_ar:item.name_ar,
        name_en:item.name_en,

      },
      meta:sharedMeta
       
    };
  }

  // حذف ال القيم الفارقة من route
  // routes
  function removeNullPathNodes(data) {
    return data.flatMap((item) => {
      if (item.path === null && item.children) {
        return removeNullPathNodes(item.children);
      } 
       if (item.path === null) return [];

       if (item.children)
        return { ...item, children: removeNullPathNodes(item.children) };

       return item;
    });
  }

  async function fetchRotes() {
    return api(`${settings.url_sidbar}screens/screen/list/`)
      .then((response) => {
        const data = response?.data?.data || response.data;
        primaryStore.addedRoutes = data;

        return buildNestedRoutes(data);
      })
      .catch(() => {
        return [];
      });

    
  }

  const routers = await fetchRotes();

  if (routers.length === 0) {
    return [];
  }

  return removeNullPathNodes(routers);
}
