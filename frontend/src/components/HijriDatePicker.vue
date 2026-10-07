<template>
<v-col :cols="12" :lg="cols" :md="cols" class="pt-2">
  <div
    class="hijri-picker"
    :class="[`size-${size}`, `variant-${variant}`, { block, disabled, readonly }]"
    :style="pickerStyle"
    ref="wrapperRef"

  >
    <label v-if="label" class="hijri-label" :class="{ 'label-error': computedError,'label-active' : isOpen ,'floating':isLabelFloating}">
      {{ label }}<span v-if="required" class="required-star">*</span>
    </label>
    <v-menu
      v-model="isOpen"
      :disabled="disabled || readonly"
      :close-on-content-click="false"
      :location="popupPosition"
      :offset="6"
      transition="slide-y-transition"
      content-class="hijri-menu-content-wrapper"
    >
      <template v-slot:activator="{ props }">
        <div
          class="hijri-input"
          v-bind="props"
          :class="{
            'is-open': isOpen,
            'is-error': !!computedError,
            'is-success': isSuccess,
            'is-disabled': disabled,
            'is-readonly': readonly,
          }"
          :style="inputStyle"
          :tabindex="disabled || readonly ? -1 : 0"
          @keydown.enter="open"
          @keydown.space.prevent="open"
          @keydown.escape="close"
          role="combobox"
          :aria-expanded="isOpen"
          :aria-label="label || placeholder"
          :aria-disabled="disabled"
        >
          <span v-if="prefixIcon" class="prefix-icon" v-html="prefixIcon" />
          <svg v-else class="icon-cal" viewBox="0 0 24 24">
            <path
              d="M19 4h-1V2h-2v2H8V2H6v2H5C3.9 4 3 4.9 3 6v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11zm0-13H5V6h14v1z"
            />
          </svg>
          <span class="hijri-value" :class="{ 'is-placeholder': !selectedLabel }":style="{opacity:(label && !isLabelFloating)? 0:1}">{{
            selectedLabel || placeholder
          }}</span>
          <span v-if="loading" class="spinner" />
          <svg v-else-if="isSuccess" class="icon-success" viewBox="0 0 24 24">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
          </svg>
          <span
            v-else-if="clearable && selectedLabel && !disabled && !readonly"
            class="icon-clear"
            @click.stop="clearSelection"
            >✕</span
          >
          <svg
            v-if="!loading"
            class="icon-chevron"
            :class="{ rotated: isOpen }"
            viewBox="0 0 24 24"
          >
            <path d="M7 10l5 5 5-5z" />
          </svg>
        </div>
      </template>

      <div
        class="hijri-popup"
        :class="`popup-${popupPosition}`"
        :style="popupStyle"
        role="dialog"
      >
        <div class="popup-header">
          <button
            v-if="!fixedMonth"
            class="nav-btn"
            @click.stop="prevMonth"
            :disabled="currentMonthIndex <= 1"
          >
            &#8250;
          </button>
          <div class="header-info" @click.stop="toggleYearPicker">
            <span class="month-name">
              {{
                selectedDay
                  ? getWeekDayName(selectedDay) +
                    " ، " +
                    selectedDay.day +
                    " " +
                    (locale === "en"
                      ? MONTH_NAMES_EN[currentMonth.index - 1]
                      : currentMonth.name)
                  : locale === "en"
                  ? MONTH_NAMES_EN[currentMonth.index - 1]
                  : currentMonth.name
              }}

            </span>
          </div>
          <span class="year-badge"
            >{{ hijriYear }} {{ locale === "en" ? "AH" : "هـ" }}</span
          >
          <button
            v-if="!fixedMonth"
            class="nav-btn"
            @click.stop="nextMonth"
            :disabled="currentMonthIndex >= 12"
          >
            &#8249;
          </button>
        </div>
        <Transition name="slide-down">
          <div v-if="showMonthPicker" class="month-picker">
            <div
              v-for="(name, i) in MONTH_NAMES"
              :key="i"
              class="month-item"
              :class="{ active: currentMonthIndex === i + 1 }"
              @click.stop="selectMonth(i + 1)"
            >
              {{ locale === "en" ? MONTH_NAMES_EN[i] : name }}
            </div>
          </div>
        </Transition>
        <template v-if="!showMonthPicker">
          <div class="week-row">
            <div
              v-for="d in locale === 'en' ? WEEK_DAYS_EN : WEEK_DAYS_FULL"
              :key="d"
              class="wlabel"
            >
              {{ d }}
            </div>
          </div>
          <div class="days-grid">
            <div
              v-for="e in currentMonth.startOffset"
              :key="'e' + e"
              class="cell empty"
            />
            <div
              v-for="day in currentMonth.days"
              :key="day"
              class="cell"
              :class="{
                today: isToday(day),
                selected: isSelected(day),
                'in-range': isInRange(day),
                'range-start': isRangeStart(day),
                'range-end': isRangeEnd(day),
                friday: getDayOfWeek(currentMonth.startOffset, day) === 6,
                disabled: isDayDisabled(day),
              }"
              :title="getDayLabel(day)"
              @click.stop="!isDayDisabled(day) && selectDay(day)"
              @mouseenter="rangeMode && setHoverDay(day)"
            >
              <span class="cell-inner">{{ day }}</span>
            </div>
          </div>
          <div class="popup-footer">
            <div class="footer-right">
              <button v-if="showCancel" class="btn-confirm" @click.stop="close" type="button">
                {{ locale === "en" ? "Cancel" : "الغاء" }}
              </button>
              <button v-if="clearable" class="btn-clear" @click.stop="clearSelection" type="button">
                {{ locale === "en" ? "Clear" : "مسح" }}
              </button>
            </div>
          </div>
        </template>
      </div>
    </v-menu>
    <div class="input-footer" >
      <span class="error-msg" v-if="computedError">{{ computedError }}</span>
      <span class="hint-msg" v-else-if="hint">{{ hint }}</span>
      <span v-else />
      <span v-if="showCounter" class="counter">{{ selectedLabel ? 1 : 0 }} / 1</span>
    </div>
    </div>

    </v-col>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import moment from "moment-hijri";

// ══════════════════════════════════════════
// منطق التقويم باستخدام moment-hijri
// ══════════════════════════════════════════

const MONTH_NAMES = [
  "محرم",
  "صفر",
  "ربيع الأول",
  "ربيع الآخر",
  "جمادى الأولى",
  "جمادى الآخرة",
  "رجب",
  "شعبان",
  "رمضان",
  "شوال",
  "ذو القعدة",
  "ذو الحجة",
];

function _getTodayHijri() {
  const m = moment();
  return { year: m.iYear(), month: m.iMonth() + 1, day: m.iDate() };
}

function _monthDays(month, year) {
  return moment()
    .iYear(year)
    .iMonth(month - 1)
    .iDate(1)
    .iDaysInMonth();
}

function _firstDayOfMonth(year, month) {
  const dow = moment()
    .iYear(year)
    .iMonth(month - 1)
    .iDate(1)
    .day();
  // moment: 0=أحد → نريد: 0=سبت
  return (dow + 1) % 7;
}

function _buildMonths(year) {
  return MONTH_NAMES.map((name, i) => {
    const mn = i + 1;
    return {
      index: mn,
      name,
      days: _monthDays(mn, year),
      startOffset: _firstDayOfMonth(year, mn),
    };
  });
}

function getDayOfWeek(startOffset, day) {
  return (startOffset + day - 1) % 7;
}

function _gregorianToHijri(gy, gm, gd) {
  const m = moment(new Date(gy, gm - 1, gd));
  return { year: m.iYear(), month: m.iMonth() + 1, day: m.iDate() };
}

// ══════════════════════════════════════════
// Props & Emits
// ══════════════════════════════════════════
const props = defineProps({
  modelValue: { type: [String, Array], default: null },
  month: { type: Number, default: null },
  placeholder: { type: String, default: "اختر تاريخاً هجرياً" },
  label: { type: String, default: "" },
  hint: { type: String, default: "" },
  errorMessage: { type: String, default: "" },
  disabled: { type: Boolean, default: false },
  readonly: { type: Boolean, default: false },
  clearable: { type: Boolean, default: true },
  required: { type: Boolean, default: false },
  size: { type: String, default: "md" },
  block: { type: Boolean, default: false },
  width: { type: String, default: "" },
  height: { type: String, default: "" },
  borderColor: { type: String, default: "" },
  borderWidth: { type: String, default: "" },
  borderRadius: { type: String, default: "" },
  borderStyle: { type: String, default: "" },
  popupPosition: { type: String, default: "bottom" },
  fixedMonth: { type: Boolean, default: true },
  variant: { type: String, default: "outlined" },
  loading: { type: Boolean, default: false },
  success: { type: Boolean, default: false },
  prefixIcon: { type: String, default: "" },
  showCounter: { type: Boolean, default: false },
  showConfirm: { type: Boolean, default: false },
  showCancel: { type: Boolean, default: true },
  onConfirm: { type: Function, default: null },
  rangeMode: { type: Boolean, default: false },
  minDate: { type: String, default: "" },
  maxDate: { type: String, default: "" },
  disabledDays: { type: Array, default: () => [] },
  rules: { type: Array, default: () => [] },
  validateOnChange: { type: Boolean, default: true },
  displayFormat: { type: String, default: "YYYY-MM-DD" },
  locale: { type: String, default: "ar" },
  cols: { type: [Number, String], default: 12 },
});

const emit = defineEmits([
  "update:modelValue",
  "change",
  "clear",
  "open",
  "close",
  "month-change",
  "validate",
  "confirm",
]);

// ══════════════════════════════════════════
// Constants
// ══════════════════════════════════════════
const MONTH_NAMES_EN = [
  "Muharram",
  "Safar",
  "Rabi' al-Awwal",
  "Rabi' al-Thani",
  "Jumada al-Ula",
  "Jumada al-Akhirah",
  "Rajab",
  "Sha'ban",
  "Ramadan",
  "Shawwal",
  "Dhu al-Qi'dah",
  "Dhu al-Hijjah",
];
const WEEK_DAYS_FULL = [
  "السبت",
  "الأحد",
  "الاثنين",
  "الثلاثاء",
  "الأربعاء",
  "الخميس",
  "الجمعة",
];

const WEEK_DAYS_EN = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"];


const WEEK_DAYS_EN_FULL = [
  "Saturday",
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
];



// ══════════════════════════════════════════
// State
// ══════════════════════════════════════════
const today = _getTodayHijri();
const hijriYear = today.year;
const todayMonth = today.month;
const todayDay = today.day;
const months = _buildMonths(hijriYear);

const isOpen = ref(false);
const currentMonthIndex = ref(props.month ?? todayMonth);
const wrapperRef = ref(null);
const internalError = ref("");
const showMonthPicker = ref(false);
const hoverDay = ref(null);
const selectedDay = ref(null);
const rangeStart = ref(null);
const rangeEnd = ref(null);

function init(val) {
  if (!val) {
    selectedDay.value = null;
    return;
  }
  if (props.rangeMode && Array.isArray(val)) {
    rangeStart.value = parseDate(val[0]);
    rangeEnd.value = parseDate(val[1]);
  } else if (typeof val === "string") selectedDay.value = parseDate(val);
}
init(props.modelValue);

// ══════════════════════════════════════════
// Computed
// ══════════════════════════════════════════
const currentMonth = computed(() =>
  months.find((m) => m.index === currentMonthIndex.value)
);
const locale = computed(() => props.locale);
const isLabelFloating = computed(() => isOpen.value || !!selectedLabel.value) ;
const computedError = computed(() => props.errorMessage || internalError.value);
const isSuccess = computed(
  () => props.success && !computedError.value && !!selectedLabel.value
);
const popupStyle = computed(() => ({ width: "100%"  }));
const pickerStyle = computed(() => {
 const style ={ ...(props.width ? { width: props.width } : {}),
  ...(props.height ? { height: props.height } : {}),
 }
  if(props.col){
   const percentage = (Number(props.cols)/12)*100
   style.flex=`0 0 ${percentage}`
   style.maxWidth=` ${percentage}`
   style.width='100%'
   style.padding='0 12px'

  }
  return style
});

const inputStyle = computed(() => ({
  ...(props.height ? { height: props.height, minHeight: props.height } : {}),
  ...(props.borderColor ? { borderColor: props.borderColor } : {}),
  ...(props.borderWidth ? { borderWidth: props.borderWidth } : {}),
  ...(props.borderRadius ? { borderRadius: props.borderRadius } : {}),
  ...(props.borderStyle ? { borderStyle: props.borderStyle } : {}),
}));

const selectedLabel = computed(() => {
  if (props.rangeMode) {
    if (!rangeStart.value) return "";
    return `${formatDate(rangeStart.value)}  ←  ${
      rangeEnd.value ? formatDate(rangeEnd.value) : "..."
    }`;
  }
  return selectedDay.value ? formatDate(selectedDay.value) : "";
});

watch(() => props.modelValue, init);
watch(
  () => props.month,
  (val) => {
    // نحدّث الشهر فقط إذا لم يكن الـ popup مفتوحاً
    if (val && !isOpen.value) currentMonthIndex.value = val;
  }
);

// ══════════════════════════════════════════
// Helpers
// ══════════════════════════════════════════
function parseDate(val) {
  if (!val) return null;
  const p = val.split("-");
  return p.length === 3 ? { year: +p[0], month: +p[1], day: +p[2] } : null;
}

function formatDate(d) {
  if (!d) return "";
  const y = d.year || hijriYear;
  const m = String(d.month).padStart(2, "0");
  const dd = String(d.day).padStart(2, "0");
  if (props.displayFormat === "DD/MM/YYYY") return `${dd}/${m}/${y}`;
  if (props.displayFormat === "full") {
    const mn =
      props.locale === "ar" ? MONTH_NAMES[d.month - 1] : MONTH_NAMES_EN[d.month - 1];
    return props.locale === "ar" ? `${d.day} ${mn} ${y} هـ` : `${d.day} ${mn} ${y} AH`;
  }
  return `${y}-${m}-${dd}`;
}

function dateToNum(d) {
  return d ? (d.year || hijriYear) * 10000 + d.month * 100 + d.day : 0;
}

function isDayDisabled(day) {
  const dow = getDayOfWeek(currentMonth.value.startOffset, day);
  if (props.disabledDays.includes(dow)) return true;
  const num = dateToNum({ month: currentMonthIndex.value, day });
  if (props.minDate && num < dateToNum(parseDate(props.minDate))) return true;
  if (props.maxDate && num > dateToNum(parseDate(props.maxDate))) return true;
  return false;
}

function getDayLabel(day) {
  return formatDate({ year: hijriYear, month: currentMonthIndex.value, day });
}

function getWeekDayName(d) {
  const m = months.find((m) => m.index === d.month);
  if (!m) return "";
  const dow = getDayOfWeek(m.startOffset, d.day);
  return props.locale === "en" ? WEEK_DAYS_EN_FULL[dow] : '';
}

function isRangeStart(day) {
  return (
    props.rangeMode &&
    rangeStart.value?.day === day &&
    rangeStart.value?.month === currentMonthIndex.value
  );
}
function isRangeEnd(day) {
  return (
    props.rangeMode &&
    rangeEnd.value?.day === day &&
    rangeEnd.value?.month === currentMonthIndex.value
  );
}
function isInRange(day) {
  if (!props.rangeMode || !rangeStart.value) return false;
  const end = rangeEnd.value || hoverDay.value;
  if (!end) return false;
  const num = dateToNum({ month: currentMonthIndex.value, day });
  const s = dateToNum(rangeStart.value),
    e = dateToNum(end);
  return num > Math.min(s, e) && num < Math.max(s, e);
}

// ══════════════════════════════════════════
// Actions
// ══════════════════════════════════════════
function handleClick() {
  if (props.disabled || props.readonly) return;
  isOpen.value = !isOpen.value;
}
function open() {
  isOpen.value = true;
}
function close() {
  isOpen.value = false;
}

watch(isOpen, (val) => {
  if (val) {
    currentMonthIndex.value = props.month ?? todayMonth;
    showMonthPicker.value = false;
    emit("open");
  } else {
    showMonthPicker.value = false;
    hoverDay.value = null;
    emit("close");
  }
});
function prevMonth() {
  if (currentMonthIndex.value > 1) {
    currentMonthIndex.value--;
    emit("month-change", currentMonthIndex.value);
  }
}
function nextMonth() {
  if (currentMonthIndex.value < 12) {
    currentMonthIndex.value++;
    emit("month-change", currentMonthIndex.value);
  }
}
function toggleYearPicker() {
  if (!props.fixedMonth) showMonthPicker.value = !showMonthPicker.value;
}
function selectMonth(idx) {
  currentMonthIndex.value = idx;
  showMonthPicker.value = false;
  emit("month-change", idx);
}
function setHoverDay(day) {
  if (rangeStart.value && !rangeEnd.value)
    hoverDay.value = { year: hijriYear, month: currentMonthIndex.value, day };
}

function selectDay(day) {
  if (props.rangeMode) {
    if (!rangeStart.value || rangeEnd.value) {
      rangeStart.value = { year: hijriYear, month: currentMonthIndex.value, day };
      rangeEnd.value = null;
    } else {
      const s = dateToNum(rangeStart.value),
        e = dateToNum({ year: hijriYear, month: currentMonthIndex.value, day });
      if (e < s) {
        rangeEnd.value = rangeStart.value;
        rangeStart.value = { year: hijriYear, month: currentMonthIndex.value, day };
      } else rangeEnd.value = { year: hijriYear, month: currentMonthIndex.value, day };
      if (!props.showConfirm) emitRange();
    }
    return;
  }
  selectedDay.value = { year: hijriYear, month: currentMonthIndex.value, day };
  const formatted = formatDate(selectedDay.value);
  if (props.validateOnChange) validate(formatted);
  emit("update:modelValue", formatted);
  emit("change", formatted);
  if (!props.showConfirm) close();
}

function confirmSelection() {
  const value = props.rangeMode
    ? [formatDate(rangeStart.value), formatDate(rangeEnd.value)]
    : formatDate(selectedDay.value);
  emit("update:modelValue", value);
  emit("change", value);
  emit("confirm", value);
  if (typeof props.onConfirm === "function") props.onConfirm(value);
  close();
}

function emitRange() {
  const val = [formatDate(rangeStart.value), formatDate(rangeEnd.value)];
  emit("update:modelValue", val);
  emit("change", val);
  close();
}

function clearSelection() {
  selectedDay.value = rangeStart.value = rangeEnd.value = null;
  if (props.validateOnChange) validate(null);
  emit("update:modelValue", props.rangeMode ? [] : null);
  emit("clear");
}

function goToday() {
  currentMonthIndex.value = todayMonth;
  selectedDay.value = { year: hijriYear, month: todayMonth, day: todayDay };
  const formatted = formatDate(selectedDay.value);
  if (props.validateOnChange) validate(formatted);
  emit("update:modelValue", formatted);
  emit("change", formatted);
  if (!props.showConfirm) close();
}
function isToday(day) {
  return day === todayDay && currentMonthIndex.value === todayMonth;
}
function isSelected(day) {
  if (props.rangeMode) return isRangeStart(day) || isRangeEnd(day);
  return (
    selectedDay.value?.day === day && selectedDay.value?.month === currentMonthIndex.value
  );
}

// function validate(value) {
//   for (const rule of props.rules) {
//     const result = rule(value);
//     if (result !== true) {
//       internalError.value = result;
//       emit("validate", false);
//       return false;
//     }
//   }
//   internalError.value = "";
//   emit("validate", true);
//   return true;
// }
function validate(value) {
    if (props.required && !value) {
      internalError.value = props.locale ==='en' ? 'This Field is required' : 'هذا الحقل مطلوب';
      emit("validate", false);
      return false;
    }

  internalError.value = "";
  emit("validate", true);
  return true;
}
// onMounted(() => document.addEventListener("mousedown", onClickOutside));
// onUnmounted(() => document.removeEventListener("mousedown", onClickOutside));

defineExpose({
  validate: () => validate(selectedLabel.value ||null ),
  rest:()=>{internalError.value=''},
  clear: clearSelection,
  open,
  close,
  getValue: () => selectedLabel.value,
});
</script>

<style scoped>
.hijri-picker {
  --p: rgb(var(--v-theme-primary, 19, 99, 223));
  --pd: rgba(var(--v-theme-primary, 19, 99, 223), 0.85);
  --pl: rgba(var(--v-theme-primary, 19, 99, 223), 0.15);
  --pg: rgba(var(--v-theme-primary, 19, 99, 223), 0.25);
  --on-p: rgb(var(--v-theme-on-primary, 255, 255, 255));
  --err: rgb(var(--v-theme-error, 220, 38, 38));
  --errl: rgba(var(--v-theme-error, 220, 38, 38), 0.15);
  --ok: rgb(var(--v-theme-success, 22, 163, 74));
  --okl: rgba(var(--v-theme-success, 22, 163, 74), 0.15);
  --txt: rgb(var(--v-theme-on-surface, 15, 23, 42));
  --sub: rgba(var(--v-theme-on-surface, 15, 23, 42), 0.6);
  --bdr: rgba(var(--v-border-color, 226, 232, 240), var(--v-border-opacity, 0.38));
  --bg: rgb(var(--v-theme-surface, 255, 255, 255));
  --soft: rgba(var(--v-theme-on-surface, 15, 23, 42), 0.05);
  --r: 12px;
  --sh: 0 8px 40px rgba(0, 0, 0, 0.25);
  position: relative;
  display: inline-flex;
  flex-direction: column;
  direction: rtl;
  font-family: "Almarai", sans-serif;
  width: 100%;
}
.hijri-picker.block {
  display: flex;
  width: 100%;
}
.hijri-picker.disabled {
  opacity: 0.5;
  pointer-events: none;
}
.hijri-picker.readonly .hijri-input {
  cursor: default;
  background: var(--soft);
}

.hijri-label {
  position: absolute;
  top: 50px;
  transform: translateY(-210%);
  right: 44px;
  font-size: 0.875rem;
  padding: 0;
  background: transparent;
  z-index: 5;
  font-weight: 600;
  pointer-events: none;

}
.hijri-label.floating {
  top: -12px;
  transform: translateY(0);
  right: 14px;
  font-size: 0.875rem;
  padding: 0 6px;
  background: var(--bg);
  z-index: 5;
  font-weight: 600;
  pointer-events: none;

}
.hijri-label.label-error {
  color: var(--err);
}
.required-star {

  margin-right: 3px;
}

.hijri-input {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 16px;
  border: 1.5px solid var(--bdr);
  border-radius: var(--r);
  cursor: pointer;
  background: var(--bg);
  color: var(--txt);
  min-width: 0;
  width: 100%;
  transition: all 0.2s ease;
  user-select: none;
  outline: none;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.hijri-input:hover:not(.is-disabled):not(.is-readonly) {
  border-color: var(--p);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05), 0 0 0 3px var(--pg);
}
.hijri-input:focus,
.hijri-input.is-open {
  border-color: var(--p);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05), 0 0 0 4px var(--pg);
}
.hijri-input.is-error {
  border-color: var(--err);
  box-shadow: 0 0 0 4px var(--errl);
}
.hijri-input.is-success {
  border-color: var(--ok);
  box-shadow: 0 0 0 4px var(--okl);
}

.variant-filled .hijri-input {
  background: var(--soft);
  border-color: transparent;
  border-radius: var(--r) var(--r) 4px 4px;
  border-bottom: 2px solid var(--bdr);
  box-shadow: none;
}
.variant-filled .hijri-input.is-open {
  border-bottom-color: var(--p);
  background: var(--pl);
}

.variant-underlined .hijri-input {
  background: transparent;
  border: none;
  border-bottom: 2px solid var(--bdr);
  border-radius: 0;
  padding-right: 0;
  padding-left: 0;
  box-shadow: none;
}
.variant-underlined .hijri-input.is-open {
  border-bottom-color: var(--p);
}

.size-sm .hijri-input {
  padding: 7px 12px;
}
.size-sm .hijri-value {
  font-size: 0.82rem;
}
.size-lg .hijri-input {
  padding: 14px 18px;
}
.size-lg .hijri-value {
  font-size: 1rem;
}

.icon-cal {
  width: 18px;
  height: 18px;
  fill: var(--sub);
  flex-shrink: 0;
  opacity: 0.8;
}
.hijri-value {
  flex: 1;
  font-size: 0.925rem;
  color: var(--txt);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hijri-value.is-placeholder {
  color: var(--sub);
  font-weight: 400;
}
.icon-clear {
  font-size: 0.7rem;
  color: var(--sub);
  cursor: pointer;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  flex-shrink: 0;
  background: var(--soft);
}
.icon-clear:hover {
  background: var(--errl);
  color: var(--err);
}
.icon-chevron {
  width: 20px;
  height: 20px;
  fill: var(--sub);
  flex-shrink: 0;
  transition: transform 0.25s ease;
}
.icon-chevron.rotated {
  transform: rotate(180deg);
  fill: var(--p);
}
.icon-success {
  width: 18px;
  height: 18px;
  fill: var(--ok);
  flex-shrink: 0;
}
.spinner {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  border: 2px solid var(--pl);
  border-top-color: var(--p);
  border-radius: 50%;
  animation: spin 0.65s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 18px;
  padding: 0 2px;
}
.error-msg {
  font-size: 0.78rem;
  color: var(--err);
  font-weight: 500;
}
.hint-msg {
  font-size: 0.78rem;
  color: var(--sub);
}
.counter {
  font-size: 0.75rem;
  color: var(--sub);
}







:deep(.hijri-menu-content-wrapper) {
  z-index: 999999 !important;
  --p: rgb(var(--v-theme-primary, 19, 99, 223));
  --pd: rgba(var(--v-theme-primary, 19, 99, 223), 0.85);
  --pl: rgba(var(--v-theme-primary, 19, 99, 223), 0.15);
  --pg: rgba(var(--v-theme-primary, 19, 99, 223), 0.25);
  --on-p: rgb(var(--v-theme-on-primary, 255, 255, 255));
  --err: rgb(var(--v-theme-error, 220, 38, 38));
  --errl: rgba(var(--v-theme-error, 220, 38, 38), 0.15);
  --ok: rgb(var(--v-theme-success, 22, 163, 74));
  --okl: rgba(var(--v-theme-success, 22, 163, 74), 0.15);
  --txt: rgb(var(--v-theme-on-surface, 15, 23, 42));
  --sub: rgba(var(--v-theme-on-surface, 15, 23, 42), 0.6);
  --bdr: rgba(var(--v-border-color, 226, 232, 240), var(--v-border-opacity, 0.38));
  --bg: rgb(var(--v-theme-surface, 255, 255, 255));
  --soft: rgba(var(--v-theme-on-surface, 15, 23, 42), 0.05);
  --r: 12px;
  --sh: 0 8px 40px rgba(0, 0, 0, 0.25);
  font-family: "Almarai", sans-serif;
  direction: rtl;
}

/* --- Dark Theme Harmonization --- */
.v-theme--dark .hijri-picker,
.v-theme--blueTheme .hijri-picker,
.v-theme--darkTheme .hijri-picker,
.v-theme--natureTheme .hijri-picker,
.hijri-picker.dark,
[data-theme="dark"] .hijri-picker {
  --header-bg: linear-gradient(135deg, rgba(var(--v-theme-primary, 79, 140, 255), 0.25) 0%, rgba(var(--v-theme-surface, 22, 32, 51), 0.95) 100%);
  --header-txt: rgb(var(--v-theme-on-surface, 248, 250, 252));
  --header-badge-bg: rgba(var(--v-theme-primary, 79, 140, 255), 0.2);
  --header-badge-txt: rgb(var(--v-theme-primary, 79, 140, 255));
  --header-btn-bg: rgba(var(--v-theme-on-surface, 248, 250, 252), 0.08);
  --header-btn-bdr: rgba(var(--v-theme-on-surface, 248, 250, 252), 0.15);
  --header-btn-txt: rgb(var(--v-theme-on-surface, 248, 250, 252));
}

:deep(.v-theme--dark.hijri-menu-content-wrapper),
:deep(.v-theme--dark .hijri-menu-content-wrapper),
:deep(.v-theme--blueTheme.hijri-menu-content-wrapper),
:deep(.v-theme--blueTheme .hijri-menu-content-wrapper),
:deep(.v-theme--darkTheme.hijri-menu-content-wrapper),
:deep(.v-theme--darkTheme .hijri-menu-content-wrapper),
:deep(.v-theme--natureTheme.hijri-menu-content-wrapper),
:deep(.v-theme--natureTheme .hijri-menu-content-wrapper),
:deep(.hijri-menu-content-wrapper.dark),
:deep([data-theme="dark"] .hijri-menu-content-wrapper) {
  --header-bg: linear-gradient(135deg, rgba(var(--v-theme-primary, 79, 140, 255), 0.25) 0%, rgba(var(--v-theme-surface, 22, 32, 51), 0.95) 100%);
  --header-txt: rgb(var(--v-theme-on-surface, 248, 250, 252));
  --header-badge-bg: rgba(var(--v-theme-primary, 79, 140, 255), 0.2);
  --header-badge-txt: rgb(var(--v-theme-primary, 79, 140, 255));
  --header-btn-bg: rgba(var(--v-theme-on-surface, 248, 250, 252), 0.08);
  --header-btn-bdr: rgba(var(--v-theme-on-surface, 248, 250, 252), 0.15);
  --header-btn-txt: rgb(var(--v-theme-on-surface, 248, 250, 252));
}

:deep(.hijri-popup) {
  background: var(--bg);
  border-radius: 18px;
  box-shadow: var(--sh);
  overflow: hidden;
  border: 1px solid var(--bdr);
  container-type: inline-size;
  margin-top: 6px;
  color: var(--txt);
}


:deep(.popup-header) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 16px 14px;
  background: var(--header-bg, linear-gradient(135deg, var(--p) 0%, var(--pd) 100%));
  color: var(--header-txt, #fff);
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--bdr);
}
:deep(.popup-header::after) {
  content: "";
  position: absolute;
  top: -30px;
  left: -30px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.07);
  pointer-events: none;
}
:deep(.year-badge) {
  font-size: clamp(1rem, 2cqw, 0.8rem);
  background: var(--header-badge-bg, rgba(255, 255, 255, 0.22));
  color: var(--header-badge-txt, #fff);
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 700;
  white-space: nowrap;
  align-self: flex-start;
}
:deep(.header-info) {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 10px;
  transition: background 0.15s;
  flex: 1;
}
:deep(.header-info:hover) {
  background: rgba(255, 255, 255, 0.12);
}
:deep(.month-name) {
  font-size: clamp(1rem, 3.5cqw, 1.05rem);
  font-weight: 800;
  letter-spacing: 0.01em;
}
:deep(.nav-btn) {
  background: var(--header-btn-bg, rgba(255, 255, 255, 0.15));
  border: 1px solid var(--header-btn-bdr, rgba(255, 255, 255, 0.2));
  color: var(--header-btn-txt, #fff);
  font-size: 1.2rem;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
:deep(.nav-btn:hover:not(:disabled)) {
  background: rgba(255, 255, 255, 0.28);
  transform: scale(1.05);
}
:deep(.nav-btn:disabled) {
  opacity: 0.3;
  cursor: default;
}

:deep(.month-picker) {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  padding: 14px;
}
:deep(.month-item) {
  text-align: center;
  padding: 9px 4px;
  border-radius: 10px;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  color: var(--txt);
  transition: all 0.15s;
  border: 1.5px solid transparent;
}
:deep(.month-item:hover) {
  background: var(--pl);
  color: var(--p);
  border-color: var(--pl);
}
:deep(.month-item.active) {
  background: var(--p);
  color: var(--on-p, #fff);
  font-weight: 700;
  box-shadow: 0 2px 8px var(--pg);
}

:deep(.week-row) {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  padding: 15px 12px 10px;
  background: var(--soft);
  border-bottom: 1px solid var(--bdr);
}
:deep(.wlabel) {
  text-align: center;
  font-size: clamp(0.8rem, 1.8cqw, 0.62rem);
  font-weight: 700;
  color: var(--sub);
  padding: 2px 0;
  letter-spacing: 0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@container (max-width: 260px) {
  :deep(.days-grid) {
    padding: 4px 6px 6px;
    gap: 2px;
  }
 :deep(.popup-header ){
    padding: 10px 10px 8px;
  }
  :deep(.month-name ){
    font-size: 1rem;
  }
 :deep(.year-badge) {
    font-size: 1rem;
    padding: 3px 7px;
  }
  :deep(.nav-btn) {
    width: 28px;
    height: 28px;
    font-size: 1rem;
  }
  :deep(.popup-footer) {
    padding: 6px 10px 10px;
  }
  :deep(.btn-clear),
  :deep(.btn-confirm) {
    padding: 5px 12px;
    font-size: 1rem;
  }
}

:deep(.days-grid) {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  padding: 8px 12px 18px;
  gap: 8px;
}
:deep(.cell) {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  position: relative;
  transition: all 0.12s;
}
:deep(.cell-inner) {
  width: 90%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: clamp(1rem, 2.5cqw, 0.875rem);
  font-weight: 500;
  color: var(--txt);
  transition: all 0.15s;
}
:deep(.cell:not(.empty):not(.disabled):hover .cell-inner) {
  background: var(--pl);
  color: var(--p);
  font-weight: 600;
}
:deep(.cell.empty) {
  pointer-events: none;
}
:deep(.cell.disabled ){
  opacity: 0.3;
  cursor: not-allowed;
}
:deep(.cell.friday .cell-inner) {
  color: #ef4444;
}
:deep(.cell.today .cell-inner) {
  background: var(--pl);
  color: var(--p) !important;
  font-weight: 800;
  border: 2px solid var(--p);
}
:deep(.cell.selected .cell-inner),
:deep(.cell.range-start .cell-inner),
:deep(.cell.range-end .cell-inner) {
  background: var(--p) !important;
  color: var(--on-p, #fff) !important;
  font-weight: 700;
  box-shadow: 0 2px 10px var(--pg);
}
:deep(.cell.in-range) {
  background: var(--pl);
  border-radius: 0;
}
:deep(.cell.in-range .cell-inner) {
  color: var(--p);
  font-weight: 600;
}
:deep(.cell.range-start) {
  border-radius: 50% 0 0 50%;
  background: var(--pl);
}
:deep(.cell.range-end) {
  border-radius: 0 50% 50% 0;
  background: var(--pl);
}

:deep(.popup-footer ){
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  padding: 15px 14px 20px;
  border-top: 1px solid var(--bdr);
  background: var(--soft);
}
:deep(.footer-right) {
  display: flex;
  gap: 8px;
}
:deep(.btn-clear),
:deep(.btn-confirm ){
  padding: 7px 18px;
  border: none;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  font-family: "Almarai", sans-serif;
  transition: all 0.18s ease;
}
:deep(.btn-clear) {
  background: transparent;
  color: var(--sub);
  border: 1.5px solid var(--bdr);
}
:deep(.btn-clear:hover) {
  background: var(--errl);
  color: var(--err);
  border-color: var(--err);
}
:deep(.btn-confirm) {
  background: var(--p);
  color: var(--on-p, #fff);
  border: 1.5px solid var(--p);
  box-shadow: 0 1px 4px var(--pg);
}
:deep(.btn-confirm:hover) {
  background: var(--pd);
  box-shadow: 0 4px 14px var(--pg);
  transform: translateY(-1px);
}


:deep(.slide-down-enter-active) {
  transition: opacity 0.18s ease, transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
}
:deep(.slide-down-leave-active) {
  transition: opacity 0.12s ease, transform 0.12s ease;
}
:deep(.slide-down-enter-from) {
  opacity: 0;
  transform: translateY(-8px);
}
:deep(.slide-down-leave-to) {
  opacity: 0;
  transform: translateY(-4px);
}
</style>



