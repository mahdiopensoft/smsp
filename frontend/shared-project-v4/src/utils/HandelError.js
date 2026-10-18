// add by samer
// axios-plugins file

import { alertProtectedRecords, alert, showAlert } from "./Globals";

function relatedObjects(list) {
  return list;
}

export const HandelError = function (error) {
  if(error.code === 'ERR_CANCELED'){
  
    alert("errorData", { message: 'تم الغاء الطلب' });
    showAlert();
    return
  }
 else if (error.status == 409 || error.status == 418) {
    let error_messages = [];

    const method = error?.config?.method;

    if (method === "post" || method === "put" || method === "patch") {
      var message = error?.response?.data || error?.response;
      alert("errorData", { message: message });
      showAlert();
      return;
    }

    error_messages = relatedObjects(error?.response?.data);

    alertProtectedRecords(error_messages);
  } else if (error.status === 404) {
    alert("errorData", {
      message: ` المسار - ${error?.request?.responseURL} - غير صحيح`,
    });
    showAlert();
  } else {
    var message = error?.response?.data;

    alert("errorData", { message: message });
    showAlert();
  }
};
