<template>
  <div class="ums-cards-page" dir="rtl">
    <VContainer class="container" height="100%">
      <!-- Header Section -->
      <header class="page-header">
        <div class="header-accent"></div>
        <div class="header-content">
          <p class="header-label">لوحة التحكم الرئيسية</p>
          <h1>{{ `أنظمة ${$t("systemName")}` }}</h1>

          <!-- <p class="header-desc">
            منصة متكاملة لأتمتة العمليات الأكاديمية والإدارية والمالية داخل المؤسسات
            التعليمية، ترفع كفاءة الأداء وتحسّن تجربة جميع المستخدمين.
          </p> -->
        </div>
      </header>

      <!-- Modules Grid -->
      <div class="cards-grid">
        <div
          v-for="(card, index) in cards"
          :key="card.id"
          class="card"
          :class="{ 'card-dark': card.isDark }"
          @click="handleCardClick(card)"
          role="button"
          tabindex="0"
        >
          <template v-if="!card.isDark">
            <!-- Watermark background icon -->
            <div class="card-bg-icon">
              <v-icon>{{ card.icon }}</v-icon>
            </div>
            <!-- Card number badge -->
            <span class="card-index">{{ String(index + 1).padStart(2, "0") }}</span>
            <div class="card-header">
              <div class="icon-wrapper">
                <v-icon size="22" class="icon">{{ card.icon }}</v-icon>
              </div>
              <h2>{{ card.name_ar }}</h2>
            </div>
            <p class="card-desc">{{ card.description }}</p>
            <div class="card-footer">
              <span class="card-cta">عرض النظام</span>
              <v-icon size="16" class="cta-arrow">mdi-arrow-left</v-icon>
            </div>
          </template>
          <template v-else>
            <div class="card-bg-icon dark-bg-icon">
              <v-icon>mdi-school</v-icon>
            </div>
            <div class="dark-logo">
              <v-icon size="38" class="dark-icon">mdi-school</v-icon>
            </div>
            <h2>{{ card.name_ar }}</h2>
            <p class="dark-subtitle">نظام إدارة تعليمي متكامل</p>
          </template>
        </div>
      </div>
    </VContainer>
  </div>
</template>

<script setup>
import { state } from "@/store/state";
import { ref, onMounted } from "vue";
import { getRouter } from "../router/routerInstance"; // إضافة الـ Router
import shared from "external-components";
const router = getRouter();

// تعريف الأحداث (Events) التي يمكن للمكون الأب الاستماع إليها (اختياري)
const emit = defineEmits(["cardClick"]);

const handleCardClick = (card) => {
  state.current_system = card.id;
  setTimeout(() => {
    router.push({ path: "/" });
  }, 1000);

  // 1. إرسال حدث للمكون الأب في حال أردت استخدامه: @cardClick="..."
  emit("cardClick", card);

  // // 2. الانتقال إلى الصفحة المحددة عبر الـ Router
  // // سيقوم بالانتقال فقط إذا قمت بتحديد مسار للبطاقة (routePath أو routeName)
  // if (card.routePath) {
  //     router.push({ path: card.routePath });
  // } else if (card.routeName) {
  //     router.push({ name: card.routeName });
  // }
};

// بيانات البطاقات
const cards = ref([]);

const getSystems = async () => {
  const response = await shared.api("screens/systems/");
  cards.value = response?.data?.data;
};
onMounted(() => {
  getSystems();
});
</script>

<style scoped>
/* ===================== DESIGN TOKENS ===================== */
.ums-cards-page {
  --primary: #1a365d;
  --primary-mid: #2b4c7e;
  --blue: #164de4;
  --primary-pale: #eef2f8;
  --gold: #c8872a;
  --gold-light: #e4a740;
  --text-dark: #1e2d42;
  --text-mid: #4a5568;
  --text-soft: #8898aa;
  --surface: #ffffff;
  --surface-alt: #f7f9fc;
  --border: #dde4ef;
  --radius: 12px;
  --shadow-sm: 0 2px 8px rgba(26, 54, 93, 0.06);
  --shadow-md: 0 8px 28px rgba(26, 54, 93, 0.12);
  --shadow-lg: 0 20px 50px rgba(26, 54, 93, 0.16);
  --speed: 0.3s;

  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  /* background-color: var(--surface-alt); */
  /* color: var(--text-dark); */
  -webkit-font-smoothing: antialiased;
  padding: 40px 24px 60px;
  min-height: 100vh;
}
.ums-cards-page * {
  box-sizing: border-box;
}

/* ===================== SCROLL CONTAINER ===================== */
.container {
  max-width: 1260px;
  margin: 0 auto;
  max-height: 100vh;
  overflow-y: auto;
  padding-bottom: 80px;
}
.container::-webkit-scrollbar {
  display: none;
}

/* ===================== HEADER ===================== */
.page-header {
  display: flex;
  align-items: stretch;
  gap: 22px;
  margin-bottom: 48px;
  padding: 32px 36px;
  background-color: rgb(var(--v-theme-surface, 31, 41, 55));
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  position: relative;
  overflow: hidden;
}

/* subtle background shape */
.page-header::after {
  content: "SYS";
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%) rotate(-15deg);
  font-size: 7rem;
  font-weight: 900;
  /* color: var(--primary); */
  opacity: 0.03;
  letter-spacing: -4px;
  pointer-events: none;
  user-select: none;
}

.header-accent {
  width: 5px;
  border-radius: 4px;
  background: linear-gradient(180deg, var(--gold) 0%, var(--primary-mid) 100%);
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.header-label {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--gold);
  margin: 0 0 8px;
}

.page-header h1 {
  font-size: 1.85rem;
  font-weight: 800;
  /* color: var(--primary); */
  margin: 0 0 10px;
  line-height: 1.25;
}

.header-desc {
  font-size: 0.97rem;
  /* color: var(--text-mid); */
  line-height: 1.75;
  margin: 0;
  max-width: 7000px;
}

/* ===================== GRID ===================== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}
@media (min-width: 1024px) {
  .cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ===================== CARD BASE ===================== */
.card {
  /* background: var(--surface); */
  background-color: rgb(var(--v-theme-surface, 31, 41, 55));
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 28px 24px 22px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: transform var(--speed) ease, box-shadow var(--speed) ease,
    border-color var(--speed) ease;
}

/* top accent line */
.card::after {
  content: "";
  position: absolute;
  top: 0;
  right: 30%;
  left: 30%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-mid), var(--primary));
  border-radius: var(--radius) var(--radius) 0 0;
  transition: left var(--speed) ease, right var(--speed) ease;
}

/* .card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
} */
.card:hover::after {
  left: 0;
  right: 0;
}
.card:focus {
  outline: 1px solid var(--blue);
}

/* ===================== CARD NUMBER BADGE ===================== */
.card-index {
  position: absolute;
  left: 18px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 1px;
  /* color: var(--text-soft); */
  opacity: 0.5;
  transition: opacity var(--speed) ease;
}
.card:hover .card-index {
  opacity: 0.9;
}

/* ===================== WATERMARK ICON ===================== */
.card-bg-icon {
  position: absolute;
  bottom: -22px;
  left: -14px;
  pointer-events: none;
  opacity: 0.05;
  transition: opacity var(--speed) ease, transform var(--speed) ease;
}
.card-bg-icon .v-icon {
  /* color: var(--primary) !important; */
  font-size: 120px !important;
}
.card:hover .card-bg-icon {
  opacity: 0.09;
  transform: scale(1.1) rotate(-6deg);
}

/* ===================== CARD HEADER ===================== */
.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.icon-wrapper {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: var(--primary-pale);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background var(--speed) ease, transform var(--speed) ease;
}

.icon-wrapper .icon {
  /* color: var(--primary-mid) !important; */
  transition: color var(--speed) ease;
}

.card:hover .icon-wrapper {
  /* background: var(--primary); */
  transform: rotate(6deg) scale(1.05);
}
.card:hover .icon-wrapper .icon {
  /* color: #ffffff !important; */
}

.card-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  /* color: var(--text-dark); */

  margin: 0;
  transition: color var(--speed) ease;
  line-height: 1.3;
}
/* .card:hover .card-header h2 { color: var(--primary); } */

/* ===================== CARD DESCRIPTION ===================== */
.card-desc {
  font-size: 0.88rem;
  /* color: var(--text-mid); */
  line-height: 1.75;
  margin: 0 0 18px;
  flex: 1;
}

/* ===================== CARD FOOTER CTA ===================== */
.card-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid var(--border);
  transition: border-color var(--speed) ease;
}
.card:hover .card-footer {
  border-color: var(--primary-pale);
}

.card-cta {
  font-size: 0.8rem;
  font-weight: 600;
  /* color: var(--text-soft); */
  letter-spacing: 0.5px;
  transition: color var(--speed) ease;
}
.cta-arrow {
  /* color: var(--text-soft) !important; */
  transition: color var(--speed) ease, transform var(--speed) ease !important;
}
/* .card:hover .card-cta { color: var(--primary-mid); } */
.card:hover .cta-arrow {
  color: var(--gold) !important;
  transform: translateX(-4px);
}

/* ===================== DARK CARD ===================== */
.card.card-dark {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-mid) 100%);
  border-color: transparent;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 190px;
}

.dark-bg-icon {
  bottom: -24px;
  left: -18px;
  opacity: 0.07;
}
.dark-bg-icon .v-icon {
  /* color: var(--gold) !important; */
  font-size: 140px !important;
}
.card-dark:hover .dark-bg-icon {
  opacity: 0.14;
  transform: scale(1.12) rotate(-7deg);
}

.dark-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1.5px solid rgba(255, 255, 255, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  transition: background var(--speed) ease, transform var(--speed) ease;
}
.card-dark:hover .dark-logo {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.08);
}

/* .dark-icon { color: var(--gold-light) !important; } */

.card.card-dark h2 {
  font-size: 1.55rem;
  font-weight: 800;
  /* color: #ffffff; */
  margin: 0 0 6px;
  letter-spacing: 0.5px;
  transition: transform var(--speed) ease;
}
.card-dark:hover h2 {
  transform: scale(1.04);
}

.dark-subtitle {
  font-size: 0.78rem;
  /* color: rgba(255,255,255,0.55); */
  margin: 0;
  letter-spacing: 0.8px;
}

.card.card-dark:hover,
.card.card-dark:focus {
  box-shadow: 0 20px 50px rgba(26, 54, 93, 0.3);
}
.dark-bg-icon .v-icon {
  color: var(--gold) !important;
  font-size: 140px !important;
}
.card-dark:hover .dark-bg-icon {
  opacity: 0.14;
  transform: scale(1.12) rotate(-7deg);
}

.dark-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1.5px solid rgba(255, 255, 255, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  transition: background var(--speed) ease, transform var(--speed) ease;
}
.card-dark:hover .dark-logo {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.08);
}

.dark-icon {
  color: var(--gold-light) !important;
}

/* ===================== RESPONSIVE ===================== */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    padding: 24px 20px;
  }
  .header-accent {
    width: 100%;
    height: 4px;
  }
  .page-header h1 {
    font-size: 1.5rem;
  }
  .cards-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }
  .card {
    padding: 22px 18px 18px;
  }
}
</style>
