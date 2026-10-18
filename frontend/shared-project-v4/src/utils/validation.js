import i18n from "@/plugins/i18n";

const ValueValidationPlugin = {
  install(Vue) {
    // دالة مساعد لاختيار الترجمة حسب اللغة
    const t = (arMsg, enMsg) => (i18n.global.locale === "ar" ? arMsg : enMsg);

    // required validation
    Vue.config.globalProperties.$required = (value) => {
    
      if (Array.isArray(value))
        return (
          value?.length > 0 || t("هذا الحقل مطلوب", "This field is required")
        );

      return (
        !!value ||
        typeof value === "boolean" ||
        value === 0 ||
        t("هذا الحقل مطلوب", "This field is required")
      );
    };
 
    Vue.config.globalProperties.$startsWith = (char = 100) => (value) => {
    
      if(value)
      if(!value.startsWith(char)) return `يجب ان يبداء ب  ${String(char)}`

      return true
     
    };

    // numeric validation
    Vue.config.globalProperties.$numeric = (value) =>
      !value ||
      /^[0-9+',.]+$/.test(value) ||
      t("يجب أن تكون أرقام فقط", "Must be numbers only");

    // max_length validation
    Vue.config.globalProperties.$max_length =
      (length = 100) =>
      (value) => {
        if (value && value.length > length) {
          return `${t(
            "أقصى عدد من الحروف",
            "Maximum number of characters"
          )} ${length}`;
        }
        return true;
      };

    // min_length validation
    Vue.config.globalProperties.$min_length =
      (length = 10) =>
      (value) =>
        !value ||
        value.length >= length ||
        `${t("أقل عدد من الحروف", "Minimum number of characters")} ${length}`;

    // ar_letters_only validation
    Vue.config.globalProperties.$ar = (value) =>
      !value ||
      !(/^[a-zA-Z` *?]+$/.test(value)) ||
      t("يجب أن تكون أحرف عربية فقط", "Must be Arabic letters only");

    // en_letters_only validation
    Vue.config.globalProperties.$en = (value) =>
      !value ||
      /^[a-zA-Z' '0-9+  '-.,@#$%^&*()_+=!*?]+$/.test(value) ||
      t("يجب أن تكون أحرف إنجليزية فقط", "Must be English letters only");

    // ar_with_numbers validation
    Vue.config.globalProperties.$ar_num = (value) =>
      !value ||
      /^[\u0621-\u064A0-9 ]+$/.test(value) ||
      t(
        "يجب أن تكون أحرف عربية وأرقام فقط",
        "Must be Arabic letters with numbers"
      );

    // en_with_numbers validation
    Vue.config.globalProperties.$en_num = (value) =>
      !value ||
      /^[a-zA-Z'0-9 ]+$/.test(value) ||
      t(
        "يجب أن تكون أحرف إنجليزية وأرقام فقط",
        "Must be English letters with numbers"
      );

    // max_date validation
    Vue.config.globalProperties.$max_date = (year) => (value) =>
      !value ||
      !year ||
      year >= value ||
      `${t("أقصى تاريخ هو", "Maximum date is")} ${year}`;

    // min_date validation
    Vue.config.globalProperties.$min_date = (year) => (value) =>
      !value || !year||
      year <= value ||
      `${t("أدنى تاريخ هو", "Minimum date is")} ${year}`;

    // max_value validation
    Vue.config.globalProperties.$max_value =
      (length = 10) =>
      (value) => {
         
        if (value && Number(value) > Number(length)) {
        
          return `${
            isNaN(parseInt(value))
              ? t("أقصى عدد من الحروف", "Max characters")
              : t("أقصى قيمة رقمية", "Max numeric value")
          } ${length}`;
        }
        return true;
      };

    // min_value validation
    Vue.config.globalProperties.$min_value =
      (length = 10) =>
      (value) => {
        if (value && Number(value) < Number(length)) {
          return `${
            isNaN(parseInt(value))
              ? t("أقل عدد من الحروف", "Min characters")
              : t("أقل قيمة رقمية", "Min numeric value")
          } ${length}`;
        }
        return true;
      };

    // email validation
    Vue.config.globalProperties.$email = (value) =>
      !value ||
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ||
      t("بريد إلكتروني غير صحيح", "Invalid email address");

    // more than
    Vue.config.globalProperties.$more_than = (value2) => (value) =>
      !value ||
      !value2 ||
      parseFloat(value) > parseFloat(value2) ||
      `${t("يجب أن تكون أكبر من", "Must be greater than")} ${value2}`;

    // less than
    Vue.config.globalProperties.$less_than = (value2) => (value) =>
      !value ||
      !value2 ||
      parseFloat(value) < parseFloat(value2) ||
      `${t("يجب أن تكون أقل من", "Must be less than")} ${value2}`;

    // isTime
    Vue.config.globalProperties.$isTime = (value) => {
      const pattern = /^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$/;
      return (
        pattern.test(value) || t("صيغة الوقت غير صحيحة", "Invalid time format")
      );
    };

    // time_min_max
    Vue.config.globalProperties.$time_min_max = (min, max) => {
      if (min && max) {
        if (min >= max) {
          return t(
            "وقت النهاية أصغر أو يساوي وقت البداية",
            "End time is earlier or equal to start time"
          );
        }
      }
      return true;
    };

    // validUniqe
    Vue.config.globalProperties.$validUniqe = (value) =>
      value ? t("موجود مسبقًا", "Already exists") : true;

    // compare_time
    Vue.config.globalProperties.$compare_time = (start, end) => {
      if (start && end) {
        const [start_hr, start_min] = start.split(":").map(Number);
        const [end_hr, end_min] = end.split(":").map(Number);
        const startTime = start_hr * 60 + start_min;
        const endTime = end_hr * 60 + end_min;
        return startTime <= endTime || t("الوقت غير صحيح", "Invalid time");
      }
      return true;
    };

    // max_number
    Vue.config.globalProperties.$min_number =
      (length = 10) =>
      (value) =>
        !value ||
        value >= length ||
        `${t("اقل عدد هو", "Minimum number is")} ${length}`;

    Vue.config.globalProperties.$max_number =
      (length = 10) =>
      (value) =>
        !value ||
        value <= length ||
        `${t("أقصى عدد هو", "Maximum number is")} ${length}`;

    // addNameToRouter
    Vue.config.globalProperties.$addNameToRouter = function (name, name_ar) {
      let route = this.$route.matched.find((e) => e.name == name);
      route.name_ar = name_ar;
    };

    // PositiveSmallIntegerField
    Vue.config.globalProperties.$PositiveSmallIntegerField = (value) => {
      if (!Number.isInteger(Number(value)))
        return t(
          "يجب أن تكون القيمة عددًا صحيحًا.",
          "Value must be an integer."
        );
      if (value < 0)
        return t(
          "يجب أن تكون القيمة موجبة أو صفرًا.",
          "Value must be positive or zero."
        );
      if (value > 32767)
        return t(
          "يجب أن تكون القيمة أقل من أو تساوي 32767.",
          "Value must be less than or equal to 32767."
        );
      return true;
    };

    // IntegerField
    Vue.config.globalProperties.$IntegerField = (value) => {
      if (value < -2147483648)
        return t(
          "يجب أن تكون القيمة أكبر من أو تساوي -2147483648.",
          "Value must be greater than or equal to -2147483648."
        );
      if (value > 2147483647)
        return t(
          "يجب أن تكون القيمة أقل من أو تساوي 2147483647.",
          "Value must be less than or equal to 2147483647."
        );
      return true;
    };

    // decimal_valid
    Vue.config.globalProperties.$decimal_valid =
      (max_digits=10, decimal_places=2) => (value) => {
        const md = Number(max_digits) || 10;
        const dp = Number(decimal_places) || 2;
        const regex = new RegExp(
          `^\\d{1,${md}}$|^\\d{1,${
            md - dp
          }}(\\.\\d{1,${dp}})?$`
        );
        if (!regex.test(String(value)?.replace(/[^0-9.]/g, "")) && value) {
          return t(
            `يجب إدخال رقم صحيح بحد أقصى ${md} أرقام و ${dp} بعد الفاصلة`,
            `Must enter a valid number with up to ${md} digits and ${dp} decimals`
          );
        }
        return true;
      };

    // duplicate
    Vue.config.globalProperties.$duplicate =
      (items, key = undefined) =>
      (value) => {        
        if (items) {
          let data;
          if (!key) data = items.filter((e) => e == value);
          else data = items.filter((e) => e == value[key]);
          if (data.length > 1) {
            return t("البيانات مكررة", "Duplicate data");
          }
        }
        return true;
      };
    Vue.config.globalProperties.$confrim_pass = (new_pass) => (value) =>
      new_pass == value ||
      t("كلمة المرور غير متطابقة", "Password does not match");


    Vue.config.globalProperties.$wordCount = (word_count) =>(value)=>{
      if(!value) return
      const words = value.trim().split(/\s+/)
      return words.length >= word_count || `الحد الادنى لعدد الكلمات ${word_count}`
    }

    Vue.config.globalProperties.$valid_pass = (pass) => {
      if(!pass){
        return "كلمة المرور مطلوبة "
      }
      if(pass.length <8 ){
        return  "على الأقل 8 أحرف"
      }
      if(!/[A-Z]/.test(pass) && !/[a-z]/.test(pass)){
        return  "حرف كبير (A) وحرف صغير (a)"
      }
      if(!/\d/.test(pass) ){
        return "رقم واحد على الأقل (0-9)"
      }
      if(!/[!@#$%^&*(),.?":{}|<>]/.test(pass)){
        return "رمز خاص واحد (@, #, !...)"
      }
      if(/^\d+$/.test(pass)){
        return  "لايجب ان تكون ارقام فقط"
      }
      if(/(.)\1{2,}/.test(pass)){
        return  "لا يحتوي على تكرار مفرط (مثل 111)"
      }
     
    
      
      return true
      

     }

  },
};

export default ValueValidationPlugin;
