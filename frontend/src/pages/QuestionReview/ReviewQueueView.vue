<template>
  <div>
    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="تصفية نتائج المراجعة" class="main-card border-0 pa-5 rounded-2xl">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / معاهد) -->
        <v-col cols="12" sm="6" :md="filterInstitutionType ? 2 : 3">
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

        <!-- Status Filter -->
        <v-col cols="12" sm="6" :md="filterInstitutionType ? 2 : 3">
          <v-select v-model="filterStatus" :items="statusOptions" item-title="text" item-value="value" class="mb-6"
            placeholder="حالة السؤال" prepend-inner-icon="mdi-flag-outline" hide-details clearable density="compact"
            variant="outlined" />
        </v-col>

        <!-- الظهور مشروط باختيار نوع المؤسسة: مدارس أو جامعات أو معاهد -->
        <template v-if="filterInstitutionType">
          <!-- 🏫 School Filters -->
          <template v-if="filterInstitutionType === 'school'">
            <auto-list
              v-model="filterStage"
              name="Stage"
              label="المرحلة الدراسية"
              cols="2"
              :add="false"
              @update:model-value="() => { filterClassTrack = null; filterSubject = null; }"
            />
            <auto-list
              v-model="filterClassTrack"
              name="ClassTrackByStage"
              :param="filterStage"
              label="الصف والمسار"
              cols="2"
              :add="false"
              :disabled="!filterStage"
              @update:model-value="filterSubject = null"
            />
            <auto-list
              v-model="filterSubject"
              name="Subject"
              :param="filterClassTrack || filterStage"
              label="المادة الدراسية"
              cols="2"
              :add="false"
              :disabled="!filterClassTrack && !filterStage"
              @update:model-value="filterUnit = null"
            />
          </template>

          <!-- 🎓 University Filters -->
          <template v-if="filterInstitutionType === 'university'">
            <auto-list
              v-model="filterCollege"
              name="College"
              label="الكلية الجامعية"
              cols="2"
              :add="false"
              @update:model-value="onCollegeChange"
            />
            <auto-list
              v-model="filterDepartment"
              name="DepartmentByCollege"
              :param="filterCollege"
              label="القسم الأكاديمي"
              cols="2"
              :add="false"
              :disabled="!filterCollege"
              @update:model-value="filterSpecialization = null"
            />
            <auto-list
              v-model="filterSpecialization"
              name="Specialization"
              :param="filterDepartment"
              label="التخصص والبرنامج"
              cols="2"
              :add="false"
              :disabled="!filterDepartment"
            />
            <auto-list
              v-model="filterSemesterSubject"
              name="SemesterSubject"
              :param="filterSpecialization"
              label="مقرر الفصل الجامعي"
              cols="2"
              :add="false"
              @update:model-value="filterUnit = null"
            />
          </template>

          <!-- 🏢 Institute Filters -->
          <template v-if="filterInstitutionType === 'institute'">
            <auto-list
              v-model="filterInstituteField"
              name="InstituteField"
              label="المجال المهني"
              cols="2"
              :add="false"
              @update:model-value="filterInstituteSpecialization = null"
            />
            <auto-list
              v-model="filterInstituteEducationSystem"
              name="InstituteEducationSystem"
              label="نظام التعليم"
              cols="2"
              :add="false"
              @update:model-value="filterInstituteSpecialization = null"
            />
            <auto-list
              v-model="filterInstituteSpecialization"
              name="InstituteSpecialization"
              :param="filterInstituteSpecParam"
              label="التخصص المهني"
              cols="2"
              :add="false"
              :disabled="!filterInstituteField && !filterInstituteEducationSystem"
              @update:model-value="filterInstituteCurriculum = null"
            />
            <auto-list
              v-model="filterInstituteCurriculum"
              name="InstituteCurriculum"
              :param="filterInstituteSpecialization"
              label="الخطة الدراسية"
              cols="2"
              :add="false"
              :disabled="!filterInstituteSpecialization"
              @update:model-value="filterInstituteSubject = null"
            />
            <auto-list
              v-model="filterInstituteSubject"
              name="InstituteSubject"
              :param="filterInstituteCurriculum"
              label="المادة التدريبية"
              cols="2"
              :add="false"
              :disabled="!filterInstituteCurriculum"
              @update:model-value="filterUnit = null"
            />
          </template>

          <!-- Unit / Topic Filter (الوحدة للمدارس ومفردة المقرر للجامعات والوحدة التدريبية للمعاهد) -->
          <auto-list
            v-model="filterUnit"
            name="UnitBySubject"
            :param="filterUnitParam"
            :label="filterInstitutionType === 'university' ? 'مفردة / موضوع المقرر' : (filterInstitutionType === 'institute' ? 'الوحدة التدريبية' : 'الوحدة الدراسية')"
            cols="2"
            :add="false"
            :disabled="filterInstitutionType === 'university' ? !filterSemesterSubject : (filterInstitutionType === 'institute' ? !filterInstituteSubject : !filterSubject)"
          />
        </template>

        <!-- Filter Actions -->
        <v-col cols="12" sm="12" md="2" class="d-flex align-center gap-2">
          <custom-btn type="show" label="تصفية" color="primary" class="font-weight-bold flex-grow-1 mb-6"
            :click="getData" />
          <custom-btn type="cancel_filter" :click="resetFilters" variant="tonal" color="error" label="تفريغ"
            class="font-weight-bold mb-6" />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Questions Data Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table :items="tableItems" :getData="getData" :headers="headers" :hasFilter="false" :log="false"
        :restore="false">
        <template v-slot:item-slot="{ item, key }">

          <!-- Author, Modifier & Excel Import (Same as Question Bank) -->
          <template v-if="key === 'audit' || key === 'author'">
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
                    {{ item.author_name || item.created_by_username || getAuthorName(item) }}
                  </span>
                  <v-chip
                    v-if="isImportedFromExcel(item)"
                    size="x-small"
                    variant="flat"
                    color="teal"
                    class="px-1 font-weight-bold"
                    style="height: 18px; font-size: 0.65rem !important;"
                    title="مصدر السؤال: مستورد من ملف إكسل"
                  >
                    <v-icon start size="11">mdi-file-excel</v-icon>
                    إكسل
                  </v-chip>
                  <v-chip
                    v-else
                    size="x-small"
                    variant="tonal"
                    color="primary"
                    class="px-1 font-weight-bold"
                    style="height: 18px; font-size: 0.65rem !important;"
                    title="مصدر السؤال: إدخال يدوي في النظام"
                  >
                    <v-icon start size="11">mdi-keyboard-outline</v-icon>
                    يدوي
                  </v-chip>
                  <v-chip
                    v-if="item.edit_count > 0"
                    size="x-small"
                    variant="flat"
                    color="warning"
                    class="px-1 font-weight-bold"
                    style="height: 18px; font-size: 0.65rem !important;"
                    title="عدد مرات التعديل"
                  >
                    {{ item.edit_count }} تعديل
                  </v-chip>
                </div>

                <div class="text-caption text-disabled d-flex align-center gap-1 mt-0-5" style="font-size: 0.72rem !important;">
                  <v-icon size="11">mdi-clock-outline</v-icon>
                  <span>{{ formatAuditDate(item.last_modified_at || item.created_at) }}</span>
                  <span
                    v-if="item.last_modified_by && item.last_modified_by !== (item.author_name || item.created_by_username)"
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

          <!-- Content Snippet -->
          <div v-else-if="key === 'content'" class="text-body-2 text-truncate"
            style="max-width: 300px; white-space: normal; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
            <span
              v-html="(item.questionType === 'صح وخطأ' || item.questionType === 'True/False') && !item.content ? '[صواب/خطأ بدون نص]' : item.content"></span>
          </div>

          <!-- Subject -->
          <div v-else-if="key === 'subject'" class="d-flex flex-column align-start gap-1">
            <v-chip size="small" color="surface-variant" class="font-weight-medium px-3 justify-start">
              <v-icon start size="14" color="secondary">mdi-book-open-variant</v-icon>
              {{ getSubjectName(item) }}
            </v-chip>
            <v-chip v-if="filterInstitutionType === 'all' && item.institution_type" size="x-small"
              :color="item.institution_type === 'university' ? 'purple' : 'primary'" variant="tonal" class="font-weight-bold">
              {{ item.institution_type === 'university' ? '🎓 جامعي' : '🏫 مدرسي' }}
            </v-chip>
          </div>

          <!-- Question Type -->
          <div v-else-if="key === 'questionType'">
            <v-chip size="small" color="info" variant="tonal" class="font-weight-bold">
              {{ item.questionType === 'True/False' ? 'صح وخطأ' : item.questionType }}
            </v-chip>
          </div>

          <!-- Difficulty -->
          <div v-else-if="key === 'difficulty'">
            <v-chip size="small" :color="getDifficultyColor(item.difficulty)" variant="tonal"
              class="font-weight-bold text-white">
              {{ getDifficultyText(item.difficulty) }}
            </v-chip>
          </div>

          <!-- Status -->
          <div v-else-if="key === 'status'">
            <v-chip size="small" :color="getStatusColor(item.status)" class="font-weight-bold" variant="tonal">
              {{ getStatusText(item.status) }}
            </v-chip>
          </div>

          <!-- Actions -->
          <div v-else-if="key === 'actions'" class="d-flex align-center justify-center">
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

                <v-card-text class="pa-1">
                  <v-list density="compact" class="bg-transparent pa-0">
                    <v-list-subheader class="modern-subheader px-2 mt-1 mb-1">
                      خيارات المراجعة
                    </v-list-subheader>

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

                    <template v-if="item.parent_version || item.version_number > 1">
                      <v-list-item @click="openDiffDialog(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="indigo" class="me-2">mdi-compare-horizontal</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-indigo">
                          مقارنة النسخ (Diff v{{ item.version_number }})
                        </v-list-item-title>
                      </v-list-item>
                    </template>

                    <template v-if="item.status === 'قيد المراجعة'">
                      <v-list-item @click="openChecklistDialog(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="success" class="me-2">mdi-check-decagram</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-success">
                          تدقيق واعتماد السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item @click="escalateToDeptHead(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="amber" class="me-2">mdi-account-tie-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-amber">
                          إحالة لرئيس القسم
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item @click="openRejectDialog(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="error" class="me-2">mdi-close-octagon</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-error">
                          رفض مسبب
                        </v-list-item-title>
                      </v-list-item>
                    </template>

                    <template v-else>
                      <v-list-item v-if="item.status !== 'معتمد'" @click="openChecklistDialog(item)"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="success" class="me-2">mdi-refresh</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-success">
                          إعادة اعتماد
                        </v-list-item-title>
                      </v-list-item>
                    </template>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-menu>
          </div>
        </template>
      </custom-data-table>
    </div>

    <!-- View Question Dialog (Modern Official Dossier) -->
    <CustomDialog v-model="viewDialog" width="960" :showClose="true">
      <template #title>
        <div class="d-flex align-center justify-space-between w-100 flex-wrap gap-2">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" size="44" rounded="xl" class="elevation-1">
              <v-icon size="26" color="primary">mdi-clipboard-check-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2">
                <span class="text-h6 font-weight-black" style="color: rgb(var(--v-theme-on-surface));">
                  بطاقة فحص ومراجعة السؤال الأكاديمي
                </span>
                <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
                  #{{ selectedQuestion?.id }}
                </v-chip>
                <v-chip size="x-small" variant="tonal" color="info" class="font-weight-bold">
                  v{{ selectedQuestion?.version_number || 1 }}
                </v-chip>
                <v-chip v-if="isImportedFromExcel(selectedQuestion)" size="x-small" color="teal" variant="flat" class="font-weight-bold">
                  <v-icon start size="12">mdi-file-excel</v-icon>
                  مستورد من إكسل
                </v-chip>
                <v-chip v-else size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                  <v-icon start size="12">mdi-keyboard-outline</v-icon>
                  إدخال يدوي
                </v-chip>
              </div>
              <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-1">
                <span>{{ getInstitutionLabel(selectedQuestion?.institution_type) }}</span>
                <span>•</span>
                <span v-if="selectedQuestion?.subject_name">{{ selectedQuestion.subject_name }}</span>
                <span v-else>{{ getSubjectName(selectedQuestion) }}</span>
              </div>
            </div>
          </div>

          <div class="d-flex align-center gap-2">
            <custom-btn
              text="سجل التعديلات والتدقيق"
              icon="mdi-history"
              size="small"
              variant="tonal"
              color="indigo"
              class="font-weight-bold"
              @click="openAuditDialog(selectedQuestion)"
            />
            <custom-btn
              v-if="selectedQuestion?.parent_version"
              text="مقارنة الإصدارات"
              icon="mdi-source-branch"
              size="small"
              variant="tonal"
              color="indigo"
              class="font-weight-bold"
              @click="openDiffDialog(selectedQuestion)"
            />
          </div>
        </div>
      </template>

      <template v-if="selectedQuestion">
        <div class="review-details-canvas pa-1">
          <!-- Specifications Ribbon -->
          <div class="d-flex flex-wrap align-center gap-2 mb-4">
            <!-- Current Status Chip -->
            <v-chip :color="getStatusColor(selectedQuestion.status)" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">{{ getStatusIcon(selectedQuestion.status) }}</v-icon>
              الحالة: {{ getStatusText(selectedQuestion.status) }}
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
              :style="`color: ${getBloomColor(selectedQuestion.bloomLevel)}; background-color: ${getBloomColor(selectedQuestion.bloomLevel)}14; border: 1px solid ${getBloomColor(selectedQuestion.bloomLevel)}35;`">
              <v-icon start size="16">mdi-brain</v-icon>
              بلوم: {{ getBloomText(selectedQuestion.bloomLevel) }}
            </v-chip>

            <!-- Default Mark -->
            <v-chip color="amber-darken-3" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-star-circle-outline</v-icon>
              الدرجة: {{ selectedQuestion.defaultMark || 1 }} درجات
            </v-chip>

            <!-- Expected Time -->
            <v-chip v-if="selectedQuestion.expected_time_minutes" color="teal" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-clock-outline</v-icon>
              الوقت: {{ selectedQuestion.expected_time_minutes }} دقيقة
            </v-chip>

            <!-- Question Source Tag (Excel or Manual) -->
            <v-chip v-if="isImportedFromExcel(selectedQuestion)" color="teal-darken-1" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-file-excel</v-icon>
              المصدر: مستورد من ملف إكسل
            </v-chip>
            <v-chip v-else color="primary" variant="tonal" class="font-weight-bold px-3 py-1">
              <v-icon start size="16">mdi-keyboard-outline</v-icon>
              المصدر: إدخال يدوي مباشر
            </v-chip>
          </div>

          <!-- Rejection Alert (if rejected) -->
          <v-alert
            v-if="selectedQuestion.status === 'مرفوض' && (selectedQuestion.rejectionReason || selectedQuestion.rejection_reason)"
            type="error"
            variant="tonal"
            density="comfortable"
            class="rounded-xl mb-4 border"
            icon="mdi-alert-octagon-outline"
          >
            <div class="font-weight-bold text-subtitle-2 mb-1">سبب الرفض المدوّن من المراجع:</div>
            <div class="text-body-2">{{ selectedQuestion.rejectionReason || selectedQuestion.rejection_reason }}</div>
          </v-alert>

          <!-- Academic Pathway Card (Breadcrumbs) -->
          <div class="academic-hierarchy-card pa-3 px-4 rounded-xl mb-4 border d-flex align-center flex-wrap gap-2">
            <div class="d-flex align-center gap-1 text-caption font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">
              <v-icon size="16" color="primary">mdi-sitemap</v-icon>
              <span>المسار الأكاديمي:</span>
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
          </div>

          <!-- Question Paper Canvas (Official Exam Card) -->
          <div class="question-paper-card rounded-2xl mb-4 border overflow-hidden">
            <div class="question-paper-header px-5 py-3 d-flex align-center justify-space-between border-b">
              <div class="d-flex align-center gap-2">
                <v-icon size="18" color="primary">mdi-format-quote-open</v-icon>
                <span class="text-subtitle-2 font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">
                  نص السؤال المعروض للطالب
                </span>
              </div>
              <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                السؤال الأساسي
              </v-chip>
            </div>

            <div class="pa-5">
              <!-- Description / Educational Idea Box -->
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

              <!-- Question Image Frame -->
              <div v-if="selectedQuestion.image" class="question-image-frame mb-4 pa-3 rounded-xl text-center border">
                <v-img :src="selectedQuestion.image" max-height="320" class="rounded-lg mx-auto" contain />
                <div class="text-caption text-medium-emphasis mt-2">
                  <v-icon size="14">mdi-image-outline</v-icon> رسم / شكل توضيحي مرفق بالسؤال
                </div>
              </div>

              <!-- Question Text Body -->
              <div class="question-body-rendered text-body-1 font-weight-bold" style="line-height: 2.1; font-size: 1.15rem !important;"
                v-html="selectedQuestion.content" />
            </div>
          </div>

          <!-- Answers & Alternatives Section -->
          <div class="answers-section mb-4">
            <div class="d-flex align-center justify-space-between mb-3 px-1">
              <div class="d-flex align-center gap-2">
                <v-icon size="20" color="success">mdi-format-list-checks</v-icon>
                <h4 class="text-subtitle-1 font-weight-black" style="color: rgb(var(--v-theme-on-surface));">
                  {{ (getQuestionAnswers(selectedQuestion.id).length > 0) ? 'بدائل وخيارات الإجابة' : 'نموذج الإجابة المعتمدة' }}
                </h4>
              </div>
              <span class="text-caption text-medium-emphasis" v-if="getQuestionAnswers(selectedQuestion.id).length > 0">
                {{ getQuestionAnswers(selectedQuestion.id).length }} بدائل مسجلة
              </span>
            </div>

            <!-- 1. Multiple Choice / Single Choice Options List -->
            <div v-if="getQuestionAnswers(selectedQuestion.id).length > 0" class="d-flex flex-column gap-2">
              <div
                v-for="(answer, i) in getQuestionAnswers(selectedQuestion.id)"
                :key="answer.id || i"
                class="option-row-card pa-4 rounded-xl d-flex align-center justify-space-between gap-3 border"
                :class="{ 'option-row-correct': answer.isTrue, 'option-row-neutral': !answer.isTrue }"
              >
                <div class="d-flex align-center gap-3 overflow-hidden flex-grow-1">
                  <!-- Arabic Letter Avatar (أ، ب، ج، د...) -->
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

                <!-- Correct Indicator Chip -->
                <div class="flex-shrink-0">
                  <v-chip
                    v-if="answer.isTrue"
                    color="success"
                    variant="flat"
                    size="small"
                    class="font-weight-bold px-3"
                  >
                    <v-icon start size="14">mdi-check-decagram</v-icon>
                    الإجابة الصحيحة
                  </v-chip>
                  <v-chip v-else size="x-small" variant="tonal" color="blue-grey" class="text-caption px-2">
                    بديل غير صحيح
                  </v-chip>
                </div>
              </div>
            </div>

            <!-- 2. True / False Dual Showcase -->
            <div v-else-if="selectedQuestion.isTrue !== null && selectedQuestion.isTrue !== undefined" class="d-flex gap-4">
              <!-- True Card -->
              <div
                class="pa-4 rounded-xl flex-grow-1 border d-flex align-center justify-space-between transition-all"
                :class="selectedQuestion.isTrue ? 'tf-card-active' : 'tf-card-inactive'"
              >
                <div class="d-flex align-center gap-3">
                  <v-avatar size="38" :color="selectedQuestion.isTrue ? 'success' : 'primary'" :variant="selectedQuestion.isTrue ? 'flat' : 'tonal'">
                    <v-icon size="22" :color="selectedQuestion.isTrue ? 'white' : 'primary'">mdi-check</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-1 font-weight-bold" :class="selectedQuestion.isTrue ? 'text-success' : 'text-medium-emphasis'">
                      صواب (True)
                    </div>
                    <div class="text-caption text-medium-emphasis">العبارة صحيحة علمياً</div>
                  </div>
                </div>
                <v-chip v-if="selectedQuestion.isTrue" color="success" size="small" variant="flat" class="font-weight-bold">
                  <v-icon start size="14">mdi-check-decagram</v-icon>
                  الإجابة الصحيحة
                </v-chip>
              </div>

              <!-- False Card -->
              <div
                class="pa-4 rounded-xl flex-grow-1 border d-flex align-center justify-space-between transition-all"
                :class="!selectedQuestion.isTrue ? 'tf-card-active' : 'tf-card-inactive'"
              >
                <div class="d-flex align-center gap-3">
                  <v-avatar size="38" :color="!selectedQuestion.isTrue ? 'success' : 'primary'" :variant="!selectedQuestion.isTrue ? 'flat' : 'tonal'">
                    <v-icon size="22" :color="!selectedQuestion.isTrue ? 'white' : 'primary'">mdi-close</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-1 font-weight-bold" :class="!selectedQuestion.isTrue ? 'text-success' : 'text-medium-emphasis'">
                      خطأ (False)
                    </div>
                    <div class="text-caption text-medium-emphasis">العبارة خاطئة علمياً</div>
                  </div>
                </div>
                <v-chip v-if="!selectedQuestion.isTrue" color="success" size="small" variant="flat" class="font-weight-bold">
                  <v-icon start size="14">mdi-check-decagram</v-icon>
                  الإجابة الصحيحة
                </v-chip>
              </div>
            </div>

            <!-- 3. Essay / Fill in the blank Model Answer -->
            <div v-else-if="selectedQuestion.answerText" class="model-answer-box pa-5 rounded-2xl border">
              <div class="d-flex align-center gap-2 mb-3">
                <v-icon size="20" color="success">mdi-text-box-check-outline</v-icon>
                <span class="text-subtitle-2 font-weight-bold text-success-darken-1">معايير الإجابة النموذجية وسلّم التقدير</span>
              </div>
              <div class="text-body-1 font-weight-medium" style="line-height: 1.9;" v-html="selectedQuestion.answerText" />
            </div>
          </div>

          <!-- Author and Reviewer Dossier Card -->
          <div class="author-dossier-card pa-4 rounded-2xl border mb-2">
            <div class="d-flex align-center gap-2 mb-3 border-b pb-2">
              <v-icon size="18" color="primary">mdi-account-details-outline</v-icon>
              <span class="text-subtitle-2 font-weight-bold" style="color: rgb(var(--v-theme-on-surface));">
                سجل إسناد ومراجعة السؤال
              </span>
            </div>

            <v-row dense>
              <!-- Author Column -->
              <v-col cols="12" md="6">
                <div class="d-flex align-center gap-3 pa-3 rounded-xl border audit-person-tile">
                  <v-avatar color="primary" variant="tonal" size="44" class="font-weight-black">
                    {{ getAuthorName(selectedQuestion).charAt(0) }}
                  </v-avatar>
                  <div class="overflow-hidden">
                    <div class="text-caption text-medium-emphasis">مُعدّ ومؤلف السؤال</div>
                    <div class="text-subtitle-2 font-weight-bold text-truncate" style="color: rgb(var(--v-theme-on-surface));">
                      {{ getAuthorName(selectedQuestion) }}
                    </div>
                    <div class="text-caption text-medium-emphasis d-flex align-center gap-1 mt-1">
                      <v-icon size="13">mdi-calendar-clock</v-icon>
                      <span>تاريخ الإعداد: {{ formatAuditDate(selectedQuestion.created_at || selectedQuestion.createdAt) }}</span>
                    </div>
                    <div class="mt-1 d-flex align-center gap-1">
                      <v-chip
                        size="x-small"
                        :color="isImportedFromExcel(selectedQuestion) ? 'teal' : 'primary'"
                        :variant="isImportedFromExcel(selectedQuestion) ? 'flat' : 'tonal'"
                        class="font-weight-bold"
                      >
                        <v-icon start size="12">{{ isImportedFromExcel(selectedQuestion) ? 'mdi-file-excel' : 'mdi-keyboard-outline' }}</v-icon>
                        {{ isImportedFromExcel(selectedQuestion) ? 'طريقة الإنشاء: مستورد من ملف إكسل' : 'طريقة الإنشاء: إدخال يدوي مباشر' }}
                      </v-chip>
                    </div>
                  </div>
                </div>
              </v-col>

              <!-- Reviewer Column -->
              <v-col cols="12" md="6">
                <div class="d-flex align-center gap-3 pa-3 rounded-xl border audit-person-tile">
                  <v-avatar :color="selectedQuestion.reviewer_name || selectedQuestion.approved_at ? 'success' : 'primary'" variant="tonal" size="44" class="font-weight-black">
                    <v-icon size="22">{{ selectedQuestion.reviewer_name || selectedQuestion.approved_at ? 'mdi-account-check' : 'mdi-account-clock' }}</v-icon>
                  </v-avatar>
                  <div class="overflow-hidden">
                    <div class="text-caption text-medium-emphasis">المراجع الأكاديمي</div>
                    <div class="text-subtitle-2 font-weight-bold text-truncate" style="color: rgb(var(--v-theme-on-surface));">
                      {{ selectedQuestion.reviewer_name || (selectedQuestion.status === 'معتمد' ? 'مراجع معتمد' : 'بانتظار المراجعة') }}
                    </div>
                    <div class="text-caption text-medium-emphasis d-flex align-center gap-1 mt-1">
                      <v-icon size="13">mdi-check-decagram-outline</v-icon>
                      <span v-if="selectedQuestion.approved_at">تاريخ الاعتماد: {{ formatAuditDate(selectedQuestion.approved_at) }}</span>
                      <span v-else-if="selectedQuestion.status === 'قيد المراجعة'">قيد الفحص والتدقيق حالياً</span>
                      <span v-else>—</span>
                    </div>
                  </div>
                </div>
              </v-col>
            </v-row>
          </div>
        </div>
      </template>

      <template #actions>
        <custom-btn
          label="إغلاق"
          variant="outlined"
          color="primary"
          class="font-weight-bold px-4"
          :click="() => viewDialog = false"
        />

        <div class="d-flex align-center gap-2 ms-auto">
          <template v-if="selectedQuestion && selectedQuestion.status === 'قيد المراجعة'">
            <!-- Reject Button -->
            <custom-btn
              type="del"
              label="رفض السؤال"
              icon="mdi-close-circle-outline"
              color="error"
              variant="tonal"
              class="font-weight-bold"
              :click="() => { openRejectDialog(selectedQuestion); viewDialog = false; }"
            />

            <!-- Review Checklist Dialog Button -->
            <custom-btn
              label="فحص المعايير السبعة"
              icon="mdi-checkbox-marked-circle-outline"
              color="primary"
              variant="tonal"
              class="font-weight-bold"
              :click="() => { openChecklistDialog(selectedQuestion); viewDialog = false; }"
            />

            <!-- Direct Approve Button with Success Glow -->
            <custom-btn
              type="add"
              label="اعتماد السؤال"
              icon="mdi-check-decagram"
              color="success"
              class="font-weight-bold btn-glow-success px-5"
              :click="() => { approveQuestion(selectedQuestion); viewDialog = false; }"
            />
          </template>

          <template v-else-if="selectedQuestion && selectedQuestion.status === 'مرفوض'">
            <custom-btn
              type="restore"
              label="إعادة النظر والاعتماد"
              icon="mdi-refresh"
              color="success"
              class="font-weight-bold btn-glow-success px-5"
              :click="() => { approveQuestion(selectedQuestion); viewDialog = false; }"
            />
          </template>

          <template v-else-if="selectedQuestion && selectedQuestion.status === 'معتمد'">
            <v-chip color="success" variant="flat" class="font-weight-bold px-3">
              <v-icon start size="16">mdi-check-decagram</v-icon>
              السؤال معتمد رسمياً
            </v-chip>
          </template>
        </div>
      </template>
    </CustomDialog>

    <!-- Audit Log Dialog -->
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
                <v-chip v-if="isImportedFromExcel(auditQuestion)" size="x-small" variant="flat" color="teal" class="font-weight-bold">
                  <v-icon start size="12">mdi-file-excel</v-icon>
                  مستورد من إكسل
                </v-chip>
                <v-chip v-else size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                  <v-icon start size="12">mdi-keyboard-outline</v-icon>
                  إدخال يدوي
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
                    {{ auditQuestion.author_name || auditQuestion.created_by_username || getAuthorName(auditQuestion) }}
                  </div>
                  <div class="d-flex align-center gap-1 flex-wrap mt-1">
                    <v-chip
                      size="x-small"
                      :color="isImportedFromExcel(auditQuestion) ? 'teal' : 'primary'"
                      :variant="isImportedFromExcel(auditQuestion) ? 'flat' : 'tonal'"
                      class="font-weight-bold px-2"
                      style="height: 20px;"
                    >
                      <v-icon start size="12">{{ isImportedFromExcel(auditQuestion) ? 'mdi-file-excel' : 'mdi-keyboard-outline' }}</v-icon>
                      {{ isImportedFromExcel(auditQuestion) ? 'طريقة الإنشاء: مستورد من ملف إكسل' : 'طريقة الإنشاء: إدخال يدوي' }}
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
                <v-avatar size="42" :color="auditQuestion.last_modified_by ? 'warning' : 'primary'" variant="tonal" class="flex-shrink-0">
                  <v-icon size="22" :color="auditQuestion.last_modified_by ? 'warning' : 'primary'">mdi-pencil-clock-outline</v-icon>
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
                <v-avatar size="42" :color="auditQuestion.reviewer_name ? 'success' : 'primary'" variant="tonal" class="flex-shrink-0">
                  <v-icon size="22" :color="auditQuestion.reviewer_name ? 'success' : 'primary'">mdi-account-check-outline</v-icon>
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

    <!-- Reject Dialog -->
    <CustomDialog v-model="rejectDialog" width="500" title="رفض السؤال">
      <div class="d-flex align-center gap-3 mb-4">
        <v-avatar color="error" variant="tonal" size="48" rounded="xl">
          <v-icon size="26">mdi-close-circle</v-icon>
        </v-avatar>
        <div>
          <span class="text-caption text-medium-emphasis">يرجى توضيح سبب عدم الاعتماد للمؤلف</span>
        </div>
      </div>

      <custom-text-note v-model="rejectReason" placeholder="اكتب سبب الرفض بالتفصيل هنا..." rows="4"
        :rules="[rules.requiredWithMessage('يرجى كتابة سبب الرفض')]" variant="outlined" density="comfortable"
        rounded="xl" auto-grow hide-details="auto" class="mb-4" />

      <div class="text-caption font-weight-bold text-medium-emphasis mb-2">ردود سريعة:</div>
      <v-chip-group v-model="selectedRejectReason" class="flex-wrap mb-6">
        <v-chip v-for="reason in quickRejectReasons" :key="reason" filter variant="tonal" color="primary"
          @click="rejectReason = reason">
          {{ reason }}
        </v-chip>
      </v-chip-group>

      <template #actions>
        <custom-btn label="إلغاء" variant="text" class="font-weight-bold" :click="() => rejectDialog = false" />
        <custom-btn type="del" label="تأكيد رفض السؤال" color="error" class="font-weight-bold px-6"
          :disabled="!rejectReason" :click="rejectQuestion" />
      </template>
    </CustomDialog>

    <!-- Review Checklist Dialog -->
    <CustomDialog v-model="checklistDialog" width="620" title="قائمة تدقيق معايير المراجعة والاعتماد">
      <div class="mb-4">
        <v-alert type="info" variant="tonal" class="rounded-xl mb-4">
          يرجى التحقق من معايير الجودة السبعة قبل اعتماد السؤال رسميًا لبنك الأسئلة:
        </v-alert>

        <v-checkbox v-model="checklist.linguistic_check" label="1. السلامة اللغوية والإملائية وخلو السؤال من الأخطاء النحوية" hide-details density="compact" color="success" class="mb-2" />
        <v-checkbox v-model="checklist.scientific_check" label="2. السلامة العلمية وصحة المفاهيم المطروحة" hide-details density="compact" color="success" class="mb-2" />
        <v-checkbox v-model="checklist.image_check" label="3. وضوح وجودة الصور والرسومات المرفقة (إن وجدت)" hide-details density="compact" color="success" class="mb-2" />
        <v-checkbox v-model="checklist.answer_check" label="4. دقة وصحة الإجابة المحددة وخلو البدائل من التمويه الخاطئ" hide-details density="compact" color="success" class="mb-2" />
        <v-checkbox v-model="checklist.curriculum_check" label="5. توافق محتوى السؤال مع الدرس والوحدة المحددة" hide-details density="compact" color="success" class="mb-2" />
        <v-checkbox v-model="checklist.bloom_check" label="6. صحة تصنيف مستوى بلوم المعرفي ودرجة الصعوبة" hide-details density="compact" color="success" class="mb-3" />

        <v-textarea v-model="checklist.notes" label="ملاحظات المراجع (اختياري)" variant="outlined" density="compact" rows="2" hide-details class="mt-3" />
      </div>

      <template #actions>
        <custom-btn label="إلغاء" variant="text" :click="() => checklistDialog = false" />
        <custom-btn label="تأكيد الاعتماد النهائي" color="success" class="font-weight-bold px-6" :loading="approvingWithChecklist" :click="confirmApprovalWithChecklist" />
      </template>
    </CustomDialog>

    <!-- Question Diff Dialog -->
    <QuestionDiffDialog
      v-model="diffDialog"
      :v1-id="diffV1Id"
      :v2-id="diffV2Id"
    />

    <!-- Success Snackbar -->
    <CustomSnackBar v-model="snackbar" :color="snackbarColor" :text="snackbarText" />
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted, getCurrentInstance } from 'vue'
import { rules } from '@/utils/validations'
import { bankService } from '@/services/bankService'
import { academicService } from '@/services/academicService'
import { usersService } from '@/services/usersService'
import QuestionDiffDialog from './QuestionDiffDialog.vue'

const { proxy } = getCurrentInstance()

// State
const filterInstitutionType = ref(null)
const institutionTypeOptions = [
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]
const filterCollege = ref(null)
const filterDepartment = ref(null)
const filterSpecialization = ref(null)
const filterSemesterSubject = ref(null)

const filterInstituteField = ref(null)
const filterInstituteEducationSystem = ref(null)
const filterInstituteSpecialization = ref(null)
const filterInstituteCurriculum = ref(null)
const filterInstituteSubject = ref(null)

const filterInstituteSpecParam = computed(() => {
  const p = {}
  if (filterInstituteField.value) p.field = filterInstituteField.value
  if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
  return Object.keys(p).length ? p : null
})

const filterUnitParam = computed(() => {
  if (filterInstitutionType.value === 'university') {
    return filterSemesterSubject.value ? { semester_subject: filterSemesterSubject.value } : null
  }
  if (filterInstitutionType.value === 'institute') {
    return filterInstituteSubject.value ? { institute_subject: filterInstituteSubject.value } : null
  }
  return filterSubject.value || null
})

const filterSubject = ref(null)
const filterUnit = ref(null)
const filterStage = ref(null)
const filterClassTrack = ref(null)
const filterStatus = ref(null)

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterClassTrack.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteCurriculum.value = null
  filterInstituteSubject.value = null
  filterSubject.value = null
  filterUnit.value = null
  getData()
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterUnit.value = null
}

const getQuestionAnswers = (questionId) => {
  if (!selectedQuestion.value) return []
  return selectedQuestion.value.options || selectedQuestion.value.answers || []
}

const auditDialog = ref(false)
const auditLoading = ref(false)
const auditQuestion = ref(null)

const openAuditDialog = async (question) => {
  if (!question) return
  auditQuestion.value = { ...question }
  auditDialog.value = true
  auditLoading.value = true
  try {
    const res = await proxy.$axios.get(`api/bank/question-review/${question.id}/`)
    const fullData = res.data?.data || res.data
    if (fullData) {
      auditQuestion.value = { ...auditQuestion.value, ...fullData }
    }
  } catch (err) {
    console.error("فشل في جلب سجل التدقيق:", err)
  } finally {
    auditLoading.value = false
  }
}

const getActionBadgeColor = (action) => {
  if (!action) return "primary"
  const act = String(action).trim()
  if (act === "استيراد جماعي") return "teal"
  if (act === "إنشاء") return "primary"
  if (act === "تعديل") return "warning"
  if (act === "اعتماد" || act === "استعادة") return "success"
  if (act === "رفض" || act === "حذف") return "error"
  if (act === "استنساخ") return "indigo"
  if (act === "إصدار جديد") return "teal"
  if (act === "أرشفة") return "purple"
  return "info"
}

const getActionIcon = (action) => {
  if (!action) return "mdi-checkbox-blank-circle-outline"
  const act = String(action).trim()
  if (act === "إنشاء") return "mdi-plus-circle"
  if (act === "تعديل") return "mdi-pencil"
  if (act === "اعتماد") return "mdi-check-decagram"
  if (act === "رفض") return "mdi-close-octagon"
  if (act === "استنساخ") return "mdi-content-copy"
  if (act === "إصدار جديد") return "mdi-source-branch"
  if (act === "أرشفة") return "mdi-archive-arrow-down"
  if (act === "استعادة") return "mdi-archive-arrow-up"
  if (act === "استيراد جماعي") return "mdi-file-excel-outline"
  return "mdi-clock-outline"
}

const viewDialog = ref(false)
const rejectDialog = ref(false)
const checklistDialog = ref(false)
const approvingWithChecklist = ref(false)
const questionToApprove = ref(null)

const diffDialog = ref(false)
const diffV1Id = ref(null)
const diffV2Id = ref(null)

const checklist = ref({
  linguistic_check: true,
  scientific_check: true,
  image_check: true,
  answer_check: true,
  curriculum_check: true,
  bloom_check: true,
  notes: '',
})

const selectedQuestion = ref(null)
const questionToReject = ref(null)
const rejectReason = ref('')
const selectedRejectReason = ref()

// Local Data
const subjects = ref([])
const users = ref([])
const tableItems = ref({ results: [], pagination: {}, count: 0 })

const statusOptions = [
  { text: 'الكل', value: null },
  { text: 'بانتظار المراجعة', value: 'قيد المراجعة' },
  { text: 'معتمد', value: 'معتمد' },
  { text: 'مرفوض', value: 'مرفوض' },
  { text: 'مسودة', value: 'مسودة' },
]

const quickRejectReasons = [
  'صياغة غير واضحة',
  'الإجابة الصحيحة غير دقيقة',
  'لا يتناسب مع المستوى المحدد',
  'يحتاج إضافة صورة توضيحية',
]

const headers = computed(() => [
  { title: 'السؤال', key: 'content', sortable: false },
  { title: 'المادة / المقرر', key: 'subject', sortable: false },
  { title: 'نوع السؤال', key: 'questionType', sortable: false },
  { title: 'الصعوبة', key: 'difficulty', sortable: false },
  { title: 'الحالة', key: 'status', sortable: true },
  { title: 'المؤلف وآخر تعديل', key: 'audit', sortable: false },
])

onMounted(async () => {
  try {
    const [subjectsRes, usersRes] = await Promise.all([
      academicService.getSubjects(),
      usersService.getAll()
    ])
    subjects.value = (Array.isArray(subjectsRes) ? subjectsRes : subjectsRes?.data) || []
    users.value = (Array.isArray(usersRes) ? usersRes : usersRes?.data) || []
  } catch (error) {
    console.error("Failed to load base data", error)
  }
})

const getData = async (params = proxy.$params) => {
  try {
    let queryParams = {}
    if (params && params.params) {
      queryParams = { ...params.params, hasPagination: true }
    } else {
      queryParams = { page: 1, perPage: 10, hasPagination: true }
    }

    let filters = []
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      filters.push({ field: "institution_type", value: filterInstitutionType.value })
    }
    if (filterStatus.value) filters.push({ field: "status", value: filterStatus.value })

    // School filters
    const stageId = filterStage.value?.id || filterStage.value
    if (stageId) filters.push({ field: "lesson__unit__class_subject__class_track__level__stage", value: stageId })

    const classTrackId = filterClassTrack.value?.id || filterClassTrack.value
    if (classTrackId) filters.push({ field: "lesson__unit__class_subject__class_track", value: classTrackId })

    // University filters
    const semSubjectId = filterSemesterSubject.value?.id || filterSemesterSubject.value
    const specId = filterSpecialization.value?.id || filterSpecialization.value
    const deptId = filterDepartment.value?.id || filterDepartment.value
    const collegeId = filterCollege.value?.id || filterCollege.value

    if (semSubjectId) {
      filters.push({ field: "lesson__unit__semester_subject", value: semSubjectId })
    } else if (specId) {
      filters.push({ field: "lesson__unit__semester_subject__fk_specialization", value: specId })
    } else if (deptId) {
      filters.push({ field: "lesson__unit__semester_subject__fk_specialization__fk_section", value: deptId })
    } else if (collegeId) {
      filters.push({ field: "lesson__unit__semester_subject__fk_specialization__fk_college", value: collegeId })
    }

    // Institute filter
    if (filterInstitutionType.value === 'institute') {
      const instSubId = filterInstituteSubject.value?.id || filterInstituteSubject.value
      if (instSubId) {
        filters.push({ field: "lesson__subject", value: instSubId })
      }
    }

    // Common Subject Filter
    const subjectId = filterSubject.value?.id || filterSubject.value
    if (subjectId) {
      if (filterInstitutionType.value === 'university') {
        filters.push({ field: "lesson__unit__semester_subject__fk_subject", value: subjectId })
      } else if (filterInstitutionType.value === 'school') {
        filters.push({ field: "lesson__unit__class_subject__subject", value: subjectId })
      } else {
        queryParams.subject = subjectId
      }
    }

    // Unit Filter
    const unitId = filterUnit.value?.id || filterUnit.value
    if (unitId) {
      filters.push({ field: "lesson__unit", value: unitId })
    }

    let response
    if (filters.length > 0) {
      response = await proxy.$axios.post(
        "api/bank/question-review/filter-paginate/",
        { filters },
        { params: queryParams }
      )
    } else {
      response = await proxy.$axios.get("api/bank/question-review/", { params: queryParams })
    }

    tableItems.value = response?.data || response?.data?.data || { results: [], pagination: {} }
  } catch (err) {
    console.error("Failed to fetch review questions:", err)
  }
}

// Methods
const resetFilters = () => {
  filterInstitutionType.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteCurriculum.value = null
  filterInstituteSubject.value = null
  filterStage.value = null
  filterClassTrack.value = null
  filterSubject.value = null
  filterUnit.value = null
  filterStatus.value = null
  getData()
}

const isImportedFromExcel = (q) => {
  if (!q) return false
  return Boolean(
    q.is_imported ||
    q.import_session ||
    q.import_source === 'إكسل' ||
    q.status === 'مستورد' ||
    (q.audit_trail && q.audit_trail.some(a => a.action === 'استيراد جماعي'))
  )
}

const getAuthorName = (question) => {
  if (!question) return 'مؤلف غير معروف'
  if (typeof question === 'object') {
    if (question.author_name) return question.author_name
    if (question.created_by_username) return question.created_by_username
    const userId = question.createdBy
    if (!userId) return 'مؤلف غير معروف'
    const user = users.value.find(u => u.id === userId)
    return user ? (user.name || user.username || 'مؤلف غير معروف') : 'مؤلف غير معروف'
  }
  const user = users.value.find(u => u.id === question)
  return user ? (user.name || user.username || `مستخدم #${question}`) : `مستخدم #${question}`
}

const getSubjectName = (question) => {
  if (question?.subject_name) return question.subject_name
  if (!question?.fk_subject) return 'عام'
  const subject = subjects.value.find(s => s.id === question.fk_subject)
  return subject ? (subject.name_ar || subject.name) : 'عام'
}

const getUnitName = (question) => {
  if (question?.unit_name) return question.unit_name
  return question?.fk_unit ? `وحدة #${question.fk_unit}` : 'عام'
}

const getLessonName = (question) => {
  if (question?.lesson_name) return question.lesson_name
  return question?.lesson ? `درس #${question.lesson}` : 'عام'
}

const viewQuestion = async (question) => {
  if (!question) return
  selectedQuestion.value = { ...question }
  viewDialog.value = true
  if (!question.options || question.options.length === 0) {
    try {
      const res = await proxy.$axios.get(`api/bank/question-review/${question.id}/`)
      if (res?.data) {
        selectedQuestion.value = { ...selectedQuestion.value, ...res.data }
      }
    } catch (e) {
      console.warn("Could not fetch detailed question data, using cached item", e)
    }
  }
}

const openChecklistDialog = (question) => {
  questionToApprove.value = question
  checklist.value = {
    linguistic_check: true,
    scientific_check: true,
    image_check: true,
    answer_check: true,
    curriculum_check: true,
    bloom_check: true,
    notes: '',
  }
  checklistDialog.value = true
}

const confirmApprovalWithChecklist = async () => {
  if (!questionToApprove.value) return
  approvingWithChecklist.value = true
  try {
    await bankService.approveReviewQuestion(questionToApprove.value.id, {
      checklist: checklist.value
    })
    questionToApprove.value.status = 'معتمد'
    proxy.$alert("success", { message: "تم تدقيق واعتماد السؤال بنجاح", title: "عملية ناجحة" })
    checklistDialog.value = false
  } catch (error) {
    console.error("Failed to approve question with checklist", error)
    proxy.$alert("errorData", { message: "حدث خطأ أثناء اعتماد السؤال", title: "فشل الاعتماد" })
  } finally {
    approvingWithChecklist.value = false
  }
}

const openDiffDialog = (question) => {
  if (!question) return
  diffV1Id.value = question.parent_version || question.id
  diffV2Id.value = question.id
  diffDialog.value = true
}

const escalateToDeptHead = async (question) => {
  try {
    await bankService.escalateDeptHead(question.id)
    question.status = 'قيد مراجعة رئيس القسم'
    proxy.$alert("success", { message: "تمت إحالة السؤال لرئيس القسم بنجاح", title: "تمت الإحالة" })
  } catch (error) {
    console.error("Failed to escalate question", error)
    proxy.$alert("errorData", { message: "حدث خطأ أثناء إحالة السؤال", title: "فشل الإحالة" })
  }
}

const approveQuestion = async (question) => {
  openChecklistDialog(question)
}

const openRejectDialog = (question) => {
  questionToReject.value = question
  rejectReason.value = ''
  selectedRejectReason.value = undefined
  rejectDialog.value = true
}

const rejectQuestion = async () => {
  if (questionToReject.value) {
    try {
      await bankService.rejectReviewQuestion(questionToReject.value.id, {
        reason: rejectReason.value || selectedRejectReason.value
      })

      questionToReject.value.status = 'مرفوض'

      proxy.$alert("success", { message: "تم رفض السؤال بنجاح", title: "تم الرفض" })

    } catch (error) {
      console.error("Failed to reject question", error)
      proxy.$alert("errorData", { message: "حدث خطأ أثناء رفض السؤال", title: "فشل الرفض" })
    }
  }
  rejectDialog.value = false
}

// Helpers
const getDifficultyColor = (difficulty) => {
  const d = String(difficulty ?? '').toLowerCase().trim()
  if (d === '1' || d === 'easy' || d === 'سهل') return 'success'
  if (d === '2' || d === 'medium' || d === 'متوسط') return 'warning'
  if (d === '3' || d === 'hard' || d === 'صعب') return 'error'
  return 'primary'
}

const getDifficultyText = (difficulty) => {
  const d = String(difficulty ?? '').toLowerCase().trim()
  if (d === '1' || d === 'easy' || d === 'سهل') return 'سهل'
  if (d === '2' || d === 'medium' || d === 'متوسط') return 'متوسط'
  if (d === '3' || d === 'hard' || d === 'صعب') return 'صعب'
  return difficulty || '-'
}

const getDifficultyIcon = (difficulty) => {
  const d = String(difficulty ?? '').toLowerCase().trim()
  if (d === '1' || d === 'easy' || d === 'سهل') return 'mdi-signal-cellular-1'
  if (d === '2' || d === 'medium' || d === 'متوسط') return 'mdi-signal-cellular-2'
  if (d === '3' || d === 'hard' || d === 'صعب') return 'mdi-signal-cellular-3'
  return 'mdi-help-circle-outline'
}

const getStatusColor = (status) => {
  switch (status) {
    case 'معتمد': return 'success'
    case 'مرفوض': return 'error'
    case 'قيد المراجعة': return 'warning'
    case 'مسودة': return 'info'
    default: return 'primary'
  }
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'معتمد': return 'mdi-check-decagram'
    case 'مرفوض': return 'mdi-close-octagon'
    case 'قيد المراجعة': return 'mdi-clock-alert-outline'
    case 'مسودة': return 'mdi-file-document-edit-outline'
    default: return 'mdi-help-circle-outline'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'معتمد': return 'معتمد'
    case 'مرفوض': return 'مرفوض'
    case 'قيد المراجعة': return 'بانتظار المراجعة'
    case 'مسودة': return 'مسودة'
    default: return status || '-'
  }
}

const getBloomText = (level) => {
  const texts = {
    'تذكر': 'تذكر',
    'فهم': 'فهم',
    'تطبيق': 'تطبيق',
    'تحليل': 'تحليل',
    'تقييم': 'تقويم',
    'إبداع': 'إبداع',
    'ابتكار': 'إبداع',
  }
  return texts[level] || level || '-'
}

const getBloomColor = (level) => {
  const colors = {
    'تذكر': '#6366f1',
    'فهم': '#0284c7',
    'تطبيق': '#059669',
    'تحليل': '#d97706',
    'تقييم': '#7c3aed',
    'إبداع': '#db2777',
    'ابتكار': '#db2777',
  }
  return colors[level] || '#6366f1'
}

const getTypeText = (type) => {
  const types = {
    'Single Choice': 'اختيار واحد',
    'Multiple Choice': 'عدة إجابات',
    'True/False': 'صواب / خطأ',
    'Essay': 'مقالي',
    'Fill in the Blanks': 'فراغات',
    'Matching': 'مطابقة',
    'Ordering': 'ترتيب',
  }
  return types[type] || type || '-'
}

const getOptionLetter = (idx) => {
  const letters = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
  return letters[idx] || String(idx + 1)
}

const getInstitutionLabel = (type) => {
  const labels = {
    school: 'تعليم مدرسي',
    university: 'تعليم جامعي',
    institute: 'معاهد وتدريب مهني',
  }
  return labels[type] || 'تعليم مدرسي'
}

const getAcademicHierarchy = (q) => {
  if (!q) return []
  const parts = []
  if (q.institution_type === 'university') {
    if (q.college_name) parts.push({ label: 'الكلية', value: q.college_name, icon: 'mdi-town-hall' })
    if (q.department_name) parts.push({ label: 'القسم', value: q.department_name, icon: 'mdi-door' })
    if (q.specialization_name) parts.push({ label: 'التخصص', value: q.specialization_name, icon: 'mdi-certificate' })
    if (q.semester_subject_name) parts.push({ label: 'المقرر', value: q.semester_subject_name, icon: 'mdi-book-education' })
    else if (q.subject_name) parts.push({ label: 'المادة', value: q.subject_name, icon: 'mdi-book-education' })
  } else if (q.institution_type === 'institute') {
    if (q.institute_field_name) parts.push({ label: 'المجال', value: q.institute_field_name, icon: 'mdi-tools' })
    if (q.institute_specialization_name) parts.push({ label: 'التخصص', value: q.institute_specialization_name, icon: 'mdi-certificate' })
    if (q.subject_name) parts.push({ label: 'المادة', value: q.subject_name, icon: 'mdi-book-education' })
  } else {
    if (q.stage_name) parts.push({ label: 'المرحلة', value: q.stage_name, icon: 'mdi-stairs' })
    if (q.class_track_name) parts.push({ label: 'الصف والمسار', value: q.class_track_name, icon: 'mdi-google-classroom' })
    const sub = q.subject_name || getSubjectName(q)
    if (sub && sub !== 'عام') parts.push({ label: 'المادة', value: sub, icon: 'mdi-book-education' })
  }
  if (q.unit_name) parts.push({ label: 'الوحدة', value: q.unit_name, icon: 'mdi-folder-outline' })
  if (q.lesson_name) parts.push({ label: 'الدرس', value: q.lesson_name, icon: 'mdi-bookmark-outline' })
  return parts
}

const formatAuditDate = (dateStr) => {
  if (!dateStr) return '—'
  try {
    const d = new Date(dateStr)
    if (isNaN(d.getTime())) return dateStr
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const hours = String(d.getHours()).padStart(2, '0')
    const mins = String(d.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${mins}`
  } catch (e) {
    return dateStr
  }
}

</script>

<style scoped>
.qb-review-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Review Details Canvas & Modal Styling ===== */
.review-details-canvas {
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
  opacity: 0.8;
}

.model-answer-box {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.3) !important;
  border-right: 5px solid #10b981 !important;
}

.author-dossier-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
}

.audit-person-tile {
  background: rgba(var(--v-theme-on-surface), 0.02) !important;
  border: 1px solid rgba(var(--v-border-color), 0.1) !important;
}

.btn-glow-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
  color: #fff !important;
  box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.4) !important;
  transition: all 0.25s ease !important;
}

.btn-glow-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px 0 rgba(16, 185, 129, 0.55) !important;
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

</style>
