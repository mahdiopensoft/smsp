<template>

  <div>
    <v-card class="custom-card">
      <v-img :src="image2" height="250px" cover></v-img>
      <v-avatar class="profile-avatar" size="100">
        <v-img :src="image"></v-img>

      </v-avatar>
      <v-card-text class="mt-8 text-center">
        <h2>{{ items?.first_name }} {{ items?.last_name }}</h2>
        <p class="mt-2 text-blue-accent-3">{{ items?.academic_id }}</p>
        <p class="mt-2">{{ items?.role_name }}</p>
      </v-card-text>
    </v-card>

    <div>
      <v-row>
        <v-col cols="12" md="4">
          <v-card class="custom-card">
            <v-col cols="12" class="text-center">
              <v-icon size="35">mdi-account-outline</v-icon>
              <h2>الملف الشخصي</h2>
              <br />
              <h4 class="grey--text">
                البيانات الشخصية المتعلقة بحساب المستخدم مع الدور الذي يملكة للتعامل مع
                النظام
              </h4>
            </v-col>
            <v-divider class="my-2"></v-divider>
            <v-list>
              <v-list-item>
                <v-list-item-content class="d-flex align-center py-2">


                </v-list-item-content>

                <v-list-item-content class="d-flex align-center py-2">
                  <v-list-item-title class="px-2"
                    ><v-icon>mdi-circle-medium</v-icon> اسم المستخدم:
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ items.username }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-content class="d-flex align-center py-2">
                  <v-list-item-title class="px-2"
                    ><v-icon>mdi-circle-medium</v-icon> تاريخ الميلاد:
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ items.date_of_birth }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-content class="d-flex align-center py-2">
                  <v-list-item-title class="px-2"
                    ><v-icon>mdi-circle-medium</v-icon> الجنس:</v-list-item-title
                  >
                  <v-list-item-subtitle>{{ items.gender_name }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-content class="d-flex align-center py-2">
                  <v-list-item-title class="px-2"
                    ><v-icon>mdi-circle-medium</v-icon> رقم الهاتف:</v-list-item-title
                  >
                  <v-list-item-subtitle>{{ items.phone_number }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-content class="d-flex align-center py-2">
                  <v-list-item-title class="px-2"
                    ><v-icon>mdi-circle-medium</v-icon> الايميل:</v-list-item-title
                  >
                  <v-list-item-subtitle>{{ items.email }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-content class="d-flex align-center py-2">
                  <v-list-item-title class="px-2"
                    ><v-icon>mdi-circle-medium</v-icon> العنوان:</v-list-item-title
                  >
                  <v-list-item-subtitle>{{ items.address }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" md="8">
          <v-card class="custom-card">
            <v-tabs v-model="tab" grow>
              <v-tab value="news2">الأخبار</v-tab>
              <v-tab value="generalization2">التعميمات</v-tab>
              <v-tab value="password">كلمة المرور</v-tab>
            </v-tabs>

            <v-window v-model="tab">
              <v-window-item value="news2">
                <v-list-item>
                  <v-list-item-content class="px-1">
                    <v-div class="d-flex">
                      <v-avatar color="#43A047" size="40" variant="tonal">
                        <v-icon size="23">mdi-bell-outline</v-icon>
                      </v-avatar>
                      <v-div class="px-2">
                        <v-list-item-title>aaaaaaa</v-list-item-title>
                      </v-div>
                    </v-div>
                  </v-list-item-content>
                  <v-divider></v-divider>
                </v-list-item>
              </v-window-item>

              <v-window-item value="generalization2">
                <v-list-item>
                  <v-list-item-content class="px-1">
                    <v-div class="d-flex">
                      <v-avatar color="blue-darken-2" size="40" variant="tonal">
                        <v-icon size="23">mdi-message-text-outline</v-icon>
                      </v-avatar>
                      <v-div class="px-2">
                        <v-list-item-title>wwwwwwww</v-list-item-title>
                      </v-div>
                    </v-div>
                  </v-list-item-content>
                  <v-divider></v-divider>
                </v-list-item>
              </v-window-item>

              <v-window-item value="password">
                <v-list-item>
                  <v-list-item-content class="px-1">
                    <v-row align="center" justify="center" class="mt-1 mb-2 pb-2">
                      <v-col cols="12">
                        <h2 class="text-center">تعديل كلمة المرور</h2>
                        <br />
                        <h4 class="text-center grey--text">
                          البيانات الشخصية المتعلقة بحساب المستخدم مع الدور الذي يملكة
                          للتعامل مع النظام
                        </h4>
                      </v-col>
                      <custom-text-field
                        variant="outlined"
                        :label="$t('old-password')"
                        v-model="user.old_password"
                        :icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[$required]"
                      />
                      <custom-text-field
                        variant="outlined"
                        :label="$t('new-password')"
                        :type="showPassword ? 'text' : 'password'"
                        v-model="user.new_password"
                        :icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[$required]"
                      />
                      <custom-text-field
                        variant="outlined"
                        :label="$t('convert-password')"
                        :type="showPassword ? 'text' : 'password'"
                        v-model="user.convert_new_password"
                        :icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[$required]"
                      />

                      <custom-btn type="save" :click="changePassword" />
                    </v-row>
                  </v-list-item-content>
                </v-list-item>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      image: "",
      image2: "",
      items: {},
      url: "user-manager/profile/",
      user: {},
      tab: {},
      confirmPassword: [
        (v) => !!v || "يجب تاكيد كلمة المرور",
        (v) => v === this.user.new_password || "كلمات المرور غير متطابقة",
      ],
    };
  },
  methods: {
    async getData() {
      return await this.$axios(this.url).then((response) => (this.items = response.data));
    },
    async changePassword() {
      return await this.$axios.post("user-manager/change-password/").then((response) => {
        this.$snack("add", { message: response.data });
      });
    },
  },
  created() {
    this.getData();
  },
};
</script>
<style scoped>
.profile-avatar {
  position: absolute;
  top: 180px;
  left: 50%;
  transform: translateX(-50%);
  border: 4px solid white;
}

.custom-card {
  border-radius: 24px !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.98) !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  transition: all 0.3s ease;
}
</style>
