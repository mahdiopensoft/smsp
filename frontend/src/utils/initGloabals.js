import moment from "moment";
import cloneDeep from "lodash/cloneDeep";
import dataList from "@/utils/DataAutoList";
import { useDisplay } from "vuetify";
import { isRef, unref } from "vue";
import setting from "@/../settings";
import shared from "external-components";
import { state } from "@/store/state";

//variables
import { globals } from "@/utils/variable";

export function makeGlobals(app) {
  app.config.globalProperties.$moment = moment;

  app.config.globalProperties.$cloneDeep = cloneDeep;

  // Enhance $filters to support dynamic route parameter formats (:id, :fk_..., ?id=)
  app.config.globalProperties.$filters = (context, field, value) => {
    const val =
      context?.$route?.params?.[value || field] ??
      context?.$route?.params?.id ??
      context?.$route?.query?.[value || field] ??
      context?.$route?.query?.id;
    return val !== undefined && val !== null && val !== ""
      ? [{ field: field, value: !isNaN(Number(val)) && typeof val !== "boolean" ? Number(val) : val }]
      : [];
  };

  function reactiveUnwrapRefs(obj) {
    return new Proxy(obj, {
      get(target, prop) {
        const val = target[prop];
        return isRef(val) ? val.value : val;
      },
    });
  }

  Object.defineProperty(app.config.globalProperties, "$display", {
    get() {
      const use_display = useDisplay();
      return reactiveUnwrapRefs(use_display);
    },
  });

  app.config.globalProperties.$mainCurrency = async function () {
    const main_currency = await dataList().MainCurrency.method();
    return main_currency;
  };

  app.config.globalProperties.$onlyPositive = (value) => {
    if (value < 0) {
      value = 0;
      return Number(value);
    } else {
      return Number(value);
    }
  };

  app.config.globalProperties.$discount = (value, percent) => {
    if (value && percent) {
      return value * (percent / 100);
    }
  };

  app.config.globalProperties.$percentage = (value) => {
    if (value > 100) {
      value = 100;
      return Number(value);
    } else {
      return Number(value || 0);
    }
  };

  const current_date = moment().format("YYYY-MM-DD");
  app.config.globalProperties.DDate = current_date;

  app.config.globalProperties.$endOfMonth = (
    added = 0,
    date = current_date
  ) => {
    return moment(date, "YYYY-MM-DD")
      .add(added, "month")
      .endOf("month")
      .format("YYYY-MM-DD");
  };

  app.config.globalProperties.$addToDate = (
    added,
    section = "days",
    date = current_date
  ) => {
    return moment(date, "YYYY-MM-DD").add(added, section).format("YYYY-MM-DD");
  };

  // دالة لفورمات حقول الشاشات MrAlt
  app.config.globalProperties.headerFormat = (data) => {
    const formatted = data.map((item) => {
      return {
        title: `this?.$t('${item.name}')`,
        key: item.name,
      };
    });
    console.log(JSON.stringify(formatted));
  };

  // دالة لفورمات حقول جدول custom date table with save MrAlt
  app.config.globalProperties.dHeaderFormat = (data) => {
    const formatted = data.map((item) => {
      return {
        title: `this?.$t('${item.name}')`,
        key: item.name,
        field: { ...item },
      };
    });
    console.log(JSON.stringify(formatted));
  };

  // دالة بناء بناء شكل الشجرة MrAlt
  app.config.globalProperties.$buildTree = function (items, parent_id = null) {
    const data = items
      .filter((item) => item.fk_parent == parent_id)
      .map((item) => ({
        ...item,
        children: this.$buildTree(items, item.id),
        name_en: item.name_en ?? item.name_ar,
      }));
    return data.length > 0 ? data : undefined;
  };

  // دالة ترتيب بيانات الشجرة MrAlt
  app.config.globalProperties.$sortTreeData = function (tree_data) {
    var sortedParents = [];
    if (typeof tree_data == "Array") {
      sortedParents = [...tree_data];
    } else {
      sortedParents = [];
    }
    // console.log(sortedParents);
    sortedParents.sort((a, b) => {
      const aHasChildren = !!a.children?.length;
      const bHasChildren = !!b.children?.length;

      if (!aHasChildren && bHasChildren) return -1;
      if (aHasChildren && !bHasChildren) return 1;

      return 0;
    });
    const sorted = sortedParents.map((parent) => {
      const sortedParent = { ...parent };
      if (sortedParent.children) {
        sortedParent.children = [...sortedParent.children].sort((a, b) => {
          return a.sequence - b.sequence;
        });
      }
      return sortedParent;
    });
    return sorted?.length > 0 ? JSON.parse(JSON.stringify(sorted)) : tree_data;
  };

  app.config.globalProperties.$formatNumber = function (number) {
    if (number && number != "0.00") {
      number = String(number)?.replace(/[^0-9.-]/g, "");

      return new Intl.NumberFormat("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(Number(number));
    } else {
      return "0.00";
    }
  };

  for (const key in globals) {
    if (Object.hasOwnProperty.call(globals, key)) {
      app.config.globalProperties[`${key}`] = globals[key];
    }
  }

  app.config.globalProperties.$get_timeline = async () => {
    if (state.profile.zi == 50) {
      await shared
        .api(setting.url + "school/branch-month/get-time-line/")
        .then((e) => {
          app.config.globalProperties.$time_obj = e.data.data;
        });
    } else if ([20, 30, 40].includes(state.profile.zi)) {
      await shared
        .api(setting.url + "system-management/year-of-study/get-time-line/")
        .then((e) => {
          app.config.globalProperties.$time_obj = e.data.data;
        });
    } else {
      app.config.globalProperties.$time_obj = null;
    }
  };
  //داله جلب تاريخ اليوم
  app.config.globalProperties.$today = () => {
    return new Date().toISOString().split("T")[0];
  };
}
