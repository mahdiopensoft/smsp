import settings from "@/../settings";

import CustomRouter from "../components/CustomRouter.vue";
import InitializationView from "../page/InitializationScreen/InitializationView.vue";
import api from "../../plugins/axios-plugin";
import { primaryStore } from "../../store/state";

export default async function dynamicRoutes(modules=[]) {

 
   
  const pages = import.meta.glob("../page/**/*.vue");
 
  const userPage = import.meta.glob("../UserManagement/**/*.vue");
  const chatPage = import.meta.glob("../../chating/pages/**/*.vue");
  
  const allPages = { ...modules, ...pages,...userPage, ...chatPage  };
  // const allPages = { ...modules, ...pages,...userPage };
 
  let page = {};

  await Promise.all(
    Object.entries(allPages).map(async ([filePath, resolver]) => {
      const fileName = filePath
        .split("/")
        .pop()
        .replace(/\.\w+$/, "");

      const component = await resolver();

      page[fileName] = component.default;
    })
  );

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
      primaryStore.notes_screen[item.route] = {};
      if (!primaryStore.notes_screen[item.route])
        primaryStore.notes_screen[item.route] = {};
        
      primaryStore.notes_screen[item.route].notes = item.json_notes;
    }
    if (item.json_notes) {
      if (!primaryStore.notes_screen[item.route])
        primaryStore.notes_screen[item.route] = {};
        
      primaryStore.notes_screen[item.route].functions = item.screen_functions;
    }
    // محاولة جلب الكمبوننت المسجّل، أو الوقوع إلى DashBoard
    const component = page[item.component] ?? page.DashBoard;
    let path = item.path || item.route;
    if (settings.multiple_company) {
      // إذا كان هناك مسار متعدد الشركات، نضيف الشركة إلى المسار
      path = `/:company/${path}`;
    }

    // بيانات أساسية للمسار
    const route = {
      path: path,
      name: item.route,
      type_of_screen: item.type_of_screen,
      meta: {
        requiresAuth: true,
        system: item.fk_default_system,
        json_notes: item.json_notes,
      },
    };

    // بناء المسارات الفرعية بشكلٍ متكرر
    const children = buildNestedRoutes(items, item.id);

    if (children.length) {
      // إذا كان هناك مسارات فرعية
      return {
        ...route,
        component: CustomRouter,
        children,

        props: {
          component,
          name_ar: item.name_ar,
          name_en: item.name_en,
          name_path: item.route,
          id: item.id,
        },
        meta: {
          requiresAuth: true,
          system: item.fk_default_system,
          json_notes: item.json_notes,
          fk_print_report_setting_id: item.fk_print_report_setting_id,
          fk_screen: item.id,
          name_ar: item?.name_ar,
          name_en: item?.name_en,
        },
      };
    }

    // مسار نهائي (بدون أطفال)
    // حالة خاصة: لا يوجد component لكن يوجد back_end_link
    if (!item.component && item.back_end_link) {
      return {
        ...route,
        component: CustomRouter,
        props: {
          component: InitializationView,
          name_ar: item.name_ar,
          name_en: item.name_en,
          url: item.back_end_link,
          route: item.route,
          name_path: item.route,
          id: item.id,
        },
        meta: {
          route: item.route,
          name_path: item.route,
          url: item.back_end_link,
          requiresAuth: true,
          system: item.fk_default_system,
          json_notes: item.json_notes,
          fk_screen: item.id,
          name_ar: item?.name_ar,
          name_en: item?.name_en,
        },
      };
    }

    // الحالة الافتراضية: مسار مباشر إلى الكمبوننت
    return {
      ...route,
      component,
      props: {
        name_ar: item.name_ar,
        name_en: item.name_en,
      },
      meta: {
        requiresAuth: true,
        system: item.fk_default_system,
        json_notes: item.json_notes,
        fk_screen: item.id,
        name_ar: item?.name_ar,
        name_en: item?.name_en,
      },
    };
  }

  // حذف ال القيم الفارقة من route
  // routes
  function removeNullPathNodes(data) {
    return data.flatMap((item) => {
      if (item.path === null && item.children) {
        return removeNullPathNodes(item.children);
      } else if (item.path === null) return [];
      else if (item.children)
        return { ...item, children: removeNullPathNodes(item.children) };
      else return item;
    });
  }

  async function fetchRotes() {
     
    
 
    const response = api(`${settings.url_sidbar}screens/screen/list/?t=${Date.now()}`)
    .then((response) => {
 
      const data = response?.data?.data || response.data;
      primaryStore.addedRoutes = data
       
      return buildNestedRoutes(data);
      })
      .catch(() => {
        return [];
      });

    return response;
  }

  const routers = await fetchRotes();
 

  if (routers.length === 0) {
    return [];
  }
 
  return removeNullPathNodes(routers);
}
