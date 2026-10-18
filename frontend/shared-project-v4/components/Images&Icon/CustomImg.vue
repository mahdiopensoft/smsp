<template>
  <div class="custom-img-upload-component">
    <!-- Optional Title -->
    <div v-if="title" class="custom-img-label mb-2">
      {{ title }}
    </div>

    <v-hover>
      <template v-slot:default="{ isHovering, props }">
        <div
          v-bind="props"
          class="custom-img-container"
          :class="{ 'is-empty': !imageSrc, 'is-hovering': isHovering && imageSrc }"
          :style="{
            height: height + (height.includes('px') ? '' : 'px'),
            width: width + (width.includes('px') ? '' : 'px'),
          }"
        >
          <!-- Quick Actions Overlay (when image exists) -->
          <div
            v-if="imageSrc"
            class="img-actions-overlay"
            :class="{ visible: isHovering }"
          >
            <v-btn
              icon="mdi-eye-outline"
              variant="elevated"
              color="white"
              size="36"
              class="mx-1 action-btn"
              @click.stop="dialog = true"
            />
            <v-btn
              icon="mdi-trash-can-outline"
              variant="elevated"
              color="white"
              size="36"
              class="mx-1 action-btn delete"
              @click.stop="(value = undefined), (imageSrc = undefined)"
            />
          </div>

          <!-- Preview Dialog -->
          <v-dialog v-model="dialog" width="500">
            <v-card class="rounded-xl overflow-hidden shadow-xl">
              <v-toolbar color="transparent" density="compact" class="px-2">
                <v-spacer />
                <v-btn
                  icon="mdi-close"
                  variant="text"
                  size="small"
                  @click="dialog = false"
                />
              </v-toolbar>
              <div class="pa-4 pt-0">
                <v-img :src="imageSrc" cover class="rounded-lg shadow-sm" />
              </div>
            </v-card>
          </v-dialog>

          <!-- Main Image / Upload Zone -->
          <VImg
            :src="imageSrc"
            height="100%"
            width="100%"
            cover
            class="display-img"
            @click="triggerFileInput"
          >
            <!-- Loading State -->
            <template v-slot:placeholder>
              <div class="shimmer-wrapper">
                <div class="shimmer-base"></div>
              </div>
            </template>

            <!-- Empty / Upload State UI -->
            <div
              v-if="!imageSrc"
              class="upload-placeholder d-flex flex-column align-center justify-center fill-height"
            >
              <div class="upload-icon-wrapper mb-2">
                <v-icon icon="mdi-cloud-upload-outline" size="32" color="primary" />
              </div>
              <span class="text-caption font-weight-bold text-primary">
                {{ $i18n.locale == "ar" ? "رفع صورة" : "Upload Photo" }}
              </span>
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
            />
          </VImg>
        </div>
      </template>
    </v-hover>
  </div>
</template>

<style scoped>
.custom-img-upload-component {
  display: inline-block;
  vertical-align: top;
}

.custom-img-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.7);
  text-align: center;
}

.custom-img-container {
  position: relative;
  background-color: rgba(var(--v-theme-on-surface), 0.02);
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.1);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: border-color 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.custom-img-container:not(.is-empty) {
  border-style: solid;
  border-color: rgba(var(--v-theme-on-surface), 0.08);
}

.custom-img-container:hover {
  border-color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.02);
  box-shadow: var(--shadow-md);
}

.custom-img-container.is-hovering .display-img {
  transform: scale(1.05);
  filter: brightness(0.85);
}

.display-img {
  transition: all 0.4s ease;
}

/* Action Overlay */
.img-actions-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.img-actions-overlay.visible {
  opacity: 1;
  pointer-events: auto;
}

.action-btn {
  transform: translateY(10px);
  transition: opacity 0.3s ease, transform 0.3s ease-out;
}

.img-actions-overlay.visible .action-btn {
  transform: translateY(0);
}

.action-btn.delete:hover {
  color: rgb(var(--v-theme-error)) !important;
}

/* Upload State UI */
.upload-icon-wrapper {
  width: 56px;
  height: 56px;
  background-color: rgba(var(--v-theme-primary), 0.08);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.custom-img-container:hover .upload-icon-wrapper {
  transform: translateY(-4px);
}

/* Shimmer State */
.shimmer-wrapper {
  width: 100%;
  height: 100%;
  background: #f6f7f8;
  overflow: hidden;
}

.shimmer-base {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.6) 50%,
    rgba(255, 255, 255, 0) 100%
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
</style>

<script>
export default {
  props: {
    title: { type: String },
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
  },
  data() {
    return {
      imageSrc: undefined,
      dialog: false,
      base_url: this.setting.url_img,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.$el.querySelector('input[type="file"]').click();
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
  // watch: {
  //   value() {

  //   },
  // },
};
</script>
