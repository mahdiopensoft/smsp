<template>
  <!-- added by samer -->
  <Home>
    <template v-slot:title>
      <VCol v-if="profile">
        <h2
          style="
    font-size: 20px;
    text-align: center;
}"
        >
          {{ profile?.organization_name }}
        </h2>
        <h4 class="mt-2 ms-3" style="text-align: center">
          {{ profile?.year_m }}
        </h4>
        <h4 class="ms-3" style="text-align: center">{{ profile?.year_h }}</h4>
      </VCol>
      <VCol v-else class="text-center"> </VCol>
    </template>
  </Home>
</template>
<script setup>
import { state } from "@/store/state";
</script>

<script>
import shared from "external-components";
// import connectWebSocket from "@/utils/notifications";
import logo from "@/assets/logo.png";

export default {
  data() {
    return {
      image2: new URL("@/assets/logo.png", import.meta.url).href,


      profile: undefined,
      // Websocket: null,
      tab: {},
    };
  },
  components: { Home: shared.Home },
  mounted() {
    // this.Websocket = connectWebSocket();
  },

  async created() {
    // await this.getDataGeneralizations();
    // await this.getDataRegulation();
    // await this.getunreadNotificationsCount();
  },


  methods: {


    moveToNex(screen) {
      this.$navigateTo({
        name: screen,
        blank: false,
      });
    },
    async getDataGeneralizations() {
      try {
        const response = await this.$axios.get(
          "system-management/generalizations-notifications",
          {
            params: {
              user: state.profile?.id,
            },
          }
        );
        state.unread_generalization = response.data;
      } catch (error) {
        console.error("Error fetching group generalizations:", error);
      }
    },
    async getDataRegulation() {
      try {
        const response = await this.$axios.get(
          "system-management/regulations-notifications",
          {
            params: {
              user: state.profile?.id,
            },
          }
        );
        state.unread_regulations = response.data;
      } catch (error) {
        console.error("Error fetching group regulations:", error);
      }
    },
    getunreadNotificationsCount() {
      var generalization_count = state.unread_generalization?.length;
      var occation_count = state.unread_regulations?.length;
      state.notifications_count = generalization_count + occation_count;
      return state.notifications_count;
    },
  },

};
</script>
<style scoped>
.custom-menu-card {
  width: 400px;
  max-height: 500px;
  overflow-y: auto;
}
.custom-menu-card2 {
  width: 250px;
  max-height: 500px;
  overflow-y: auto;
}
.custom-menu-list {
  padding: 12px;
}
.custom-menu-list .v-list-item {
  min-height: 64px;
  padding: 8px 16px;
}
</style>
