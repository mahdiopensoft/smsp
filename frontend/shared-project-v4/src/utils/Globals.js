import { state } from "@/../src/store/state";
import { primaryStore } from "../../store/state";
import i18n from "@/plugins/i18n";
import logoo from "@/assets/logo.png";
import ExcelJS from "exceljs";
import { saveAs } from "file-saver";
import api from "../../plugins/axios-plugin";
import settings from "@/../settings";
 import { useAuthStore } from "../UserManagement/stores/auth";


// import * as XLSX from "xlsx";
// import ValueValidationPlugin from "./validation.js";

export function showSnackBar() {
  state.snackbar = true;
}

export const alert = (
  type,
  data = {
    title: "",
    message: "",
    icon: "",
    icon_color: "",
    sub_message: "",
    component: "",
  }
) => {
  // Default configurations for alerts
  const defaults = {
    success: {
      icon_color: "success",
      icon: "check-circle",
      title:
        i18n.global.locale == "ar"
          ? "تمت العملية بنجاح"
          : "The operation was completed successfully",
    },
    add: {
      icon_color: "success",
      icon: "check-circle",
      title:
        i18n.global.locale == "ar"
          ? "تمت العملية بنجاح"
          : "The operation was completed successfully",
      message:
        i18n.global.locale == "ar"
          ? "تم إضافة البيانات بنجاح"
          : "Data added successfully",
    },
    update: {
      icon_color: "success",
      icon: "check-circle",
      title:
        i18n.global.locale == "ar"
          ? "تمت العملية بنجاح"
          : "The operation was completed successfully",
      message:
        i18n.global.locale == "ar"
          ? "تم تعديل البيانات بنجاح"
          : "The data has been modified successfully",
    },
    errorData: {
      icon_color: "error",
      icon: "cancel",
      title: i18n.global.locale == "ar" ? "فشل" : "Failure",
      message:
        i18n.global.locale == "ar" ? "خطاء في البيانات" : "Error in data",
    },
    dublicateData: {
      icon_color: "error",
      icon: "cancel",
      title: i18n.global.locale == "ar" ? "فشل" : "Failure",
      message:
        i18n.global.locale == "ar" ? "البيانات مكررة" : "Data is duplicated",
    },
    empty: {
      icon_color: "green",
      icon: "message-alert-outline",
      message: i18n.global.locale == "ar" ? "لايوجد بيانات" : "No Data",
    },
    del: {
      icon_color: "success",
      icon: "check-circle",
      title:
        i18n.global.locale == "ar"
          ? "تمت العملية بنجاح"
          : "The operation was completed successfully",
      message:
        i18n.global.locale == "ar"
          ? "تم حذف البيانات بنجاح"
          : "The data has been deleted successfully",
    },
    info: {
      icon_color: "blue",
      icon: "information-outline",
      title: i18n.global.locale == "ar" ? "معلومة" : "Information",
      message: "",
    },
    notFound: {
      icon_color: "error",
      icon: "cancel",
      title: i18n.global.locale == "ar" ? "فشل" : "Failure",
      message:
        i18n.global.locale == "ar" ? "المسار غير موجود" : "path not exist",
    },
  };

  const defaultData = defaults[type] || {};

  // Update state with provided or default values
  state.alert_details.alert_icon_color =
    data.icon_color || defaultData.icon_color;
  state.alert_details.alert_icon = data.icon || defaultData.icon;
  state.alert_details.alert_title = data.title || defaultData.title;
  state.alert_details.message = data.message || defaultData.message;
  state.alert_details.alert_sub_message = data.sub_message;
  state.alert_details.type = type;
  state.alert_details.component = data.component;

  // Log message for debugging in specific cases
  if ((type === "add" || type === "update") && data.message) {
    // console.log(data.message);
  }
};

export function showAlert(is_closed = true) {
  state.alert = true;
  // if (is_closed) {
  //   // setTimeout(() => {
  //   //   state.alert = false;
  //   // }, 4000);
  // }
}

export const alertProtectedRecords = (items) => {
  state.message_protected_records = items;
  state.protected_records = true;
};

const globalVariable = {
  install(Vue) {
    let profile = state.profile;

    // Project logo
    Vue.config.globalProperties.$logo = profile?.org_logo
      ? settings.url_img + profile?.org_logo
      : logoo;

    // Default parameters
    Vue.config.globalProperties.$params = {
      params: { page: 1, perPage: 10, sort_by: "id", txt_search: "" },
    };

    // Default filters
    Vue.config.globalProperties.$filters = (context, field, value) => {
      return [{ field: field, value: context.$route.params[value || field] }];
    };

    // Alert
    Vue.config.globalProperties.$alert = (type, data) => {
      alert(type, data);
      showAlert();
    };

    // Snackbar
    Vue.config.globalProperties.$snack = (type, data) => {
      alert(type, data);
      showSnackBar();
    };

    // Alert for protected records
    Vue.config.globalProperties.$alertProtectedRecords = (items) => {
      alertProtectedRecords(items);
    };

    // Navigate to another page
    Vue.config.globalProperties.$navigateTo = async function (param) {
 
      const local_breadcrumbs =
        JSON.parse(localStorage.getItem("breadcrumbs")) || [];
 
      local_breadcrumbs.push({
        name: param.name,
        title: param.ar,
        title_en: param.en,
        icon: param.icon,
      });
      localStorage.setItem("breadcrumbs", JSON.stringify(local_breadcrumbs));

      if (param.blank) {
        const newTabUrl = this.$router.resolve({
          name: param.name,
          params: param.params,
        });
        const newTab = window.open(newTabUrl.path, "_blank");

        if (!newTab || newTab.closed || typeof newTab.closed === "undefined") {
          alert("", {
            title: i18n.global.t("blocked_window"),
            message: `${i18n.global.t("popup_windows_blocked")} ${i18n.global.t(
              "enabled_popups"
            )}`,
            icon: "window-restore",
          });
          showAlert(false);
        }
      } else {
        this.$router.push({
          name: param.name,
          params: param.params,
          query: param.query,
        });
      }
    };

    // // Refresh autoList
    // Vue.config.globalProperties.$refresh_list = function (context, param) {
    //   setTimeout(() => {
    //     context[param] = false;
    //   }, 500);
    //   context[param] = true;
    // };

    Vue.config.globalProperties.$moveItems = function (
      sourceList = [],
      selectIds = []
    ) {
      var items_2 = [];
      if (sourceList && sourceList.length > 0) {
        sourceList = sourceList.filter((item) => {
          if (selectIds.includes(item.id)) {
            items_2.push(item);
            return false;
          }
          return true;
        });
      }
      return { sourceList, items_2 };
    };

    Vue.config.globalProperties.$mergeItems = function (
      selectArray,
      sourceArray,
      targetArray
    ) {
      selectArray.forEach((item, index_select) => {
        const existsInTarget = targetArray.some((targetItem) =>
          objectsAreEqual(targetItem, item)
        );
        if (!existsInTarget) targetArray.push(item);

        const index = sourceArray.findIndex((obj) =>
          objectsAreEqual(obj, item)
        );

        if (index !== -1) {
          sourceArray.splice(index, 1);
        }
      });
      selectArray.splice(0, selectArray.length);
    };

    Vue.config.globalProperties.$removeItems = function (
      selectArray,
      sourceArray
    ) {
      selectArray.forEach((item, index_select) => {
        const index = sourceArray.findIndex((obj) => {
          return objectsAreEqual(obj, item);
        });
        if (index !== -1) {
          sourceArray.splice(index, 1);
        }
      });
      selectArray.splice(0, selectArray.length);
    };

    // دالة لفورمات حقول الشاشات MrAlt
    Vue.config.globalProperties.$headerFormat = (data) => {
      const formatted = data.map((item) => {
        return {
          title: `this?.$t('${item.name}')`,
          key: item.name,
        };
      });
    };
    // دالة لفورمات حقول الشاشات MrAlt
    Vue.config.globalProperties.$createTrans = (data) => {
      const ar = Object.assign(
        {},
        ...data.map((item) => {
          return {
            [item.name]: item.label_ar,
          };
        })
      );
      const en = Object.assign(
        {},
        ...data.map((item) => {
          return {
            [item.name]: item.label_en,
          };
        })
      );
    };

    Vue.config.globalProperties.$perm = (name, path) => {
      let is_super_user = state.is_super_user;
      if (is_super_user === "true" || is_super_user === true) {
        return true;
      } else {
        const object_perm = {
          view: 1,
          add: 2,
          edit: 3,
          delete: 4,
          force_delete: 5,
          export: 6,
          import: 7,
          view_delete: 8,
          restore: 9,
          select: 10,
          log: 11,
          print: 12,
        };

        const obj = state?.permissions[path] || undefined;
        if (obj) {
          const state = obj.find((e) => e == object_perm[name]);

          if (state) return true;
          else return false;
        } else return false;
      }
    };
  },
};

export default globalVariable;

function objectsAreEqual(obj1, obj2) {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
}

function deepEqual(obj1, obj2) {
  if (obj1 === obj2) return true;
  if (
    typeof obj1 !== "object" ||
    obj1 === null ||
    typeof obj2 !== "object" ||
    obj2 === null
  )
    return false;

  const keys1 = Object.keys(obj1);
  const keys2 = Object.keys(obj2);
  if (keys1.length !== keys2.length) return false;

  for (let key of keys1) {
    if (!keys2.includes(obj1[key])) return false;
    if (!deepEqual(obj1[key], obj2[key])) return false;
  }
  return true;
}
export function printReport(print) {
  state.print = true;
  setTimeout(() => {
    let printContent = document.querySelector(`#${print}`).innerHTML;
    document.getElementById("printView").style.display = "block";
    document.getElementById("printView").innerHTML = printContent;
    document.getElementById("appViewId").style.display = "none";
    window.print();
    document.getElementById("printView").innerHTML = "";
    document.getElementById("printView").style.display = "none";
    document.getElementById("appViewId").style.display = "block";
    document.getElementById("appViewId").style.fontSize = "5px";
    state.print = false;
  }, 10);
}

// routes / index
export function controlRoutes(to, next) {
  
  var local_breadcrumbs = JSON.parse(localStorage.getItem("breadcrumbs"));
  var length = to.matched.length;

  if (local_breadcrumbs) {
    if (length <= 2) localStorage.removeItem("breadcrumbs");
    else {
      local_breadcrumbs.length = length - 2;
      localStorage.setItem("breadcrumbs", JSON.stringify(local_breadcrumbs));
    }
  }
  next();
}
//فحص التوكن
export function checkAuth() {
  const authStore = useAuthStore();
  return authStore.isAuthenticated;

  // const token = localStorage.getItem("token") || null;
  // const decoded = token ? jwtDecode(token) : null;

  // if (decoded != null) {
  //   if (Date.now() >= decoded.exp * 1000) {
  //     logOut();
  //     return false;
  //   }
  //   return true;
  // } else {
  //   return false;
  // }
}

export async function logOut(status = true) {
  localStorage.removeItem("token");
  state.isAuthenticated = false;
  if (status) window.location.reload();
}

// التصدير الى اكسل
export const ExportToExcel = function (header, data, name = "ملف") {
  return new Promise((resolve, reject) => {
    try {
      const today = new Date();
      const options = { year: "numeric", month: "2-digit", day: "2-digit" };
      const dateString = today
        .toLocaleDateString("en-US", options)
        .replace(/\//g, "-");
      const style = {
        font: {
          bold: true,
          color: { argb: "FFFFFF" },
        },
        fill: {
          type: "pattern",
          pattern: "solid",
          fgColor: { argb: "2F75B5" },
        },
      };
      const workbook = new ExcelJS.Workbook();
      const worksheet = workbook.addWorksheet("Data");
      worksheet.views = [{ rightToLeft: true }];
      worksheet.columns = header;
      const row = worksheet.getRow(1);
      row.eachCell((cell) => {
        cell.style = style;
        cell.alignment = { horizontal: "right", vertical: "middle" };
      });
      worksheet.addRows(data);
      worksheet.eachRow((row) => {
        row.values.forEach((value, col) => {
          const column = worksheet.getColumn(col);
          const cell = value ? value.length : 0;

          if (cell > column.width) {
            column.width = cell + 2;
          }
        });
        row.eachCell((cell) => {
          cell.alignment = { horizontal: "right", vertical: "right" };
          cell.border = {
            top: { style: "thin" },
            left: { style: "thin" },
            right: { style: "thin" },
            bottom: { style: "thin" },
          };
        });
      });

      const file_name = prompt(
        i18n.global.t("enter_file_name"),
        `${name}-${dateString}`
      );
      if (file_name) {
        workbook.xlsx.writeBuffer().then((buffer) => {
          const data = new Blob([buffer], { type: "application/octet-stream" });
          saveAs(data, file_name + ".xlsx");
        });
        resolve();
      }
    } catch (error) {
      reject(error);
    }
  });
};

export const convertToObject = function (items) {
  const result = {};
  Object.entries(items).forEach(([key, value]) => {
    try {
      const keys = key.split("__");
      let current = result;
      keys.forEach((k, index) => {
        if (index === keys.length - 1) current[k] = value;
        else {
          current[k] = current[k] || {};
          current = current[k];
        }
      });
    } catch (e) {}
  });

  return result;
};

export const convertFromObject = function (
  nestedObj,
  parentKey = "",
  result = {}
) {
  for (let key in nestedObj) {
    if (nestedObj.hasOwnProperty(key)) {
      const newKey = parentKey ? `${parentKey}__${key}` : key;
      if (
        typeof nestedObj[key] === "object" &&
        nestedObj[key] &&
        !Array.isArray(nestedObj[key])
      ) {
        convertFromObject(nestedObj[key], newKey, result);
      } else {
        result[newKey] = nestedObj[key];
      }
    }
  }

  return result;
};

export const getData = async function (
  data = {
    path: "",
    params: {},
    data: undefined,
    filters: undefined,
    re_path: false,
  }
) {
  var token = localStorage.getItem("token") || null;
  if (data.re_path === true) return data.path;
  if (!data.filters) {
    const response = await api(settings.url + data.path, {
      params: {
        ...data.params,
      },
      headers: {
        Authorization: token ? `Bearer ${token}` : null,
      },
    })
      .then((e) => {
        if (data.data)
          return data.data.reduce(
            (acc, key) => {
              return acc[key];
            },
            e,
            data.data || e.data
          );
        else return e?.data?.data || e.data;
      })
      .catch((error) => {
        if (error?.response?.status === 403) {
     
          if (
            error.response?.data?.detail ===
            "ليس لديك صلاحية للقيام بهذا الإجراء."
          ) {
            return "notPermitted";
          }
        }

        return "error";
      });
    return response;
  } else {
    const filters = {
      filters: data.filters,
    };

    const response = await api
      .post(settings.url + data.path, filters, {
        headers: {
          Authorization: token ? `Bearer ${token}` : null,
        },
      })
      .then((e) => {
        if (data.data)
          return data.data.reduce((acc, key) => acc[key], e?.data?.data);
        else return e?.data?.data || e.data;
      })
      .catch((error) => {
        if (error?.response?.status === 403) {
           
          if (
            error.response?.data?.detail ===
            "ليس لديك صلاحية للقيام بهذا الإجراء."
          ) {
            return "notPermitted";
          }
        }
        return "error";
      });
    return response;
  }
};



export const changeKeyScreen = function () {
  
  primaryStore.keySreen += 1;
 };
