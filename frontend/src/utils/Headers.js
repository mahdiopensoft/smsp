import i18n from "@/plugins/i18n";

const headers = {
  //انواع المؤهلات
  "document-type": [
    { title: i18n.global.t("documentname"), key: "name_ar" },
    { title: i18n.global.t("documentEname"), key: "name_en" },
    { title: i18n.global.t("code"), key: "code" },
    { title: i18n.global.t("section"), key: "category__display" },
    { title: i18n.global.t("describtion"), key: "description" },
    { title: i18n.global.t("is_active"), key: "is_active" },
  ],
};

export default headers;
