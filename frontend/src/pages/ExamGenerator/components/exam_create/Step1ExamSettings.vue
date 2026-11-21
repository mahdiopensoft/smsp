<template>
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
                        @click="$emit('update:activeStep1Section', item.id)"
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

</template>

<script setup>
import { ref } from 'vue'
import { rules } from '@/utils/validations'
import { difficultyColor, difficultyLabel } from '../../composables/examHelpers'

const step1Form = ref(null)

const props = defineProps({
  exam: {
    type: Object,
    required: true
  },
  activeStep1Section: {
    type: Number,
    default: 1
  },
  validatedOnce: {
    type: Boolean,
    default: false
  },
  invalidSectionsCount: {
    type: Number,
    default: 0
  },
  isSectionValid: {
    type: Function,
    required: true
  },
  step1NavItems: {
    type: Array,
    required: true
  },
  isLoadingForEdit: {
    type: Boolean,
    default: false
  },
  requiredRule: {
    type: [Array, Function],
    default: () => [v => !!v || 'هذا الحقل مطلوب']
  },
  modelsMode: {
    type: String,
    default: 'uniform'
  },
  totalModelsCount: {
    type: Number,
    default: 1
  },
  modelGroups: {
    type: Array,
    default: () => []
  },
  difficultyItems: {
    type: Array,
    default: () => []
  },
  difficultyProfiles: {
    type: Array,
    default: () => []
  },
  governoratesList: {
    type: Array,
    default: () => []
  },
  loadingGeoData: {
    type: Boolean,
    default: false
  },
  loadingSchools: {
    type: Boolean,
    default: false
  },
  onInstitutionTypeToggle: {
    type: Function,
    required: true
  },
  setModelsMode: {
    type: Function,
    required: true
  },
  setModelsCount: {
    type: Function,
    required: true
  },
  addModelGroup: {
    type: Function,
    required: true
  },
  removeModelGroup: {
    type: Function,
    required: true
  },
  applyDifficultyPreset: {
    type: Function,
    required: true
  },
  updateGroupDiff: {
    type: Function,
    required: true
  },
  stepGroupDiff: {
    type: Function,
    required: true
  },
  groupDiffTotal: {
    type: Function,
    required: true
  },
  onGroupScopeLevelChange: {
    type: Function,
    required: true
  },
  onGroupFilterGovForSchool: {
    type: Function,
    required: true
  },
  onGroupFilterDirForSchool: {
    type: Function,
    required: true
  },
  getDirectoratesForGroup: {
    type: Function,
    required: true
  },
  getDirectoratesForFilterGov: {
    type: Function,
    required: true
  },
  isGroupSchoolDisabled: {
    type: Function,
    required: true
  }
})

defineEmits(['update:activeStep1Section'])

defineExpose({
  validate: () => step1Form.value?.validate(),
  step1Form
})
</script>
