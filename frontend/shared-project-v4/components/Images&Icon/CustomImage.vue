<template>
  <div class="custom-image-component">
    <!-- Title Label -->
    <div v-if="title" class="custom-image-label mb-2">
      {{ title }}
    </div>

    <!-- Image Container Wrapper -->
    <component
      :is="circle ? 'v-avatar' : 'v-card'"
      :height="height"
      :width="width"
      :rounded="circle ? 'full' : 'lg'"
      class="custom-image-container"
      :class="{ clickable: true, 'circle-mode': circle }"
      @click="!canEdit ? () => {} : imageSrc ? (showDialog = true) : triggerFileInput()"
      elevation="0"
    >
      <!-- Action Overlay (Edit/Pencil) -->
      <div v-if="canEdit" class="custom-image-overlay-action">
        <v-dialog v-model="dialog" width="450">
          <template v-slot:activator="{ props }">
            <VBtn
              v-bind="props"
              @click.stop="dialog = true"
              icon="mdi-pencil"
              size="32"
              class="edit-btn shadow-sm"
              :disabled="disabled"
              color="primary"
              variant="elevated"
            />
          </template>

          <v-card class="image-dialog-card overflow-hidden">
            <v-toolbar color="transparent" density="compact" class="px-2">
              <v-toolbar-title class="text-subtitle-1 font-weight-bold">
                {{ title ? title : "عرض الصورة" }}
              </v-toolbar-title>
              <v-spacer />
              <v-btn
                icon="mdi-close"
                variant="text"
                size="small"
                @click="dialog = false"
              />
            </v-toolbar>

            <v-divider />

            <div
              class="pa-4 bg-surface d-flex justify-center align-center min-h-300"
              style="background-color: rgba(var(--v-theme-on-surface), 0.02) !important"
            >
              <v-img
                v-if="imageSrc"
                :src="imageSrc"
                width="100%"
                max-height="400"
                contain
                class="rounded-md shadow-sm"
              />
              <div v-else class="text-center py-10">
                <v-icon
                  icon="mdi-account-circle-outline"
                  size="80"
                  style="color: rgba(var(--v-theme-on-surface), 0.12)"
                />
                <div class="mt-2" style="color: rgba(var(--v-theme-on-surface), 0.6)">
                  لا توجد صورة
                </div>
              </div>
            </div>

            <v-divider />

            <v-card-actions class="pa-4 bg-surface">
              <v-btn
                v-if="!imageSrc"
                variant="elevated"
                color="primary"
                prepend-icon="mdi-camera-plus"
                block
                class="rounded-md"
                height="44"
                @click="triggerFileInput"
              >
                إضافة صورة
              </v-btn>

              <div v-else class="d-flex gap-x-2 w-100">
                <CustomBtn
                  v-if="changeImg"
                  type="save"
                  variant="tonal"
                  height="44"
                  :click="changeImg"
                />
                <v-btn
                  variant="tonal"
                  color="secondary"
                  prepend-icon="mdi-pencil"
                  flex="1"
                  class="rounded-md flex-grow-1"
                  height="44"
                  @click="triggerFileInput"
                  :loading="loading"
                >
                  تغيير
                </v-btn>

                <v-btn
                  variant="tonal"
                  color="error"
                  prepend-icon="mdi-trash-can-outline"
                  flex="1"
                  class="rounded-md flex-grow-1"
                  height="44"
                  @click="removeImage"
                  :loading="loading"
                >
                  إزالة
                </v-btn>
              </div>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>

      <!-- Main Image Display -->

      <VImg
        :src="imageSrc"
        :height="height"
        :width="width"
        :max-height="height"
        :max-width="width"
        cover
        class="main-image"
        style="overflow: hidden"
      >
        <!-- Loading State (Shimmer) -->
        <template v-slot:placeholder>
          <div class="shimmer-wrapper">
            <div class="shimmer-base"></div>
          </div>
        </template>

        <!-- Error / Empty State -->
        <template v-slot:error>
          <div
            class="error-placeholder d-flex flex-column align-center justify-center h-100"
          >
            <v-icon
              icon="mdi-image-off-outline"
              size="32"
              style="color: rgba(var(--v-theme-on-surface), 0.12)"
            />
            <span
              v-if="!circle && height > 80"
              class="text-caption mt-1"
              style="color: rgba(var(--v-theme-on-surface), 0.4)"
              >خطأ في التحميل</span
            >
          </div>
        </template>

        <!-- Empty State UI -->
        <div
          v-if="!imageSrc"
          class="empty-state-placeholder d-flex flex-column align-center justify-center h-100"
        >
          <v-icon
            :icon="circle ? 'mdi-account' : 'mdi-image-outline'"
            :size="circle ? '40' : '36'"
            style="color: rgba(var(--v-theme-on-surface), 0.08)"
          />
          <span
            v-if="!circle && height > 100"
            class="text-caption mt-2"
            style="color: rgba(var(--v-theme-on-surface), 0.4)"
            >لا توجد صورة</span
          >
        </div>

        <!-- Hidden File Input -->
        <v-file-input
          v-show="false"
          v-model="value"
          ref="fileInput"
          accept="image/*"
          :hide-input="true"
          class="position-absolute"
          prepend-icon=""
          @change="changeImage"
        />
      </VImg>
    </component>

    <custom-dialog v-model="showDialog" title="عرض الصورة">
      <template v-slot>
        <div class="d-flex justify-center align-center pa-4">
          <VImg :src="imageSrc" width="100%" contain max-height="85vh" />
        </div>
      </template>
    </custom-dialog>
  </div>
</template>

<script>
import { VSheet } from "vuetify/components";
import { VAvatar } from "vuetify/components";
export default {
  components: {
    VSheet,
    VAvatar,
  },
  props: {
    title: String,
    modelValue: {
      type: [String, Object],
      default: null,
    },
    width: {
      type: String,
      default() {
        return "200";
      },
    },
    height: {
      type: String,
      default() {
        return "200";
      },
    },
    changeImg: Function,
    removeImg: Function,
    circle: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    canEdit: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      imageSrc: undefined,
      dialog: false,
      loading: false,

      showDialog: false,
      base_url: this.setting.url_img,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.$el.querySelector('input[type="file"]').click();
    },
    async changeImage() {
      // try {
      //   this.loading = true;
      //   if (this.changeImg) {
      //     await this.changeImg();
      //   }
      // } catch (error) {
      //   console.log(error);
      //   this.value = null;
      //   this.imageSrc = null;
      // } finally {
      //   this.loading = false;
      // }
    },
    async removeImage() {
      try {
        this.loading = true;
        if (this.removeImg) {
          await this.removeImg();
          this.value = undefined;
          this.imageSrc = undefined;
        } else {
          this.value = null;
          this.imageSrc = null;
        }
      } catch (error) {
      } finally {
        this.loading = false;
      }
    },
  },
  computed: {
    value: {
      get() {
        if (this.modelValue && this.modelValue instanceof File) {
          this.imageSrc = URL.createObjectURL(this.modelValue);
        } else if (this.modelValue != null) {
          this.imageSrc = this.base_url + this.modelValue;
        } else {
          this.imageSrc = null;
        }
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>

<style scoped>
.custom-image-component {
  display: inline-block;
  vertical-align: top;
}

.custom-image-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.7);
  text-align: center;
}

.custom-image-container {
  position: relative;
  background-color: rgba(var(--v-theme-on-surface), 0.03);
  /* border: 1px solid transparent; */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.custom-image-container.clickable {
  cursor: pointer;
}

.custom-image-container:hover {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: var(--shadow-md) !important;
}

.custom-image-container:hover .main-image {
  transform: scale(1.04);
}

.main-image {
  transition: transform 0.4s ease;
}

/* Action Overlay Styling */
.custom-image-overlay-action {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  pointer-events: none;
}

.edit-btn {
  position: absolute;
  bottom: var(--space-sm);
  left: var(--space-sm);
  pointer-events: auto;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s ease, transform 0.3s ease-out;
}

.custom-image-container:hover .edit-btn {
  opacity: 1;
  transform: translateY(0);
}

/* States Styling */
.shimmer-wrapper {
  width: 100%;
  height: 100%;
  background: rgba(var(--v-theme-on-surface), 0.05);
  overflow: hidden;
}

.shimmer-base {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(var(--v-theme-surface), 0) 0%,
    rgba(var(--v-theme-surface), 0.6) 50%,
    rgba(var(--v-theme-surface), 0) 100%
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }

  100% {
    transform: translateX(100%);
  }
}

.empty-state-placeholder,
.error-placeholder {
  background-color: rgba(var(--v-theme-on-surface), 0.02);
}

/* Dialog Styling */
.min-h-300 {
  min-height: 300px;
}

.gap-x-2 {
  gap: 8px;
}

.preview-dialog :deep(.v-overlay__content) {
  margin: 16px;
}
</style>
