<template>
  <div class="qb-exam-create-v4">

    <!-- Main Stepper Wizard Window Content -->
    <div class="main-card rounded-2xl mb-8">

      <!-- Premium Connected Wizard Stepper -->
      <div class="premium-wizard-wrapper">
        <div class="premium-wizard-container">
          <!-- Connecting Progress Line -->
          <div class="wizard-progress-track">
            <div class="wizard-progress-fill"
              :style="{ width: ((step - 1) / (wizardSteps.length - 1)) * 100 + '%', right: 0, left: 'auto' }">
            </div>
          </div>

          <!-- Step Nodes -->
          <div v-for="s in wizardSteps" :key="s.value" class="premium-wizard-node" :class="{
            'is-active': step === s.value,
            'is-completed': step > s.value,
            'is-pending': step < s.value
          }" @click="s.value < step ? step = s.value : null">

            <div class="node-icon-wrapper">
              <v-icon v-if="step > s.value" size="22" color="white" class="node-icon">mdi-check</v-icon>
              <v-icon v-else size="22" class="node-icon" :color="step === s.value ? 'white' : 'primary'">{{ s.icon }}</v-icon>
            </div>

            <div class="node-content">
              <span class="node-title font-weight-black">{{ s.title }}</span>
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
                          :rules="requiredRule" @update:model-value="() => { exam.classTrackId = null; exam.subjectId = null; }" />
                        <auto-list v-model="exam.classTrackId" name="ClassTrackByStage" :param="exam.stageId" placeholder="اختر الصف والمسار"
                          cols="3" :add="false" :rules="requiredRule" :disabled="!exam.stageId" @update:model-value="exam.subjectId = null" />
                        <auto-list v-model="exam.subjectId" name="Subject" :param="exam.classTrackId || exam.stageId" placeholder="اختر المادة الدراسية" cols="3" :add="false"
                          :rules="requiredRule" :disabled="!exam.classTrackId && !exam.stageId" />
                      </template>

                      <!-- 🎓 University Classification Fields -->
                      <template v-else-if="exam.institution_type === 'university'">
                        <auto-list v-model="exam.collegeId" name="College" placeholder="اختر الكلية" cols="3" :add="false"
                          :rules="requiredRule" @update:model-value="() => { exam.departmentId = null; exam.specializationId = null; exam.semesterSubjectId = null; }" />
                        <auto-list v-model="exam.departmentId" name="UniversitySection" :param="exam.collegeId" placeholder="اختر القسم الأكاديمي"
                          cols="3" :add="false" :rules="requiredRule" :disabled="!exam.collegeId"
                          @update:model-value="() => { exam.specializationId = null; exam.semesterSubjectId = null; }" />
                        <auto-list v-model="exam.specializationId" name="Specialization" :param="exam.departmentId" placeholder="اختر التخصص الدراسي"
                          cols="3" :add="false" :rules="requiredRule" :disabled="!exam.departmentId"
                          @update:model-value="exam.semesterSubjectId = null" />
                        <auto-list v-model="exam.semesterSubjectId" name="SemesterSubjectBySpec" :param="exam.specializationId"
                          placeholder="اختر المقرر الدراسي" cols="3" :add="false" :rules="requiredRule"
                          :disabled="!exam.specializationId" />
                      </template>

                      <!-- 🏢 Institute & Vocational Training Classification Fields -->
                      <template v-else-if="exam.institution_type === 'institute'">
                        <auto-list v-model="exam.instituteFieldId" name="InstituteField" placeholder="اختر المجال المهني" cols="3" :add="false"
                          :rules="requiredRule"
                          @update:model-value="() => { exam.instituteSpecializationId = null; exam.instituteCurriculumId = null; exam.instituteSubjectId = null; }" />
                        <auto-list v-model="exam.instituteEducationSystemId" name="InstituteEducationSystem" placeholder="اختر النظام التعليمي"
                          cols="3" :add="false" :rules="requiredRule"
                          @update:model-value="() => { exam.instituteSpecializationId = null; exam.instituteCurriculumId = null; exam.instituteSubjectId = null; }" />
                        <auto-list
                          v-model="exam.instituteSpecializationId"
                          name="InstituteSpecialization"
                          :param="{ field: exam.instituteFieldId, education_system: exam.instituteEducationSystemId }"
                          placeholder="اختر التخصص المهني"
                          cols="3"
                          :add="false"
                          :rules="requiredRule"
                          :disabled="!exam.instituteFieldId || !exam.instituteEducationSystemId"
                          @update:model-value="() => { exam.instituteCurriculumId = null; exam.instituteSubjectId = null; }"
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
                          @update:model-value="exam.instituteSubjectId = null"
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
                        <!-- Model Groups Cards -->
                        <div v-for="(group, gIdx) in modelGroups" :key="gIdx" class="pa-5 rounded-2xl border-subtle mb-4 model-group-card">
                          <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                            <div class="d-flex align-center gap-3">
                              <v-avatar size="34" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="rounded-xl">
                                <span class="text-subtitle-2 font-weight-black text-white">{{ gIdx + 1 }}</span>
                              </v-avatar>
                              <div>
                                <span class="font-weight-black text-subtitle-2">{{ group.name || ('المجموعة ' + (gIdx + 1)) }}</span>
                                <span class="text-caption text-medium-emphasis ms-2">({{ group.count }} نماذج)</span>
                              </div>
                              <v-chip size="small" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="font-weight-bold">
                                {{ difficultyLabel(group.difficulty_profile) }}
                              </v-chip>
                            </div>
                            <v-btn v-if="modelGroups.length > 1" icon variant="text" size="small" color="error" @click="removeModelGroup(gIdx)">
                              <v-icon size="20">mdi-trash-can-outline</v-icon>
                            </v-btn>
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

                          <!-- Difficulty Distribution Sliders -->
                          <div class="pa-4 rounded-xl border-subtle mb-3">
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
                          <div class="pa-4 rounded-xl border-subtle mb-3">
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
                    <v-chip size="x-small" :color="exam.exclude_previously_used ? 'warning' : 'grey'" variant="tonal" class="font-weight-bold">
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
            خطوة {{ step }} من 3
          </span>
        </div>

        <v-btn color="primary" class="font-weight-bold px-8" rounded="lg" elevation="2" :loading="generating" @click="nextStep">
          <v-icon start size="20">{{ step === 3 ? 'mdi-check-decagram' : 'mdi-arrow-left' }}</v-icon>
          {{ step === 3 ? 'إنشاء وتوليد الاختبار' : 'التالي' }}
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

      <v-alert type="warning" variant="tonal" density="compact" class="mb-4 rounded-xl">
        <v-icon start size="18">mdi-alert-circle</v-icon>
        يمكنك تعديل نسب المصفوفة لتقليل العجز، أو المتابعة وتوليد أسئلة بديلة من البنك لتغطية النقص.
      </v-alert>

      <template #actions>
        <custom-btn label="تعديل المعايير" variant="text" class="font-weight-bold"
          :click="() => shortageDialog = false" />
        <custom-btn type="add" label="المتابعة وتوليد الاختبار بالأسئلة المتوفرة" color="warning" class="font-weight-bold"
          :click="confirmGenerateWithMocks" />
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
import { useRouter } from 'vue-router'
import { useDataStore } from '@/stores/dataStore'
import { useTheme } from 'vuetify'
import { rules } from '@/utils/validations'
import { examsService } from '@/services/examsService'
import { academicService } from '@/services/academicService'
import api from '@/services/api'

const { proxy } = getCurrentInstance()
const router = useRouter()
const store = useDataStore()
const theme = useTheme()

const requiredRule = [rules.required]

// Stepper Step Indicator Config - NOW 3 STEPS
const step = ref(1)
const step1Form = ref(null)
const generating = ref(false)

const wizardSteps = [
  { value: 1, title: 'إعدادات الاختبار', icon: 'mdi-tune-variant' },
  { value: 2, title: 'مصفوفة المعايير', icon: 'mdi-chart-pie' },
  { value: 3, title: 'المعاينة والتأكيد', icon: 'mdi-clipboard-check-outline' },
]

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
  if (newVal !== oldVal) {
    exam.value.classTrackId = null
  }
})

watch(() => exam.value.countryId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    exam.value.governorateId = null
    exam.value.directorateId = null
    exam.value.regionId = null
    selectedTargetIds.value = []
    loadGovernorates(newVal)
  }
})

watch(() => exam.value.governorateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    exam.value.directorateId = null
    exam.value.regionId = null
  }
})

watch(() => exam.value.directorateId, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    exam.value.regionId = null
  }
})

watch(() => exam.value.target_scope_level, () => {
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

onMounted(async () => {
  if (store.getAll('questions').length === 0) await store.fetchQuestions()
  if (store.getAll('lessons').length === 0) await store.fetchLessons()
  if (store.getAll('units').length === 0) await store.fetchUnits()
  if (store.getAll('years').length === 0) await store.fetchYears()

  if (!exam.value.yearId) {
    const currentYear = years.value.find(y => y.is_current || y.isCurrent)
    if (currentYear) {
      exam.value.yearId = currentYear.id
    } else if (years.value.length > 0) {
      exam.value.yearId = years.value[0].id
    }
  }



  // Load geographic organizations
  await loadGeographicOrgs()
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
      color: 'blue-grey',
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

const confirmGenerateWithMocks = () => {
  shortageDialog.value = false
  performGenerationSequence()
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
      await performGenerationSequence()
    } catch (e) {
      console.error("Shortage check error:", e)
      await performGenerationSequence()
    }
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
.qb-exam-create-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ==========================================================================
   1. Executive Official Hero Banner
   ========================================================================== */
.exam-hero-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.95) 100%);
  border: 1px solid rgba(var(--v-border-color), 0.15);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03);
  backdrop-filter: blur(10px);
}

.hero-icon-box {
  background: rgba(var(--v-theme-primary), 0.12);
  border: 1px solid rgba(var(--v-theme-primary), 0.25);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.15);
}

/* ==========================================================================
   2. Main Container & Section Groups
   ========================================================================== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
}

.section-group-card {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  background: rgb(var(--v-theme-surface));
}

.border-b-subtle {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12) !important;
}

/* ==========================================================================
   3. Premium Connected Stepper Wizard
   ========================================================================== */
.premium-wizard-wrapper {
  position: relative;
  padding: 30px 40px;
  background: rgb(var(--v-theme-surface));
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
}

.premium-wizard-container {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 900px;
  margin: 0 auto;
}

.wizard-progress-track {
  position: absolute;
  top: 24px;
  left: 60px;
  right: 60px;
  height: 3px;
  background: rgba(var(--v-border-color), 0.2);
  z-index: 1;
  border-radius: 999px;
}

.wizard-progress-fill {
  height: 100%;
  background: rgb(var(--v-theme-primary));
  transition: width 0.35s ease;
  border-radius: 999px;
}

.premium-wizard-node {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  width: 180px;
  transition: opacity 0.2s ease;
}

.node-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid rgba(var(--v-border-color), 0.25);
  background: rgb(var(--v-theme-surface));
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.node-title {
  font-size: 15px;
  color: rgb(var(--v-theme-on-surface));
  display: block;
  line-height: 1.4;
  font-weight: 700;
  transition: color 0.2s ease;
}

/* Active Node State */
.premium-wizard-node.is-active .node-icon-wrapper {
  border-color: rgb(var(--v-theme-primary));
  background: rgb(var(--v-theme-primary));
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.25);
}
.premium-wizard-node.is-active .node-title {
  color: rgb(var(--v-theme-primary)) !important;
  font-weight: 900;
}

/* Completed Node State */
.premium-wizard-node.is-completed .node-icon-wrapper {
  border-color: rgb(var(--v-theme-success));
  background: rgb(var(--v-theme-success));
  box-shadow: none;
}

/* Pending Node State */
.premium-wizard-node.is-pending {
  opacity: 0.65;
}
.premium-wizard-node.is-pending:hover {
  opacity: 0.85;
}

/* ==========================================================================
   4. Interactive Visual Selection Cards
   ========================================================================== */
.selection-card,
.model-mode-card {
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-border-color), 0.15);
  border-radius: 14px;
  padding: 16px 20px;
  cursor: pointer;
  transition: border-color 0.2s ease, background 0.2s ease;
  user-select: none;
}

.selection-card:hover,
.model-mode-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.45);
}

.selection-card.is-active,
.model-mode-card.is-active {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: rgba(var(--v-theme-primary), 0.04) !important;
  box-shadow: none !important;
}

.model-mode-card.is-active-warning {
  border-color: rgb(var(--v-theme-warning)) !important;
  background: rgba(var(--v-theme-warning), 0.04) !important;
  box-shadow: none !important;
}

.field-preset-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.15);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.field-preset-card:focus-within {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 1px rgba(var(--v-theme-primary), 0.3);
}

/* ==========================================================================
   5. Segmented Institution Controls & Quick Presets
   ========================================================================== */
.segmented-control {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.15);
}

.segmented-control-btn {
  flex: 1 1 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  border: none;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
}

.segmented-control-btn:hover {
  color: rgb(var(--v-theme-on-surface));
  background: rgba(var(--v-border-color), 0.08);
}

.segmented-control-btn.is-active {
  background: rgb(var(--v-theme-primary)) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}

.preset-pill-btn {
  padding: 2px 10px;
  border-radius: 6px;
  border: 1px solid rgba(var(--v-border-color), 0.18);
  background: rgb(var(--v-theme-surface));
  color: rgba(var(--v-theme-on-surface), 0.75);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.preset-pill-btn:hover {
  border-color: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-primary));
}

.preset-pill-btn.is-active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: #ffffff;
}

/* ==========================================================================
   6. Scope Level Cards Grid
   ========================================================================== */
.scope-grid {
  display: flex;
  gap: 8px;
  width: 100%;
}

.scope-card {
  flex: 1 1 0;
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-border-color), 0.15);
  border-radius: 12px;
  padding: 12px 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  min-width: 100px;
}

.scope-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.45);
  transform: translateY(-1px);
}

.scope-card.is-active {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: rgba(var(--v-theme-primary), 0.06) !important;
  box-shadow: 0 0 0 1px rgb(var(--v-theme-primary));
}

/* ==========================================================================
   7. Schedule Info Ribbon & Model Group Cards
   ========================================================================== */
.schedule-ribbon {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1px solid rgba(var(--v-theme-primary), 0.18);
}

.model-group-card {
  background: rgb(var(--v-theme-surface));
  transition: all 0.25s ease;
}

.model-group-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
}

/* ==========================================================================
   8. Matrix Specification Tabs & Executive Tables
   ========================================================================== */
.matrix-tabs-bar {
  background: rgba(var(--v-theme-background), 0.6);
}

.matrix-tab-btn {
  border: none;
  border-bottom: 3px solid transparent;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.65);
  font-weight: 700;
  font-size: 14px;
  min-width: 160px;
  transition: all 0.2s ease;
}

.matrix-tab-btn:hover {
  color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.04);
}

.matrix-tab-btn.is-active {
  background: rgb(var(--v-theme-surface)) !important;
  border-bottom: 3px solid rgb(var(--v-theme-primary)) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

.executive-table {
  background: rgb(var(--v-theme-surface)) !important;
}

.table-header-row {
  background: rgba(var(--v-theme-background), 0.8) !important;
}

/* ==========================================================================
   9. Executive KPI Certification Cards (Step 3)
   ========================================================================== */
.kpi-cert-card {
  background: rgb(var(--v-theme-surface));
  transition: all 0.2s ease;
}

.kpi-cert-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.kpi-title {
  font-size: 15px;
  color: rgb(var(--v-theme-on-surface));
}

.kpi-metric {
  font-size: 22px;
  line-height: 1.1;
}

/* ==========================================================================
   10. Step 1 Master-Detail Sidebar Navigation
   ========================================================================== */
.step1-sidebar-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  position: sticky;
  top: 24px;
  z-index: 10;
}

.step1-nav-item {
  background: transparent;
  border: 1.5px solid transparent;
  transition: background 0.18s ease;
  user-select: none;
}

.step1-nav-item:hover {
  background: rgba(var(--v-theme-on-surface), 0.04);
}

.step1-nav-item.is-active {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  border-right: 3px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: none !important;
}

.step1-nav-item.has-error {
  border-right: 3px solid rgb(var(--v-theme-error)) !important;
  background: rgba(var(--v-theme-error), 0.07) !important;
  border-color: rgba(var(--v-theme-error), 0.35) !important;
}

.step1-nav-item.has-error:hover {
  background: rgba(var(--v-theme-error), 0.12) !important;
}

.step1-nav-item.has-error.is-active {
  background: rgba(var(--v-theme-error), 0.15) !important;
  border-right: 3px solid rgb(var(--v-theme-error)) !important;
}

@media (max-width: 959px) {
  .step1-sidebar-card {
    position: static;
    margin-bottom: 20px;
  }
  .step1-nav-list {
    flex-direction: row !important;
    overflow-x: auto;
    padding-bottom: 6px;
  }
  .step1-nav-item {
    min-width: 230px;
    border-right: 1.5px solid transparent !important;
    border-bottom: 3px solid transparent;
  }
  .step1-nav-item.is-active {
    border-bottom: 3px solid rgb(var(--v-theme-primary)) !important;
  }
  .step1-nav-item.has-error {
    border-bottom: 3px solid rgb(var(--v-theme-error)) !important;
    border-right: 1.5px solid transparent !important;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .premium-wizard-wrapper {
    padding: 16px 12px;
  }
  .premium-wizard-container {
    flex-wrap: wrap;
    gap: 12px;
  }
  .wizard-progress-track {
    display: none;
  }
  .premium-wizard-node {
    width: 30%;
  }
}

/* ==========================================================================
   Units Distribution Tab Modern Executive Styles (Zero Gray)
   ========================================================================== */
.units-tab-header {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05) 0%, rgba(var(--v-theme-surface), 0.98) 100%);
  border: 1px solid rgba(var(--v-theme-primary), 0.14);
  border-radius: 18px;
  padding: 18px 24px;
}

.units-header-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(var(--v-theme-primary), 0.1);
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.model-groups-selector-hub {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.04) 0%, rgba(var(--v-theme-surface), 0.98) 100%);
  border: 1px solid rgba(var(--v-theme-primary), 0.16);
  border-radius: 18px;
  padding: 16px 20px;
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.04);
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
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14);
  border-radius: 14px;
  padding: 12px 14px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  user-select: none;
}

.group-switch-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(var(--v-theme-primary), 0.1);
}

.group-switch-pill.is-active {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.14) 0%, rgba(var(--v-theme-primary), 0.04) 100%);
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.22);
}

.group-pill-title {
  font-size: 0.92rem;
  color: rgb(var(--v-theme-on-surface));
}

.pill-percentage-badge {
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 0.78rem;
  display: inline-flex;
  align-items: center;
}

.pill-percentage-badge.is-complete {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.pill-percentage-badge.is-pending {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.25);
}

.active-group-hero-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12) 0%, rgba(var(--v-theme-primary), 0.03) 60%, rgb(var(--v-theme-surface)) 100%);
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
  border-right: 5px solid rgb(var(--v-theme-primary));
  border-radius: 18px;
  padding: 18px 24px;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.08);
}

.active-group-hero-avatar {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #2563eb 100%);
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

.modern-empty-state {
  border: 2px dashed rgba(var(--v-theme-primary), 0.25);
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.03) 0%, rgba(var(--v-theme-surface), 0.98) 100%);
  border-radius: 20px;
  padding: 40px 24px;
  text-align: center;
}

.empty-state-icon-box {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: rgba(var(--v-theme-primary), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modern-unit-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.14);
  border-radius: 16px;
  padding: 16px 20px;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.modern-unit-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
  box-shadow: 0 6px 20px rgba(var(--v-theme-primary), 0.08);
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
  opacity: 0.8;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.modern-unit-card.is-excluded {
  background: rgba(var(--v-theme-error), 0.04);
  border-color: rgba(var(--v-theme-error), 0.25);
  opacity: 0.75;
}

.modern-unit-card.is-excluded::before {
  background: rgb(var(--v-theme-error));
}

.unit-stepper-box {
  background: rgba(var(--v-theme-primary), 0.04);
  border: 1px solid rgba(var(--v-theme-primary), 0.12);
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

.unit-balance-alert-card {
  border-radius: 16px;
  padding: 16px 20px;
  border: 1px solid transparent;
}

.unit-balance-alert-card.is-warning {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(var(--v-theme-surface), 0.95) 100%);
  border-color: rgba(245, 158, 11, 0.3);
}

.unit-balance-alert-card.is-success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(var(--v-theme-surface), 0.95) 100%);
  border-color: rgba(16, 185, 129, 0.3);
}

.term-header-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.95) 100%);
  border: 1px solid rgba(var(--v-theme-primary), 0.15);
  border-right: 3px solid rgb(var(--v-theme-primary));
  padding: 8px 16px;
  border-radius: 12px;
}


.modern-type-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.14);
  border-radius: 16px;
  padding: 16px 20px;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.modern-type-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
  box-shadow: 0 6px 20px rgba(var(--v-theme-primary), 0.08);
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
  opacity: 0.8;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}


/* ==========================================================================
   Exam Total Marks & Question Types Metrics Styles (Zero Gray)
   ========================================================================== */
.exam-total-marks-card {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%);
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
  border-right: 5px solid rgb(var(--v-theme-primary));
  border-radius: 18px;
  padding: 16px 20px;
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.05);
}

.total-marks-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.score-input-wrapper {
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25);
}

.score-number-input {
  width: 60px;
  text-align: center;
  font-size: 1.15rem;
  color: rgb(var(--v-theme-primary));
  outline: none;
  border: none;
  background: transparent;
}

.type-metrics-bar {
  background: rgba(var(--v-theme-primary), 0.04);
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  padding: 8px 12px;
}

.type-metric-item {
  flex: 1;
}

</style>
