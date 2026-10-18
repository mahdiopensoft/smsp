<template>
  <v-col :cols="12" :lg="cols" :md="cols" class="py-2">
    <div :dir="language === 'ar' ? 'rtl' : 'ltr'" class="date-picker-wrapper">
      <!-- Activator Input Field -->
      <v-text-field
        ref="activatorRef"
        v-model="formattedDate"
        :label="label + (isRequired ? '   *' : '')"
        :placeholder="translations.selectDatePlaceholder"
        readonly
        clearable
        :variant="variant"
        density="compact"
        :rules="rules"
        :hide-details="hideDetails"
        :rounded="rounded ? 'xl' : 's'"
        class="custom-datepicker-input no-autofill-bg"
        color="primary"
        :style="containerStyle"
        @click:clear.stop="clearDate"
        :disabled="disabled"
      >
        <template v-slot:prepend-inner>
          <!-- icon?.startsWith("mdi-") ? icon : "mdi-" + icon -->
          <v-icon class="datepicker-icon">{{ "mdi-calendar" }}</v-icon>
        </template>
        <template #clear="{ props }">
          <VIcon
            v-bind="props"
            icon="mdi-close-circle"
            class="clear-icon"
            tabindex="-1"
          />
        </template>
      </v-text-field>

      <!-- Desktop Selection Menu -->
      <v-menu
        v-if="!isMobile"
        v-model="showPicker"
        :activator="activatorRef"
        :close-on-content-click="false"
        location="bottom center"
        offset="8"
        transition="slide-y-transition"
        min-width="320"
        max-width="360"
        :z-index="9999"
      >
        <v-card class="v-date-picker-card" border="0">
          <!-- Calendar Header -->
          <div class="v-date-picker-header">
            <div
              class="d-flex align-center justify-space-between w-100"
              :class="{ 'flex-row-reverse': language === 'ar' }"
            >
              <div
                class="header-year-text cursor-pointer"
                :class="{ 'header-text-active': isYearSelection }"
                @click="toggleYearSelection"
              >
                {{ currentYear }}
              </div>
              <div class="d-flex align-center gap-x-4">
                <div
                  class="header-date-text cursor-pointer"
                  :class="{
                    'header-text-active':
                      displayMode === 'date' && !isYearSelection && !isMonthSelection,
                  }"
                  @click="
                    displayMode = 'date';
                    isYearSelection = false;
                    isMonthSelection = false;
                  "
                >
                  {{ headerDateText }}
                </div>
                <div
                  v-if="withTime"
                  class="header-date-text cursor-pointer"
                  :class="{ 'header-text-active': displayMode === 'time' }"
                  @click="
                    displayMode = 'time';
                    isYearSelection = false;
                    isMonthSelection = false;
                  "
                >
                  {{ formattedTime }}
                </div>
              </div>
            </div>
          </div>

          <!-- Calendar Body -->
          <div class="datepicker-container">
            <div class="picker-content">
              <template v-if="displayMode === 'date'">
                <!-- Month/Year Navigation -->
                <div class="navigation-row px-1">
                  <div class="d-flex align-center flex-grow-1 overflow-hidden">
                    <v-btn
                      variant="text"
                      density="compact"
                      class="nav-label-btn px-2"
                      rounded
                      @click="toggleMonthSelection"
                    >
                      <span class="text-truncate">{{ currentMonth }}</span>
                      <v-icon icon="mdi-menu-down" size="small" class="ml-1" />
                    </v-btn>
                    <v-btn
                      variant="text"
                      density="compact"
                      class="nav-label-btn px-2"
                      rounded
                      @click="toggleYearSelection"
                    >
                      {{ currentYear }}
                      <v-icon icon="mdi-menu-down" size="small" class="ml-1" />
                    </v-btn>
                  </div>
                  <div class="d-flex flex-shrink-0">
                    <v-btn
                      icon="mdi-chevron-right"
                      variant="text"
                      density="comfortable"
                      size="small"
                      class="nav-arrow-btn"
                      @click="
                        isYearSelection || isMonthSelection
                          ? prevYearsOrMonths()
                          : prevMonth()
                      "
                    />
                    <v-btn
                      icon="mdi-chevron-left"
                      variant="text"
                      density="comfortable"
                      size="small"
                      class="nav-arrow-btn"
                      @click="
                        isYearSelection || isMonthSelection
                          ? nextYearsOrMonths()
                          : nextMonth()
                      "
                    />
                  </div>
                </div>

                <!-- Selection Grids -->
                <div v-if="isYearSelection" class="selection-grid year-grid">
                  <v-btn
                    v-for="year in visibleYears"
                    :key="year"
                    :variant="year === currentYear ? 'flat' : 'text'"
                    :color="year === currentYear ? 'primary' : undefined"
                    class="selection-item"
                    @click="selectYear(year)"
                  >
                    {{ year }}
                  </v-btn>
                </div>

                <div v-else-if="isMonthSelection" class="selection-grid month-grid">
                  <v-btn
                    v-for="(month, index) in months"
                    :key="month"
                    :variant="index + 1 === currentMonth ? 'flat' : 'text'"
                    :color="index + 1 === currentMonth ? 'primary' : undefined"
                    class="selection-item"
                    @click="selectMonth(index)"
                  >
                    {{ month }}
                  </v-btn>
                </div>

                <!-- Days Calendar -->
                <div v-else class="calendar-view">
                  <div class="weekdays-row mb-2">
                    <span v-for="day in daysOfWeek" :key="day" class="weekday-label">
                      {{ day }}
                    </span>
                  </div>
                  <div class="days-grid">
                    <div
                      v-for="(day, i) in daysInMonth"
                      :key="i"
                      class="day-cell-wrapper"
                    >
                      <v-btn
                        v-if="day.date"
                        icon
                        :variant="isSelected(day.date) ? 'flat' : 'text'"
                        :color="
                          isSelected(day.date)
                            ? 'primary'
                            : isToday(day.date)
                            ? 'primary'
                            : undefined
                        "
                        :class="[
                          'day-btn',
                          {
                            'today-border': isToday(day.date) && !isSelected(day.date),
                          },
                        ]"
                        size="small"
                        @click="selectDate(day.date)"
                      >
                        {{ day.day }}
                      </v-btn>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Time View -->
              <div v-else-if="displayMode === 'time'" class="time-view">
                <div class="time-scroller-container">
                  <!-- Hour Scroller -->
                  <div class="time-column">
                    <div class="time-column-label">{{ translations.hh }}</div>
                    <div
                      class="modern-time-scroller"
                      ref="hourScroller"
                      @scroll.passive="handleScroll($event, 'hour')"
                    >
                      <div
                        v-for="h in 24"
                        :key="h"
                        class="time-item"
                        :class="{ active: selectedHour === h - 1 }"
                        @click="selectTimeItem('hour', h - 1)"
                      >
                        {{ String(h - 1).padStart(2, "0") }}
                      </div>
                    </div>
                  </div>

                  <div class="time-separator">:</div>

                  <!-- Minute Scroller -->
                  <div class="time-column">
                    <div class="time-column-label">{{ translations.mm }}</div>
                    <div
                      class="modern-time-scroller"
                      ref="minuteScroller"
                      @scroll.passive="handleScroll($event, 'minute')"
                    >
                      <div
                        v-for="m in 60"
                        :key="m"
                        class="time-item"
                        :class="{ active: selectedMinute === m - 1 }"
                        @click="selectTimeItem('minute', m - 1)"
                      >
                        {{ String(m - 1).padStart(2, "0") }}
                      </div>
                    </div>
                  </div>

                  <div class="time-separator">:</div>

                  <!-- Second Scroller -->
                  <div class="time-column">
                    <div class="time-column-label">{{ translations.ss }}</div>
                    <div
                      class="modern-time-scroller"
                      ref="secondScroller"
                      @scroll.passive="handleScroll($event, 'second')"
                    >
                      <div
                        v-for="s in 60"
                        :key="s"
                        class="time-item"
                        :class="{ active: selectedSecond === s - 1 }"
                        @click="selectTimeItem('second', s - 1)"
                      >
                        {{ String(s - 1).padStart(2, "0") }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer Actions -->
          <div
            class="actions-bar d-flex align-center justify-space-between flex-wrap gap-2"
          >
            <v-btn variant="text" color="primary" @click="selectTodayAndConfirm">
              {{ translations.today }}
            </v-btn>
            <div class="d-flex align-center gap-2">
              <v-btn variant="text" color="grey-darken-1" @click="cancelSelection">
                {{ translations.cancel }}
              </v-btn>
              <v-btn
                variant="elevated"
                color="primary"
                size="small"
                class="px-4"
                @click="confirmSelection"
              >
                {{ translations.ok }}
              </v-btn>
            </div>
          </div>
        </v-card>
      </v-menu>

      <!-- Mobile Selection Dialog -->
      <v-dialog
        v-else
        v-model="showPicker"
        :activator="activatorRef"
        max-width="360"
        class="mobile-datepicker-dialog"
        :z-index="9999"
      >
        <v-card class="v-date-picker-card">
          <!-- Calendar Header -->
          <div class="v-date-picker-header bg-primary text-white">
            <div
              class="d-flex align-center justify-space-between w-100"
              :class="{ 'flex-row-reverse': language === 'ar' }"
            >
              <div
                class="header-year-text cursor-pointer"
                :class="{ 'header-text-active': isYearSelection }"
                @click="toggleYearSelection"
              >
                {{ currentYear }}
              </div>
              <div class="d-flex align-center gap-x-4">
                <div
                  class="header-date-text cursor-pointer"
                  :class="{
                    'header-text-active':
                      displayMode === 'date' && !isYearSelection && !isMonthSelection,
                  }"
                  @click="
                    displayMode = 'date';
                    isYearSelection = false;
                    isMonthSelection = false;
                  "
                >
                  {{ headerDateText }}
                </div>
                <div
                  v-if="withTime"
                  class="header-date-text ml-4 cursor-pointer"
                  :class="{ 'header-text-active': displayMode === 'time' }"
                  @click="
                    displayMode = 'time';
                    isYearSelection = false;
                    isMonthSelection = false;
                  "
                >
                  {{ formattedTime }}
                </div>
              </div>
            </div>
          </div>

          <div class="datepicker-container">
            <div class="picker-content">
              <template v-if="displayMode === 'date'">
                <div class="navigation-row px-1 mb-4">
                  <div class="d-flex align-center flex-grow-1 overflow-hidden">
                    <v-btn
                      variant="text"
                      density="compact"
                      class="nav-label-btn px-2"
                      @click="toggleMonthSelection"
                    >
                      <span class="text-truncate">{{ currentMonth }}</span>
                    </v-btn>
                    <v-btn
                      variant="text"
                      density="compact"
                      class="nav-label-btn px-2"
                      @click="toggleYearSelection"
                      >{{ currentYear }}</v-btn
                    >
                  </div>
                  <div class="d-flex flex-shrink-0">
                    <v-btn
                      icon="mdi-chevron-right"
                      variant="text"
                      size="small"
                      @click="
                        isYearSelection || isMonthSelection
                          ? prevYearsOrMonths()
                          : prevMonth()
                      "
                    />
                    <v-btn
                      icon="mdi-chevron-left"
                      variant="text"
                      size="small"
                      @click="
                        isYearSelection || isMonthSelection
                          ? nextYearsOrMonths()
                          : nextMonth()
                      "
                    />
                  </div>
                </div>

                <!-- Selection Grids for Mobile -->
                <div v-if="isYearSelection" class="selection-grid year-grid">
                  <v-btn
                    v-for="year in visibleYears"
                    :key="year"
                    :variant="year === currentYear ? 'flat' : 'text'"
                    :color="year === currentYear ? 'primary' : undefined"
                    class="selection-item"
                    @click="selectYear(year)"
                  >
                    {{ year }}
                  </v-btn>
                </div>

                <div v-else-if="isMonthSelection" class="selection-grid month-grid">
                  <v-btn
                    v-for="(month, index) in months"
                    :key="month"
                    :variant="index + 1 === currentMonth ? 'flat' : 'text'"
                    :color="index + 1 === currentMonth ? 'primary' : undefined"
                    class="selection-item"
                    @click="selectMonth(index)"
                  >
                    {{ month }}
                  </v-btn>
                </div>

                <!-- Days Calendar -->
                <div v-else class="calendar-view">
                  <div class="weekdays-row mb-2">
                    <span v-for="day in daysOfWeek" :key="day" class="weekday-label">{{
                      day
                    }}</span>
                  </div>
                  <div class="days-grid">
                    <div
                      v-for="(day, i) in daysInMonth"
                      :key="i"
                      class="day-cell-wrapper"
                    >
                      <v-btn
                        v-if="day.date"
                        icon
                        :variant="isSelected(day.date) ? 'flat' : 'text'"
                        :color="
                          isSelected(day.date)
                            ? 'primary'
                            : isToday(day.date)
                            ? 'primary'
                            : undefined
                        "
                        class="day-btn"
                        size="small"
                        @click="selectDate(day.date)"
                        >{{ day.day }}</v-btn
                      >
                    </div>
                  </div>
                </div>
              </template>
              <!-- Time View for Mobile -->
              <div v-else-if="displayMode === 'time'" class="time-view">
                <div class="time-scroller-container">
                  <!-- Hour Scroller -->
                  <div class="time-column">
                    <div class="time-column-label">{{ translations.hh }}</div>
                    <div
                      class="modern-time-scroller"
                      ref="hourScroller"
                      @scroll.passive="handleScroll($event, 'hour')"
                    >
                      <div
                        v-for="h in 24"
                        :key="h"
                        class="time-item"
                        :class="{ active: selectedHour === h - 1 }"
                        @click="selectTimeItem('hour', h - 1)"
                      >
                        {{ String(h - 1).padStart(2, "0") }}
                      </div>
                    </div>
                  </div>

                  <div class="time-separator">:</div>

                  <!-- Minute Scroller -->
                  <div class="time-column">
                    <div class="time-column-label">{{ translations.mm }}</div>
                    <div
                      class="modern-time-scroller"
                      ref="minuteScroller"
                      @scroll.passive="handleScroll($event, 'minute')"
                    >
                      <div
                        v-for="m in 60"
                        :key="m"
                        class="time-item"
                        :class="{ active: selectedMinute === m - 1 }"
                        @click="selectTimeItem('minute', m - 1)"
                      >
                        {{ String(m - 1).padStart(2, "0") }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            class="actions-bar d-flex align-center justify-space-between flex-wrap gap-2"
          >
            <v-btn variant="text" color="primary" @click="selectTodayAndConfirm">{{
              translations.today
            }}</v-btn>
            <div class="d-flex align-center gap-2">
              <v-btn variant="text" color="grey-darken-1" @click="cancelSelection">{{
                translations.cancel
              }}</v-btn>
              <v-btn variant="elevated" color="primary" @click="confirmSelection">{{
                translations.ok
              }}</v-btn>
            </div>
          </div>
        </v-card>
      </v-dialog>
    </div>
  </v-col>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import moment from "moment-hijri";
import { format, addMonths, subMonths } from "date-fns";

const props = defineProps({
  initialType: { type: String, default: "DD" },
  withTime: { type: Boolean, default: false },
  modelValue: { type: String, default: null },
  language: { type: String, default: "ar" },
  format: { type: String, default: "" },
  label: { type: String, default: "" },
  cols: { type: [Number, String], default: 12 },
  rules: { type: Array, default: () => [] },
  hideDetails: { type: [String, Boolean], default: false },

  icon: { type: String, default: "calendar-outline" },
  rounded: { type: Boolean, default: false },
  variant: { type: String, default: "outlined" },
  disabled: { type: Boolean, default: false },
});

const emit = defineEmits(["update:modelValue", "cancel"]);

const isHijri = ref(props.initialType === "hijri");
const showPicker = ref(false);
const activatorRef = ref(null);
const currentDate = ref(isHijri.value ? moment().startOf("day").toDate() : new Date());
const selectedDate = ref(currentDate.value);
const selectedHour = ref(0);
const selectedMinute = ref(0);
const selectedSecond = ref(0);
const isYearSelection = ref(false);
const isMonthSelection = ref(false);
const yearRangeStart = ref(isHijri.value ? 1440 : 2020);
const isMobile = ref(false);
const displayMode = ref("date");

// Scroller Refs
const hourScroller = ref(null);
const minuteScroller = ref(null);
const secondScroller = ref(null);

const scrollToSelected = () => {
  setTimeout(() => {
    const itemHeight = 48; // Matches CSS .time-item height
    if (hourScroller.value) {
      hourScroller.value.scrollTop = selectedHour.value * itemHeight;
    }
    if (minuteScroller.value) {
      minuteScroller.value.scrollTop = selectedMinute.value * itemHeight;
    }
    if (secondScroller.value) {
      secondScroller.value.scrollTop = selectedSecond.value * itemHeight;
    }
  }, 0);
};

const selectTimeItem = (type, val) => {
  if (type === "hour") selectedHour.value = val;
  else if (type === "minute") selectedMinute.value = val;
  else if (type === "second") selectedSecond.value = val;
  scrollToSelected();
};

const handleScroll = (event, type) => {
  const scrollTop = event.target.scrollTop;
  const itemHeight = 48;
  const index = Math.round(scrollTop / itemHeight);

  if (type === "hour" && index >= 0 && index < 24) {
    selectedHour.value = index;
  } else if (type === "minute" && index >= 0 && index < 60) {
    selectedMinute.value = index;
  } else if (type === "second" && index >= 0 && index < 60) {
    selectedSecond.value = index;
  }
};

watch(displayMode, (val) => {
  if (val === "time") {
    scrollToSelected();
  }
});

watch(showPicker, (val) => {
  if (val) {
    displayMode.value = "date";
    initializeDate();
  }
});

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 600;
};

const translations = computed(() => {
  return props.language === "ar"
    ? {
        ok: "موافق",
        cancel: "إلغاء",
        today: "اليوم",
        selectDatePlaceholder: "انقر لاختيار التاريخ",
        hh: "ساعة",
        mm: "دقيقة",
        ss: "ثانية",
        monthsGregorian: [
          "يناير",
          "فبراير",
          "مارس",
          "أبريل",
          "مايو",
          "يونيو",
          "يوليو",
          "أغسطس",
          "سبتمبر",
          "أكتوبر",
          "نوفمبر",
          "ديسمبر",
        ],
        monthsHijri: [
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
        ],
        daysOfWeek: ["ح", "ن", "ث", "ر", "خ", "ج", "س"],
      }
    : {
        ok: "OK",
        cancel: "Cancel",
        today: "Today",
        selectDatePlaceholder: "Click to select date",
        hh: "HH",
        mm: "MM",
        ss: "SS",
        monthsGregorian: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        monthsHijri: [
          "Muharram",
          "Safar",
          "Rabi' I",
          "Rabi' II",
          "Jumada I",
          "Jumada II",
          "Rajab",
          "Sha'ban",
          "Ramadan",
          "Shawwal",
          "Dhu al-Qi'dah",
          "Dhu al-Hijjah",
        ],
        daysOfWeek: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
      };
});

const formattedDate = computed(() => {
  if (!props.modelValue) return null;
  const date = parseModelValue(props.modelValue);
  if (!date) return props.modelValue;
  if (isHijri.value) {
    let fmt = props.withTime ? "iYYYY-iMM-iDD HH:mm:ss" : "iYYYY-iMM-iDD";
    return moment(date).format(fmt);
  } else {
    let fmt = props.withTime ? "yyyy-MM-dd HH:mm:ss" : "yyyy-MM-dd";
    return format(date, fmt);
  }
});

const headerDateText = computed(() => {
  if (isHijri.value) {
    return moment(selectedDate.value).format("iDD iMMMM");
  } else {
    return format(selectedDate.value, "dd MMMM");
  }
});

const formattedTime = computed(() => {
  return `${pad(selectedHour.value)}:${pad(selectedMinute.value)}`;
});

const currentYear = computed(() => {
  return isHijri.value
    ? moment(currentDate.value).iYear()
    : currentDate.value.getFullYear();
});

const currentMonth = computed(() => {
  const m = isHijri.value
    ? moment(currentDate.value).iMonth()
    : currentDate.value.getMonth();
  return months.value[m];
});

const months = computed(() =>
  isHijri.value ? translations.value.monthsHijri : translations.value.monthsGregorian
);
const daysOfWeek = computed(() => translations.value.daysOfWeek);

const visibleYears = computed(() => {
  const years = [];
  for (let i = 0; i < 12; i++) {
    years.push(yearRangeStart.value + i);
  }
  return years;
});

const daysInMonth = computed(() => {
  const days = [];
  if (isHijri.value) {
    const m = moment(currentDate.value).startOf("iMonth");
    const firstDay = m.day();
    const daysCount = moment.iDaysInMonth(m.iYear(), m.iMonth());
    for (let i = 0; i < firstDay; i++) days.push({ day: null, date: null });
    for (let i = 1; i <= daysCount; i++) {
      const d = moment(m).iDate(i).toDate();
      days.push({ day: i, date: d });
    }
  } else {
    const start = new Date(
      currentDate.value.getFullYear(),
      currentDate.value.getMonth(),
      1
    );
    const firstDay = start.getDay();
    const lastDay = new Date(
      currentDate.value.getFullYear(),
      currentDate.value.getMonth() + 1,
      0
    ).getDate();
    for (let i = 0; i < firstDay; i++) days.push({ day: null, date: null });
    for (let i = 1; i <= lastDay; i++) {
      const d = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth(),
        i
      );
      days.push({ day: i, date: d });
    }
  }
  return days;
});

const pad = (n) => String(n).padStart(2, "0");

const prevMonth = () => {
  currentDate.value = isHijri.value
    ? moment(currentDate.value).subtract(1, "iMonth").toDate()
    : subMonths(currentDate.value, 1);
};

const nextMonth = () => {
  currentDate.value = isHijri.value
    ? moment(currentDate.value).add(1, "iMonth").toDate()
    : addMonths(currentDate.value, 1);
};

const toggleYearSelection = () => {
  isYearSelection.value = !isYearSelection.value;
  isMonthSelection.value = false;
};

const toggleMonthSelection = () => {
  isMonthSelection.value = !isMonthSelection.value;
  isYearSelection.value = false;
};

const selectYear = (year) => {
  if (isHijri.value) {
    currentDate.value = moment(currentDate.value).iYear(year).toDate();
  } else {
    const d = new Date(currentDate.value);
    d.setFullYear(year);
    currentDate.value = d;
  }
  isYearSelection.value = false;
};

const selectMonth = (monthIndex) => {
  if (isHijri.value) {
    currentDate.value = moment(currentDate.value).iMonth(monthIndex).toDate();
  } else {
    const d = new Date(currentDate.value);
    d.setMonth(monthIndex);
    currentDate.value = d;
  }
  isMonthSelection.value = false;
};

const prevYearsOrMonths = () => {
  yearRangeStart.value -= 12;
};
const nextYearsOrMonths = () => {
  yearRangeStart.value += 12;
};

const selectDate = (date) => {
  selectedDate.value = date;
};

const selectToday = () => {
  const today = new Date();
  selectedDate.value = today;
  currentDate.value = today;
};

const selectTodayAndConfirm = () => {
  selectToday();
  confirmSelection();
};

const confirmSelection = () => {
  const finalDate = new Date(selectedDate.value);
  finalDate.setHours(selectedHour.value, selectedMinute.value, selectedSecond.value);
  let result = "";
  if (isHijri.value) {
    result = moment(finalDate).format(
      props.withTime ? "iYYYY-iMM-iDD HH:mm:ss" : "iYYYY-iMM-iDD"
    );
  } else {
    result = format(finalDate, props.withTime ? "yyyy-MM-dd HH:mm:ss" : "yyyy-MM-dd");
  }
  emit("update:modelValue", result);
  showPicker.value = false;
};

const cancelSelection = () => {
  showPicker.value = false;
  emit("cancel");
};

const clearDate = () => {
  emit("update:modelValue", null);
};

const switchCalendar = () => {
  isHijri.value = !isHijri.value;
  // Recalculate year range
  const curY = isHijri.value
    ? moment(currentDate.value).iYear()
    : currentDate.value.getFullYear();
  yearRangeStart.value = curY - (curY % 12);
};

const isSelected = (date) => {
  if (!date || !selectedDate.value) return false;
  return date.toDateString() === selectedDate.value.toDateString();
};

const isToday = (date) => {
  if (!date) return false;
  return date.toDateString() === new Date().toDateString();
};

const parseModelValue = (val) => {
  if (!val) return null;
  if (isHijri.value) {
    const m = moment(val, props.withTime ? "iYYYY-iMM-iDD HH:mm:ss" : "iYYYY-iMM-iDD");
    return m.isValid() ? m.toDate() : null;
  } else {
    const d = new Date(val);
    return isNaN(d.getTime()) ? null : d;
  }
};

const initializeDate = () => {
  const parsed = parseModelValue(props.modelValue);
  if (parsed) {
    selectedDate.value = parsed;
    selectedHour.value = parsed.getHours();
    selectedMinute.value = parsed.getMinutes();
    selectedSecond.value = parsed.getSeconds();
    currentDate.value = parsed;
  }
  const curY = isHijri.value
    ? moment(currentDate.value).iYear()
    : currentDate.value.getFullYear();
  yearRangeStart.value = curY - (curY % 12);
};

const containerStyle = computed(() => {
  const style = { width: "100%", maxWidth: "100%" };
  if (typeof props.col === "number") {
    style.maxWidth = (Math.min(Math.max(props.col, 1), 12) / 12) * 100 + "%";
  } else if (typeof props.col === "string" && props.col.trim()) {
    style.maxWidth = props.col;
  }
  return style;
});

const isRequired = ref(false);
onMounted(() => {
  initializeDate();
  checkMobile();
  window.addEventListener("resize", checkMobile);

  if (props.rules)
    props.rules?.forEach((e) => {
      if (typeof e === "function")
        if (e() == "هذا الحقل مطلوب" || e() === "This field is required")
          isRequired.value = true;
    });
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", checkMobile);
});
</script>

<style scoped>
.date-picker-wrapper {
  width: 100%;
  position: relative;
  font-family: "Inter", system-ui, -apple-system, sans-serif;
}

.custom-datepicker-input :deep(.v-field__outline) {
  transition: var(--transition-hover);
}

.custom-datepicker-input:hover :deep(.v-field__outline) {
  --v-field-border-opacity: 0.9;
}

.custom-datepicker-input :deep(.v-field--focused .v-field__outline) {
  box-shadow: none !important;
  color: inherit !important;
}

.no-focus-border :deep(.v-field--focused .v-field__outline) {
  --v-field-border-width: 1px !important;
  --v-field-border-opacity: 0.38 !important;
}

.custom-datepicker-input :deep(.v-label) {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.1px;
}

.datepicker-icon {
  opacity: 0.45;
  transition: var(--transition-hover);
}

.custom-datepicker-input :deep(.v-field--focused .datepicker-icon) {
  opacity: 1;
  color: var(--color-primary);
}

.clear-icon {
  opacity: 0.4;
  transition: var(--transition-hover);
}

.clear-icon:hover {
  opacity: 1;
  color: var(--color-error);
}

.v-date-picker-card {
  border-radius: var(--radius-xl) !important;
  overflow: hidden;
  background: var(--color-surface);
  box-shadow: var(--shadow-xl) !important;
  border: 1px solid rgba(var(--shadow-key-umbra-color), 0.08) !important;
}

.v-date-picker-header {
  padding: var(--space-md) var(--space-lg) !important;
  position: relative;
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    var(--color-primary-darken) 100%
  ) !important;
  display: flex !important;
  height: auto !important;
  grid-template-areas: none !important;
  grid-template-columns: none !important;
  align-items: center !important;
}

.v-date-picker-header::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at top right,
    rgba(255, 255, 255, 0.15) 0%,
    transparent 70%
  );
  pointer-events: none;
}

.header-year-text {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  opacity: 0.75;
  letter-spacing: 1px;
  margin-bottom: 2px;
}

.header-main-text {
  line-height: 1.3;
}

.header-date-text {
  font-size: 1.55rem;
  font-weight: 700;
  opacity: 0.5;
  transition: all 0.2s ease;
  white-space: normal;
  display: inline-block;
}

.header-date-text:hover {
  opacity: 0.85;
}

.header-text-active {
  opacity: 1 !important;
}

.datepicker-container {
  padding: var(--space-md);
  min-height: 320px;
}

.picker-content {
  animation: dp-slide-in var(--motion-duration-normal) var(--motion-easing-out);
}

@keyframes dp-slide-in {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.navigation-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-md);
  min-height: 40px;
}

.nav-label-btn {
  font-weight: 700;
  letter-spacing: 0.3px;
  max-width: 140px;
}

.nav-arrow-btn {
  color: var(--color-secondary);
}

.calendar-view {
  display: flex;
  flex-direction: column;
}

.weekdays-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
}

.weekday-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-secondary);
  opacity: 0.7;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.day-cell-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  aspect-ratio: 1;
}

.day-btn {
  width: 36px !important;
  height: 36px !important;
  border-radius: var(--radius-lg) !important;
  font-weight: 600;
  font-size: 0.9rem;
  transition: var(--transition-hover);
}

.day-btn:hover {
  /* background: rgba(var(--v-theme-primary), 0.08) !important; */
}

.day-btn.v-btn--active {
  box-shadow: 0 4px 10px rgba(var(--v-theme-primary), 0.3) !important;
}

.today-border {
  border: 2px solid rgba(var(--v-theme-primary), 0.35) !important;
}

.selection-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 4px;
}

.selection-item {
  height: 52px !important;
  font-weight: 600;
  letter-spacing: 0.3px;
  border-radius: var(--radius-md) !important;
  transition: all 0.2s ease !important;
}

.selection-item:hover:not(.v-btn--active) {
  background-color: rgba(var(--v-theme-primary), 0.05) !important;
}

.time-view {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  position: relative;
  overflow: hidden;
}

/* ── Autofill Flash Prevention ───────────────────────── */
.no-autofill-bg :deep(input:-webkit-autofill),
.no-autofill-bg :deep(input:-webkit-autofill:hover),
.no-autofill-bg :deep(input:-webkit-autofill:focus),
.no-autofill-bg :deep(input:-webkit-autofill:active) {
  -webkit-text-fill-color: inherit !important;
  transition: background-color 5000s ease-in-out 0s !important;
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
}

/* ── Label Typography ────────────────────────────────── */
.no-autofill-bg :deep(.v-label) {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.1px;
}

/* ── Placeholder ─────────────────────────────────────── */
.no-autofill-bg :deep(input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.35);
  font-size: 0.875rem;
}

/* ── Input Text ──────────────────────────────────────── */
.no-autofill-bg :deep(.v-field__input) {
  font-size: 0.9rem;
  line-height: 1.5;
}

.datepicker-icon {
  opacity: 0.5;
  font-size: 1.2rem;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.no-autofill-bg :deep(.v-field--focused .datepicker-icon) {
  opacity: 1;
  color: rgb(var(--v-theme-primary));
}

.clear-icon {
  opacity: 0.4;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.clear-icon:hover {
  opacity: 1;
  color: rgb(var(--v-theme-error));
}

.date-picker-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
}

.time-scroller-container {
  display: flex;
  align-items: flex-end;
  /* Align scrollers to bottom */
  gap: 24px;
  position: relative;
  z-index: 1;
  padding: 0 10px;
}

/* Selector Indicator Bar - Aligned exactly with the center item */
.time-scroller-container::before {
  content: "";
  position: absolute;
  bottom: 76px;
  /* Exactly matches the .modern-time-scroller padding-bottom */
  left: 0;
  right: 0;
  height: 48px;
  /* Matches .time-item height */
  background: rgba(var(--v-theme-primary), 0.05);
  border-top: 1px solid rgba(var(--v-theme-primary), 0.12);
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.12);
  border-radius: var(--radius-md);
  pointer-events: none;
  z-index: -1;
}

.time-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50px;
}

.time-column-label {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 12px;
  letter-spacing: 1px;
  opacity: 0.6;
}

.modern-time-scroller {
  height: 200px;
  width: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 76px 0;
  /* (200 - 48) / 2 = 76px */
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    black 25%,
    black 75%,
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    black 25%,
    black 75%,
    transparent 100%
  );
}

.modern-time-scroller::-webkit-scrollbar {
  display: none;
}

.time-item {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: var(--color-secondary);
  opacity: 0.4;
  cursor: pointer;
  transition: all var(--motion-duration-normal) var(--motion-easing-standard);
  font-weight: 500;
  border-radius: var(--radius-sm);
  scroll-snap-align: center;
}

.time-item:hover:not(.active) {
  opacity: 0.7;
}

.time-item.active {
  font-size: 1.85rem;
  font-weight: 800;
  color: var(--color-primary);
  opacity: 1;
  text-shadow: 0 0 20px rgba(var(--v-theme-primary), 0.2);
}

.time-separator {
  font-size: 1.8rem;
  font-weight: 300;
  color: var(--color-primary);
  opacity: 0.5;
  height: 200px;
  /* Match scroller height */
  display: flex;
  align-items: center;
  /* Center colon vertically relative to scroller */
  padding-top: 4px;
  /* Tiny adjustment for font baseline */
}

.actions-bar {
  padding: 16px 24px;
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.v-date-picker-card {
  border-radius: var(--radius-lg) !important;
  overflow: hidden;
  box-shadow: var(--shadow-lg) !important;
  border: none !important;
}

.mobile-datepicker-dialog .v-date-picker-card {
  box-shadow: none !important;
  border-radius: 0 !important;
  height: 100%;
}

@media (max-width: 600px) {
  .day-btn {
    width: 32px !important;
    height: 32px !important;
  }

  .v-date-picker-header {
    padding: 16px 20px;
  }
}
</style>
