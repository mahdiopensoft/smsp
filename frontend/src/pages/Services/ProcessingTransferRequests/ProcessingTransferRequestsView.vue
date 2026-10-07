<template>
  <!-- <pre dir="ltr">{{ items }}</pre> -->
  <custom-data-table
    :="{
      items,
      getData,
      headers,
      actions: false,
    }"
  >
    <!-- قبول الكل -->
    <!-- <template v-slot:action>
      <custom-btn
        v-if="Object.keys(items).length > 0"
        :label="$t('approv_all')"
        icon="account-multiple-check-outline"
        color="primary"
        cols="2"
        class="ml-2"
        @click="saveAll()"
      ></custom-btn>
    </template> -->
    <template v-slot:item-slot="{ item, key }">
      <div v-if="key == 'approval_step__status__display'">
        <v-chip
          color="primary"
          variant="tonal"
          rounded="0"
          class="text-sm rounded mb-3"
          style="border-radius: 10px"
          text-color="white"
        >
          {{ item.approval_step__status__display }}
        </v-chip>
        <span>
          {{ item.approval_step__rejection_reason }}
        </span>
      </div>
      <div v-if="key == 'actions'">
        <!-- قبول -->
        <v-btn
          density="comfortable"
          variant="tonal"
          color="primary"
          @click="openDialogApproveTransfer(item.approval_step)"
        >
          <template #prepend>
            <v-icon>mdi-check</v-icon>
            <v-divider vertical class="mx-1"></v-divider>
          </template>
          <span>قبول</span>
        </v-btn>
        <!-- رفص -->
        <v-btn
          density="comfortable"
          variant="tonal"
          color="error"
          class="ms-2"
          @click="openDialogRejectTransfer(item.approval_step, item.request)"
        >
          <template #prepend>
            <v-icon>mdi-cancel</v-icon>
            <v-divider vertical class="mx-1"></v-divider>
          </template>
          <span>رفض</span>
        </v-btn>
      </div>
    </template>
  </custom-data-table>
  <confirm-dialog
    v-model="confirm_dialog_approve_transfer"
    type="info"
    :confirmBtn="approveTransfer"
    title="رسالة تاكيد"
    :message="'سوف يتم قبول الطالب وتسجيلة '"
  />
  <!-- <confirm-dialog
    v-model="confirm_dialog_reject_transfer"
    type="info"
    :confirmBtn="rejectTransfer"
    title="رسالة تاكيد"
    :message="'سوف يتم الغاء قبول الطالب'"
    ><template v-slot:body>
      <custom-btn
        type="cancel"
        :label="this.$t('generate-new-student')"
        size="small"
        density="compact"
        :click="() => (fileDialog.show = false)"
      ></custom-btn> </template
  ></confirm-dialog> -->
  <custom-dialog
    v-model="confirm_dialog_reject_transfer"
    title="رفض الطلب للنقل"
    width="400"
    height="auto"
  >
    <template v-slot>
      <VForm ref="reason_form">
        <custom-text-note
          v-model="reason"
          icon=""
          :label="$t('reason')"
          :rules="[$max_length(250), $required]"
        />
      </VForm>
    </template>
    <template #actions>
      <v-row class="justify-center">
        <custom-btn
          :label="this.$t('reject-step')"
          type="del"
          size="small"
          density="default"
          :click="rejectTransfer"
        ></custom-btn>
        <custom-btn
          :label="this.$t('final-rejection')"
          type="del"
          class="ms-1"
          size="small"
          density="default"
          :click="finalTransfer"
        ></custom-btn>
      </v-row>
    </template>
  </custom-dialog>
</template>
<script>
export default {
  data() {
    return {
      confirm_dialog_approve_transfer: false,
      confirm_dialog_reject_transfer: false,
      request: {},
      data: {},
      reason: null,
      items: {},
      url: "d-services/workflow-tasks/my-tasks/",
    };
  },
  async created() {
    await this.getData();
  },
  computed: {
    headers() {
      return [
        {
          title: this.$t("student_name"),
          key: "approval_step__transfer__fk_student_class__fk_student__name_ar",
        },
        {
          title: this.$t("branch-class"),
          key: "approval_step__transfer__fk_student_class__fk_branch_class__fk_class__name_ar",
        },
        {
          title: this.$t("school_name"),
          key: "request__fk_from_branch__name_ar",
        },
        {
          title: this.$t("reason"),
          key: "request__reason",
        },
        {
          title: this.$t("request_status"),
          key: "approval_step__status__display",
        },
        {
          title: this.$t("actions"),
          key: "actions",
        },
      ];
    },
  },
  methods: {
    // جلب الطلبات
    async getData(params = this.$params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items.results = response.data.results)
      );
    },
    // قبول الطلب
    async approveTransfer() {
      return await this.$axios
        .post(`d-services/workflow-tasks/${this.approval_step}/approval/`, {
          step_id: this.approval_step,
        })
        .then(() => {
          this.$snack("update");
          this.getData();
        });
    },
    // ديلوف القبول
    openDialogApproveTransfer(approval_step) {
      (this.approval_step = approval_step),
        (this.confirm_dialog_approve_transfer = true);
    },
    // ديلوق الرفض
    openDialogRejectTransfer(approval_step, request) {
      (this.approval_step = approval_step),
        (this.transfer_ids = request),
        (this.confirm_dialog_reject_transfer = true);
    },
    // دلة الرفض المرحلي
    async rejectTransfer() {
      const { valid } = await this.$refs.reason_form.validate();
      if (valid) {
        return await this.$axios
          .post(
            `d-services/workflow-tasks/${this.approval_step}/reject_approval/ `,
            {
              step_id: this.approval_step,
              reason: this.reason,
            }
          )
          .then(() => {
            this.$snack("update");
            this.getData();
          });
      }
    },
    // دلة الرفض النهائي
    async finalTransfer() {
      const { valid } = await this.$refs.reason_form.validate();
      if (valid) {
        return await this.$axios
          .post("d-services/workflow-tasks/reject-transfer/", {
            transfer_ids: this.transfer_ids,
            reason: this.reason,
          })
          .then(() => {
            this.$snack("update");
            this.getData();
          });
      }
    },
    // saveAll() {
    //   const allIds = this.items.results.map((s) => s.transfer_id);
    //   this.transfer_id = allIds;
    //   this.approveTransfer();
    // },
  },
};
</script>
