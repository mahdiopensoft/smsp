<template>
  <!-- المستخدمين -->

  <filter-fields>
    <template #fields>
      <auto-list v-model="user_type" name="UserType" @update:modelValue="getData" />
    </template>
  </filter-fields>
  <add-user v-model="drawer" :data="data" :getData="getData" :items="items" />
  <custom-data-table
    :="{
      headers,
      items,
      getData: getData,
      create: () => (drawer = true),
      delItem: url,
      editItem,

      customLoading: loading,
    }"
  >
    <!-- admin-change-password -->
    <!-- change-image -->
    <template v-slot:item-slot="{ item, key }">
      <span v-if="key === 'operation'">
        <custom-btn
          :label="item.is_approved ? 'الغاء المصادقة' : 'مصادقة'"
          :icon="item.is_approved ? 'check-circle' : 'close-circle'"
          isIcon
          class="text-primary"
          @click="open_approve(item.id, item.approved_to, item.is_approved)"
        />
        <custom-btn
          v-if="isPlatFormSys || state?.is_super_user"
          label="استعادة كلمة المرور"
          icon="lock-reset"
          isIcon
          class="ms-2"
          color="grey"
          @click="(data.id = item.id), (dialog_reset_pass = true)"
        />
        <custom-btn
          :label="item.is_active ? 'الغاء تفعيل' : 'تفعيل'"
          :icon="item.is_active ? 'account-check' : 'account-off'"
          isIcon
          class="ms-2"
          :color="item.is_active ? 'green' : 'warning'"
          @click="toggleActive(item)"
        />

        <custom-btn
          v-if="isSSO"
          label="اسناد الانظمة"
          icon="shield-key"
          isIcon
          class="ms-2"
          color="primary"
          @click="openRolesDialog(item)"
        />
      </span>
    </template>
  </custom-data-table>

  <custom-dialog v-model="dialog_reset_pass" width="300" title="تغيير كلمة المرور">
    <template v-slot>
      <password v-model="password" :id="data?.id" />
    </template>
  </custom-dialog>
  <custom-dialog
    v-if="!approve.is_approved"
    v-model="dialog_approve_user"
    title="مصاقة المدير"
    height="auto"
    width="500"
    class="px-2"
  >
    <template v-slot>
      <custom-date
        v-model="approve.approved_to"
        label="تاريخ انتهاء المصادقة"
        hideDetails="auto"
      />
    </template>
    <template #actions>
      <custom-btn type="save" width="95%" class="mx-2" :click="approveManager" />
    </template>
  </custom-dialog>

  <custom-dialog v-model="rolesDialog" title="اسناد الانظمة" width="500" class="px-2">
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon start color="deep-purple">mdi-shield-key</v-icon>
        أسناد ألانظمة
        <v-spacer></v-spacer>
        <v-chip size="small" color="primary">{{ rolesUser?.username }}</v-chip>
      </v-card-title>

      <v-card-text>
        <v-progress-linear
          v-if="rolesLoading"
          indeterminate
          color="deep-purple"
          class="mb-4"
        ></v-progress-linear>

        <v-alert
          v-if="!rolesLoading && keycloakRoles.length === 0"
          type="info"
          variant="tonal"
          class="mb-4"
        >
          لا توجد أنظمة متاحة في Keycloak
        </v-alert>

        <v-list v-else density="compact">
          <v-list-item
            v-for="role in keycloakRoles"
            :key="role.name"
            @click="toggleRole(role)"
            class="rounded mb-1"
            :class="{ 'bg-deep-purple-lighten-5': role.assigned }"
          >
            <template v-slot:prepend>
              <v-checkbox-btn
                :model-value="role.assigned"
                color="deep-purple"
                @click.stop="toggleRole(role)"
                :loading="role.saving"
                :disabled="role.saving"
              ></v-checkbox-btn>
            </template>
            <v-list-item-title class="font-weight-medium">{{
              role.display_name
            }}</v-list-item-title>
            <v-list-item-subtitle>{{ role.name }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="rolesDialog = false">إغلاق</v-btn>
      </v-card-actions>
    </v-card>
  </custom-dialog>

  <!-- 🛡️ Role Confirmation Dialog -->
  <v-dialog v-model="roleConfirmDialog" max-width="480">
    <v-card rounded="xl" elevation="8">
      <!-- Header with gradient -->
      <div
        :style="{
          background:
            roleConfirmAction === 'assign'
              ? 'linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%)'
              : 'linear-gradient(135deg, #EF5350 0%, #C62828 100%)',
          padding: '24px',
          textAlign: 'center',
        }"
      >
        <v-icon size="48" color="white">
          {{ roleConfirmAction === "assign" ? "mdi-shield-plus" : "mdi-shield-remove" }}
        </v-icon>
        <h3 class="text-white mt-2" style="font-size: 1.2rem; font-weight: 700">
          {{ roleConfirmAction === "assign" ? "تأكيد إسناد الدور" : "تأكيد إزالة الدور" }}
        </h3>
      </div>

      <v-card-text class="pa-6">
        <!-- Operation message -->
        <div class="text-center mb-4">
          <p class="text-body-1 mb-3" style="line-height: 1.8">
            {{
              roleConfirmAction === "assign"
                ? "أنت على وشك إسناد الدور التالي للمستخدم:"
                : "أنت على وشك إزالة الدور التالي من المستخدم:"
            }}
          </p>
        </div>

        <!-- Role & User details -->
        <v-card
          variant="tonal"
          :color="roleConfirmAction === 'assign' ? 'success' : 'error'"
          class="pa-4 rounded-lg mb-4"
        >
          <div class="d-flex align-center mb-3">
            <v-icon
              class="me-3"
              :color="roleConfirmAction === 'assign' ? 'success' : 'error'"
              >mdi-shield-key</v-icon
            >
            <div>
              <div class="text-caption text-medium-emphasis">الدور</div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ roleConfirmRole?.display_name }}
              </div>
            </div>
          </div>
          <v-divider class="mb-3"></v-divider>
          <div class="d-flex align-center">
            <v-icon
              class="me-3"
              :color="roleConfirmAction === 'assign' ? 'success' : 'error'"
              >mdi-account</v-icon
            >
            <div>
              <div class="text-caption text-medium-emphasis">المستخدم</div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ rolesUser?.username }}
              </div>
            </div>
          </div>
        </v-card>

        <!-- Warning -->
        <v-alert
          :type="roleConfirmAction === 'assign' ? 'info' : 'warning'"
          variant="tonal"
          density="compact"
          class="text-body-2"
        >
          {{
            roleConfirmAction === "assign"
              ? "💡 سيتمكن المستخدم من الوصول إلى النظام المرتبط بهذا الدور فوراً."
              : "⚠️ سيفقد المستخدم الوصول إلى النظام المرتبط بهذا الدور فوراً."
          }}
        </v-alert>
      </v-card-text>

      <v-card-actions class="pa-4 pt-0">
        <v-btn variant="text" @click="roleConfirmDialog = false" class="text-body-2">
          تراجع
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          :color="roleConfirmAction === 'assign' ? 'success' : 'error'"
          variant="elevated"
          :loading="roleConfirmLoading"
          @click="executeRoleToggle"
          class="px-6"
        >
          <v-icon start>{{
            roleConfirmAction === "assign" ? "mdi-check-circle" : "mdi-close-circle"
          }}</v-icon>
          {{ roleConfirmAction === "assign" ? "نعم، إسناد الدور" : "نعم، إزالة الدور" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <confirm-dialog
    v-if="approve.is_approved"
    v-model="dialog_approve_user"
    title="تاكيد الغاء المصادقة"
    icon="information"
    color="primary"
    message="هلا انت متاكد من الغاء مصادفة المستخدم"
    :confirmBtn="() => approveManager()"
  />
</template>
<script setup>
import { state } from "@/../src/store/state";
</script>
<script>
import usersApi from "../../../api/users";
import AddUser from "./AddUser.vue";
import { useAuthStore } from "../../../stores/auth";

export default {
  components: { AddUser },

  data() {
    return {
      isSSO: useAuthStore().isSSO,
      data: {},
      items: {},
      password: {},
      filter: {},
      approve: {},

      keycloakRoles: [],

      user_type: undefined,
      rolesUser: null,
      roleConfirmRole: null,

      drawer: false,
      loading: false,
      showPass: false,
      dialog_reset_pass: false,
      dialog_approve_user: false,
      rolesDialog: false,
      rolesLoading: false,
      roleConfirmLoading: false,
      roleConfirmAction: "assign",
      roleConfirmDialog: false,

      url: "user-manager/users/",
      url2: "user-manager/users/filter-paginate/",
    };
  },
  methods: {
    open_approve(id, approved_to, is_approved) {
      this.dialog_approve_user = true;

      this.approve.id = id;
      this.approve.approved_to = approved_to;
      this.approve.is_approved = is_approved;
    },
    async approveManager() {
      const url = this.approve.is_approved ? "unapprove" : "approve";
      await this.$axios
        .post(`user-manager/users/${this.approve.id}/${url}/ `, {
          approved_to: this.approve.approved_to,
        })
        .then((e) => {
          this.$alert("add", { message: e.data });
          this.getData();
        });
    },
    async toggleActive(user) {
      await usersApi.toggleActive(user.id);
      this.$snack("success", {
        message: `تم ${user.is_active ? "إلغاء تفعيل" : "تفعيل"} المستخدم`,
      });

      await this.getData();
    },
    async openRolesDialog(user) {
      this.rolesUser = user;
      this.rolesDialog = true;
      this.rolesLoading = true;

      this.keycloakRoles = [];

      try {
        const data = await usersApi.getKeycloakRoles(user.id);
        this.keycloakRoles = (data.data || data).map((r) => ({
          ...r,
          saving: false,
        }));
      } finally {
        this.rolesLoading = false;
      }
    },

    toggleRole(role) {
      if (role.saving) return;
      // Show confirmation dialog instead of executing immediately
      this.roleConfirmRole = role;
      this.roleConfirmAction = role.assigned ? "remove" : "assign";
      this.roleConfirmDialog = true;
    },
    async executeRoleToggle() {
      const role = this.roleConfirmRole;
      if (!role) return;

      this.roleConfirmLoading = true;
      role.saving = true;

      try {
        if (this.roleConfirmAction === "remove") {
          await usersApi.removeKeycloakRoles(this.rolesUser.id, [role.name]);
          role.assigned = false;
          this.$snack("success", {
            message: `✅ تم إزالة الدور: ${role.display_name}`,
          });
        } else {
          await usersApi.assignKeycloakRoles(this.rolesUser.id, [role.name]);
          role.assigned = true;
          this.$snack("success", {
            message: `✅ تم إسناد الدور: ${role.display_name}`,
          });
        }
        this.roleConfirmDialog = false;
      } finally {
        this.roleConfirmLoading = false;
        role.saving = false;
      }
    },

    async changePassword() {
      const { valid } = await this.$refs.form_password.validate();
      if (!valid) return;

      await this.$axios
        .post(`user-manager/users/${this.data?.id}/admin-change-password/`, {
          new_password: this.password.new_password,
        })
        .then(() => {
          this.$snack("update");
          this.dialog_reset_pass = false;
          this.password = {};
        });
    },
    actionList(item) {
      return [
        {
          title_ar: "صلاحيات الخدمات",
          title_en: "Services Permissions",
          click: () => {
            this.moveToNex("user-services-permissions", { user_id: item.id }, {});
          },
        },
      ];
    },
    moveToNex(screen, params = null, query = null) {
      this.$navigateTo({
        name: screen,
        params: params,
        query: query,
        blank: false,
      });
    },
    async getData(params = this.$params) {
      try {
        this.loading = true;
        if (this.user_type) {
          const filters = {
            filters: [{ field: "fk_user_type", value: this.user_type }],
          };
          return await this.$axios
            .post(this.url2, filters, { ...params })
            .then((response) => (this.items = response.data));
        } else {
          return await this.$axios(this.url, { ...params }).then(
            (response) => (this.items = response.data)
          );
        }
      } finally {
        this.loading = false;
      }
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("first_name"), key: "first_name" },
        { title: this.$t("last_name"), key: "last_name" },
        { title: this.$t("user_name"), key: "username" },
        { title: this.$t("email"), key: "email" },
        // { title: this.$t("system_type"), key: "system_type" },

        { title: this.$t("groups"), key: "groups_names", sortable: false },
        // { title: this.$t("image_user"), key: "image_user", type: "img" },
        { title: this.$t("is_active"), key: "is_active" },
        { title: "العمليات", key: "operation" },
      ];
    },
    isPlatFormSys() {
      // return state?.isSSO||false;
      return state?.isPlatFormSys || false;
    },
  },
  watch: {
    drawer(val) {
      this.data.active_level = false;
    },
    dialog_reset_pass(val) {
      if (!val) this.password = {};
    },
  },
};
</script>
