<template>
  <!-- added by samer -->
  <header class="th-root">
    <!-- ─── Three-Column Row ─── -->
    <div class="th-grid">
      <!-- Arabic Column (Right-Aligned) -->
      <div class="th-col th-col--ar">
        <p class="th-text th-text--country">الجمهورية اليمنية</p>
        <p class="th-text">وزارة الإرشاد وشؤون الحج والعمرة</p>
        <p class="th-text">الأكاديمية العليا للقرآن الكريم وعلومه</p>
        <p class="th-text">كلية القرآن الكريم وعلومه</p>
        <p class="th-text th-text--branch">المركز الرئيسي</p>
      </div>

      <!-- Center Column -->
      <div class="th-col th-col--center">
        <p class="th-basmala">بسمِ اللهِ الرحمنِ الرحيم</p>
        <img :src="imageUrl" class="th-logo" />
      </div>

      <!-- English Column (Left-Aligned) -->
      <div class="th-col th-col--en">
        <p class="th-text th-text--country">Republic of Yemen</p>
        <p class="th-text">Ministry of Guidance</p>
        <p class="th-text">Hajj and Umrah matters</p>
        <p class="th-text">the Supreme Academy of the Holy</p>
        <p class="th-text">Quran and its Sciences</p>
        <p class="th-text">College of the Holy Quran</p>
        <p class="th-text th-text--branch">MAIN CENTER</p>
      </div>
    </div>

    <!-- ─── Primary Accent Divider (DataTable-style) ─── -->
    <div class="th-divider"></div>

    <!-- ─── Document Title ─── -->
    <h3 v-if="title || titleAuto" class="th-title">
      {{ title ? title + " - " : "" }} {{ titleAuto }}
    </h3>
  </header>
</template>

<script>
import { state } from "@/../src/store/state";
import settings from "@/../settings";
import logoo from "@/assets/logo.png";

export default {
  props: {
    title: {
      type: Number,
      default() {
        return "";
      },
    },
    autoTile: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    titleAuto() {
      if (this.autoTile) {
        let route = this.$route.matched.find((e) => e.name == this.$route.name);
        if (route)
          return this.$i18n.locale == "ar"
            ? route.props.default.name_ar || ""
            : route.props.default.name_en || "";
        else return "";
      } else return "";
    },
    imageUrl() {
      return state.profile?.org_logo ? settings.url_img + profile?.org_logo : logoo;
    },
  },
};
</script>

<style scoped>
/* ═══════════════════════════════════════════════
   TABLE HEADER — Unified with DataTable Identity
   Uses: --v-theme-primary, --v-theme-on-surface,
         --v-theme-surface, --shadow-key-umbra-color
   ═══════════════════════════════════════════════ */

.th-root {
  width: 100%;
  background-color: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
  padding: 20px 24px 12px;
  /* Force RTL for header order: Arabic (Source Column 1) on Right, English (Source Column 3) on Left */
  direction: rtl !important;
}

/* ── CSS Grid Layout ── */
.th-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: start;
  gap: 20px;
}

/* ── Columns ── */
.th-col {
  display: flex;
  flex-direction: column;
}

.th-col--ar {
  text-align: right !important;
  direction: rtl !important;
  align-items: flex-start !important;
  padding-top: 4px;
}

.th-col--center {
  text-align: center;
  align-items: center;
  justify-content: center;
}

.th-col--en {
  text-align: left !important;
  direction: ltr !important;
  align-items: flex-start !important;
  padding-top: 4px;
}

/* ── Typography ── */
.th-text {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.65);
}

.th-text--country {
  font-weight: 800;
  font-size: 0.85rem;
  color: rgba(var(--v-theme-on-surface), 0.87);
  margin-bottom: 1px;
}

.th-text--branch {
  font-weight: 700;
  font-size: 0.7rem;
  margin-top: 2px;
  color: rgba(var(--v-theme-on-surface), 0.4);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* ── Basmala ── */
.th-basmala {
  margin: 0 0 6px;
  font-size: 0.9rem;
  font-weight: 700;
  color: rgba(var(--v-theme-on-surface), 0.8);
  direction: rtl;
}

/* ── Logo ── */
.th-logo {
  height: 76px;
  width: auto;
  max-width: 120px;
  object-fit: contain;
  display: block;
}

/* ── Divider — matches DataTable header bottom border ── */
.th-divider {
  height: 2px;
  margin: 14px 0 10px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(var(--v-theme-primary), 0.15) 15%,
    rgba(var(--v-theme-primary), 0.15) 85%,
    transparent
  );
}

/* ── Document Title ── */
.th-title {
  text-align: center;
  font-size: 0.95rem;
  font-weight: 800;
  color: rgba(var(--v-theme-on-surface), 0.87);
  margin: 0;
  letter-spacing: 0.01em;
  text-transform: uppercase;
}
</style>
