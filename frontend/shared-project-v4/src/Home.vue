<template>
  <!-- added by samer -->
  <!-- التطبيق -->

  <!-- SIDE BAR -->
  <v-navigation-drawer
    v-model="drawer"
    :permanent="!$vuetify.display.mobile"
    temporary
    class="sidebar sneat-sidebar border-0"
    elevation="0"
  >
    <div class="sidebar-layout-container d-flex flex-column h-100 overflow-hidden">
      <div class="sidebar-top-fixed border-b border-opacity-12">
        <v-btn
          v-if="$vuetify.display.mobile"
          icon="mdi-close"
          variant="tonal"
          size="small"
          color="grey-darken-2"
          elevation="0"
          style="position: absolute; top: 10px; inset-inline-end: 10px; z-index: 9999999"
          @click="drawer = false"
        />

        <div class="sidebar-brand" v-if="state.profile?.org_logo">
          <v-img
            :src="setting?.url_img + state.profile?.org_logo"
            height="40"
            class="cursor-pointer"
            @click="$router.push({ name: 'home' })"
          />
        </div>
        <div class="sidebar-brand justify-center opacity-50" v-else>
          <v-icon icon="mdi-image" color="primary" size="50" />
        </div>

        <!-- Mobile System Picker -->
        <div class="px-3 py-3 d-md-none border-bottom-subtle">
          <auto-list
            v-model="state.current_system"
            name="system"
            hide-details
            @update:modelValue="pushToSystem"
            variant="outlined"
            density="compact"
            :label="$i18n.locale == 'ar' ? 'اختيار النظام' : 'Select System'"
            class="w-100"
          />
        </div>

        <slot name="title" />
      </div>
      <div class="sidebar-list-scrollable flex-grow-1 overflow-y-auto">
        <side-bar :items="side_bar_items" :loading="loading_sys" />
      </div>
    </div>
  </v-navigation-drawer>
  <v-app-bar elevation="0" class="app-header px-2" style="border-opacity">
    <v-app-bar-nav-icon
      :icon="drawer ? 'mdi-menu' : 'mdi-menu-open'"
      @click="drawer = !drawer"
    />
    <v-toolbar-title>
      <div class="navbar-system-picker-wrapper d-none d-md-flex align-center">
        <div class="modern-search-field">
          <auto-list
            v-model="state.current_system"
            name="system"
            hide-details
            @update:modelValue="pushToSystem"
            width="250"
            density="compact"
            :label="' '"
            variant="plan"
            elevation="1"
          />
        </div>
      </div>
    </v-toolbar-title>
    <slot name="centerTop" />
    <v-spacer />

    <!-- RIGHT ZONE: Quick Actions + Profile -->
    <div class="navbar-zone-right d-flex align-center">
      <!-- Auth Status Badge -->
      <div
        class="navbar-auth-badge d-none d-md-flex align-center"
        :class="isSSO ? 'auth-sso' : 'auth-standard'"
      >
        <div class="auth-status-dot"></div>
        <span class="auth-text font-weight-black">
          {{
            isSSO
              ? $i18n.locale === "ar"
                ? "المنصة الموحدة"
                : "Unified Platform"
              : $i18n.locale === "ar"
              ? "تسجيل دخول عادي"
              : "Standard Login"
          }}
        </span>
      </div>

      <!-- System Selector Link (if SSO) -->
      <v-btn
        v-if="isSSO"
        :to="{ name: 'SystemSelector' }"
        variant="text"
        size="small"
        class="rounded-lg text-caption font-weight-bold px-2 d-none d-md-flex"
        color="primary"
      >
        {{ $i18n.locale == "ar" ? "اختيار الأنظمة" : "Switch Systems" }}
      </v-btn>

      <div
        v-if="isSSO"
        class="navbar-zone-divider d-none d-md-block"
        style="margin-inline: 8px"
      ></div>

      <!-- Quick Action Icons -->
      <div class="navbar-actions-group d-flex align-center">
        <BtnGeneralization class="navbar-icon-btn" />
        <BtnNotification v-if="hasNotiffication" class="navbar-icon-btn" />

        <!-- Theme Switcher -->
        <v-menu v-if="addThemes" offset="8" transition="slide-y-transition">
          <template v-slot:activator="{ props }">
            <v-btn
              icon
              class="navbar-icon-btn"
              variant="text"
              v-bind="props"
              v-tooltip:bottom="'تغيير المظهر'"
            >
              <v-icon size="18">mdi-palette-outline</v-icon>
            </v-btn>
          </template>
          <v-card width="210" class="navbar-profile-card" rounded="lg">
            <v-list density="compact" class="pa-2" nav>
              <v-list-item
                v-for="t in themes"
                :key="t.id"
                @click="
                  theme = t;
                  changeTheme();
                "
                :active="theme?.id === t.id"
                rounded="lg"
                color="primary"
                class="theme-menu-item-pro mb-1"
              >
                <template v-slot:prepend>
                  <div class="theme-icon-box me-3">
                    <v-icon
                      size="17"
                      :color="theme?.id === t.id ? 'primary' : undefined"
                      :style="{ opacity: theme?.id === t.id ? 1 : 0.5 }"
                      >{{ t.icon }}</v-icon
                    >
                  </div>
                </template>
                <v-list-item-title class="text-body-2 font-weight-bold">{{
                  t.name_ar
                }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card>
        </v-menu>

        <!-- Language Toggle -->
        <v-btn
          icon
          class="navbar-icon-btn"
          variant="text"
          @click="changeLang"
          v-tooltip:bottom="$i18n.locale === 'ar' ? 'English' : 'العربية'"
        >
          <v-icon size="18">mdi-translate</v-icon>
        </v-btn>

        <slot name="menu" />
      </div>

      <div class="navbar-zone-divider"></div>

      <!-- Profile Menu -->
      <v-menu
        :close-on-content-click="true"
        location="bottom end"
        offset="8"
        transition="slide-y-transition"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            class="navbar-profile-trigger"
            v-bind="props"
            variant="text"
            :ripple="false"
          >
            <!-- Avatar -->

            <v-avatar
              size="34"
              :color="imgUser ? '' : 'primary'"
              :variant="imgUser ? undefined : 'tonal'"
              class="navbar-profile-avatar"
            >
              <v-img v-if="imgUser" :src="imgUser" cover />
              <span
                v-else
                style="font-size: 1rem; font-weight: 700; letter-spacing: 0.02em"
              >
                {{ state?.profile?.username?.charAt(0)?.toUpperCase() || "U" }}
              </span>
            </v-avatar>

            <!-- Name & Chevron (hidden on mobile) -->
            <div class="navbar-profile-info d-none d-sm-flex align-center ms-2 me-1">
              <span
                class="navbar-profile-name text-truncate"
                style="font-weight: 600; font-size: 0.88rem"
              >
                {{ state?.profile?.username || "مستخدم" }}
              </span>
              <v-icon size="18" class="ms-1 profile-chevron">mdi-chevron-down</v-icon>
            </div>
          </v-btn>
        </template>

        <v-card min-width="260" class="navbar-profile-card" rounded="lg">
          <!-- Profile Header -->
          <v-list-item class="profile-header-section-pro px-4 py-3">
            <template v-slot:prepend>
              <v-avatar
                size="38"
                color="primary"
                variant="tonal"
                class="me-3 border-subtle"
              >
                <v-img v-if="imgUser" :src="imgUser" cover />
                <span v-else class="text-subtitle-2 font-weight-bold">
                  {{ state?.profile?.username?.charAt(0)?.toUpperCase() || "U" }}
                </span>
              </v-avatar>
            </template>
            <v-list-item-title
              class="text-body-2 font-weight-bold"
              style="color: rgb(var(--v-theme-on-surface))"
            >
              {{ state?.profile?.username || "مستخدم" }}
            </v-list-item-title>
            <v-list-item-subtitle
              class="text-caption"
              style="color: rgb(var(--v-theme-on-surface))"
            >
              {{ state?.profile?.email || "" }}
            </v-list-item-subtitle>
          </v-list-item>

          <!-- Menu Items -->
          <v-list density="compact" class="pa-2" nav>
            <v-list-item
              @click="moveToNex('user-profile', 'en')"
              class="theme-menu-item-pro mb-1"
              color="primary"
              rounded="lg"
            >
              <template v-slot:prepend>
                <div class="theme-icon-box me-3">
                  <v-icon size="18">mdi-account-outline</v-icon>
                </div>
              </template>
              <v-list-item-title class="text-body-2 font-weight-bold"
                >الملف الشخصي</v-list-item-title
              >
              <template v-slot:append>
                <v-chip
                  size="x-small"
                  color="primary"
                  variant="tonal"
                  class="font-weight-bold"
                  style="font-size: 0.625rem"
                  >جديد</v-chip
                >
              </template>
            </v-list-item>

            <v-divider class="my-2" style="opacity: 0.06" />

            <v-list-item
              @click="confirmLogout"
              class="profile-logout-pro theme-menu-item-pro"
              color="error"
              rounded="lg"
            >
              <template v-slot:prepend>
                <div class="theme-icon-box-error me-3">
                  <v-icon size="18">mdi-logout-variant</v-icon>
                </div>
              </template>
              <v-list-item-title class="text-body-2 font-weight-bold"
                >تسجيل الخروج</v-list-item-title
              >
            </v-list-item>
          </v-list>
        </v-card>
      </v-menu>
    </div>

    <template v-slot:extension>
      <div
        class="app-breadcrumbs-fixed border-t border-opacity-12 bg-surface"
        style="width: 100%"
      >
        <div class="d-flex align-center justify-space-between">
          <div class="toolbar-nav-section overflow-auto">
            <v-breadcrumbs
              :items="breadcrumbs"
              elevation="0"
              density="compact"
              class="pa-1 ma-0"
            >
              <template #divider>
                <v-icon size="11" class="text-medium-emphasis mx-1"
                  >mdi-chevron-left</v-icon
                >
              </template>
              <template #title="{ item, index }">
                <div
                  v-if="index === 0"
                  class="toolbar-home"
                  @click="$router.push('/')"
                  v-tooltip:bottom="'الرئيسية'"
                >
                  <v-icon size="16">mdi-home-variant-outline</v-icon>
                </div>
                <div v-else>
                  <span
                    class="toolbar-crumb"
                    :class="{
                      'toolbar-crumb--active': index === breadcrumbs.length - 1,
                    }"
                    @click="navigateTo(index)"
                  >
                    {{
                      $i18n.locale == "ar"
                        ? item?.title || item?.name_ar
                        : item?.title || item?.name_en
                    }}
                  </span>
                </div>
              </template>
            </v-breadcrumbs>
          </div>
          <div class="toolbar-quick-actions">
            <slot name="end-breadcrumbs" />

            <v-menu
              :close-on-content-click="true"
              transition="slide-y-transition"
              location="bottom end"
              offset="6"
            >
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  variant="text"
                  density="compact"
                  v-tooltip:bottom="'خصائص'"
                  class="tqa-btn tqa-settings"
                >
                  <v-icon size="17">mdi-dots-horizontal</v-icon>
                </v-btn>
              </template>
              <v-card width="220" class="navbar-profile-card" rounded="lg">
                <v-list density="compact" class="pa-2" nav>
                  <v-list-item
                    @click="openDialogReport"
                    rounded="lg"
                    class="theme-menu-item-pro mb-1"
                  >
                    <template v-slot:prepend>
                      <div class="theme-icon-box me-3">
                        <v-icon size="17">mdi-file-cog-outline</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="text-body-2 font-weight-bold">
                      إعدادات الرأس والتذييل
                    </v-list-item-title>
                    <v-tooltip activator="parent" location="top" open-delay="500">
                      إعدادات الرأس والتذييل
                    </v-tooltip>
                  </v-list-item>
                  <v-list-item
                    @click="openDialogAddInstructions"
                    rounded="lg"
                    class="theme-menu-item-pro mb-1"
                  >
                    <template v-slot:prepend>
                      <div class="theme-icon-box me-3">
                        <v-icon size="17">mdi-text-box-plus-outline</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="text-body-2 font-weight-bold"
                      >إضافة تعليمات</v-list-item-title
                    >
                  </v-list-item>

                  <v-list-item
                    @click="openDialogAddFunctions"
                    rounded="lg"
                    class="theme-menu-item-pro mb-1"
                  >
                    <template v-slot:prepend>
                      <div class="theme-icon-box me-3">
                        <v-icon size="17">mdi-cog-sync-outline</v-icon>
                      </div>
                    </template>
                    <v-list-item-title class="text-body-2 font-weight-bold"
                      >إضافة وظائف</v-list-item-title
                    >
                  </v-list-item>

                  <v-divider class="my-2" style="opacity: 0.06" />

                  <VTooltip
                    v-model="instructions.dialogShow"
                    v-if="instructions"
                    :open-on-hover="false"
                    open-on-click
                    background-color="primary"
                    content-class="custom-tooltip bg-transparent"
                    style="z-index: 99999 !important"
                  >
                    <template #activator="{ props }">
                      <v-list-item
                        v-bind="props"
                        :prepend-icon="
                          instructions.dialogShow
                            ? 'mdi-close'
                            : 'mdi-information-box-outline'
                        "
                        :color="instructions.dialogShow ? 'red' : 'primary'"
                        rounded="lg"
                        class="theme-menu-item-pro mb-1"
                      >
                        <template v-slot:prepend>
                          <div
                            :class="
                              instructions.dialogShow
                                ? 'theme-icon-box-error'
                                : 'theme-icon-box'
                            "
                            class="me-3"
                          >
                            <v-icon size="17">{{
                              instructions.dialogShow
                                ? "mdi-eye-off-outline"
                                : "mdi-eye-outline"
                            }}</v-icon>
                          </div>
                        </template>
                        <v-list-item-title class="text-body-2 font-weight-bold">
                          {{
                            instructions.dialogShow ? "إخفاء التعليمات" : "عرض التعليمات"
                          }}
                        </v-list-item-title>
                      </v-list-item>
                    </template>

                    <VCard>
                      <VCardTitle class="bg-primary">التعليمات</VCardTitle>
                      <VCardText class="pa-5">
                        <div v-html="getInstructions" />
                      </VCardText>
                    </VCard>
                  </VTooltip>
                  <VTooltip
                    v-model="functions.dialogShow"
                    v-if="getFunctions"
                    :open-on-hover="false"
                    open-on-click
                    background-color="primary"
                    content-class="custom-tooltip bg-transparent"
                    style="z-index: 99999 !important"
                  >
                    <template #activator="{ props }">
                      <v-list-item
                        v-bind="props"
                        :prepend-icon="functions.dialogShow ? 'mdi-close' : 'mdi-cogs'"
                        :color="functions.dialogShow ? 'red' : 'primary'"
                        rounded="lg"
                        class="theme-menu-item-pro mb-1"
                      >
                        <template v-slot:prepend>
                          <div
                            :class="
                              functions.dialogShow
                                ? 'theme-icon-box-error'
                                : 'theme-icon-box'
                            "
                            class="me-3"
                          >
                            <v-icon size="17">{{
                              functions.dialogShow
                                ? "mdi-eye-off-outline"
                                : "mdi-eye-outline"
                            }}</v-icon>
                          </div>
                        </template>
                        <v-list-item-title class="text-body-2 font-weight-bold">
                          {{ functions.dialogShow ? "إخفاء الوظائف" : "عرض الوظائف" }}
                        </v-list-item-title>
                      </v-list-item>
                    </template>

                    <VCard>
                      <VCardTitle class="bg-primary">الوظائف</VCardTitle>
                      <VCardText class="pa-3">
                        <div v-html="getFunctions" />
                      </VCardText>
                    </VCard>
                  </VTooltip>
                </v-list>
              </v-card>
            </v-menu>

            <div class="tqa-divider"></div>

            <v-btn
              icon
              variant="text"
              density="compact"
              @click="changeKeyScreen"
              v-tooltip:bottom="'تحديث'"
              class="tqa-btn tqa-refresh"
            >
              <v-icon size="17">mdi-refresh</v-icon>
            </v-btn>
          </div>
        </div>
      </div>
    </template>
  </v-app-bar>
  <v-main>
    <v-card
      class="app-body-container overflow-y-auto pa-4 pa-md-6 border-0 elevation-2 h-100"
    >
      <router-view
        v-slot="{ Component }"
        :key="$route.name + primaryStore.keySreen"
        :name_ar="name_ar"
      >
        <transition name="fade" mode="out-in">
          <component
            :is="Component"
            :key="$route.name + primaryStore.keySreen"
            :name_ar="name_ar"
          />
        </transition>
      </router-view>
    </v-card>
  </v-main>
  <IdleTimer />

  <alert
    v-if="state.alert"
    v-model="state.alert"
    :details="state.alert_details"
    class="text-white"
  />

  <custom-snackBar
    v-model="state.snackbar"
    location="top"
    class="text-center"
    :title="state?.alert_details?.message"
    :icon="state?.alert_details?.alert_icon"
  />
  <VOverlay v-model="dialog" style="z-index: 10000 !important" />

  <custom-dialog v-model="dialog_report" :title="$t('header_footer')">
    <VRow class="pa-5">
      <auto-list
        v-model="fk_print_report_setting"
        name="VariableHeaderFooter"
        returnObject
        cols="8"
      />
      <VSpacer />

      <custom-btn
        v-if="headerFooterStore.headerFooterData"
        type="del"
        variant="text"
        :click="deleteRelationReport"
        class="ma-4"
      />
    </VRow>
    <v-card class="pa-4 mt-4" dir="rtl" v-for="i in ['header', 'footer']" :key="i">
      <v-card-title class="rtl-preview">📄 المعاينة الحية لل {{ i }}</v-card-title>
      <v-divider></v-divider>
      <v-card-text class="rtl-preview">
        <div v-html="previewHtml[i]" />
        <!-- <preview-content-html
          :items="
            fk_print_report_setting ? JSON.parse(fk_print_report_setting[i] || '') : ''
          "
        /> -->
        <v-row> </v-row>
      </v-card-text>
    </v-card>
    <template v-slot:actions>
      <v-spacer></v-spacer>
      <custom-btn type="save" class="ma-2" :click="saveReport" />
    </template>
  </custom-dialog>

  <custom-dialog v-model="instructions.dialogAdd" title="اضافة تعليمات للشاشة">
    <div class="pa-5">
      <QuillEditor
        v-model:content="instructions.editor"
        toolbar="full"
        content-type="html"
        dense="compact"
        style="height: 300px"
      />
    </div>
    <template v-slot:actions>
      <custom-btn
        type="update"
        :click="async () => await saveInstructionsOrFunctions('instructions')"
        class="ma-2"
      />
    </template>
  </custom-dialog>

  <custom-dialog v-model="functions.dialogAdd" title="اضافة وظائف للشاشة">
    <QuillEditor
      v-model:content="functions.editor"
      toolbar="full"
      content-type="html"
      dense="compact"
      style="height: 300px"
    />
    <template v-slot:actions>
      <custom-btn
        type="update"
        :click="async () => await saveInstructionsOrFunctions('functions')"
        class="ma-2"
      />
    </template>
  </custom-dialog>

  <SystemAnnouncementDialog />
  <GlobalToast />
  <!-- <custom-dialog v-model="dialog_education_video" title="فديو تعليمي للشاشة">
    <VContainer class="text-center">
      <video controls width="100%">
        <source
          src="/15.15- DjangoTutorial for Beginners - Forms -  دورة جانغو للمبتدئين - النماذج.mp4"
          type="video/mp4"
        />
      </video>
    </VContainer>
  </custom-dialog> -->

  <!-- Logout Confirmation Dialog -->
  <custom-dialog
    v-model="showLogoutDialog"
    title="تسجيل الخروج"
    width="400"
    height="auto"
    :mobileFullscreen="false"
    persistent
  >
    <div class="logout-dialog-body">
      <!-- Decoration header -->
      <div class="logout-card-header d-flex justify-center align-center pt-4 pb-4">
        <div class="icon-circle d-flex justify-center align-center">
          <v-icon size="36" color="error">mdi-logout-variant</v-icon>
        </div>
      </div>

      <div class="text-center pb-2">
        <div class="text-h6 font-weight-bold color-text-heading">هل أنت متأكد؟</div>
      </div>

      <div class="text-center text-body-2 text-medium-emphasis pb-6 px-8">
        {{
          isSSO
            ? "سيتم إنهاء جلستك الحالية. يمكنك اختيار الخروج من هذا النظام فقط أو الخروج من جميع الأنظمة المرتبطة."
            : "سيتم تسجيل خروجك من النظام، هل أنت متأكد من رغبتك في المغادرة؟"
        }}
      </div>
    </div>

    <template v-slot:actions>
      <div class="d-flex flex-column w-100 ga-3 px-4 pb-4">
        <!-- SSO: Two options -->
        <template v-if="isSSO">
          <v-btn
            color="primary"
            variant="flat"
            block
            height="48"
            rounded="lg"
            class="font-weight-bold text-none shadow-sm"
            :loading="loadingLogout"
            @click="handleLocalLogout"
          >
            <v-icon start size="20">mdi-application-outline</v-icon>
            خروج من النظام الحالي
          </v-btn>

          <v-btn
            color="error"
            variant="tonal"
            block
            height="48"
            rounded="lg"
            class="font-weight-bold text-none"
            :loading="loadingLogout"
            @click="handleFullLogout"
          >
            <v-icon start size="20">mdi-shield-lock-outline</v-icon>
            خروج كامل من المنصة
          </v-btn>
        </template>

        <!-- Non-SSO: Single confirm -->
        <template v-else>
          <v-btn
            color="error"
            variant="flat"
            block
            height="48"
            rounded="lg"
            class="font-weight-bold text-none shadow-sm"
            :loading="loadingLogout"
            @click="handleLocalLogout"
          >
            <v-icon start size="20">mdi-logout</v-icon>
            نعم، سجل الخروج
          </v-btn>
        </template>

        <v-btn
          variant="text"
          block
          height="44"
          rounded="lg"
          class="text-none font-weight-medium"
          style="color: rgb(var(--v-theme-on-surface))"
          :disabled="loadingLogout"
          @click="showLogoutDialog = false"
        >
          إلغاء، ابقني مسجلاً
        </v-btn>
      </div>
    </template>
  </custom-dialog>

  <DraggableChatBtn />

  <QuickChatWidget />
</template>
<script setup>
import { state } from "@/../src/store/state";
import { primaryStore } from "../store/state";
</script>
<script>
import HfTemplateSelectDialog from "../src/headerandfooter/components/HfTemplateSelectDialog.vue";
import SystemAnnouncementDialog from "../chating/components/common/SystemAnnouncementDialog.vue";
import GlobalToast from "../chating/components/common/GlobalToast.vue";
import { state } from "@/../src/store/state";
import SideBar from "./layouts/SideBar.vue";
import { useRoute } from "vue-router";

import { QuillEditor } from "@vueup/vue-quill";
import { primaryStore } from "../store/state";
import { useAuthStore } from "../src/UserManagement/stores/auth";
import api from "../plugins/axios-plugin";
import { useHeaderFooterStore } from "../src/stores/headerFooterStore";
import { useCustomHeaderFooter } from "../src/headerandfooter/composables/useCustomHeaderFooter";

import BtnNotification from "../chating/components/BtnNotification.vue";
import BtnGeneralization from "../chating/components/BtnGeneralization.vue";
import QuickChatWidget from "../chating/components/QuickChatWidget.vue";
import DraggableChatBtn from "../chating/components/DraggableChatBtn.vue";
import setting from "@/../settings";

export default {
  components: {
    QuillEditor,
    SystemAnnouncementDialog,
    GlobalToast,
    BtnNotification,
    BtnGeneralization,
    QuickChatWidget,
  },
  props: {
    addThemes: {
      type: Boolean,
      default: true,
    },
    hasNotiffication: {
      type: Boolean,
      default: true,
    },
  },

  components: { SideBar },
  async created() {
    this.authStore = useAuthStore();
    this.authStore.getProfile();
    const store = useCustomHeaderFooter();
    try {
      store.fetchApiVariables();
    } catch {}

    try {
      if (!state?.systems?.length) {
        const response = await api("screens/systems/all/");
        state.systems = response?.data?.data || response.data;
      }
      if (!state.current_system)
        if (state?.systems?.length > 0) state.current_system = state?.systems[0].id;

      // this.getSideBarSys();

      var local_breadcrumbs = JSON.parse(localStorage.getItem("breadcrumbs"));

      if (local_breadcrumbs) {
        local_breadcrumbs = local_breadcrumbs.filter((item) => item != null);
        this.$route.matched.map((e) => {
          var l = local_breadcrumbs.find((f) => f.name === e.name);
          if (l) {
            e.title = l.title;
            e.title_en = l.title_en;
          }
        });
      }
    } catch (e) {
      this.$alert("errorData");
    }
  },
  data() {
    return {
      instructions: {},
      functions: {},

      route: undefined,
      system: null,
      theme: state.theme,

      side_bar_items: [],
      themes: [
        {
          id: 1,
          name_en: "lightTheme",
          name_ar: "فاتح",
          color: "#696cff",
          icon: "mdi-weather-sunny",
        },
        {
          id: 2,
          name_en: "darkTheme",
          name_ar: "داكن",
          color: "#232333",
          icon: "mdi-weather-night",
        },
        {
          id: 3,
          name_en: "blueTheme",
          name_ar: "ازرق",
          color: "#00cfe8",
          icon: "mdi-palette-outline",
        },
        {
          id: 4,
          name_en: "natureTheme",
          name_ar: "طبيعي",
          color: "#28c76f",
          icon: "mdi-leaf",
        },
      ],

      dialog: false,
      showLogoutDialog: false,
      loadingLogout: false,
      dialog_education_video: false,
      dialog_report: false,
      drawer: true,
      loading_sys: false,
      // rail: false,
      show_alert: false,
      alert_icon_color: undefined,
      alert_icon: undefined,
      alert_title: undefined,
      alert_message: undefined,
      fk_print_report_setting: undefined,

      keySreen: 0,

      authStore: null,
      headerFooterStore: useHeaderFooterStore(),
      customHeaderFooter: useCustomHeaderFooter(),
    };
  },
  mounted() {
    if (this.$vuetify.display.mobile) this.drawer = false;
    const savedLocale = localStorage.getItem("lang");
    if (savedLocale) {
      this.$i18n.locale = savedLocale || "ar";
    }
  },
  computed: {
    previewHtml() {
      if (!this.fk_print_report_setting) return { header: "", footer: "" };
      const header = this.fk_print_report_setting.header
        ? JSON.parse(this.fk_print_report_setting.header)
        : "";
      const footer = this.fk_print_report_setting.footer
        ? JSON.parse(this.fk_print_report_setting.footer)
        : "";

      const jsondata = {
        name: this.fk_print_report_setting.name,
        header,
        footer,
      };

      return this.customHeaderFooter.generateHTMLForTemplate(jsondata);
    },
    isSSO() {
      return this.authStore.isSSO;
    },
    title() {
      // Find the current route entry
      let route = this.$route.matched.find((e) => e.name == this.$route.name);
      if (!route) return "";

      // Try to get title from props, then from meta, then from the route name
      const nameAr = route.props?.default?.name_ar || route.meta?.title || route.name;
      const nameEn = route.props?.default?.name_en || route.meta?.title_en || route.name;

      return this.$i18n.locale == "ar" ? nameAr : nameEn;
    },
    breadcrumbs() {
      var local_breadcrumbs = JSON.parse(localStorage.getItem("breadcrumbs")) || [];

      return this.$route?.matched?.map((e) => {
        if (e.path === "/") return;
        var local_title = local_breadcrumbs?.find((f) => f?.name === e.name);
        return {
          title: local_title ? local_title.title : e.title,
          name_ar: e.props.default.name_ar,
          name_en: e.props.default.name_en,
          current_path: e.name,
        };
      });
    },
    // التعليمات
    getInstructions() {
      return primaryStore?.notes_screen[this.$route.name]?.notes || null;
    },
    // الوظائف
    getFunctions() {
      return primaryStore?.notes_screen[this.$route.name]?.functions || null;
    },

    getVideo() {
      return null;
    },

    imgUser() {
      if (state.profile?.image_user) return setting.url_img + state.profile?.image_user;
      return null;
    },
  },
  methods: {
    pushToSystem() {
      this.loading_sys = true;
      setTimeout(() => {
        this.loading_sys = false;
      }, 500);
      if (state.current_system) {
        if (this.$router.hasRoute('dash-board"')) {
          this.$router.push({ name: "dash-board" }) || this.$router.push({ path: "/" });
        } else {
          this.$router.push({ path: "/" });
        }
      } else {
        try {
          this.$router.push({ name: "Index" });
        } catch {
          if (state?.systems?.length > 0) state.current_system = state?.systems[0].id;
        }
      }
    },
    changeKeyScreen() {
      primaryStore.keySreen += 1;
    },
    confirmLogout() {
      this.showLogoutDialog = true;
    },
    moveToNex(screen) {
      this.$navigateTo({
        name: screen,
        blank: false,
      });
    },
    // Local logout — clear tokens, go to login, keep Keycloak session
    async handleLocalLogout() {
      this.loadingLogout = true;
      try {
        await this.authStore.logout();
        this.showLogoutDialog = false;
        window.location.reload();
      } finally {
        this.loadingLogout = false;
      }
    },

    // Full logout — end Keycloak session completely
    async handleFullLogout() {
      this.loadingLogout = true;
      try {
        await this.authStore.fullLogout();
        // For SSO, fullLogout redirects the page, so we only reach here for non-SSO
        this.showLogoutDialog = false;
        // window.location.reload();
        // window.location.href = "login"
      } finally {
        this.loadingLogout = false;
      }
    },
    async openDialogAddInstructions() {
      this.instructions.editor =
        primaryStore?.notes_screen[this.$route.name]?.notes || null;

      this.instructions.dialogAdd = true;
    },
    async openDialogAddFunctions() {
      this.functions.editor =
        primaryStore?.notes_screen[this.$route.name]?.functions || null;

      this.functions.dialogAdd = true;
    },
    async saveInstructionsOrFunctions(type) {
      const fk_screen = this.$route?.meta?.fk_screen;
      const fk_default_system = this.$route?.meta?.system;

      let data = { fk_default_system: fk_default_system };

      if (type === "functions") data.screen_functions = this.functions.editor;
      else data.json_notes = this.instructions.editor;

      await api.patch("screens/screen/" + fk_screen + "/", data);

      if (!primaryStore.notes_screen[this.$route.name])
        primaryStore.notes_screen[this.$route.name] = {};

      if (type === "functions")
        primaryStore.notes_screen[this.$route.name].functions = this.functions.editor;
      else primaryStore.notes_screen[this.$route.name].notes = this.instructions.editor;

      this.$snack("update");
    },

    // Methods
    async openDialogReport() {
      const fk_screen = this.$route?.meta?.fk_screen;

      await this.headerFooterStore.changeHeaderFooter({ fk_screen: fk_screen });

      this.fk_print_report_setting = this.headerFooterStore.headerFooterData;

      this.dialog_report = true;
    },
    async saveReport() {
      if (!this.fk_print_report_setting) return;
      const fk_screen = this.$route.meta?.fk_screen;

      const fk_print_report_setting_id = this.fk_print_report_setting?.id;
      const res = await api.post(
        "screens/screen/save-print-report-setting/?fk_print_report_setting_id=" +
          fk_print_report_setting_id +
          "&fk_screen=" +
          fk_screen
      );

      this.$snack("update");
    },
    async deleteRelationReport() {
      const fk_screen = this.$route?.meta?.fk_screen;
      await api.delete(
        "screens/screen/delete-print-report-setting/?fk_screen=" + fk_screen
      );

      this.$alert("success");

      this.fk_print_report_setting = null;
      this.headerFooterStore.headerFooterData = null;
    },

    async getSideBarSys() {
      try {
        if (state.current_system) {
          this.loading_sys = true;
          await api("screens/screen/sidebar/", {
            params: {
              fk_system: state.current_system,
            },
          }).then((response) => {
            this.side_bar_items = response?.data?.data || response.data;
          });
        }
      } finally {
        this.loading_sys = false;
      }
    },
    navigateTo(index) {
      this.$router.push({
        name: this.$route.matched[index].name,
        params: this.$route.params,
      });
    },
    // تغيير الثيم
    changeTheme() {
      state.theme = this.theme;

      localStorage.setItem("theme", JSON.stringify(this.theme));
    },
    //تغيير اللغة
    changeLang() {
      const lang = this.$i18n.locale === "ar";
      this.$i18n.locale = lang ? "en" : "ar";
      localStorage.setItem("lang", this.$i18n.locale);
    },
  },
  watch: {
    "$vuetify.display.mobile"(isMobile) {
      if (isMobile) this.drawer = false;
    },
    dialog_report(val) {
      if (!val) this.fk_print_report_setting = null;
    },
    "instructions.dialogAdd"(val) {
      if (!val) this.instructions = {};
    },
    "functions.dialogAdd"(val) {
      if (!val) this.functions = {};
    },
  },
};
</script>
<style>
.sidebar-layout-container {
  height: 100%;
}
.sidebar-top-fixed {
  flex-shrink: 0;
}
.custom-tooltip {
  min-width: 500px !important;
}

.fill-height {
  height: 80svh !important;
}

.overflowContainer {
  overflow-y: auto;
}

/* Sidebar list-item typography — aligned to Sneat */
.sneat-sidebar .v-list-item-title {
  font-size: var(--font-size-sm) !important;
}

.v-navigation-drawer .v-list-item.first {
  position: sticky;
  top: 0;
  z-index: 1;
}

.pointer-cursor {
  cursor: pointer;
}

/* ───── Navbar Auth Badge ───── */
.navbar-auth-badge {
  height: 28px;
  padding: 0 12px;
  border-radius: 14px;
  font-size: 0.7rem;
  letter-spacing: 0.4px;
  font-weight: 600;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
  background: rgba(var(--v-theme-on-surface), 0.04);
  box-shadow: none;
  display: inline-flex;
  align-items: center;
  margin-inline-end: 12px;
}

.auth-sso {
  border-color: rgba(var(--v-theme-primary), 0.2);
  background: rgba(var(--v-theme-primary), 0.04);
  color: rgb(var(--v-theme-primary));
}

.auth-standard {
  border-color: rgba(var(--v-theme-on-surface), 0.15);
  background: rgba(var(--v-theme-on-surface), 0.02);
  color: rgba(var(--v-theme-on-surface), 0.8);
}

.auth-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-inline-end: 8px;
  background: currentColor;
  opacity: 0.8;
}

.auth-text {
  line-height: 1;
}

.icon_theme_hide .v-input__control .v-field .v-field__append-inner {
  display: none;
}

/* Global Scrollbar — Theme-aware */
::-webkit-scrollbar {
  width: 6px;
  height: 6px !important;
}

::-webkit-scrollbar-track {
  background: rgba(var(--v-theme-on-surface), 0.03);
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.12);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.25);
}
.v-navigation-drawer__content {
  /* overflow: hidden !important; */
}

.main-viewport-wrapper {
  height: 100svh;
  overflow: hidden;
}

.app-breadcrumbs-fixed {
  flex-shrink: 0;
  z-index: 10;
  user-select: none;
}
.main-viewport-wrapper {
  height: 100svh;
  overflow: hidden;
}
.app-body-container {
  margin: 12px !important;
  border-radius: 16px !important;
  scrollbar-width: thin;
}

@media (max-width: 768px) {
  .app-body-container {
    border-radius: 0 !important;
    margin: 0 !important;
  }
}
</style>
