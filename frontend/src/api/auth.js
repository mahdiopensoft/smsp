import shared from "external-components";
import settings from "../../settings";

const API_LOGIN = settings.url + "user-manager/token/";

export function login(username, password) {
  return shared.api.post(
    API_LOGIN,

    {
      username: username,
      password: password,
    },
    {
      skipInterceptor: true,
    }
  );
}
