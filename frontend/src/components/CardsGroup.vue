<template>
  <v-container fluid>
    <v-row class="pa-5 d-flex align-center" style="row-gap: 2rem">
      <v-col
        v-for="(item, index) in items"
        :key="index"
        :lg="3"
        :md="6"
        :sm="12"
      >
        <v-card
          class="card service pa-5 text-center"
          border
          evevation="6"
          rounded="xl"
        >
          <v-menu v-if="key !== 'name'" location="start top" origin="start top">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon=""
                title="تنفيذ الخدمات"
                size="small"
                color="light-blue-darken-3"
                class="rounded-circle ma-2"
                style="position: absolute; right: 0; top: 0;"
              >
                <v-icon>mdi-dots-horizontal</v-icon>
              </v-btn>
            </template>
            <v-list style="border-radius: 5%; border: 1px solid #ccc">
              <v-list-item
                v-for="implement in item?.Implementation"
                :key="implement"
                :title="implement.name"
                @click="goto(implement.route)"
              >
              </v-list-item>
            </v-list>
          </v-menu>
          <v-avatar
            size="80"
            variant="outlined"
            class="mb-4 mx-auto"
            color="light-blue-darken-3"
            style="background: rgba(2, 120, 189, 0.04)"
          >
            <v-icon size="40" color="light-blue-darken-3">{{
              item.icon
            }}</v-icon>
          </v-avatar>

          <v-card-title class="text-h6 font-weight-bold">
            {{ item.value }}
          </v-card-title>

          <v-card-subtitle class="mb-4 text-body-2 text-grey-darken-1">
            {{ item.sup_title }}
          </v-card-subtitle>

          <v-row dense class="mt-2 align-center ga-1">
            <v-col>
              <v-btn
                block
                color="light-blue-darken-1"
                variant="outlined"
                class="text-white custom-btn"
                @click="goto(item.viewRoute, item.type)"
              >
                <v-icon start> mdi-eye</v-icon>
                عرض
              </v-btn>
            </v-col>

            <v-col>
              <v-btn
                block
                color="light-blue-darken-1"
                variant="outlined"
                class="text-white custom-btn"
                @click="goto(item.addRoute, item.type)"
              >
                <v-icon start> mdi-plus</v-icon>
                اضافة
              </v-btn>
            </v-col>
          </v-row>
          <!-- <div class="decorative-circle circle-1"></div>
          <div class="decorative-circle circle-2"></div>
          <div class="decorative-circle circle-3"></div> -->
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<!-- <template>
  <v-container fluid>
    <v-row justify="center" dense>
      <v-col></col></v-col>
    </v-row>
  </v-container>
</template> -->

<script>
export default {
  name: "CardsGroup",
  props: {
    items: Array,
    title: {
      type: String,
      required: true,
    },
    addRoute: Array,
    viewRoute: {
      type: String,
      required: true,
    },
    cols: {
      type: Number,
      default: 3,
    },
    type: {
      type: Number,
      default: 3,
    },
    icon: {
      type: String,
      required: true,
    },
  },

  methods: {
    calcWidth(cols) {
      const width = `${100 / cols}%`;

      return {
        flexBasis: width,
        maxwidth: width,
      };
    },
    goto(route, type) {
      console.log(route, "route");
      this.$navigateTo({
        name: route,
        params: {
          fk_services: type,
        },
        blank: false,
      });
    },
  },
};
</script>
<style scoped>
* {
  font-family: Cairo !important;
}

.service {
  --bg-color: #667782;
  --bg-color-light: #94e2f6;
  --text-color-hover: #fff;
  --box-shadow-color: rgba(75, 70, 80, 0.48);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  transition: all 0.3s ease-out;
  text-decoration: none;
  /* background: rgba(2, 120, 189, 0.01); */
}
.service:hover {
  transform: translateY(-5px) scale(1.005) translateZ(0);
  box-shadow: 0 24px 36px rgba(0, 0, 0, 0.11),
    0 24px 46px var(--box-shadow-color) !important;
  border: 1px solid #0278bd86 !important;
}
.decorative-circle {
  position: absolute;
  border-radius: 50%;
  /* background: rgba(14, 21, 32, 0.1); */
  background: rgb(2 119 189 / 8%);
  z-index: 0;
}
.circle-1 {
  width: 100px;
  height: 100px;
  top: -30px;
  right: -30px;
}
.circle-3 {
  width: 100px;
  height: 100px;
  top: -30px;
  left: -30px;
}
.circle-2 {
  width: 60px;
  height: 60px;
  bottom: -20px;
  left: -20px;
}
.custom-btn:hover {
  background: #0277bd;
  color: white !important;
}
</style>
