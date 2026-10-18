<template>
  <!-- ══════════════════════════════════════════════════════
       MODE: nav-bar (Slide-in Drawer)
  ══════════════════════════════════════════════════════ -->
  <VForm
    v-model="valid"
    v-if="type_screen === 'nav-bar'"
    ref="form"
    @submit.prevent="handleSubmit"
  >
    <VNavigationDrawer
      app
      v-model="value"
      temporary
      :width="$vuetify.display.mobile ? '1000' : parseInt(width) + 20"
      class="drawer-wrapper"
      color="transparent"
      elevation="0"
      border="none"
      :location="$i18n.locale !== 'ar' ? 'right' : 'left'"
      v-if="first_load"
    >
      <div class="drawer-card">
        <!-- ── Header ── -->
        <div class="drawer-header-wrapper">
          <!-- Top dynamic stripe -->
          <div
            class="drawer-top-stripe"
            :class="data.id ? 'drawer-top-stripe--edit' : 'drawer-top-stripe--add'"
          />

          <div class="drawer-header">
            <!-- Left: Icon Avatar + Text -->
            <div class="drawer-header-inner">
              <div
                class="drawer-accent-bar"
                :class="data.id ? 'drawer-accent-bar--edit' : 'drawer-accent-bar--add'"
              />
              <div>
                <h3
                  class="drawer-title"
                  :class="data.id ? 'text-warning' : 'text-primary'"
                >
                  {{ computedTitle }}
                </h3>
              </div>
            </div>

            <!-- Right: Close -->
            <button
              type="button"
              class="drawer-close-btn"
              @click="handleCancel"
              aria-label="close"
            >
              <VIcon size="16">mdi-close</VIcon>
            </button>
          </div>
          <VDivider class="drawer-divider" />
        </div>

        <!-- ── Content ── -->
        <div class="drawer-content-wrapper">
          <slot :value="value" />
        </div>

        <!-- ── Footer ── -->
        <div class="drawer-footer-wrapper" v-if="actions || $slots.actions">
          <slot name="actions" />
          <template v-if="actions">
            <VDivider class="drawer-divider" />
            <div class="drawer-footer">
              <custom-btn type="cancel" :click="handleCancel" elevation="0" />
              <custom-btn
                :type="data.id ? 'update' : 'save'"
                :color="data.id ? 'warning' : 'primary'"
                :click="handleSubmit"
                :disabled="disabledBtn"
                is_submit
              />
            </div>
          </template>
        </div>
      </div>
    </VNavigationDrawer>
  </VForm>

  <!-- ══════════════════════════════════════════════════════
       MODE: dialog
  ══════════════════════════════════════════════════════ -->
  <VDialog
    v-else-if="type_screen === 'dialog'"
    v-model="value"
    :width="$vuetify.display.mobile ? '100%' : width"
    :height="$vuetify.display.mobile ? '100%' : height"
    :fullscreen="$vuetify.display.mobile"
    transition="dialog-bottom-transition"
  >
    <VForm v-model="valid" ref="form" @submit.prevent="handleSubmit">
      <VCard class="dialog-card overflow-hidden">
        <!-- Top dynamic stripe -->
        <div
          class="drawer-top-stripe"
          :class="data.id ? 'drawer-top-stripe--edit' : 'drawer-top-stripe--add'"
        />

        <!-- Dialog Header -->
        <div class="dialog-header">
          <div class="drawer-header-inner">
            <div
              class="drawer-accent-bar"
              :class="data.id ? 'drawer-accent-bar--edit' : 'drawer-accent-bar--add'"
            />
            <div>
              <h3 class="dialog-title" :class="data.id ? 'text-warning' : 'text-primary'">
                {{ computedTitle }}
              </h3>
            </div>
          </div>
          <button
            type="button"
            class="drawer-close-btn"
            @click="value = false"
            aria-label="close"
          >
            <VIcon size="16">mdi-close</VIcon>
          </button>
        </div>

        <VDivider class="drawer-divider" />

        <!-- Dialog Body -->
        <VContainer class="dialog-body overflow-auto">
          <slot />
        </VContainer>

        <!-- Dialog Footer -->
        <v-card-action>
          <VSheet class="overflow-hidden">
            <slot name="actions" />
            <template v-if="actions">
              <VDivider class="drawer-divider" />
              <div class="drawer-footer">
                <custom-btn type="cancel" :click="handleCancel" elevation="0" />
                <custom-btn
                  :type="data.id ? 'update' : 'save'"
                  :color="data.id ? 'warning' : 'primary'"
                  :click="handleSubmit"
                  :disabled="disabledBtn"
                  is_submit
                />
              </div>
            </template>
          </VSheet>
        </v-card-action>
      </VCard>
    </VForm>
  </VDialog>

  <!-- ══════════════════════════════════════════════════════
       MODE: component (inline / page section)
  ══════════════════════════════════════════════════════ -->
  <VForm v-model="valid" v-else ref="form" @submit.prevent="handleSubmit">
    <component :is="type" class="overflow-auto pa-5">
      <slot :value="value" />
      <slot name="actions" />

      <template v-if="actions">
        <VDivider class="my-4" />
        <VRow class="py-2">
          <VCol class="text-center">
            <custom-btn
              :type="data.id ? 'update' : 'save'"
              :color="data.id ? 'warning' : 'primary'"
              :click="handleSubmit"
              :disabled="disabledBtn"
              is_submit
            />
          </VCol>
        </VRow>
      </template>
    </component>
  </VForm>

  <!-- Confirm discard dialog -->
  <confirm-dialog
    v-model="dialog_change_state"
    type_btn="ok"
    :confirmBtn="() => (value = false)"
    title="تنبية "
    :cancel="() => (this.value = true)"
    message="هل انت متاكد من تجاهل جميع التغيرات ؟ "
    type="warning"
  />
</template>

<script>
import { VRow, VCol, VContainer, VCard, VSheet } from "vuetify/components";
import _ from "lodash";

export default {
  name: "Drawer",
  components: { VRow, VCol, VContainer, VCard, VSheet },
  props: {
    title: {
      type: String,
      default: "",
    },
    type: String,
    click: [Function, String],
    cancel: Function,
    getData: Function,
    actions: {
      type: Boolean,
      default: true,
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
    data: {
      type: Object,
      default: () => ({}),
    },
    width: {
      type: String,
      default: "300",
    },
    re_open: {
      type: Boolean,
      default: true,
    },
    files: {
      type: Array,
      default: [],
    },

    items: [Array, Object],

    extraData: { type: Object, default: {} },

    beforeSave: { type: Function, default: () => true },
  },

  data() {
    return {
      change_state: false,
      dialog_change_state: false,
      disabledBtn: false,
      data_patch: undefined,
      valid: false,
      type_screen: "nav-bar",
      first_load: false,
    };
  },
  created() {
    if (this.type) this.type_screen = this.type;
  },
  computed: {
    computedTitle() {
      if (!this.data?.id)
        return `${this.$i18n.locale == "ar" ? "إضافة" : "Add"} ${this.title}`;
      return `${this.$i18n.locale == "ar" ? "تعديل " : "update "} ${this.title}`;
    },
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
  methods: {
    handleCancel() {
      if (this.cancel) this.cancel();
      else this.value = false;
    },
    async handleSubmit() {
      if (!this.beforeSave()) return;

      const { valid } = await this.$refs.form.validate();
      if (valid && this.click) {
        if (typeof this.click === "function")
          await this.click().then((response) => {
            this.value = false;
            this.$snack(this.data.id ? "update" : "add");
            if (this.re_open === true) {
              setTimeout(() => {
                if (!this.data.id) this.value = true;
              }, 500);
            }
            this.resetForm();
            if (this.getData) this.getData();
          });
        else if (typeof this.click === "string") await this.entryData();
      }
    },
    removeSuffix(inputString) {
      if (inputString.includes("__")) {
        return inputString.split("__")[0];
      }
      return inputString;
    },
    async entryData() {
      var data = { ...this.data, ...this.extraData };
      let headers;

      if (data.id) {
        var is_patch = false;
        for (const key in data) {
          if (
            this.files.includes(key) &&
            Object.prototype.toString.call(data[key]) === "[object File]"
          ) {
            is_patch = true;
          } else if (this.files.includes(key) && typeof data[key] == "string") {
            delete data[key];
          }
        }

        is_patch
          ? await this.$axios
              .patch(
                `${this.click}${data.id}/`,
                { ...data },
                { headers: { "Content-Type": "multipart/form-data" } }
              )
              .then((response) => {
                this.value = false;
                this.$snack("update");
                this.resetForm();
                this.value = false;
                const updatedItem = response?.data?.data || response?.data;
                if (this.getData) this.getData();
                if (this.items === undefined) {
                } else {
                  try {
                    if ("results" in this.items) {
                      const index = this.items.results.findIndex(
                        (item) => item.id === updatedItem.id
                      );
                      if (index !== -1) {
                        this.items.results.splice(index, 1, updatedItem);
                      }
                    } else {
                      const index = this.items.findIndex(
                        (item) => item.id === updatedItem.id
                      );
                      if (index !== -1) {
                        this.items.splice(index, 1, updatedItem);
                      }
                    }
                  } catch (error) {}
                }
                this.$emit("after-patch");
              })
          : await this.$axios
              .put(`${this.click}${data.id}/`, { ...data })
              .then((response) => {
                this.value = false;
                this.$snack("update");
                this.resetForm();
                this.value = false;
                const updatedItem = response?.data?.data || response.data;
                updatedItem.new_colors = true;
                if (this.items === undefined) {
                  if (this.getData) this.getData();
                } else {
                  try {
                    if ("results" in this.items) {
                      const index = this.items.results.findIndex(
                        (item) => item.id === updatedItem.id
                      );
                      if (index !== -1) {
                        this.items.results.splice(index, 1, updatedItem);
                      }
                    } else {
                      const index = this.items.findIndex(
                        (item) => item.id === updatedItem.id
                      );
                      if (index !== -1) {
                        this.items.splice(index, 1, updatedItem);
                      }
                    }
                  } catch (error) {}
                }
                this.$emit("after-put");
              });
      } else {
        for (const key in data) {
          if (Object.prototype.toString.call(data[key]) === "[object File]")
            headers = {
              "Content-Type": "multipart/form-data",
            };
        }
        await this.$axios.post(this.click, { ...data }, { headers }).then((response) => {
          this.value = false;
          this.$snack("add");
          this.resetForm();
          const newData = { ...response?.data?.data, new_colors: true };
          if (this.items === undefined) {
            if (this.getData) this.getData();
          } else {
            try {
              if ("results" in this.items) {
                this.items.results.unshift(newData);
                if ("pagination" in this.items) {
                  this.items.pagination.count += 1;
                  let totalPages = Math.ceil(
                    this.items.pagination.count / this.items.pagination.page_size
                  );
                  this.items.pagination.num_pages = totalPages;
                }
              } else {
                this.items.unshift(newData);
              }
            } catch (error) {
              if (this.getData) this.getData();
            }
          }
          if (this.re_open === true)
            setTimeout(() => {
              this.value = true;
            }, 500);
          this.$emit("after-post");
        });
      }
    },
    resetForm() {
      this.$refs.form.reset();
      this.data_patch = undefined;
      for (const key in this.data) {
        if (Object.prototype.toString.call(this.data[key]) === "[object Object]")
          this.data[key] = {};
        else if (typeof this.data[key] == "boolean") this.data[key] = false;
        else this.data[key] = null;
      }
      this.disabledBtn = false;
    },
  },
  watch: {
    value(newValue) {
      if (!newValue) {
        // High-end UX: Delay data reset until drawer is out of sight
        this.resetForm();
      } else {
        this.first_load = true;
        if (this.data.id) this.data_patch = { ...this.data };
      }
    },
    data: {
      handler(newValue, oldValue) {
        this.disabledBtn = this.data.id && !oldValue.id && newValue.id;
        if (this.data.id) {
          this.change_state = !this.disabledBtn;
        }
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
/* ── Scrim: Full-screen light black overlay ── */
:deep(.v-navigation-drawer__scrim) {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(0, 0, 0, 0.7) !important;
  z-index: 99 !important;
}

/* ══════════════════════════════════════════════════════
   Base Drawer & Card Layout
══════════════════════════════════════════════════════ */
.drawer-wrapper {
  overflow: visible !important;
}

.drawer-card {
  height: calc(100% - 85px);
  margin: 10px;
  /* margin-top: 30px; */
  display: flex;
  flex-direction: column;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-on-surface), 0.12);
  border-left: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

/* Subtle background pattern for premium feel */
.drawer-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 160px;
  background: radial-gradient(
    circle at top right,
    rgba(var(--v-theme-primary), 0.05),
    transparent
  );
  pointer-events: none;
  z-index: 0;
}

.drawer-content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 14px 10px;
  position: relative;
  z-index: 1;
}

/* Staggered Reveal Animation for high-end feel */
.drawer-content-wrapper > * {
  animation: reveal-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}

/* Precise staggered delays for first 4 elements */
.drawer-content-wrapper > *:nth-child(1) {
  animation-delay: 0.1s;
}

.drawer-content-wrapper > *:nth-child(2) {
  animation-delay: 0.15s;
}

.drawer-content-wrapper > *:nth-child(3) {
  animation-delay: 0.2s;
}

.drawer-content-wrapper > *:nth-child(4) {
  animation-delay: 0.25s;
}

@keyframes reveal-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ══════════════════════════════════════════════════════
   Dialog Card Mode
══════════════════════════════════════════════════════ */
.dialog-card {
  border-radius: 16px !important;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-on-surface), 0.12);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
  overflow: hidden;
}

/* ══════════════════════════════════════════════════════
   Visual Elements: Stripe & Accents
══════════════════════════════════════════════════════ */
.drawer-top-stripe {
  height: 4px;
  width: 100%;
  position: relative;
  z-index: 20;
}

.drawer-top-stripe--add {
  background: linear-gradient(90deg, rgb(var(--v-theme-primary)), #60a5fa, transparent);
}

.drawer-top-stripe--edit {
  background: linear-gradient(90deg, #f59e0b, #fbbf24, transparent);
}

.drawer-header-wrapper {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgb(var(--v-theme-surface));
}

.drawer-header,
.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  min-height: 80px;
}

.drawer-header-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* ── Accent Bar ── */
.drawer-accent-bar {
  width: 5px;
  height: 32px;
  border-radius: 4px;
  flex-shrink: 0;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.drawer-accent-bar--add {
  background: rgb(var(--v-theme-primary));
  box-shadow: 0 0 15px rgba(var(--v-theme-primary), 0.4);
}

.drawer-accent-bar--edit {
  background: #f59e0b;
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
}

/* ══════════════════════════════════════════════════════
   Typography & Controls
══════════════════════════════════════════════════════ */
.drawer-title,
.dialog-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: rgb(var(--v-theme-on-surface));
  letter-spacing: -0.02em;
  margin: 0 !important;
}

.drawer-close-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(var(--v-theme-on-surface), 0.04);
  color: rgba(var(--v-theme-on-surface), 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}

.drawer-close-btn:hover {
  background: rgba(var(--v-theme-error), 0.08);
  color: rgb(var(--v-theme-error));
  border-color: rgba(var(--v-theme-error), 0.1);
  transform: rotate(90deg);
}

/* ══════════════════════════════════════════════════════
   Footer & Dividers
══════════════════════════════════════════════════════ */
.drawer-divider {
  opacity: 0.06;
}

.drawer-footer-wrapper {
  position: sticky;
  bottom: 0;
  z-index: 10;
}

.drawer-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: rgb(var(--v-theme-surface));
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

/* Scrollbar refinement */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 20px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.2);
}

/* RTL Specific Adjustments */
[dir="rtl"] .drawer-card {
  border-left: none;
  border-right: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.15);
}
</style>
