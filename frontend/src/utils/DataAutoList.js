import shared from "external-components";
// import DataAutoListSchool from "./DataAutoListSchool";
import DataAutoListAcademic from "./DataAutoListAcademic";

export default function dataList(param) {
  return {
    ...DataAutoListAcademic(param),
    // ...DataAutoListSchool(param),

    ScreenTypeChoices: {
      label: "نوع الشاشة",
      icon: "list",
      method: () =>
        shared.getData({
          path: "choices/ScreenTypeChoices/",
        }),
    },
    TypeOfDisplayChoices: {
      label: "service_status",
      icon: "numerc",
      method: () =>
        shared.getData({
          path: "choices/TypeOfDisplayChoices/",
        }),
    },

    parent_screen: {
      label: "parent_screen",
      icon: "account-box",
      method: () =>
        shared.getData({
          path: "screens/screen/all/",
        }),
    },
    screen_by_system: {
      label: "parent_screen",
      icon: "account-box",
      method: () =>
        param
          ? shared.getData({
            path: "screens/screen/filter/",
            filters: [
              {
                field: "fk_default_system",
                value: param,
              },
            ],
          })
          : [],
    },
    System: {
      label: "system",
      icon: "account-box",
      method: () => { },
      title: "name_ar",
    },
    GroupesPermissions: {
      label: "group",
      icon: "account-group",
      method: () =>
        shared.getData({
          path: "user-manager/groups/filter/",
          filters: [
            {
              field: "is_active",
              value: true,
            },
          ],
        }),
      title: "name",
    },
    permissionsByScreen: {
      label: "screen_permissions",
      icon: "account-group",
      method: () =>
        param
          ? shared.getData({
            path: "screens/screen-permission/filter/",
            filters: [
              {
                field: "fk_screen",
                value: param,
              },
            ],
          })
          : [],
      title: "operation_type__display",
    },
    system: {
      label: "system",
      icon: "application-cog-outline",
      method: () =>
        shared.getData({
          path: "screens/systems/all/",
        }),

      title: "name_ar",
    },
    testservices: {
      label: "",
      icon: "",
      method: () => [],
      value: "value",
      title: "title",
    },

    // Geographic Locations
    Country: {
      label: "الدولة",
      icon: "earth",
      method: async () => {
        const res = await shared.getData({
          path: "api/common/country/all/",
        });
        if (Array.isArray(res)) return res;
        if (res?.data && Array.isArray(res.data)) return res.data;
        if (res?.results && Array.isArray(res.results)) return res.results;
        // Fallback to non-all path
        const fallback = await shared.getData({ path: "api/common/country/" });
        if (Array.isArray(fallback)) return fallback;
        if (fallback?.data && Array.isArray(fallback.data)) return fallback.data;
        if (fallback?.results && Array.isArray(fallback.results)) return fallback.results;
        return [];
      },
      title: "name_ar",
      value: "id",
    },
    Governorate: {
      label: "المحافظة",
      icon: "map-marker",
      method: async () => {
        if (!param) {
          const res = await shared.getData({ path: "api/common/governorate/all/" });
          if (Array.isArray(res)) return res;
          if (res?.data && Array.isArray(res.data)) return res.data;
          if (res?.results && Array.isArray(res.results)) return res.results;
          return [];
        }
        const res = await shared.getData({
          path: "api/common/governorate/filter/",
          filters: [{ field: "fk_country", value: param }],
        });
        if (Array.isArray(res)) return res;
        if (res?.data && Array.isArray(res.data)) return res.data;
        if (res?.results && Array.isArray(res.results)) return res.results;
        return [];
      },
      title: "name",
      value: "id",
    },
    GovernorateByCountry: {
      label: "المحافظة",
      icon: "map-marker",
      method: async () => {
        if (!param) return [];
        const res = await shared.getData({
          path: "api/common/governorate/filter/",
          filters: [{ field: "fk_country", value: param }],
        });
        if (Array.isArray(res)) return res;
        if (res?.data && Array.isArray(res.data)) return res.data;
        if (res?.results && Array.isArray(res.results)) return res.results;
        return [];
      },
      title: "name",
      value: "id",
    },
    Directorate: {
      label: "المديرية",
      icon: "city",
      method: async (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        if (!raw) return [];
        const govId = (typeof raw === 'object') ? (raw.governorate || raw.governorate_id || raw.fk_governorate || raw.id) : raw;
        if (!govId || govId === '__none__') return [];
        const res = await shared.getData({
          path: "api/common/directorate/filter/",
          filters: [{ field: "fk_governorate", value: govId }],
        });
        let list = [];
        if (Array.isArray(res)) list = res;
        else if (res?.data && Array.isArray(res.data)) list = res.data;
        else if (res?.results && Array.isArray(res.results)) list = res.results;

        return list.map((item) => ({
          ...item,
          name: item.name || item.name_ar || item.name_en || "",
          name_ar: item.name_ar || item.name || "",
        }));
      },
      title: "name",
      value: "id",
    },
    DirectorateByGovernorate: {
      label: "المديرية",
      icon: "city",
      method: async (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        if (!raw) return [];
        const govId = (typeof raw === 'object') ? (raw.governorate || raw.governorate_id || raw.fk_governorate || raw.id) : raw;
        if (!govId || govId === '__none__') return [];
        const res = await shared.getData({
          path: "api/common/directorate/filter/",
          filters: [{ field: "fk_governorate", value: govId }],
        });
        let list = [];
        if (Array.isArray(res)) list = res;
        else if (res?.data && Array.isArray(res.data)) list = res.data;
        else if (res?.results && Array.isArray(res.results)) list = res.results;

        return list.map((item) => ({
          ...item,
          name: item.name || item.name_ar || item.name_en || "",
          name_ar: item.name_ar || item.name || "",
        }));
      },
      title: "name",
      value: "id",
    },
    Region: {
      label: "المنطقة",
      icon: "home-map-marker",
      method: async () => {
        if (!param) {
          const res = await shared.getData({ path: "api/common/region/all/" });
          if (Array.isArray(res)) return res;
          if (res?.data && Array.isArray(res.data)) return res.data;
          if (res?.results && Array.isArray(res.results)) return res.results;
          return [];
        }
        const res = await shared.getData({
          path: "api/common/region/filter/",
          filters: [{ field: "fk_directorate", value: param }],
        });
        if (Array.isArray(res)) return res;
        if (res?.data && Array.isArray(res.data)) return res.data;
        if (res?.results && Array.isArray(res.results)) return res.results;
        return [];
      },
      title: "name",
      value: "id",
    },
    RegionByDirectorate: {
      label: "المنطقة",
      icon: "home-map-marker",
      method: async () => {
        if (!param) return [];
        const res = await shared.getData({
          path: "api/common/region/filter/",
          filters: [{ field: "fk_directorate", value: param }],
        });
        if (Array.isArray(res)) return res;
        if (res?.data && Array.isArray(res.data)) return res.data;
        if (res?.results && Array.isArray(res.results)) return res.results;
        return [];
      },
      title: "name",
      value: "id",
    },
  };
}

// normal
/*
        name: {

          label: "label",
          icon: "icon",
          method: ()=>get Data({path:"path" }),
        },
        */
// with params
/*
          name: {
            label: "label",
            icon: "icon",
            method: ()=>param?  shared.getData({path:"path" ,params:{name_parm:param}}):[],
          },
          */
// with change variabe results
/*
          name: {
            label: "label",
            icon: "icon",
            method: ()=>shared.getData({path:"path"},data:['variable_results_name']}),
          },
          */
// with change  value and title
/*
          name: {
            label: "label",
            icon: "icon",
            method: ()=>shared.getData({path:"path" }),
            value: "id",
            title: "title",
          },
        // with screen add
          /*
          name: {
            label: "label",
            icon: "icon",
            method: ()=>shared.getData({path:"path"}}),
            screen: "name_screen"
          },
          */
