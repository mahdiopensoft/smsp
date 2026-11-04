<template>
  <div class="qb-page-v4">




    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات التصفية المتقدمة" class="main-card border-0 pa-5 rounded-2xl mb-8">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / معاهد) -->
        <v-col cols="12" sm="6" :md="filterInstitutionType ? 3 : 4">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            label="نوع المؤسسة التعليمية"
            placeholder="اختر نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            clearable
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
            </template>
          </v-select>
        </v-col>

        <!-- الظهور مشروط باختيار نوع المؤسسة: مدارس أو جامعات أو معاهد -->
        <template v-if="filterInstitutionType">
          <!-- 🏫 School Filters (المرحلة، الصف والمسار، المادة، الوحدة) -->
          <template v-if="filterInstitutionType === 'school'">
            <auto-list v-model="filterStage" name="Stage"
              label="المرحلة الدراسية" cols="3" sm="6" md="3" :add="false" @update:model-value="onStageChange" />
            <auto-list v-model="filterClassTrack" name="ClassTrackByStage"
              :param="filterStage" label="الصف والمسار المدرسي" cols="3" sm="6" md="3" :add="false"
              :disabled="!filterStage" @update:model-value="onClassTrackChange" />
            <auto-list v-model="filterSubject" name="Subject" :param="subjectFilterParam" label="المادة الدراسية"
              cols="3" sm="6" md="3" :add="false" @update:model-value="onSubjectChange" />
            <auto-list v-model="filterUnit" name="UnitBySubject"
              :param="unitFilterParam" label="الوحدة الدراسية"
              cols="3" sm="6" md="3" :add="false"
              :disabled="!filterSubject" />
          </template>

          <!-- 🎓 University Filters (الكلية، القسم، التخصص، المقرر، مفردة المقرر) -->
          <template v-if="filterInstitutionType === 'university'">
            <auto-list v-model="filterCollege" name="College" label="الكلية الجامعية" cols="3" sm="6" md="3"
              :add="false" @update:model-value="onCollegeChange" />
            <auto-list v-model="filterDepartment" name="DepartmentByCollege" :param="filterCollege"
              label="القسم الأكاديمي" cols="3" sm="6" md="3" :add="false" :disabled="!filterCollege"
              @update:model-value="onDepartmentChange" />
            <auto-list v-model="filterSpecialization" name="Specialization" :param="filterDepartment"
              label="التخصص والبرنامج" cols="3" sm="6" md="3" :add="false" :disabled="!filterDepartment"
              @update:model-value="onSpecializationChange" />
            <auto-list v-model="filterSemesterSubject" name="SemesterSubject" :param="filterSpecialization"
              label="مقرر الفصل الجامعي" cols="3" sm="6" md="3" :add="false"
              @update:model-value="onSemesterSubjectChange" />
            <auto-list v-model="filterUnit" name="UnitBySubject"
              :param="unitFilterParam" label="مفردة / موضوع المقرر"
              cols="3" sm="6" md="3" :add="false"
              :disabled="!filterSemesterSubject" />
          </template>

          <!-- 🏢 Institute Filters (المجال المهني، نظام التعليم، التخصص، المادة، الوحدة) -->
          <template v-if="filterInstitutionType === 'institute'">
            <auto-list v-model="filterInstituteField" name="InstituteField" label="المجال المهني / التقني"
              cols="3" sm="6" md="3" :add="false" @update:model-value="onInstituteFieldChange" />
            <auto-list v-model="filterInstituteEducationSystem" name="InstituteEducationSystem"
              :param="filterInstituteField" label="نظام التعليم والتدريب" cols="3" sm="6" md="3" :add="false"
              :disabled="!filterInstituteField" @update:model-value="onInstituteEducationSystemChange" />
            <auto-list v-model="filterInstituteSpecialization" name="InstituteSpecialization"
              :param="instituteSpecParam"
              label="التخصص المهني" cols="3" sm="6" md="3" :add="false"
              :disabled="!filterInstituteEducationSystem" @update:model-value="onInstituteSpecializationChange" />
            <auto-list v-model="filterInstituteSubject" name="InstituteSubject"
              :param="instituteSubjectParam" label="المادة الدراسية للمعهد" cols="3" sm="6" md="3"
              :add="false" @update:model-value="onInstituteSubjectChange" />
            <auto-list v-model="filterUnit" name="UnitBySubject"
              :param="unitFilterParam" label="الوحدة / التدريب العملي"
              cols="3" sm="6" md="3" :add="false"
              :disabled="!filterInstituteSubject" />
          </template>

          <!-- Status -->
          <v-col cols="3" sm="6" md="3">
            <v-select v-model="filterStatus" :items="statusOptions" item-title="text" item-value="value" class="mb-6"
              placeholder="حالة السؤال" prepend-inner-icon="mdi-flag-outline" hide-details clearable density="compact"
              variant="outlined" />
          </v-col>

          <!-- Difficulty & Question Type -->
          <auto-list v-model="filterDifficulty" name="Difficulty" label="مستوى الصعوبة" cols="3" sm="6" md="3"
            :add="false" />
          <auto-list v-model="filterType" name="QuestionType" label="نوع السؤال" cols="3" sm="6" md="3"
            :add="false" />

          <!-- Bloom Level -->
          <v-col cols="3" sm="6" md="3">
            <v-select v-model="filterBloom" :items="bloomOptions" item-title="title" item-value="value" class="mb-6"
              placeholder="مستوى بلوم المعرفي" prepend-inner-icon="mdi-brain" hide-details clearable density="compact"
              variant="outlined" />
          </v-col>

          <!-- Filter Actions -->
          <v-col cols="3" sm="12" md="3" class="d-flex align-center gap-2">
            <custom-btn type="show" label="تصفية" color="primary" class="font-weight-bold flex-grow-1 mb-6"
              :click="applyFilters" />
            <custom-btn type="cancel_filter" :click="resetFilters" variant="tonal" color="error" label="تفريغ"
              class="font-weight-bold mb-6" />
          </v-col>
        </template>
      </v-row>
    </filter-fields>

    <!-- Table View -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table :headers="headers" :items="items" :getData="getData" :customLoading="loading"
        class="bg-transparent" :hasFilter="false" :log="false" :restore="false">
        <template v-slot:item-slot="{ item, key }">
          <!-- Content Snippet -->
          <template v-if="key === 'content'">
            <div class="d-flex align-center flex-wrap gap-2">
              <span class="text-truncate font-weight-medium d-inline-block" style="max-width: 360px">
                {{ stripHtml(item.content) }}
              </span>
              <v-chip
                v-if="item.is_imported || item.import_session"
                size="x-small"
                color="teal"
                variant="tonal"
                class="font-weight-bold px-1"
                style="height: 19px; font-size: 0.68rem !important;"
                title="تم استيراد هذا السؤال من ملف إكسل"
              >
                <v-icon start size="11">mdi-file-excel</v-icon>
                إكسل
              </v-chip>
            </div>
          </template>

          <template v-else-if="key === 'subject'">
            <div>
              <div class="text-body-2 font-weight-bold text-primary">{{ item.subject_name || getSubjectName(item) }}
              </div>
              <div class="text-caption text-medium-emphasis" v-if="item.lesson_name">{{ item.lesson_name }}</div>
            </div>
          </template>

          <template v-else-if="key === 'status'">
            <v-chip :color="getStatusColor(item.status)" variant="tonal" size="small"
              class="font-weight-bold text-white">
              <v-icon start size="14">{{ getStatusIcon(item.status) }}</v-icon>
              {{ item.status }}
            </v-chip>
          </template>

          <template v-else-if="key === 'difficulty'">
            <v-chip :color="getDifficultyColor(item.difficulty)" variant="tonal" size="small"
              class="font-weight-bold text-white">
              <v-icon start size="14">{{ getDifficultyIcon(item.difficulty) }}</v-icon>
              {{ getDifficultyText(item.difficulty) }}
            </v-chip>
          </template>

          <template v-else-if="key === 'questionType'">
            <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
              {{ getTypeText(item.questionType) }}
            </v-chip>
          </template>

          <template v-else-if="key === 'defaultMark'">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
              <v-icon start size="14">mdi-star</v-icon> {{ item.defaultMark || 1 }}
            </v-chip>
          </template>

          <template v-else-if="key === 'audit'">
            <div
              class="audit-table-cell d-flex align-center gap-2 py-1 px-2 rounded-lg cursor-pointer"
              @click="openAuditDialog(item)"
              title="انقر لعرض تفاصيل المنشئ وسجل التعديلات"
            >
              <v-avatar size="32" :color="(item.is_imported || item.import_session) ? 'teal' : 'primary'" variant="tonal" class="flex-shrink-0">
                <v-icon size="16" :color="(item.is_imported || item.import_session) ? 'teal-darken-1' : 'primary'">
                  {{ (item.is_imported || item.import_session) ? 'mdi-file-excel' : 'mdi-account-outline' }}
                </v-icon>
              </v-avatar>

              <div class="overflow-hidden flex-grow-1" style="min-width: 125px; max-width: 175px;">
                <div class="d-flex align-center gap-1">
                  <span class="font-weight-bold text-caption text-truncate" style="color: rgb(var(--v-theme-on-surface));">
                    {{ item.author_name || item.created_by_username || 'غير محدد' }}
                  </span>
                  <v-chip
                    v-if="item.is_imported || item.import_session"
                    size="x-small"
                    variant="flat"
                    color="teal"
                    class="px-1 font-weight-bold"
                    style="height: 16px; font-size: 0.6rem !important;"
                    title="مستورد من ملف إكسل"
                  >
                    إكسل
                  </v-chip>
                  <v-chip
                    v-if="item.edit_count > 0"
                    size="x-small"
                    variant="flat"
                    color="warning"
                    class="px-1 font-weight-bold"
                    style="height: 16px; font-size: 0.6rem !important;"
                    title="عدد مرات التعديل"
                  >
                    {{ item.edit_count }} تعديل
                  </v-chip>
                </div>

                <div class="text-caption text-disabled d-flex align-center gap-1 mt-0-5" style="font-size: 0.72rem !important;">
                  <v-icon size="11">mdi-clock-outline</v-icon>
                  <span>{{ formatAuditDate(item.last_modified_at || item.created_at) }}</span>
                  <span
                    v-if="item.last_modified_by && item.last_modified_by !== item.author_name"
                    class="text-warning-darken-1 text-truncate"
                    style="max-width: 75px;"
                    :title="'آخر من عدّل: ' + item.last_modified_by"
                  >
                    • {{ item.last_modified_by }}
                  </span>
                </div>
              </div>

              <v-icon size="16" color="primary" class="audit-hover-icon flex-shrink-0">mdi-open-in-new</v-icon>
            </div>
          </template>

          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center">
              <v-menu transition="slide-y-transition" location="bottom end" offset="8">
                <template v-slot:activator="{ props }">
                  <custom-btn v-bind="props" is-icon icon="dots-vertical" color="secondary" variant="text" />
                </template>

                <v-card elevation="24" rounded="lg" class="premium-menu-card border-thin overflow-hidden"
                  style="min-width: 220px">
                  <div class="pa-3 border-b d-flex align-center"
                    style="background-color: rgba(var(--v-theme-primary), 0.08)">
                    <v-icon color="primary" class="me-2" size="20">mdi-dots-horizontal-circle-outline</v-icon>
                    <div class="text-caption font-weight-bold" style="color: rgb(var(--v-theme-on-surface))">
                      إجراءات السجل
                    </div>
                  </div>

                  <v-card-text class="pa-2">
                    <v-list density="compact" class="bg-transparent pa-0">
                      <v-list-item @click="viewQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="primary" class="me-2">mdi-eye-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium"
                          style="color: rgba(var(--v-theme-on-surface), 0.7)">
                          معاينة التفاصيل
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item @click="openAuditDialog(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="indigo" class="me-2">mdi-history</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-indigo">
                          سجل التعديلات والتدقيق
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status !== 'معتمد'" @click="editQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="warning" class="me-2">mdi-pencil-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-warning">
                          تعديل السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item @click="duplicateQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="indigo" class="me-2">mdi-content-copy</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-indigo">
                          استنساخ السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status === 'معتمد'" @click="createQuestionVersion(item)"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="teal" class="me-2">mdi-source-branch</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-teal">
                          إنشاء إصدار جديد (v{{ (item.version_number || 1) + 1 }})
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status === 'مسودة'" @click="updateQuestionStatus(item, 'قيد المراجعة')"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="info" class="me-2">mdi-send-clock</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-info">
                          تقديم للمراجعة
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status !== 'مؤرشف'" @click="archiveQuestion(item)"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="purple" class="me-2">mdi-archive-arrow-down-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-purple">
                          أرشفة السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-else @click="restoreQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="success" class="me-2">mdi-archive-arrow-up-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-success">
                          استعادة من الأرشيف
                        </v-list-item-title>
                      </v-list-item>

                      <v-divider class="my-1 opacity-20"></v-divider>

                      <v-list-item @click="openDeleteDialog(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="error" class="me-2">mdi-trash-can-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-error">
                          نقل للمهملات
                        </v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-menu>
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- View Question Dialog (Official Exam-Grade Preview) -->
    <CustomDialog v-model="viewDialog" width="920" :showClose="true">
      <template #title>
        <div class="d-flex align-center justify-space-between w-100 flex-wrap gap-2 pe-2">
          <div class="d-flex align-center gap-3">
            <v-avatar size="44" rounded="lg" color="primary" variant="tonal" class="border">
              <v-icon size="24" color="primary">mdi-file-document-check-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2">
                <span class="text-h6 font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">معاينة بطاقة السؤال</span>
                <v-chip size="small" variant="tonal" color="primary" class="font-weight-black px-2">
                  #{{ selectedQuestion ? selectedQuestion.id : '' }}
                </v-chip>
                <v-chip v-if="selectedQuestion?.version_number" size="x-small" variant="tonal" color="secondary" class="font-weight-bold">
                  v{{ selectedQuestion.version_number }}.0
                </v-chip>
                <v-chip v-if="selectedQuestion?.is_imported || selectedQuestion?.import_session" size="x-small" variant="tonal" color="teal" class="font-weight-bold">
                  <v-icon start size="12">mdi-file-excel</v-icon>
                  مستورد من إكسل
                </v-chip>
              </div>
              <div class="text-caption text-medium-emphasis">
                {{ selectedQuestion ? getTypeText(selectedQuestion.questionType) : '' }}
                <span v-if="selectedQuestion?.institution_type" class="ms-1">
                  • {{ getInstitutionLabel(selectedQuestion.institution_type) }}
                </span>
              </div>
            </div>
          </div>

          <div class="d-flex align-center gap-2">
            <custom-btn
              text="سجل التعديلات والتدقيق"
              icon="history"
              size="small"
              variant="tonal"
              color="indigo"
              class="font-weight-bold"
              @click="openAuditDialog(selectedQuestion)"
            />
          </div>
        </div>
      </template>

      <template v-if="selectedQuestion">
        <div class="qb-preview-dialog-canvas pa-2">
          <!-- Loading indicator while full details are loaded on demand -->
          <v-progress-linear v-if="selectedQuestion._loading" indeterminate color="primary" class="mb-4 rounded" />

          <!-- Specifications Badges Ribbon -->
          <div class="d-flex flex-wrap align-center gap-2 mb-4">
            <!-- Status Badge -->
            <v-chip :color="getStatusColor(selectedQuestion.status)" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">{{ getStatusIcon(selectedQuestion.status) }}</v-icon>
              {{ selectedQuestion.status }}
            </v-chip>

            <!-- Question Type -->
            <v-chip color="primary" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-shape-outline</v-icon>
              {{ getTypeText(selectedQuestion.questionType) }}
            </v-chip>

            <!-- Difficulty -->
            <v-chip :color="getDifficultyColor(selectedQuestion.difficulty)" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">{{ getDifficultyIcon(selectedQuestion.difficulty) }}</v-icon>
              الصعوبة: {{ getDifficultyText(selectedQuestion.difficulty) }}
            </v-chip>

            <!-- Bloom Level -->
            <v-chip v-if="selectedQuestion.bloomLevel" variant="tonal" class="font-weight-bold px-3 py-1"
              :style="`color: ${getBloomColor(selectedQuestion.bloomLevel)}; background-color: ${getBloomColor(selectedQuestion.bloomLevel)}18; border: 1px solid ${getBloomColor(selectedQuestion.bloomLevel)}40;`">
              <v-icon start size="16">mdi-brain</v-icon>
              بلوم: {{ selectedQuestion.bloomLevel }}
            </v-chip>

            <!-- Mark / Score -->
            <v-chip color="amber-darken-3" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-star-circle-outline</v-icon>
              {{ selectedQuestion.defaultMark || 1 }} درجة
            </v-chip>

            <!-- Expected Time -->
            <v-chip v-if="selectedQuestion.expected_time_minutes" color="teal" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-clock-outline</v-icon>
              {{ selectedQuestion.expected_time_minutes }} دقيقة
            </v-chip>

            <!-- Source: Excel Import -->
            <v-chip v-if="selectedQuestion.is_imported || selectedQuestion.import_session" color="teal-darken-1" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-file-excel</v-icon>
              المصدر: استيراد من ملف إكسل
            </v-chip>
          </div>

          <!-- Rejection Reason Alert if rejected -->
          <v-alert
            v-if="selectedQuestion.status === 'مرفوض' && selectedQuestion.rejectionReason"
            type="error"
            variant="tonal"
            density="comfortable"
            class="rounded-xl mb-4 border-error border"
            icon="mdi-alert-octagon-outline"
          >
            <div class="font-weight-bold text-subtitle-2 mb-1">تم رفض السؤال من قِبل المراجع</div>
            <div class="text-body-2">{{ selectedQuestion.rejectionReason }}</div>
          </v-alert>

          <!-- Academic Hierarchy Breadcrumb Ribbon -->
          <div class="academic-hierarchy-card pa-3 px-4 rounded-xl mb-4 border d-flex align-center flex-wrap gap-2">
            <div class="d-flex align-center gap-1 text-caption font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">
              <v-icon size="16" color="primary">mdi-sitemap</v-icon>
              <span>المسار التعليمي:</span>
            </div>
            <template v-for="(item, idx) in getAcademicHierarchy(selectedQuestion)" :key="idx">
              <div class="d-flex align-center gap-1 text-body-2">
                <span class="text-caption text-disabled" v-if="idx > 0">
                  <v-icon size="14">mdi-chevron-left</v-icon>
                </span>
                <div class="hierarchy-pill d-flex align-center gap-1 px-3 py-1 rounded-lg border text-caption">
                  <v-icon size="13" color="primary">{{ item.icon }}</v-icon>
                  <span class="text-medium-emphasis">{{ item.label }}:</span>
                  <span class="font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">{{ item.value }}</span>
                </div>
              </div>
            </template>

            <!-- Learning Outcome if present -->
            <div v-if="selectedQuestion.learningOutcome" class="ms-auto d-flex align-center gap-1">
              <v-chip size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
                <v-icon start size="12">mdi-target</v-icon>
                مخرج التعلم: {{ selectedQuestion.learningOutcome.name_ar || selectedQuestion.learningOutcome }}
              </v-chip>
            </div>
          </div>

          <!-- Official Question Paper Canvas -->
          <div class="question-paper-card rounded-2xl mb-4 border overflow-hidden">
            <!-- Header bar of the question card -->
            <div class="question-paper-header px-5 py-3 d-flex align-center justify-space-between border-b">
              <div class="d-flex align-center gap-2">
                <v-icon size="18" color="primary">mdi-format-quote-open</v-icon>
                <span class="text-subtitle-2 font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">نص السؤال المطلوب من الطالب</span>
              </div>
              <div class="d-flex align-center gap-2">
                <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                  السؤال الأساسي
                </v-chip>
              </div>
            </div>

            <div class="pa-5">
              <!-- Idea / Description Callout -->
              <div v-if="selectedQuestion.description"
                class="question-idea-box pa-3 px-4 rounded-xl mb-4 border d-flex align-center gap-3">
                <v-avatar size="32" color="amber-lighten-4" class="flex-shrink-0">
                  <v-icon size="18" color="amber-darken-3">mdi-lightbulb-on</v-icon>
                </v-avatar>
                <div class="text-body-2">
                  <span class="font-weight-bold text-amber-darken-4">فكرة السؤال / المفهوم العلمي: </span>
                  <span>{{ selectedQuestion.description }}</span>
                </div>
              </div>

              <!-- Question Image -->
              <div v-if="selectedQuestion.image" class="question-image-frame mb-4 pa-3 rounded-xl text-center border">
                <v-img :src="selectedQuestion.image" max-height="300" class="rounded-lg mx-auto" contain />
                <div class="text-caption text-medium-emphasis mt-2">
                  <v-icon size="14">mdi-image-outline</v-icon> شكل / رسم توضيحي مرفق بالسؤال
                </div>
              </div>

              <!-- Question Text -->
              <div class="question-body-rendered text-body-1 font-weight-bold" style="line-height: 2.1; font-size: 1.15rem !important;"
                v-html="selectedQuestion.content" />
            </div>
          </div>

          <!-- Answers / Options Section -->
          <div class="answers-section mb-4">
            <div class="d-flex align-center justify-space-between mb-3 px-1">
              <div class="d-flex align-center gap-2">
                <v-icon size="20" color="success">mdi-format-list-checks</v-icon>
                <h4 class="text-subtitle-1 font-weight-black">
                  {{ (selectedQuestion.options && selectedQuestion.options.length) ? 'الخيارات وبدائل الإجابة' : 'نموذج الإجابة الصحيحة' }}
                </h4>
              </div>
              <span class="text-caption text-medium-emphasis" v-if="selectedQuestion.options && selectedQuestion.options.length">
                {{ selectedQuestion.options.length }} خيارات معتمدة
              </span>
            </div>

            <!-- Single Choice / Multiple Choice Options -->
            <div v-if="selectedQuestion.options && selectedQuestion.options.length" class="d-flex flex-column gap-2">
              <div
                v-for="(answer, i) in selectedQuestion.options"
                :key="answer.id || i"
                class="option-row-card pa-4 rounded-xl d-flex align-center justify-space-between gap-3 border"
                :class="{ 'option-row-correct': answer.isTrue, 'option-row-neutral': !answer.isTrue }"
              >
                <div class="d-flex align-center gap-3 overflow-hidden flex-grow-1">
                  <!-- Letter Badge (أ ، ب ، ج ، د) -->
                  <v-avatar
                    size="36"
                    :color="answer.isTrue ? 'success' : 'primary'"
                    :variant="answer.isTrue ? 'flat' : 'tonal'"
                    class="font-weight-bold flex-shrink-0"
                  >
                    {{ getOptionLetter(i) }}
                  </v-avatar>

                  <div class="d-flex flex-column flex-grow-1 overflow-hidden">
                    <div class="text-body-1 font-weight-medium" v-html="answer.text" />
                    <v-img v-if="answer.image" :src="answer.image" max-height="120" contain class="mt-2 rounded-lg border" />
                    <div v-if="answer.latex" class="text-caption font-weight-medium mt-1 dir-ltr text-left">
                      <code>{{ answer.latex }}</code>
                    </div>
                  </div>
                </div>

                <!-- Right Indicator Badge -->
                <div class="flex-shrink-0">
                  <v-chip
                    v-if="answer.isTrue"
                    color="success"
                    variant="flat"
                    size="small"
                    class="font-weight-bold px-3"
                  >
                    <v-icon start size="14">mdi-check-circle</v-icon>
                    الإجابة الصحيحة
                  </v-chip>
                  <v-chip v-else size="x-small" variant="tonal" color="blue-grey" class="text-caption px-2">
                    بديل غير صحيح
                  </v-chip>
                </div>
              </div>
            </div>

            <!-- True / False Dual Card Showcase -->
            <div v-else-if="selectedQuestion.isTrue !== null && selectedQuestion.isTrue !== undefined" class="d-flex gap-4">
              <!-- True Card -->
              <div
                class="pa-4 rounded-xl flex-grow-1 border d-flex align-center justify-space-between transition-all"
                :class="selectedQuestion.isTrue ? 'tf-card-active' : 'tf-card-inactive'"
              >
                <div class="d-flex align-center gap-3">
                  <v-avatar size="36" :color="selectedQuestion.isTrue ? 'success' : 'grey-lighten-2'" :variant="selectedQuestion.isTrue ? 'flat' : 'tonal'">
                    <v-icon size="20" :color="selectedQuestion.isTrue ? 'white' : 'grey'">mdi-check</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-1 font-weight-bold" :class="selectedQuestion.isTrue ? 'text-success' : 'text-medium-emphasis'">
                      صواب (True)
                    </div>
                    <div class="text-caption text-medium-emphasis">العبارة صحيحة علمياً</div>
                  </div>
                </div>
                <v-chip v-if="selectedQuestion.isTrue" color="success" size="small" variant="flat" class="font-weight-bold">
                  الإجابة الصحيحة
                </v-chip>
              </div>

              <!-- False Card -->
              <div
                class="pa-4 rounded-xl flex-grow-1 border d-flex align-center justify-space-between transition-all"
                :class="!selectedQuestion.isTrue ? 'tf-card-active' : 'tf-card-inactive'"
              >
                <div class="d-flex align-center gap-3">
                  <v-avatar size="36" :color="!selectedQuestion.isTrue ? 'success' : 'grey-lighten-2'" :variant="!selectedQuestion.isTrue ? 'flat' : 'tonal'">
                    <v-icon size="20" :color="!selectedQuestion.isTrue ? 'white' : 'grey'">mdi-close</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-1 font-weight-bold" :class="!selectedQuestion.isTrue ? 'text-success' : 'text-medium-emphasis'">
                      خطأ (False)
                    </div>
                    <div class="text-caption text-medium-emphasis">العبارة خاطئة علمياً</div>
                  </div>
                </div>
                <v-chip v-if="!selectedQuestion.isTrue" color="success" size="small" variant="flat" class="font-weight-bold">
                  الإجابة الصحيحة
                </v-chip>
              </div>
            </div>

            <!-- Essay / Fill in the blank Model Answer -->
            <div v-else-if="selectedQuestion.answerText" class="model-answer-box pa-5 rounded-2xl border">
              <div class="d-flex align-center gap-2 mb-3">
                <v-icon size="20" color="success">mdi-text-box-check-outline</v-icon>
                <span class="text-subtitle-2 font-weight-bold text-success-darken-1">معايير الإجابة النموذجية وسلّم التقدير</span>
              </div>
              <div class="text-body-1 font-weight-medium" style="line-height: 1.9;" v-html="selectedQuestion.answerText" />
            </div>
          </div>

          <!-- Psychometrics & Cumulative Analytics -->
          <div v-if="selectedQuestion.metrics" class="psychometrics-box pa-4 rounded-2xl border mb-4">
            <div class="d-flex align-center justify-space-between mb-3 border-b pb-2">
              <div class="d-flex align-center gap-2">
                <v-avatar size="28" color="indigo-lighten-5">
                  <v-icon size="16" color="indigo">mdi-chart-bell-curve-cumulative</v-icon>
                </v-avatar>
                <span class="text-subtitle-2 font-weight-bold text-indigo-darken-2">مؤشرات التحليل السيكومتري للمفردة (Item Analysis)</span>
              </div>
              <v-chip size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
                تحليل تراكمي
              </v-chip>
            </div>

            <v-row dense>
              <!-- 1. Usage Count -->
              <v-col cols="6" sm="3">
                <div class="metric-tile pa-3 rounded-xl border text-center">
                  <div class="text-caption text-medium-emphasis mb-1">مرات الاستخدام</div>
                  <div class="text-h6 font-weight-black">{{ selectedQuestion.metrics.usage_count || 0 }}</div>
                  <div class="text-caption text-disabled mt-1">امتحانات رسمية</div>
                </div>
              </v-col>

              <!-- 2. Facility Value (P-Value) -->
              <v-col cols="6" sm="3">
                <div class="metric-tile pa-3 rounded-xl border text-center">
                  <div class="text-caption text-medium-emphasis mb-1">معامل السهولة (p-value)</div>
                  <div class="text-h6 font-weight-black text-primary">
                    {{ selectedQuestion.metrics.actual_difficulty != null ? selectedQuestion.metrics.actual_difficulty : '—' }}
                  </div>
                  <v-chip size="x-small" :color="getDifficultyAnalysis(selectedQuestion.metrics.actual_difficulty).color" variant="tonal" class="mt-1 font-weight-bold">
                    {{ getDifficultyAnalysis(selectedQuestion.metrics.actual_difficulty).text }}
                  </v-chip>
                </div>
              </v-col>

              <!-- 3. Discrimination Index D -->
              <v-col cols="6" sm="3">
                <div class="metric-tile pa-3 rounded-xl border text-center">
                  <div class="text-caption text-medium-emphasis mb-1">معامل التمييز (D)</div>
                  <div class="text-h6 font-weight-black text-teal">
                    {{ selectedQuestion.metrics.discrimination_index != null ? selectedQuestion.metrics.discrimination_index : '—' }}
                  </div>
                  <v-chip size="x-small" :color="getDiscriminationAnalysis(selectedQuestion.metrics.discrimination_index).color" variant="tonal" class="mt-1 font-weight-bold">
                    {{ getDiscriminationAnalysis(selectedQuestion.metrics.discrimination_index).text }}
                  </v-chip>
                </div>
              </v-col>

              <!-- 4. Point-Biserial rpb -->
              <v-col cols="6" sm="3">
                <div class="metric-tile pa-3 rounded-xl border text-center">
                  <div class="text-caption text-medium-emphasis mb-1">الارتباط النقطي (rpb)</div>
                  <div class="text-h6 font-weight-black text-purple">
                    {{ selectedQuestion.metrics.point_biserial != null ? selectedQuestion.metrics.point_biserial : '—' }}
                  </div>
                  <div class="text-caption text-disabled mt-1">اتساق داخلي</div>
                </div>
              </v-col>
            </v-row>
          </div>
        </div>
      </template>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => viewDialog = false"
          variant="text"
          label="إغلاق"
          class="font-weight-bold"
        />

        <div class="d-flex align-center gap-2 ms-auto">
          <custom-btn
            v-if="selectedQuestion && selectedQuestion.status !== 'معتمد'"
            type="update"
            :click="() => { editQuestion(selectedQuestion); viewDialog = false; }"
            variant="tonal"
            color="warning"
            label="تعديل السؤال"
            class="font-weight-bold"
          />
          <custom-btn
            v-if="selectedQuestion && selectedQuestion.status === 'مسودة'"
            type="add"
            :click="() => { updateQuestionStatus(selectedQuestion, 'قيد المراجعة'); viewDialog = false; }"
            color="info"
            label="تقديم للمراجعة"
            class="font-weight-bold"
          />
          <custom-btn
            v-if="selectedQuestion && selectedQuestion.status === 'قيد المراجعة'"
            type="confirm"
            :click="() => { updateQuestionStatus(selectedQuestion, 'معتمد'); viewDialog = false; }"
            color="success"
            label="اعتماد السؤال"
            class="font-weight-bold"
          />
        </div>
      </template>
    </CustomDialog>

    <!-- Delete Confirmation Modal -->
    <DeleteDialog v-model="deleteDialog" title="تأكيد الحذف"
      message="هل أنت متأكد من حذف هذا السؤال؟ سيتم نقله إلى سلة المحذوفات." @confirm-delete="executeDelete" />

    <!-- Dedicated Audit & History Dialog (سجل التدقيق والتعديلات المستقل) -->
    <CustomDialog v-model="auditDialog" width="800" :showClose="true">
      <template #title>
        <div class="d-flex align-center justify-space-between w-100 flex-wrap gap-2 pe-2">
          <div class="d-flex align-center gap-3">
            <v-avatar size="44" rounded="lg" color="indigo" variant="tonal" class="border">
              <v-icon size="24" color="indigo">mdi-shield-account-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2">
                <span class="text-h6 font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">
                  سجل تدقيق وتعديلات السؤال
                </span>
                <v-chip size="small" variant="tonal" color="primary" class="font-weight-black px-2">
                  #{{ auditQuestion ? auditQuestion.id : '' }}
                </v-chip>
                <v-chip v-if="auditQuestion?.version_number" size="x-small" variant="tonal" color="secondary" class="font-weight-bold">
                  v{{ auditQuestion.version_number }}.0
                </v-chip>
                <v-chip v-if="auditQuestion?.is_imported || auditQuestion?.import_session" size="x-small" variant="tonal" color="teal" class="font-weight-bold">
                  <v-icon start size="12">mdi-file-excel</v-icon>
                  مستورد من إكسل
                </v-chip>
              </div>
              <div class="text-caption text-medium-emphasis">
                تتبع تفصيلي لمنشئ السؤال وآخر من قام بالتعديل والمراجعة والاعتماد
              </div>
            </div>
          </div>
        </div>
      </template>

      <template v-if="auditQuestion">
        <div class="pa-2">
          <!-- Loading indicator -->
          <v-progress-linear v-if="auditLoading" indeterminate color="indigo" class="mb-4 rounded" />

          <!-- Summary 3-Column Grid -->
          <v-row dense class="mb-4">
            <!-- 1. Creator / Author -->
            <v-col cols="12" sm="4">
              <div class="audit-summary-tile pa-3 rounded-xl border d-flex align-center gap-3 h-100">
                <v-avatar size="42" :color="(auditQuestion.is_imported || auditQuestion.import_session) ? 'teal' : 'primary'" variant="tonal" class="flex-shrink-0">
                  <v-icon size="22" :color="(auditQuestion.is_imported || auditQuestion.import_session) ? 'teal' : 'primary'">
                    {{ (auditQuestion.is_imported || auditQuestion.import_session) ? 'mdi-file-excel' : 'mdi-account-plus-outline' }}
                  </v-icon>
                </v-avatar>
                <div class="overflow-hidden flex-grow-1">
                  <div class="text-caption text-medium-emphasis">منشئ السؤال (المؤلف):</div>
                  <div class="text-body-2 font-weight-bold text-truncate" style="color: rgb(var(--v-theme-on-surface));">
                    {{ auditQuestion.author_name || auditQuestion.created_by_username || 'مستخدم النظام' }}
                  </div>
                  <div class="d-flex align-center gap-1 flex-wrap mt-1">
                    <v-chip v-if="auditQuestion.is_imported || auditQuestion.import_session" size="x-small" color="teal" variant="flat" class="font-weight-bold px-1" style="height: 18px; font-size: 0.65rem !important;">
                      <v-icon start size="10">mdi-file-excel</v-icon>
                      مستورد من إكسل
                    </v-chip>
                    <div class="text-caption text-disabled d-flex align-center gap-1">
                      <v-icon size="12">mdi-clock-outline</v-icon>
                      <span>{{ formatAuditDate(auditQuestion.created_at || auditQuestion.createdAt) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </v-col>

            <!-- 2. Last Modifier -->
            <v-col cols="12" sm="4">
              <div class="audit-summary-tile pa-3 rounded-xl border d-flex align-center gap-3 h-100">
                <v-avatar size="42" :color="auditQuestion.last_modified_by ? 'warning' : 'grey'" variant="tonal" class="flex-shrink-0">
                  <v-icon size="22" :color="auditQuestion.last_modified_by ? 'warning' : 'grey'">mdi-pencil-clock-outline</v-icon>
                </v-avatar>
                <div class="overflow-hidden flex-grow-1">
                  <div class="text-caption text-medium-emphasis">آخر من قام بالتعديل:</div>
                  <div class="text-body-2 font-weight-bold text-truncate" :class="auditQuestion.last_modified_by ? 'text-warning-darken-1' : 'text-medium-emphasis'">
                    {{ auditQuestion.last_modified_by || 'لا توجد تعديلات سابقة' }}
                  </div>
                  <div class="text-caption text-disabled d-flex align-center gap-1 mt-1">
                    <v-icon size="12">mdi-clock-outline</v-icon>
                    <span>{{ auditQuestion.last_modified_at ? formatAuditDate(auditQuestion.last_modified_at) : 'الإصدار الأصلي' }}</span>
                    <v-chip v-if="auditQuestion.edit_count > 0" size="x-small" variant="tonal" color="warning" class="px-1 ms-1 font-weight-bold">
                      {{ auditQuestion.edit_count }} تعديل
                    </v-chip>
                  </div>
                </div>
              </div>
            </v-col>

            <!-- 3. Reviewer / Approver -->
            <v-col cols="12" sm="4">
              <div class="audit-summary-tile pa-3 rounded-xl border d-flex align-center gap-3 h-100">
                <v-avatar size="42" :color="auditQuestion.reviewer_name ? 'success' : 'grey'" variant="tonal" class="flex-shrink-0">
                  <v-icon size="22" :color="auditQuestion.reviewer_name ? 'success' : 'grey'">mdi-account-check-outline</v-icon>
                </v-avatar>
                <div class="overflow-hidden flex-grow-1">
                  <div class="text-caption text-medium-emphasis">المراجع المعتمد:</div>
                  <div class="text-body-2 font-weight-bold text-truncate" :class="auditQuestion.reviewer_name ? 'text-success' : 'text-medium-emphasis'">
                    {{ auditQuestion.reviewer_name || (auditQuestion.status === 'معتمد' ? 'اللجنة العلمية' : 'بانتظار المراجعة') }}
                  </div>
                  <div class="text-caption text-disabled d-flex align-center gap-1 mt-1">
                    <v-icon size="12">mdi-calendar-check-outline</v-icon>
                    <span>{{ auditQuestion.approved_at ? formatAuditDate(auditQuestion.approved_at) : 'لم يتم الاعتماد بعد' }}</span>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>

          <!-- Detailed Audit Timeline Section -->
          <div class="pa-4 rounded-2xl border" style="background: rgba(var(--v-theme-surface), 0.7);">
            <div class="d-flex align-center justify-space-between mb-3 border-b pb-2 flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <v-icon size="18" color="indigo">mdi-timeline-clock-outline</v-icon>
                <span class="text-subtitle-2 font-weight-bold">السجل الزمني لكافة العمليات على هذا السؤال</span>
              </div>
              <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold">
                {{ (auditQuestion.audit_trail && auditQuestion.audit_trail.length) || 1 }} عمليات مسجلة
              </v-chip>
            </div>

            <div v-if="auditQuestion.audit_trail && auditQuestion.audit_trail.length" class="audit-timeline-container d-flex flex-column gap-2">
              <div
                v-for="(log, idx) in auditQuestion.audit_trail"
                :key="log.id || idx"
                class="audit-timeline-row pa-3 rounded-xl border d-flex align-center justify-space-between gap-3 text-caption"
              >
                <div class="d-flex align-center gap-3 overflow-hidden">
                  <v-avatar size="34" :color="getActionBadgeColor(log.action)" variant="tonal" class="flex-shrink-0">
                    <v-icon size="18" :color="getActionBadgeColor(log.action)">{{ getActionIcon(log.action) }}</v-icon>
                  </v-avatar>
                  <div class="overflow-hidden">
                    <div class="d-flex align-center gap-2 flex-wrap">
                      <span class="font-weight-bold text-body-2" style="color: rgb(var(--v-theme-on-surface));">
                        {{ log.user_name || log.username || 'مستخدم النظام' }}
                      </span>
                      <v-chip size="x-small" :color="getActionBadgeColor(log.action)" variant="flat" class="font-weight-bold px-2">
                        {{ log.action }}
                      </v-chip>
                    </div>
                    <div class="text-caption text-medium-emphasis text-truncate mt-1">
                      {{ log.description || 'إجراء على السؤال' }}
                    </div>
                  </div>
                </div>

                <div class="text-caption text-disabled d-flex align-center gap-1 flex-shrink-0 dir-ltr">
                  <v-icon size="13">mdi-clock-time-four-outline</v-icon>
                  <span class="font-weight-medium">{{ formatAuditDate(log.created_at) }}</span>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-6 text-medium-emphasis">
              <v-icon size="36" color="disabled" class="mb-2">mdi-history</v-icon>
              <div class="text-caption font-weight-medium">تم إنشاء السؤال في {{ formatAuditDate(auditQuestion.created_at) }} ولا توجد أي تعديلات أو إجراءات إضافية مسجلة حتى الآن.</div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="d-flex align-center justify-end w-100 gap-2 pa-2">
          <custom-btn label="إغلاق" color="primary" variant="outlined" class="font-weight-bold px-5" :click="() => auditDialog = false" />
        </div>
      </template>
    </CustomDialog>


  </div>
</template>

<script>

import { bankService } from "@/services/bankService";
import { academicService } from "@/services/academicService";

export default {
  name: "QuestionBankView",
  components: {
  },

  data() {
    return {
      // State
      loading: false,
      items: { results: [], pagination: {} },
      subjects: [],

      // Filters
      search: "",
      filterInstitutionType: null,
      institutionTypeOptions: [
        { text: "تعليم مدرسي", value: "school", icon: "mdi-school" },
        { text: "تعليم جامعي", value: "university", icon: "mdi-domain" },
        { text: "معاهد وتدريب مهني", value: "institute", icon: "mdi-tools" },
      ],
      // Institute Filters
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteSubject: null,
      // University Filters
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      // School Filters
      filterStage: null,
      filterClassTrack: null,
      // General Filters
      filterSubject: null,
      filterUnit: null,
      filterDifficulty: null,
      filterStatus: null,
      filterType: null,
      filterBloom: null,

      statusOptions: [
        { text: "الكل", value: null },
        { text: "معتمد", value: "معتمد" },
        { text: "مسودة", value: "مسودة" },
        { text: "قيد المراجعة", value: "قيد المراجعة" },
        { text: "مستورد", value: "مستورد" },
        { text: "مرفوض", value: "مرفوض" },
      ],
      bloomOptions: [
        { title: "تذكر", value: "تذكر" },
        { title: "فهم", value: "فهم" },
        { title: "تطبيق", value: "تطبيق" },
        { title: "تحليل", value: "تحليل" },
        { title: "تقييم", value: "تقييم" },
        { title: "ابتكار", value: "ابتكار" },
      ],

      // Pagination
      currentPage: 1,
      itemsPerPage: 12,

      // Dialogs
      viewDialog: false,
      deleteDialog: false,
      selectedQuestion: null,
      questionToDelete: null,
      deleteLoading: false,
      auditDialog: false,
      auditQuestion: null,
      auditLoading: false,

      // Options
      difficulties: [
        { name: "سهل", id: 1 },
        { name: "متوسط", id: 2 },
        { name: "صعب", id: 3 },
      ],
      questionTypes: [
        { name: "اختيار واحد", id: "single_choice" },
        { name: "اختيارات متعددة", id: "multiple_choice" },
        { name: "صواب/خطأ", id: "true_false" },
      ],

      // Table Headers
      headers: [
        { title: "السؤال", key: "content", sortable: false },
        { title: "المادة", key: "subject", sortable: true },
        { title: "نوع السؤال", key: "questionType", sortable: true },
        { title: "الصعوبة", key: "difficulty", sortable: true },
        { title: "الدرجة", key: "defaultMark", sortable: true, align: "center" },
        { title: "الحالة", key: "status", sortable: true },
        { title: "المُنشئ وآخر تعديل", key: "audit", sortable: false },
      ],
    };
  },

  computed: {
    subjectFilterParam() {
      const p = {};
      if (this.filterInstitutionType) {
        p.institution_type = this.filterInstitutionType;
      }
      if (this.filterClassTrack) {
        p.class_track = this.filterClassTrack;
      } else if (this.filterStage) {
        p.stage = this.filterStage;
      }
      if (this.filterSemesterSubject) {
        p.semester_subject = this.filterSemesterSubject;
      } else if (this.filterSpecialization) {
        p.specialization = this.filterSpecialization;
      } else if (this.filterDepartment) {
        p.department = this.filterDepartment;
      } else if (this.filterCollege) {
        p.college = this.filterCollege;
      }
      return Object.keys(p).length > 0 ? p : null;
    },

    instituteSpecParam() {
      const p = {};
      if (this.filterInstituteField) p.field = this.filterInstituteField;
      if (this.filterInstituteEducationSystem) p.education_system = this.filterInstituteEducationSystem;
      return Object.keys(p).length ? p : null;
    },

    instituteSubjectParam() {
      if (this.filterInstituteField) return { field: this.filterInstituteField };
      return null;
    },

    unitFilterParam() {
      if (this.filterInstitutionType === 'university') {
        return this.filterSemesterSubject ? { semester_subject: this.filterSemesterSubject } : null;
      }
      if (this.filterInstitutionType === 'institute') {
        return this.filterInstituteSubject ? { subject: this.filterInstituteSubject } : null;
      }
      return this.filterSubject || null;
    },
  },

  watch: {
    // Only watch page changes if table triggers it, but mostly custom-data-table handles its own.
  },

  async created() {
    await this.fetchData();
  },

  methods: {
    // === DATA FETCHING ===
    async fetchData() {
      this.loading = true;
      try {
        const subjectsRes = await academicService.getSubjects();
        this.subjects = (Array.isArray(subjectsRes) ? subjectsRes : subjectsRes?.data) || [];

        await this.getData();
      } catch (err) {
        console.error("فشل في تحميل البيانات:", err);
      } finally {
        this.loading = false;
      }
    },

    async getData(tableParams = null) {
      this.loading = true;
      try {
        let queryParams = {};
        if (tableParams && tableParams.params) {
          queryParams = { ...tableParams.params, hasPagination: true };
        } else {
          queryParams = { page: this.currentPage, perPage: this.itemsPerPage, hasPagination: true };
        }

        if (this.search) queryParams.search = this.search;
        if (queryParams.page) this.currentPage = queryParams.page;

        // Map local filters to backend API fields
        let filters = [];
        if (this.filterInstitutionType) {
          filters.push({ field: "institution_type", value: this.filterInstitutionType });
        }
        if (this.filterStatus) filters.push({ field: "status", value: this.filterStatus });
        if (this.filterDifficulty) filters.push({ field: "difficulty", value: this.filterDifficulty });
        if (this.filterType) filters.push({ field: "questionType", value: this.filterType });
        if (this.filterBloom) filters.push({ field: "bloomLevel", value: this.filterBloom });
        if (this.filterSubject) {
          if (this.filterInstitutionType === "university") {
            filters.push({ field: "lesson__unit__semester_subject__fk_subject", value: this.filterSubject });
          } else if (this.filterInstitutionType === "school") {
            filters.push({ field: "lesson__unit__class_subject__subject", value: this.filterSubject });
          } else {
            queryParams.subject = this.filterSubject;
          }
        }
        if (this.filterUnit) filters.push({ field: "lesson__unit", value: this.filterUnit });

        // School filters
        if (this.filterStage) filters.push({ field: "lesson__unit__class_subject__class_track__level__stage", value: this.filterStage });
        if (this.filterClassTrack) filters.push({ field: "lesson__unit__class_subject__class_track", value: this.filterClassTrack });

        // University filters
        if (this.filterSemesterSubject) {
          filters.push({ field: "lesson__unit__semester_subject", value: this.filterSemesterSubject });
        } else if (this.filterSpecialization) {
          filters.push({ field: "lesson__unit__semester_subject__fk_specialization", value: this.filterSpecialization });
        } else if (this.filterDepartment) {
          filters.push({ field: "lesson__unit__semester_subject__fk_specialization__fk_section", value: this.filterDepartment });
        } else if (this.filterCollege) {
          filters.push({ field: "lesson__unit__semester_subject__fk_specialization__fk_college", value: this.filterCollege });
        }

        // Institute filters
        if (this.filterInstituteSubject) {
          filters.push({ field: "lesson__subject", value: this.filterInstituteSubject });
        }

        if (filters.length > 0) {
          const response = await this.$axios.post(
            "api/bank/questions/filter-paginate/",
            { filters },
            { params: queryParams }
          );
          this.items = response.data || response?.data?.data || { results: [], pagination: {} };
        } else {
          const response = await this.$axios.get("api/bank/questions/", { params: queryParams });
          this.items = response.data || response?.data?.data || { results: [], pagination: {} };
        }
      } catch (err) {
        console.error("فشل في تحميل بيانات الأسئلة:", err);
      } finally {
        this.loading = false;
      }
    },

    onInstitutionTypeChange() {
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
      this.applyFilters();
    },

    onInstituteFieldChange() {
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterUnit = null;
    },

    onInstituteEducationSystemChange() {
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterUnit = null;
    },

    onInstituteSpecializationChange() {
      this.filterInstituteSubject = null;
      this.filterUnit = null;
    },

    onInstituteSubjectChange() {
      this.filterUnit = null;
    },

    onStageChange() {
      this.filterClassTrack = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onClassTrackChange() {
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onCollegeChange() {
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onDepartmentChange() {
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onSpecializationChange() {
      this.filterSemesterSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onSemesterSubjectChange() {
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onSubjectChange() {
      this.filterUnit = null;
    },

    // === FILTERING ===
    applyFilters() {
      this.currentPage = 1;
      this.getData();
    },

    resetFilters() {
      this.search = "";
      this.filterInstitutionType = null;
      this.filterSubject = null;
      this.filterUnit = null;
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterDifficulty = null;
      this.filterStatus = null;
      this.filterType = null;
      this.filterBloom = null;
      this.currentPage = 1;
      this.getData();
    },

    // === NAVIGATION ===
    editQuestion(question) {
      this.$navigateTo({
        name: "question-bank-new",
        blank: false,
        query: { id: question.id },
      });
    },


    // === QUESTION ACTIONS ===
    async viewQuestion(question) {
      this.selectedQuestion = { ...question, _loading: true };
      this.viewDialog = true;
      try {
        const res = await this.$axios.get(`api/bank/questions/${question.id}/`);
        const details = res?.data?.data || res?.data || res;
        this.selectedQuestion = { ...this.selectedQuestion, ...details, _loading: false };
      } catch (err) {
        console.error("فشل في جلب تفاصيل السؤال:", err);
        if (this.selectedQuestion) {
          this.selectedQuestion._loading = false;
        }
      }
    },

    async openAuditDialog(question) {
      if (!question) return;
      this.auditQuestion = { ...question };
      this.auditDialog = true;
      this.auditLoading = true;
      try {
        const res = await this.$axios.get(`api/bank/questions/${question.id}/`);
        const fullData = res.data?.data || res.data;
        if (fullData) {
          this.auditQuestion = { ...this.auditQuestion, ...fullData };
        }
      } catch (err) {
        console.error("فشل في جلب سجل التدقيق:", err);
      } finally {
        this.auditLoading = false;
      }
    },

    openDeleteDialog(question) {
      this.questionToDelete = question;
      this.deleteDialog = true;
    },

    async executeDelete() {
      if (!this.questionToDelete) return;
      this.deleteLoading = true;
      try {
        await bankService.deleteQuestion(this.questionToDelete.id);
        this.$alert("success", { message: "تم نقل السؤال إلى المهملات بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة حذف السؤال" });
        console.error(err);
      } finally {
        this.deleteDialog = false;
        this.questionToDelete = null;
        this.deleteLoading = false;
      }
    },

    async duplicateQuestion(question) {
      try {
        const res = await bankService.duplicateQuestion(question.id);
        this.$alert("success", { message: "تم استنساخ السؤال بنجاح كمسودة جديدة" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة استنساخ السؤال" });
        console.error(err);
      }
    },

    async archiveQuestion(question) {
      try {
        await bankService.archiveQuestion(question.id);
        this.$alert("success", { message: "تمت أرشفة السؤال بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء أرشفة السؤال" });
        console.error(err);
      }
    },

    async restoreQuestion(question) {
      try {
        await bankService.restoreQuestion(question.id);
        this.$alert("success", { message: "تمت استعادة السؤال إلى مسودة بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء استعادة السؤال" });
        console.error(err);
      }
    },

    async createQuestionVersion(question) {
      const reason = prompt("يرجى كتابة سبب إنشاء إصدار جديد:");
      if (reason === null) return;
      try {
        const res = await bankService.createQuestionVersion(question.id, { reason });
        this.$alert("success", { message: "تم إنشاء الإصدار الجديد بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء إنشاء الإصدار الجديد" });
        console.error(err);
      }
    },

    async updateQuestionStatus(question, newStatus) {
      try {
        await bankService.updateQuestion(question.id, {
          status: newStatus,
        });
        question.status = newStatus;
        this.$alert("success", { message: "تم تحديث حالة السؤال بنجاح" });
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة تحديث حالة السؤال" });
        console.error(err);
      }
    },




    // === HELPERS ===
    stripHtml(html) {
      if (!html) return "";
      const tmp = document.createElement("div");
      tmp.innerHTML = html;
      return tmp.textContent || tmp.innerText || "";
    },

    getSubjectName(question) {
      if (question.subject_name) return question.subject_name;
      const subId = question.subject_id || question.fk_subject;
      if (!subId) return "عام";
      const subject = this.subjects.find((s) => s.id === subId);
      return subject ? subject.name : "عام";
    },

    getStatusColor(status) {
      switch (status) {
        case 'معتمد': return 'success';
        case 'مرفوض': return 'error';
        case 'قيد المراجعة': return 'warning';
        case 'مسودة': return 'grey';
        case 'مستورد': return 'teal';
        default: return 'grey';
      }
    },

    getStatusIcon(status) {
      const icons = {
        معتمد: "mdi-check-decagram",
        مرفوض: "mdi-close-octagon",
        "قيد المراجعة": "mdi-clock-outline",
        مسودة: "mdi-pencil-outline",
        مستورد: "mdi-file-excel-outline",
      };
      return icons[status] || "mdi-file-document-outline";
    },

    getDifficultyColor(difficulty) {
      const d = String(difficulty ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'success';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'warning';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'error';
      return 'blue-grey';
    },

    getDifficultyText(difficulty) {
      const d = String(difficulty ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'سهل';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'متوسط';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'صعب';
      return difficulty || '-';
    },

    getDifficultyIcon(difficulty) {
      const d = String(difficulty ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'mdi-signal-cellular-1';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'mdi-signal-cellular-2';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'mdi-signal-cellular-3';
      return 'mdi-help-circle-outline';
    },

    getTypeText(type) {
      const types = {
        'Single Choice': "اختيار واحد",
        'Multiple Choice': "عدة إجابات",
        'True/False': "صواب / خطأ",
        'Essay': "مقالي",
        'Fill in the Blanks': "فراغات",
        'Matching': "مطابقة",
        'Ordering': "ترتيب",
      };
      return types[type] || type || "-";
    },

    getOptionLetter(idx) {
      const letters = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح'];
      return letters[idx] || String(idx + 1);
    },

    getInstitutionLabel(type) {
      const labels = {
        school: 'تعليم مدرسي',
        university: 'تعليم جامعي',
        institute: 'معاهد وتدريب مهني',
      };
      return labels[type] || 'تعليم مدرسي';
    },

    getBloomColor(level) {
      const colors = {
        'تذكر': '#6366f1',
        'فهم': '#0284c7',
        'تطبيق': '#059669',
        'تحليل': '#d97706',
        'تقييم': '#7c3aed',
        'ابتكار': '#db2777',
      };
      return colors[level] || '#64748b';
    },

    getAcademicHierarchy(q) {
      if (!q) return [];
      const parts = [];
      if (q.institution_type === 'university') {
        if (q.college_name) parts.push({ label: 'الكلية', value: q.college_name, icon: 'mdi-town-hall' });
        if (q.department_name) parts.push({ label: 'القسم', value: q.department_name, icon: 'mdi-door' });
        if (q.specialization_name) parts.push({ label: 'التخصص', value: q.specialization_name, icon: 'mdi-certificate' });
        if (q.semester_subject_name) parts.push({ label: 'المقرر', value: q.semester_subject_name, icon: 'mdi-book-education' });
        else if (q.subject_name) parts.push({ label: 'المادة', value: q.subject_name, icon: 'mdi-book-education' });
      } else if (q.institution_type === 'institute') {
        if (q.institute_field_name) parts.push({ label: 'المجال', value: q.institute_field_name, icon: 'mdi-tools' });
        if (q.institute_specialization_name) parts.push({ label: 'التخصص', value: q.institute_specialization_name, icon: 'mdi-certificate' });
        if (q.subject_name) parts.push({ label: 'المادة', value: q.subject_name, icon: 'mdi-book-education' });
      } else {
        if (q.stage_name) parts.push({ label: 'المرحلة', value: q.stage_name, icon: 'mdi-stairs' });
        if (q.class_track_name) parts.push({ label: 'الصف والمسار', value: q.class_track_name, icon: 'mdi-google-classroom' });
        const sub = q.subject_name || this.getSubjectName(q);
        if (sub && sub !== 'عام') parts.push({ label: 'المادة', value: sub, icon: 'mdi-book-education' });
      }
      if (q.unit_name) parts.push({ label: 'الوحدة', value: q.unit_name, icon: 'mdi-folder-outline' });
      if (q.lesson_name) parts.push({ label: 'الدرس', value: q.lesson_name, icon: 'mdi-bookmark-outline' });
      return parts;
    },

    copyQuestionContent(q) {
      if (!q) return;
      const cleanContent = this.stripHtml(q.content);
      let text = `السؤال #${q.id} (${this.getTypeText(q.questionType)}):\n${cleanContent}\n\n`;
      if (q.options && q.options.length) {
        text += 'الخيارات:\n';
        q.options.forEach((opt, idx) => {
          const letter = this.getOptionLetter(idx);
          const correct = opt.isTrue ? ' (✓ الإجابة الصحيحة)' : '';
          text += `${letter}) ${this.stripHtml(opt.text)}${correct}\n`;
        });
      } else if (q.isTrue !== null && q.isTrue !== undefined) {
        text += `الإجابة الصحيحة: ${q.isTrue ? 'صح (صواب)' : 'خطأ'}\n`;
      } else if (q.answerText) {
        text += `الإجابة المرجعية: ${this.stripHtml(q.answerText)}\n`;
      }
      if (navigator?.clipboard?.writeText) {
        navigator.clipboard.writeText(text);
        this.$alert?.('success', { message: 'تم نسخ نص السؤال وخياراته بنجاح' });
      }
    },

    printQuestionCard() {
      window.print();
    },

    getDiscriminationAnalysis(d) {
      if (d == null) return { text: 'غير محسوب', color: 'grey', desc: 'لا توجد بيانات كافية' };
      const val = Number(d);
      if (val >= 0.4) return { text: 'ممتاز جداً', color: 'success', desc: 'يميز بدقة عالية بين مستويات الطلاب' };
      if (val >= 0.3) return { text: 'جيد ومقبول', color: 'primary', desc: 'قدرة تمييز مناسبة لمعايير القياس' };
      if (val >= 0.2) return { text: 'حد حرج', color: 'warning', desc: 'يحتاج مراجعة أو تحسين صياغة البدائل' };
      return { text: 'ضعيف / سالب', color: 'error', desc: 'فقرة غير مميزة ويُنصح بتعديلها أو استبعادها' };
    },

    getDifficultyAnalysis(p) {
      if (p == null) return { text: 'غير محسوب', color: 'grey', desc: 'لا توجد بيانات كافية' };
      const val = Number(p);
      if (val > 0.8) return { text: 'سهل جداً', color: 'success', desc: 'نسبة الإجابة الصحيحة مرتفعة' };
      if (val >= 0.3) return { text: 'متوازن ومثالي', color: 'info', desc: 'صعوبة متوازنة ضمن النطاق القياسي' };
      return { text: 'صعب جداً', color: 'error', desc: 'نسبة النجاح منخفضة' };
    },

    formatAuditDate(dateStr) {
      if (!dateStr) return "—";
      try {
        const d = new Date(dateStr);
        if (isNaN(d.getTime())) return dateStr;
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, "0");
        const day = String(d.getDate()).padStart(2, "0");
        const hours = String(d.getHours()).padStart(2, "0");
        const mins = String(d.getMinutes()).padStart(2, "0");
        return `${year}-${month}-${day} ${hours}:${mins}`;
      } catch (e) {
        return dateStr;
      }
    },

    getActionBadgeColor(action) {
      if (!action) return "grey";
      const act = String(action).trim();
      if (act === "استيراد جماعي") return "teal";
      if (act === "إنشاء") return "primary";
      if (act === "تعديل") return "warning";
      if (act === "اعتماد" || act === "استعادة") return "success";
      if (act === "رفض" || act === "حذف") return "error";
      if (act === "استنساخ") return "indigo";
      if (act === "إصدار جديد") return "teal";
      if (act === "أرشفة") return "purple";
      return "info";
    },

    getActionIcon(action) {
      if (!action) return "mdi-checkbox-blank-circle-outline";
      const act = String(action).trim();
      if (act === "إنشاء") return "mdi-plus-circle";
      if (act === "تعديل") return "mdi-pencil";
      if (act === "اعتماد") return "mdi-check-decagram";
      if (act === "رفض") return "mdi-close-octagon";
      if (act === "استنساخ") return "mdi-content-copy";
      if (act === "إصدار جديد") return "mdi-source-branch";
      if (act === "أرشفة") return "mdi-archive-arrow-down";
      if (act === "استعادة") return "mdi-archive-arrow-up";
      if (act === "استيراد جماعي") return "mdi-file-excel-outline";
      return "mdi-clock-outline";
    },
  },
};
</script>

<style scoped>
.qb-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Primary Action Button ===== */
.btn-glow-primary {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, color-mix(in srgb, rgb(var(--v-theme-primary)) 85%, #000) 100%) !important;
  box-shadow: 0 8px 24px -4px rgba(var(--v-theme-primary), 0.45) !important;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
  letter-spacing: 0.02em;
}

.btn-glow-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 32px -4px rgba(var(--v-theme-primary), 0.55) !important;
}

.btn-glow-primary:active {
  transform: translateY(-1px);
}

/* ===== Question Preview Dialog Styles ===== */
.qb-preview-dialog-canvas {
  font-family: inherit;
  color: rgb(var(--v-theme-on-surface));
}

.academic-hierarchy-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.02);
}

.hierarchy-pill {
  background: rgba(var(--v-theme-on-surface), 0.03) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  color: rgb(var(--v-theme-on-surface));
}

.question-paper-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
  box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
}

.question-paper-header {
  background: rgb(var(--v-theme-surface)) !important;
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12) !important;
}

.bg-surface-variant-subtle {
  background: rgb(var(--v-theme-surface)) !important;
}

.question-idea-box {
  background: rgba(245, 158, 11, 0.07);
  border: 1px solid rgba(245, 158, 11, 0.28) !important;
}

.question-image-frame {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
}

.question-body-rendered {
  color: rgb(var(--v-theme-on-surface));
  letter-spacing: -0.01em;
}

.question-body-rendered :deep(p) {
  margin-bottom: 0.5rem;
}

.question-body-rendered :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

.question-body-rendered :deep(th),
.question-body-rendered :deep(td) {
  border: 1px solid rgba(var(--v-border-color), 0.2);
  padding: 8px 12px;
}

.option-row-card {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.option-row-correct {
  background: rgba(16, 185, 129, 0.08) !important;
  border: 2px solid #10b981 !important;
  box-shadow: 0 4px 12px -2px rgba(16, 185, 129, 0.18);
}

.option-row-neutral {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
}

.option-row-neutral:hover {
  background: rgba(var(--v-theme-primary), 0.03) !important;
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
}

.tf-card-active {
  background: rgba(16, 185, 129, 0.08) !important;
  border: 2px solid #10b981 !important;
}

.tf-card-inactive {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
  opacity: 0.75;
}

.model-answer-box {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.3) !important;
  border-right: 5px solid #10b981 !important;
}

.psychometrics-box {
  background: rgba(99, 102, 241, 0.04);
  border-color: rgba(99, 102, 241, 0.2) !important;
}

.metric-tile {
  background: rgb(var(--v-theme-surface)) !important;
  border-color: rgba(var(--v-border-color), 0.1) !important;
  transition: transform 0.2s ease;
}

.metric-tile:hover {
  transform: translateY(-2px);
}

.audit-table-cell {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}

.audit-table-cell:hover {
  background-color: rgba(var(--v-theme-primary), 0.06);
  border-color: rgba(var(--v-theme-primary), 0.25);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.audit-hover-icon {
  opacity: 0;
  transform: translateX(-4px);
  transition: all 0.2s ease;
}

.audit-table-cell:hover .audit-hover-icon {
  opacity: 0.9;
  transform: translateX(0);
}

.institutional-audit-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.02);
}

.audit-summary-tile {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
  transition: transform 0.2s ease;
}

.audit-summary-tile:hover {
  transform: translateY(-2px);
}

.audit-timeline-row {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  transition: all 0.2s ease;
}

.audit-timeline-row:hover {
  background: rgba(var(--v-theme-primary), 0.02) !important;
  border-color: rgba(var(--v-theme-primary), 0.25) !important;
}

@media print {
  body * {
    visibility: hidden;
  }
  .v-dialog, .v-dialog * {
    visibility: visible;
  }
  .v-dialog {
    position: absolute;
    left: 0;
    top: 0;
    width: 100% !important;
  }
  .footer-zone, .v-btn {
    display: none !important;
  }
}
</style>
