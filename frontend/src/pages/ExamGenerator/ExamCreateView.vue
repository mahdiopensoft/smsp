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
                        {{ activeStep1Section }} / 5
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
                        توجد حقول إجبارية غير مكتملة في الأقسام المحددة باللون الأحمر ({{ invalidSectionsCount }} من 5 بحاجة للاستكمال).
                      </span>
                    </div>
                  </v-alert>
                  <!-- Section 1: Setup Mode & Schedule -->
                  <div v-show="activeStep1Section === 1" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-5">
                      <v-avatar size="40" color="primary" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-tune-variant</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">1. نمط الإعداد والربط الهيكلي</h4>
                        <span class="text-caption text-medium-emphasis">تحديد طريقة بناء مواصفات الاختبار ومصدر البيانات</span>
                      </div>
                    </div>

                    <!-- Primary Choice: New Setup vs Template Side-by-Side (متقابلة وواضحة) -->
                    <v-row dense class="mb-4">
                      <!-- Card A: New Exam Setup -->
                      <v-col cols="12" md="6">
                        <div
                          class="selection-card h-100 pa-4 rounded-xl cursor-pointer"
                          :class="{ 'is-active': settingsMode === 'new' }"
                          @click="settingsMode = 'new'"
                        >
                          <div class="d-flex align-start gap-3">
                            <v-avatar size="40" :color="settingsMode === 'new' ? 'primary' : 'surface-variant'" :variant="settingsMode === 'new' ? 'flat' : 'tonal'" class="rounded-lg flex-shrink-0">
                              <v-icon size="20" :color="settingsMode === 'new' ? 'white' : 'medium-emphasis'">mdi-plus-circle-outline</v-icon>
                            </v-avatar>
                            <div class="flex-grow-1">
                              <div class="d-flex align-center justify-space-between mb-1">
                                <span class="font-weight-black text-subtitle-1">إعداد جديد ومخصص</span>
                                <v-icon :color="settingsMode === 'new' ? 'primary' : 'medium-emphasis'" size="20">
                                  {{ settingsMode === 'new' ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                                </v-icon>
                              </div>
                              <p class="text-caption text-medium-emphasis mb-0 leading-relaxed">
                                تحديد المعايير، الأوزان النسبية، ومستويات الصعوبة بشكل مباشر وتفاعلي لهذا الاختبار.
                              </p>
                            </div>
                          </div>
                        </div>
                      </v-col>

                      <!-- Card B: Template Setup -->
                      <v-col cols="12" md="6">
                        <div
                          class="selection-card h-100 pa-4 rounded-xl cursor-pointer"
                          :class="{ 'is-active': settingsMode === 'template' }"
                          @click="settingsMode = 'template'"
                        >
                          <div class="d-flex align-start gap-3">
                            <v-avatar size="40" :color="settingsMode === 'template' ? 'secondary' : 'surface-variant'" :variant="settingsMode === 'template' ? 'flat' : 'tonal'" class="rounded-lg flex-shrink-0">
                              <v-icon size="20" :color="settingsMode === 'template' ? 'white' : 'medium-emphasis'">mdi-file-document-outline</v-icon>
                            </v-avatar>
                            <div class="flex-grow-1">
                              <div class="d-flex align-center justify-space-between mb-1">
                                <span class="font-weight-black text-subtitle-1">استدعاء قالب معتمد</span>
                                <v-icon :color="settingsMode === 'template' ? 'secondary' : 'medium-emphasis'" size="20">
                                  {{ settingsMode === 'template' ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                                </v-icon>
                              </div>
                              <p class="text-caption text-medium-emphasis mb-0 leading-relaxed">
                                تحميل مصفوفة مواصفات سابقة تم اعتمادها لتطبيق معاييرها وأوزانها فوراً وتوفير الوقت.
                              </p>
                            </div>
                          </div>
                        </div>
                      </v-col>
                    </v-row>

                    <!-- Sub-options for Template Mode -->
                    <v-expand-transition>
                      <div v-if="settingsMode === 'template'" class="pt-3">
                        <div class="d-flex align-center gap-2 mb-2">
                          <v-icon color="secondary" size="18">mdi-file-download-outline</v-icon>
                          <span class="text-subtitle-2 font-weight-bold">اختر القالب المعتمد لتطبيقه:</span>
                        </div>
                        <v-autocomplete
                          v-model="selectedTemplate"
                          :items="savedTemplates"
                          item-title="name"
                          item-value="id"
                          placeholder="ابحث واختر من القوالب المعتمدة المحفوظة..."
                          prepend-inner-icon="mdi-file-document-outline"
                          variant="outlined"
                          density="compact"
                          rounded="lg"
                          return-object
                          hide-details="auto"
                          :rules="settingsMode === 'template' ? [v => !!v || 'يرجى اختيار القالب المعتمد'] : []"
                          @update:model-value="applyTemplate"
                        >
                          <template #append>
                            <v-btn icon variant="text" size="small" color="error" v-if="selectedTemplate" @click.stop="deleteTemplate(selectedTemplate.id)">
                              <v-icon size="18">mdi-delete</v-icon>
                            </v-btn>
                          </template>
                        </v-autocomplete>
                      </div>
                    </v-expand-transition>

                    <!-- Sub-options for New Mode (Subject Assignment Method) -->
                    <v-expand-transition>
                      <div v-if="settingsMode === 'new'" class="pt-3">
                        <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                          <div>
                            <div class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
                              <v-icon size="18" color="primary">mdi-source-branch</v-icon>
                              طريقة تعيين المقرر الدراسي للاختبار:
                            </div>
                            <div class="text-caption text-medium-emphasis">هل تريد تحديد المادة يدوياً من الشجرة الأكاديمية أم استيرادها من جدول امتحانات مجدول؟</div>
                          </div>
                          <v-btn-toggle
                            v-model="scheduleMode"
                            mandatory
                            color="primary"
                            variant="outlined"
                            density="comfortable"
                            rounded="lg"
                          >
                            <v-btn value="manual" class="font-weight-bold" prepend-icon="mdi-cursor-default-click">
                              تحديد يدوي مباشر
                            </v-btn>
                            <v-btn value="schedule" class="font-weight-bold" prepend-icon="mdi-calendar-clock">
                              من جدول الاختبارات المعتمد
                            </v-btn>
                          </v-btn-toggle>
                        </div>

                        <!-- Schedule Dropdown if scheduleMode === 'schedule' -->
                        <v-expand-transition>
                          <div v-if="scheduleMode === 'schedule'" class="mt-3">
                            <v-select
                              v-model="exam.examScheduleId"
                              :items="enrichedSchedules"
                              item-title="displayLabel"
                              item-value="id"
                              placeholder="اختر من جدول الاختبارات المتاح..."
                              prepend-inner-icon="mdi-calendar-clock"
                              clearable
                              density="compact"
                              variant="outlined"
                              rounded="lg"
                              :rules="scheduleMode === 'schedule' ? [v => !!v || 'يرجى اختيار جدول الاختبار'] : []"
                              hide-details="auto"
                              @update:model-value="onScheduleChange"
                            />
                          </div>
                        </v-expand-transition>
                      </div>
                    </v-expand-transition>
                  </div>

                  <!-- Section 2: Academic Classification Scope -->
                  <div v-show="activeStep1Section === 2" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-4">
                      <v-avatar size="40" color="secondary" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-school-outline</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">2. النطاق والتصنيف الأكاديمي</h4>
                        <span class="text-caption text-medium-emphasis">تحديد الفترة، القسم، الصف، والمادة أو المقرر المستهدف</span>
                      </div>
                    </div>

                    <!-- Case A: Manual Selection -->
                    <div v-if="settingsMode === 'new' && scheduleMode === 'manual'">
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
                        <template v-if="exam.institution_type === 'university'">
                          <auto-list v-model="exam.collegeId" name="College" placeholder="الكلية الجامعية" cols="3" :add="false"
                            :rules="requiredRule" @update:model-value="exam.departmentId = null" />
                          <auto-list v-model="exam.departmentId" name="DepartmentByCollege" :param="exam.collegeId" placeholder="القسم الأكاديمي"
                            cols="3" :add="false" :rules="requiredRule" :disabled="!exam.collegeId" @update:model-value="exam.specializationId = null" />
                          <auto-list v-model="exam.specializationId" name="Specialization" :param="exam.departmentId" placeholder="التخصص والبرنامج"
                            cols="3" :add="false" :rules="requiredRule" :disabled="!exam.departmentId" />
                          <auto-list v-model="exam.semesterSubjectId" name="SemesterSubject" :param="exam.specializationId" placeholder="مقرر الفصل الجامعي"
                            cols="3" :add="false" :rules="requiredRule" />
                        </template>

                        <!-- 🏢 Institute Classification Fields -->
                        <template v-if="exam.institution_type === 'institute'">
                          <auto-list
                            v-model="exam.instituteFieldId"
                            name="InstituteField"
                            placeholder="المجال المهني"
                            cols="3"
                            :add="false"
                            :rules="requiredRule"
                            @update:model-value="() => { exam.instituteEducationSystemId = null; exam.instituteSpecializationId = null; exam.instituteCurriculumId = null; exam.instituteSubjectId = null; }"
                          />
                          <auto-list
                            v-model="exam.instituteEducationSystemId"
                            name="InstituteEducationSystem"
                            :param="exam.instituteFieldId"
                            placeholder="نظام التعليم"
                            cols="3"
                            :add="false"
                            :rules="requiredRule"
                            :disabled="!exam.instituteFieldId"
                            @update:model-value="() => { exam.instituteSpecializationId = null; exam.instituteCurriculumId = null; exam.instituteSubjectId = null; }"
                          />
                          <auto-list
                            v-model="exam.instituteSpecializationId"
                            name="InstituteSpecialization"
                            :param="{ field: exam.instituteFieldId, education_system: exam.instituteEducationSystemId }"
                            placeholder="التخصص المهني"
                            cols="3"
                            :add="false"
                            :rules="requiredRule"
                            :disabled="!exam.instituteEducationSystemId"
                            @update:model-value="() => { exam.instituteCurriculumId = null; exam.instituteSubjectId = null; }"
                          />
                          <auto-list
                            v-model="exam.instituteCurriculumId"
                            name="InstituteCurriculum"
                            :param="exam.instituteSpecializationId"
                            placeholder="الخطة الدراسية"
                            cols="3"
                            :add="false"
                            :rules="requiredRule"
                            :disabled="!exam.instituteSpecializationId"
                            @update:model-value="exam.instituteSubjectId = null"
                          />
                          <auto-list
                            v-model="exam.instituteSubjectId"
                            name="InstituteSubject"
                            :param="exam.instituteCurriculumId"
                            placeholder="المادة التدريبية"
                            cols="3"
                            :add="false"
                            :rules="requiredRule"
                            :disabled="!exam.instituteCurriculumId"
                          />
                        </template>
                      </v-row>
                    </div>

                    <!-- Case B: From Schedule -->
                    <div v-else-if="scheduleMode === 'schedule'">
                      <div class="pa-5 rounded-xl border-subtle text-center">
                        <v-avatar size="52" color="primary" variant="tonal" class="mb-3 rounded-2xl">
                          <v-icon size="28">mdi-calendar-check</v-icon>
                        </v-avatar>
                        <h4 class="text-subtitle-1 font-weight-black mb-1">البيانات الأكاديمية مرتبطة بجدول الاختبارات المعتمد</h4>
                        <p class="text-caption text-medium-emphasis mb-4">
                          تم استيراد المادة والصف والفترة الامتحانية تلقائياً بناءً على جدول الامتحانات المختار في القسم الأول.
                        </p>

                        <div v-if="selectedScheduleInfo" class="pa-4 rounded-xl schedule-ribbon d-flex flex-wrap gap-2 justify-center align-center mb-4">
                          <v-chip variant="tonal" color="primary" class="font-weight-bold" prepend-icon="mdi-calendar-range">
                            {{ selectedScheduleInfo.periodName }}
                          </v-chip>
                          <v-chip variant="tonal" color="secondary" class="font-weight-bold" prepend-icon="mdi-book">
                            {{ selectedScheduleInfo.subjectName }}
                          </v-chip>
                          <v-chip variant="tonal" color="info" class="font-weight-bold" prepend-icon="mdi-school">
                            {{ selectedScheduleInfo.levelName }}
                          </v-chip>
                          <v-chip variant="tonal" color="warning" class="font-weight-bold" prepend-icon="mdi-shape">
                            {{ selectedScheduleInfo.branchName }}
                          </v-chip>
                          <v-chip variant="tonal" color="success" class="font-weight-bold" prepend-icon="mdi-calendar">
                            {{ selectedScheduleInfo.date }}
                          </v-chip>
                        </div>

                        <v-btn variant="tonal" color="primary" size="small" class="font-weight-bold" prepend-icon="mdi-tune" @click="goToStep1Section(1)">
                          تغيير جدول الاختبارات من القسم الأول
                        </v-btn>
                      </div>
                    </div>

                    <!-- Case C: From Template -->
                    <div v-else>
                      <div class="pa-5 rounded-xl border-subtle text-center">
                        <v-avatar size="52" color="secondary" variant="tonal" class="mb-3 rounded-2xl">
                          <v-icon size="28">mdi-file-document-check-outline</v-icon>
                        </v-avatar>
                        <h4 class="text-subtitle-1 font-weight-black mb-1">بيانات المقرر مستوردة من القالب المعتمد</h4>
                        <p class="text-caption text-medium-emphasis mb-4">
                          {{ selectedTemplate ? `تم استدعاء مصفوفة المواصفات والمقرر من القالب: ${selectedTemplate.name}` : 'يرجى اختيار القالب من القسم الأول' }}
                        </p>
                        <v-btn variant="tonal" color="secondary" size="small" class="font-weight-bold" prepend-icon="mdi-tune" @click="goToStep1Section(1)">
                          تعديل اختيار القالب من القسم الأول
                        </v-btn>
                      </div>
                    </div>
                  </div>

                  <!-- Section 3: Technical Details & Capacity -->
                  <div v-show="activeStep1Section === 3" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-5">
                      <v-avatar size="40" color="info" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-card-account-details-outline</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">3. تفاصيل وسعة ورقة الاختبار</h4>
                        <span class="text-caption text-medium-emphasis">تحديد عنوان ورقة الاختبار، رصيد الأسئلة، وإعدادات مكافحة التكرار</span>
                      </div>
                    </div>

                    <v-row dense class="mb-3">
                      <custom-text-field v-model="exam.title" cols="12" label="عنوان الاختبار الرسمي" icon="text"
                        :rules="[rules.required]" />

                      <!-- Questions Count: Field on one side, Quick Presets directly opposite (مقابل الحقل وبشكل جميل) -->
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
                      <v-col cols="12" md="6" class="d-flex align-center gap-1.5 flex-wrap pt-md-2">
                        <span class="text-caption font-weight-bold text-medium-emphasis me-1">سريع:</span>
                        <v-btn
                          v-for="qCount in [20, 30, 40, 50]"
                          :key="qCount"
                          size="small"
                          rounded="pill"
                          :color="exam.questionsCount === qCount ? 'primary' : undefined"
                          :variant="exam.questionsCount === qCount ? 'flat' : 'tonal'"
                          class="font-weight-bold px-2.5"
                          @click="setQuestionsCount(qCount)"
                        >
                          {{ qCount }} سؤال
                        </v-btn>
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

                  <!-- Section 4: Geographic Target Scope (Segmented Controls Aligned) -->
                  <div v-show="activeStep1Section === 4" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-5">
                      <v-avatar size="40" color="deep-purple" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-map-marker-radius</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">4. النطاق الجغرافي للاختبار</h4>
                        <span class="text-caption text-medium-emphasis">حدد مستوى الاستهداف والمناطق أو المؤسسات المشمولة في هذا الاختبار</span>
                      </div>
                    </div>

                    <!-- Country and Scope Level Options directly opposite each other on the same row -->
                    <v-row dense class="align-center mb-2">
                      <auto-list v-model="exam.countryId" name="Country" placeholder="اختر الدولة" cols="4" :add="false" />
                      <v-col cols="12" md="8">
                        <v-btn-toggle
                          v-model="exam.target_scope_level"
                          mandatory
                          color="primary"
                          variant="outlined"
                          density="comfortable"
                          rounded="lg"
                          class="w-100 d-flex flex-wrap"
                          @update:model-value="(val) => { if (val === 'all') selectedTargetIds = []; }"
                        >
                          <v-btn value="all" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-earth">
                            كافة المناطق (شامل)
                          </v-btn>
                          <v-btn value="governorate" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-city-variant-outline">
                            محافظات محددة
                          </v-btn>
                          <v-btn value="directorate" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-map-marker-radius">
                            مديريات محددة
                          </v-btn>
                          <v-btn value="school" class="flex-grow-1 font-weight-bold" prepend-icon="mdi-school-outline">
                            مدارس / مراكز
                          </v-btn>
                        </v-btn-toggle>
                      </v-col>
                    </v-row>

                    <v-expand-transition>
                      <div v-if="exam.target_scope_level !== 'all'" class="mt-3 pt-4 border-t border-subtle">
                        <v-row dense>
                          <!-- محافظات محددة -->
                          <v-col cols="12" v-if="exam.target_scope_level === 'governorate'">
                            <v-autocomplete
                              v-model="selectedTargetIds"
                              :items="governoratesList"
                              item-title="name_ar"
                              item-value="id"
                              label="المحافظات المستهدفة للاختبار *"
                              placeholder="اختر المحافظات (أمانة العاصمة، صنعاء، تعز، الحديدة...)"
                              cols="12"
                              multiple
                              chips
                              closable-chips
                              variant="outlined"
                              density="compact"
                              rounded="lg"
                              hide-details="auto"
                              :rules="exam.target_scope_level === 'governorate' ? [v => (Array.isArray(v) && v.length > 0) || 'يرجى تحديد محافظة واحدة على الأقل'] : []"
                              prepend-inner-icon="mdi-city-variant-outline"
                              :loading="loadingGeographicOrgs"
                            />
                          </v-col>

                          <!-- مديريات محددة -->
                          <v-col cols="12" v-if="exam.target_scope_level === 'directorate'">
                            <v-row dense>
                              <v-col cols="12" md="4">
                                <v-autocomplete
                                  v-model="selectedGovernorateForFilter"
                                  :items="governoratesList"
                                  item-title="name_ar"
                                  item-value="id"
                                  label="تصفية حسب المحافظة (اختياري)"
                                  placeholder="اختر المحافظة لتصفية المديريات..."
                                  clearable
                                  variant="outlined"
                                  density="compact"
                                  rounded="lg"
                                  hide-details="auto"
                                  prepend-inner-icon="mdi-filter-variant"
                                  :loading="loadingGeographicOrgs"
                                />
                              </v-col>
                              <v-col cols="12" md="8">
                                <v-autocomplete
                                  v-model="selectedTargetIds"
                                  :items="availableDirectorates"
                                  item-title="name_ar"
                                  item-value="id"
                                  label="المديريات المستهدفة للاختبار *"
                                  placeholder="اختر المديريات المستهدفة..."
                                  multiple
                                  chips
                                  closable-chips
                                  variant="outlined"
                                  density="compact"
                                  rounded="lg"
                                  hide-details="auto"
                                  :rules="exam.target_scope_level === 'directorate' ? [v => (Array.isArray(v) && v.length > 0) || 'يرجى تحديد مديرية واحدة على الأقل'] : []"
                                  prepend-inner-icon="mdi-map-marker-radius"
                                  :loading="loadingGeographicOrgs"
                                />
                              </v-col>
                            </v-row>
                          </v-col>

                          <!-- مدارس محددة -->
                          <v-col cols="12" v-if="exam.target_scope_level === 'school'">
                            <v-row dense>
                              <v-col cols="12" md="3">
                                <v-autocomplete
                                  v-model="selectedGovernorateForFilter"
                                  :items="governoratesList"
                                  item-title="name_ar"
                                  item-value="id"
                                  label="المحافظة (تصفية اختيارية)"
                                  placeholder="المحافظة..."
                                  clearable
                                  variant="outlined"
                                  density="compact"
                                  rounded="lg"
                                  hide-details="auto"
                                  @update:model-value="selectedDirectorateForFilter = null"
                                  :loading="loadingGeographicOrgs"
                                />
                              </v-col>
                              <v-col cols="12" md="3">
                                <v-autocomplete
                                  v-model="selectedDirectorateForFilter"
                                  :items="availableDirectorates"
                                  item-title="name_ar"
                                  item-value="id"
                                  label="المديرية (تصفية اختيارية)"
                                  placeholder="المديرية..."
                                  clearable
                                  variant="outlined"
                                  density="compact"
                                  rounded="lg"
                                  hide-details="auto"
                                  :disabled="!selectedGovernorateForFilter"
                                  :loading="loadingGeographicOrgs"
                                />
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-autocomplete
                                  v-model="selectedTargetIds"
                                  :items="availableSchools"
                                  item-title="name_ar"
                                  item-value="id"
                                  label="المدارس / المؤسسات المستهدفة *"
                                  placeholder="ابحث بالاسم أو رقم الفرع للمدرسة..."
                                  multiple
                                  chips
                                  closable-chips
                                  variant="outlined"
                                  density="compact"
                                  rounded="lg"
                                  hide-details="auto"
                                  :rules="exam.target_scope_level === 'school' ? [v => (Array.isArray(v) && v.length > 0) || 'يرجى تحديد مؤسسة/مدرسة واحدة على الأقل'] : []"
                                  prepend-inner-icon="mdi-school"
                                  :loading="loadingGeographicOrgs"
                                />
                              </v-col>
                            </v-row>
                          </v-col>
                        </v-row>

                        <!-- Selected Targets Summary Badge -->
                        <div v-if="selectedTargetIds && selectedTargetIds.length > 0" class="mt-3 pa-3 rounded-lg border-subtle d-flex align-center justify-space-between flex-wrap gap-2">
                          <div class="d-flex align-center gap-2">
                            <v-icon size="18" color="success">mdi-check-circle</v-icon>
                            <span class="text-caption font-weight-bold">
                              تم اعتماد تحديد {{ selectedTargetIds.length }} منطقة / مؤسسة مستهدفة في نطاق الاختبار
                            </span>
                          </div>
                          <v-btn size="x-small" variant="text" color="error" class="font-weight-bold" @click="selectedTargetIds = []">
                            مسح التحديد
                          </v-btn>
                        </div>
                      </div>
                    </v-expand-transition>
                  </div>

                  <!-- Section 5: Advanced Models Configuration -->
                  <div v-show="activeStep1Section === 5" class="section-group-card pa-6 rounded-2xl mb-6">
                    <div class="d-flex align-center gap-3 mb-5">
                      <v-avatar size="40" color="warning" variant="tonal" class="rounded-xl">
                        <v-icon size="22">mdi-file-multiple-outline</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1 font-weight-black mb-0">5. إعدادات النماذج التوليدية</h4>
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
                                <span class="font-weight-black text-subtitle-2">المجموعة {{ gIdx + 1 }}</span>
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
                            <span class="text-caption font-weight-bold text-medium-emphasis mb-3 d-block">
                              <v-icon size="14" class="me-1">mdi-speedometer</v-icon>
                              توزيع أوزان الصعوبة للمجموعة {{ gIdx + 1 }}:
                            </span>
                            <v-row dense>
                              <v-col v-for="diff in difficultyItems" :key="diff.key" cols="12" md="4">
                                <div class="pa-3 rounded-lg border-subtle">
                                  <div class="d-flex align-center justify-space-between mb-1">
                                    <span class="text-caption font-weight-bold">{{ diff.label }}</span>
                                    <v-chip size="x-small" :color="diff.color" variant="tonal" class="font-weight-bold">
                                      {{ group.difficulty_distribution[diff.key] }}%
                                    </v-chip>
                                  </div>
                                  <v-slider
                                    v-model="group.difficulty_distribution[diff.key]"
                                    :min="0" :max="100" :step="5"
                                    :color="diff.color"
                                    hide-details
                                    thumb-size="14"
                                    track-size="5"
                                  />
                                </div>
                              </v-col>
                            </v-row>
                            <v-alert v-if="groupDiffTotal(group) !== 100" type="warning" density="compact" variant="tonal" class="mt-3 rounded-lg">
                              إجمالي نسب الصعوبة: {{ groupDiffTotal(group) }}% (يجب أن يعادل 100%)
                            </v-alert>
                          </div>

                          <!-- Region Assignment for this group -->
                          <div v-if="exam.target_scope_level !== 'all' && selectedTargetIds.length > 0" class="pa-4 rounded-xl border-subtle">
                            <div class="d-flex align-center justify-space-between mb-2 flex-wrap gap-1">
                              <span class="text-caption font-weight-bold text-medium-emphasis d-flex align-center">
                                <v-icon size="16" class="me-1" color="primary">mdi-map-marker-multiple</v-icon>
                                المناطق المستهدفة حصرياً بهذه المجموعة:
                              </span>
                              <span class="text-caption text-primary font-weight-bold">
                                (متاح {{ targetOptionsForGroups.length }} منطقة محددة من النطاق الجغرافي للاختبار)
                              </span>
                            </div>
                            <v-autocomplete
                              v-model="group.assigned_target_ids"
                              :items="targetOptionsForGroups"
                              item-title="name"
                              item-value="id"
                              variant="outlined"
                              density="compact"
                              rounded="lg"
                              hide-details
                              multiple
                              chips
                              closable-chips
                              placeholder="اختر من المناطق المحددة للاختبار لهذه المجموعة..."
                              no-data-text="لا توجد مناطق متاحة — حدد المناطق أولاً في النطاق الجغرافي للاختبار"
                            />
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
            <div class="d-flex align-center justify-space-between mb-6 flex-wrap gap-2">
              <h3 class="text-h5 font-weight-black mb-0 d-flex align-center gap-2">
                <v-icon color="secondary">mdi-chart-pie</v-icon>
                مصفوفة المعايير والمواصفات
              </h3>
              <div class="d-flex align-center gap-2">
                <custom-btn type="add" label="تطبيق التوزيع القياسي" icon="mdi-tune-vertical" variant="tonal"
                  color="primary" class="font-weight-bold" :click="applyStandardCriteria" />
              </div>
            </div>

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
                  <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-2">
                    <div>
                      <h4 class="text-subtitle-1 font-weight-black mb-0">
                        {{ exam.institution_type === 'university' ? 'توزيع الأسئلة على مفردات وموضوعات المقرر' : 'توزيع الأسئلة على الوحدات الدراسية' }}
                      </h4>
                      <span class="text-caption text-medium-emphasis">تحديد الأوزان النسبية للوحدات بحيث يكون المجموع 100%</span>
                    </div>
                    <custom-btn label="توزيع متساوٍ" icon="mdi-scale-balance" variant="tonal" color="primary" class="font-weight-bold"
                      :click="() => autoDistribute('units')" />
                  </div>

                  <template v-for="termId in [1, 2, 3]" :key="termId">
                    <div v-if="blueprint.units.some(u => u.term === termId)" class="mb-4">
                      <v-divider v-if="termId > 1" class="my-4 opacity-20" />
                      <div class="d-flex align-center justify-space-between mb-3">
                        <h5 class="text-subtitle-2 font-weight-black text-primary d-flex align-center gap-2 mb-0">
                          <v-icon size="18">mdi-book-open-page-variant</v-icon>
                          <span v-if="termId === 1">الفصل الدراسي الأول</span>
                          <span v-else-if="termId === 2">الفصل الدراسي الثاني</span>
                          <span v-else>{{ exam.institution_type === 'university' ? 'موضوعات عامة' : 'وحدات عامة' }}</span>
                        </h5>
                      </div>
                      <v-row dense>
                        <v-col v-for="unit in blueprint.units.filter(u => u.term === termId)" :key="unit.id" cols="12"
                          md="6">
                          <div class="pa-4 rounded-xl border-subtle mb-2" :style="unit.isExcluded ? 'background: rgba(var(--v-theme-error), 0.08); border-color: rgba(var(--v-theme-error), 0.3);' : ''">
                            <div class="d-flex justify-space-between align-start mb-1">
                              <div>
                                <div class="font-weight-bold text-subtitle-2 d-flex align-center gap-1">
                                  <span>{{ unit.name }}</span>
                                  <v-chip v-if="unit.isExcluded" size="x-small" color="error" variant="tonal" class="font-weight-bold">
                                    <v-icon start size="12">mdi-cancel</v-icon>
                                    محذوف من الاختبارات
                                  </v-chip>
                                </div>
                                <div class="d-flex align-center mt-1 gap-2 flex-wrap">
                                  <custom-btn :label="exam.institution_type === 'university' ? 'محتوى المفردة' : 'محتوى الوحدة'" variant="tonal" color="info" class="font-weight-bold"
                                    :click="() => openUnitDetails(unit.id, unit.name)" />
                                  <span class="text-caption text-medium-emphasis">({{ getUnitLessonsCount(unit.id) }}
                                    {{ exam.institution_type === 'university' ? 'محاضرة' : 'درس' }}،
                                    {{ getUnitApprovedQuestionsCount(unit.id) }} سؤال)</span>
                                </div>
                              </div>
                              <v-chip size="small" :color="unit.isExcluded ? 'error' : 'primary'" variant="tonal" class="font-weight-bold">{{
                                unit.percentage }}%</v-chip>
                            </div>
                            <v-slider :model-value="unit.percentage" :disabled="unit.isExcluded" @update:model-value="(val) => {
                              const realIndex = blueprint.units.findIndex(u => u.id === unit.id);
                              updateDistribution(blueprint.units, realIndex, val);
                            }" :min="0" :max="100" :step="5" :color="unit.isExcluded ? 'error' : 'primary'" hide-details thumb-size="14"
                              track-size="6" class="mt-2" />
                          </div>
                        </v-col>
                      </v-row>
                    </div>
                  </template>

                  <v-alert v-if="totalUnitsPercentage !== 100"
                    :type="totalUnitsPercentage === 100 ? 'success' : 'warning'" density="compact" variant="tonal"
                    class="mt-4 rounded-xl">
                    إجمالي النسبة الحالية: {{ totalUnitsPercentage }}% (يجب أن يعادل 100% تماماً)
                  </v-alert>
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
                            <th class="font-weight-bold" v-if="exam.target_scope_level !== 'all'">المناطق المستهدفة</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(group, gIdx) in modelGroups" :key="gIdx">
                            <td class="font-weight-bold">مجموعة {{ gIdx + 1 }}</td>
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
                            <td v-if="exam.target_scope_level !== 'all'" class="text-caption">
                              <span v-if="group.assigned_target_ids && group.assigned_target_ids.length > 0" class="font-weight-bold text-primary">
                                {{ getAssignedTargetNames(group.assigned_target_ids) }}
                              </span>
                              <span v-else class="text-medium-emphasis">غير مخصص (جميع المناطق المستهدفة)</span>
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
                        :label="bloomEnabled ? 'مفعّل' : 'معطّل'"
                      />
                    </div>
                    <custom-btn v-if="bloomEnabled" label="توزيع متساوٍ" icon="mdi-scale-balance" variant="tonal" color="primary" class="font-weight-bold"
                      :click="() => autoDistribute('bloom')" />
                  </div>

                  <v-alert v-if="!bloomEnabled" type="info" variant="tonal" density="compact" class="rounded-xl mb-4">
                    <v-icon start>mdi-information</v-icon>
                    مستويات بلوم معطلة — سيتم توزيع الأسئلة حسب الصعوبة والوحدات فقط دون إلزام بلوم
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
                  <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-2">
                    <div>
                      <h4 class="text-subtitle-1 font-weight-black mb-0">توزيع أنواع الأسئلة</h4>
                      <span class="text-caption text-medium-emphasis">تحديد نسبة كل نوع من أنواع الأسئلة (اختيار من متعدد، صح وخطأ، وغيرها)</span>
                    </div>
                    <custom-btn label="توزيع متساوٍ" icon="mdi-scale-balance" variant="tonal" color="primary" class="font-weight-bold"
                      :click="() => autoDistribute('types')" />
                  </div>

                  <v-row dense>
                    <v-col v-for="(type, index) in blueprint.types" :key="index" cols="12" md="6">
                      <div class="pa-4 rounded-xl border-subtle mb-2">
                        <div class="d-flex justify-space-between align-center mb-1">
                          <span class="font-weight-bold">{{ type.name }}</span>
                          <v-chip size="small" :color="type.color" variant="tonal" class="font-weight-bold">{{
                            type.percentage }}%</v-chip>
                        </div>
                        <v-slider :model-value="type.percentage"
                          @update:model-value="(val) => updateDistribution(blueprint.types, index, val)" :min="0"
                          :max="100" :step="5" :color="type.color" hide-details thumb-size="14" track-size="6"
                          class="mt-2" />
                      </div>
                    </v-col>
                  </v-row>

                  <v-alert v-if="totalTypesPercentage !== 100"
                    :type="totalTypesPercentage === 100 ? 'success' : 'warning'" density="compact" variant="tonal"
                    class="mt-4 rounded-xl">
                    إجمالي النسبة: {{ totalTypesPercentage }}% (يجب أن يعادل 100%)
                  </v-alert>
                </v-window-item>

                <!-- Summary Dashboard -->
                <v-window-item :value="4">
                  <v-row>
                    <!-- Types Breakdown -->
                    <v-col cols="12" md="6">
                      <div class="pa-5 rounded-2xl border-subtle">
                        <h4 class="text-subtitle-1 font-weight-bold mb-4 d-flex align-center gap-2">
                          <v-icon color="primary" size="20">mdi-shape</v-icon>
                          توزيع أنواع الأسئلة ورصيدها
                        </h4>
                        <div v-for="type in blueprint.types" :key="type.name"
                          class="d-flex align-center justify-space-between pa-3 rounded-lg mb-2 border-subtle">
                          <span class="font-weight-bold">{{ type.name }}</span>
                          <v-chip size="small" :color="type.color" variant="tonal" class="font-weight-bold">
                            {{ Math.round(exam.questionsCount * type.percentage / 100) }} سؤال ({{ type.percentage }}%)
                          </v-chip>
                        </div>
                      </div>
                    </v-col>

                    <!-- Difficulty Breakdown -->
                    <v-col cols="12" md="6">
                      <div class="pa-5 rounded-2xl border-subtle">
                        <div class="d-flex align-center justify-space-between mb-4">
                          <h4 class="text-subtitle-1 font-weight-bold mb-0 d-flex align-center gap-2">
                            <v-icon color="warning" size="20">mdi-speedometer</v-icon>
                            توزيع الصعوبة المعتمد
                          </h4>
                          <v-chip size="small" :color="modelsMode === 'advanced' ? 'warning' : 'primary'" variant="tonal" class="font-weight-bold">
                            {{ modelsMode === 'advanced' ? 'وضع متقدم' : 'وضع موحد' }}
                          </v-chip>
                        </div>
                        <template v-if="modelsMode === 'uniform'">
                          <div v-for="level in blueprint.difficulty" :key="level.name"
                            class="d-flex align-center justify-space-between pa-3 rounded-lg mb-2 border-subtle">
                            <span class="font-weight-bold">{{ level.name }}</span>
                            <v-chip size="small" :color="level.color" variant="tonal" class="font-weight-bold">
                              {{ Math.round(exam.questionsCount * level.percentage / 100) }} سؤال ({{ level.percentage }}%)
                            </v-chip>
                          </div>
                        </template>
                        <template v-else>
                          <div v-for="(group, gIdx) in modelGroups" :key="gIdx"
                            class="pa-3 rounded-xl mb-3 border-subtle">
                            <div class="d-flex align-center justify-space-between mb-2">
                              <span class="font-weight-bold">مجموعة {{ gIdx + 1 }} ({{ group.count }} نماذج)</span>
                              <v-chip size="x-small" :color="difficultyColor(group.difficulty_profile)" variant="tonal" class="font-weight-bold">
                                {{ difficultyLabel(group.difficulty_profile) }}
                              </v-chip>
                            </div>
                            <div class="d-flex gap-2 flex-wrap">
                              <v-chip size="x-small" color="success" variant="tonal">سهل {{ group.difficulty_distribution.easy }}%</v-chip>
                              <v-chip size="x-small" color="warning" variant="tonal">متوسط {{ group.difficulty_distribution.medium }}%</v-chip>
                              <v-chip size="x-small" color="error" variant="tonal">صعب {{ group.difficulty_distribution.hard }}%</v-chip>
                            </div>
                          </div>
                        </template>
                      </div>
                    </v-col>
                  </v-row>
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
              <div class="d-flex align-center gap-2">
                <custom-btn type="add" label="حفظ كقالب معتمد" icon="mdi-content-save" variant="tonal"
                  color="secondary" class="font-weight-bold" :click="openSaveTemplateDialog" />
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
                    <span v-if="exam.target_scope_level === 'all'">كافة المناطق</span>
                    <span v-else>{{ selectedTargetIds?.length || 0 }} <span class="text-caption font-weight-bold text-medium-emphasis">هدف</span></span>
                  </div>
                  <div class="d-flex align-center gap-1 mb-2">
                    <v-chip size="x-small" color="deep-purple" variant="tonal" class="font-weight-bold">
                      {{ scopeLevelOptions.find(o => o.value === exam.target_scope_level)?.label }}
                    </v-chip>
                  </div>
                  <span class="text-caption text-medium-emphasis d-block">تغطية النماذج حسب التوزيع</span>
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
                    <th v-if="exam.target_scope_level !== 'all'" class="font-weight-bold">المناطق المخصصة</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(group, gIdx) in modelGroups" :key="gIdx">
                    <td class="font-weight-bold">مجموعة {{ gIdx + 1 }}</td>
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
                    <td v-if="exam.target_scope_level !== 'all'" class="text-caption">
                      <span v-if="group.assigned_target_ids && group.assigned_target_ids.length > 0" class="font-weight-bold text-primary">
                        {{ getAssignedTargetNames(group.assigned_target_ids) }}
                      </span>
                      <span v-else class="text-medium-emphasis">غير مخصص (تسري على جميع المناطق المستهدفة)</span>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>

            <!-- Distribution Summary Mini-Widgets -->
            <v-row dense>
              <v-col cols="12" md="4">
                <div class="section-group-card pa-4 rounded-2xl h-100">
                  <h4 class="text-subtitle-2 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon size="18" color="primary">mdi-book-open-page-variant</v-icon>
                    توزيع الوحدات المعتمدة
                  </h4>
                  <div v-for="unit in blueprint.units.filter(u => u.percentage > 0)" :key="unit.id"
                    class="d-flex align-center justify-space-between py-1 border-b-subtle">
                    <span class="text-caption font-weight-bold text-truncate" style="max-width: 70%;">{{ unit.name }}</span>
                    <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">{{ unit.percentage }}%</v-chip>
                  </div>
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
                        <span>مجموعة {{ gIdx + 1 }} ({{ difficultyLabel(group.difficulty_profile) }})</span>
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
                  <div v-for="type in blueprint.types" :key="type.name"
                    class="d-flex align-center justify-space-between py-1 border-b-subtle">
                    <span class="text-caption font-weight-bold">{{ type.name }}</span>
                    <v-chip size="x-small" :color="type.color" variant="tonal" class="font-weight-bold">
                      {{ Math.round(exam.questionsCount * type.percentage / 100) }} ({{ type.percentage }}%)
                    </v-chip>
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

    <!-- Save Template Dialog -->
    <CustomDialog v-model="saveTemplateDialog" width="500" title="حفظ كقالب">
      <v-text-field v-model="templateName" label="اسم القالب" variant="outlined" density="compact" rounded="lg"
        prepend-inner-icon="mdi-file-document-edit" class="mb-4" />
      <v-textarea v-model="templateDescription" label="وصف القالب (اختياري)" variant="outlined" density="compact" rounded="lg"
        rows="2" prepend-inner-icon="mdi-text" />
      <template #actions>
        <custom-btn label="إلغاء" variant="text" class="font-weight-bold"
          :click="() => saveTemplateDialog = false" />
        <custom-btn type="add" label="حفظ القالب" color="primary" class="font-weight-bold"
          :click="saveAsTemplate" />
      </template>
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
const settingsMode = ref('new')
const scheduleMode = ref('manual')
const modelsMode = ref('uniform')
const bloomEnabled = ref(true)
const savedTemplates = ref([])
const selectedTemplate = ref(null)
const saveTemplateDialog = ref(false)
const templateName = ref('')
const templateDescription = ref('')

// Exam Settings
const exam = ref({
  title: '',
  institution_type: 'school',
  examScheduleId: null,
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
  target_scope_level: 'all',
  exclude_previously_used: false,
})

// Matrix Inner Tabs Items
const activeTab = ref(0)
const matrixTabItems = computed(() => [
  { label: 'توزيع الوحدات', icon: 'mdi-book-open-page-variant' },
  { label: modelsMode.value === 'advanced' ? 'مستويات الصعوبة (متقدم)' : 'مستويات الصعوبة', icon: 'mdi-speedometer' },
  { label: 'مستويات بلوم', icon: 'mdi-brain' },
  { label: 'أنواع الأسئلة', icon: 'mdi-shape' },
  { label: 'الملخص النهائي', icon: 'mdi-clipboard-check-outline' },
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
const setQuestionsCount = (num) => {
  exam.value.questionsCount = num
}
const setModelsCount = (num) => {
  exam.value.modelsCount = num
}
const setTargetScopeLevel = (lvl) => {
  exam.value.target_scope_level = lvl
  if (lvl === 'all') {
    selectedTargetIds.value = []
  }
}
const setSettingsMode = (mode) => {
  settingsMode.value = mode
}
const setScheduleMode = (mode) => {
  scheduleMode.value = mode
}
const setModelsMode = (mode) => {
  modelsMode.value = mode
}

// ⭐ Advanced Model Groups
const modelGroups = ref([
  { count: 2, difficulty_profile: 'hard', difficulty_distribution: { easy: 10, medium: 30, hard: 60 }, assigned_target_ids: [] },
  { count: 2, difficulty_profile: 'easy', difficulty_distribution: { easy: 60, medium: 30, hard: 10 }, assigned_target_ids: [] },
])

// ⭐ Geographic Targeting & Organizations (Loaded from branch hierarchy)
const selectedTargetIds = ref([])
const selectedGovernorateForFilter = ref(null)
const selectedDirectorateForFilter = ref(null)

const governoratesList = ref([])
const directoratesList = ref([])
const allSchoolsList = ref([])
const loadingGeographicOrgs = ref(false)

const loadGeographicOrgs = async () => {
  loadingGeographicOrgs.value = true
  try {
    const orgsRes = await api.get('common/branch/?page_size=500&limit=500')
    const allOrgs = orgsRes.data?.data || orgsRes.data?.results || orgsRes.data || []
    governoratesList.value = allOrgs.filter(o => o.company_level === 30)
    directoratesList.value = allOrgs.filter(o => o.company_level === 40)
    allSchoolsList.value = allOrgs.filter(o => o.company_level === 50)
  } catch (e) {
    console.error("Error loading geographic branches:", e)
  } finally {
    loadingGeographicOrgs.value = false
  }
}

// Available Directorates filtered by selected governorate if any
const availableDirectorates = computed(() => {
  if (!selectedGovernorateForFilter.value) {
    return directoratesList.value
  }
  const govId = selectedGovernorateForFilter.value
  return directoratesList.value.filter(d => {
    const parentId = typeof d.fk_parent_organization === 'object' && d.fk_parent_organization !== null
      ? d.fk_parent_organization.id
      : (d.fk_parent_organization || d.fk_parent_organization_id || d.parent || d.parent_id)
    const gId = typeof d.fk_governorate === 'object' && d.fk_governorate !== null
      ? d.fk_governorate.id
      : (d.fk_governorate || d.fk_governorate_id)
    return parentId === govId || gId === govId
  })
})

// Available Schools filtered by governorate or directorate
const availableSchools = computed(() => {
  let list = allSchoolsList.value
  if (selectedDirectorateForFilter.value) {
    const dirId = selectedDirectorateForFilter.value
    list = list.filter(s => {
      const parentId = typeof s.fk_parent_organization === 'object' && s.fk_parent_organization !== null
        ? s.fk_parent_organization.id
        : (s.fk_parent_organization || s.fk_parent_organization_id || s.parent || s.parent_id)
      const dId = typeof s.fk_directorate === 'object' && s.fk_directorate !== null
        ? s.fk_directorate.id
        : (s.fk_directorate || s.fk_directorate_id)
      return parentId === dirId || dId === dirId
    })
  } else if (selectedGovernorateForFilter.value) {
    const govId = selectedGovernorateForFilter.value
    list = list.filter(s => {
      const gId = typeof s.fk_governorate === 'object' && s.fk_governorate !== null
        ? s.fk_governorate.id
        : (s.fk_governorate || s.fk_governorate_id)
      return gId === govId
    })
  }
  return list
})

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
]

const difficultyItems = [
  { key: 'easy', label: 'سهل', color: 'success' },
  { key: 'medium', label: 'متوسط', color: 'warning' },
  { key: 'hard', label: 'صعب', color: 'error' },
]

const difficultyColor = (profile) => {
  const map = { easy: 'success', medium: 'warning', hard: 'error', mixed: 'info' }
  return map[profile] || 'info'
}

const difficultyLabel = (profile) => {
  const map = { easy: 'سهل', medium: 'متوسط', hard: 'صعب', mixed: 'مختلط' }
  return map[profile] || profile
}

const applyDifficultyPreset = (group) => {
  const presets = {
    easy: { easy: 60, medium: 30, hard: 10 },
    medium: { easy: 20, medium: 60, hard: 20 },
    hard: { easy: 10, medium: 30, hard: 60 },
    mixed: { easy: 30, medium: 40, hard: 30 },
  }
  group.difficulty_distribution = { ...presets[group.difficulty_profile] || presets.mixed }
}

const groupDiffTotal = (group) => {
  const d = group.difficulty_distribution
  return (d.easy || 0) + (d.medium || 0) + (d.hard || 0)
}

const addModelGroup = () => {
  modelGroups.value.push({
    count: 2,
    difficulty_profile: 'medium',
    difficulty_distribution: { easy: 20, medium: 60, hard: 20 },
    assigned_target_ids: []
  })
}

const removeModelGroup = (idx) => {
  modelGroups.value.splice(idx, 1)
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
    if (settingsMode.value === 'template') {
      return !!selectedTemplate.value
    }
    if (scheduleMode.value === 'schedule') {
      return !!exam.value.examScheduleId
    }
    return true
  }

  if (sectionId === 2) {
    if (settingsMode.value === 'template') {
      return !!selectedTemplate.value
    }
    if (scheduleMode.value === 'schedule') {
      return !!exam.value.examScheduleId
    }
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

  if (sectionId === 3) {
    const hasTitle = !!exam.value.title && String(exam.value.title).trim().length > 0
    const qCount = Number(exam.value.questionsCount)
    return hasTitle && !isNaN(qCount) && qCount >= 5 && qCount <= 100
  }

  if (sectionId === 4) {
    if (exam.value.target_scope_level === 'all') return true
    return Array.isArray(selectedTargetIds.value) && selectedTargetIds.value.length > 0
  }

  if (sectionId === 5) {
    if (modelsMode.value === 'uniform') {
      const mCount = Number(exam.value.modelsCount)
      return !isNaN(mCount) && mCount >= 1 && mCount <= 10
    }
    if (!modelGroups.value || modelGroups.value.length === 0) return false
    return modelGroups.value.every(g => {
      const cnt = Number(g.count)
      return !isNaN(cnt) && cnt >= 1 && cnt <= 10 && groupDiffTotal(g) === 100
    })
  }

  return true
}

const invalidSections = computed(() => {
  const list = []
  for (let s = 1; s <= 5; s++) {
    if (!isSectionValid(s)) {
      list.push(s)
    }
  }
  return list
})

const invalidSectionsCount = computed(() => invalidSections.value.length)

const step1NavItems = computed(() => {
  const isAcademicManual = settingsMode.value === 'new' && scheduleMode.value === 'manual'
  return [
    {
      id: 1,
      title: '1. نمط الإعداد والربط الهيكلي',
      desc: settingsMode.value === 'new' ? 'إعداد مخصص جديد' : 'قالب معتمد',
      icon: 'mdi-tune-variant',
      color: 'primary',
    },
    {
      id: 2,
      title: '2. النطاق والتصنيف الأكاديمي',
      desc: isAcademicManual 
        ? (exam.value.institution_type === 'school' ? 'تعليم عام ومدرسي' : exam.value.institution_type === 'university' ? 'تعليم جامعي' : 'تعليم مهني')
        : (scheduleMode.value === 'schedule' ? 'مستورد من جدول الاختبارات' : 'مستورد من قالب المواصفات'),
      icon: 'mdi-school-outline',
      color: 'secondary',
    },
    {
      id: 3,
      title: '3. تفاصيل وسعة ورقة الاختبار',
      desc: `${exam.value.questionsCount} سؤال`,
      icon: 'mdi-card-account-details-outline',
      color: 'info',
    },
    {
      id: 4,
      title: '4. النطاق الجغرافي للاختبار',
      desc: exam.value.target_scope_level === 'all' 
        ? 'كافة المناطق (شامل)' 
        : (selectedTargetIds.value?.length ? `${selectedTargetIds.value.length} جهة محددة` : 'تحديد مخصص'),
      icon: 'mdi-map-marker-radius',
      color: 'deep-purple',
    },
    {
      id: 5,
      title: '5. إعدادات النماذج التوليدية',
      desc: modelsMode.value === 'uniform' ? `${exam.value.modelsCount} نماذج موحدة` : `${totalModelsCount.value} نماذج متقدمة`,
      icon: 'mdi-file-multiple-outline',
      color: 'warning',
    }
  ]
})

const goToStep1Section = (sectionId) => {
  if (sectionId >= 1 && sectionId <= 5) {
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

const enrichedSchedules = computed(() => {
  return examSchedules.value.map(schedule => {
    const period = examPeriods.value.find(p => p.id === schedule.examPeriodId)
    const lsb = levelSubjectBranches.value.find(l => l.id === schedule.levelSubjectBranchId)
    const subject = lsb ? subjects.value.find(s => s.id === lsb.subjectId) : null
    const level = lsb ? levels.value.find(l => l.id === lsb.levelId) : null
    const branch = lsb ? branches.value.find(b => b.id === lsb.branchId) : null

    const periodName = period?.name || ''
    const subjectName = subject?.name || ''
    const levelName = level?.name || ''
    const branchName = branch?.name || ''

    return {
      ...schedule,
      periodName,
      subjectName,
      levelName,
      branchName,
      displayLabel: `${periodName} - ${subjectName} - ${levelName} (${branchName}) - ${schedule.date}`,
      subtitle: `التاريخ: ${schedule.date} | ${branchName}`,
      resolvedSubjectId: lsb?.subjectId,
      resolvedLevelId: lsb?.levelId,
      resolvedBranchId: lsb?.branchId,
      resolvedPeriodId: schedule.examPeriodId,
      resolvedYearId: period?.yearId || schedule.yearId || schedule.academic_year || schedule.year,
    }
  })
})

const selectedScheduleInfo = computed(() => {
  if (!exam.value.examScheduleId) return null
  return enrichedSchedules.value.find(s => s.id === exam.value.examScheduleId) || null
})

const onScheduleChange = (scheduleId) => {
  if (!scheduleId) {
    exam.value.subjectId = null
    exam.value.levelId = null
    exam.value.branchId = null
    exam.value.examPeriodId = null
    return
  }

  const schedule = enrichedSchedules.value.find(s => s.id === scheduleId)
  if (!schedule) return

  exam.value.subjectId = schedule.resolvedSubjectId
  exam.value.levelId = schedule.resolvedLevelId
  exam.value.branchId = schedule.resolvedBranchId
  exam.value.examPeriodId = schedule.resolvedPeriodId
  if (schedule.resolvedYearId) {
    exam.value.yearId = schedule.resolvedYearId
  } else if (!exam.value.yearId) {
    const currentYear = years.value.find(y => y.is_current || y.isCurrent)
    exam.value.yearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
  }

  if (!exam.value.title) {
    exam.value.title = `${schedule.subjectName} - ${schedule.periodName} - ${schedule.date}`
  }
}

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

  // Load saved templates
  try {
    savedTemplates.value = await examsService.getExamTemplates()
  } catch (e) {
    console.warn('Could not load templates:', e)
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
    { name: 'اختيار من متعدد (MCQ)', value: 'mcq', percentage: 60, color: 'primary' },
    { name: 'صح/خطأ (True/False)', value: 'tf', percentage: 40, color: 'success' },
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
  if (exam.value.institution_type === 'university' && exam.value.semesterSubjectId) {
    try {
      const res = await academicService.getUnits({ semester_subject_id: exam.value.semesterSubjectId })
      const uList = res.results || res || []
      if (uList.length > 0) {
        const perUnit = Math.floor(100 / uList.length)
        blueprint.value.units = uList.map((u, idx) => ({
          id: u.id,
          name: u.name_ar || u.name_en || u.name || `مفردة #${u.id}`,
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
      const params = { subject_id: exam.value.subjectId }
      if (exam.value.classTrackId) params.class_track_id = exam.value.classTrackId
      if (exam.value.levelId) params.level_id = exam.value.levelId
      if (exam.value.stageId) params.stage_id = exam.value.stageId
      const res = await academicService.getUnits(params)
      let dbUnits = res.results || res || []
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

        let activeUnits = dbUnits.filter(u => targetTerms.includes(u.term || 3))
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
            term: u.term || 3,
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
        term: u.term || 3,
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
})

const totalUnitsPercentage = computed(() =>
  blueprint.value.units.reduce((sum, u) => sum + u.percentage, 0)
)
const totalDifficultyPercentage = computed(() =>
  blueprint.value.difficulty.reduce((sum, d) => sum + d.percentage, 0)
)
const totalBloomPercentage = computed(() =>
  blueprint.value.bloom.reduce((sum, b) => sum + b.percentage, 0)
)
const totalTypesPercentage = computed(() =>
  blueprint.value.types.reduce((sum, t) => sum + t.percentage, 0)
)

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
// Template Management
// ═══════════════════════════════════════════════════════════
const applyTemplate = (template) => {
  if (!template || !template.config_json) return
  const config = template.config_json

  if (config.exam) {
    Object.keys(config.exam).forEach(key => {
      if (exam.value.hasOwnProperty(key)) {
        exam.value[key] = config.exam[key]
      }
    })
  }
  if (config.blueprint) {
    if (config.blueprint.difficulty) blueprint.value.difficulty = config.blueprint.difficulty
    if (config.blueprint.bloom) blueprint.value.bloom = config.blueprint.bloom
    if (config.blueprint.types) blueprint.value.types = config.blueprint.types
  }
  if (config.modelsMode) modelsMode.value = config.modelsMode
  if (config.modelGroups) modelGroups.value = config.modelGroups
  if (config.bloomEnabled !== undefined) bloomEnabled.value = config.bloomEnabled
}

const openSaveTemplateDialog = () => {
  templateName.value = exam.value.title ? `قالب - ${exam.value.title}` : 'قالب جديد'
  templateDescription.value = ''
  saveTemplateDialog.value = true
}

const saveAsTemplate = async () => {
  try {
    const config = {
      exam: { ...exam.value },
      blueprint: {
        difficulty: blueprint.value.difficulty,
        bloom: blueprint.value.bloom,
        types: blueprint.value.types,
      },
      modelsMode: modelsMode.value,
      modelGroups: modelsMode.value === 'advanced' ? modelGroups.value : [],
      bloomEnabled: bloomEnabled.value,
    }
    await examsService.saveExamTemplate({
      name: templateName.value,
      description: templateDescription.value,
      institution_type: exam.value.institution_type,
      config: config,
    })
    saveTemplateDialog.value = false
    savedTemplates.value = await examsService.getExamTemplates()
    if (proxy && proxy.$alert) {
      proxy.$alert("success", { message: "تم حفظ القالب بنجاح", title: "نجاح" })
    }
  } catch (e) {
    console.error("Error saving template:", e)
  }
}

const deleteTemplate = async (templateId) => {
  try {
    await examsService.deleteExamTemplate(templateId)
    savedTemplates.value = await examsService.getExamTemplates()
    selectedTemplate.value = null
  } catch (e) {
    console.error("Error deleting template:", e)
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

    step.value = 2
    return
  }

  if (step.value === 2) {
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

  // Build target scopes from selectedTargetIds
  const target_scopes = selectedTargetIds.value.map(id => {
    const scope = { scope_level: exam.value.target_scope_level }
    if (exam.value.target_scope_level === 'governorate') scope.governorate_id = id
    else if (exam.value.target_scope_level === 'directorate') scope.directorate_id = id
    else if (exam.value.target_scope_level === 'school') scope.organization_id = id
    return scope
  })

  // Build model-region assignments from model groups
  const model_region_assignments = []
  if (modelsMode.value === 'advanced' && exam.value.target_scope_level !== 'all') {
    modelGroups.value.forEach((group, gIdx) => {
      if (group.assigned_target_ids && group.assigned_target_ids.length > 0) {
        group.assigned_target_ids.forEach(targetId => {
          const assignment = {
            model_group_index: gIdx,
            difficulty_profile: group.difficulty_profile,
            scope_level: exam.value.target_scope_level,
          }
          if (exam.value.target_scope_level === 'governorate') assignment.governorate_id = targetId
          else if (exam.value.target_scope_level === 'directorate') assignment.directorate_id = targetId
          else if (exam.value.target_scope_level === 'school') assignment.organization_id = targetId
          model_region_assignments.push(assignment)
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
    examScheduleId: exam.value.examScheduleId || null,
    countryId: exam.value.countryId || null,
    governorateId: exam.value.governorateId || null,
    directorateId: exam.value.directorateId || null,
    regionId: exam.value.regionId || null,
    questionsCount: exam.value.questionsCount,
    modelsCount: modelsMode.value === 'uniform' ? exam.value.modelsCount : totalModelsCount.value,
    blueprint: blueprint.value,
    // Advanced Options
    bloom_enabled: bloomEnabled.value,
    models_mode: modelsMode.value,
    model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
    target_scope_level: exam.value.target_scope_level,
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
</style>
