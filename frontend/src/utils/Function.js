
import setting from "@/../settings";
import { state } from "@/store/state";
import shared from "external-components";
export const getProfile = async function () {
  await shared.api(setting.url + "user-manager/profile/").then((e) => {

    const response = e.data.data ?? e.data
    state.organization_id = response.ip;
    state.is_super_user = response.ib;
    state.is_manager = response?.iv

    let profile = {};
    profile.first_name = response.first_name;
    profile.last_name = response.last_name;
    profile.username = response.username;
    profile.image_user = response.image_user;
    profile.org_logo = response.org_logo;
    profile.ip = response.ip;
    profile.zi = response.zi;
    profile.is_manager = response?.iv
    state.profile = profile;

    let data = {};
    if (Array.isArray(response.permissions)){
      response.permissions.forEach((element) => {
        if (!data[element.route]) data[element.route] = [];

        data[element.route].push(element.operation_type);
      });

    state.permissions = data;
    }
  });
};
export const fix_image_url = (url) => {
  if (url.includes('http')) {
    url = url.replace(/:\/\/\/+/, '://')
    const [http, rem] = url.split(/:\/\//)
    return `${http}://${rem.replace(/\/+/, '/')}`
  }
  return url.replace(/\/+/, '/')
}

export const fix_branch_field = (field, data) => {
  return Object?.assign(data, { [field]: data[field] ?? null })
}

