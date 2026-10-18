<template>
  <div>
    <!-- Sync All Banner -->
    <!-- <v-card class="mb-6 sync-banner" color="primary" variant="flat">
      <v-card-text class="d-flex align-center pa-6">
        <v-avatar size="56" color="white" class="me-4">
          <v-icon size="32" color="primary">mdi-cloud-sync</v-icon>
        </v-avatar>
        <div class="text-white flex-grow-1">
          <h2 class="text-h5 font-weight-bold mb-1">مزامنة شاملة</h2>
          <p class="text-body-2 opacity-80 mb-0">
            مزامنة جميع البيانات (أنواع المستخدمين، المجموعات، المنظمات، مديري
            النظام) إلى جميع الأنظمة الفرعية
          </p>
        </div>
        <v-btn
          color="white"
          variant="elevated"
          size="large"
          :loading="syncAllLoading"
          :disabled="anySyncLoading"
          class="ms-4"
          @click="syncAll"
        >
          <v-icon start>mdi-sync-circle</v-icon>
          مزامنة الكل
        </v-btn>
      </v-card-text>
    </v-card> -->

    <!-- Sync Cards Grid -->
    <v-row>
      <!-- SuperUser Sync -->
      <v-col cols="12" md="6">
        <v-card class="sync-card" elevation="2" :loading="loading.superuser">
          <v-card-text class="pa-5">
            <div class="d-flex align-center mb-4">
              <v-avatar color="error" variant="tonal" size="48" class="me-4">
                <v-icon size="24">mdi-shield-account</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <h3 class="text-h6 font-weight-bold">مديري النظام</h3>
                <p class="text-body-2 text-grey mb-0">SuperUsers</p>
              </div>
              <v-chip :color="getStatusColor('superuser')" variant="tonal" size="small">
                {{ getStatusText("superuser") }}
              </v-chip>
            </div>

            <v-btn
              v-if="loading.superuser"
              color="error"
              variant="tonal"
              block
              size="large"
              @click="cancelRequest('superuser')"
              class="mb-3"
            >
              <v-icon start>mdi-close</v-icon>
              الغاء المزامنة
            </v-btn>
            <v-btn
              v-else
              color="error"
              variant="tonal"
              block
              size="large"
              :disabled="anySyncLoading"
              @click="syncEntity('superuser')"
              class="mb-3"
            >
              <v-icon start>mdi-sync</v-icon>
              مزامنة مديري النظام
            </v-btn>
            <v-alert
              type="info"
              variant="tonal"
              density="compact"
              class="mb-3 text-body-2"
            >
              يتم مزامنة <strong>المنظمة</strong> و<strong>نوع المستخدم</strong>
              تلقائياً مع كل مدير نظام إذا لم تكن موجودة في النظام المستقبل
            </v-alert>
            <sync-results :results="results.superuser" v-if="results.superuser" />
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Organization Sync -->
      <v-col cols="12" md="6">
        <v-card class="sync-card" elevation="2" :loading="loading.organization">
          <v-card-text class="pa-5">
            <div class="d-flex align-center mb-4">
              <v-avatar color="success" variant="tonal" size="48" class="me-4">
                <v-icon size="24">mdi-domain</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <h3 class="text-h6 font-weight-bold">المؤسسات التعليمية</h3>
                <p class="text-body-2 text-grey mb-0">Educational institutions</p>
              </div>
              <v-chip
                :color="getStatusColor('organization')"
                variant="tonal"
                size="small"
              >
                {{ getStatusText("organization") }}
              </v-chip>
            </div>
            <v-btn
              v-if="loading.organization"
              color="error"
              variant="tonal"
              block
              size="large"
              @click="cancelRequest('organization')"
              class="mb-3"
            >
              <v-icon start>mdi-close</v-icon>
              الغاء المزامنة
            </v-btn>
            <v-btn
              v-else
              color="success"
              variant="tonal"
              block
              size="large"
              :loading="loading.organization"
              :disabled="anySyncLoading"
              @click="syncEntity('organization')"
              class="mb-3"
            >
              <v-icon start>mdi-sync</v-icon>
              مزامنة المنظمات
            </v-btn>
            <v-alert
              type="info"
              variant="tonal"
              density="compact"
              class="mb-3 text-body-2"
            >
              يتم مزامنة <strong>المدير</strong> و<strong>مجموعة المدير</strong> و<strong
                >بيانات الاتصال</strong
              >
              و<strong>العنوان</strong>
              تلقائياً مع كل منظمة
            </v-alert>
            <sync-results :results="results.organization" v-if="results.organization" />
          </v-card-text>
        </v-card>
      </v-col>

      <!-- UserType Sync -->
      <v-col cols="12" md="6">
        <v-card class="sync-card" elevation="2" :loading="loading.usertype">
          <v-card-text class="pa-5">
            <div class="d-flex align-center mb-4">
              <v-avatar color="info" variant="tonal" size="48" class="me-4">
                <v-icon size="24">mdi-badge-account</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <h3 class="text-h6 font-weight-bold">أنواع المستخدمين</h3>
                <p class="text-body-2 text-grey mb-0">UserTypes</p>
              </div>
              <v-chip :color="getStatusColor('usertype')" variant="tonal" size="small">
                {{ getStatusText("usertype") }}
              </v-chip>
            </div>
            <v-btn
              v-if="loading.usertype"
              color="error"
              variant="tonal"
              block
              size="large"
              @click="cancelRequest('usertype')"
              class="mb-3"
            >
              <v-icon start>mdi-close</v-icon>
              الغاء المزامنة
            </v-btn>
            <v-btn
              v-else
              color="khaki"
              variant="tonal"
              block
              size="large"
              :loading="loading.usertype"
              :disabled="anySyncLoading"
              @click="syncEntity('usertype')"
              class="mb-3"
            >
              <v-icon start>mdi-sync</v-icon>
              مزامنة أنواع المستخدمين
            </v-btn>
            <v-alert
              type="info"
              variant="tonal"
              density="compact"
              class="mb-3 text-body-2"
            >
              يتم مزامنة <strong>نوع المستخدم الأب</strong> تلقائياً إذا كان مرتبطاً بنوع
              مستخدم آخر
            </v-alert>
            <sync-results :results="results.usertype" v-if="results.usertype" />
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Group Sync -->
      <v-col cols="12" md="6">
        <v-card class="sync-card" elevation="2" :loading="loading.group">
          <v-card-text class="pa-5">
            <div class="d-flex align-center mb-4">
              <v-avatar color="warning" variant="tonal" size="48" class="me-4">
                <v-icon size="24">mdi-account-group</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <h3 class="text-h6 font-weight-bold">المجموعات</h3>
                <p class="text-body-2 text-grey mb-0">Groups</p>
              </div>
              <v-chip :color="getStatusColor('group')" variant="tonal" size="small">
                {{ getStatusText("group") }}
              </v-chip>
            </div>
            <v-btn
              v-if="loading.group"
              color="error"
              variant="tonal"
              block
              size="large"
              @click="cancelRequest('group')"
              class="mb-3"
            >
              <v-icon start>mdi-close</v-icon>
              الغاء المزامنة
            </v-btn>
            <v-btn
              v-else
              color="warning"
              variant="tonal"
              block
              size="large"
              :loading="loading.group"
              :disabled="anySyncLoading"
              @click="syncEntity('group')"
              class="mb-3"
            >
              <v-icon start>mdi-sync</v-icon>
              مزامنة المجموعات
            </v-btn>
            <v-alert
              type="info"
              variant="tonal"
              density="compact"
              class="mb-3 text-body-2"
            >
              يتم مزامنة <strong>مجموعات المدير فقط</strong> — المجموعات المرتبطة بالمنظمة
              ونوع المستخدم
            </v-alert>
            <sync-results :results="results.group" v-if="results.group" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ═══════════════════════════════════════════════════════════════ -->
    <!-- ObjectSync Status Table                                        -->
    <!-- ═══════════════════════════════════════════════════════════════ -->
    <v-card class="mt-8" elevation="2">
      <v-card-title class="d-flex align-center flex-wrap ga-3 pa-4">
        <v-icon start color="primary">mdi-table-eye</v-icon>
        سجلات المزامنة

        <v-spacer />

        <!-- Filter by type -->
        <auto-list
          name="ObjectTypeChoices"
          v-model="tableFilter.object_type"
          @update:model-value="loadSyncTable()"
          cols="2"
          hide-details
        />
      </v-card-title>

      <v-divider />

      <custom-data-table
        :headers="tableHeaders"
        :items="tableItems"
        :getData="loadSyncTable"
        :show-select="false"
        :actions="false"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :customLoading="tableLoading"
      >
        <template v-slot:item="{ item, index }">
          <tr>
            <td>
              {{ index + 1 }}
            </td>
            <td>
              {{ item.object_name }}
            </td>
            <td>
              <!-- ex_id formatted smaller -->
              <span class="text-caption" style="font-family: monospace">{{
                item.object_ex_id
              }}</span>
            </td>
            <td>
              <!-- Object type chip -->
              <v-chip
                size="small"
                :color="objectTypeColor(item.object_type)"
                variant="tonal"
              >
                {{ item.object_type_display }}
              </v-chip>
            </td>

            <td v-for="sys in systems" :key="sys">
              <v-chip
                size="x-small"
                :color="syncStatusColor(item[sys.key])"
                variant="flat"
                v-tooltip:top="item[`${sys.key}_error`]"
              >
                {{ item[`${sys.key}_display`] }}
              </v-chip>
            </td>
            <td>
              {{ item.last_sync_attempt }}
            </td>
          </tr>
        </template>
      </custom-data-table>
    </v-card>

    <!-- Global Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="4000"
      location="bottom end"
    >
      <v-icon start>{{ snackbar.icon }}</v-icon>
      {{ snackbar.text }}
    </v-snackbar>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="confirmDialog.show" max-width="450" persistent>
      <v-card>
        <v-card-title class="d-flex align-center pa-4">
          <v-icon start color="warning">mdi-alert-circle</v-icon>
          تأكيد المزامنة
        </v-card-title>
        <v-card-text>
          <p class="text-body-1">
            هل أنت متأكد من مزامنة
            <strong>{{ confirmDialog.label }}</strong>
            إلى جميع الأنظمة الفرعية؟
          </p>
          <v-alert type="info" variant="tonal" density="compact" class="mt-3">
            سيتم إرسال جميع السجلات التي لم تتم مزامنتها أو تم تعديلها بعد المزامنة.
          </v-alert>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" @click="confirmDialog.show = false">إلغاء</v-btn>
          <custom-btn
            color="primary"
            variant="elevated"
            :loading="confirmDialog.loading"
            @click="executeSync"
            label=" تأكيد المزامنة"
            icon="sync"
          >
          </custom-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="errorMessage.show" max-width="800">
      <VCard class="glass-card" rounded="xl">
        <VCardTitle class="d-flex align-center justify-space-between pa-6">
          <div class="d-flex align-center">
            <VAvatar color="primary" size="48" class="ma-4 glow-icon">
              <VIcon icon="mdi-cloud-sync" color="white" size="28" />
            </VAvatar>

            <div class="text-h5 font-weight-bold">تقرير بحالة المزامنة</div>
          </div>
          <VSpacer />
          <VBtn icon="mdi-close" variant="flat" @click="errorMessage.show = false" />

          <div></div>
        </VCardTitle>
        <VDivider />
        <VCardText>
          <VRow>
            <VCol
              v-for="(system, index) in errorMessage.data"
              :key="index"
              cols="12"
              md="6"
            >
              <VHover v-slot="{ isHovering, props }">
                <VCard
                  v-bind="props"
                  :elevation="isHovering ? 12 : 2"
                  class="system-bento-card overflow-auto"
                  :class="{
                    'border-fail': system?.status == 'error',
                    'border-success': system?.status == 'success',
                  }"
                  variant="flar"
                  min-height="150"
                  max-height="300"
                >
                  <div class="d-flex justify-space-between align-center mb-4">
                    <span class="text-subtitle-1 font-weight-bold">
                      {{ system.system_label }}
                    </span>
                    <VChip
                      :color="system?.status == 'error' ? 'error' : 'primary'"
                      size="small"
                      variant="flat"
                    >
                      {{ system?.status == "success" ? "مكتمل" : "فشل" }}
                    </VChip>
                  </div>
                  <div v-if="system?.status === 'error'">
                    <span v-if="system?.error_type === 'http_404'">
                      لم يتم العثور على الرابط
                    </span>
                    <span v-else>
                      {{ system?.error }}
                    </span>
                  </div>
                  <div
                    class="d-flex justify-space-between gap-2 mt-2"
                    v-else-if="system?.status === 'success'"
                  >
                    <div class="stat-box">
                      <div class="text-caption text-grey-lighten-1">جديد</div>
                      <div class="text-h6 font-weight-bold text-primary">
                        {{ system?.created?.length }}
                      </div>
                    </div>
                    <div class="stat-box border-x">
                      <div class="text-caption text-grey-lighten-1">تحديث</div>
                      <div class="text-h6 font-weight-bold text-green">
                        {{ system?.updated?.length }}
                      </div>
                    </div>
                    <div class="stat-box border-x">
                      <div class="text-caption text-grey-lighten-1">فشل</div>
                      <div class="text-h6 font-weight-bold text-red">
                        {{ system?.failed?.length }}
                      </div>
                      <div>
                        <v-dialog max-width="400" v-if="system?.failed?.length">
                          <template v-slot:activator="{ props: activatorProps }">
                            <v-btn
                              v-bind="activatorProps"
                              dinsety
                              variant="text"
                              color="primary"
                            >
                              عرض
                            </v-btn>
                          </template>
                          <template v-slot:default="{ isActive }">
                            <VCard
                              rounded="xl"
                              class="pa-5"
                              max-height="600"
                              max-width="600"
                            >
                              <VCardTitle>
                                <VRow justify="center" align="center">
                                  <span> العناصر التي فشل النظام في مزامنتها </span>
                                  <VSpacer />

                                  <VBtn
                                    icon="mdi-close"
                                    variant="flat"
                                    @click="isActive.value = false"
                                  />
                                </VRow>

                                <VDivider />
                              </VCardTitle>
                              <VList>
                                <template
                                  v-for="(fail, index) in system?.failed"
                                  :key="fail"
                                >
                                  <VRow>
                                    <span cols="2" class="align-self-center">
                                      {{ index + 1 }} -
                                    </span>
                                    <VCol cols="11">
                                      <VListItem class="bg-header">
                                        {{ fail.error }}
                                      </VListItem>
                                    </VCol>
                                  </VRow>
                                  <VDivider />
                                </template>
                              </VList>
                            </VCard>
                          </template>
                        </v-dialog>
                      </div>
                    </div>
                  </div>
                </VCard>
              </VHover>
            </VCol>
          </VRow>
        </VCardText>
      </VCard>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import syncApi from "../../api/sync";

// ─── Push State ──────────────────────────────────────────────────────

const loading = reactive({
  superuser: false,
  organization: false,
  usertype: false,
  group: false,
});
const syncAllLoading = ref(false);
const results = reactive({
  superuser: null,
  organization: null,
  usertype: null,
  group: null,
});
const status = reactive({
  superuser: "idle",
  organization: "idle",
  usertype: "idle",
  group: "idle",
});

const snackbar = reactive({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});
const confirmDialog = reactive({
  show: false,
  label: "",
  entity: "",
  loading: false,
});

const errorMessage = reactive({
  show: false,
  data: [],
});

const anySyncLoading = computed(
  () => Object.values(loading).some((v) => v) || syncAllLoading.value
);

const entityLabels = {
  superuser: "مديري النظام",
  organization: "المؤسسات التعليمية",
  usertype: "أنواع المستخدمين",
  group: "المجموعات",
};
const apiMap = {
  superuser: () => syncApi.pushSuperUsers(controller.value["superuser"]),
  organization: () => syncApi.pushOrganizations(controller.value["organization"]),
  usertype: () => syncApi.pushUserTypes(controller.value["usertype"]),
  group: () => syncApi.pushGroups(controller.value["group"]),
};

// ─── Table State ─────────────────────────────────────────────────────
const tableLoading = ref(false);
const tableItems = ref({});

const tableFilter = reactive({ object_type: null, search: "" });

const systems = reactive([
  { name: "المنصة الموحدة", key: "unified_educational_platform" },
  { name: "الكنترول", key: "control" },
  { name: "ERP", key: "enterprise_resource_planning" },
  { name: "البوابة", key: "portal" },
  { name: "المدارس", key: "school" },
  { name: "الجامعات", key: "university" },
  { name: "المعاهد", key: "institute" },
  { name: "التسجيل الموحد", key: "sso" },
]);
const tableHeaders = [
  { title: "الاسم", key: "object_name", sortable: false },
  { title: "المعرف (ex_id)", key: "object_ex_id", sortable: false },
  {
    title: "النوع",
    key: "object_type_display",
    width: "130px",
    sortable: false,
  },
  ...systems.map((e) => ({
    title: e.name,
    key: `${e.key}_display`,
    sortable: false,
  })),
  { title: "اخر تاريخ للمزامنة", key: "last_sync_attempt" },
];

async function loadSyncTable(
  params = { params: { page: 1, page_size: 10, sort_by: "id", txt_search: "" } }
) {
  try {
    tableLoading.value = true;
    const resp = await syncApi.getStatus(params, tableFilter.object_type);
    tableItems.value.results = resp.data.results || [];
    tableItems.value.pagination = { page: 1, pageSize: 10, count: resp.data.count };
  } catch (e) {
    this.$snack("errorData", { message: "فشل تحميل سجلات المزامنة" });
  } finally {
    tableLoading.value = false;
  }
}

function objectTypeColor(type) {
  return { 1: "error", 2: "info", 3: "warning", 4: "success" }[type] || "grey";
}
function syncStatusColor(val) {
  // 1=NOT_SYNCED, 2=SYNCED, 3=MODIFIED_AFTER_SYNC, 4=CANNOT_SYNC
  return { 1: "orange", 2: "success", 3: "warning", 4: "grey" }[val] || "grey";
}

// ─── Push Methods ────────────────────────────────────────────────────
function syncEntity(entity) {
  confirmDialog.entity = entity;
  confirmDialog.label = entityLabels[entity];
  confirmDialog.show = true;
  confirmDialog.loading = false;
}

const controller = ref({});
async function executeSync() {
  confirmDialog.show = false;
  const entity = confirmDialog.entity;
  controller.value[entity] = new AbortController();
  confirmDialog.loading = true;
  loading[entity] = true;
  status[entity] = "syncing";
  results[entity] = null;

  try {
    const response = await apiMap[entity]();
    const data = response.data;
    const systemResults = data.results || [];

    results[entity] = systemResults;
    errorMessage.show = true;

    errorMessage.data = systemResults.filter((e) => e.error_type !== "no_url");

    const errorCount = systemResults.filter((r) => r.status === "error").length;
    status[entity] = errorCount === systemResults.length ? "error" : "success";

    // const successCount = systemResults.filter(
    //   (r) => r.status === "success"
    // ).length;
    // const totalCreated = systemResults.reduce(
    //   (s, r) =>
    //     s + (Array.isArray(r.created) ? r.created.length : r.created || 0),
    //   0
    // );
    // const totalUpdated = systemResults.reduce(
    //   (s, r) =>
    //     s + (Array.isArray(r.updated) ? r.updated.length : r.updated || 0),
    //   0
    // );

    // if (errorCount > 0 && successCount > 0) {
    //   showSnackbar(
    //     `${entityLabels[entity]}: نجح ${successCount} أنظمة، فشل ${errorCount}`,
    //     "warning",
    //     "mdi-alert"
    //   );
    // } else if (errorCount > 0) {
    //   showSnackbar(
    //     `فشل مزامنة ${entityLabels[entity]} في جميع الأنظمة`,
    //     "error",
    //     "mdi-alert-circle"
    //   );
    // } else {
    //   showSnackbar(
    //     `تمت مزامنة ${entityLabels[entity]} (إنشاء: ${totalCreated}، تحديث: ${totalUpdated})`,
    //     "success",
    //     "mdi-check-circle"
    //   );
    // }
    loadSyncTable();
  } catch (error) {
    status[entity] = "error";
    const msg = error.response?.data?.detail || error.message || "خطأ غير معروف";
    results[entity] = [
      {
        status: "error",
        system_label: "خطأ عام",
        error: msg,
        error_type: "unexpected",
      },
    ];
    showSnackbar(
      `فشل مزامنة ${entityLabels[entity]}: ${msg}`,
      "error",
      "mdi-alert-circle"
    );
  } finally {
    loading[entity] = false;
    confirmDialog.show = false;
    confirmDialog.loading = false;
  }
}

const cancelRequest = (entity) => {
  controller.value?.[entity].abort();
};
async function syncAll() {
  syncAllLoading.value = true;
  const order = ["usertype", "group", "organization", "superuser"];
  for (const entity of order) {
    syncSelect(entity);
  }
  syncAllLoading.value = false;
  showSnackbar("تمت المزامنة الشاملة", "success", "mdi-check-circle");
  loadSyncTable(); // refresh table
}
async function syncSelect(entity) {
  loading[entity] = true;
  status[entity] = "syncing";
  results[entity] = null;
  try {
    const response = await apiMap[entity]();
    results[entity] = response.data.results || [];
    status[entity] = "success";
  } catch (error) {
    status[entity] = "error";
    const msg = error.response?.data?.detail || error.message || "خطأ";
    results[entity] = [{ status: "error", detail: msg }];
  } finally {
    loading[entity] = false;
  }
}

function getStatusColor(entity) {
  const s = status[entity];
  if (s === "success") return "success";
  if (s === "error") return "error";
  if (s === "syncing") return "info";
  return "grey";
}
function getStatusText(entity) {
  const s = status[entity];

  if (s === "success") return "تمت المزامنة";
  if (s === "error") return "فشل";
  if (s === "syncing") return "جاري...";
  return "جاهز";
}
function showSnackbar(text, color, icon) {
  snackbar.text = text;
  snackbar.color = color;
  snackbar.icon = icon;
  snackbar.show = true;
}
</script>

<script>
/**
 * Inline SyncResults sub-component
 */
export default {
  components: {
    "sync-results": {
      props: { results: { type: Array, default: () => [] } },
      template: `
        <div class="sync-results mt-2">
          <v-divider class="mb-3" />

          <!-- Summary header -->
          <div v-if="results.length > 0" class="d-flex ga-3 mb-3 flex-wrap">
            <v-chip v-if="successCount > 0" color="success" variant="tonal" size="small" prepend-icon="mdi-check-circle">
              نجح: {{ successCount }} نظام
            </v-chip>
            <v-chip v-if="errorCount > 0" color="error" variant="tonal" size="small" prepend-icon="mdi-alert-circle">
              فشل: {{ errorCount }} نظام
            </v-chip>
            <v-chip v-if="pendingCount > 0" color="grey" variant="tonal" size="small" prepend-icon="mdi-minus-circle">
              لا سجلات: {{ pendingCount }}
            </v-chip>
          </div>

          <!-- Per-system results -->
          <div v-for="(r, i) in results" :key="i" class="mb-2">

            <!-- Error -->
            <v-alert v-if="r.status === 'error'" type="error" variant="tonal" density="compact" class="text-body-2">
              <div class="d-flex align-center flex-wrap ga-2">
                <v-icon size="16">{{ errorIcon(r.error_type) }}</v-icon>
                <strong>{{ r.system_label || r.system || 'خطأ' }}</strong>
                <v-chip v-if="r.attempts" size="x-small" variant="outlined" color="error">
                  {{ r.attempts }} محاولة
                </v-chip>
                <v-chip v-if="r.elapsed" size="x-small" variant="outlined">
                  {{ r.elapsed }}s
                </v-chip>
              </div>
              <div class="mt-1 opacity-80">{{ r.error || 'فشل غير معروف' }}</div>
            </v-alert>

            <!-- No pending -->
            <v-alert v-else-if="r.status === 'no_pending'" type="info" variant="tonal" density="compact" class="text-body-2">
              <strong>{{ r.system_label || formatSystem(r.system) }}:</strong> لا توجد سجلات معلقة
            </v-alert>

            <!-- Success -->
            <v-alert v-else-if="r.status === 'success'" type="success" variant="tonal" density="compact" class="text-body-2">
              <div class="d-flex align-center flex-wrap ga-2">
                <v-icon size="16">mdi-check-circle</v-icon>
                <strong>{{ r.system_label || formatSystem(r.system) }}</strong>
                <v-chip v-if="r.attempts" size="x-small" variant="outlined" color="success">
                  {{ r.attempts }} محاولة
                </v-chip>
                <v-chip v-if="r.elapsed" size="x-small" variant="outlined">
                  {{ r.elapsed }}s
                </v-chip>
              </div>
              <div class="mt-1">
                إنشاء: {{ Array.isArray(r.created) ? r.created.length : (r.created || 0) }}
                ، تحديث: {{ Array.isArray(r.updated) ? r.updated.length : (r.updated || 0) }}
              </div>
            </v-alert>
          </div>

          <v-alert v-if="results.length === 0" type="info" variant="tonal" density="compact" class="text-body-2">
            لا توجد أنظمة فرعية تحتاج مزامنة
          </v-alert>
        </div>
      `,
      computed: {
        successCount() {
          return this.results.filter((r) => r.status === "success").length;
        },
        errorCount() {
          return this.results.filter((r) => r.status === "error").length;
        },
        pendingCount() {
          return this.results.filter((r) => r.status === "no_pending").length;
        },
      },
      methods: {
        formatSystem(role) {
          const map = {
            "access-login-role-unified-educational-platform": "المنصة الموحدة",
            "access-login-role-university-management-system": "الجامعات",
            "access-login-role-school": "المدارس",
            "access-login-role-portal": "البوابة",
            "access-login-role-control": "الكنترول",
            "access-login-role-institute": "المعاهد",
            "access-login-role-enterprise-resource-planning": "ERP",
          };
          return map[role] || role || "—";
        },
        errorIcon(type) {
          const icons = {
            connection: "mdi-lan-disconnect",
            timeout: "mdi-clock-alert",
            auth: "mdi-shield-alert",
            no_url: "mdi-link-off",
            unexpected: "mdi-bug",
          };
          return icons[type] || "mdi-alert-circle";
        },
      },
    },
  },
};
</script>

<style scoped>
.sync-banner {
  border-radius: 16px;
  overflow: hidden;
}
.sync-card {
  border-radius: 12px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.sync-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}
.sync-results {
  max-height: 300px;
  overflow-y: auto;
}
.sync-table :deep(th) {
  white-space: nowrap !important;
  font-weight: 700 !important;
}

.system-bento-card {
  border-radius: 16px !important;
  padding: 20px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.5);
}
.system-bento-card:hover {
  transform: translateY(-5px);
}
.border-success {
  border-right: 4px solid rgba(var(--v-theme-primary)) !important;
}
.border-fail {
  border-right: 4px solid #ff5252 !important;
}
.stat-box {
  flex: 1;
  text-align: center;
  padding: 8px;
}
.border-x {
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
