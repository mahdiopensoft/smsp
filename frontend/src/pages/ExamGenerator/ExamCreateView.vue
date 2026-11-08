<template>
  <div class="qb-exam-create-v4 position-relative">

    <!-- Top Subtle Linear Progress during Edit Loading -->
    <v-progress-linear
      v-if="isLoadingForEdit"
      indeterminate
      color="primary"
      height="3"
      rounded
      class="mb-3"
    />

    <!-- Lightweight Formal Transparent Overlay -->
    <v-fade-transition>
      <div v-if="isLoadingForEdit" class="formal-loading-overlay">
        <div class="formal-loading-pill d-flex align-center gap-3 pa-3 px-5 rounded-pill elevation-3">
          <v-progress-circular
            indeterminate
            color="primary"
            size="22"
            width="2.5"
          />
          <span class="text-caption font-weight-bold text-high-emphasis">
            جاري استرجاع بيانات الاختبار...
          </span>
        </div>
      </div>
    </v-fade-transition>

    <!-- Active Editing Draft Mode Banner (Zero Gray executive design) -->
    <div
      v-if="isEditing && !isLoadingForEdit"
      class="editing-mode-banner mb-6 pa-4 rounded-2xl d-flex align-center justify-space-between flex-wrap gap-3"
    >
      <div class="d-flex align-center gap-3">
        <v-avatar color="warning" size="44" class="font-weight-black text-white shadow-sm">
          <v-icon color="white" size="24">mdi-pencil-box-multiple</v-icon>
        </v-avatar>
        <div>
          <div class="d-flex align-center gap-2 flex-wrap">
            <h3 class="text-subtitle-1 font-weight-black mb-0 text-warning">
              تعديل مسودة الاختبار: {{ exam.title || editingExamCode }}
            </h3>
            <v-chip size="x-small" color="warning" variant="flat" class="font-weight-black text-white">
              مسودة غير معتمدة
            </v-chip>
            <span class="text-caption font-mono font-weight-bold opacity-80">({{ editingExamCode }})</span>
          </div>
          <p class="text-caption font-weight-medium text-medium-emphasis mb-0">
            أنت الآن تقوم بتعديل معايير وتوزيعات الاختبار الحالية. يمكنك تعديل أي خطوة وإعادة توليد وتحديث الاختبار.
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <v-btn
          variant="tonal"
          color="warning"
          size="small"
          class="font-weight-bold rounded-xl text-none"
          prepend-icon="mdi-plus"
          @click="exitEditMode"
        >
          إنشاء اختبار جديد بدلاً من التعديل
        </v-btn>
      </div>
    </div>

    <!-- Main Stepper Wizard Window Content -->
    <div
      class="main-card rounded-2xl mb-8"
      :class="{ 'content-loading-blur': isLoadingForEdit }"
    >

      <!-- Premium Connected Wizard Stepper Pipeline (دوائر تفاعلية مع خطوط توصيل وحالات نجاح/فشل صريحة) -->
      <div class="premium-wizard-wrapper">
        <div class="premium-wizard-container">
          <!-- Connecting Progress Line with RTL support -->
          <div class="wizard-progress-track">
            <div
              class="wizard-progress-fill"
              :style="{ width: wizardProgressPercentage + '%' }"
            >
              <span class="wizard-beam-glow"></span>
            </div>
          </div>

          <!-- Step Nodes -->
          <div
            v-for="s in wizardSteps"
            :key="s.value"
            class="premium-wizard-node"
            :class="getStepNodeClasses(s.value)"
            @click="handleStepClick(s.value)"
          >
            <!-- Circular Node Anchor -->
            <div class="stepper-circle-anchor">
              <!-- Number badge on top-right corner -->
              <span class="node-step-number">{{ s.value }}</span>

              <!-- Active pulsing wave ring for active or warning steps -->
              <span
                v-if="getStepStatus(s.value).type === 'active'"
                class="stepper-pulse-ring pulse-primary"
              ></span>
              <span
                v-else-if="getStepStatus(s.value).type === 'error'"
                class="stepper-pulse-ring pulse-error"
              ></span>

              <div class="stepper-circle">
                <!-- If Completed/Success: Show Animated Checkmark -->
                <v-icon
                  v-if="getStepStatus(s.value).type === 'completed'"
                  size="22"
                  class="checkmark-pop"
                >
                  mdi-check-bold
                </v-icon>

                <!-- If Error/Failure: Show Alert Icon -->
                <v-icon
                  v-else-if="getStepStatus(s.value).type === 'error'"
                  size="22"
                  class="error-icon-shake"
                >
                  mdi-alert-circle
                </v-icon>

                <!-- Otherwise (Active / Pending): Show Step Custom Icon -->
                <v-icon
                  v-else
                  size="20"
                  :class="{ 'icon-active-breath': getStepStatus(s.value).type === 'active' }"
                >
                  {{ s.icon }}
                </v-icon>
              </div>
            </div>

            <!-- Step Titles & Explicit Status Pill -->
            <div class="node-content text-center mt-2">
              <span class="node-title font-weight-black">{{ s.title }}</span>
              <span v-if="s.subtitle" class="node-subtitle text-caption text-medium-emphasis d-none d-lg-block">
                {{ s.subtitle }}
              </span>

              <!-- Explicit Status Indicator (نجاح / فشل / قيد الضبط / انتظار) -->
              <div class="node-status-badge-wrapper mt-1">
                <span
                  class="node-status-pill font-weight-bold"
                  :class="`status-${getStepStatus(s.value).type}`"
                >
                  <v-icon size="11" class="me-1">
                    {{ getStepStatus(s.value).statusIcon }}
                  </v-icon>
                  {{ getStepStatus(s.value).text }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="pa-6">
        <v-window v-model="step" class="bg-transparent">
          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- STEP 1: SETTINGS (GROUPED SECTIONS)                             -->
          <!-- ════════════════════════════════════════════════════════════════ -->
          <v-window-item :value="1">
            <v-form ref="step1Form">
              <!-- Master-Detail Layout for Step 1 -->
              <v-row class="step1-master-detail-row">
                <!-- ════════════════════════════════════════════════════════════ -->
                <!-- RIGHT COLUMN: SECTIONS SIDEBAR MENU (قائمة اليمين)            -->
                <!-- ════════════════════════════════════════════════════════════ -->
                <v-col cols="12" md="4" lg="3.5">
                  <div class="step1-sidebar-card pa-4 rounded-2xl border-subtle">
                    <div class="sidebar-header mb-3 pb-3 border-b-subtle d-flex align-center justify-space-between">
                      <h4 class="text-subtitle-1 font-weight-black mb-0 d-flex align-center gap-2">
                        <v-icon size="20" :color="validatedOnce && invalidSectionsCount > 0 ? 'error' : 'primary'">mdi-format-list-bulleted-square</v-icon>
                        أقسام إعداد الاختبار
                      </h4>
                      <v-chip
                        v-if="validatedOnce && invalidSectionsCount > 0"
                        size="x-small"
                        color="error"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        {{ invalidSectionsCount }} غير مكتمل
                      </v-chip>
                      <v-chip
                        v-else
                        size="x-small"
                        color="primary"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        {{ activeStep1Section }} / 3
                      </v-chip>
                    </div>

                    <!-- Navigation Items List -->
                    <div class="step1-nav-list d-flex flex-column gap-2">
                      <div
                        v-for="item in step1NavItems"
                        :key="item.id"
                        class="step1-nav-item pa-3 rounded-xl cursor-pointer"
                        :class="{
                          'is-active': activeStep1Section === item.id,
                          'has-error': validatedOnce && !isSectionValid(item.id)
                        }"
                        @click="activeStep1Section = item.id"
                      >
                        <div class="d-flex align-center gap-3">
                          <v-avatar
                            size="36"
                            :color="validatedOnce && !isSectionValid(item.id) ? 'error' : (activeStep1Section === item.id ? item.color : 'surface-variant')"
                            :variant="activeStep1Section === item.id || (validatedOnce && !isSectionValid(item.id)) ? 'flat' : 'tonal'"
                            class="rounded-lg flex-shrink-0"
                          >
                            <v-icon size="18" :color="activeStep1Section === item.id || (validatedOnce && !isSectionValid(item.id)) ? 'white' : 'medium-emphasis'">
                              {{ validatedOnce && !isSectionValid(item.id) ? 'mdi-alert-circle' : item.icon }}
                            </v-icon>
                          </v-avatar>

                          <div class="flex-grow-1 min-w-0">
                            <div class="d-flex align-center justify-space-between gap-1">
                              <span
                                class="text-subtitle-2 font-weight-bold text-truncate d-block"
                                :class="{
                                  'text-error': validatedOnce && !isSectionValid(item.id),
                                  'text-primary': activeStep1Section === item.id && (!validatedOnce || isSectionValid(item.id))
                                }"
                              >
                                {{ item.title }}
                              </span>
                              <v-chip
                                v-if="validatedOnce && !isSectionValid(item.id)"
                                size="x-small"
                                color="error"
                                variant="tonal"
                                class="font-weight-black flex-shrink-0"
                              >
                                مطلوب
                              </v-chip>
                            </div>
                            <span class="text-caption text-medium-emphasis text-truncate d-block">
                              {{ item.desc }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-col>

                <!-- ════════════════════════════════════════════════════════════ -->
                <!-- LEFT COLUMN: ACTIVE SECTION CONTENT (المحتوى يظهر في القائمة اليسرى)-->
                <!-- ════════════════════════════════════════════════════════════ -->
                <v-col cols="12" md="8" lg="8.5">
                  <!-- Section Validation Alert Banner -->
                  <v-alert
                    v-if="validatedOnce && invalidSectionsCount > 0"
                    type="error"
                    variant="tonal"
                    density="comfortable"
                    class="rounded-xl mb-4"
                    closable
                  >
                    <div class="d-flex align-center gap-2">
                      <v-icon size="20">mdi-alert-circle-outline</v-icon>
                      <span class="font-weight-bold text-body-2">
                        توجد حقول إجبارية غير مكتملة في الأقسام المحددة باللون الأحمر ({{ invalidSectionsCount }} من 3 بحاجة للاستكمال).
                      </span>
                    </div>
                  </v-alert>
                  <!-- Section 1: Academic Classification Scope -->
                  <div v-show="activeStep1Section === 1" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-4">
                      <v-avatar size="40" color="primary" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-school-outline</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">1. النطاق والتصنيف الأكاديمي</h4>
                        <span class="text-caption text-medium-emphasis">تحديد الفترة، القسم، الصف، والمادة أو المقرر المستهدف</span>
                      </div>
                    </div>

                    <!-- Modern Segmented Tabs for Institution Type -->
                    <div class="mb-5">
                      <div class="segmented-control rounded-xl pa-1 border-subtle d-flex flex-wrap gap-1">
                        <button type="button" class="segmented-control-btn" :class="{ 'is-active': exam.institution_type === 'school' }"
                          @click="exam.institution_type = 'school'; onInstitutionTypeToggle()">
                          <v-icon start size="18">mdi-school</v-icon>
                          <span>التعليم العام والمدرسي</span>
                        </button>
                        <button type="button" class="segmented-control-btn" :class="{ 'is-active': exam.institution_type === 'university' }"
                          @click="exam.institution_type = 'university'; onInstitutionTypeToggle()">
                          <v-icon start size="18">mdi-domain</v-icon>
                          <span>التعليم الجامعي والأكاديمي</span>
                        </button>
                        <button type="button" class="segmented-control-btn" :class="{ 'is-active': exam.institution_type === 'institute' }"
                          @click="exam.institution_type = 'institute'; onInstitutionTypeToggle()">
                          <v-icon start size="18">mdi-tools</v-icon>
                          <span>التعليم الفني والمهني</span>
                        </button>
                      </div>
                    </div>

                    <v-row dense>
                      <auto-list v-model="exam.yearId" name="AcademicYear" label="السنة الدراسية" placeholder="اختر السنة الدراسية" cols="3" :add="false"
                        :rules="requiredRule" />
                      <auto-list v-model="exam.examPeriodId" name="Period" label="الفترة الامتحانية" placeholder="اختر الفترة الامتحانية" cols="3" :add="false"
                        :rules="requiredRule" />

                      <!-- 🏫 School Classification Fields -->
                      <template v-if="exam.institution_type === 'school'">
                        <auto-list v-model="exam.stageId" name="Stage" placeholder="اختر المرحلة الدراسية" cols="3" :add="false"
                          :rules="requiredRule" @update:model-value="() => { if (!isLoadingForEdit) { exam.classTrackId = null; exam.subjectId = null; } }" />
                        <auto-list v-model="exam.classTrackId" name="ClassTrackByStage" :param="exam.stageId" placeholder="اختر الصف والمسار"
                          cols="3" :add="false" :rules="requiredRule" :disabled="!exam.stageId" @update:model-value="() => { if (!isLoadingForEdit) { exam.subjectId = null; } }" />
                        <auto-list v-model="exam.subjectId" name="Subject" :param="exam.classTrackId || exam.stageId" placeholder="اختر المادة الدراسية" cols="3" :add="false"
                          :rules="requiredRule" :disabled="!exam.classTrackId && !exam.stageId" />
                      </template>

                      <!-- 🎓 University Classification Fields -->
                      <template v-else-if="exam.institution_type === 'university'">
                        <auto-list v-model="exam.collegeId" name="College" placeholder="اختر الكلية" cols="3" :add="false"
                          :rules="requiredRule" @update:model-value="() => { if (!isLoadingForEdit) { exam.departmentId = null; exam.specializationId = null; exam.semesterSubjectId = null; } }" />
                        <auto-list v-model="exam.departmentId" name="UniversitySection" :param="exam.collegeId" placeholder="اختر القسم الأكاديمي"
                          cols="3" :add="false" :rules="requiredRule" :disabled="!exam.collegeId"
                          @update:model-value="() => { if (!isLoadingForEdit) { exam.specializationId = null; exam.semesterSubjectId = null; } }" />
                        <auto-list v-model="exam.specializationId" name="Specialization" :param="exam.departmentId" placeholder="اختر التخصص الدراسي"
                          cols="3" :add="false" :rules="requiredRule" :disabled="!exam.departmentId"
                          @update:model-value="() => { if (!isLoadingForEdit) { exam.semesterSubjectId = null; } }" />
                        <auto-list v-model="exam.semesterSubjectId" name="SemesterSubjectBySpec" :param="exam.specializationId"
                          placeholder="اختر المقرر الدراسي" cols="3" :add="false" :rules="requiredRule"
                          :disabled="!exam.specializationId" />
                      </template>

                      <!-- 🏢 Institute & Vocational Training Classification Fields -->
                      <template v-else-if="exam.institution_type === 'institute'">
                        <auto-list v-model="exam.instituteFieldId" name="InstituteField" placeholder="اختر المجال المهني" cols="3" :add="false"
                          :rules="requiredRule"
                          @update:model-value="() => { if (!isLoadingForEdit) { exam.instituteSpecializationId = null; exam.instituteCurriculumId = null; exam.instituteSubjectId = null; } }" />
                        <auto-list v-model="exam.instituteEducationSystemId" name="InstituteEducationSystem" placeholder="اختر النظام التعليمي"
                          cols="3" :add="false" :rules="requiredRule"
                          @update:model-value="() => { if (!isLoadingForEdit) { exam.instituteSpecializationId = null; exam.instituteCurriculumId = null; exam.instituteSubjectId = null; } }" />
                        <auto-list
                          v-model="exam.instituteSpecializationId"
                          name="InstituteSpecialization"
                          :param="{ field: exam.instituteFieldId, education_system: exam.instituteEducationSystemId }"
                          placeholder="اختر التخصص المهني"
                          cols="3"
                          :add="false"
                          :rules="requiredRule"
                          :disabled="!exam.instituteFieldId || !exam.instituteEducationSystemId"
                          @update:model-value="() => { if (!isLoadingForEdit) { exam.instituteCurriculumId = null; exam.instituteSubjectId = null; } }"
                        />
                        <auto-list
                          v-model="exam.instituteCurriculumId"
                          name="InstituteCurriculum"
                          :param="{ specialization: exam.instituteSpecializationId }"
                          placeholder="اختر الخطة الدراسية / المنهج"
                          cols="3"
                          :add="false"
                          :rules="requiredRule"
                          :disabled="!exam.instituteSpecializationId"
                          @update:model-value="() => { if (!isLoadingForEdit) { exam.instituteSubjectId = null; } }"
                        />
                        <auto-list
                          v-model="exam.instituteSubjectId"
                          name="InstituteSubject"
                          :param="{ curriculum: exam.instituteCurriculumId }"
                          placeholder="اختر المادة التدريبية"
                          cols="3"
                          :add="false"
                          :rules="requiredRule"
                          :disabled="!exam.instituteCurriculumId"
                        />
                      </template>
                    </v-row>
                  </div>

                  <!-- Section 2: Technical Details & Capacity -->
                  <div v-show="activeStep1Section === 2" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-5">
                      <v-avatar size="40" color="info" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-card-account-details-outline</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">2. تفاصيل وسعة ورقة الاختبار</h4>
                        <span class="text-caption text-medium-emphasis">تحديد عنوان ورقة الاختبار، رصيد الأسئلة، وإعدادات مكافحة التكرار</span>
                      </div>
                    </div>

                    <v-row dense class="mb-3">
                      <custom-text-field v-model="exam.title" cols="12" label="عنوان الاختبار الرسمي" icon="text"
                        :rules="[rules.required]" />

                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model.number="exam.questionsCount"
                          type="number"
                          label="عدد الأسئلة المطلوبة *"
                          variant="outlined"
                          density="compact"
                          rounded="lg"
                          hide-details="auto"
                          :min="5"
                          :max="100"
                          :rules="[v => (!!v && Number(v) >= 5 && Number(v) <= 100) || 'مطلوب (بين 5 و 100 سؤال)']"
                          prepend-inner-icon="mdi-counter"
                        />
                      </v-col>
                    </v-row>

                    <!-- Security Feature -->
                    <div class="pt-3 d-flex align-center justify-space-between flex-wrap gap-3">
                      <div class="d-flex align-center gap-3">
                        <v-avatar size="36" color="warning" variant="tonal" class="rounded-lg">
                          <v-icon size="20">mdi-shield-lock-outline</v-icon>
                        </v-avatar>
                        <div>
                          <div class="font-weight-bold text-subtitle-2">استبعاد الأسئلة المستخدمة سابقاً</div>
                          <div class="text-caption text-medium-emphasis">عدم إدراج الأسئلة التي تم استخدامها في اختبارات سابقة لنفس المقرر</div>
                        </div>
                      </div>
                      <v-switch v-model="exam.exclude_previously_used" color="warning" hide-details density="compact"
                        :label="exam.exclude_previously_used ? 'مفعّل' : 'معطّل'" class="font-weight-bold ma-0" />
                    </div>
                  </div>

                  <!-- Section 3: Advanced Models Configuration -->
                  <div v-show="activeStep1Section === 3" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-5">
                      <v-avatar size="40" color="warning" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-file-multiple-outline</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">3. إعدادات النماذج التوليدية والتوزيع المناطقي</h4>
                        <span class="text-caption text-medium-emphasis">اختر نمط توليد النماذج: متطابقة وموحدة، أو متقدمة بمستويات صعوبة وتوزيع جغرافي</span>
                      </div>
                    </div>

                    <!-- Mode Comparison Cards Side-by-Side (متقابلة وواضحة) -->
                    <v-row dense class="mb-4">
                      <!-- Card 1: Uniform -->
                      <v-col cols="12" md="6">
                        <div
                          class="selection-card model-mode-card h-100 pa-4 rounded-xl cursor-pointer"
                          :class="{ 'is-active': modelsMode === 'uniform' }"
                          @click="setModelsMode('uniform')"
                        >
                          <div class="d-flex align-start gap-3">
                            <v-avatar size="40" :color="modelsMode === 'uniform' ? 'primary' : 'surface-variant'" :variant="modelsMode === 'uniform' ? 'flat' : 'tonal'" class="rounded-lg flex-shrink-0">
                              <v-icon size="20" :color="modelsMode === 'uniform' ? 'white' : 'medium-emphasis'">mdi-checkbox-multiple-marked-outline</v-icon>
                            </v-avatar>
                            <div class="flex-grow-1">
                              <div class="d-flex align-center justify-space-between mb-1">
                                <span class="font-weight-black text-subtitle-1">النمط الموحد (القياسي)</span>
                                <v-icon :color="modelsMode === 'uniform' ? 'primary' : 'medium-emphasis'" size="20">
                                  {{ modelsMode === 'uniform' ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                                </v-icon>
                              </div>
                              <p class="text-caption text-medium-emphasis mb-0 leading-relaxed">
                                توليد نماذج بنفس بنك الأسئلة المعتمد مع خلط وترتيب الأسئلة والخيارات آلياً لكل نموذج.
                              </p>
                            </div>
                          </div>
                        </div>
                      </v-col>

                      <!-- Card 2: Advanced -->
                      <v-col cols="12" md="6">
                        <div
                          class="selection-card model-mode-card h-100 pa-4 rounded-xl cursor-pointer"
                          :class="{ 'is-active is-active-warning': modelsMode === 'advanced' }"
                          @click="setModelsMode('advanced')"
                        >
                          <div class="d-flex align-start gap-3">
                            <v-avatar size="40" :color="modelsMode === 'advanced' ? 'warning' : 'surface-variant'" :variant="modelsMode === 'advanced' ? 'flat' : 'tonal'" class="rounded-lg flex-shrink-0">
                              <v-icon size="20" :color="modelsMode === 'advanced' ? 'white' : 'medium-emphasis'">mdi-layers-triple-outline</v-icon>
                            </v-avatar>
                            <div class="flex-grow-1">
                              <div class="d-flex align-center justify-space-between mb-1">
                                <span class="font-weight-black text-subtitle-1">النمط المتقدم والمناطقي</span>
                                <v-icon :color="modelsMode === 'advanced' ? 'warning' : 'medium-emphasis'" size="20">
                                  {{ modelsMode === 'advanced' ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                                </v-icon>
                              </div>
                              <p class="text-caption text-medium-emphasis mb-0 leading-relaxed">
                                توليد مجموعات نماذج متمايزة بنسب صعوبة متفاوتة، مع إمكانية ربطها بمناطق جغرافية محددة.
                              </p>
                            </div>
                          </div>
                        </div>
                      </v-col>
                    </v-row>

                    <!-- Uniform Mode: Models Count Configuration -->
                    <v-expand-transition>
                      <div v-if="modelsMode === 'uniform'" class="pt-2 mb-4">
                        <div class="d-flex align-center gap-3 mb-3">
                          <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
                            <v-icon size="20">mdi-file-multiple</v-icon>
                          </v-avatar>
                          <div>
                            <span class="font-weight-bold text-subtitle-2">تحديد عدد النماذج المتطابقة للاختبار</span>
                            <div class="text-caption text-medium-emphasis">سيتم توليد عدد النماذج المحددة بنفس بنك الأسئلة المعتمد وترتيب مختلف للأسئلة والخيارات (نموذج A, B, C...)</div>
                          </div>
                        </div>

                        <v-row dense class="align-center">
                          <v-col cols="12" md="6">
                            <v-text-field
                              v-model.number="exam.modelsCount"
                              type="number"
                              label="عدد النماذج المنسخة *"
                              variant="outlined"
                              density="compact"
                              rounded="lg"
                              hide-details="auto"
                              :min="1"
                              :max="10"
                              :rules="modelsMode === 'uniform' ? [v => (!!v && Number(v) >= 1 && Number(v) <= 10) || 'مطلوب (بين 1 و 10 نماذج)'] : []"
                              prepend-inner-icon="mdi-file-multiple"
                            />
                          </v-col>
                          <v-col cols="12" md="6" class="d-flex align-center gap-1.5 flex-wrap pt-md-2">
                            <span class="text-caption font-weight-bold text-medium-emphasis me-1">اختيار سريع:</span>
                            <v-btn
                              v-for="mCount in [1, 2, 3, 4]"
                              :key="mCount"
                              size="small"
                              rounded="pill"
                              :color="exam.modelsCount === mCount ? 'primary' : undefined"
                              :variant="exam.modelsCount === mCount ? 'flat' : 'tonal'"
                              class="font-weight-bold px-2.5"
                              @click="setModelsCount(mCount)"
                            >
                              {{ mCount }} {{ mCount === 1 ? 'نموذج' : mCount === 2 ? 'نموذجان' : 'نماذج' }}
                            </v-btn>
                          </v-col>
                        </v-row>
                      </div>
                    </v-expand-transition>

                    <v-expand-transition>
                      <div v-if="modelsMode === 'advanced'">
                        <!-- Model Groups Cards with Distinct Borders & Visual Separation -->
                        <template v-for="(group, gIdx) in modelGroups" :key="gIdx">
                          <div class="pa-5 pa-md-6 rounded-2xl model-group-card">
                            <!-- Distinctive Group Header Banner -->
                            <div class="model-group-header-banner d-flex align-center justify-space-between mb-5 pa-3.5 px-4 rounded-xl flex-wrap gap-3">
                              <div class="d-flex align-center gap-3 flex-wrap">
                                <div class="d-flex align-center gap-2.5">
                                  <v-avatar
                                    size="38"
                                    color="primary"
                                    variant="flat"
                                    class="rounded-xl font-weight-black text-subtitle-2 text-white shadow-sm"
                                  >
                                    {{ gIdx + 1 }}
                                  </v-avatar>
                                  <div>
                                    <div class="d-flex align-center gap-2">
                                      <span class="font-weight-black text-subtitle-1 text-high-emphasis">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</span>
                                      <v-chip size="small" color="primary" variant="flat" class="font-weight-black">
                                        {{ group.count }} {{ group.count === 1 ? 'نموذج' : group.count === 2 ? 'نموذجان' : 'نماذج' }}
                                      </v-chip>
                                    </div>
                                    <span class="text-caption text-medium-emphasis">إعدادات النماذج والخصائص المخصصة لهذه المجموعة</span>
                                  </div>
                                </div>
                              </div>

                              <div class="d-flex align-center gap-2 flex-wrap">
                                <v-chip size="small" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="font-weight-bold">
                                  <v-icon start size="14">mdi-speedometer</v-icon>
                                  {{ difficultyLabel(group.difficulty_profile) }}
                                </v-chip>
                                <v-chip
                                  size="small"
                                  :color="(group.questions_variation || 'same_scrambled') === 'different_questions' ? 'secondary' : 'primary'"
                                  variant="tonal"
                                  class="font-weight-bold"
                                >
                                  <v-icon start size="14">
                                    {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'mdi-layers-triple' : 'mdi-shuffle-variant' }}
                                  </v-icon>
                                  {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'أسئلة مستقلة' : 'خلط وترتيب' }}
                                </v-chip>
                                <v-btn
                                  v-if="modelGroups.length > 1"
                                  variant="tonal"
                                  size="small"
                                  color="error"
                                  class="rounded-lg font-weight-bold px-3 ms-md-2"
                                  prepend-icon="mdi-trash-can-outline"
                                  @click="removeModelGroup(gIdx)"
                                >
                                  حذف المجموعة
                                </v-btn>
                              </div>
                            </div>

                          <v-row dense class="mb-4">
                            <v-col cols="12" md="4">
                              <v-text-field
                                v-model="group.name"
                                label="اسم / مسمى المجموعة"
                                :placeholder="'المجموعة ' + (gIdx + 1)"
                                variant="outlined"
                                density="compact"
                                rounded="lg"
                                hide-details="auto"
                                prepend-inner-icon="mdi-tag-outline"
                              />
                            </v-col>
                            <v-col cols="12" md="4">
                              <v-text-field
                                v-model.number="group.count"
                                type="number"
                                label="عدد النماذج في هذه المجموعة *"
                                variant="outlined"
                                density="compact"
                                rounded="lg"
                                hide-details="auto"
                                :min="1"
                                :max="10"
                                :rules="[v => (!!v && Number(v) >= 1 && Number(v) <= 10) || 'مطلوب (1-10 نماذج)']"
                                prepend-inner-icon="mdi-file-multiple"
                              />
                            </v-col>
                            <v-col cols="12" md="4">
                              <v-select
                                v-model="group.difficulty_profile"
                                :items="difficultyProfiles"
                                item-title="label"
                                item-value="value"
                                label="ملف الصعوبة المعتمد"
                                variant="outlined"
                                density="compact"
                                rounded="lg"
                                hide-details
                                @update:model-value="applyDifficultyPreset(group)"
                              />
                            </v-col>
                          </v-row>

                          <!-- Question Variation Mode for this Group -->
                          <div class="pa-4 rounded-xl mb-4 group-inner-section group-variation-container">
                            <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                              <span class="text-caption font-weight-black text-primary d-flex align-center">
                                <v-icon size="16" color="primary" class="me-1">mdi-swap-horizontal-bold</v-icon>
                                تنوع الأسئلة داخل نماذج {{ group.name || ('المجموعة ' + (gIdx + 1)) }}:
                              </span>
                              <v-chip
                                size="x-small"
                                :color="(group.questions_variation || 'same_scrambled') === 'different_questions' ? 'secondary' : 'primary'"
                                variant="tonal"
                                class="font-weight-bold"
                              >
                                {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'أسئلة مستقلة لكل نموذج' : 'نفس الأسئلة (خلط وترتيب)' }}
                              </v-chip>
                            </div>

                            <v-row dense>
                              <v-col cols="12" sm="6">
                                <div
                                  class="selection-card h-100 pa-3 rounded-lg cursor-pointer transition-swing"
                                  :class="{ 'is-active': (group.questions_variation || 'same_scrambled') === 'same_scrambled' }"
                                  @click="group.questions_variation = 'same_scrambled'"
                                >
                                  <div class="d-flex align-start gap-2.5">
                                    <v-avatar
                                      size="32"
                                      :color="(group.questions_variation || 'same_scrambled') === 'same_scrambled' ? 'primary' : 'surface-variant'"
                                      :variant="(group.questions_variation || 'same_scrambled') === 'same_scrambled' ? 'flat' : 'tonal'"
                                      class="rounded-lg flex-shrink-0"
                                    >
                                      <v-icon size="18" :color="(group.questions_variation || 'same_scrambled') === 'same_scrambled' ? 'white' : 'medium-emphasis'">
                                        mdi-shuffle-variant
                                      </v-icon>
                                    </v-avatar>
                                    <div class="flex-grow-1">
                                      <div class="d-flex align-center justify-space-between mb-1">
                                        <span class="font-weight-bold text-caption text-high-emphasis">نفس الأسئلة والخيارات بترتيب مختلف</span>
                                        <v-icon
                                          :color="(group.questions_variation || 'same_scrambled') === 'same_scrambled' ? 'primary' : 'medium-emphasis'"
                                          size="16"
                                        >
                                          {{ (group.questions_variation || 'same_scrambled') === 'same_scrambled' ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                                        </v-icon>
                                      </div>
                                      <p class="text-caption text-medium-emphasis mb-0" style="font-size: 11px !important; line-height: 1.4;">
                                        نماذج المجموعة تتشارك نفس حزمة الأسئلة مع إعادة ترتيب مواقع الأسئلة وخيارات الإجابة منعاً للغش.
                                      </p>
                                    </div>
                                  </div>
                                </div>
                              </v-col>

                              <v-col cols="12" sm="6">
                                <div
                                  class="selection-card h-100 pa-3 rounded-lg cursor-pointer transition-swing"
                                  :class="{ 'is-active': group.questions_variation === 'different_questions' }"
                                  @click="group.questions_variation = 'different_questions'"
                                >
                                  <div class="d-flex align-start gap-2.5">
                                    <v-avatar
                                      size="32"
                                      :color="group.questions_variation === 'different_questions' ? 'secondary' : 'surface-variant'"
                                      :variant="group.questions_variation === 'different_questions' ? 'flat' : 'tonal'"
                                      class="rounded-lg flex-shrink-0"
                                    >
                                      <v-icon size="18" :color="group.questions_variation === 'different_questions' ? 'white' : 'medium-emphasis'">
                                        mdi-layers-triple
                                      </v-icon>
                                    </v-avatar>
                                    <div class="flex-grow-1">
                                      <div class="d-flex align-center justify-space-between mb-1">
                                        <span class="font-weight-bold text-caption text-high-emphasis">أسئلة مختلفة ومستقلة في كل نموذج</span>
                                        <v-icon
                                          :color="group.questions_variation === 'different_questions' ? 'secondary' : 'medium-emphasis'"
                                          size="16"
                                        >
                                          {{ group.questions_variation === 'different_questions' ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                                        </v-icon>
                                      </div>
                                      <p class="text-caption text-medium-emphasis mb-0" style="font-size: 11px !important; line-height: 1.4;">
                                        توليد حزمة أسئلة مختلفة ومستقلة تماماً لكل نموذج من بنك الأسئلة وفق معايير المجموعة.
                                      </p>
                                    </div>
                                  </div>
                                </div>
                              </v-col>
                            </v-row>
                          </div>

                          <!-- Difficulty Distribution Sliders -->
                          <div class="pa-4 rounded-xl mb-4 group-inner-section group-difficulty-container">
                            <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                              <span class="text-caption font-weight-bold text-medium-emphasis d-flex align-center">
                                <v-icon size="16" class="me-1">mdi-speedometer</v-icon>
                                توزيع أوزان الصعوبة لـ {{ group.name || ('المجموعة ' + (gIdx + 1)) }}:
                              </span>
                              <div class="d-flex align-center gap-2">
                                <v-chip
                                  size="small"
                                  :color="groupDiffTotal(group) === 100 ? 'success' : 'warning'"
                                  variant="tonal"
                                  class="font-weight-bold"
                                >
                                  الإجمالي: {{ groupDiffTotal(group) }}% / 100%
                                </v-chip>
                              </div>
                            </div>

                            <v-row dense>
                              <v-col v-for="diff in difficultyItems" :key="diff.key" cols="12" md="4">
                                <div class="pa-3 rounded-lg border-subtle h-100 d-flex flex-column justify-space-between">
                                  <div class="d-flex align-center justify-space-between mb-2">
                                    <span class="text-caption font-weight-bold">{{ diff.label }}</span>
                                    <v-chip size="x-small" :color="diff.color" variant="flat" class="font-weight-black">
                                      {{ Math.round(group.difficulty_distribution[diff.key] || 0) }}%
                                    </v-chip>
                                  </div>

                                  <div class="d-flex align-center gap-2">
                                    <v-btn
                                      icon
                                      size="x-small"
                                      variant="tonal"
                                      :color="diff.color"
                                      :disabled="(group.difficulty_distribution[diff.key] || 0) <= 0"
                                      @click="stepGroupDiff(group, diff.key, -5)"
                                    >
                                      <v-icon size="14">mdi-minus</v-icon>
                                    </v-btn>

                                    <v-slider
                                      :model-value="group.difficulty_distribution[diff.key]"
                                      :min="0"
                                      :max="100"
                                      :step="5"
                                      :color="diff.color"
                                      hide-details
                                      thumb-size="14"
                                      track-size="6"
                                      class="flex-grow-1"
                                      @update:model-value="(val) => updateGroupDiff(group, diff.key, val)"
                                    />

                                    <v-btn
                                      icon
                                      size="x-small"
                                      variant="tonal"
                                      :color="diff.color"
                                      :disabled="groupDiffTotal(group) >= 100"
                                      @click="stepGroupDiff(group, diff.key, 5)"
                                    >
                                      <v-icon size="14">mdi-plus</v-icon>
                                    </v-btn>
                                  </div>
                                </div>
                              </v-col>
                            </v-row>

                            <v-alert v-if="groupDiffTotal(group) !== 100" type="warning" density="compact" variant="tonal" class="mt-3 rounded-lg">
                              إجمالي نسب الصعوبة: {{ groupDiffTotal(group) }}% (المتبقي: {{ 100 - groupDiffTotal(group) }}% يجب توزيعه للوصول إلى 100%)
                            </v-alert>
                          </div>

                          <!-- Geographic Target Scope for this Model Group -->
                          <div class="pa-4 rounded-xl mb-2 group-inner-section group-geo-container">
                            <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                              <span class="text-caption font-weight-bold text-medium-emphasis d-flex align-center">
                                <v-icon size="16" class="me-1" color="deep-purple">mdi-map-marker-radius</v-icon>
                                النطاق والمناطق المستهدفة حصرياً لـ {{ group.name || ('المجموعة ' + (gIdx + 1)) }}:
                              </span>
                              <v-chip v-if="(group.scope_level || 'all') !== 'all' && group.target_ids?.length" size="x-small" color="deep-purple" variant="tonal" class="font-weight-bold">
                                تم تحديد {{ group.target_ids.length }} منطقة
                              </v-chip>
                            </div>

                            <!-- Scope Level Toggle -->
                            <v-btn-toggle
                              v-model="group.scope_level"
                              mandatory
                              color="deep-purple"
                              variant="outlined"
                              density="compact"
                              rounded="lg"
                              class="mb-3 d-flex flex-wrap"
                              @update:model-value="onGroupScopeLevelChange(group)"
                            >
                              <v-btn value="all" size="small" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-earth">
                                كافة المناطق (عام)
                              </v-btn>
                              <v-btn value="governorate" size="small" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-city-variant-outline">
                                محافظات محددة
                              </v-btn>
                              <v-btn v-if="exam.institution_type === 'school'" value="directorate" size="small" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-map-marker-radius">
                                مديريات محددة
                              </v-btn>
                              <v-btn value="school" size="small" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-school-outline">
                                {{ exam.institution_type === 'university' ? 'جامعات محددة' : exam.institution_type === 'institute' ? 'معاهد محددة' : 'مدارس محددة' }}
                              </v-btn>
                            </v-btn-toggle>

                            <!-- Level 1: All regions -->
                            <div v-if="(group.scope_level || 'all') === 'all'" class="d-flex align-center gap-2 py-1 text-medium-emphasis text-caption">
                              <v-icon size="16" color="success">mdi-check-circle-outline</v-icon>
                              <span>تسري هذه المجموعة على جميع المناطق دون حصر جغرافي.</span>
                            </div>

                            <!-- Level 2: Specific Governorates -->
                            <div v-else-if="group.scope_level === 'governorate'">
                              <v-autocomplete
                                v-model="group.target_ids"
                                :items="governoratesList"
                                item-title="name_ar"
                                item-value="id"
                                label="المحافظات المستهدفة لهذه المجموعة *"
                                placeholder="اختر المحافظات المستهدفة (مثال: أمانة العاصمة، صنعاء، تعز، عدن...)"
                                multiple
                                chips
                                closable-chips
                                variant="outlined"
                                density="compact"
                                rounded="lg"
                                hide-details="auto"
                                prepend-inner-icon="mdi-city-variant-outline"
                                :rules="[v => (Array.isArray(v) && v.length > 0) || 'يرجى تحديد محافظة واحدة على الأقل لهذه المجموعة']"
                                :loading="loadingGeoData"
                              />
                            </div>

                            <!-- Level 3: Specific Directorates -->
                            <div v-else-if="group.scope_level === 'directorate'">
                              <v-row dense>
                                <v-col cols="12" md="4">
                                  <v-autocomplete
                                    v-model="group.filter_governorate_id"
                                    :items="governoratesList"
                                    item-title="name_ar"
                                    item-value="id"
                                    label="تصفية بالمحافظة (اختياري)"
                                    placeholder="اختر المحافظة لتصفية المديريات..."
                                    clearable
                                    variant="outlined"
                                    density="compact"
                                    rounded="lg"
                                    hide-details="auto"
                                    prepend-inner-icon="mdi-filter-variant"
                                    :loading="loadingGeoData"
                                  />
                                </v-col>
                                <v-col cols="12" md="8">
                                  <v-autocomplete
                                    v-model="group.target_ids"
                                    :items="getDirectoratesForGroup(group)"
                                    item-title="name_ar"
                                    item-value="id"
                                    label="المديريات المستهدفة لهذه المجموعة *"
                                    placeholder="اختر المديريات..."
                                    multiple
                                    chips
                                    closable-chips
                                    variant="outlined"
                                    density="compact"
                                    rounded="lg"
                                    hide-details="auto"
                                    prepend-inner-icon="mdi-map-marker-radius"
                                    :rules="[v => (Array.isArray(v) && v.length > 0) || 'يرجى تحديد مديرية واحدة على الأقل']"
                                    :loading="loadingGeoData"
                                  />
                                </v-col>
                              </v-row>
                            </div>

                            <!-- Level 4: Specific Schools / Institutions -->
                            <div v-else-if="group.scope_level === 'school'">
                              <v-row dense>
                                <v-col cols="12" :md="exam.institution_type === 'school' ? 3 : 4">
                                  <v-autocomplete
                                    v-model="group.filter_governorate_id"
                                    :items="governoratesList"
                                    item-title="name_ar"
                                    item-value="id"
                                    label="المحافظة *"
                                    placeholder="المحافظة..."
                                    clearable
                                    variant="outlined"
                                    density="compact"
                                    rounded="lg"
                                    hide-details="auto"
                                    :loading="loadingGeoData"
                                    @update:model-value="onGroupFilterGovForSchool(group)"
                                  />
                                </v-col>
                                <v-col cols="12" md="3" v-if="exam.institution_type === 'school'">
                                  <v-autocomplete
                                    v-model="group.filter_directorate_id"
                                    :items="getDirectoratesForFilterGov(group.filter_governorate_id)"
                                    item-title="name_ar"
                                    item-value="id"
                                    label="المديرية *"
                                    :placeholder="group.filter_governorate_id ? 'المديرية...' : 'اختر المحافظة أولاً'"
                                    clearable
                                    variant="outlined"
                                    density="compact"
                                    rounded="lg"
                                    hide-details="auto"
                                    :disabled="!group.filter_governorate_id"
                                    :loading="loadingGeoData"
                                    @update:model-value="onGroupFilterDirForSchool(group)"
                                  />
                                </v-col>
                                <v-col cols="12" :md="exam.institution_type === 'school' ? 6 : 8">
                                  <v-autocomplete
                                    v-model="group.target_ids"
                                    :items="group.availableSchools || []"
                                    item-title="name_ar"
                                    item-value="id"
                                    :label="exam.institution_type === 'university' ? 'الجامعات / الكليات المستهدفة *' : exam.institution_type === 'institute' ? 'المعاهد المستهدفة *' : 'المدارس المستهدفة *'"
                                    placeholder="اختر المؤسسات المستهدفة..."
                                    :disabled="isGroupSchoolDisabled(group)"
                                    multiple
                                    chips
                                    closable-chips
                                    variant="outlined"
                                    density="compact"
                                    rounded="lg"
                                    hide-details="auto"
                                    :rules="[v => (Array.isArray(v) && v.length > 0) || 'يرجى تحديد مؤسسة واحدة على الأقل']"
                                    :prepend-inner-icon="exam.institution_type === 'university' ? 'mdi-domain' : 'mdi-school'"
                                    :loading="group.loadingSchools"
                                  />
                                </v-col>
                              </v-row>
                            </div>
                          </div>
                        </div>

                        <!-- Distinctive Visual Divider between consecutive groups -->
                        <div v-if="gIdx < modelGroups.length - 1" class="d-flex align-center justify-center my-6">
                          <div class="group-divider-line flex-grow-1"></div>
                          <div class="group-divider-badge d-flex align-center gap-1.5 px-4 py-1.5 rounded-pill mx-3 text-caption font-weight-bold">
                            <v-icon size="16" color="primary">mdi-arrow-down-bold-circle-outline</v-icon>
                            <span>المجموعة التالية ({{ gIdx + 2 }})</span>
                          </div>
                          <div class="group-divider-line flex-grow-1"></div>
                        </div>
                      </template>

                        <div class="d-flex align-center justify-space-between mt-4 flex-wrap gap-2">
                          <custom-btn type="add" label="إضافة مجموعة نماذج جديدة" icon="mdi-plus" variant="tonal" color="primary"
                            class="font-weight-bold" :click="addModelGroup" />
                          <v-chip color="info" variant="tonal" class="font-weight-bold">
                            إجمالي عدد النماذج الإجمالي: {{ totalModelsCount }}
                          </v-chip>
                        </div>
                      </div>
                    </v-expand-transition>
                  </div>
                </v-col>
              </v-row>
            </v-form>
          </v-window-item>

          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- STEP 2: BLUEPRINT MATRIX (SEGMENTED CONTROL OVERHAUL)            -->
          <!-- ════════════════════════════════════════════════════════════════ -->
          <v-window-item :value="2">
            <!-- Integrated Flush Tabs inside a single card -->
            <div class="section-group-card rounded-2xl overflow-hidden mb-6 border-subtle">
              <div class="matrix-tabs-bar border-b-subtle d-flex" style="overflow-x: auto;">
                <button v-for="(tab, tIdx) in matrixTabItems" :key="tIdx"
                  class="matrix-tab-btn flex-1-1-100 pa-4 text-center cursor-pointer font-weight-bold d-flex align-center justify-center gap-2"
                  :class="{ 'is-active': activeTab === tIdx }"
                  @click="activeTab = tIdx">
                  <v-icon size="20">{{ tab.icon }}</v-icon>
                  <span>{{ tab.label }}</span>
                </button>
              </div>

              <v-window v-model="activeTab" class="pa-6 bg-transparent">
                <!-- Units Distribution -->
                <v-window-item :value="0">
                  <!-- Units Header & Actions -->
                  <div class="units-tab-header d-flex justify-space-between align-center mb-5 flex-wrap gap-3">
                    <div class="d-flex align-center gap-3">
                      <div class="units-header-icon-box">
                        <v-icon size="26" color="primary">mdi-layers-triple</v-icon>
                      </div>
                      <div>
                        <div class="d-flex align-center gap-2 flex-wrap">
                          <h3 class="text-subtitle-1 font-weight-black mb-0 text-high-emphasis">
                            {{ exam.institution_type === 'university' ? 'توزيع الأسئلة على المفردات والموضوعات' : 'توزيع الأسئلة على الوحدات الدراسية' }}
                          </h3>
                          <v-chip v-if="modelsMode === 'advanced'" size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                            تخصيص حسب المجموعات
                          </v-chip>
                        </div>
                        <p class="text-caption text-medium-emphasis mb-0 mt-0.5">
                          {{ modelsMode === 'advanced' ? 'تحديد وتخصيص الأوزان النسبية للوحدات لكل مجموعة نماذج بشكل مستقل لضمان تنوع المحتوى، بحيث يعادل مجموع كل مجموعة 100%' : 'تحديد الأوزان النسبية للوحدات بحيث يكون مجموع نسب الأسئلة 100% تماماً' }}
                        </p>
                      </div>
                    </div>

                    <!-- Global Action buttons -->
                    <div v-if="modelsMode === 'advanced'" class="d-flex align-center gap-2 flex-wrap">
                      <v-btn
                        variant="tonal"
                        color="secondary"
                        size="small"
                        class="font-weight-bold rounded-xl text-none px-4"
                        prepend-icon="mdi-equal-box"
                        @click="autoDistributeAllGroupsUnits"
                      >
                        توزيع متساوٍ للكل
                      </v-btn>
                      <v-btn
                        v-if="modelGroups.length > 1"
                        variant="outlined"
                        color="info"
                        size="small"
                        class="font-weight-bold rounded-xl text-none px-4"
                        prepend-icon="mdi-content-copy"
                        @click="copyCurrentGroupUnitsToAll"
                      >
                        نسخ هذا التوزيع للباقي
                      </v-btn>
                    </div>
                    <v-btn
                      v-else
                      variant="tonal"
                      color="primary"
                      size="small"
                      class="font-weight-bold rounded-xl text-none px-4"
                      prepend-icon="mdi-scale-balance"
                      @click="() => autoDistribute('units')"
                    >
                      توزيع متساوٍ
                    </v-btn>
                  </div>

                  <!-- Advanced Mode: Modern Model Groups Selector Hub (Zero Gray) -->
                  <div v-if="modelsMode === 'advanced'" class="model-groups-selector-hub mb-5">
                    <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                      <div class="d-flex align-center gap-2">
                        <div class="hub-bullet-dot"></div>
                        <span class="font-weight-black text-subtitle-2 text-high-emphasis">اختر مجموعة النماذج لتخصيص وحداتها:</span>
                        <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
                          {{ modelGroups.length }} مجموعات
                        </v-chip>
                      </div>
                      <span class="text-caption text-medium-emphasis d-flex align-center gap-1">
                        <v-icon size="14" color="primary">mdi-gesture-tap</v-icon>
                        انقر على أي مجموعة للانتقال لتخصيص وحداتها الدراسية
                      </span>
                    </div>

                    <div class="group-pills-grid">
                      <div
                        v-for="(grp, gIdx) in modelGroups"
                        :key="gIdx"
                        class="group-switch-pill"
                        :class="{ 'is-active': activeUnitGroupIndex === gIdx }"
                        @click="selectUnitGroup(gIdx)"
                      >
                        <div class="d-flex align-center justify-space-between gap-2 mb-1.5">
                          <div class="d-flex align-center gap-2">
                            <v-icon size="20" :color="activeUnitGroupIndex === gIdx ? 'primary' : 'medium-emphasis'">
                              {{ activeUnitGroupIndex === gIdx ? 'mdi-folder-open' : 'mdi-folder-outline' }}
                            </v-icon>
                            <span class="group-pill-title font-weight-black">
                              {{ grp.name || ('المجموعة ' + (gIdx + 1)) }}
                            </span>
                          </div>
                          <v-chip
                            size="x-small"
                            :color="difficultyColor(grp.difficulty_profile)"
                            variant="tonal"
                            class="font-weight-bold"
                          >
                            {{ difficultyLabel(grp.difficulty_profile) }}
                          </v-chip>
                        </div>

                        <div class="d-flex align-center justify-space-between mt-2 pt-2 border-t-subtle text-caption">
                          <span class="text-medium-emphasis">
                            النماذج: <strong class="text-high-emphasis">{{ getGroupVersionCodes(gIdx) }}</strong>
                            ({{ grp.count || 1 }})
                          </span>
                          <span
                            class="font-weight-black font-mono pill-percentage-badge"
                            :class="getGroupUnitsTotal(grp) === 100 ? 'is-complete' : 'is-pending'"
                          >
                            <v-icon size="12" start>{{ getGroupUnitsTotal(grp) === 100 ? 'mdi-check' : 'mdi-clock-outline' }}</v-icon>
                            {{ getGroupUnitsTotal(grp) }}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Advanced Mode: Prominent Active Group Hero Command Banner -->
                  <div v-if="modelsMode === 'advanced'" class="active-group-hero-banner mb-5">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-4">
                      <div class="d-flex align-center gap-3">
                        <div class="active-group-hero-avatar">
                          <v-icon size="28" color="white">mdi-tune-vertical-variant</v-icon>
                        </div>
                        <div>
                          <div class="d-flex align-center gap-2 flex-wrap mb-1">
                            <h4 class="text-subtitle-1 font-weight-black mb-0 text-primary">
                              أوزان: {{ currentUnitGroup ? (currentUnitGroup.name || ('المجموعة ' + (activeUnitGroupIndex + 1))) : '' }}
                            </h4>
                            <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
                              {{ getGroupVersionCodes(activeUnitGroupIndex) }} ({{ currentUnitGroup ? currentUnitGroup.count : 1 }} نماذج)
                            </v-chip>
                            <v-chip size="small" :color="difficultyColor(currentUnitGroup?.difficulty_profile)" variant="tonal" class="font-weight-bold">
                              {{ difficultyLabel(currentUnitGroup?.difficulty_profile) }}
                            </v-chip>
                          </div>
                          <span class="text-caption text-medium-emphasis d-block">
                            النسب المحددة بالأسفل تنطبق حصرياً على نماذج هذه المجموعة وتحدد نسبة الأسئلة المستخرجة من كل وحدة
                          </span>
                        </div>
                      </div>

                      <div class="d-flex align-center gap-3 flex-wrap">
                        <div class="hero-total-badge d-flex align-center gap-2 px-3 py-2 rounded-xl"
                          :class="currentGroupUnitsTotal === 100 ? 'badge-success' : 'badge-warning'">
                          <div>
                            <div class="text-caption font-weight-bold opacity-80">إجمالي النسبة</div>
                            <div class="font-weight-black text-h6 font-mono leading-none">
                              {{ currentGroupUnitsTotal }}%
                            </div>
                          </div>
                          <v-icon size="24">{{ currentGroupUnitsTotal === 100 ? 'mdi-check-decagram' : 'mdi-alert-circle-outline' }}</v-icon>
                        </div>

                        <v-btn
                          variant="tonal"
                          color="primary"
                          size="small"
                          class="font-weight-bold rounded-xl px-4"
                          prepend-icon="mdi-scale-balance"
                          @click="autoDistributeCurrentGroupUnits"
                        >
                          توزيع متساوٍ لهذه المجموعة
                        </v-btn>
                      </div>
                    </div>
                  </div>

                  <!-- Empty State when no units loaded (Zero Gray, clean dotted border) -->
                  <div v-if="!currentActiveUnitsList || currentActiveUnitsList.length === 0" class="modern-empty-state mb-5">
                    <div class="empty-state-icon-box mx-auto mb-3">
                      <v-icon size="36" color="primary">mdi-book-open-blank-variant</v-icon>
                    </div>
                    <h4 class="font-weight-black text-subtitle-1 mb-1 text-high-emphasis">
                      لا توجد وحدات أو مفردات دراسية مسجلة لهذه المادة حالياً
                    </h4>
                    <p class="text-caption text-medium-emphasis mb-4 mx-auto" style="max-width: 480px;">
                      تأكد من اختيار المادة والصف الدراسي في الخطوة 1، أو انقر على الزر أدناه لإعادة فحص وتحميل الوحدات من قاعدة البيانات.
                    </p>
                    <v-btn
                      variant="tonal"
                      color="primary"
                      class="font-weight-bold rounded-xl px-5"
                      prepend-icon="mdi-refresh"
                      @click="loadBlueprintUnits"
                    >
                      إعادة تحميل وفحص الوحدات
                    </v-btn>
                  </div>

                  <!-- Units Cards Rendering -->
                  <template v-else-if="hasTermSeparation">
                    <template v-for="termId in [1, 2, 3]" :key="'term-' + termId">
                      <div v-if="currentActiveUnitsList.some(u => isUnitInTerm(u, termId))" class="mb-5">
                        <div class="term-header-banner mb-3 d-flex align-center gap-2">
                          <v-icon size="20" color="primary">mdi-book-open-page-variant</v-icon>
                          <span class="font-weight-black text-subtitle-2 text-primary" v-if="termId === 1">الفصل الدراسي الأول</span>
                          <span class="font-weight-black text-subtitle-2 text-primary" v-else-if="termId === 2">الفصل الدراسي الثاني</span>
                          <span class="font-weight-black text-subtitle-2 text-primary" v-else>{{ exam.institution_type === 'university' ? 'موضوعات عامة' : 'وحدات عامة' }}</span>
                        </div>
                        <v-row dense>
                          <v-col
                            v-for="unit in currentActiveUnitsList.filter(u => isUnitInTerm(u, termId))"
                            :key="'grp-' + activeUnitGroupIndex + '-u-' + unit.id"
                            cols="12"
                            md="6"
                          >
                            <div class="modern-unit-card mb-3" :class="{ 'is-excluded': unit.isExcluded }">
                              <div class="d-flex justify-space-between align-start mb-2 gap-2">
                                <div class="flex-grow-1">
                                  <div class="d-flex align-center gap-2 flex-wrap mb-1">
                                    <span class="unit-title font-weight-black text-subtitle-2">{{ unit.name }}</span>
                                    <v-chip v-if="unit.isExcluded" size="x-small" color="error" variant="flat" class="font-weight-bold">
                                      <v-icon start size="12">mdi-cancel</v-icon>
                                      مستبعد من الاختبار
                                    </v-chip>
                                  </div>
                                  
                                  <div class="d-flex align-center gap-2 flex-wrap">
                                    <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                                      <v-icon start size="12">mdi-book-open-page-variant</v-icon>
                                      {{ getUnitLessonsCount(unit.id) }} {{ exam.institution_type === 'university' ? 'محاضرة' : 'درس' }}
                                    </v-chip>
                                    <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold">
                                      <v-icon start size="12">mdi-check-circle-outline</v-icon>
                                      {{ getUnitApprovedQuestionsCount(unit.id) }} سؤال معتمد
                                    </v-chip>
                                    <v-btn
                                      variant="text"
                                      color="info"
                                      size="x-small"
                                      class="font-weight-bold px-1 text-none"
                                      prepend-icon="mdi-eye-outline"
                                      @click="openUnitDetails(unit.id, unit.name)"
                                    >
                                      {{ exam.institution_type === 'university' ? 'محتوى المفردة' : 'محتوى الوحدة' }}
                                    </v-btn>
                                  </div>
                                </div>

                                <!-- Stepper & Direct Percentage Display -->
                                <div class="d-flex align-center gap-1 unit-stepper-box">
                                  <v-btn
                                    icon="mdi-minus"
                                    size="x-small"
                                    variant="tonal"
                                    color="primary"
                                    class="rounded-lg"
                                    :disabled="unit.isExcluded || (unit.percentage || 0) <= 0"
                                    @click="adjustUnitPercentage(unit.id, -5)"
                                  />
                                  <div class="unit-percentage-display font-mono" :class="{ 'is-zero': !unit.percentage, 'is-excluded': unit.isExcluded }">
                                    {{ unit.percentage || 0 }}%
                                  </div>
                                  <v-btn
                                    icon="mdi-plus"
                                    size="x-small"
                                    variant="tonal"
                                    color="primary"
                                    class="rounded-lg"
                                    :disabled="unit.isExcluded || currentGroupUnitsTotal >= 100"
                                    @click="adjustUnitPercentage(unit.id, 5)"
                                  />
                                </div>
                              </div>

                              <!-- Custom Slider -->
                              <v-slider
                                :model-value="unit.percentage"
                                :disabled="unit.isExcluded"
                                @update:model-value="(val) => updateUnitPercentage(unit.id, val)"
                                :min="0"
                                :max="100"
                                :step="5"
                                :color="unit.isExcluded ? 'error' : 'primary'"
                                track-color="rgba(var(--v-theme-primary), 0.15)"
                                hide-details
                                thumb-size="16"
                                track-size="6"
                                class="mt-1"
                              />
                            </div>
                          </v-col>
                        </v-row>
                      </div>
                    </template>
                  </template>
                  <template v-else>
                    <v-row dense>
                      <v-col
                        v-for="unit in currentActiveUnitsList"
                        :key="'grp-' + activeUnitGroupIndex + '-u-' + unit.id"
                        cols="12"
                        md="6"
                      >
                        <div class="modern-unit-card mb-3" :class="{ 'is-excluded': unit.isExcluded }">
                          <div class="d-flex justify-space-between align-start mb-2 gap-2">
                            <div class="flex-grow-1">
                              <div class="d-flex align-center gap-2 flex-wrap mb-1">
                                <span class="unit-title font-weight-black text-subtitle-2">{{ unit.name }}</span>
                                <v-chip v-if="unit.isExcluded" size="x-small" color="error" variant="flat" class="font-weight-bold">
                                  <v-icon start size="12">mdi-cancel</v-icon>
                                  مستبعد من الاختبار
                                </v-chip>
                              </div>
                              
                              <div class="d-flex align-center gap-2 flex-wrap">
                                <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                                  <v-icon start size="12">mdi-book-open-page-variant</v-icon>
                                  {{ getUnitLessonsCount(unit.id) }} {{ exam.institution_type === 'university' ? 'محاضرة' : 'درس' }}
                                </v-chip>
                                <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold">
                                  <v-icon start size="12">mdi-check-circle-outline</v-icon>
                                  {{ getUnitApprovedQuestionsCount(unit.id) }} سؤال معتمد
                                </v-chip>
                                <v-btn
                                  variant="text"
                                  color="info"
                                  size="x-small"
                                  class="font-weight-bold px-1 text-none"
                                  prepend-icon="mdi-eye-outline"
                                  @click="openUnitDetails(unit.id, unit.name)"
                                >
                                  {{ exam.institution_type === 'university' ? 'محتوى المفردة' : 'محتوى الوحدة' }}
                                </v-btn>
                              </div>
                            </div>

                            <!-- Stepper & Direct Percentage Display -->
                            <div class="d-flex align-center gap-1 unit-stepper-box">
                              <v-btn
                                icon="mdi-minus"
                                size="x-small"
                                variant="tonal"
                                color="primary"
                                class="rounded-lg"
                                :disabled="unit.isExcluded || (unit.percentage || 0) <= 0"
                                @click="adjustUnitPercentage(unit.id, -5)"
                              />
                              <div class="unit-percentage-display font-mono" :class="{ 'is-zero': !unit.percentage, 'is-excluded': unit.isExcluded }">
                                {{ unit.percentage || 0 }}%
                              </div>
                              <v-btn
                                icon="mdi-plus"
                                size="x-small"
                                variant="tonal"
                                color="primary"
                                class="rounded-lg"
                                :disabled="unit.isExcluded || currentGroupUnitsTotal >= 100"
                                @click="adjustUnitPercentage(unit.id, 5)"
                              />
                            </div>
                          </div>

                          <!-- Custom Slider -->
                          <v-slider
                            :model-value="unit.percentage"
                            :disabled="unit.isExcluded"
                            @update:model-value="(val) => updateUnitPercentage(unit.id, val)"
                            :min="0"
                            :max="100"
                            :step="5"
                            :color="unit.isExcluded ? 'error' : 'primary'"
                            track-color="rgba(var(--v-theme-primary), 0.15)"
                            hide-details
                            thumb-size="16"
                            track-size="6"
                            class="mt-1"
                          />
                        </div>
                      </v-col>
                    </v-row>
                  </template>

                  <!-- Bottom Balance Status Card (Modern and Zero Gray) -->
                  <div v-if="currentGroupUnitsTotal !== 100" class="unit-balance-alert-card is-warning mt-4">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                      <div class="d-flex align-center gap-3">
                        <v-icon size="26" color="warning">mdi-alert-circle</v-icon>
                        <div>
                          <div class="font-weight-black text-subtitle-2 mb-0.5">
                            <span v-if="modelsMode === 'advanced'">
                              توزيع أوزان الوحدات لـ ({{ currentUnitGroup ? (currentUnitGroup.name || ('المجموعة ' + (activeUnitGroupIndex + 1))) : '' }}) غير مكتمل
                            </span>
                            <span v-else>
                              توزيع أوزان الوحدات غير مكتمل
                            </span>
                          </div>
                          <span class="text-caption text-medium-emphasis">
                            <template v-if="currentGroupUnitsTotal < 100">
                              المجموع الحالي <strong>{{ currentGroupUnitsTotal }}%</strong>. يتبقى <strong>{{ 100 - currentGroupUnitsTotal }}%</strong> للوصول إلى 100% تماماً.
                            </template>
                            <template v-else>
                              المجموع الحالي <strong>{{ currentGroupUnitsTotal }}%</strong>. تم تجاوز 100% بمقدار <strong>{{ currentGroupUnitsTotal - 100 }}%</strong>، يرجى تخفيض بعض الوحدات.
                            </template>
                          </span>
                        </div>
                      </div>

                      <v-btn
                        v-if="currentGroupUnitsTotal < 100"
                        variant="tonal"
                        color="warning"
                        size="small"
                        class="font-weight-bold rounded-xl text-none px-4"
                        prepend-icon="mdi-scale-balance"
                        @click="autoDistributeCurrentGroupUnits"
                      >
                        إعادة توزيع متساوٍ لهذه المجموعة
                      </v-btn>
                    </div>
                  </div>

                  <div v-else class="unit-balance-alert-card is-success mt-4">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                      <div class="d-flex align-center gap-3">
                        <v-icon size="26" color="success">mdi-check-decagram</v-icon>
                        <div>
                          <div class="font-weight-black text-subtitle-2 mb-0.5 text-success">
                            توزيع أوزان الوحدات مكتمل تماماً ومثالي (100%)
                          </div>
                          <span class="text-caption text-medium-emphasis">
                            <template v-if="modelsMode === 'advanced'">
                              أوزان الوحدات لـ ({{ currentUnitGroup ? (currentUnitGroup.name || ('المجموعة ' + (activeUnitGroupIndex + 1))) : '' }}) جاهزة ومعتمدة لتوليد نماذج هذه المجموعة.
                            </template>
                            <template v-else>
                              تم ضبط نسب جميع الوحدات بنجاح وجاهزة لتوليد أسئلة الاختبار.
                            </template>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-window-item>

                <!-- Difficulty Distribution -->
                <v-window-item :value="1">
                  <!-- ═══ ADVANCED MODE: Managed per group in Step 1 ═══ -->
                  <template v-if="modelsMode === 'advanced'">
                    <v-alert type="info" variant="tonal" density="comfortable" class="rounded-2xl mb-5">
                      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                        <div class="d-flex align-center gap-3">
                          <v-avatar size="38" color="info" variant="tonal" class="rounded-xl">
                            <v-icon size="24" color="info">mdi-tune-variant</v-icon>
                          </v-avatar>
                          <div>
                            <div class="font-weight-black text-subtitle-2">أنت تعمل في وضع النماذج المتقدمة والمناطقية (Advanced Mode)</div>
                            <div class="text-caption text-medium-emphasis">
                              تم تحديد وتوزيع نسب مستويات الصعوبة لكل مجموعة نماذج ومناطقها بشكل مستقل في <strong>الخطوة 1</strong>، ولا تسري أشرطة الصعوبة الموحدة هنا.
                            </div>
                          </div>
                        </div>
                        <v-btn variant="tonal" color="primary" size="small" class="font-weight-bold" @click="step = 1">
                          <v-icon start size="16">mdi-cog-outline</v-icon>
                          تعديل صعوبة المجموعات في الخطوة 1
                        </v-btn>
                      </div>
                    </v-alert>

                    <div class="pa-5 rounded-2xl border-subtle mb-4">
                      <h5 class="text-subtitle-2 font-weight-black mb-3 d-flex align-center gap-2">
                        <v-icon size="20" color="primary">mdi-format-list-checks</v-icon>
                        جدول توزيع الصعوبة المعتمد لمجموعات النماذج:
                      </h5>
                      <v-table density="compact" class="executive-table rounded-xl border-subtle">
                        <thead>
                          <tr class="table-header-row">
                            <th class="font-weight-bold">المجموعة</th>
                            <th class="font-weight-bold">النماذج التابعة</th>
                            <th class="font-weight-bold">ملف الصعوبة</th>
                            <th class="font-weight-bold">سهل</th>
                            <th class="font-weight-bold">متوسط</th>
                            <th class="font-weight-bold">صعب</th>
                            <th class="font-weight-bold">المناطق المستهدفة</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(group, gIdx) in modelGroups" :key="gIdx">
                            <td class="font-weight-bold">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</td>
                            <td>
                              <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold font-mono">
                                {{ getGroupVersionCodes(gIdx) }} ({{ group.count }} نماذج)
                              </v-chip>
                            </td>
                            <td>
                              <v-chip size="x-small" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="font-weight-bold">
                                {{ difficultyLabel(group.difficulty_profile) }}
                              </v-chip>
                            </td>
                            <td>
                              <span class="text-success font-weight-bold">{{ group.difficulty_distribution.easy }}%</span>
                            </td>
                            <td>
                              <span class="text-warning font-weight-bold">{{ group.difficulty_distribution.medium }}%</span>
                            </td>
                            <td>
                              <span class="text-error font-weight-bold">{{ group.difficulty_distribution.hard }}%</span>
                            </td>
                            <td class="text-caption">
                              <span v-if="group.target_ids && group.target_ids.length > 0" class="font-weight-bold text-primary">
                                {{ getGroupTargetNames(group) }}
                              </span>
                              <span v-else-if="(group.scope_level || 'all') === 'all'" class="text-success font-weight-bold">
                                كافة المناطق (عام)
                              </span>
                              <span v-else class="text-medium-emphasis">لم يتم التحديد</span>
                            </td>
                          </tr>
                        </tbody>
                      </v-table>
                    </div>
                  </template>

                  <!-- ═══ UNIFORM MODE: Editable Sliders ═══ -->
                  <template v-else>
                    <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-2">
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">توزيع مستويات الصعوبة (الوضع الموحد)</h4>
                        <span class="text-caption text-medium-emphasis">تسري هذه النسب على جميع النماذج المنتجة بالتساوي</span>
                      </div>
                      <custom-btn label="توزيع متساوٍ" icon="mdi-scale-balance" variant="tonal" color="primary" class="font-weight-bold"
                        :click="() => autoDistribute('difficulty')" />
                    </div>

                    <v-row dense>
                      <v-col v-for="(level, index) in blueprint.difficulty" :key="index" cols="12" md="4">
                        <div class="pa-4 rounded-xl border-subtle mb-2">
                          <div class="d-flex justify-space-between align-center mb-1">
                            <span class="font-weight-bold">{{ level.name }}</span>
                            <v-chip size="small" :color="level.color" variant="tonal"
                              class="font-weight-bold">{{
                                level.percentage }}%</v-chip>
                          </div>
                          <v-slider :model-value="level.percentage"
                            @update:model-value="(val) => updateDistribution(blueprint.difficulty, index, val)" :min="0"
                            :max="100" :step="5" :color="level.color" hide-details thumb-size="14" track-size="6"
                            class="mt-2" />
                        </div>
                      </v-col>
                    </v-row>

                    <v-alert v-if="totalDifficultyPercentage !== 100"
                      :type="totalDifficultyPercentage === 100 ? 'success' : 'warning'" density="compact" variant="tonal"
                      class="mt-4 rounded-xl">
                      إجمالي النسبة الحالية: {{ totalDifficultyPercentage }}% (يجب أن يعادل 100% تماماً)
                    </v-alert>
                  </template>
                </v-window-item>

                <!-- Bloom Levels (Optional) -->
                <v-window-item :value="2">
                  <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-2">
                    <div class="d-flex align-center gap-3">
                      <h4 class="text-subtitle-1 font-weight-black mb-0">مستويات بلوم المعرفية</h4>
                      <v-switch
                        v-model="bloomEnabled"
                        color="primary"
                        hide-details
                        density="compact"
                        class="ma-0 pa-0"
                        :label="bloomEnabled ? 'مفعّل' : 'معطّل (تلقائي)'"
                      />
                    </div>
                    <custom-btn v-if="bloomEnabled" label="توزيع متساوٍ" icon="mdi-scale-balance" variant="tonal" color="primary" class="font-weight-bold"
                      :click="() => autoDistribute('bloom')" />
                  </div>

                  <v-alert v-if="!bloomEnabled" type="info" variant="tonal" density="compact" class="rounded-xl mb-4">
                    <v-icon start>mdi-information</v-icon>
                    مستويات بلوم المعرفية معطلة تلقائياً — لن تدخل في حسبة توليد الاختبار، ويتم توزيع الأسئلة واعتمادها حسب أوزان الصعوبة والوحدات فقط.
                  </v-alert>

                  <v-row v-if="bloomEnabled" dense>
                    <v-col v-for="(level, index) in blueprint.bloom" :key="index" cols="12" sm="6" md="4">
                      <div class="pa-4 rounded-xl border-subtle mb-2">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-bold">{{ level.name }}</span>
                          <v-chip size="small" :color="level.color" variant="tonal"
                            class="font-weight-bold">{{
                              level.percentage }}%</v-chip>
                        </div>
                        <v-slider :model-value="level.percentage"
                          @update:model-value="(val) => updateDistribution(blueprint.bloom, index, val)" :min="0"
                          :max="100" :step="5" :color="level.color" hide-details thumb-size="14" track-size="6"
                          class="mt-2" />
                      </div>
                    </v-col>
                  </v-row>
                  <v-alert v-if="bloomEnabled && totalBloomPercentage !== 100"
                    :type="totalBloomPercentage === 100 ? 'success' : 'warning'" density="compact" variant="tonal"
                    class="mt-4 rounded-xl">
                    إجمالي النسبة: {{ totalBloomPercentage }}% (يجب أن يعادل 100%)
                  </v-alert>
                </v-window-item>

                <!-- Question Types -->
                <v-window-item :value="3">
                  <!-- Types Tab Header & Actions -->
                  <div class="units-tab-header d-flex justify-space-between align-center mb-5 flex-wrap gap-3">
                    <div class="d-flex align-center gap-3">
                      <div class="units-header-icon-box">
                        <v-icon size="26" color="primary">mdi-shape</v-icon>
                      </div>
                      <div>
                        <div class="d-flex align-center gap-2 flex-wrap">
                          <h3 class="text-subtitle-1 font-weight-black mb-0 text-high-emphasis">
                            توزيع أنواع الأسئلة ودرجات الاختبار
                          </h3>
                          <v-chip v-if="modelsMode === 'advanced'" size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                            تخصيص حسب المجموعات
                          </v-chip>
                        </div>
                        <p class="text-caption text-medium-emphasis mb-0 mt-0.5">
                          تحديد الدرجة النهائية للاختبار وتوزيع أوزان أنواع الأسئلة ودرجة كل سؤال
                        </p>
                      </div>
                    </div>

                    <!-- Global Action buttons -->
                    <div v-if="modelsMode === 'advanced'" class="d-flex align-center gap-2 flex-wrap">
                      <v-btn
                        variant="tonal"
                        color="secondary"
                        size="small"
                        class="font-weight-bold rounded-xl text-none px-4"
                        prepend-icon="mdi-equal-box"
                        @click="autoDistributeAllGroupsTypes"
                      >
                        توزيع متساوٍ للكل
                      </v-btn>
                      <v-btn
                        v-if="modelGroups.length > 1"
                        variant="outlined"
                        color="info"
                        size="small"
                        class="font-weight-bold rounded-xl text-none px-4"
                        prepend-icon="mdi-content-copy"
                        @click="copyCurrentGroupTypesToAll"
                      >
                        نسخ هذا التوزيع للباقي
                      </v-btn>
                    </div>
                    <v-btn
                      v-else
                      variant="tonal"
                      color="primary"
                      size="small"
                      class="font-weight-bold rounded-xl text-none px-4"
                      prepend-icon="mdi-scale-balance"
                      @click="() => autoDistributeCurrentGroupTypes()"
                    >
                      توزيع متساوٍ
                    </v-btn>
                  </div>

                  <!-- 🌟 Final Exam Total Score Command Card (Zero Gray) -->
                  <div class="exam-total-marks-card mb-5">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-4">
                      <div class="d-flex align-center gap-3">
                        <div class="total-marks-icon-box">
                          <v-icon size="28" color="amber-darken-2">mdi-star-circle</v-icon>
                        </div>
                        <div>
                          <div class="d-flex align-center gap-2 flex-wrap mb-1">
                            <span class="font-weight-black text-subtitle-1 text-high-emphasis">الدرجة النهائية للاختبار:</span>
                            <div class="d-flex align-center gap-1.5 ms-1">
                              <v-btn
                                v-for="scorePreset in [100, 60, 50, 40, 30]"
                                :key="scorePreset"
                                size="x-small"
                                :variant="exam.totalMarks === scorePreset ? 'flat' : 'outlined'"
                                :color="exam.totalMarks === scorePreset ? 'primary' : undefined"
                                class="font-weight-black px-2.5 rounded-lg font-mono text-none"
                                @click="setTotalMarks(scorePreset)"
                              >
                                {{ scorePreset }}
                              </v-btn>
                            </div>
                          </div>
                          <span class="text-caption text-medium-emphasis d-block">
                            إجمالي درجات الامتحان التي يتم احتساب درجات الطلاب بناءً عليها (مثلاً 100 أو 60 درجة)
                          </span>
                        </div>
                      </div>

                      <!-- Score Input & Quick Auto-Balance -->
                      <div class="d-flex align-center gap-3 flex-wrap">
                        <div class="score-input-wrapper d-flex align-center px-3 py-1.5 rounded-xl border-subtle">
                          <span class="text-caption text-medium-emphasis font-weight-bold me-2">الدرجة:</span>
                          <input
                            type="number"
                            v-model.number="exam.totalMarks"
                            min="1"
                            max="1000"
                            class="score-number-input font-weight-black font-mono"
                            @change="autoBalanceMarks"
                          />
                          <span class="text-caption text-medium-emphasis ms-1.5">درجة</span>
                        </div>

                        <!-- Distributed Marks Indicator -->
                        <div
                          class="hero-total-badge d-flex align-center gap-2 px-3 py-2 rounded-xl"
                          :class="currentGroupDistributedMarks === exam.totalMarks ? 'badge-success' : 'badge-warning'"
                        >
                          <div>
                            <div class="text-caption font-weight-bold opacity-80">الدرجات الموزعة</div>
                            <div class="font-weight-black text-h6 font-mono leading-none">
                              {{ currentGroupDistributedMarks }} / {{ exam.totalMarks }}
                            </div>
                          </div>
                          <v-icon size="22">{{ currentGroupDistributedMarks === exam.totalMarks ? 'mdi-check-decagram' : 'mdi-alert-circle-outline' }}</v-icon>
                        </div>

                        <v-btn
                          variant="tonal"
                          color="primary"
                          size="small"
                          class="font-weight-bold rounded-xl px-4"
                          prepend-icon="mdi-calculator-variant"
                          @click="autoBalanceMarks"
                        >
                          موازنة الدرجات تلقائياً
                        </v-btn>
                      </div>
                    </div>
                  </div>

                  <!-- Advanced Mode: Groups Tabs Selector (Zero Gray) -->
                  <div v-if="modelsMode === 'advanced'" class="model-groups-selector-hub mb-5">
                    <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                      <div class="d-flex align-center gap-2">
                        <div class="hub-bullet-dot"></div>
                        <span class="font-weight-black text-subtitle-2 text-high-emphasis">اختر مجموعة النماذج لتخصيص أنواع أسئلتها ودرجاتها:</span>
                        <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
                          {{ modelGroups.length }} مجموعات
                        </v-chip>
                      </div>
                      <span class="text-caption text-medium-emphasis d-flex align-center gap-1">
                        <v-icon size="14" color="primary">mdi-gesture-tap</v-icon>
                        انقر على أي مجموعة لتخصيص نسب ودرجات أنواع أسئلتها بشكل مستقل
                      </span>
                    </div>

                    <div class="group-pills-grid">
                      <div
                        v-for="(grp, gIdx) in modelGroups"
                        :key="gIdx"
                        class="group-switch-pill"
                        :class="{ 'is-active': activeTypeGroupIndex === gIdx }"
                        @click="selectTypeGroup(gIdx)"
                      >
                        <div class="d-flex align-center justify-space-between gap-2 mb-1.5">
                          <div class="d-flex align-center gap-2">
                            <v-icon size="20" :color="activeTypeGroupIndex === gIdx ? 'primary' : 'medium-emphasis'">
                              {{ activeTypeGroupIndex === gIdx ? 'mdi-folder-open' : 'mdi-folder-outline' }}
                            </v-icon>
                            <span class="group-pill-title font-weight-black">
                              {{ grp.name || ('المجموعة ' + (gIdx + 1)) }}
                            </span>
                          </div>
                          <v-chip
                            size="x-small"
                            :color="difficultyColor(grp.difficulty_profile)"
                            variant="tonal"
                            class="font-weight-bold"
                          >
                            {{ difficultyLabel(grp.difficulty_profile) }}
                          </v-chip>
                        </div>

                        <div class="d-flex align-center justify-space-between mt-2 pt-2 border-t-subtle text-caption">
                          <span class="text-medium-emphasis">
                            النماذج: <strong class="text-high-emphasis">{{ getGroupVersionCodes(gIdx) }}</strong>
                            ({{ grp.count || 1 }})
                          </span>
                          <span
                            class="font-weight-black font-mono pill-percentage-badge"
                            :class="getGroupTypesTotal(grp) === 100 ? 'is-complete' : 'is-pending'"
                          >
                            <v-icon size="12" start>{{ getGroupTypesTotal(grp) === 100 ? 'mdi-check' : 'mdi-clock-outline' }}</v-icon>
                            {{ getGroupTypesTotal(grp) }}% أسئلة
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Advanced Mode: Prominent Active Group Hero Command Banner -->
                  <div v-if="modelsMode === 'advanced'" class="active-group-hero-banner mb-5">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-4">
                      <div class="d-flex align-center gap-3">
                        <div class="active-group-hero-avatar">
                          <v-icon size="28" color="white">mdi-shape</v-icon>
                        </div>
                        <div>
                          <div class="d-flex align-center gap-2 flex-wrap mb-1">
                            <h4 class="text-subtitle-1 font-weight-black mb-0 text-primary">
                              أنواع أسئلة ودرجات: {{ currentTypeGroup ? (currentTypeGroup.name || ('المجموعة ' + (activeTypeGroupIndex + 1))) : '' }}
                            </h4>
                            <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
                              {{ getGroupVersionCodes(activeTypeGroupIndex) }} ({{ currentTypeGroup ? currentTypeGroup.count : 1 }} نماذج)
                            </v-chip>
                            <v-chip size="small" :color="difficultyColor(currentTypeGroup?.difficulty_profile)" variant="tonal" class="font-weight-bold">
                              {{ difficultyLabel(currentTypeGroup?.difficulty_profile) }}
                            </v-chip>
                          </div>
                          <span class="text-caption text-medium-emphasis d-block">
                            النسب والدرجات المحددة بالأسفل تنطبق حصرياً على نماذج هذه المجموعة
                          </span>
                        </div>
                      </div>

                      <div class="d-flex align-center gap-3 flex-wrap">
                        <div class="hero-total-badge d-flex align-center gap-2 px-3 py-2 rounded-xl"
                          :class="currentGroupTypesTotal === 100 ? 'badge-success' : 'badge-warning'">
                          <div>
                            <div class="text-caption font-weight-bold opacity-80">نسبة الأسئلة</div>
                            <div class="font-weight-black text-h6 font-mono leading-none">
                              {{ currentGroupTypesTotal }}%
                            </div>
                          </div>
                          <v-icon size="24">{{ currentGroupTypesTotal === 100 ? 'mdi-check-decagram' : 'mdi-alert-circle-outline' }}</v-icon>
                        </div>

                        <v-btn
                          variant="tonal"
                          color="primary"
                          size="small"
                          class="font-weight-bold rounded-xl px-4"
                          prepend-icon="mdi-scale-balance"
                          @click="autoDistributeCurrentGroupTypes"
                        >
                          توزيع متساوٍ للأسئلة
                        </v-btn>
                      </div>
                    </div>
                  </div>

                  <!-- Question Types Cards Grid (Modern with Marks & Counts) -->
                  <v-row dense>
                    <v-col
                      v-for="qType in currentActiveTypesList"
                      :key="'type-' + (qType.id || qType.value)"
                      cols="12"
                      md="6"
                    >
                      <div class="modern-type-card mb-3" :class="`border-accent-${qType.color || 'primary'}`">
                        <div class="d-flex justify-space-between align-start mb-3 gap-2">
                          <div class="d-flex align-center gap-3 flex-grow-1">
                            <v-avatar size="44" :color="qType.color || 'primary'" variant="tonal" class="rounded-xl flex-shrink-0">
                              <v-icon size="24" :color="qType.color || 'primary'">{{ qType.icon || 'mdi-help-circle-outline' }}</v-icon>
                            </v-avatar>
                            <div>
                              <div class="d-flex align-center gap-2 flex-wrap mb-0.5">
                                <span class="font-weight-black text-subtitle-2 text-high-emphasis">{{ qType.name }}</span>
                              </div>
                              <span class="text-caption text-medium-emphasis d-block">
                                {{ qType.subtitle || '' }}
                              </span>
                            </div>
                          </div>

                          <!-- Question Count % Stepper -->
                          <div class="d-flex align-center gap-1 unit-stepper-box flex-shrink-0">
                            <v-btn
                              icon="mdi-minus"
                              size="x-small"
                              variant="tonal"
                              :color="qType.color || 'primary'"
                              class="rounded-lg"
                              :disabled="(qType.percentage || 0) <= 0"
                              @click="adjustTypePercentage(qType.id || qType.value, -5)"
                            />
                            <div class="unit-percentage-display font-mono" :class="{ 'is-zero': !qType.percentage }">
                              {{ qType.percentage || 0 }}%
                            </div>
                            <v-btn
                              icon="mdi-plus"
                              size="x-small"
                              variant="tonal"
                              :color="qType.color || 'primary'"
                              class="rounded-lg"
                              :disabled="currentGroupTypesTotal >= 100"
                              @click="adjustTypePercentage(qType.id || qType.value, 5)"
                            />
                          </div>
                        </div>

                        <!-- 📊 Three Metrics Grid: Questions Count × Mark = Total Marks -->
                        <div class="type-metrics-bar d-flex align-center justify-space-between p-2 mb-2 rounded-xl">
                          <!-- Metric 1: Count of Questions -->
                          <div class="type-metric-item text-center flex-1">
                            <div class="text-caption text-medium-emphasis mb-0.5">عدد الأسئلة</div>
                            <div class="font-weight-black text-subtitle-2 font-mono text-high-emphasis">
                              {{ getTypeQuestionsCount(qType) }} سؤال
                            </div>
                          </div>

                          <div class="text-medium-emphasis font-weight-black px-1">×</div>

                          <!-- Metric 2: Mark per Question with Stepper -->
                          <div class="type-metric-item text-center flex-1">
                            <div class="text-caption text-medium-emphasis mb-0.5">درجة السؤال</div>
                            <div class="d-flex align-center justify-center gap-1">
                              <v-btn
                                icon="mdi-minus"
                                size="x-small"
                                variant="text"
                                color="medium-emphasis"
                                :disabled="(qType.mark || 1) <= 0.25"
                                @click="adjustTypeMark(qType.id || qType.value, -0.5)"
                              />
                              <span class="font-weight-black text-subtitle-2 font-mono text-primary px-1">
                                {{ qType.mark !== undefined ? qType.mark : 1 }} د
                              </span>
                              <v-btn
                                icon="mdi-plus"
                                size="x-small"
                                variant="text"
                                color="medium-emphasis"
                                @click="adjustTypeMark(qType.id || qType.value, 0.5)"
                              />
                            </div>
                          </div>

                          <div class="text-medium-emphasis font-weight-black px-1">=</div>

                          <!-- Metric 3: Total Marks for this Type -->
                          <div class="type-metric-item text-center flex-1">
                            <div class="text-caption text-medium-emphasis mb-0.5">إجمالي الدرجات</div>
                            <div class="font-weight-black text-subtitle-2 font-mono text-success">
                              {{ getTypeTotalMarks(qType) }} درجة
                            </div>
                          </div>
                        </div>

                        <!-- Custom Slider for percentage -->
                        <v-slider
                          :model-value="qType.percentage"
                          @update:model-value="(val) => updateTypePercentage(qType.id || qType.value, val)"
                          :min="0"
                          :max="100"
                          :step="5"
                          :color="qType.color || 'primary'"
                          track-color="rgba(var(--v-theme-primary), 0.12)"
                          hide-details
                          thumb-size="16"
                          track-size="6"
                          class="mt-1"
                        />
                      </div>
                    </v-col>
                  </v-row>

                  <!-- Bottom Combined Status Card (Questions % & Marks Balance) -->
                  <div
                    class="unit-balance-alert-card mt-4"
                    :class="(currentGroupTypesTotal === 100 && currentGroupDistributedMarks === exam.totalMarks) ? 'is-success' : 'is-warning'"
                  >
                    <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                      <div class="d-flex align-center gap-3">
                        <v-icon size="26" :color="(currentGroupTypesTotal === 100 && currentGroupDistributedMarks === exam.totalMarks) ? 'success' : 'warning'">
                          {{ (currentGroupTypesTotal === 100 && currentGroupDistributedMarks === exam.totalMarks) ? 'mdi-check-decagram' : 'mdi-alert-circle' }}
                        </v-icon>
                        <div>
                          <div class="font-weight-black text-subtitle-2 mb-0.5">
                            <template v-if="currentGroupTypesTotal === 100 && currentGroupDistributedMarks === exam.totalMarks">
                              توزيع الأسئلة والدرجات مكتمل تماماً ومطابق للمواصفات
                            </template>
                            <template v-else>
                              توزيع الأسئلة أو الدرجات يحتاج إلى موازنة
                            </template>
                          </div>
                          <span class="text-caption text-medium-emphasis">
                            <template v-if="currentGroupTypesTotal !== 100">
                              نسبة الأسئلة الحالية: <strong>{{ currentGroupTypesTotal }}%</strong> (يجب أن تعادل 100%).
                            </template>
                            <template v-if="currentGroupDistributedMarks !== exam.totalMarks">
                              مجموع الدرجات الموزعة: <strong>{{ currentGroupDistributedMarks }}</strong> من أصل <strong>{{ exam.totalMarks }}</strong> درجة
                              (الفارق: {{ Math.abs(exam.totalMarks - currentGroupDistributedMarks) }} درجة).
                            </template>
                            <template v-if="currentGroupTypesTotal === 100 && currentGroupDistributedMarks === exam.totalMarks">
                              تم توزيع 100% من الأسئلة و{{ exam.totalMarks }} درجة بنجاح ومطابقة للمواصفات الوزارية.
                            </template>
                          </span>
                        </div>
                      </div>

                      <div class="d-flex align-center gap-2 flex-wrap">
                        <v-btn
                          v-if="currentGroupTypesTotal !== 100"
                          variant="tonal"
                          color="warning"
                          size="small"
                          class="font-weight-bold rounded-xl text-none px-4"
                          prepend-icon="mdi-scale-balance"
                          @click="autoDistributeCurrentGroupTypes"
                        >
                          موازنة نسبة الأسئلة
                        </v-btn>
                        <v-btn
                          v-if="currentGroupDistributedMarks !== exam.totalMarks"
                          variant="tonal"
                          color="primary"
                          size="small"
                          class="font-weight-bold rounded-xl text-none px-4"
                          prepend-icon="mdi-calculator-variant"
                          @click="autoBalanceMarks"
                        >
                          موازنة الدرجات تلقائياً
                        </v-btn>
                      </div>
                    </div>
                  </div>
                </v-window-item>

              </v-window>
            </div>
          </v-window-item>

          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- STEP 3: PREVIEW & CONFIRMATION (EXECUTIVE DASHBOARD)            -->
          <!-- ════════════════════════════════════════════════════════════════ -->
          <v-window-item :value="3">
            <div class="d-flex align-center justify-space-between mb-6 flex-wrap gap-2">
              <div>
                <h3 class="text-h5 font-weight-black mb-1 d-flex align-center gap-2">
                  <v-icon color="success">mdi-clipboard-check-outline</v-icon>
                  المعاينة والتأكيد
                </h3>
                <span class="text-body-2 text-medium-emphasis">مراجعة تفاصيل ورقة الاختبار ومطابقة المواصفات قبل بدء التوليد</span>
              </div>

            </div>

            <!-- 4 Executive KPI Certification Cards -->
            <v-row dense class="mb-5">
              <!-- KPI Card 1: Academic Scope -->
              <v-col cols="12" sm="6" md="3">
                <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <span class="text-caption font-weight-bold text-medium-emphasis">المقرر والتصنيف</span>
                    <v-avatar size="34" color="primary" variant="tonal" class="rounded-lg">
                      <v-icon size="18">mdi-school</v-icon>
                    </v-avatar>
                  </div>
                  <div class="kpi-title font-weight-black text-truncate mb-1" :title="exam.title || 'اختبار بدون عنوان'">
                    {{ exam.title || 'اختبار بدون عنوان' }}
                  </div>
                  <div class="d-flex align-center gap-1 mb-2">
                    <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                      {{ exam.institution_type === 'school' ? 'تعليم مدرسي' : exam.institution_type === 'university' ? 'تعليم جامعي' : 'تعليم مهني' }}
                    </v-chip>
                  </div>
                  <span class="text-caption text-medium-emphasis d-block">السنة الدراسية والفترة معتمدة</span>
                </div>
              </v-col>

              <!-- KPI Card 2: Exam Capacity -->
              <v-col cols="12" sm="6" md="3">
                <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <span class="text-caption font-weight-bold text-medium-emphasis">سعة الاختبار ورصيد الأسئلة</span>
                    <v-avatar size="34" color="info" variant="tonal" class="rounded-lg">
                      <v-icon size="18">mdi-file-document-check</v-icon>
                    </v-avatar>
                  </div>
                  <div class="kpi-metric font-weight-black text-info mb-1">
                    {{ exam.questionsCount }} <span class="text-caption font-weight-bold text-medium-emphasis">سؤال معتمد</span>
                  </div>
                  <div class="d-flex align-center gap-1 mb-2">
                    <v-chip size="x-small" :color="exam.exclude_previously_used ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
                      <v-icon start size="12">mdi-shield-check</v-icon>
                      {{ exam.exclude_previously_used ? 'مكافحة التكرار نشطة' : 'السماح بالتكرار' }}
                    </v-chip>
                  </div>
                  <span class="text-caption text-medium-emphasis d-block">بلوم: {{ bloomEnabled ? 'مفعّل' : 'معطّل' }}</span>
                </div>
              </v-col>

              <!-- KPI Card 3: Models System -->
              <v-col cols="12" sm="6" md="3">
                <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <span class="text-caption font-weight-bold text-medium-emphasis">منظومة النماذج التوليدية</span>
                    <v-avatar size="34" color="warning" variant="tonal" class="rounded-lg">
                      <v-icon size="18">mdi-layers-triple</v-icon>
                    </v-avatar>
                  </div>
                  <div class="kpi-metric font-weight-black text-warning mb-1">
                    {{ totalModelsCount }} <span class="text-caption font-weight-bold text-medium-emphasis">نماذج فرعية</span>
                  </div>
                  <div class="d-flex align-center gap-1 mb-2">
                    <v-chip size="x-small" :color="modelsMode === 'advanced' ? 'warning' : 'success'" variant="tonal" class="font-weight-bold">
                      {{ modelsMode === 'advanced' ? 'نمط متقدم ومناطقي' : 'نمط موحد قياسي' }}
                    </v-chip>
                  </div>
                  <span class="text-caption text-medium-emphasis d-block">
                    {{ modelsMode === 'advanced' ? `${modelGroups.length} مجموعات صعوبة` : 'نماذج بنفس الأسئلة' }}
                  </span>
                </div>
              </v-col>

              <!-- KPI Card 4: Geographic Scope -->
              <v-col cols="12" sm="6" md="3">
                <div class="kpi-cert-card pa-4 rounded-2xl border-subtle h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <span class="text-caption font-weight-bold text-medium-emphasis">النطاق والانتشار الجغرافي</span>
                    <v-avatar size="34" color="deep-purple" variant="tonal" class="rounded-lg">
                      <v-icon size="18">mdi-map-marker-radius</v-icon>
                    </v-avatar>
                  </div>
                  <div class="kpi-metric font-weight-black text-deep-purple mb-1">
                    <span v-if="modelsMode === 'uniform' || isAllGroupsAllRegions">كافة المناطق</span>
                    <span v-else>{{ totalUniqueAssignedTargetsCount }} <span class="text-caption font-weight-bold text-medium-emphasis">منطقة مخصصة</span></span>
                  </div>
                  <div class="d-flex align-center gap-1 mb-2">
                    <v-chip size="x-small" color="deep-purple" variant="tonal" class="font-weight-bold">
                      {{ modelsMode === 'advanced' ? 'توزيع مناطقي بالمجموعات' : 'شامل عام' }}
                    </v-chip>
                  </div>
                  <span class="text-caption text-medium-emphasis d-block">تغطية النماذج حسب المجموعات</span>
                </div>
              </v-col>
            </v-row>

            <!-- Model Groups Summary (Advanced Mode) -->
            <div v-if="modelsMode === 'advanced'" class="section-group-card pa-5 rounded-2xl mb-5">
              <h4 class="text-subtitle-1 font-weight-black mb-3 d-flex align-center gap-2">
                <v-icon size="20" color="warning">mdi-file-multiple-outline</v-icon>
                شهادة اعتماد مجموعات النماذج والتوزيع المناطقي:
              </h4>
              <v-table density="compact" class="executive-table rounded-xl border-subtle">
                <thead>
                  <tr class="table-header-row">
                    <th class="font-weight-bold">المجموعة</th>
                    <th class="font-weight-bold">النماذج الفرعية</th>
                    <th class="font-weight-bold">تنوع الأسئلة</th>
                    <th class="font-weight-bold">ملف الصعوبة</th>
                    <th class="font-weight-bold">أوزان الصعوبة (سهل / متوسط / صعب)</th>
                    <th class="font-weight-bold">المناطق المخصصة</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(group, gIdx) in modelGroups" :key="gIdx">
                    <td class="font-weight-bold">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</td>
                    <td>
                      <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold font-mono">
                        {{ getGroupVersionCodes(gIdx) }} ({{ group.count }} نماذج)
                      </v-chip>
                    </td>
                    <td>
                      <v-chip
                        size="x-small"
                        :color="(group.questions_variation || 'same_scrambled') === 'different_questions' ? 'secondary' : 'primary'"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        <v-icon start size="14">
                          {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'mdi-layers-triple' : 'mdi-shuffle-variant' }}
                        </v-icon>
                        {{ (group.questions_variation || 'same_scrambled') === 'different_questions' ? 'أسئلة مستقلة' : 'نفس الأسئلة (خلط)' }}
                      </v-chip>
                    </td>
                    <td>
                      <v-chip size="x-small" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="font-weight-bold">
                        {{ difficultyLabel(group.difficulty_profile) }}
                      </v-chip>
                    </td>
                    <td class="text-caption">
                      <span class="text-success font-weight-bold">{{ group.difficulty_distribution.easy }}%</span> /
                      <span class="text-warning font-weight-bold">{{ group.difficulty_distribution.medium }}%</span> /
                      <span class="text-error font-weight-bold">{{ group.difficulty_distribution.hard }}%</span>
                    </td>
                    <td class="text-caption">
                      <span v-if="group.target_ids && group.target_ids.length > 0" class="font-weight-bold text-primary">
                        {{ getGroupTargetNames(group) }}
                      </span>
                      <span v-else-if="(group.scope_level || 'all') === 'all'" class="text-success font-weight-bold">
                        كافة المناطق (عام)
                      </span>
                      <span v-else class="text-medium-emphasis">غير مخصص</span>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>

            <!-- Distribution Summary Mini-Widgets -->
            <v-row dense>
              <v-col cols="12" md="4">
                <div class="section-group-card pa-4 rounded-2xl h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <h4 class="text-subtitle-2 font-weight-bold mb-0 d-flex align-center gap-2">
                      <v-icon size="18" color="primary">mdi-book-open-page-variant</v-icon>
                      توزيع الوحدات المعتمدة
                    </h4>
                    <v-chip size="x-small" :color="modelsMode === 'advanced' ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
                      {{ modelsMode === 'advanced' ? 'حسب المجموعات' : 'موحد' }}
                    </v-chip>
                  </div>

                  <template v-if="modelsMode === 'uniform'">
                    <div v-for="unit in blueprint.units.filter(u => u.percentage > 0)" :key="unit.id"
                      class="d-flex align-center justify-space-between py-1 border-b-subtle">
                      <span class="text-caption font-weight-bold text-truncate" style="max-width: 70%;">{{ unit.name }}</span>
                      <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">{{ unit.percentage }}%</v-chip>
                    </div>
                  </template>
                  <template v-else>
                    <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="py-2 border-b-subtle">
                      <div class="d-flex justify-space-between text-caption font-weight-bold mb-1">
                        <span class="text-primary">{{ group.name || ('المجموعة ' + (gIdx + 1)) }} ({{ group.count }} نماذج)</span>
                        <v-chip size="x-small" :color="getGroupUnitsTotal(group) === 100 ? 'success' : 'warning'" variant="tonal">
                          {{ getGroupUnitsTotal(group) }}%
                        </v-chip>
                      </div>
                      <div v-for="unit in (group.units && group.units.length > 0 ? group.units : blueprint.units).filter(u => u.percentage > 0)" :key="unit.id"
                        class="d-flex align-center justify-space-between py-0-5 text-caption">
                        <span class="text-truncate text-medium-emphasis" style="max-width: 70%;">{{ unit.name }}</span>
                        <span class="font-weight-bold">{{ unit.percentage }}%</span>
                      </div>
                    </div>
                  </template>
                </div>
              </v-col>

              <v-col cols="12" md="4">
                <div class="section-group-card pa-4 rounded-2xl h-100">
                  <div class="d-flex align-center justify-space-between mb-3">
                    <h4 class="text-subtitle-2 font-weight-bold mb-0 d-flex align-center gap-2">
                      <v-icon size="18" color="warning">mdi-speedometer</v-icon>
                      توزيع الصعوبة المعتمد
                    </h4>
                    <v-chip size="x-small" :color="modelsMode === 'advanced' ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
                      {{ modelsMode === 'advanced' ? 'متقدم' : 'موحد' }}
                    </v-chip>
                  </div>
                  <template v-if="modelsMode === 'uniform'">
                    <div v-for="level in blueprint.difficulty" :key="level.name"
                      class="d-flex align-center justify-space-between py-1 border-b-subtle">
                      <span class="text-caption font-weight-bold">{{ level.name }}</span>
                      <v-chip size="x-small" :color="level.color" variant="tonal" class="font-weight-bold">
                        {{ Math.round(exam.questionsCount * level.percentage / 100) }} ({{ level.percentage }}%)
                      </v-chip>
                    </div>
                  </template>
                  <template v-else>
                    <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="py-2 border-b-subtle">
                      <div class="d-flex justify-space-between text-caption font-weight-bold mb-1">
                        <span>{{ group.name || ('المجموعة ' + (gIdx + 1)) }} ({{ difficultyLabel(group.difficulty_profile) }})</span>
                        <v-chip size="x-small" color="primary" variant="tonal">{{ group.count }} نماذج</v-chip>
                      </div>
                      <div class="d-flex gap-1">
                        <v-chip size="x-small" color="success" variant="tonal">سهل {{ group.difficulty_distribution.easy }}%</v-chip>
                        <v-chip size="x-small" color="warning" variant="tonal">متوسط {{ group.difficulty_distribution.medium }}%</v-chip>
                        <v-chip size="x-small" color="error" variant="tonal">صعب {{ group.difficulty_distribution.hard }}%</v-chip>
                      </div>
                    </div>
                  </template>
                </div>
              </v-col>

              <v-col cols="12" md="4">
                <div class="section-group-card pa-4 rounded-2xl h-100">
                  <h4 class="text-subtitle-2 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon size="18" color="info">mdi-shape</v-icon>
                    توزيع أنواع الأسئلة
                  </h4>
                  <div v-if="modelsMode === 'advanced'">
                    <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="mb-2 pb-1 border-b-subtle">
                      <span class="text-caption font-weight-black text-primary d-block mb-1">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</span>
                      <div v-for="type in (group.types || []).filter(t => (t.percentage || 0) > 0)" :key="type.name"
                        class="d-flex align-center justify-space-between py-0.5 text-caption">
                        <span class="text-caption">{{ type.shortName || type.name }}</span>
                        <v-chip size="x-small" :color="type.color" variant="tonal" class="font-weight-bold">
                          {{ Math.round(exam.questionsCount * type.percentage / 100) }} ({{ type.percentage }}%)
                        </v-chip>
                      </div>
                    </div>
                  </div>
                  <div v-else>
                    <div v-for="type in (blueprint.types || []).filter(t => (t.percentage || 0) > 0)" :key="type.name"
                      class="d-flex align-center justify-space-between py-1 border-b-subtle">
                      <span class="text-caption font-weight-bold">{{ type.shortName || type.name }}</span>
                      <v-chip size="x-small" :color="type.color" variant="tonal" class="font-weight-bold">
                        {{ Math.round(exam.questionsCount * type.percentage / 100) }} ({{ type.percentage }}%)
                      </v-chip>
                    </div>
                  </div>
                </div>
              </v-col>
            </v-row>

            <!-- Call to Action Banner to Step 4 (مسودة استعراض النماذج) -->
            <div class="mt-6 pa-5 rounded-2xl border-subtle d-flex align-center justify-space-between flex-wrap gap-4"
              style="background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%); border: 1.5px solid rgba(var(--v-theme-primary), 0.2);">
              <div class="d-flex align-center gap-3">
                <v-avatar size="48" color="primary" variant="tonal" class="rounded-xl">
                  <v-icon size="26" color="primary">mdi-file-document-edit-outline</v-icon>
                </v-avatar>
                <div>
                  <h4 class="text-subtitle-1 font-weight-black mb-0 text-high-emphasis">
                    المرحلة الرابعة: مسودة استعراض وضبط نماذج الاختبار
                  </h4>
                  <p class="text-caption text-medium-emphasis mb-0 mt-0.5">
                    سيتم سحب الأسئلة من البنك وعرض كافة النماذج في بيئة تفاعلية تتيح لك مراجعة الأسئلة واستبدالها أو إنشاء أسئلة جديدة قبل الاعتماد النهائي.
                  </p>
                </div>
              </div>
              <v-btn
                color="primary"
                size="large"
                class="font-weight-black rounded-xl px-6 elevation-2"
                prepend-icon="mdi-arrow-left"
                :loading="stagingLoading"
                @click="nextStep"
              >
                الانتقال لمسودة واستعراض النماذج
              </v-btn>
            </div>
          </v-window-item>

          <!-- ═════════════════════════════════════════════════════════════════════ -->
          <!-- STEP 4: INTERACTIVE EXAM STAGING & MODEL COMPOSER (المسودة التفاعلية) -->
          <!-- ═════════════════════════════════════════════════════════════════════ -->
          <v-window-item :value="4">
            <!-- Staging Loading Pulse -->
            <div v-if="stagingLoading" class="py-16 text-center">
              <v-progress-circular indeterminate color="primary" size="64" width="4" />
              <h3 class="text-h6 font-weight-black mt-4 text-high-emphasis">جاري تحضير المسودة التفاعلية لنماذج الاختبار...</h3>
              <p class="text-caption text-medium-emphasis mt-1">يتم سحب وتوزيع الأسئلة وفق محددات مصفوفة المعايير والمجموعات</p>
            </div>

            <div v-else-if="!stagedModels || stagedModels.length === 0" class="py-16 text-center">
              <v-icon size="64" color="warning" class="mb-3">mdi-alert-circle-outline</v-icon>
              <h3 class="text-h6 font-weight-bold">لم يتم تجهيز مسودة النماذج بعد</h3>
              <p class="text-caption text-medium-emphasis mb-4">يرجى الرجوع للخطوة السابقة وتأكيد الانتقال للمسودة التفاعلية</p>
              <v-btn color="primary" variant="tonal" class="font-weight-bold rounded-xl" @click="step = 3">
                العودة للمعاينة والتأكيد
              </v-btn>
            </div>

            <div v-else>
              <!-- 🌟 Staged Hero Banner (Zero Gray) -->
              <div class="staged-hero-banner pa-5 mb-5 d-flex align-center justify-space-between flex-wrap gap-4">
                <div class="d-flex align-center gap-3">
                  <div class="staged-hero-icon-box">
                    <v-icon size="28" color="primary">mdi-file-document-edit-outline</v-icon>
                  </div>
                  <div>
                    <div class="d-flex align-center gap-2 flex-wrap">
                      <h2 class="text-h6 font-weight-black mb-0 text-high-emphasis">
                        استعراض وضبط أسئلة نماذج الاختبار
                      </h2>
                      <v-chip size="small" color="primary" variant="tonal" class="font-weight-black">
                        مسودة تفاعلية ذكية
                      </v-chip>
                      <v-chip size="small" color="success" variant="tonal" class="font-weight-bold">
                        لم يتم الحفظ في القاعدة بعد
                      </v-chip>
                    </div>
                    <p class="text-caption text-medium-emphasis mb-0 mt-1">
                      يمكنك معاينة الأسئلة لكل نموذج، وتبديل أي سؤال فورياً، أو اختياره من البنك، أو صياغة سؤال بديل جديد مع خياراته قبل الاعتماد الرسمي.
                    </p>
                  </div>
                </div>

                <div class="d-flex align-center gap-2 flex-wrap">
                  <v-btn
                    variant="tonal"
                    color="primary"
                    size="small"
                    class="font-weight-bold rounded-xl text-none px-4"
                    prepend-icon="mdi-refresh"
                    :loading="stagingLoading"
                    @click="prepareStagingAndProceed"
                  >
                    إعادة توليد عشوائي للمسودة
                  </v-btn>
                  <v-btn
                    color="success"
                    size="default"
                    class="font-weight-black rounded-xl px-6 shadow-success text-none"
                    prepend-icon="mdi-check-decagram"
                    :loading="generating"
                    @click="commitFinalExam"
                  >
                    اعتماد وتوليد الاختبار النهائي (تثبيت رسمي)
                  </v-btn>
                </div>
              </div>

              <!-- Model Selector Pills Hub (Zero Gray) -->
              <div class="section-group-card pa-4 rounded-2xl border-subtle mb-5">
                <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-3 pb-3 border-b-subtle">
                  <div class="d-flex align-center gap-2">
                    <v-icon size="20" color="primary">mdi-view-carousel-outline</v-icon>
                    <span class="font-weight-black text-subtitle-2">نماذج الاختبار المتاحة للمراجعة والتحكيم:</span>
                    <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                      {{ stagedModels.length }} نماذج معتمدة
                    </v-chip>
                  </div>
                  <div class="d-flex align-center gap-3">
                    <v-switch
                      v-model="showCorrectAnswers"
                      color="success"
                      hide-details
                      density="compact"
                      label="إظهار الإجابات الصحيحة"
                      class="ma-0 pa-0 font-weight-bold"
                    />
                  </div>
                </div>

                <!-- Model Pills List -->
                <div class="d-flex align-center flex-wrap gap-2">
                  <div
                    v-for="(model, mIdx) in stagedModels"
                    :key="mIdx"
                    class="staged-version-pill"
                    :class="{ 'is-active': activeStagedModelIndex === mIdx }"
                    @click="activeStagedModelIndex = mIdx"
                  >
                    <v-avatar size="28" :color="activeStagedModelIndex === mIdx ? 'primary' : 'surface-variant'" class="font-weight-black text-caption">
                      {{ model.versionCode }}
                    </v-avatar>
                    <div class="d-flex flex-column text-start">
                      <span class="font-weight-black text-body-2">
                        النموذج ({{ model.versionCode }})
                      </span>
                      <span class="text-caption text-medium-emphasis" style="font-size: 0.72rem;">
                        {{ model.group_name || ('المجموعة ' + (Number(model.model_group_index || 0) + 1)) }} &bull; {{ model.questions_variation === 'different_questions' ? 'أسئلة مستقلة' : 'خلط' }} &bull; {{ model.questions?.length || 0 }} سؤال
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Active Model Control & Key Stats Strip -->
              <div v-if="currentStagedModel" class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4 pa-3 rounded-xl border-subtle bg-surface">
                <div class="d-flex align-center gap-3 flex-wrap">
                  <span class="font-weight-black text-subtitle-2 text-primary">
                    محتويات النموذج: ({{ currentStagedModel.versionCode }})
                  </span>
                  <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                    {{ currentStagedModel.questions?.length || 0 }} / {{ exam.questionsCount }} سؤال
                  </v-chip>
                  <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                    إجمالي الدرجات: {{ calculateStagedTotalMarks(currentStagedModel) }} / {{ exam.totalMarks || 100 }} درجة
                  </v-chip>
                  <v-chip size="small" :color="difficultyColor(currentStagedModel.difficulty_profile)" variant="tonal" class="font-weight-bold">
                    صعوبة النموذج: {{ difficultyLabel(currentStagedModel.difficulty_profile) }}
                  </v-chip>
                  <v-chip
                    size="small"
                    :color="currentStagedModel.questions_variation === 'different_questions' ? 'secondary' : 'primary'"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    <v-icon start size="14">
                      {{ currentStagedModel.questions_variation === 'different_questions' ? 'mdi-layers-triple' : 'mdi-shuffle-variant' }}
                    </v-icon>
                    {{ currentStagedModel.questions_variation === 'different_questions' ? 'أسئلة مستقلة' : 'نفس الأسئلة (خلط وترتيب)' }}
                  </v-chip>
                </div>
                <div class="text-caption text-medium-emphasis">
                  انقر على أي سؤال لاستبداله أو تعديله فورياً
                </div>
              </div>

              <!-- Questions List for Current Staged Model -->
              <div v-if="currentStagedModel && currentStagedModel.questions" class="d-flex flex-column gap-3 mb-6">
                <div
                  v-for="(q, qIdx) in currentStagedModel.questions"
                  :key="q.id || qIdx"
                  class="staged-question-card pa-4 rounded-2xl border-subtle"
                >
                  <!-- Card Header Bar -->
                  <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
                    <div class="d-flex align-center gap-2 flex-wrap">
                      <v-chip size="small" color="primary" variant="flat" class="font-weight-black font-mono">
                        سؤال #{{ q.orderIndex || (qIdx + 1) }}
                      </v-chip>
                      <v-chip size="small" :color="questionTypeColor(q.questionType)" variant="tonal" class="font-weight-bold">
                        <v-icon start size="14">{{ questionTypeIcon(q.questionType) }}</v-icon>
                        {{ questionTypeLabel(q.questionType) }}
                      </v-chip>
                      <v-chip size="small" :color="difficultyColor(q.difficulty)" variant="tonal" class="font-weight-bold">
                        {{ difficultyLabel(q.difficulty) }}
                      </v-chip>
                      <v-chip v-if="q.unitName" size="small" color="secondary" variant="tonal" class="font-weight-medium">
                        {{ q.unitName }}
                      </v-chip>
                      <v-chip size="small" color="info" variant="tonal" class="font-weight-black">
                        {{ q.assignedMark }} درجة
                      </v-chip>
                    </div>

                    <!-- Question Action Tools (Swap / Browse / Quick Create) -->
                    <div class="d-flex align-center gap-1 flex-wrap">
                      <v-btn
                        size="small"
                        variant="tonal"
                        color="primary"
                        class="font-weight-bold rounded-lg text-none px-3"
                        prepend-icon="mdi-swap-horizontal"
                        @click="quickAutoSwap(q, activeStagedModelIndex)"
                      >
                        استبدال فوري
                      </v-btn>
                      <v-btn
                        size="small"
                        variant="tonal"
                        color="secondary"
                        class="font-weight-bold rounded-lg text-none px-3"
                        prepend-icon="mdi-database-search"
                        @click="openSwapDialog(q, activeStagedModelIndex)"
                      >
                        اختيار من البنك
                      </v-btn>
                      <v-btn
                        size="small"
                        variant="tonal"
                        color="success"
                        class="font-weight-bold rounded-lg text-none px-3"
                        prepend-icon="mdi-plus-circle-outline"
                        @click="openQuickCreateDialog(q, activeStagedModelIndex)"
                      >
                        إنشاء بديل جديد
                      </v-btn>
                    </div>
                  </div>

                  <!-- Question Text Content -->
                  <div class="text-body-1 font-weight-bold mb-3 text-high-emphasis pe-2" style="line-height: 1.6;">
                    {{ q.content }}
                  </div>

                  <!-- Optional Question Image -->
                  <div v-if="q.image" class="mb-3">
                    <img :src="q.image" alt="Question Image" style="max-height: 200px; border-radius: 12px; border: 1px solid rgba(var(--v-theme-primary), 0.15);" />
                  </div>

                  <!-- Question Options (For Single Choice & Multi Choice) -->
                  <div v-if="q.options && q.options.length > 0" class="d-flex flex-column gap-2 mt-2">
                    <div
                      v-for="(opt, optIdx) in q.options"
                      :key="opt.id || optIdx"
                      class="staged-option-item pa-2.5 px-3 rounded-xl d-flex align-center justify-space-between gap-2"
                      :class="{ 'is-correct-option': showCorrectAnswers && opt.isTrue }"
                    >
                      <div class="d-flex align-center gap-2">
                        <span class="font-weight-black font-mono text-body-2" style="min-width: 24px;">
                          {{ String.fromCharCode(1571 + optIdx) }})
                        </span>
                        <span class="text-body-2">{{ opt.text }}</span>
                      </div>
                      <v-chip v-if="showCorrectAnswers && opt.isTrue" size="x-small" color="success" variant="flat" class="font-weight-black">
                        <v-icon start size="12">mdi-check</v-icon>
                        الإجابة الصحيحة
                      </v-chip>
                    </div>
                  </div>

                  <!-- True / False Indicator -->
                  <div v-else-if="q.questionType === 'True/False' || q.questionType === 'صح وخطأ'" class="d-flex align-center gap-2 mt-2">
                    <span class="text-caption font-weight-bold text-medium-emphasis">الإجابة المعتمدة:</span>
                    <v-chip v-if="showCorrectAnswers" size="small" :color="q.isTrue ? 'success' : 'error'" variant="tonal" class="font-weight-black">
                      <v-icon start size="14">{{ q.isTrue ? 'mdi-check' : 'mdi-close' }}</v-icon>
                      {{ q.isTrue ? 'صواب (True)' : 'خطأ (False)' }}
                    </v-chip>
                  </div>
                </div>
              </div>
            </div>
          </v-window-item>
        </v-window>
      </div>

      <!-- Stepper Action Buttons Footer (Sticky) -->
      <div class="px-6 py-4 border-t border-subtle d-flex align-center justify-space-between wizard-footer"
        style="position: sticky; bottom: 0; background: rgb(var(--v-theme-surface)); z-index: 99; box-shadow: 0 -10px 30px rgba(0,0,0,0.05); border-bottom-left-radius: 16px; border-bottom-right-radius: 16px;">
        <v-btn variant="tonal" color="medium-emphasis" class="font-weight-bold px-5" rounded="lg" :disabled="step === 1 || generating"
          @click="step--">
          <v-icon start size="18">mdi-arrow-right</v-icon>
          السابق
        </v-btn>

        <div class="d-none d-sm-flex align-center gap-2">
          <span class="text-caption font-weight-bold text-medium-emphasis">
            خطوة {{ step }} من 4
          </span>
        </div>

        <v-btn
          v-if="step < 3"
          color="primary"
          class="font-weight-bold px-8"
          rounded="lg"
          elevation="2"
          @click="nextStep"
        >
          <v-icon start size="20">mdi-arrow-left</v-icon>
          التالي
        </v-btn>

        <v-btn
          v-else-if="step === 3"
          color="primary"
          class="font-weight-bold px-8"
          rounded="lg"
          elevation="2"
          :loading="stagingLoading"
          @click="nextStep"
        >
          <v-icon start size="20">mdi-file-document-edit-outline</v-icon>
          الانتقال لمسودة واستعراض النماذج
        </v-btn>

        <v-btn
          v-else-if="step === 4"
          color="success"
          class="font-weight-bold px-8 shadow-success"
          rounded="lg"
          elevation="3"
          size="large"
          :loading="generating"
          @click="commitFinalExam"
        >
          <v-icon start size="20">mdi-check-decagram</v-icon>
          اعتماد وتوليد الاختبار النهائي (تثبيت رسمي)
        </v-btn>
      </div>
    </div>
    <CustomDialog v-model="shortageDialog" width="650" title="تقرير عجز الأسئلة المعتمدة"
      subTitle="نقص في بعض المستويات مقارنة بالمصفوفة المطلوبة">
      <p class="text-body-2 text-medium-emphasis mb-3">
        يوجد نقص في رصيد الأسئلة المعتمدة المتوفرة ببنك الأسئلة للمادة المحددة مقارنة باحتياجات المصفوفة:
      </p>

      <v-table density="compact" class="rounded-xl border-subtle mb-4">
        <thead>
          <tr class="bg-surface-variant">
            <th class="font-weight-bold">المعيار المطلوب</th>
            <th class="font-weight-bold text-center">المطلوب</th>
            <th class="font-weight-bold text-center">المتوفر</th>
            <th class="font-weight-bold text-center">العجز</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="shortageReport.mcq && shortageReport.mcq.missing > 0">
            <td><v-icon size="14" color="primary" class="me-1">mdi-radiobox-marked</v-icon> اختيار من متعدد (MCQ)</td>
            <td class="text-center">{{ shortageReport.mcq.required }}</td>
            <td class="text-center text-success font-weight-bold">{{ shortageReport.mcq.available }}</td>
            <td class="text-center text-error font-weight-bold">-{{ shortageReport.mcq.missing }}</td>
          </tr>
          <tr v-if="shortageReport.tf && shortageReport.tf.missing > 0">
            <td><v-icon size="14" color="success" class="me-1">mdi-check-circle-outline</v-icon> صح وخطأ (True/False)</td>
            <td class="text-center">{{ shortageReport.tf.required }}</td>
            <td class="text-center text-success font-weight-bold">{{ shortageReport.tf.available }}</td>
            <td class="text-center text-error font-weight-bold">-{{ shortageReport.tf.missing }}</td>
          </tr>
          <tr v-if="shortageReport.easy && shortageReport.easy.missing > 0">
            <td><v-icon size="14" color="success" class="me-1">mdi-speedometer-slow</v-icon> مستوى سهل</td>
            <td class="text-center">{{ shortageReport.easy.required }}</td>
            <td class="text-center text-success font-weight-bold">{{ shortageReport.easy.available }}</td>
            <td class="text-center text-error font-weight-bold">-{{ shortageReport.easy.missing }}</td>
          </tr>
          <tr v-if="shortageReport.medium && shortageReport.medium.missing > 0">
            <td><v-icon size="14" color="warning" class="me-1">mdi-speedometer-medium</v-icon> مستوى متوسط</td>
            <td class="text-center">{{ shortageReport.medium.required }}</td>
            <td class="text-center text-success font-weight-bold">{{ shortageReport.medium.available }}</td>
            <td class="text-center text-error font-weight-bold">-{{ shortageReport.medium.missing }}</td>
          </tr>
          <tr v-if="shortageReport.hard && shortageReport.hard.missing > 0">
            <td><v-icon size="14" color="error" class="me-1">mdi-speedometer</v-icon> مستوى صعب</td>
            <td class="text-center">{{ shortageReport.hard.required }}</td>
            <td class="text-center text-success font-weight-bold">{{ shortageReport.hard.available }}</td>
            <td class="text-center text-error font-weight-bold">-{{ shortageReport.hard.missing }}</td>
          </tr>
          <tr v-if="shortageReport.totalMissing > 0" :style="'background: rgba(var(--v-theme-error), 0.08);'">
            <td class="font-weight-black text-error">إجمالي النقص العام للأسئلة</td>
            <td class="text-center font-weight-bold">{{ shortageReport.totalRequired }}</td>
            <td class="text-center font-weight-bold text-success">{{ shortageReport.totalAvailable }}</td>
            <td class="text-center font-weight-black text-error">-{{ shortageReport.totalMissing }}</td>
          </tr>
        </tbody>
      </v-table>

      <v-alert type="error" variant="tonal" density="compact" class="mb-4 rounded-xl">
        <v-icon start size="18">mdi-alert-octagon</v-icon>
        <strong>تنبيه وزاري ملزم:</strong> لا يمكن المتابعة أو توليد الاختبار طالما يوجد عجز في رصيد الأسئلة المعتمدة لضمان تحقيق الجودة والعدالة الامتحانية. يرجى تعديل نسب المصفوفة أو تغذية بنك الأسئلة بالأسئلة المطلوبة أولاً.
      </v-alert>

      <template #actions>
        <v-btn variant="text" color="medium-emphasis" class="font-weight-bold" @click="shortageDialog = false">
          إغلاق
        </v-btn>
        <v-btn variant="tonal" color="primary" class="font-weight-bold rounded-lg" @click="shortageDialog = false; step = 2">
          <v-icon start size="16">mdi-cog-outline</v-icon>
          الرجوع للمصفوفة لتعديل النسب
        </v-btn>
        <v-btn variant="flat" color="info" class="font-weight-bold rounded-lg" @click="goToAddQuestion()">
          <v-icon start size="16">mdi-plus-circle-outline</v-icon>
          إضافة أسئلة بالبنك
        </v-btn>
      </template>
    </CustomDialog>

    <!-- ═══════════════════════════════════════════════════════════════ -->
    <!-- QUESTION BANK REPLACEMENT DIALOG (استبدال يدوي من البنك)       -->
    <!-- ═══════════════════════════════════════════════════════════════ -->
    <CustomDialog v-model="swapDialog" width="850" title="اختيار سؤال بديل من بنك الأسئلة"
      subTitle="يتم استعراض الأسئلة المعتمدة المتوافقة مع معايير السؤال الحالي">
      <div v-if="targetSwapQuestion" class="pa-1">
        <!-- Target Question Summary Banner -->
        <div class="pa-3 rounded-xl border-subtle mb-4 bg-surface-variant d-flex align-center justify-space-between flex-wrap gap-2">
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
              السؤال المستهدف: #{{ targetSwapQuestion.orderIndex }}
            </v-chip>
            <v-chip size="small" :color="questionTypeColor(targetSwapQuestion.questionType)" variant="tonal" class="font-weight-bold">
              {{ questionTypeLabel(targetSwapQuestion.questionType) }}
            </v-chip>
            <v-chip size="small" :color="difficultyColor(targetSwapQuestion.difficulty)" variant="tonal" class="font-weight-bold">
              {{ difficultyLabel(targetSwapQuestion.difficulty) }}
            </v-chip>
            <v-chip size="small" color="secondary" variant="tonal">
              {{ targetSwapQuestion.unitName }}
            </v-chip>
          </div>
          <span class="text-caption text-medium-emphasis">الدرجة: {{ targetSwapQuestion.assignedMark }}</span>
        </div>

        <!-- Search Bar -->
        <div class="d-flex align-center gap-2 mb-4">
          <v-text-field
            v-model="swapSearchQuery"
            density="compact"
            variant="outlined"
            placeholder="البحث بنص السؤال في بنك الأسئلة..."
            hide-details
            clearable
            prepend-inner-icon="mdi-magnify"
            class="flex-grow-1"
            @keyup.enter="searchSwapCandidates"
          />
          <v-btn color="primary" variant="tonal" :loading="swapLoading" class="font-weight-bold" @click="searchSwapCandidates">
            بحث
          </v-btn>
        </div>

        <!-- Candidate Questions List -->
        <div v-if="swapLoading" class="py-10 text-center">
          <v-progress-circular indeterminate color="primary" size="40" />
          <p class="text-caption text-medium-emphasis mt-2">جاري البحث عن الأسئلة البديلة المطابقة...</p>
        </div>
        <div v-else-if="swapCandidates.length === 0" class="py-8 text-center">
          <v-icon size="48" color="warning" class="mb-2">mdi-alert-circle-outline</v-icon>
          <div class="text-subtitle-1 font-weight-bold">لم يتم العثور على أسئلة بديلة مطابقة تماماً في البنك</div>
          <p class="text-caption text-medium-emphasis mt-1 mb-4">
            يمكنك إنشاء سؤال بديل جديد فوراً وإدراجه في هذا الموضع.
          </p>
          <v-btn color="primary" variant="flat" class="font-weight-bold rounded-lg" @click="openQuickCreateFromSwap">
            <v-icon start size="16">mdi-plus</v-icon>
            إنشاء سؤال بديل جديد فوراً
          </v-btn>
        </div>
        <div v-else class="d-flex flex-column gap-3" style="max-height: 420px; overflow-y: auto;">
          <div
            v-for="cand in swapCandidates"
            :key="cand.id"
            class="pa-4 rounded-xl border-subtle d-flex flex-column gap-2"
          >
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-chip size="x-small" :color="questionTypeColor(cand.questionType)" variant="tonal" class="font-weight-bold">
                  {{ questionTypeLabel(cand.questionType) }}
                </v-chip>
                <v-chip size="x-small" :color="difficultyColor(cand.difficulty)" variant="tonal" class="font-weight-bold">
                  {{ difficultyLabel(cand.difficulty) }}
                </v-chip>
                <span class="text-caption text-medium-emphasis">{{ cand.unitName }} - {{ cand.lessonName }}</span>
              </div>
              <v-btn size="small" color="success" variant="flat" class="font-weight-bold rounded-lg" @click="applyReplacement(cand)">
                <v-icon start size="16">mdi-check</v-icon>
                اختيار هذا البديل
              </v-btn>
            </div>
            <div class="font-weight-bold text-body-2 mt-1">{{ cand.content }}</div>
            <div v-if="cand.options && cand.options.length > 0" class="d-flex flex-wrap gap-2 mt-1">
              <v-chip
                v-for="(opt, oIdx) in cand.options"
                :key="oIdx"
                size="x-small"
                :color="opt.isTrue ? 'success' : undefined"
                :variant="opt.isTrue ? 'flat' : 'tonal'"
              >
                {{ String.fromCharCode(1571 + oIdx) }}: {{ opt.text }}
              </v-chip>
            </div>
          </div>
        </div>
      </div>
      <template #actions>
        <v-btn variant="text" color="medium-emphasis" class="font-weight-bold" @click="swapDialog = false">
          إغلاق
        </v-btn>
      </template>
    </CustomDialog>

    <!-- ═══════════════════════════════════════════════════════════════ -->
    <!-- QUICK CREATE QUESTION DIALOG (إنشاء سؤال فوري وإدراجه)        -->
    <!-- ═══════════════════════════════════════════════════════════════ -->
    <CustomDialog v-model="quickCreateDialog" width="750" title="إنشاء سؤال بديل جديد وإدراجه فورياً"
      subTitle="سيتم حفظ السؤال في بنك الأسئلة كمعتمد وإدراجه مباشرة في النموذج الحالي">
      <div class="pa-1">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="quickCreateForm.unitName"
              label="الوحدة الدراسية"
              density="compact"
              variant="outlined"
              readonly
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="quickCreateForm.difficulty"
              :items="[
                { title: 'سهل', value: 1 },
                { title: 'متوسط', value: 2 },
                { title: 'صعب', value: 3 }
              ]"
              label="مستوى الصعوبة"
              density="compact"
              variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="quickCreateForm.questionType"
              :items="[
                { title: 'اختيار من متعدد (Single Choice)', value: 'Single Choice' },
                { title: 'صح وخطأ (True/False)', value: 'True/False' },
                { title: 'سؤال مقالي (Essay)', value: 'Essay' },
                { title: 'إكمال الفراغ (Fill Blanks)', value: 'Fill in the Blanks' }
              ]"
              label="نوع السؤال"
              density="compact"
              variant="outlined"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model.number="quickCreateForm.defaultMark"
              label="درجة السؤال"
              type="number"
              step="0.5"
              min="0.5"
              density="compact"
              variant="outlined"
            />
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="quickCreateForm.content"
              label="نص السؤال *"
              rows="3"
              density="compact"
              variant="outlined"
              placeholder="اكتب صياغة السؤال هنا بدقة..."
            />
          </v-col>
        </v-row>

        <!-- Options for Choice Questions -->
        <div v-if="quickCreateForm.questionType === 'Single Choice'" class="mt-3">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="font-weight-bold text-subtitle-2">خيارات الإجابة (حدد الإجابة الصحيحة):</span>
            <v-btn size="x-small" color="primary" variant="tonal" prepend-icon="mdi-plus" @click="addQuickOption">
              إضافة خيار
            </v-btn>
          </div>
          <div class="d-flex flex-column gap-2">
            <div
              v-for="(opt, optIdx) in quickCreateForm.options"
              :key="optIdx"
              class="d-flex align-center gap-2 pa-2 rounded-xl border-subtle"
              :class="{ 'border-success': opt.isTrue }"
              :style="opt.isTrue ? 'background: rgba(16, 185, 129, 0.08);' : ''"
            >
              <v-radio
                :model-value="opt.isTrue"
                color="success"
                hide-details
                density="compact"
                class="ma-0"
                @click="setQuickCorrectOption(optIdx)"
              />
              <span class="font-weight-bold font-mono">{{ String.fromCharCode(1571 + optIdx) }})</span>
              <v-text-field
                v-model="opt.text"
                density="compact"
                variant="plain"
                placeholder="نص الخيار..."
                hide-details
                class="flex-grow-1"
              />
              <v-btn
                v-if="quickCreateForm.options.length > 2"
                size="x-small"
                icon="mdi-trash-can-outline"
                variant="text"
                color="error"
                @click="removeQuickOption(optIdx)"
              />
            </div>
          </div>
        </div>

        <!-- Options for True/False Questions -->
        <div v-else-if="quickCreateForm.questionType === 'True/False'" class="mt-3">
          <span class="font-weight-bold text-subtitle-2 d-block mb-2">الإجابة الصحيحة:</span>
          <v-radio-group v-model="quickCreateForm.tfAnswer" inline hide-details>
            <v-radio label="صواب (True)" :value="true" color="success" />
            <v-radio label="خطأ (False)" :value="false" color="error" class="ms-4" />
          </v-radio-group>
        </div>
      </div>

      <template #actions>
        <v-btn variant="text" color="medium-emphasis" class="font-weight-bold" @click="quickCreateDialog = false">
          إلغاء
        </v-btn>
        <v-btn
          color="success"
          variant="flat"
          class="font-weight-bold rounded-lg"
          :loading="quickCreateLoading"
          @click="submitQuickCreateQuestion"
        >
          <v-icon start size="16">mdi-content-save-check</v-icon>
          حفظ وتضمين في النموذج فوراً
        </v-btn>
      </template>
    </CustomDialog>

    <!-- Unit Details Dialog -->
    <CustomDialog v-model="unitDetailsDialog.show" width="550" :title="(exam.institution_type === 'university' ? 'محتوى مفردة المقرر: ' : 'محتوى الوحدة: ') + unitDetailsDialog.unitName">
      <div v-if="unitDetailsDialog.lessons.length > 0" class="d-flex flex-column gap-2 mb-4">
        <div v-for="(lesson, i) in unitDetailsDialog.lessons" :key="i"
          class="d-flex align-center justify-space-between pa-3 rounded-xl border-subtle">
          <div>
            <div class="font-weight-bold text-subtitle-2">{{ lesson.name }}</div>
            <span class="text-caption text-medium-emphasis">{{ lesson.questionsCount }} سؤال معتمد</span>
          </div>
          <custom-btn label="إضافة سؤال" variant="tonal" color="primary" class="font-weight-bold"
            :click="() => goToAddQuestion(unitDetailsDialog.unitId, lesson.id)" />
        </div>
      </div>
      <div v-else class="text-center text-medium-emphasis pa-6">
        لا توجد دروس مضافة لهذه الوحدة بعد
      </div>
    </CustomDialog>


  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, getCurrentInstance } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDataStore } from '@/stores/dataStore'
import { useTheme } from 'vuetify'
import { rules } from '@/utils/validations'
import { examsService } from '@/services/examsService'
import { academicService } from '@/services/academicService'
import api from '@/services/api'

const { proxy } = getCurrentInstance()
const router = useRouter()
const route = useRoute()

// Edit Exam Mode States
const isEditing = ref(false)
const editingExamId = ref(null)
const editingExamCode = ref('')
const isLoadingForEdit = ref(Boolean(route.query.edit_exam_id))
const store = useDataStore()
const theme = useTheme()

const requiredRule = [rules.required]

// Stepper Step Indicator Config - NOW 3 STEPS
const step = ref(1)
const step1Form = ref(null)
const generating = ref(false)

const wizardSteps = [
  { value: 1, title: 'إعدادات الاختبار', subtitle: 'البيانات والنطاق والنماذج', icon: 'mdi-tune-variant' },
  { value: 2, title: 'مصفوفة المعايير', subtitle: 'الوحدات والصعوبة والدرجات', icon: 'mdi-chart-pie' },
  { value: 3, title: 'المعاينة والتأكيد', subtitle: 'مطابقة ملخص المواصفات', icon: 'mdi-clipboard-check-outline' },
  { value: 4, title: 'استعراض وضبط النماذج', subtitle: 'المسودة التفاعلية والتحكيم', icon: 'mdi-file-document-edit-outline' },
]

const validatedStep2Once = ref(false)

const wizardProgressPercentage = computed(() => {
  return ((step.value - 1) / (wizardSteps.length - 1)) * 100
})

function getStepStatus(sValue) {
  // ── Step 1: إعدادات الاختبار ──
  if (sValue === 1) {
    if (step.value === 1) {
      if (validatedOnce.value && invalidSectionsCount.value > 0) {
        return {
          type: 'error',
          badge: 'تنبيه',
          text: `فشل: ${invalidSectionsCount.value} أقسام غير مكتملة`,
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الإعداد',
        text: 'جاري ضبط الإعدادات...',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    if (invalidSectionsCount.value > 0) {
      return {
        type: 'error',
        badge: 'تنبيه',
        text: 'فشل: حقول مطلوبة غير مكتملة',
        statusIcon: 'mdi-alert-circle',
      }
    }
    return {
      type: 'completed',
      badge: 'نجاح',
      text: 'تم بنجاح (مكتمل)',
      statusIcon: 'mdi-check-bold',
    }
  }

  // ── Step 2: مصفوفة المعايير ──
  if (sValue === 2) {
    const isStep2Valid = modelsMode.value === 'advanced'
      ? (Array.isArray(modelGroups.value) && modelGroups.value.length > 0 && modelGroups.value.every(g => getGroupUnitsTotal(g) === 100 && getGroupTypesTotal(g) === 100))
      : (totalUnitsPercentage.value === 100 && totalTypesPercentage.value === 100)

    if (step.value === 2) {
      if (validatedStep2Once.value && !isStep2Valid) {
        return {
          type: 'error',
          badge: 'غير متطابق',
          text: `فشل: الأوزان ${totalUnitsPercentage.value}% (المطلوب 100%)`,
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الضبط',
        text: isStep2Valid ? 'المصفوفة متوازنة (جاهزة)' : 'جاري موازنة النسب...',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    if (step.value > 2) {
      if (!isStep2Valid) {
        return {
          type: 'error',
          badge: 'تنبيه',
          text: 'فشل: المصفوفة غير متوازنة',
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'completed',
        badge: 'نجاح',
        text: 'تم بنجاح (المصفوفة متطابقة)',
        statusIcon: 'mdi-check-bold',
      }
    }
    return {
      type: 'pending',
      badge: 'في الانتظار',
      text: 'في الانتظار',
      statusIcon: 'mdi-clock-outline',
    }
  }

  // ── Step 3: المعاينة والتأكيد ──
  if (sValue === 3) {
    if (step.value === 3) {
      if (shortageReport.value && shortageReport.value.totalMissing > 0) {
        return {
          type: 'error',
          badge: 'عجز بالأسئلة',
          text: `فشل: عجز ${shortageReport.value.totalMissing} سؤال`,
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الفحص',
        text: 'جاري مطابقة الملخص والمواصفات...',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    if (step.value > 3) {
      return {
        type: 'completed',
        badge: 'نجاح',
        text: 'تم الاعتماد والتأكيد بنجاح',
        statusIcon: 'mdi-check-bold',
      }
    }
    return {
      type: 'pending',
      badge: 'في الانتظار',
      text: 'في الانتظار',
      statusIcon: 'mdi-clock-outline',
    }
  }

  // ── Step 4: استعراض وضبط النماذج ──
  if (sValue === 4) {
    if (step.value === 4) {
      if (generating.value) {
        return {
          type: 'active',
          badge: 'جاري التوليد',
          text: 'جاري بناء النماذج وسحب الأسئلة...',
          statusIcon: 'mdi-loading',
        }
      }
      if (stagedModels.value && stagedModels.value.length > 0) {
        return {
          type: 'completed',
          badge: 'نجاح',
          text: `تم بنجاح (${stagedModels.value.length} نماذج جاهزة)`,
          statusIcon: 'mdi-check-bold',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الاستعراض',
        text: 'معاينة النماذج والتحكيم',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    return {
      type: 'pending',
      badge: 'في الانتظار',
      text: 'في الانتظار',
      statusIcon: 'mdi-clock-outline',
    }
  }

  return {
    type: 'pending',
    badge: 'في الانتظار',
    text: 'في الانتظار',
    statusIcon: 'mdi-clock-outline',
  }
}

function getStepNodeClasses(sVal) {
  const status = getStepStatus(sVal).type
  return {
    'is-active': status === 'active',
    'is-completed': status === 'completed',
    'is-error': status === 'error',
    'is-pending': status === 'pending',
  }
}

const handleStepClick = (stepVal) => {
  if (stepVal < step.value) {
    step.value = stepVal
  } else if (stepVal === step.value + 1) {
    nextStep()
  } else if (isEditing.value) {
    step.value = stepVal
  }
}

// State declarations
const modelsMode = ref('uniform')
const bloomEnabled = ref(false)

// Exam Settings
const exam = ref({
  title: '',
  institution_type: 'school',
  subjectId: null,
  classTrackId: null,
  stageId: null,
  collegeId: null,
  departmentId: null,
  specializationId: null,
  semesterSubjectId: null,
  instituteFieldId: null,
  instituteEducationSystemId: null,
  instituteSpecializationId: null,
  instituteCurriculumId: null,
  instituteSubjectId: null,
  yearId: null,
  examPeriodId: null,
  organizationId: null,
  countryId: null,
  governorateId: null,
  directorateId: null,
  regionId: null,
  questionsCount: 20,
  modelsCount: 2,
  totalMarks: 100,
  target_scope_level: 'all',
  exclude_previously_used: false,
})

const examTotalScore = computed(() => Number(exam.value?.totalMarks) || 100)

// Matrix Inner Tabs Items
const activeTab = ref(0)
const instituteSpecParam = computed(() => {
  const p = {}
  if (exam.value.instituteFieldId) p.field = exam.value.instituteFieldId
  if (exam.value.instituteEducationSystemId) p.education_system = exam.value.instituteEducationSystemId
  return Object.keys(p).length ? p : null
})

const matrixTabItems = computed(() => [
  { label: modelsMode.value === 'advanced' ? 'توزيع الوحدات (حسب المجموعات)' : 'توزيع الوحدات', icon: 'mdi-book-open-page-variant' },
  { label: modelsMode.value === 'advanced' ? 'مستويات الصعوبة (متقدم)' : 'مستويات الصعوبة', icon: 'mdi-speedometer' },
  { label: bloomEnabled.value ? 'مستويات بلوم' : 'مستويات بلوم (معطّل)', icon: 'mdi-brain' },
  { label: modelsMode.value === 'advanced' ? 'أنواع الأسئلة (حسب المجموعات)' : 'أنواع الأسئلة', icon: 'mdi-shape' },
])

// Shortage Dialog State
const shortageDialog = ref(false)
const shortageReport = ref({
  mcq: { required: 0, available: 0, missing: 0 },
  tf: { required: 0, available: 0, missing: 0 },
  easy: { required: 0, available: 0, missing: 0 },
  medium: { required: 0, available: 0, missing: 0 },
  hard: { required: 0, available: 0, missing: 0 },
  totalMissing: 0
})

// Quick Selection Helpers

const setModelsCount = (num) => {
  exam.value.modelsCount = num
}
const setTargetScopeLevel = (lvl) => {
  exam.value.target_scope_level = lvl
  if (lvl === 'all') {
    selectedTargetIds.value = []
  }
}

const setModelsMode = (mode) => {
  modelsMode.value = mode
}

// ⭐ Advanced Model Groups
const modelGroups = ref([
  {
    name: 'المجموعة 1',
    count: 2,
    difficulty_profile: 'hard',
    difficulty_distribution: { easy: 10, medium: 30, hard: 60 },
    questions_variation: 'same_scrambled',
    scope_level: 'governorate',
    target_ids: [],
    units: [],
    types: [],
    filter_governorate_id: null,
    filter_directorate_id: null,
    availableSchools: [],
    loadingSchools: false,
  },
  {
    name: 'المجموعة 2',
    count: 2,
    difficulty_profile: 'easy',
    difficulty_distribution: { easy: 60, medium: 30, hard: 10 },
    questions_variation: 'same_scrambled',
    scope_level: 'governorate',
    target_ids: [],
    units: [],
    types: [],
    filter_governorate_id: null,
    filter_directorate_id: null,
    availableSchools: [],
    loadingSchools: false,
  },
])

// ⭐ Geographic Targeting & Organizations (Loaded from dedicated APIs)
const selectedTargetIds = ref([])
const selectedGovernorateForFilter = ref(null)
const selectedDirectorateForFilter = ref(null)

const educationalOrgsList = ref([])
const allSchoolsList = ref([])

const loadingGeoData = ref(false)
const loadingSchools = ref(false)

const loadEducationalHierarchy = async () => {
  loadingGeoData.value = true
  try {
    const res = await examsService.getEducationalHierarchy()
    const data = res?.data || res?.results || (Array.isArray(res) ? res : [])
    educationalOrgsList.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Error loading educational hierarchy:', err)
  } finally {
    loadingGeoData.value = false
  }
}

const governoratesList = computed(() => {
  return educationalOrgsList.value
    .filter(o => o.company_level === 30)
    .map(o => ({
      id: o.id,
      name: o.name_ar,
      name_ar: o.name_ar,
      name_en: o.name_en,
      branch_no: o.branch_no,
      fk_parent_organization: o.fk_parent_organization
    }))
})

const allDirectoratesList = computed(() => {
  return educationalOrgsList.value
    .filter(o => o.company_level === 40)
    .map(o => ({
      id: o.id,
      name: o.name_ar,
      name_ar: o.name_ar,
      name_en: o.name_en,
      branch_no: o.branch_no,
      fk_parent_organization: o.fk_parent_organization
    }))
})

const directoratesList = computed(() => {
  if (!selectedGovernorateForFilter.value) return allDirectoratesList.value
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === selectedGovernorateForFilter.value)
})

const filteredDirectoratesForSchool = computed(() => {
  if (!selectedGovernorateForFilter.value) return []
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === selectedGovernorateForFilter.value)
})

const loadGovernorates = async () => {
  await loadEducationalHierarchy()
}

const loadDirectorates = async () => {}
const loadDirectoratesForSchoolFilter = async () => {}

const isTargetInstitutionsDisabled = computed(() => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school') {
    return !selectedGovernorateForFilter.value || !selectedDirectorateForFilter.value
  }
  return !selectedGovernorateForFilter.value
})

const targetInstitutionsPlaceholder = computed(() => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school') {
    if (!selectedGovernorateForFilter.value) return 'اختر المحافظة أولاً...'
    if (!selectedDirectorateForFilter.value) return 'اختر المديرية أولاً...'
    return 'ابحث بالاسم للمدرسة...'
  }
  if (!selectedGovernorateForFilter.value) return 'اختر المحافظة أولاً...'
  return instType === 'university'
    ? 'ابحث بالاسم للجامعة أو الكلية...'
    : 'ابحث بالاسم للمعهد...'
})

const loadOrganizations = async (params = {}) => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school' && (!params.governorate || !params.directorate)) {
    allSchoolsList.value = []
    return
  }
  if ((instType === 'university' || instType === 'institute') && !params.governorate) {
    allSchoolsList.value = []
    return
  }

  loadingSchools.value = true
  try {
    const queryParts = [`institution_type=${instType}`]
    if (params.governorate) queryParts.push(`governorate=${params.governorate}`)
    if (params.directorate) queryParts.push(`directorate=${params.directorate}`)
    const res = await api.get(`api/academic/organizations/all/?${queryParts.join('&')}`)
    const data = res.data?.data || res.data?.results || res.data || []
    allSchoolsList.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Error loading organizations:", e)
    allSchoolsList.value = []
  } finally {
    loadingSchools.value = false
  }
}

const loadGeographicOrgs = async () => {
  await loadEducationalHierarchy()
}

const onFilterGovForDirectorates = (val) => {
  selectedGovernorateForFilter.value = val
  selectedTargetIds.value = []
}

const onFilterGovForSchoolChange = (val) => {
  selectedGovernorateForFilter.value = val
  selectedDirectorateForFilter.value = null
  selectedTargetIds.value = []
  allSchoolsList.value = []
  const instType = exam.value.institution_type || 'school'
  if (val && instType !== 'school') {
    loadOrganizations({ governorate: val })
  }
}

const onFilterDirForSchoolChange = (val) => {
  selectedDirectorateForFilter.value = val
  selectedTargetIds.value = []
  if (val && selectedGovernorateForFilter.value) {
    loadOrganizations({ governorate: selectedGovernorateForFilter.value, directorate: val })
  } else {
    allSchoolsList.value = []
  }
}

// ⭐ STRICT FILTERING: Only the entities chosen in Section 4 are available for model groups
const targetOptionsForGroups = computed(() => {
  if (exam.value.target_scope_level === 'all' || !selectedTargetIds.value || selectedTargetIds.value.length === 0) {
    return []
  }

  const selectedIds = new Set(selectedTargetIds.value)
  let sourceList = []
  if (exam.value.target_scope_level === 'governorate') {
    sourceList = governoratesList.value
  } else if (exam.value.target_scope_level === 'directorate') {
    sourceList = directoratesList.value
  } else if (exam.value.target_scope_level === 'school') {
    sourceList = allSchoolsList.value
  }

  return sourceList
    .filter(item => selectedIds.has(item.id))
    .map(item => ({
      id: item.id,
      name: item.name_ar || item.name || `هدف #${item.id}`
    }))
})

// Clean up group assignments if target scope or selection changes
watch(selectedTargetIds, (newIds) => {
  if (isLoadingForEdit.value) return
  const validIds = new Set(newIds || [])
  modelGroups.value.forEach(group => {
    if (group.assigned_target_ids && group.assigned_target_ids.length > 0) {
      group.assigned_target_ids = group.assigned_target_ids.filter(id => validIds.has(id))
    }
  })
}, { deep: true })

const getAssignedTargetNames = (ids) => {
  if (!ids || !ids.length) return '—'
  const names = ids.map(id => {
    const opt = targetOptionsForGroups.value.find(o => o.id === id)
    if (opt) return opt.name
    const found = governoratesList.value.find(o => o.id === id) ||
                  directoratesList.value.find(o => o.id === id) ||
                  allSchoolsList.value.find(o => o.id === id)
    return found ? (found.name_ar || found.name) : `#${id}`
  })
  return names.join('، ')
}

const onGroupScopeLevelChange = (group) => {
  group.target_ids = []
  group.filter_governorate_id = null
  group.filter_directorate_id = null
  group.availableSchools = []
}

const getDirectoratesForGroup = (group) => {
  if (!group || !group.filter_governorate_id) return allDirectoratesList.value
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === group.filter_governorate_id)
}

const getDirectoratesForFilterGov = (govId) => {
  if (!govId) return []
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === govId)
}

const isGroupSchoolDisabled = (group) => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school') {
    return !group.filter_governorate_id || !group.filter_directorate_id
  }
  return !group.filter_governorate_id
}

const onGroupFilterGovForSchool = (group) => {
  group.filter_directorate_id = null
  group.target_ids = []
  group.availableSchools = []
  const instType = exam.value.institution_type || 'school'
  if (group.filter_governorate_id && instType !== 'school') {
    loadSchoolsForGroup(group)
  }
}

const onGroupFilterDirForSchool = (group) => {
  group.target_ids = []
  if (group.filter_directorate_id && group.filter_governorate_id) {
    loadSchoolsForGroup(group)
  } else {
    group.availableSchools = []
  }
}

const loadSchoolsForGroup = async (group) => {
  const instType = exam.value.institution_type || 'school'
  group.loadingSchools = true
  try {
    const queryParts = [`institution_type=${instType}`]
    if (group.filter_governorate_id) queryParts.push(`governorate=${group.filter_governorate_id}`)
    if (group.filter_directorate_id) queryParts.push(`directorate=${group.filter_directorate_id}`)
    const res = await api.get(`api/academic/organizations/all/?${queryParts.join('&')}`)
    const data = res.data?.data || res.data?.results || res.data || []
    group.availableSchools = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Error loading schools for group:', e)
    group.availableSchools = []
  } finally {
    group.loadingSchools = false
  }
}

const getGroupTargetNames = (group) => {
  if (!group) return '—'
  if ((group.scope_level || 'all') === 'all') return 'كافة المناطق (عام)'
  if (!group.target_ids || !group.target_ids.length) return 'غير محدد'

  if (group.scope_level === 'governorate') {
    const names = group.target_ids
      .map(id => governoratesList.value.find(g => g.id === id)?.name_ar)
      .filter(Boolean)
    return names.length ? names.join('، ') : `${group.target_ids.length} محافظة`
  }

  if (group.scope_level === 'directorate') {
    const names = group.target_ids
      .map(id => allDirectoratesList.value.find(d => d.id === id)?.name_ar)
      .filter(Boolean)
    return names.length ? names.join('، ') : `${group.target_ids.length} مديرية`
  }

  if (group.scope_level === 'school') {
    if (group.availableSchools && group.availableSchools.length) {
      const names = group.target_ids
        .map(id => group.availableSchools.find(s => s.id === id)?.name_ar)
        .filter(Boolean)
      if (names.length) return names.join('، ')
    }
    return `${group.target_ids.length} مؤسسة / مدرسة`
  }

  return `${group.target_ids.length} جهة`
}

const isAllGroupsAllRegions = computed(() => {
  if (!modelGroups.value || !modelGroups.value.length) return true
  return modelGroups.value.every(g => (g.scope_level || 'all') === 'all')
})

const totalUniqueAssignedTargetsCount = computed(() => {
  if (!modelGroups.value) return 0
  const allIds = new Set()
  modelGroups.value.forEach(g => {
    if ((g.scope_level || 'all') !== 'all' && Array.isArray(g.target_ids)) {
      g.target_ids.forEach(id => allIds.add(id))
    }
  })
  return allIds.size
})

const scopeLevelOptions = [
  { value: 'all', label: 'الكل (بدون تحديد)' },
  { value: 'governorate', label: 'محافظات محددة' },
  { value: 'directorate', label: 'مديريات محددة' },
  { value: 'school', label: 'مدارس محددة' },
]

const difficultyProfiles = [
  { value: 'easy', label: 'سهل' },
  { value: 'medium', label: 'متوسط' },
  { value: 'hard', label: 'صعب' },
  { value: 'mixed', label: 'مختلط' },
  { value: 'custom', label: 'مخصص' },
]

const difficultyItems = [
  { key: 'easy', label: 'سهل', color: 'success' },
  { key: 'medium', label: 'متوسط', color: 'warning' },
  { key: 'hard', label: 'صعب', color: 'error' },
]

const difficultyColor = (profile) => {
  const map = { easy: 'success', medium: 'warning', hard: 'error', mixed: 'info', custom: 'deep-purple' }
  return map[profile] || 'info'
}

const difficultyLabel = (profile) => {
  const map = { easy: 'سهل', medium: 'متوسط', hard: 'صعب', mixed: 'مختلط', custom: 'مخصص' }
  return map[profile] || profile
}

const applyDifficultyPreset = (group) => {
  if (group.difficulty_profile === 'custom') return
  const presets = {
    easy: { easy: 60, medium: 30, hard: 10 },
    medium: { easy: 20, medium: 60, hard: 20 },
    hard: { easy: 10, medium: 30, hard: 60 },
    mixed: { easy: 30, medium: 40, hard: 30 },
  }
  group.difficulty_distribution = { ...presets[group.difficulty_profile] || presets.mixed }
}

const groupDiffTotal = (group) => {
  const d = group.difficulty_distribution || {}
  return (Number(d.easy) || 0) + (Number(d.medium) || 0) + (Number(d.hard) || 0)
}

const getGroupDiffMax = (group, key) => {
  const dist = group.difficulty_distribution || {}
  const currentVal = Number(dist[key]) || 0
  const othersSum = (Number(dist.easy) || 0) + (Number(dist.medium) || 0) + (Number(dist.hard) || 0) - currentVal
  return Math.max(0, 100 - othersSum)
}

const updateGroupDiff = (group, key, newVal) => {
  const dist = group.difficulty_distribution
  if (!dist) return
  const currentVal = Number(dist[key]) || 0
  const othersSum = (Number(dist.easy) || 0) + (Number(dist.medium) || 0) + (Number(dist.hard) || 0) - currentVal
  const maxAllowed = Math.max(0, 100 - othersSum)

  if (newVal > maxAllowed) {
    if (dist[key] !== maxAllowed) {
      dist[key] = maxAllowed
    } else {
      // Force Vue reactivity tick so slider resets internal thumb position
      dist[key] = maxAllowed - 0.001
      nextTick(() => {
        dist[key] = maxAllowed
      })
    }
  } else {
    dist[key] = Math.max(0, newVal)
  }
  syncDifficultyProfile(group)
}

const stepGroupDiff = (group, key, delta) => {
  const dist = group.difficulty_distribution
  if (!dist) return
  const currentVal = Number(dist[key]) || 0
  const othersSum = (Number(dist.easy) || 0) + (Number(dist.medium) || 0) + (Number(dist.hard) || 0) - currentVal
  const maxAllowed = Math.max(0, 100 - othersSum)

  if (delta > 0) {
    dist[key] = Math.min(currentVal + delta, maxAllowed)
  } else {
    dist[key] = Math.max(0, currentVal + delta)
  }
  syncDifficultyProfile(group)
}

const syncDifficultyProfile = (group) => {
  const dist = group.difficulty_distribution || {}
  const presets = {
    easy: { easy: 60, medium: 30, hard: 10 },
    medium: { easy: 20, medium: 60, hard: 20 },
    hard: { easy: 10, medium: 30, hard: 60 },
    mixed: { easy: 30, medium: 40, hard: 30 },
  }
  for (const [profileKey, p] of Object.entries(presets)) {
    if (dist.easy === p.easy && dist.medium === p.medium && dist.hard === p.hard) {
      group.difficulty_profile = profileKey
      return
    }
  }
  group.difficulty_profile = 'custom'
}

const addModelGroup = () => {
  const nextNum = modelGroups.value.length + 1
  const initialUnits = blueprint.value.units ? JSON.parse(JSON.stringify(blueprint.value.units)) : []
  const initialTypes = blueprint.value.types ? JSON.parse(JSON.stringify(blueprint.value.types)) : []
  modelGroups.value.push({
    name: `المجموعة ${nextNum}`,
    count: 2,
    difficulty_profile: 'medium',
    difficulty_distribution: { easy: 20, medium: 60, hard: 20 },
    questions_variation: 'same_scrambled',
    scope_level: 'all',
    target_ids: [],
    units: initialUnits,
    types: initialTypes,
    filter_governorate_id: null,
    filter_directorate_id: null,
    availableSchools: [],
    loadingSchools: false,
  })
}

const removeModelGroup = (idx) => {
  modelGroups.value.splice(idx, 1)
  if (activeUnitGroupIndex.value >= modelGroups.value.length) {
    activeUnitGroupIndex.value = Math.max(0, modelGroups.value.length - 1)
  }
}

const totalModelsCount = computed(() => {
  if (modelsMode.value === 'advanced') {
    return modelGroups.value.reduce((sum, g) => sum + (g.count || 0), 0)
  }
  return exam.value.modelsCount || 2
})

const getGroupVersionCodes = (gIdx) => {
  let offset = 0
  for (let i = 0; i < gIdx; i++) {
    offset += modelGroups.value[i].count || 0
  }
  const codes = []
  for (let j = 0; j < (modelGroups.value[gIdx].count || 0); j++) {
    codes.push(String.fromCharCode(65 + offset + j))
  }
  return codes.join(', ')
}

const updateDistribution = (list, index, newVal) => {
  const othersSum = list.reduce((sum, item, idx) => idx === index ? sum : sum + (item.percentage || 0), 0)
  if (othersSum + newVal > 100) {
    list[index].percentage = Math.max(0, 100 - othersSum)
  } else {
    list[index].percentage = newVal
  }
}

// ═══════════════════════════════════════════════════════════
// Step 1 Master-Detail Sidebar Navigation State & Validation
// ═══════════════════════════════════════════════════════════
const activeStep1Section = ref(1)
const validatedOnce = ref(false)

const isSectionValid = (sectionId) => {
  if (sectionId === 1) {
    const hasBase = !!exam.value.yearId && !!exam.value.examPeriodId
    if (!hasBase) return false

    if (exam.value.institution_type === 'school') {
      return !!exam.value.stageId && !!exam.value.classTrackId && !!exam.value.subjectId
    }
    if (exam.value.institution_type === 'university') {
      return (
        !!exam.value.collegeId &&
        !!exam.value.departmentId &&
        !!exam.value.specializationId &&
        !!exam.value.semesterSubjectId
      )
    }
    if (exam.value.institution_type === 'institute') {
      return (
        !!exam.value.instituteFieldId &&
        !!exam.value.instituteEducationSystemId &&
        !!exam.value.instituteSpecializationId &&
        !!exam.value.instituteCurriculumId &&
        !!exam.value.instituteSubjectId
      )
    }
    return false
  }

  if (sectionId === 2) {
    const hasTitle = !!exam.value.title && String(exam.value.title).trim().length > 0
    const qCount = Number(exam.value.questionsCount)
    return hasTitle && !isNaN(qCount) && qCount >= 5 && qCount <= 100
  }

  if (sectionId === 3) {
    if (modelsMode.value === 'uniform') {
      const mCount = Number(exam.value.modelsCount)
      return !isNaN(mCount) && mCount >= 1 && mCount <= 10
    }
    if (!modelGroups.value || modelGroups.value.length === 0) return false
    return modelGroups.value.every(g => {
      const cnt = Number(g.count)
      const diffValid = !isNaN(cnt) && cnt >= 1 && cnt <= 10 && groupDiffTotal(g) === 100
      const geoValid = (g.scope_level || 'all') === 'all' || (Array.isArray(g.target_ids) && g.target_ids.length > 0)
      return diffValid && geoValid
    })
  }

  return true
}

const invalidSections = computed(() => {
  const list = []
  for (let s = 1; s <= 3; s++) {
    if (!isSectionValid(s)) {
      list.push(s)
    }
  }
  return list
})

const invalidSectionsCount = computed(() => invalidSections.value.length)

const step1NavItems = computed(() => {
  return [
    {
      id: 1,
      title: '1. النطاق والتصنيف الأكاديمي',
      desc: exam.value.institution_type === 'school' ? 'تعليم عام ومدرسي' : exam.value.institution_type === 'university' ? 'تعليم جامعي' : 'تعليم مهني',
      icon: 'mdi-school-outline',
      color: 'primary',
    },
    {
      id: 2,
      title: '2. تفاصيل وسعة ورقة الاختبار',
      desc: `${exam.value.questionsCount} سؤال`,
      icon: 'mdi-card-account-details-outline',
      color: 'info',
    },
    {
      id: 3,
      title: '3. إعدادات النماذج والتوزيع المناطقي',
      desc: modelsMode.value === 'uniform' ? `${exam.value.modelsCount} نماذج موحدة` : `${totalModelsCount.value} نماذج (${modelGroups.value.length} مجموعات)`,
      icon: 'mdi-file-multiple-outline',
      color: 'warning',
    }
  ]
})

const goToStep1Section = (sectionId) => {
  if (sectionId >= 1 && sectionId <= 3) {
    activeStep1Section.value = sectionId
  }
}


const onInstitutionTypeToggle = () => {
  exam.value.stageId = null
  exam.value.classTrackId = null
  exam.value.subjectId = null
  exam.value.collegeId = null
  exam.value.departmentId = null
  exam.value.specializationId = null
  exam.value.semesterSubjectId = null
  exam.value.instituteFieldId = null
  exam.value.instituteEducationSystemId = null
  exam.value.instituteSpecializationId = null
  exam.value.instituteCurriculumId = null
  exam.value.instituteSubjectId = null
  blueprint.value.units = []
  selectedTargetIds.value = []
  selectedGovernorateForFilter.value = null
  selectedDirectorateForFilter.value = null
  allSchoolsList.value = []
  if (exam.value.target_scope_level === 'directorate' && exam.value.institution_type !== 'school') {
    exam.value.target_scope_level = 'all'
  }
  if (modelGroups.value && modelGroups.value.length) {
    modelGroups.value.forEach(g => {
      if (g.scope_level === 'directorate' && exam.value.institution_type !== 'school') {
        g.scope_level = 'all'
      }
      g.target_ids = []
      g.filter_governorate_id = null
      g.filter_directorate_id = null
      g.availableSchools = []
      g.units = []
    })
  }
}

watch(() => exam.value.stageId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.classTrackId = null
  }
})

watch(() => exam.value.countryId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.governorateId = null
    exam.value.directorateId = null
    exam.value.regionId = null
    selectedTargetIds.value = []
    loadGovernorates(newVal)
  }
})

watch(() => exam.value.governorateId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.directorateId = null
    exam.value.regionId = null
  }
})

watch(() => exam.value.directorateId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.regionId = null
  }
})

watch(() => exam.value.target_scope_level, () => {
  if (isLoadingForEdit.value) return
  selectedTargetIds.value = []
  selectedGovernorateForFilter.value = null
  selectedDirectorateForFilter.value = null
  allSchoolsList.value = []
})

// Options from Store
const subjects = computed(() => store.getAll('subjects'))
const levels = computed(() => store.getAll('levels'))
const branches = computed(() => store.getAll('branches'))
const organizations = computed(() => store.getAll('organizations'))
const years = computed(() => store.getAll('years'))
const levelSubjectBranches = computed(() => store.getAll('levelSubjectBranches'))
const examPeriods = computed(() => store.getAll('examPeriods'))
const examSchedules = computed(() => store.getAll('examSchedules'))
const stages = computed(() => store.getAll('stages'))

const filteredLevels = computed(() => {
  let res = levels.value
  if (exam.value.stageId) {
    res = res.filter(l => l.stage === exam.value.stageId)
  }
  if (exam.value.branchId) {
    const validLevelIds = levelSubjectBranches.value
      .filter(lsb => (lsb.branchId || lsb.branch) === exam.value.branchId)
      .map(lsb => (lsb.levelId || lsb.level))
    res = res.filter(l => validLevelIds.includes(l.id))
  }
  return res
})

const filteredSubjects = computed(() => {
  let res = subjects.value
  if (!exam.value.branchId && !exam.value.stageId && !exam.value.levelId) return res

  let validSubjectIds = new Set(res.map(s => s.id))

  if (exam.value.branchId) {
    const branchSubIds = levelSubjectBranches.value
      .filter(lsb => (lsb.branchId || lsb.branch) === exam.value.branchId)
      .map(lsb => (lsb.subjectId || lsb.subject))
    validSubjectIds = new Set(branchSubIds)
  }

  if (exam.value.stageId && !exam.value.levelId) {
    const stageLevelIds = levels.value.filter(l => l.stage === exam.value.stageId).map(l => l.id)
    const stageSubIds = levelSubjectBranches.value
      .filter(lsb => stageLevelIds.includes(lsb.levelId || lsb.level))
      .map(lsb => (lsb.subjectId || lsb.subject))

    if (exam.value.branchId) {
      validSubjectIds = new Set([...validSubjectIds].filter(x => stageSubIds.includes(x)))
    } else {
      validSubjectIds = new Set(stageSubIds)
    }
  }

  if (exam.value.levelId) {
    const levelSubIds = levelSubjectBranches.value
      .filter(lsb => (lsb.levelId || lsb.level) === exam.value.levelId)
      .map(lsb => (lsb.subjectId || lsb.subject))

    if (exam.value.branchId || exam.value.stageId) {
      validSubjectIds = new Set([...validSubjectIds].filter(x => levelSubIds.includes(x)))
    } else {
      validSubjectIds = new Set([...levelSubIds])
    }
  }

  return res.filter(s => validSubjectIds.has(s.id))
})



watch(years, (newYears) => {
  if (!exam.value.yearId && newYears && newYears.length > 0) {
    const currentYear = newYears.find(y => y.is_current || y.isCurrent)
    exam.value.yearId = currentYear ? currentYear.id : newYears[0].id
  }
}, { immediate: true })

const loadExamForEditing = async (id) => {
  isLoadingForEdit.value = true
  try {
    const res = await examsService.getExamForEdit(id)
    if (res && res.success && res.data) {
      const d = res.data
      isEditing.value = true
      editingExamId.value = d.id
      editingExamCode.value = d.uniqueCode || `EXAM-#${d.id}`

      exam.value.title = d.title || ''
      exam.value.institution_type = d.institution_type || 'school'
      exam.value.yearId = d.yearId
      exam.value.subjectId = d.subjectId
      exam.value.examScheduleId = d.examScheduleId
      exam.value.examPeriodId = d.examPeriodId
      exam.value.stageId = d.stageId
      exam.value.levelId = d.levelId
      exam.value.classTrackId = d.classTrackId
      exam.value.collegeId = d.collegeId
      exam.value.departmentId = d.departmentId
      exam.value.specializationId = d.specializationId
      exam.value.semesterSubjectId = d.semesterSubjectId
      exam.value.countryId = d.countryId
      exam.value.governorateId = d.governorateId
      exam.value.directorateId = d.directorateId
      exam.value.regionId = d.regionId
      exam.value.questionsCount = d.questionsCount || 20
      exam.value.modelsCount = d.modelsCount || 2
      exam.value.totalMarks = d.totalMarks || 100
      exam.value.target_scope_level = d.target_scope_level || 'all'
      exam.value.exclude_previously_used = d.exclude_previously_used || false

      modelsMode.value = d.modelsMode || 'uniform'
      bloomEnabled.value = d.bloomEnabled || false

      if (Array.isArray(d.selectedTargetIds) && d.selectedTargetIds.length > 0) {
        selectedTargetIds.value = d.selectedTargetIds
      }

      if (Array.isArray(d.model_groups) && d.model_groups.length > 0) {
        modelGroups.value = d.model_groups
      }

      if (d.blueprint) {
        if (Array.isArray(d.blueprint.units) && d.blueprint.units.length > 0) {
          blueprint.value.units = d.blueprint.units
        }
        if (Array.isArray(d.blueprint.difficulty) && d.blueprint.difficulty.length > 0) {
          blueprint.value.difficulty = d.blueprint.difficulty
        }
        if (Array.isArray(d.blueprint.bloom) && d.blueprint.bloom.length > 0) {
          blueprint.value.bloom = d.blueprint.bloom
        }
        if (Array.isArray(d.blueprint.types) && d.blueprint.types.length > 0) {
          blueprint.value.types = d.blueprint.types
        }
      }

      if (Array.isArray(d.models) && d.models.length > 0) {
        stagedModels.value = d.models
        activeStagedModelIndex.value = 0
      }


    } else {
      throw new Error(res?.message || 'فشل في استرجاع بيانات الاختبار للتعديل')
    }
  } catch (err) {
    console.error('Error loading exam for edit:', err)
    const errMsg = err?.response?.data?.message || err?.message || 'تعذر استرجاع بيانات الاختبار للتعديل'
    if (proxy && proxy.$alert) {
      proxy.$alert('errorData', {
        message: errMsg,
        title: 'خطأ في تحميل الاختبار'
      })
    }
  } finally {
    setTimeout(() => {
      isLoadingForEdit.value = false
    }, 500)
  }
}

const exitEditMode = () => {
  isEditing.value = false
  editingExamId.value = null
  editingExamCode.value = ''
  router.replace({ path: '/exams-create' }).catch(() => {
    router.replace({ path: '/ExamGenerator/ExamCreateView' })
  })
  exam.value.title = ''
  exam.value.questionsCount = 20
  exam.value.modelsCount = 2
  stagedModels.value = []
  step.value = 1
}

onMounted(async () => {
  const editId = route.query.edit_exam_id

  // If editing an exam, start loading it IMMEDIATELY without waiting for background store caches
  const editTask = editId ? loadExamForEditing(editId) : Promise.resolve()

  // Background fetch store items in parallel without blocking the UI
  const bgFetches = Promise.allSettled([
    store.getAll('questions').length === 0 ? store.fetchQuestions() : Promise.resolve(),
    store.getAll('lessons').length === 0 ? store.fetchLessons() : Promise.resolve(),
    store.getAll('units').length === 0 ? store.fetchUnits() : Promise.resolve(),
    store.getAll('years').length === 0 ? store.fetchYears() : Promise.resolve(),
    loadGeographicOrgs()
  ])

  if (editId) {
    await editTask
  } else {
    await bgFetches
    if (!exam.value.yearId) {
      const currentYear = years.value.find(y => y.is_current || y.isCurrent)
      if (currentYear) {
        exam.value.yearId = currentYear.id
      } else if (years.value.length > 0) {
        exam.value.yearId = years.value[0].id
      }
    }
  }
})


watch(() => route.query.edit_exam_id, async (newId) => {
  if (newId && Number(newId) !== Number(editingExamId.value)) {
    await loadExamForEditing(newId)
  } else if (!newId && isEditing.value) {
    exitEditMode()
  }
})

// Blueprint
const blueprint = ref({
  units: [],
  difficulty: [
    { name: 'سهل', percentage: 30, color: 'success' },
    { name: 'متوسط', percentage: 50, color: 'warning' },
    { name: 'صعب', percentage: 20, color: 'error' },
  ],
  bloom: [
    { name: 'تذكر', percentage: 20, color: 'info' },
    { name: 'فهم', percentage: 25, color: 'success' },
    { name: 'تطبيق', percentage: 25, color: 'primary' },
    { name: 'تحليل', percentage: 15, color: 'warning' },
    { name: 'تقويم', percentage: 10, color: 'deep-orange' },
    { name: 'إبداع', percentage: 5, color: 'error' },
  ],
  types: [
    {
      id: 'single_choice',
      value: 'single_choice',
      name: 'اختيار من متعدد (إجابة واحدة)',
      shortName: 'MCQ فردي',
      subtitle: 'سؤال اختيار من متعدد بإجابة صحيحة واحدة فقط',
      percentage: 50,
      mark: 2.0,
      color: 'primary',
      icon: 'mdi-radiobox-marked'
    },
    {
      id: 'true_false',
      value: 'true_false',
      name: 'صواب / خطأ',
      shortName: 'صح/خطأ',
      subtitle: 'سؤال تحديد مدى صحة أو خطأ العبارة المعروضة',
      percentage: 50,
      mark: 1.0,
      color: 'success',
      icon: 'mdi-check-circle-outline'
    },
    {
      id: 'multiple_choice',
      value: 'multiple_choice',
      name: 'اختيار متعدد (أكثر من إجابة)',
      shortName: 'اختيار متعدد',
      subtitle: 'سؤال اختيار من متعدد يتضمن أكثر من إجابة صحيحة',
      percentage: 0,
      mark: 2.0,
      color: 'info',
      icon: 'mdi-checkbox-multiple-marked-outline'
    },
    {
      id: 'essay',
      value: 'essay',
      name: 'أسئلة مقالية (إنشائية)',
      shortName: 'مقالي',
      subtitle: 'أسئلة شرح وحلول تفصيلية تتطلب كتابة مقالية',
      percentage: 0,
      mark: 5.0,
      color: 'warning',
      icon: 'mdi-text-box-edit-outline'
    },
    {
      id: 'fill_blanks',
      value: 'fill_blanks',
      name: 'إكمال الفراغات',
      shortName: 'إكمال فراغ',
      subtitle: 'سؤال كتابة أو إدراج الكلمات الناقصة في الجمل',
      percentage: 0,
      mark: 2.0,
      color: 'deep-purple',
      icon: 'mdi-form-textbox'
    },
    {
      id: 'matching',
      value: 'matching',
      name: 'مطابقة وتوصيل (مزاوجة)',
      shortName: 'توصيل ومقابلة',
      subtitle: 'المقابلة والتوصيل بين مفردات القائمتين (أ) و (ب)',
      percentage: 0,
      mark: 2.0,
      color: 'teal',
      icon: 'mdi-swap-horizontal-bold'
    },
    {
      id: 'ordering',
      value: 'ordering',
      name: 'إعادة ترتيب',
      shortName: 'ترتيب تسلسلي',
      subtitle: 'إعادة ترتيب العناصر والخطوات بالترتيب الصحيح',
      percentage: 0,
      mark: 2.0,
      color: 'cyan',
      icon: 'mdi-sort-ascending'
    },
  ]
})

const getCurrentLsbId = () => {
  const lsb = levelSubjectBranches.value.find(l =>
    (l.subjectId || l.subject) === exam.value.subjectId &&
    (l.levelId || l.level) === exam.value.levelId &&
    (exam.value.branchId ? (l.branchId || l.branch) === exam.value.branchId : true)
  )
  return lsb ? lsb.id : null
}

const getUnitsForSubject = () => {
  const lsbId = getCurrentLsbId()
  if (!lsbId) return []
  const units = store.getAll('units')
  return units.filter(u => (u.levelSubjectBranchId || u.level_subject_branch) === lsbId)
}

const getUnitLessonsCount = (unitId) => {
  return store.getAll('lessons').filter(l => (l.unitId || l.unit) === unitId).length
}

const getUnitApprovedQuestionsCount = (unitId) => {
  const unitLessonIds = store.getAll('lessons').filter(l => (l.unitId || l.unit) === unitId).map(l => l.id)
  return store.getAll('questions').filter(q => unitLessonIds.includes(q.lessonId || q.lesson) && q.status === 'معتمد').length
}

const unitDetailsDialog = ref({
  show: false,
  unitId: null,
  unitName: '',
  lessons: []
})

const openUnitDetails = (unitId, unitName) => {
  const lessons = store.getAll('lessons').filter(l => (l.unitId || l.unit) === unitId)
  const enrichedLessons = lessons.map(l => {
    const questionsCount = store.getAll('questions').filter(q => (q.lessonId || q.lesson) === l.id && q.status === 'معتمد').length
    return { id: l.id, name: l.name, questionsCount }
  })

  unitDetailsDialog.value = {
    show: true,
    unitId,
    unitName,
    lessons: enrichedLessons
  }
}

const goToAddQuestion = (unitId, lessonId) => {
  router.push({ path: '/author/questions/new', query: { unitId, lessonId } })
}

const loadBlueprintUnits = async () => {
  if (exam.value.institution_type === 'university' && exam.value.semesterSubjectId) {
    try {
      const res = await academicService.getUnits({ semester_subject_id: exam.value.semesterSubjectId })
      const uList = res.results || res || []
      if (uList.length > 0) {
        const perUnit = Math.floor(100 / uList.length)
        blueprint.value.units = uList.map((u, idx) => ({
          id: u.id,
          name: u.name_ar || u.name_en || u.name || `مفردة #${u.id}`,
          term: u.term || u.semester || 3,
          percentage: idx === uList.length - 1 ? 100 - (perUnit * (uList.length - 1)) : perUnit
        }))
      } else {
        blueprint.value.units = []
      }
    } catch (e) {
      console.error("Error loading university units for blueprint:", e)
      blueprint.value.units = []
    }
  } else if (exam.value.institution_type === 'institute' && exam.value.instituteSubjectId) {
    try {
      const res = await academicService.getUnits({ subject_id: exam.value.instituteSubjectId })
      const uList = res.results || res || []
      if (uList.length > 0) {
        const perUnit = Math.floor(100 / uList.length)
        blueprint.value.units = uList.map((u, idx) => ({
          id: u.id,
          name: u.name_ar || u.name_en || u.name || `الوحدة #${u.id}`,
          term: u.term || u.semester || 3,
          percentage: idx === uList.length - 1 ? 100 - (perUnit * (uList.length - 1)) : perUnit
        }))
      } else {
        blueprint.value.units = []
      }
    } catch (e) {
      console.error("Error loading institute units for blueprint:", e)
      blueprint.value.units = []
    }
  } else if (exam.value.subjectId && (exam.value.classTrackId || exam.value.levelId || exam.value.stageId)) {
    try {
      const params = {
        subject_id: exam.value.subjectId,
        school_subject: exam.value.subjectId,
        subject: exam.value.subjectId,
        institution_type: 'school'
      }
      if (exam.value.classTrackId) {
        params.class_track_id = exam.value.classTrackId
        params.class_track = exam.value.classTrackId
      }
      if (exam.value.levelId) params.level_id = exam.value.levelId
      if (exam.value.stageId) {
        params.stage_id = exam.value.stageId
        params.stage = exam.value.stageId
      }
      const res = await academicService.getSchoolUnits(params)
      let dbUnits = Array.isArray(res) ? res : (res?.results || [])
      if (!dbUnits || dbUnits.length === 0) {
        const fallbackRes = await academicService.getUnits(params)
        dbUnits = Array.isArray(fallbackRes) ? fallbackRes : (fallbackRes?.results || [])
      }
      if (!Array.isArray(dbUnits) || dbUnits.length === 0) {
        dbUnits = getUnitsForSubject()
      }
      if (dbUnits.length > 0) {
        const periodId = exam.value.examPeriodId;
        let targetTerms = [1, 2, 3]
        const selectedPeriod = store.getAll('examPeriods').find(p => p.id === periodId)
        if (selectedPeriod && selectedPeriod.target_terms) {
          try {
            targetTerms = typeof selectedPeriod.target_terms === 'string' 
                          ? JSON.parse(selectedPeriod.target_terms) 
                          : selectedPeriod.target_terms;
          } catch(e) {
            console.error("Invalid target_terms", e)
          }
        } else {
          if (periodId === 1 || periodId === 2) targetTerms = [1]
          else if (periodId === 3) targetTerms = [2]
          else if (periodId === 4) targetTerms = [1, 2]
        }

        let activeUnits = dbUnits.filter(u => targetTerms.includes(u.term || u.semester || 3))
        if (activeUnits.length === 0) activeUnits = dbUnits

        const perUnit = Math.floor(100 / activeUnits.length)

        blueprint.value.units = dbUnits.map((u) => {
          const isActive = activeUnits.some(active => active.id === u.id)
          let percentage = 0
          if (isActive) {
            const activeIndex = activeUnits.findIndex(active => active.id === u.id)
            percentage = activeIndex === activeUnits.length - 1 ? 100 - (perUnit * (activeUnits.length - 1)) : perUnit
          }
          return {
            id: u.id,
            name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
            term: u.term || u.semester || 3,
            percentage: percentage
          }
        })
      } else {
        blueprint.value.units = []
      }
    } catch (e) {
      console.error("Error loading school units:", e)
      const fallback = getUnitsForSubject()
      blueprint.value.units = fallback.map((u, idx) => ({
        id: u.id,
        name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
        term: u.term || u.semester || 3,
        percentage: idx === fallback.length - 1 ? 100 - (Math.floor(100 / fallback.length) * (fallback.length - 1)) : Math.floor(100 / fallback.length)
      }))
    }
  }

  // 🛡️ Check active curriculum exclusions for this year and subject
  const resolvedYear = exam.value.yearId || (years.value.find(y => y.is_current || y.isCurrent)?.id)
  const effectiveSubId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId
  if (resolvedYear && effectiveSubId && blueprint.value.units && blueprint.value.units.length > 0) {
    try {
      const exclRes = await examsService.getActiveExclusionIds({
        year_id: resolvedYear,
        institution_type: exam.value.institution_type,
        subject_id: effectiveSubId
      })
      const excludedUnitIds = new Set(exclRes?.excluded_unit_ids || [])
      if (excludedUnitIds.size > 0) {
        const includedUnits = blueprint.value.units.filter(u => !excludedUnitIds.has(u.id))
        const perInc = includedUnits.length > 0 ? Math.floor(100 / includedUnits.length) : 0
        let incIdx = 0
        blueprint.value.units.forEach(u => {
          if (excludedUnitIds.has(u.id)) {
            u.isExcluded = true
            u.percentage = 0
          } else {
            u.isExcluded = false
            u.percentage = incIdx === includedUnits.length - 1 ? 100 - (perInc * (includedUnits.length - 1)) : perInc
            incIdx++
          }
        })
      }
    } catch (exclErr) {
      console.error("Error loading curriculum exclusions for exam blueprint:", exclErr)
    }
  }

  syncModelGroupsUnits()
}

watch([
  () => exam.value.subjectId, 
  () => exam.value.classTrackId,
  () => exam.value.stageId,
  () => exam.value.levelId, 
  () => exam.value.branchId, 
  () => exam.value.examPeriodId, 
  () => exam.value.semesterSubjectId,
  () => exam.value.instituteSubjectId,
  () => exam.value.institution_type
], async () => {
  if (isLoadingForEdit.value) return
  await loadBlueprintUnits()
})

const totalUnitsPercentage = computed(() =>
  blueprint.value.units.reduce((sum, u) => sum + u.percentage, 0)
)
const totalDifficultyPercentage = computed(() =>
  blueprint.value.difficulty.reduce((sum, d) => sum + d.percentage, 0)
)
const totalBloomPercentage = computed(() => {
  if (!bloomEnabled.value) return 100
  return blueprint.value.bloom.reduce((sum, b) => sum + b.percentage, 0)
})
const totalTypesPercentage = computed(() =>
  blueprint.value.types.reduce((sum, t) => sum + t.percentage, 0)
)

// ═══════════════════════════════════════════════════════════
// Advanced Model Groups Units Distribution Helpers
// ═══════════════════════════════════════════════════════════
const activeUnitGroupIndex = ref(0)

const currentUnitGroup = computed(() => {
  if (modelsMode.value !== 'advanced') return null
  if (!modelGroups.value || modelGroups.value.length === 0) return null
  const idx = Math.min(Math.max(0, activeUnitGroupIndex.value), modelGroups.value.length - 1)
  return modelGroups.value[idx]
})

const selectUnitGroup = (gIdx) => {
  activeUnitGroupIndex.value = gIdx
  const grp = modelGroups.value[gIdx]
  if (grp && (!grp.units || grp.units.length === 0) && blueprint.value.units && blueprint.value.units.length > 0) {
    grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
  }
}

const syncModelGroupsUnits = () => {
  const baseUnits = blueprint.value.units
  if (!baseUnits || baseUnits.length === 0) return
  modelGroups.value.forEach(group => {
    const isGrpEmpty = !group.units || group.units.length === 0 || group.units.every(u => (u.percentage || 0) === 0)
    if (isGrpEmpty || group.units.length !== baseUnits.length) {
      group.units = JSON.parse(JSON.stringify(baseUnits))
    } else {
      const existingMap = new Map(group.units.map(u => [u.id, u.percentage]))
      group.units = baseUnits.map(baseU => ({
        ...baseU,
        percentage: existingMap.has(baseU.id) ? existingMap.get(baseU.id) : baseU.percentage,
        isExcluded: baseU.isExcluded
      }))
    }
  })
}

// Pure computed property: NO side-effects, NO mutations
const currentActiveUnitsList = computed(() => {
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (grp && Array.isArray(grp.units) && grp.units.length > 0) {
      return grp.units
    }
  }
  return blueprint.value.units || []
})

const isUnitInTerm = (u, termId) => {
  const t = Number(u.term || u.semester || 3)
  if (termId === 1) return t === 1
  if (termId === 2) return t === 2
  return t !== 1 && t !== 2
}

const hasTermSeparation = computed(() => {
  const list = currentActiveUnitsList.value
  if (!list || list.length === 0) return false
  if (exam.value.institution_type === 'university' || exam.value.institution_type === 'institute') return false
  const hasTerm1 = list.some(u => Number(u.term || u.semester) === 1)
  const hasTerm2 = list.some(u => Number(u.term || u.semester) === 2)
  return hasTerm1 && hasTerm2
})

const updateUnitPercentage = (unitId, val) => {
  let targetList = blueprint.value.units
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (grp) {
      if (!grp.units || grp.units.length === 0) {
        if (blueprint.value.units && blueprint.value.units.length > 0) {
          grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
        }
      }
      targetList = grp.units
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(u => u.id === unitId)
  if (realIndex !== -1) {
    updateDistribution(targetList, realIndex, val)
  }
}

const adjustUnitPercentage = (unitId, delta) => {
  let targetList = blueprint.value.units
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (grp) {
      if (!grp.units || grp.units.length === 0) {
        if (blueprint.value.units && blueprint.value.units.length > 0) {
          grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
        }
      }
      targetList = grp.units
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(u => u.id === unitId)
  if (realIndex !== -1) {
    const currentVal = Number(targetList[realIndex].percentage) || 0
    const newVal = Math.max(0, Math.min(100, currentVal + delta))
    updateDistribution(targetList, realIndex, newVal)
  }
}

const getGroupUnitsTotal = (group) => {
  if (!group || !Array.isArray(group.units) || group.units.length === 0) {
    return totalUnitsPercentage.value
  }
  return group.units.reduce((sum, u) => sum + (Number(u.percentage) || 0), 0)
}

const currentGroupUnitsTotal = computed(() => {
  if (modelsMode.value === 'advanced') {
    return getGroupUnitsTotal(currentUnitGroup.value)
  }
  return totalUnitsPercentage.value
})

const distributeUnitsListEqually = (unitsList) => {
  if (!unitsList || unitsList.length === 0) return
  const activeItems = unitsList.filter(u => !u.isExcluded)
  if (activeItems.length === 0) return
  const perItem = Math.floor(100 / activeItems.length)
  let idx = 0
  unitsList.forEach(item => {
    if (item.isExcluded) {
      item.percentage = 0
    } else {
      item.percentage = idx === activeItems.length - 1 ? 100 - (perItem * (activeItems.length - 1)) : perItem
      idx++
    }
  })
}

const autoDistributeCurrentGroupUnits = async () => {
  if (!blueprint.value.units || blueprint.value.units.length === 0) {
    await loadBlueprintUnits()
  }
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (!grp) return
    if (!grp.units || grp.units.length === 0) {
      if (blueprint.value.units && blueprint.value.units.length > 0) {
        grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
      }
    }
    if (grp.units && grp.units.length > 0) {
      distributeUnitsListEqually(grp.units)
    }
  } else {
    autoDistribute('units')
  }
}

// ═══════════════════════════════════════════════════════════
// Advanced Model Groups Question Types Distribution Helpers
// ═══════════════════════════════════════════════════════════
const activeTypeGroupIndex = ref(0)

const currentTypeGroup = computed(() => {
  if (modelsMode.value !== 'advanced') return null
  if (!modelGroups.value || modelGroups.value.length === 0) return null
  const idx = Math.min(Math.max(0, activeTypeGroupIndex.value), modelGroups.value.length - 1)
  return modelGroups.value[idx]
})

const selectTypeGroup = (gIdx) => {
  activeTypeGroupIndex.value = gIdx
  activeUnitGroupIndex.value = gIdx
  const grp = modelGroups.value[gIdx]
  if (grp && (!grp.types || grp.types.length === 0) && blueprint.value.types && blueprint.value.types.length > 0) {
    grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
  }
}

const syncModelGroupsQuestionTypes = () => {
  const baseTypes = blueprint.value.types
  if (!baseTypes || baseTypes.length === 0) return
  modelGroups.value.forEach(group => {
    const isGrpEmpty = !group.types || group.types.length === 0 || group.types.every(t => (t.percentage || 0) === 0)
    if (isGrpEmpty || group.types.length !== baseTypes.length) {
      group.types = JSON.parse(JSON.stringify(baseTypes))
    } else {
      const existingMap = new Map(group.types.map(t => [t.id || t.value, { pct: t.percentage, mark: t.mark }]))
      group.types = baseTypes.map(baseT => {
        const key = baseT.id || baseT.value
        const existing = existingMap.get(key)
        return {
          ...baseT,
          percentage: existing ? existing.pct : baseT.percentage,
          mark: (existing && existing.mark !== undefined) ? existing.mark : (baseT.mark || 1.0)
        }
      })
    }
  })
}

const currentActiveTypesList = computed(() => {
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp && Array.isArray(grp.types) && grp.types.length > 0) {
      return grp.types
    }
  }
  return blueprint.value.types || []
})

const getGroupTypesTotal = (group) => {
  if (!group || !Array.isArray(group.types) || group.types.length === 0) {
    return totalTypesPercentage.value
  }
  return group.types.reduce((sum, t) => sum + (Number(t.percentage) || 0), 0)
}

const currentGroupTypesTotal = computed(() => {
  if (modelsMode.value === 'advanced') {
    return getGroupTypesTotal(currentTypeGroup.value)
  }
  return totalTypesPercentage.value
})

const getTypeQuestionsCount = (qType) => {
  const pct = Number(qType.percentage) || 0
  const totalQ = Number(exam.value.questionsCount) || 40
  return Math.round(totalQ * pct / 100)
}

const getTypeTotalMarks = (qType) => {
  const count = getTypeQuestionsCount(qType)
  const mark = Number(qType.mark !== undefined ? qType.mark : 1.0)
  return Math.round(count * mark * 100) / 100
}

const currentGroupDistributedMarks = computed(() => {
  const list = currentActiveTypesList.value
  if (!list || list.length === 0) return 0
  const total = list.reduce((sum, t) => sum + getTypeTotalMarks(t), 0)
  return Math.round(total * 100) / 100
})

const updateTypeMark = (typeId, markVal) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    targetList[realIndex].mark = Math.max(0, Math.round(Number(markVal) * 100) / 100)
  }
}

const adjustTypeMark = (typeId, delta) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    const curMark = Number(targetList[realIndex].mark !== undefined ? targetList[realIndex].mark : 1.0)
    const newMark = Math.max(0.25, Math.round((curMark + delta) * 100) / 100)
    targetList[realIndex].mark = newMark
  }
}

const autoBalanceMarks = () => {
  let list = currentActiveTypesList.value
  if (!list || list.length === 0) return
  const activeTypes = list.filter(t => (t.percentage || 0) > 0)
  if (activeTypes.length === 0) return
  const totalTarget = Number(exam.value.totalMarks) || 100

  const hasTf = activeTypes.find(t => (t.id || t.value) === 'true_false' || (t.id || t.value) === 'tf')
  const hasMcq = activeTypes.find(t => (t.id || t.value) === 'single_choice' || (t.id || t.value) === 'mcq')

  if (activeTypes.length === 2 && hasTf && hasMcq) {
    const tfCount = getTypeQuestionsCount(hasTf)
    const mcqCount = getTypeQuestionsCount(hasMcq)
    if (totalTarget === 100 && tfCount === 20 && mcqCount === 40) {
      hasTf.mark = 1.0
      hasMcq.mark = 2.0
      return
    } else if (mcqCount > 0) {
      let tfM = 1.0
      let rem = totalTarget - (tfCount * tfM)
      if (rem > 0) {
        hasTf.mark = tfM
        hasMcq.mark = Math.round((rem / mcqCount) * 100) / 100
        return
      }
    }
  }

  const totalQuestionsInActive = activeTypes.reduce((sum, t) => sum + getTypeQuestionsCount(t), 0)
  if (totalQuestionsInActive > 0) {
    const markPerQ = totalTarget / totalQuestionsInActive
    activeTypes.forEach(t => {
      t.mark = Math.round(markPerQ * 100) / 100
    })
  }
}

const setTotalMarks = (val) => {
  exam.value.totalMarks = val
  autoBalanceMarks()
}

const updateTypePercentage = (typeId, val) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    const newVal = Math.max(0, Math.min(100, Math.round(Number(val) || 0)))
    updateDistribution(targetList, realIndex, newVal)
  }
}

const adjustTypePercentage = (typeId, delta) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    const curVal = Number(targetList[realIndex].percentage) || 0
    const newVal = Math.max(0, Math.min(100, curVal + delta))
    updateDistribution(targetList, realIndex, newVal)
  }
}

const autoDistributeTypesList = (typesList) => {
  if (!typesList || typesList.length === 0) return
  let activeTypes = typesList.filter(t => (t.percentage || 0) > 0)
  if (activeTypes.length < 2) {
    activeTypes = typesList.slice(0, 2)
  }
  const perType = Math.floor(100 / activeTypes.length)
  let idx = 0
  typesList.forEach(t => {
    const isAct = activeTypes.some(at => (at.id || at.value) === (t.id || t.value))
    if (!isAct) {
      t.percentage = 0
    } else {
      t.percentage = idx === activeTypes.length - 1 ? 100 - (perType * (activeTypes.length - 1)) : perType
      idx++
    }
  })
}

const autoDistributeCurrentGroupTypes = () => {
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (!grp) return
    if (!grp.types || grp.types.length === 0) {
      if (blueprint.value.types && blueprint.value.types.length > 0) {
        grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
      }
    }
    if (grp.types && grp.types.length > 0) {
      autoDistributeTypesList(grp.types)
    }
  } else {
    autoDistributeTypesList(blueprint.value.types)
  }
}

const autoDistributeAllGroupsTypes = () => {
  if (modelsMode.value === 'advanced' && modelGroups.value.length > 0) {
    modelGroups.value.forEach(group => {
      if (!group.types || group.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          group.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      if (group.types && group.types.length > 0) {
        autoDistributeTypesList(group.types)
      }
    })
  } else {
    autoDistributeTypesList(blueprint.value.types)
  }
}

const copyCurrentGroupTypesToAll = () => {
  if (modelsMode.value !== 'advanced') return
  const currentList = currentActiveTypesList.value
  if (!currentList || currentList.length === 0) return
  modelGroups.value.forEach((grp, idx) => {
    if (idx !== activeTypeGroupIndex.value) {
      grp.types = JSON.parse(JSON.stringify(currentList))
    }
  })
  if (proxy && proxy.$alert) {
    proxy.$alert("successData", {
      message: `تم نسخ توزيع أنواع الأسئلة لـ (${currentTypeGroup.value?.name || 'المجموعة الحالية'}) إلى جميع المجموعات بنجاح.`,
      title: "نسخ توزيع أنواع الأسئلة"
    })
  }
}

const autoDistributeAllGroupsUnits = async () => {
  if (!blueprint.value.units || blueprint.value.units.length === 0) {
    await loadBlueprintUnits()
  }
  if (modelsMode.value === 'advanced') {
    modelGroups.value.forEach(g => {
      if (!g.units || g.units.length === 0) {
        if (blueprint.value.units && blueprint.value.units.length > 0) {
          g.units = JSON.parse(JSON.stringify(blueprint.value.units))
        }
      }
      if (g.units && g.units.length > 0) {
        distributeUnitsListEqually(g.units)
      }
    })
  } else {
    autoDistribute('units')
  }
}

const copyCurrentGroupUnitsToAll = () => {
  if (modelsMode.value !== 'advanced') return
  const currentUnits = currentActiveUnitsList.value
  if (!currentUnits || currentUnits.length === 0) return
  modelGroups.value.forEach((g, idx) => {
    if (idx !== activeUnitGroupIndex.value) {
      g.units = JSON.parse(JSON.stringify(currentUnits))
    }
  })
  if (proxy && proxy.$alert) {
    proxy.$alert("success", { message: "تم نسخ توزيع الوحدات بنجاح إلى جميع المجموعات الأخرى", title: "تم النسخ" })
  }
}

watch(step, async (newStep) => {
  if (newStep === 2) {
    if (!blueprint.value.units || blueprint.value.units.length === 0) {
      await loadBlueprintUnits()
    }
    syncModelGroupsUnits()
  }
})

// ═══════════════════════════════════════════════════════════
// Standard Criteria & Auto Distribution
// ═══════════════════════════════════════════════════════════
const applyStandardCriteria = () => {
  blueprint.value.difficulty = [
    { name: 'سهل', percentage: 30, color: 'success' },
    { name: 'متوسط', percentage: 50, color: 'warning' },
    { name: 'صعب', percentage: 20, color: 'error' },
  ]
  blueprint.value.bloom = [
    { name: 'تذكر', percentage: 20, color: 'info' },
    { name: 'فهم', percentage: 25, color: 'success' },
    { name: 'تطبيق', percentage: 25, color: 'primary' },
    { name: 'تحليل', percentage: 15, color: 'warning' },
    { name: 'تقويم', percentage: 10, color: 'deep-orange' },
    { name: 'إبداع', percentage: 5, color: 'error' },
  ]
  autoDistribute('units')
  if (modelsMode.value === 'advanced') {
    autoDistributeAllGroupsUnits()
  }
}

const autoDistribute = (category) => {
  const list = blueprint.value[category]
  if (!list || list.length === 0) return

  if (category === 'units') {
    const activeItems = list.filter(u => !u.isExcluded)
    if (activeItems.length === 0) return
    const perItem = Math.floor(100 / activeItems.length)
    let idx = 0
    list.forEach(item => {
      if (item.isExcluded) {
        item.percentage = 0
      } else {
        item.percentage = idx === activeItems.length - 1 ? 100 - (perItem * (activeItems.length - 1)) : perItem
        idx++
      }
    })
  } else {
    const perItem = Math.floor(100 / list.length)
    list.forEach((item, idx) => {
      item.percentage = idx === list.length - 1 ? 100 - (perItem * (list.length - 1)) : perItem
    })
  }
}

// ═══════════════════════════════════════════════════════════
// Generation Flow
// ═══════════════════════════════════════════════════════════
const performGenerationSequence = async () => {
  generating.value = true

  try {
    await generateAndSaveExam()
    if (proxy && proxy.$alert) {
      proxy.$alert("success", { message: "تم إنشاء وتوليد الاختبار بنجاح وتم تحويله إلى أرشيف الاختبارات", title: "عملية ناجحة" })
    }
    router.push('/ExamGenerator/ExamArchiveView').catch(() => {
      router.push({ name: 'exams-archive' })
    })
  } catch (e) {
    console.error("Exam generation error:", e)
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: e.message || "فشل إنشاء وتوليد الاختبار", title: "خطأ" })
    }
  } finally {
    generating.value = false
  }
}

// ═══════════════════════════════════════════════════════════════
// STEP 4: INTERACTIVE EXAM STAGING & COMPOSER LOGIC
// ═══════════════════════════════════════════════════════════════
const stagedModels = ref([])
const stagingLoading = ref(false)
const activeStagedModelIndex = ref(0)
const showCorrectAnswers = ref(true)

// Question Swap Dialog State
const swapDialog = ref(false)
const swapLoading = ref(false)
const swapCandidates = ref([])
const swapSearchQuery = ref('')
const targetSwapQuestion = ref(null)
const targetSwapModelIndex = ref(0)

// Quick Create Dialog State
const quickCreateDialog = ref(false)
const quickCreateLoading = ref(false)
const quickCreateForm = ref({
  content: '',
  unitId: null,
  unitName: '',
  lessonId: null,
  difficulty: 2,
  bloomLevel: 'تطبيق',
  questionType: 'Single Choice',
  defaultMark: 1.0,
  tfAnswer: true,
  options: [
    { text: '', isTrue: true },
    { text: '', isTrue: false },
    { text: '', isTrue: false },
    { text: '', isTrue: false },
  ]
})

const currentStagedModel = computed(() => {
  if (!stagedModels.value || stagedModels.value.length === 0) return null
  return stagedModels.value[activeStagedModelIndex.value] || stagedModels.value[0]
})

const questionTypeLabel = (type) => {
  if (!type) return 'اختيار من متعدد'
  const mapping = {
    'Single Choice': 'اختيار من متعدد',
    'single_choice': 'اختيار من متعدد',
    'mcq': 'اختيار من متعدد',
    'True/False': 'صح وخطأ',
    'true_false': 'صح وخطأ',
    'tf': 'صح وخطأ',
    'Multiple Choice': 'خيارات متعددة',
    'multiple_choice': 'خيارات متعددة',
    'Essay': 'مقالي',
    'essay': 'مقالي',
    'Fill in the Blanks': 'إكمال فراغات',
    'fill_blanks': 'إكمال فراغات',
    'Matching': 'مطابقة وتوصيل',
    'matching': 'مطابقة وتوصيل',
    'Ordering': 'إعادة ترتيب',
    'ordering': 'إعادة ترتيب',
  }
  return mapping[type] || type
}

const questionTypeColor = (type) => {
  if (!type) return 'primary'
  if (type.includes('Single') || type.includes('mcq')) return 'primary'
  if (type.includes('True') || type.includes('tf')) return 'success'
  if (type.includes('Multiple')) return 'info'
  if (type.includes('Essay')) return 'warning'
  if (type.includes('Fill')) return 'deep-purple'
  if (type.includes('Matching')) return 'teal'
  if (type.includes('Ordering')) return 'cyan'
  return 'primary'
}

const questionTypeIcon = (type) => {
  if (!type) return 'mdi-radiobox-marked'
  if (type.includes('Single') || type.includes('mcq')) return 'mdi-radiobox-marked'
  if (type.includes('True') || type.includes('tf')) return 'mdi-check-circle-outline'
  if (type.includes('Multiple')) return 'mdi-checkbox-multiple-marked-outline'
  if (type.includes('Essay')) return 'mdi-text-box-edit-outline'
  if (type.includes('Fill')) return 'mdi-form-textbox'
  if (type.includes('Matching')) return 'mdi-swap-horizontal-bold'
  if (type.includes('Ordering')) return 'mdi-sort-ascending'
  return 'mdi-help-circle-outline'
}

const calculateStagedTotalMarks = (model) => {
  if (!model || !model.questions) return 0
  const sum = model.questions.reduce((acc, q) => acc + (parseFloat(q.assignedMark) || 0), 0)
  return Math.round(sum * 100) / 100
}

const prepareStagingAndProceed = async () => {
  stagingLoading.value = true
  try {
    let resolvedYearId = exam.value.yearId
    if (!resolvedYearId) {
      const currentYear = years.value.find(y => y.is_current || y.isCurrent)
      resolvedYearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
    }

    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null

    const payload = {
      title: exam.value.title || 'اختبار جديد',
      institution_type: exam.value.institution_type || 'school',
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      yearId: resolvedYearId,
      stageId: exam.value.stageId || null,
      classTrackId: exam.value.classTrackId || null,
      questionsCount: exam.value.questionsCount,
      modelsCount: exam.value.modelsCount,
      total_marks: Number(exam.value.totalMarks) || 100,
      blueprint: blueprint.value,
      models_mode: modelsMode.value,
      model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
      bloom_enabled: bloomEnabled.value,
      exclude_previously_used: exam.value.exclude_previously_used,
    }

    const res = await examsService.previewStaging(payload)
    const modelsList = res?.models || res?.versions || []
    if (res && res.success && modelsList.length > 0) {
      stagedModels.value = modelsList
      activeStagedModelIndex.value = 0
      step.value = 4
      if (proxy && proxy.$alert) {
        proxy.$alert("successData", {
          message: res.message || "تم تجهيز المسودة التفاعلية للنماذج بنجاح! يمكنك الآن مراجعة وضبط الأسئلة.",
          title: "المسودة التفاعلية جاهزة"
        })
      }
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", {
          message: res?.message || "تعذر إعداد مسودة النماذج.",
          title: "تنبيه"
        })
      }
    }
  } catch (err) {
    console.error("Preview staging error:", err)
    const errMsg = err?.response?.data?.message || err?.message || "حدث خطأ أثناء إعداد المسودة التفاعلية."
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", {
        message: errMsg,
        title: "خطأ في سحب الأسئلة"
      })
    }
  } finally {
    stagingLoading.value = false
  }
}

// 🔄 Quick Auto-Swap for a Question
const quickAutoSwap = async (question, modelIndex) => {
  const currentModel = stagedModels.value[modelIndex]
  if (!currentModel) return

  const allUsedIds = []
  stagedModels.value.forEach(m => {
    (m.questions || []).forEach(q => {
      if (q.id) allUsedIds.push(q.id)
    })
  })

  try {
    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null
    const payload = {
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      institution_type: exam.value.institution_type || 'school',
      unitId: question.unitId,
      difficulty: question.difficulty,
      bloomLevel: question.bloomLevel,
      questionType: question.questionType,
      excludeIds: allUsedIds,
      limit: 1,
    }

    const res = await examsService.findReplacement(payload)
    if (res && res.success && res.questions && res.questions.length > 0) {
      const replacement = res.questions[0]
      replacement.orderIndex = question.orderIndex
      replacement.assignedMark = question.assignedMark

      const qIdx = currentModel.questions.findIndex(q => q.id === question.id)
      if (qIdx !== -1) {
        currentModel.questions.splice(qIdx, 1, replacement)
        if (proxy && proxy.$alert) {
          proxy.$alert("successData", {
            message: "تم استبدال السؤال بنجاح بسؤال مكافئ من البنك!",
            title: "تم الاستبدال"
          })
        }
      }
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", {
          message: "لم يتم العثور على سؤال بديل مطابق تماماً في البنك. يمكنك اختياره يدوياً أو إنشاء سؤال جديد فوراً.",
          title: "لا يوجد بديل مطابق"
        })
      }
    }
  } catch (err) {
    console.error("Auto swap error:", err)
  }
}

// 🔍 Manual Bank Replacement Dialog
const openSwapDialog = async (question, modelIndex) => {
  targetSwapQuestion.value = question
  targetSwapModelIndex.value = modelIndex
  swapSearchQuery.value = ''
  swapDialog.value = true
  await searchSwapCandidates()
}

const searchSwapCandidates = async () => {
  if (!targetSwapQuestion.value) return
  swapLoading.value = true

  const allUsedIds = []
  stagedModels.value.forEach(m => {
    (m.questions || []).forEach(q => {
      if (q.id && q.id !== targetSwapQuestion.value.id) allUsedIds.push(q.id)
    })
  })

  try {
    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null
    const payload = {
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      institution_type: exam.value.institution_type || 'school',
      unitId: targetSwapQuestion.value.unitId,
      difficulty: targetSwapQuestion.value.difficulty,
      bloomLevel: targetSwapQuestion.value.bloomLevel,
      questionType: targetSwapQuestion.value.questionType,
      excludeIds: allUsedIds,
      searchQuery: swapSearchQuery.value,
      limit: 15,
    }

    const res = await examsService.findReplacement(payload)
    if (res && res.success && res.questions) {
      swapCandidates.value = res.questions
    } else {
      swapCandidates.value = []
    }
  } catch (err) {
    console.error("Search swap candidates error:", err)
    swapCandidates.value = []
  } finally {
    swapLoading.value = false
  }
}

const applyReplacement = (cand) => {
  const currentModel = stagedModels.value[targetSwapModelIndex.value]
  if (!currentModel || !targetSwapQuestion.value) return

  const replacement = {
    ...cand,
    orderIndex: targetSwapQuestion.value.orderIndex,
    assignedMark: targetSwapQuestion.value.assignedMark,
  }

  const qIdx = currentModel.questions.findIndex(q => q.id === targetSwapQuestion.value.id)
  if (qIdx !== -1) {
    currentModel.questions.splice(qIdx, 1, replacement)
    swapDialog.value = false
    if (proxy && proxy.$alert) {
      proxy.$alert("successData", {
        message: "تم اعتماد السؤال البديل في النموذج بنجاح!",
        title: "تم الاستبدال"
      })
    }
  }
}

const openQuickCreateFromSwap = () => {
  swapDialog.value = false
  openQuickCreateDialog(targetSwapQuestion.value, targetSwapModelIndex.value)
}

// ➕ Quick On-The-Fly Question Creation
const openQuickCreateDialog = (question, modelIndex) => {
  targetSwapQuestion.value = question
  targetSwapModelIndex.value = modelIndex

  let qType = 'Single Choice'
  if (question.questionType && (question.questionType.includes('True') || question.questionType.includes('tf'))) {
    qType = 'True/False'
  } else if (question.questionType && question.questionType.includes('Essay')) {
    qType = 'Essay'
  }

  quickCreateForm.value = {
    content: '',
    unitId: question.unitId,
    unitName: question.unitName || 'الوحدة الحالية',
    lessonId: question.lessonId,
    difficulty: question.difficulty || 2,
    bloomLevel: question.bloomLevel || 'تطبيق',
    questionType: qType,
    defaultMark: question.assignedMark || 1.0,
    tfAnswer: true,
    options: [
      { text: '', isTrue: true },
      { text: '', isTrue: false },
      { text: '', isTrue: false },
      { text: '', isTrue: false },
    ]
  }

  quickCreateDialog.value = true
}

const addQuickOption = () => {
  quickCreateForm.value.options.push({ text: '', isTrue: false })
}

const removeQuickOption = (idx) => {
  if (quickCreateForm.value.options.length > 2) {
    quickCreateForm.value.options.splice(idx, 1)
    if (!quickCreateForm.value.options.some(o => o.isTrue)) {
      quickCreateForm.value.options[0].isTrue = true
    }
  }
}

const setQuickCorrectOption = (idx) => {
  quickCreateForm.value.options.forEach((opt, i) => {
    opt.isTrue = (i === idx)
  })
}

const submitQuickCreateQuestion = async () => {
  if (!quickCreateForm.value.content || !quickCreateForm.value.content.trim()) {
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: "يرجى كتابة نص السؤال أولاً", title: "حقل مطلوب" })
    }
    return
  }

  quickCreateLoading.value = true
  try {
    let optionsPayload = []
    if (quickCreateForm.value.questionType === 'Single Choice') {
      const validOptions = quickCreateForm.value.options.filter(o => o.text && o.text.trim())
      if (validOptions.length < 2) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", { message: "يرجى إدخال خيارين على الأقل لسؤال الاختيار من متعدد", title: "خيارات ناقصة" })
        }
        quickCreateLoading.value = false
        return
      }
      optionsPayload = validOptions
    } else if (quickCreateForm.value.questionType === 'True/False') {
      optionsPayload = [
        { text: 'صواب', isTrue: quickCreateForm.value.tfAnswer === true },
        { text: 'خطأ', isTrue: quickCreateForm.value.tfAnswer === false },
      ]
    }

    const payload = {
      content: quickCreateForm.value.content,
      questionType: quickCreateForm.value.questionType,
      difficulty: quickCreateForm.value.difficulty,
      bloomLevel: quickCreateForm.value.bloomLevel,
      defaultMark: quickCreateForm.value.defaultMark,
      institution_type: exam.value.institution_type || 'school',
      unitId: quickCreateForm.value.unitId,
      lessonId: quickCreateForm.value.lessonId,
      options: optionsPayload,
    }

    const res = await examsService.quickCreateQuestion(payload)
    if (res && res.success && res.question) {
      const createdQ = res.question
      createdQ.orderIndex = targetSwapQuestion.value ? targetSwapQuestion.value.orderIndex : 1
      createdQ.assignedMark = quickCreateForm.value.defaultMark

      const currentModel = stagedModels.value[targetSwapModelIndex.value]
      if (currentModel && targetSwapQuestion.value) {
        const qIdx = currentModel.questions.findIndex(q => q.id === targetSwapQuestion.value.id)
        if (qIdx !== -1) {
          currentModel.questions.splice(qIdx, 1, createdQ)
        } else {
          currentModel.questions.push(createdQ)
        }
      }

      quickCreateDialog.value = false
      if (proxy && proxy.$alert) {
        proxy.$alert("successData", {
          message: "تم حفظ السؤال في بنك الأسئلة وإدراجه في النموذج بنجاح!",
          title: "تم الحفظ والإدراج"
        })
      }
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", { message: res?.message || "فشل إنشاء السؤال", title: "خطأ" })
      }
    }
  } catch (err) {
    console.error("Quick create error:", err)
    const msg = err?.response?.data?.message || err?.message || "حدث خطأ أثناء حفظ السؤال"
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: msg, title: "خطأ" })
    }
  } finally {
    quickCreateLoading.value = false
  }
}

// 🏛️ Final Atomic Commit of Staged Models
const commitFinalExam = async () => {
  generating.value = true
  try {
    let resolvedYearId = exam.value.yearId
    if (!resolvedYearId) {
      const currentYear = years.value.find(y => y.is_current || y.isCurrent)
      resolvedYearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
    }

    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null

    const model_region_assignments = []
    const target_scopes = []
    let overall_target_scope_level = 'all'

    if (modelsMode.value === 'advanced') {
      modelGroups.value.forEach((group, gIdx) => {
        const scopeLvl = group.scope_level || 'all'
        if (scopeLvl !== 'all' && Array.isArray(group.target_ids) && group.target_ids.length > 0) {
          if (overall_target_scope_level === 'all') {
            overall_target_scope_level = scopeLvl
          }
          group.target_ids.forEach(targetId => {
            const assignment = {
              model_group_index: gIdx,
              difficulty_profile: group.difficulty_profile,
              scope_level: scopeLvl,
            }
            if (scopeLvl === 'governorate') assignment.governorate_id = targetId
            else if (scopeLvl === 'directorate') assignment.directorate_id = targetId
            else if (scopeLvl === 'sub_directorate') assignment.sub_directorate_id = targetId
            else if (scopeLvl === 'village') assignment.village_id = targetId
            else if (scopeLvl === 'center') assignment.exam_center_id = targetId
            model_region_assignments.push(assignment)
          })
        }
      })
    }

    const examPayload = {
      title: exam.value.title || 'اختبار نهائي',
      description: exam.value.description,
      exam_type: exam.value.exam_type || 'final',
      institution_type: exam.value.institution_type || 'school',
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      levelId: exam.value.levelId,
      branchId: exam.value.branchId,
      stageId: exam.value.stageId,
      classTrackId: exam.value.classTrackId,
      termId: exam.value.termId,
      academicRoundId: exam.value.academicRoundId,
      yearId: resolvedYearId,
      exam_period: exam.value.exam_period || 'morning',
      target_scope_level: overall_target_scope_level,
      target_scope_id: exam.value.target_scope_id,
      questionsCount: exam.value.questionsCount,
      modelsCount: exam.value.modelsCount,
      durationMinutes: exam.value.durationMinutes,
      totalMarks: Number(exam.value.totalMarks) || 100,
      passingMarks: exam.value.passingMarks || Math.round((Number(exam.value.totalMarks) || 100) * 0.5),
      blueprint: blueprint.value,
      models_mode: modelsMode.value,
      model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
      model_region_assignments: model_region_assignments,
      target_scopes: target_scopes,
      bloom_enabled: bloomEnabled.value,
      exclude_previously_used: exam.value.exclude_previously_used,
      final_versions: stagedModels.value,
    }

    if (isEditing.value && editingExamId.value) {
      examPayload.exam_id = editingExamId.value
    }

    const res = await examsService.generateExam(examPayload)
    if (res && res.success) {
      if (proxy && proxy.$alert) {
        proxy.$alert("successData", {
          message: isEditing.value ? "تم تحديث الاختبار ونماذجه بنجاح!" : "تم إنشاء الاختبار ونماذجه بنجاح كمسودة بانتظار الاعتماد!",
          title: isEditing.value ? "تم تحديث الاختبار بنجاح" : "مبروك! تم حفظ الاختبار"
        })
      }
      setTimeout(() => {
        router.push('/exams-archive').catch(() => {
          router.push({ path: '/ExamGenerator/ExamArchiveView' }).catch(() => {
            router.push({ name: 'exams-archive' })
          })
        })
      }, 1200)
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", {
          message: res?.message || "فشل توليد الاختبار",
          title: "خطأ في الاعتماد"
        })
      }
    }
  } catch (err) {
    console.error("Commit final exam error:", err)
    const msg = err?.response?.data?.message || err?.message || "حدث خطأ أثناء اعتماد الاختبار"
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: msg, title: "خطأ" })
    }
  } finally {
    generating.value = false
  }
}

const nextStep = async () => {
  if (step.value === 1) {
    validatedOnce.value = true

    let formValid = true
    if (step1Form.value) {
      const result = await step1Form.value.validate()
      formValid = result.valid
    }

    if (!formValid || invalidSections.value.length > 0) {
      const firstInvalid = invalidSections.value[0] || 1
      activeStep1Section.value = firstInvalid
      return
    }

    if (!blueprint.value.units || blueprint.value.units.length === 0) {
      await loadBlueprintUnits()
    }
    syncModelGroupsUnits()
    syncModelGroupsQuestionTypes()
    step.value = 2
    return
  }

  if (step.value === 2) {
    validatedStep2Once.value = true
    if (modelsMode.value === 'advanced') {
      const invalidGrp = modelGroups.value.find(g => getGroupUnitsTotal(g) !== 100)
      if (invalidGrp) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع الوحدات في (${invalidGrp.name || 'إحدى المجموعات'}) هو ${getGroupUnitsTotal(invalidGrp)}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه توزيع الوحدات"
          })
        }
        return
      }
      const invalidTypeGrp = modelGroups.value.find(g => getGroupTypesTotal(g) !== 100)
      if (invalidTypeGrp) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع أنواع الأسئلة في (${invalidTypeGrp.name || 'إحدى المجموعات'}) هو ${getGroupTypesTotal(invalidTypeGrp)}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه أنواع الأسئلة"
          })
        }
        return
      }
    } else {
      if (totalUnitsPercentage.value !== 100) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع الوحدات الحالي هو ${totalUnitsPercentage.value}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه توزيع الوحدات"
          })
        }
        return
      }
      if (totalTypesPercentage.value !== 100) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع أنواع الأسئلة الحالي هو ${totalTypesPercentage.value}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه أنواع الأسئلة"
          })
        }
        return
      }
    }
    step.value = 3
    return
  }

  if (step.value === 3) {
    try {
      const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null
      const payload = {
        subjectId: effectiveSubjectId,
        semesterSubjectId: exam.value.semesterSubjectId || null,
        instituteSubjectId: exam.value.instituteSubjectId || null,
        institution_type: exam.value.institution_type || 'school',
        stageId: exam.value.stageId || null,
        classTrackId: exam.value.classTrackId || null,
        questionsCount: exam.value.questionsCount,
        blueprint: blueprint.value,
        models_mode: modelsMode.value,
        model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
        bloom_enabled: bloomEnabled.value,
        exclude_previously_used: exam.value.exclude_previously_used,
      }
      const res = await examsService.checkShortage(payload)
      if (res && res.report) {
        shortageReport.value = res.report
        if (res.hasShortage) {
          shortageDialog.value = true
          return
        }
      }
      await prepareStagingAndProceed()
    } catch (e) {
      console.error("Shortage check error:", e)
      await prepareStagingAndProceed()
    }
    return
  }

  if (step.value === 4) {
    await commitFinalExam()
  }
}

const generateAndSaveExam = async () => {
  let resolvedYearId = exam.value.yearId
  if (!resolvedYearId) {
    const currentYear = years.value.find(y => y.is_current || y.isCurrent)
    resolvedYearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
  }

  const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null

  // Build model-region assignments and target scopes from per-group configuration
  const model_region_assignments = []
  const target_scopes = []
  let overall_target_scope_level = 'all'

  if (modelsMode.value === 'advanced') {
    modelGroups.value.forEach((group, gIdx) => {
      const scopeLvl = group.scope_level || 'all'
      if (scopeLvl !== 'all' && Array.isArray(group.target_ids) && group.target_ids.length > 0) {
        if (overall_target_scope_level === 'all') {
          overall_target_scope_level = scopeLvl
        }
        group.target_ids.forEach(targetId => {
          const assignment = {
            model_group_index: gIdx,
            difficulty_profile: group.difficulty_profile,
            scope_level: scopeLvl,
          }
          const scope = { scope_level: scopeLvl }

          if (scopeLvl === 'governorate') {
            assignment.governorate_id = targetId
            scope.governorate_id = targetId
          } else if (scopeLvl === 'directorate') {
            assignment.directorate_id = targetId
            scope.directorate_id = targetId
          } else if (scopeLvl === 'school') {
            assignment.organization_id = targetId
            scope.organization_id = targetId
          }

          model_region_assignments.push(assignment)
          target_scopes.push(scope)
        })
      }
    })
  }

  const payload = {
    title: exam.value.title,
    institution_type: exam.value.institution_type || 'school',
    subjectId: effectiveSubjectId,
    levelId: exam.value.levelId || null,
    stageId: exam.value.stageId || null,
    classTrackId: exam.value.classTrackId || null,
    branchId: exam.value.branchId || null,
    collegeId: exam.value.collegeId || null,
    departmentId: exam.value.departmentId || null,
    specializationId: exam.value.specializationId || null,
    semesterSubjectId: exam.value.semesterSubjectId || null,
    instituteFieldId: exam.value.instituteFieldId || null,
    instituteEducationSystemId: exam.value.instituteEducationSystemId || null,
    instituteSpecializationId: exam.value.instituteSpecializationId || null,
    instituteCurriculumId: exam.value.instituteCurriculumId || null,
    instituteSubjectId: exam.value.instituteSubjectId || null,
    yearId: resolvedYearId,
    countryId: exam.value.countryId || null,
    governorateId: exam.value.governorateId || null,
    directorateId: exam.value.directorateId || null,
    regionId: exam.value.regionId || null,
    questionsCount: exam.value.questionsCount,
    modelsCount: modelsMode.value === 'uniform' ? exam.value.modelsCount : totalModelsCount.value,
    total_marks: exam.value.totalMarks || 100,
    totalMarks: exam.value.totalMarks || 100,
    blueprint: {
      ...blueprint.value,
      total_marks: exam.value.totalMarks || 100
    },
    // Advanced Options
    bloom_enabled: bloomEnabled.value,
    models_mode: modelsMode.value,
    model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
    target_scope_level: overall_target_scope_level,
    target_scopes: target_scopes,
    model_region_assignments: model_region_assignments,
    exclude_previously_used: exam.value.exclude_previously_used,
  }

  if (isEditing.value && editingExamId.value) {
    payload.exam_id = editingExamId.value
  }

  const res = await examsService.generateExam(payload)
  if (res && (res.success || res.id || res.examId)) {
    if (res.data) {
      store.add('exams', res.data)
    }
    return res
  } else {
    throw new Error(res?.message || "فشل توليد الاختبار")
  }
}
</script>

<style scoped>
/* ==========================================================================
   EXECUTIVE ZERO-GRAY DESIGN SYSTEM — SMSP EXAM GENERATOR
   Standards: Modern Ministerial / Academic Portal Design
   Principles: Zero dull gray, high visual hierarchy, clean geometry, 4/8px grid
   ========================================================================== */

.editing-mode-banner {
  background: rgba(var(--v-theme-warning), 0.08) !important;
  border: 1.5px solid rgba(var(--v-theme-warning), 0.3) !important;
  box-shadow: 0 4px 20px rgba(var(--v-theme-warning), 0.06) !important;
}

.qb-exam-create-v4 {
  color: rgb(var(--v-theme-on-surface));
  background: radial-gradient(ellipse at 50% 0%, rgba(var(--v-theme-primary), 0.04) 0%, transparent 70%);
}

/* ==========================================================================
   1. Main Container & Structural Cards (No Gray)
   ========================================================================== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
  box-shadow: 0 10px 30px rgba(var(--v-theme-primary), 0.04) !important;
}

.section-group-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.02) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-group-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.28) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.06) !important;
}

.border-subtle {
  border: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
  background: rgb(var(--v-theme-surface));
}

.border-b-subtle {
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
}

.border-t-subtle {
  border-top: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
}

/* ==========================================================================
   2. Connected Stepper Wizard Pipeline (Executive 4-Step Progress)
   ========================================================================== */
.premium-wizard-wrapper {
  position: relative;
  padding: 24px 36px 20px 36px;
  background: linear-gradient(180deg, rgba(var(--v-theme-primary), 0.05) 0%, rgb(var(--v-theme-surface)) 100%) !important;
  border-bottom: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
}

.premium-wizard-container {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1080px;
  margin: 0 auto;
}

.wizard-progress-track {
  position: absolute;
  top: 23px;
  left: 60px;
  right: 60px;
  height: 4px;
  background: rgba(var(--v-theme-primary), 0.1) !important;
  z-index: 1;
  border-radius: 999px;
  overflow: hidden;
}

.wizard-progress-fill {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  background: linear-gradient(90deg, #0284c7 0%, rgb(var(--v-theme-primary)) 100%) !important;
  transition: width 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
  border-radius: 999px;
  box-shadow: 0 0 10px rgba(var(--v-theme-primary), 0.4);
}

.wizard-beam-glow {
  position: absolute;
  left: 0;
  top: -2px;
  bottom: -2px;
  width: 16px;
  background: #ffffff;
  border-radius: 50%;
  filter: blur(3px);
  opacity: 0.9;
  animation: wizard-beam-pulse 1.5s ease-in-out infinite alternate;
}

@keyframes wizard-beam-pulse {
  from { opacity: 0.5; transform: scaleX(0.8); }
  to { opacity: 1; transform: scaleX(1.3); }
}

.premium-wizard-node {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  flex: 1;
  max-width: 250px;
  transition: all 0.25s ease;
  user-select: none;
}

/* Stepper Circle Anchor & Geometry */
.stepper-circle-anchor {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}

.stepper-circle {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(var(--v-theme-surface));
  border: 2px solid rgba(var(--v-theme-primary), 0.2);
  color: rgba(var(--v-theme-on-surface), 0.55);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.node-step-number {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgb(var(--v-theme-surface));
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-size: 11px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25);
  z-index: 4;
  transition: all 0.25s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

/* 1. Active State (قيد الضبط) */
.premium-wizard-node.is-active .stepper-circle {
  background: rgb(var(--v-theme-primary)) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  color: #ffffff !important;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(var(--v-theme-primary), 0.18), 0 4px 14px rgba(var(--v-theme-primary), 0.35);
}

.premium-wizard-node.is-active .node-step-number {
  background: rgb(var(--v-theme-primary));
  color: #ffffff;
  border-color: #ffffff;
}

/* Active Pulsing Wave Ring */
.stepper-pulse-ring {
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  border-radius: 50%;
  opacity: 0.8;
  pointer-events: none;
}

.pulse-primary {
  border: 2px solid rgb(var(--v-theme-primary));
  animation: stepper-ring-expand-blue 1.8s cubic-bezier(0.24, 0, 0.38, 1) infinite;
}

@keyframes stepper-ring-expand-blue {
  0% { transform: scale(0.92); opacity: 0.85; }
  50% { transform: scale(1.22); opacity: 0.3; }
  100% { transform: scale(1.4); opacity: 0; }
}

.pulse-error {
  border: 2px solid rgb(var(--v-theme-error));
  animation: stepper-ring-expand-error 1.4s cubic-bezier(0.24, 0, 0.38, 1) infinite;
}

@keyframes stepper-ring-expand-error {
  0% { transform: scale(0.92); opacity: 0.9; }
  50% { transform: scale(1.25); opacity: 0.35; }
  100% { transform: scale(1.42); opacity: 0; }
}

.icon-active-breath {
  animation: icon-breath-subtle 1.5s ease-in-out infinite alternate;
}

@keyframes icon-breath-subtle {
  from { transform: scale(0.94); opacity: 0.9; }
  to { transform: scale(1.08); opacity: 1; }
}

/* 2. Completed State (نجاح / مكتمل) */
.premium-wizard-node.is-completed .stepper-circle {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 2px 10px rgba(var(--v-theme-primary), 0.15);
}

.premium-wizard-node.is-completed .node-step-number {
  background: rgb(var(--v-theme-primary));
  color: #ffffff;
  border-color: rgb(var(--v-theme-surface));
}

.checkmark-pop {
  animation: checkmark-pop-anim 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes checkmark-pop-anim {
  0% { transform: scale(0.3); opacity: 0; }
  70% { transform: scale(1.25); }
  100% { transform: scale(1); opacity: 1; }
}

/* 3. Error / Failure State (فشل / تنبيه / غير مكتمل) */
.premium-wizard-node.is-error .stepper-circle {
  background: rgba(var(--v-theme-error), 0.08) !important;
  border-color: rgb(var(--v-theme-error)) !important;
  color: rgb(var(--v-theme-error)) !important;
  box-shadow: 0 0 0 3px rgba(var(--v-theme-error), 0.16), 0 3px 12px rgba(var(--v-theme-error), 0.2);
}

.premium-wizard-node.is-error .node-step-number {
  background: rgb(var(--v-theme-error));
  color: #ffffff;
  border-color: rgb(var(--v-theme-surface));
}

.error-icon-shake {
  animation: error-shake-subtle 0.6s ease-in-out;
}

@keyframes error-shake-subtle {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-3px); }
  40%, 80% { transform: translateX(3px); }
}

/* 4. Pending State */
.premium-wizard-node.is-pending {
  opacity: 0.72;
}

.premium-wizard-node.is-pending:hover {
  opacity: 0.95;
}

.premium-wizard-node.is-pending:hover .stepper-circle {
  border-color: rgba(var(--v-theme-primary), 0.4);
  transform: translateY(-2px);
}

/* Stepper Node Typography & Titles */
.node-content {
  width: 100%;
}

.node-title {
  font-size: 0.88rem;
  line-height: 1.3;
  color: rgb(var(--v-theme-on-surface));
  transition: color 0.2s ease;
  white-space: nowrap;
}

.premium-wizard-node.is-active .node-title {
  color: rgb(var(--v-theme-primary)) !important;
  font-weight: 900;
}

.premium-wizard-node.is-error .node-title {
  color: rgb(var(--v-theme-error)) !important;
  font-weight: 900;
}

.node-subtitle {
  font-size: 0.72rem;
  line-height: 1.25;
  color: rgba(var(--v-theme-on-surface), 0.65);
  margin-top: 2px;
}

/* Explicit Status Badges (نجاح / فشل / قيد الضبط / انتظار) */
.node-status-badge-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.node-status-pill {
  display: inline-flex;
  align-items: center;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 6px !important;
  transition: all 0.25s ease;
  line-height: 1.2;
}

.node-status-pill.status-completed {
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgba(var(--v-theme-primary), 0.25);
}

.node-status-pill.status-active {
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgb(var(--v-theme-primary));
  animation: pulse-text-glow 1.4s ease-in-out infinite alternate;
}

@keyframes pulse-text-glow {
  from { opacity: 0.75; }
  to { opacity: 1; }
}

.node-status-pill.status-error {
  background: rgba(var(--v-theme-error), 0.1);
  color: rgb(var(--v-theme-error));
  border: 1px solid rgba(var(--v-theme-error), 0.35);
}

.node-status-pill.status-pending {
  background: rgba(var(--v-theme-on-surface), 0.05);
  color: rgba(var(--v-theme-on-surface), 0.5);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.12);
}

/* ==========================================================================
   3. Step 1 Master-Detail Sidebar Navigation
   ========================================================================== */
.step1-sidebar-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 20px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.03) !important;
  position: sticky;
  top: 24px;
  z-index: 10;
}

.step1-nav-item {
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-theme-primary), 0.1) !important;
  border-radius: 14px !important;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.step1-nav-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  transform: translateX(-2px);
  background: rgba(var(--v-theme-primary), 0.03) !important;
}

.step1-nav-item.is-active {
  background: linear-gradient(90deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  border-right: 4px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.1) !important;
}

.step1-nav-item.has-error {
  border-color: rgba(var(--v-theme-error), 0.4) !important;
  background: rgba(var(--v-theme-error), 0.04) !important;
  border-right: 4px solid rgb(var(--v-theme-error)) !important;
}

/* ==========================================================================
   4. Segmented Institution Type Controls (Zero Gray)
   ========================================================================== */
.segmented-control {
  background: rgba(var(--v-theme-primary), 0.04) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 16px !important;
  padding: 6px !important;
}

.segmented-control-btn {
  flex: 1 1 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 11px 18px;
  border-radius: 12px;
  border: none;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.75);
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.22s ease;
  min-width: 140px;
}

.segmented-control-btn:hover {
  color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.08);
}

.segmented-control-btn.is-active {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1d4ed8 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.3) !important;
}

/* ==========================================================================
   4.1 Model Group Executive Cards & Unified Soft Neutral Borders
   ========================================================================== */
.model-group-card {
  position: relative;
  background: rgb(var(--v-theme-surface)) !important;
  border: 2px solid #cbd5e1 !important; /* Unified soft light gray / slate border */
  border-inline-start: 6px solid #94a3b8 !important; /* Unified clean neutral slate side accent */
  border-radius: 20px !important;
  margin-bottom: 24px !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.model-group-card:hover {
  border-color: #94a3b8 !important;
  border-inline-start-color: #64748b !important;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.06) !important;
}

/* Header Banner inside each Group Card (Unified Soft Light Gray / Neutral) */
.model-group-header-banner {
  background: rgba(var(--v-theme-surface), 0.96) !important;
  border: 1.5px solid #e2e8f0 !important;
  border-radius: 14px !important;
}

/* Inner Subsections inside Group Card */
.model-group-card .group-inner-section {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid #e2e8f0 !important;
  border-radius: 16px !important;
  transition: all 0.2s ease !important;
}

.model-group-card .group-inner-section:hover {
  border-color: #cbd5e1 !important;
}

/* Elegant Group Divider between consecutive cards */
.group-divider-line {
  height: 1.5px;
  background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
}

.group-divider-badge {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px dashed #cbd5e1 !important;
  color: #64748b !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
}

/* ==========================================================================
   5. Interactive Selection & Model Mode Cards (Zero Gray)
   ========================================================================== */
.selection-card,
.model-mode-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 18px !important;
  padding: 18px 22px !important;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  user-select: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.selection-card:hover,
.model-mode-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.selection-card.is-active,
.model-mode-card.is-active {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.15) !important;
}

.model-mode-card.is-active-warning {
  border-color: #f59e0b !important;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  box-shadow: 0 4px 18px rgba(245, 158, 11, 0.15) !important;
}

/* ==========================================================================
   6. Scope Level Cards Grid (Zero Gray)
   ========================================================================== */
.scope-grid {
  display: flex;
  gap: 10px;
  width: 100%;
}

.scope-card {
  flex: 1 1 0;
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 14px !important;
  padding: 14px 10px !important;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease !important;
  user-select: none;
  min-width: 100px;
}

.scope-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(var(--v-theme-primary), 0.08) !important;
}

.scope-card.is-active {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.18) !important;
}

/* ==========================================================================
   7. Matrix Specification Tabs & Navigation (Step 2)
   ========================================================================== */
.matrix-tabs-bar {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.04) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border-bottom: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  padding: 8px !important;
  gap: 8px !important;
}

.matrix-tab-btn {
  border-radius: 14px !important;
  border: 1.5px solid transparent !important;
  background: transparent !important;
  color: rgba(var(--v-theme-on-surface), 0.7) !important;
  font-weight: 800 !important;
  font-size: 0.92rem !important;
  min-width: 170px !important;
  padding: 12px 18px !important;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.matrix-tab-btn:hover {
  color: rgb(var(--v-theme-primary)) !important;
  background: rgba(var(--v-theme-primary), 0.06) !important;
}

.matrix-tab-btn.is-active {
  background: rgb(var(--v-theme-surface)) !important;
  border-color: rgba(var(--v-theme-primary), 0.28) !important;
  color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.12) !important;
}

.executive-table {
  background: rgb(var(--v-theme-surface)) !important;
}

.table-header-row {
  background: rgba(var(--v-theme-primary), 0.06) !important;
}

/* ==========================================================================
   8. Units Distribution Tab Executive Styles (Zero Gray)
   ========================================================================== */
.units-tab-header {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.06) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.16) !important;
  border-radius: 18px !important;
  padding: 18px 24px !important;
}

.units-header-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(var(--v-theme-primary), 0.12) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.12);
}

.model-groups-selector-hub {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.06) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.18) !important;
  border-radius: 18px !important;
  padding: 18px 22px !important;
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.04) !important;
}

.hub-bullet-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
  box-shadow: 0 0 8px rgba(var(--v-theme-primary), 0.6);
}

.group-pills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
}

.group-switch-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.16) !important;
  border-radius: 14px !important;
  padding: 12px 16px !important;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  user-select: none;
}

.group-switch-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(var(--v-theme-primary), 0.08) !important;
}

.group-switch-pill.is-active {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.14) 0%, rgba(var(--v-theme-primary), 0.04) 100%) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.22) !important;
}

.group-pill-title {
  font-size: 0.94rem;
  color: rgb(var(--v-theme-on-surface));
}

.pill-percentage-badge {
  padding: 3px 10px;
  border-radius: 8px;
  font-size: 0.8rem;
  display: inline-flex;
  align-items: center;
}

.pill-percentage-badge.is-complete {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.pill-percentage-badge.is-pending {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.active-group-hero-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12) 0%, rgba(var(--v-theme-primary), 0.03) 60%, rgb(var(--v-theme-surface)) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.2) !important;
  border-right: 5px solid rgb(var(--v-theme-primary)) !important;
  border-radius: 18px !important;
  padding: 18px 24px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.active-group-hero-avatar {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1d4ed8 100%) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.35);
  flex-shrink: 0;
}

.hero-total-badge {
  border: 1px solid transparent;
}

.hero-total-badge.badge-success {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.hero-total-badge.badge-warning {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.3);
  color: #f59e0b;
}

.modern-unit-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.modern-unit-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateY(-2px);
}

.modern-unit-card::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: rgb(var(--v-theme-primary));
  opacity: 0.85;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.modern-unit-card.is-excluded {
  background: rgba(var(--v-theme-error), 0.04) !important;
  border-color: rgba(var(--v-theme-error), 0.25) !important;
  opacity: 0.8;
}

.modern-unit-card.is-excluded::before {
  background: rgb(var(--v-theme-error));
}

.unit-stepper-box {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14);
  border-radius: 12px;
  padding: 4px 6px;
}

.unit-percentage-display {
  min-width: 62px;
  text-align: center;
  font-size: 1.05rem;
  font-weight: 800;
  color: rgb(var(--v-theme-primary));
  padding: 2px 6px;
  border-radius: 8px;
  background: rgba(var(--v-theme-primary), 0.08);
}

.unit-percentage-display.is-zero {
  color: rgba(var(--v-theme-on-surface), 0.5);
  background: transparent;
}

.unit-percentage-display.is-excluded {
  color: rgb(var(--v-theme-error));
}

.term-header-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-right: 4px solid rgb(var(--v-theme-primary)) !important;
  padding: 10px 18px !important;
  border-radius: 14px !important;
}

/* ==========================================================================
   9. Exam Total Marks Command Center & Question Types Cards (Zero Gray)
   ========================================================================== */
.exam-total-marks-card {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.2) !important;
  border-right: 5px solid rgb(var(--v-theme-primary)) !important;
  border-radius: 18px !important;
  padding: 18px 24px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.06) !important;
}

.total-marks-icon-box {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: rgba(245, 158, 11, 0.12) !important;
  border: 1.5px solid rgba(245, 158, 11, 0.3) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.score-input-wrapper {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25) !important;
}

.score-number-input {
  width: 64px;
  text-align: center;
  font-size: 1.2rem;
  font-weight: 900;
  color: rgb(var(--v-theme-primary));
  outline: none;
  border: none;
  background: transparent;
}

.modern-type-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.modern-type-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateY(-2px);
}

.modern-type-card::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: rgb(var(--v-theme-primary));
  opacity: 0.85;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.type-metrics-bar {
  background: rgba(var(--v-theme-primary), 0.04) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
  border-radius: 12px;
  padding: 8px 14px;
}

/* ==========================================================================
   10. Step 3 Executive KPI Certification Cards
   ========================================================================== */
.kpi-cert-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 18px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02) !important;
}

.kpi-cert-card:hover {
  transform: translateY(-3px);
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.kpi-title {
  font-size: 1rem;
  color: rgb(var(--v-theme-on-surface));
}

.kpi-metric {
  font-size: 1.6rem;
  line-height: 1.15;
}

/* ==========================================================================
   11. Step 4: Interactive Exam Staging Styles (Zero Gray)
   ========================================================================== */
.staged-hero-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.18) !important;
  border-radius: 20px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.05) !important;
}

.staged-hero-icon-box {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: rgba(var(--v-theme-primary), 0.12) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25) !important;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.12);
}

.shadow-success {
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35) !important;
}

.staged-nav-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-radius: 14px !important;
  padding: 9px 18px !important;
  cursor: pointer;
  transition: all 0.22s ease !important;
  display: flex;
  align-items: center;
  gap: 8px;
}

.staged-nav-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.08);
}

.staged-nav-pill.is-active {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.18) !important;
}

.staged-version-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-radius: 14px !important;
  padding: 8px 16px !important;
  cursor: pointer;
  transition: all 0.22s ease !important;
  display: flex;
  align-items: center;
  gap: 8px;
}

.staged-version-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
}

.staged-version-pill.is-active {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12) 0%, rgba(var(--v-theme-primary), 0.04) 100%) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.2) !important;
}

.staged-question-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-right: 5px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.staged-question-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateY(-1px);
}

.staged-option-item {
  background: rgba(var(--v-theme-primary), 0.03) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
  transition: all 0.2s ease;
}

.staged-option-item:hover {
  background: rgba(var(--v-theme-primary), 0.06) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
}

.staged-option-item.is-correct-option {
  background: rgba(16, 185, 129, 0.08) !important;
  border: 1.5px solid #10b981 !important;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.14);
}

/* ==========================================================================
   12. Sticky Wizard Footer
   ========================================================================== */
.wizard-footer {
  backdrop-filter: blur(12px) !important;
  background: rgba(var(--v-theme-surface), 0.96) !important;
  border-top: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .premium-wizard-wrapper {
    padding: 16px 12px;
  }
  .premium-wizard-container {
    flex-wrap: wrap;
    gap: 16px;
  }
  .wizard-progress-track {
    display: none;
  }
  .premium-wizard-node {
    width: 48%;
    max-width: none;
  }
  .stepper-circle {
    width: 40px;
    height: 40px;
  }
  .node-title {
    font-size: 0.8rem;
  }
  .node-status-pill {
    font-size: 0.65rem;
    padding: 1px 6px;
  }
}

/* ==========================================================================
   Lightweight Formal Transparent Loading Overlay
   ========================================================================== */
.formal-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  min-height: 420px;
  background: rgba(var(--v-theme-surface), 0.72) !important;
  backdrop-filter: blur(4px) !important;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  pointer-events: all;
  transition: opacity 0.25s ease;
}

.formal-loading-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.2) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
  position: sticky;
  top: 40%;
}

.content-loading-blur {
  opacity: 0.4 !important;
  pointer-events: none !important;
  user-select: none !important;
  transition: opacity 0.25s ease !important;
}

</style>