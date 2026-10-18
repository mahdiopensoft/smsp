import { getData } from "./Globals";

export default function (param) {
  return {
    parent_screen: {
      label: "parent_screen",
      icon: "account-box",
      method: () =>
        getData({
          path: "screens/screen/all/",
        }),
    },
    UserTypeForManager: {
      label: "user_type",
      icon: "account-circle",
      method: () =>
        getData({
          path: "user-manager/user-type/for-manager/",
        }),
      title: "name_ar",
    },

    CompanyLevelChoices: {
      label: "level",
      icon: "layers",
      method: () =>
        getData({
          path: "choices/CompanyLevelChoices/",
        }),
    },

    add_to_level: {
      label: "branch",
      icon: "sitemap",
      method: (re_path) =>
        param || re_path
          ? getData({
              path: "common/branch/filter/",
              filters: [
                {
                  field: "company_level",
                  value: param,
                },
              ],
              re_path,
            })
          : [],

      title: "name_ar",
    },

    Groupes: {
      label: "group",
      icon: "account-group",
      method: () =>
        getData({
          path: "user-manager/groups/all/",
        }),
      title: "name",
    },

    UserType: {
      label: "user_type",
      icon: "account-circle",
      method: () =>
        getData({
          path: "user-manager/user-type/all/",
        }),
      title: "name_ar",
    },
    GroupesForManager: {
      label: "group",
      icon: "account-group",
      method: () =>
        param
          ? getData({
              path: `user-manager/groups/for-manager/?company_level=${param.company_level}&fk_user_type=${param.fk_user_type}`,
            })
          : [],
      title: "name",
    },
    GroupesForManager: {
      label: "group",
      icon: "account-group",
      method: () =>
        param
          ? getData({
              path: `user-manager/groups/for-manager/?company_level=${param.company_level}&fk_user_type=${param.fk_user_type}`,
            })
          : [],
      title: "name",
    },

    CompanyLevelFilterChoices: {
      label: "level",
      icon: "layers",
      method: () =>
        getData({ path: "choices/CompanyLevelChoices/" }).then((e) => {
          if (param.isEdit)
            return e.filter((f) => f.id >= param.company_level && f.id != 10);
          else return e.filter((f) => f.id > param.company_level && f.id != 10);
        }),
    },
    Country: {
      label: "country",
      icon: "flag-outline",
      method: () =>
        getData({
          path: "common/country/all/",
        }),
      title: "name_ar",
    },

    Governorate: {
      label: "governoratename",
      icon: "city",
      method: (re_path) =>
        param || re_path
          ? getData({
              path: "common/governorate/filter/",
              filters: [
                {
                  field: "fk_country",
                  value: param,
                },
              ],
              re_path,
            })
          : [],

      title: "name",
    },

    Directorate: {
      label: "directoratename",
      icon: "map-outline",
      method: (re_path) =>
        param || re_path
          ? getData({
              path: "common/directorate/filter/",
              filters: [
                {
                  field: "fk_governorate",
                  value: param,
                },
              ],
              re_path,
            })
          : [],

      title: "name_ar",
    },

    Region: {
      label: "region",
      icon: "map-marker-outline",
      method: (re_path) =>
        param || re_path
          ? getData({
              path: "common/region/filter/",
              filters: [
                {
                  field: "fk_directorate",
                  value: param,
                },
              ],
              re_path,
            })
          : [],
      title: "name_ar",
    },
    ContactTypeChoices: {
      label: "",
      icon: "account-box",
      method: () =>
        getData({
          path: "choices/ContactTypeChoices/",
        }),
    },
    BranchTypeChoice: {
      label: "branch_type",
      icon: "office-building",
      method: () =>
        getData({
          path: "choices/BranchTypeChoice/",
        }),
    },
    BranchByCompanyLevel: {
      label: "branch",
      icon: "sitemap",
      method: () =>
        param
          ? getData({
              path: "common/branch/filter/",
              filters: [
                {
                  field: "company_level",
                  value: param,
                },
              ],
            })
          : [],
      title: "name_ar",
    },
    TypeOfMainSystemChoices: {
      label: "",
      icon: "cogs",
      method: () =>
        param
          ? getData({
              path: "choices/TypeOfMainSystemChoices/",
            }).then((e) => {
              if (param < 50)
                return e.filter(
                  (f) =>
                    f.id == "access-login-role-unified-educational-platform"
                );
              else
                return e.filter(
                  (f) =>
                    f.id == "access-login-role-university-management-system" ||
                    f.id == "access-login-role-school" ||
                    f.id == "access-login-role-institute"
                );
            })
          : [],
    },
    ScreenTypeChoices: {
      label: "نوع الشاشة",
      icon: "list",
      method: () =>
        getData({
          path: "choices/ScreenTypeChoices/",
        }),
    },
    TypeOfDisplayChoices: {
      label: "service_status",
      icon: "numerc",
      method: () =>
        getData({
          path: "choices/TypeOfDisplayChoices/",
        }),
    },
    system: {
      label: "system",
      icon: "application-cog-outline",
      method: () =>
        getData({
          path: "screens/systems/all/",
        }),

      title: "name_ar",
    },

    ObjectTypeChoices: {
      label: "entity_type",
      icon: "application-cog-outline",
      method: () =>
        getData({
          path: "choices/ObjectTypeChoices/",
        }),
    },
    StudentTypeChoice: {
      label: "student_type",
      icon: "account",
      method: () =>
        getData({
          path: "choices/StudentTypeChoice/",
        }),
    },
    VariableHeaderFooter: {
      label: "header_footer",
      icon: "layers",
      method: () =>
        getData({
          path: "common/print-report-setting/all/",
        }),
    },
    ActionFlagChoices: {
      label: "operation",
      icon: "fraction-one-half",
      method: () =>
        getData({
          path: "choices/ActionFlagChoices/",
        }),
    },
    OrganizationByLevel: {
      label: "organization",
      icon: "sitemap",
      method: () =>
        getData({
          path: "common/branch/filter/",
          filters: [{ field: "company_level", value: param }],
        }),
      title: "name_ar",
    },
    statusSync: {
      label: "sync_status",
      icon: "sync",
      method: () =>
        getData({
          path: "sync/status/choices/",
        }),
      title: "label",
      value: "value",
    },
    ScreenSync: {
      label: "screens",
      icon: "layout",
      method: () =>
        getData({
          path: "sync/status/screens/",
        }),
     
    },
    OperationTypeChoices: {
      label: "",
      icon: "layers",
      method: () =>
        getData({
          path: "choices/OperationTypeChoices/",
        }),
    },
    System: {
      label: "system",
      icon: "account-box",
      method: () =>
        getData({
          path: "screens/systems/all/",
        }),

      title: "name_ar",
    },
    screen_by_system: {
      label: "parent_screen",
      icon: "account-box",
      method: () =>
        param
          ? getData({
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
    permissionsByScreen: {
      label: "screen_permissions",
      icon: "account-group",
      method: () =>
        param
          ? getData({
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
  };
}
