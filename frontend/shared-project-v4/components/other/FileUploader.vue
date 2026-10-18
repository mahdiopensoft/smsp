<template>
  <div
    class="glass-dropzone text-center d-flex flex-column justify-center align-center"
    :class="{
      'is-dragging': isDragging,
      'has-file': fileSelected,
      'theme-dark': isDark,
      'cursor-not-allowed': loading.uploading,
    }"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
    @click="triggerFileInput"
    :style="{ 'min-height': height, cursor: '' }"
  >
    <div>
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        hidden
        :multiple="!single"
        @change="handleFileSelect"
      />
      <template v-if="loading?.uploading">
        <v-progress-circular
          v-model="upload_progress"
          color="rgb(var(--v-theme-primary))"
          size="64"
          width="6"
          class="mb-4"
        >
          <span
            class="text-caption font-weight-bold g-text-high"
            style="font-size: 0.75rem"
            >{{ upload_progress }}%</span
          >
        </v-progress-circular>
        <!-- <v-progress-circular
          indeterminate
          color="rgb(var(--v-theme-primary))"
          size="48"
          width="4"
          class="mb-4"
        ></v-progress-circular> -->
        <h3 class="text-h6 font-weight-bold g-text-high mb-1">جاري الرفع...</h3>
        <!-- <p class="text-caption mb-0 g-text-med">يرجى الانتظار ثواني معدودة</p> -->
        <p class="text-caption mb-0 g-text-med" dir="ltr">
          {{ formatBytes(uploaded_bytes) }} /
          {{ formatBytes(total_upload_bytes) }}
        </p>
      </template>
      <template v-else-if="!fileSelected || !single">
        <v-icon size="48" :style="{ color: 'var(--g-icon-dim)' }" class="mb-4"
          >mdi-file-upload-outline</v-icon
        >
        <h3 class="text-h6 font-weight-bold g-text-high mb-1">
          انقر أو اسحب الملف هنا
        </h3>
        <p v-if="accept != '*/*'" class="text-caption mb-0 g-text-med">
          صيغة <span dir="ltr"> {{ accept?.toUpperCase() }}</span> مدعومة فقط
        </p>
        <p v-else class="text-caption mb-0 g-text-med">يرجى رفع الملف</p>
        <!-- <v-icon size="32" color="grey">mdi-cloud-upload</v-icon>
        <div class="text-body-2 mt-2">اضغط لاختيار الملفات او اسحبها هنا</div> -->
      </template>

      <template v-else-if="single && fileSelected">
        <v-icon
          size="48"
          :color="fileConfig(modelValue?.type)?.color"
          class="mb-4 text-glow-success"
          >{{ fileConfig(modelValue?.type)?.icon }}</v-icon
        >
        <h3
          class="text-h6 font-weight-bold g-text-high mb-1 text-truncate w-100 px-4"
        >
          {{ modelValue.name }}
        </h3>
        <p class="text-caption mb-4 g-text-med">
          {{ formatBytes(modelValue?.size) }}
        </p>
        <v-btn
          variant="text"
          color="error"
          size="small"
          @click.stop="removeAttachment()"
          >حذف الملف</v-btn
        >
      </template>
    </div>
  </div>
  <!-- Attachment List -->
  <div
    v-if="modelValue?.length && !single"
    class="d-flex flex-wrap mt-3 pt-1 overflow-auto"
    style="gap: 12px; max-height: 300px"
  >
    <v-lazy
      v-for="(file, index) in modelValue"
      :key="index"
      transition="fade-transition"
      class="flex-grow-1"
      :options="{ threshold: 0.5 }"
    >
      <v-card
        variant="outlined"
        class="pa-2 attachment-card border"
        :class="{ 'cursor-pointer': canEdit, 'cursor-default': !canEdit }"
        min-width="180"
        @click="canEdit ? editFileDetails(index) : null"
        v-ripple
      >
        <div class="d-flex align-center">
          <v-tooltip location="top" text="اضغط لفتح الملف" open-delay="500">
            <template #activator="{ props }">
              <v-icon
                v-bind="props"
                :color="fileConfig(file?.type)?.color"
                size="32"
                class="ml-2 file-icon-hover"
                @click.stop="openFile(file)"
              >
                {{ fileConfig(file?.type)?.icon }}</v-icon
              >
            </template>
          </v-tooltip>
          <div class="flex-grow-1" style="min-width: 0">
            <div class="d-flex align-center justify-space-between">
              <div width="">
                <div class="d-flex align-center text-truncate">
                  <div
                    class="font-weight-bold text-body-2 text-truncate"
                    style="max-width: 600px"
                    :title="file?.customName || file?.name"
                  >
                    {{ file?.customName || file?.name }}
                  </div>
                  <span class="text-caption text-grey ms-1"
                    >( {{ file?.size }} )</span
                  >
                  <v-icon v-if="canEdit" size="" class="ms-1 text-grey"
                    >mdi-pencil-outline</v-icon
                  >
                </div>
                <div
                  v-if="!file?.description"
                  class="text-caption mt-0 ps-1 text-grey-darken-1 text-wrap"
                  style="word-wrap: break-word"
                >
                  {{ file?.description }}
                </div>
              </div>
              <v-btn
                icon
                size="x-small"
                variant="text"
                density="comfortable"
                class="delete-btn"
                color="grey-lighten-1"
                @click.stop="removeAttachment(index)"
              >
                <v-icon size="small">mdi-close</v-icon>
                <v-tooltip activator="parent" location="top" open-delay="500"
                  >حذف الملف</v-tooltip
                >
              </v-btn>
            </div>
          </div>
        </div>
      </v-card>
    </v-lazy>
  </div>
  <!-- file details dialog -->
  <custom-dialog
    v-model="fileDialog.show"
    title="تعديل بيانات الملف"
    width="350"
    height="auto"
  >
    <template v-slot>
      <v-form ref="file_data">
        <v-container>
          <custom-text-field
            v-model="fileDialog.customName"
            icon=""
            label="اسم الملف"
            :rules="[$max_length(100)]"
          />
          <custom-text-note
            v-model="fileDialog.description"
            icon=""
            label="الوصف"
            :rules="[$max_length(250)]"
          />
          <div class="text-caption text-grey mt-1">
            الملف الاصلي: {{ fileDialog?.originalName }}
          </div>
        </v-container>
      </v-form>
    </template>
    <template #actions>
      <v-row class="pa-2">
        <v-spacer></v-spacer>
        <custom-btn
          type="cancel"
          size="small"
          density="default"
          variant="text"
          :click="() => (fileDialog.show = false)"
        ></custom-btn>
        <custom-btn
          type="save"
          class="ms-1"
          size="small"
          density="default"
          :click="saveFileDetails"
        ></custom-btn>
      </v-row>
    </template>
  </custom-dialog>
</template>
<script>
export default {
  name: "FileUploader",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    height: {
      type: [String, Number],
      default: "120px",
    },
    canEdit: {
      type: Boolean,
      default: true,
    },
    single: {
      type: Boolean,
      default: false,
    },
    accept: {
      type: String,
      default: "*/*",
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      upload_progress: 0,
      uploaded_bytes: 0,
      total_upload_bytes: 0,
      isDragging: false,
      loading: {
        uploading: false,
        importing: false,
      },
      fileDialog: {
        show: false,
        index: -1,
        customName: "",
        description: "",
        originalName: "",
        isNew: false,
        pendingFiles: [],
      },
    };
  },
  computed: {
    isDark() {
      return this.$vuetify.theme.current.dark;
    },
    fileSelected() {
      return !!this.modelValue?.length || !!this.modelValue?.name;
    },
  },
  methods: {
    // Attachment
    triggerFileInput() {
      if (!this.loading.uploading) {
        this.$refs?.fileInput.click();
      }
    },
    handleFileSelect(e) {
      this.processFiles(Array?.from(e.target?.files));
    },
    handleDrop(e) {
      if (!this.loading.uploading) {
        this.isDragging = false;
        this.processFiles(Array?.from(e.dataTransfer?.files));
      }
    },
    processFiles(files) {
      this.loading.uploading = true;
      if (files?.length === 0) return;
      var newFiles = [];
      for (const file of files) {
        if (!this.single) {
          newFiles?.push({
            fileObj: file,
            name: file?.name,
            customName: file?.name?.split(".")[0],
            description: "",
            type: file?.name?.split(".").pop().toLowerCase(),
            size: file?.size,
            // size: (file?.size / 1024 / 1024)?.toFixed(2) + "MB",
          });
          setTimeout(() => {
            this.loading.uploading = false;
            this.$emit("update:modelValue", [...this.modelValue, ...newFiles]);
          }, 300);
        } else {
          newFiles = {};
          newFiles = {
            fileObj: file,
            name: file?.name,
            customName: file?.name?.split(".")[0],
            description: "",
            type: file?.name?.split(".").pop().toLowerCase(),
            // size: (file?.size / 1024 / 1024)?.toFixed(2) + "MB",
            size: file?.size,
          };

          this.upload_progress = 0;
          this.total_upload_bytes = file?.size;
          // this.uploaded_bytes = 0;

          // //calculate duration dynamically based on file size (assumin ~5 MB/s mock speed)

          const simulated_by_bytes_per_ms = (50 * 1024 * 1024) / 1000;
          let duration = file?.size / simulated_by_bytes_per_ms;
          duration = Math.max(300, Math?.min(duration, 3000));

          // const duration = 2000;
          const start = performance.now();

          const animate = (now) => {
            const elapsed = now - start;
            const progress = Math?.min(elapsed / duration, 1);

            this.upload_progress = Math?.floor(progress * 100);
            this.uploaded_bytes = Math?.floor(file?.size * progress);
            if (progress < 1) {
              requestAnimationFrame(animate);
            } else {
              this.uploaded_bytes = file?.size;

              setTimeout(() => {
                this.loading.uploading = false;
                this.$emit("update:modelValue", { ...newFiles });
              }, 300);
            }
          };
          requestAnimationFrame(animate);

          // const interval = setInterval(() => {
          //   const chunk =
          //     Math.floor(Math?.random() * (file?.size * 0.15)) +
          //     file?.size * 0.05;
          //   this.uploaded_bytes += chunk;
          //   if (this.uploaded_bytes >= file?.size) {
          //     this.uploaded_bytes = file?.size;
          //     this.upload_progress = 100;

          //     clearInterval(interval);
          //     console.log("asdasdasdasd");
          //     setTimeout(() => {
          //       this.loading.uploading = false;
          //       this.$emit("update:modelValue", { ...newFiles });
          //     }, 300);
          //   } else {
          //     this.upload_progress = Math?.floor(
          //       (this.uploaded_bytes / file?.size) * 100
          //     );
          //     console.log(this.upload_progress, "asdasdasdasd");
          //   }
          // }, 500);

          // newFiles?.push({
          //   fileObj: file,
          //   name: file?.name,
          //   customName: file?.name?.split(".")[0],
          //   description: "",
          //   type: file?.name?.split(".").pop().toLowerCase(),
          //   size: (file?.size / 1024 / 1024)?.toFixed(2) + "MB",
          // });
        }
      }

      // this.$snack("add", { message: "تم اضافة الملفات" });

      if (this.$refs?.fileInput) {
        this.$refs.fileInput.value = "";
      }

      // this.fileDialog.pendingFiles = files;
      // this.processNextFiles();
    },
    // processNextFiles() {
    //   if (this.fileDialog?.pendingFiles?.length === 0) {
    //     if (this.$refs?.fileInput) {
    //       this.$refs.fileInput.value = "";
    //     }
    //     return;
    //   }
    //   const file = this.fileDialog?.pendingFiles[0];
    //   this.fileDialog.index = -1;
    //   this.fileDialog.originalName = file?.name;
    //   this.fileDialog.customName = file?.name?.split(".")[0];
    //   this.fileDialog.description = "";
    //   this.fileDialog.isNew = true;
    //   this.fileDialog.show = true;
    // },
    async saveFileDetails() {
      // if (this.fileDialog?.isNew) {
      //   const file = this.fileDialog?.pendingFiles?.shift();

      //   this.modelValue?.push({
      //     fileObj: file,
      //     name: file?.name,
      //     customName: this.fileDialog?.customName || file?.name,
      //     description: this.fileDialog?.description,
      //     type: file?.type?.includes("pdf")
      //       ? "pdf"
      //       : file?.type?.includes("image")
      //       ? "image"
      //       : "doc",
      //     size: (file?.size / 1024 / 1024)?.toFixed(2) + "MB",
      //   });

      //   this.fileDialog.show = false;
      //   setTimeout(() => {
      //     this.processNextFiles();
      //   }, 300);
      // } else {
      if (await this.$validate(this.$refs["file_data"])) {
        const newAttachments = [...this.modelValue];
        const attachment = { ...newAttachments[this.fileDialog?.index] };
        attachment.customName = this.fileDialog?.customName;
        attachment.description = this.fileDialog?.description;

        newAttachments[this.fileDialog?.index] = attachment;

        this.$emit("update:modelValue", newAttachments);

        this.fileDialog.show = false;
      }
      // }
    },

    editFileDetails(index) {
      const file = this.modelValue[index];
      this.fileDialog.index = index;
      this.fileDialog.originalName = file?.name;
      this.fileDialog.customName = file?.customName;
      this.fileDialog.description = file?.description;
      this.fileDialog.isNew = false;
      this.fileDialog.show = true;
    },
    addAttachment() {
      this.modelValue.push({
        name: "",
        file: null,
        description: "",
      });
    },

    removeAttachment(index) {
      let newAttachments = null;
      if (!this.single) {
        newAttachments = [...this.modelValue];
        newAttachments.splice(index, 1);
      } else {
        newAttachments = { ...this.modelValue };
        newAttachments = {};
      }
      this.$emit("update:modelValue", newAttachments);
    },

    fileConfig(ext) {
      if (ext) {
        const iconMap = {
          pdf: "mdi-file-pdf-box",
          doc: "mdi-file-word-box",
          docx: "mdi-file-word-box",
          xls: "mdi-file-excel-box",
          xlsx: "mdi-file-excel-box",
          jpg: "mdi-file-image",
          jpeg: "mdi-file-image",
          png: "mdi-file-image",
          zip: "mdi-zip-box",
          rar: "mdi-zip-box",
        };
        const colorMap = {
          pdf: "#E53935",
          doc: "#1e88e5",
          docx: "#1e88e5",
          xls: "#43A047",
          xlsx: "#43A047",
          jpg: "#FB8C00",
          jpeg: "#FB8C00",
          png: "#FB8C00",
          zip: "#6D4C41",
          rar: "#6D4C41",
        };
        return {
          icon: iconMap[ext] || "mdi-file-document-outline",
          color: colorMap[ext] || "grey",
        };
      }
    },
    // getFileIcon(t) {
    //   const icons = {
    //     pdf: "mdi-file-pdf-box",
    //     doc: "mdi-file-word",
    //     image: "mdi-file-image",
    //   };
    //   return icons[t] || "mdi-file";
    // },

    // getFileColor(t) {
    //   const icons = {
    //     pdf: "red",
    //     doc: "blue",
    //     image: "green",
    //   };
    //   return icons[t] || "grey";
    // },
    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0 Bytes";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    },
    openFile(file) {
      if (file?.fileObj) {
        const url = URL.createObjectURL(file?.fileObj);
        window.open(url, "_blank");
      } else {
        this.$alert("error", { message: "لا يمكن فتح الملف" });
      }
    },
    // EndAttachment
  },
};
</script>

<style scoped>
/* Dialog Scoped Variables */
.glass-dropzone {
  --g-dropzone-bg: rgba(255, 255, 255, 0.3);
  --g-dropzone-border: rgba(0, 0, 0, 0.2);
  --g-dropzone-hover: rgba(255, 255, 255, 0.6);
}

.theme-dark.glass-dropzone {
  /* Slightly more opaque for dialogs in dark mode */

  --g-dropzone-bg: rgba(0, 0, 0, 0.2);
  --g-dropzone-border: rgba(255, 255, 255, 0.2);
  --g-dropzone-hover: rgba(0, 0, 0, 0.4);
}

.upload-area:hover {
  border-color: #1976d2;
  background: #e3f2fd;
}

.attachment-card {
  /* border-color: #e0e0e0;
  background: #fff; */
  /* transition: all 0.2s ease; */
  background: var(--g-dropzone-bg);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
/* .attachment-card:not(:focus) {
  border-color: #e0e0e0;
  background: #fff;
} */
.attachment-card:hover {
  /* border-color: #1976d2; */
  /* background-color: #f5f9ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5); */
  /* background-color: #f0f7ff; */
  transform: translateY(-2px);
  border-color: rgba(var(--v-theme-primary), 0.5) !important;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
}
.file-icon-hover {
  transition: transform 0.2s;
  cursor: pointer;
}
.file-icon-hover:hover {
  transform: scale(1.15);
}
.delete-btn {
  opacity: 0;
  transition: all 0.2s;
}
.delete-btn:hover {
  color: red !important;
  transform: scale(1.15);
}
.attachment-card:hover .delete-btn {
  opacity: 1;
}

.glass-dropzone {
  background: var(--g-dropzone-bg);
  border: 2px dashed var(--g-dropzone-border);
  border-radius: 24px;
  padding: 48px 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.glass-dropzone:hover,
.glass-dropzone.is-dragging {
  background: var(--g-dropzone-hover);
  border-color: rgba(var(--v-theme-primary), 0.5);
}

.glass-dropzone.has-file {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgba(var(--v-theme-primary), 0.5);
  /* border: 2px solid rgba(16, 185, 129, 0.8);
  background: rgba(16, 185, 129, 0.05); */
}
.theme-dark.glass-dropzone.has-file {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgba(var(--v-theme-primary), 0.5);
  /* border-color: rgba(16, 185, 129, 0.5);
  background: rgba(16, 185, 129, 0.1); */
}
</style>
