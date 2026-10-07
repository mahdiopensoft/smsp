<template>
  <login
    :back-ground="logoImage"
    :logo="logo"
    class="hero-image"
    :hasSSO="true"
    @after-login="afterLogin"
    :loadingBtn="loading"
  >
  </login>
</template>
<script setup>
import { computed } from "vue";

import logoImage from "@/assets/logo.png";
import logo from "@/assets/logo.png";
import { useI18n } from "vue-i18n";
import shared from "external-components";
import router from "@/router";
import { ref } from "vue";
import { startProject } from "@/main";

const { locale } = useI18n();

const login = shared.LogIn;
const loading = ref(false);

const localeLang = computed(() => {
  const isArabic = locale.value === "ar";
  return isArabic;
});
const afterLogin = async () => {
  try {
    loading.value = true;
    const modules = import.meta.glob("@/pages/**/*.vue");

    await startProject(modules);
    const allRoute = await shared.dynamicRoutes(modules);
    allRoute.forEach((route) => {
      router.addRoute("home", route);
    });
    const redirectPath = router?.currentRoute?.value?.query?.redirect;

    if (redirectPath) router.push({ path: redirectPath });
    else {
      router.push({ name: "Index" });
    }
  } catch (error) {
    loading.value = false;
  } finally {    
    loading.value = false;
  }
};
</script>
<style scoped>
.hero-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}
</style>
