<template>
  <div>
    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="تصفية نتائج المراجعة" class="main-card border-0 pa-5 rounded-2xl">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- Status Filter -->
        <v-col cols="12" sm="6" md="2">
          <v-select v-model="filterStatus" :items="statusOptions" item-title="text" item-value="value" class="mb-6"
            placeholder="حالة السؤال" prepend-inner-icon="mdi-flag-outline" hide-details clearable density="compact"
            variant="outlined" />
        </v-col>

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school' || filterInstitutionType === 'all'">
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="filterClassTrack = null"
          />
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!filterStage"
          />
        </template>

        <!-- 🎓 University Filters -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filterCollege"
            name="College"
            placeholder="الكلية الجامعية"
            cols="2"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filterDepartment"
            name="DepartmentByCollege"
            :param="filterCollege"
            placeholder="القسم الأكاديمي"
            cols="2"
            :add="false"
            :disabled="!filterCollege"
            @update:model-value="filterSpecialization = null"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            cols="2"
            :add="false"
            :disabled="!filterDepartment"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
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
            placeholder="المجال المهني"
            cols="2"
            :add="false"
            @update:model-value="filterInstituteSpecialization = null"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            placeholder="نظام التعليم"
            cols="2"
            :add="false"
            @update:model-value="filterInstituteSpecialization = null"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="filterInstituteSpecParam"
            placeholder="التخصص المهني"
            cols="2"
            :add="false"
            :disabled="!filterInstituteField && !filterInstituteEducationSystem"
            @update:model-value="filterInstituteCurriculum = null"
          />
          <auto-list
            v-model="filterInstituteCurriculum"
            name="InstituteCurriculum"
            :param="filterInstituteSpecialization"
            placeholder="الخطة الدراسية"
            cols="2"
            :add="false"
            :disabled="!filterInstituteSpecialization"
            @update:model-value="filterInstituteSubject = null"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="filterInstituteCurriculum"
            placeholder="المادة التدريبية"
            cols="2"
            :add="false"
            :disabled="!filterInstituteCurriculum"
            @update:model-value="filterUnit = null"
          />
        </template>

        <!-- Common Subject Filter (يظهر للمدارس والنمط العام) -->
        <auto-list
          v-if="filterInstitutionType !== 'university' && filterInstitutionType !== 'institute'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="2"
          :add="false"
          @update:model-value="filterUnit = null"
        />

        <!-- Unit / Topic Filter (الوحدة للمدارس ومفردة المقرر للجامعات) -->
        <auto-list
          v-model="filterUnit"
          name="UnitBySubject"
          :param="filterInstitutionType === 'university' ? { semester_subject: filterSemesterSubject } : (filterInstitutionType === 'institute' ? { institute_subject: filterInstituteSubject } : filterSubject)"
          :placeholder="filterInstitutionType === 'university' ? 'مفردة / موضوع المقرر' : (filterInstitutionType === 'institute' ? 'الوحدة التدريبية' : 'الوحدة الدراسية')"
          cols="2"
          :add="false"
          :disabled="filterInstitutionType === 'university' ? !filterSemesterSubject : (filterInstitutionType === 'institute' ? !filterInstituteSubject : !filterSubject)"
        />

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

          <!-- Author -->
          <div v-if="key === 'author'" class="d-flex align-center gap-3">
            <div>
              <div class="font-weight-bold text-subtitle-2 text-primary">{{ getAuthorName(item) }}</div>
            </div>
          </div>

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

    <!-- View Question Dialog -->
    <CustomDialog v-model="viewDialog" width="720" title="مراجعة السؤال والتفاصيل">
      <template v-if="selectedQuestion">
        <!-- Author Info Box -->
        <div class="d-flex align-center gap-3 pa-4 rounded-xl mb-6 question-content-box">
          <v-avatar color="primary" size="48" class="font-weight-black text-white">
            {{ getAuthorName(selectedQuestion.createdBy).charAt(0) }}
          </v-avatar>
          <div>
            <div class="text-subtitle-1 font-weight-bold">{{ getAuthorName(selectedQuestion.createdBy) }}</div>
            <div class="text-caption text-medium-emphasis d-flex align-center gap-1">
              <v-icon size="14">mdi-clock-outline</v-icon>
              تاريخ التقديم: {{ selectedQuestion.createdAt }}
            </div>
          </div>
        </div>

        <!-- Question Content -->
        <div class="question-content-box pa-5 rounded-2xl mb-6">
          <h4 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center color-primary gap-1">
            <v-icon size="20">mdi-help-box-multiple-outline</v-icon>
            نص السؤال
          </h4>
          <div class="text-body-1 font-weight-medium" style="line-height: 1.8" v-html="selectedQuestion.content"></div>
          <v-img v-if="selectedQuestion.image" :src="selectedQuestion.image" max-height="300" class="mt-4 rounded-lg"
            contain />
        </div>

        <!-- Rejection Reason if Rejected -->
        <v-alert v-if="selectedQuestion.status === 'مرفوض'" type="error" variant="tonal" class="mb-6 rounded-xl">
          <div class="font-weight-bold mb-1">سبب الرفض المدوّن:</div>
          <div>{{ selectedQuestion.rejectionReason || 'لم يتم تحديد سبب' }}</div>
        </v-alert>

        <!-- Answers -->
        <div v-if="getQuestionAnswers(selectedQuestion.id).length > 0">
          <h4 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-1">
            <v-icon size="20" color="secondary">mdi-format-list-bulleted-type</v-icon>
            الإجابات المرتبطة
          </h4>
          <div v-for="(answer, index) in getQuestionAnswers(selectedQuestion.id)" :key="answer.id"
            class="pa-4 rounded-xl mb-2 d-flex align-center gap-3 border"
            :style="answer.isTrue ? 'background: rgba(22, 163, 74, 0.08); border-color: rgba(22, 163, 74, 0.4);' : 'background: rgba(0, 0, 0, 0.02); border-color: rgba(0, 0, 0, 0.08);'">
            <v-avatar size="32" :color="answer.isTrue ? 'success' : 'surface-variant'">
              <span class="font-weight-bold text-white">{{ String.fromCharCode(65 + index) }}</span>
            </v-avatar>
            <span class="text-body-1 flex-grow-1" :class="{ 'font-weight-bold text-success': answer.isTrue }">{{
              answer.text }}</span>
            <v-icon v-if="answer.isTrue" color="success" size="24">mdi-check-circle</v-icon>
          </div>
        </div>

        <!-- Metadata Summary Row -->
        <v-divider class="my-6 opacity-20" />
        <v-row class="ma-0 pa-3 rounded-xl question-content-box">
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">نوع المسار</div>
            <v-chip size="small" :color="selectedQuestion.institution_type === 'university' ? 'purple' : 'primary'" variant="tonal" class="font-weight-bold">
              {{ selectedQuestion.institution_type === 'university' ? '🎓 جامعي' : '🏫 مدرسي' }}
            </v-chip>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">المادة / المقرر</div>
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">{{
              getSubjectName(selectedQuestion) }}</v-chip>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">{{ selectedQuestion.institution_type === 'university' ? 'مفردة / موضوع المقرر' : 'الوحدة الدراسية' }}</div>
            <v-chip size="small" variant="outlined" class="font-weight-bold">{{ getUnitName(selectedQuestion) }}</v-chip>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">{{ selectedQuestion.institution_type === 'university' ? 'المحاضرة / الدرس الأكاديمي' : 'الدرس المدرسي' }}</div>
            <v-chip size="small" variant="outlined" class="font-weight-bold">{{ selectedQuestion.lesson_name || getLessonName(selectedQuestion) }}</v-chip>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">الصعوبة</div>
            <v-chip size="small" :color="getDifficultyColor(selectedQuestion.difficulty)" variant="tonal"
              class="font-weight-bold text-white">{{ getDifficultyText(selectedQuestion.difficulty) }}</v-chip>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">مستوى بلوم</div>
            <v-chip size="small" color="info" variant="tonal" class="font-weight-bold">{{
              getBloomText(selectedQuestion.bloomLevel) }}</v-chip>
          </v-col>
          <v-col cols="6" sm="3">
            <div class="text-caption text-medium-emphasis mb-1">الدرجة</div>
            <v-chip size="small" color="success" variant="tonal" class="font-weight-bold">
              ⭐ {{ selectedQuestion.defaultMark || 1 }} درجات
            </v-chip>
          </v-col>
          <v-col cols="6" sm="3" v-if="selectedQuestion.learningOutcome">
            <div class="text-caption text-medium-emphasis mb-1">{{ selectedQuestion.institution_type === 'university' ? 'مخرج تعلم المقرر (CLO)' : 'مخرج التعلم المستهدف' }}</div>
            <v-chip size="small" color="deep-purple" variant="tonal" class="font-weight-bold">
              {{ selectedQuestion.institution_type === 'university' ? 'CLO #' : 'مخرج #' }}{{ selectedQuestion.learningOutcome }}
            </v-chip>
          </v-col>
        </v-row>
      </template>

      <template #actions>
        <custom-btn label="إغلاق" variant="text" class="font-weight-bold" :click="() => viewDialog = false" />
        <div class="d-flex align-center gap-2 ms-auto">
          <template v-if="selectedQuestion && selectedQuestion.status === 'قيد المراجعة'">
            <custom-btn type="del" label="رفض السؤال" icon="mdi-close" color="error" variant="tonal"
              class="font-weight-bold" :click="() => { openRejectDialog(selectedQuestion); viewDialog = false; }" />
            <custom-btn type="add" label="اعتماد السؤال" icon="mdi-check-decagram" color="success"
              class="font-weight-bold" :click="() => { approveQuestion(selectedQuestion); viewDialog = false; }" />
          </template>
          <template v-else-if="selectedQuestion && selectedQuestion.status === 'مرفوض'">
            <custom-btn type="restore" label="إعادة اعتماد" icon="mdi-refresh" color="success" class="font-weight-bold"
              :click="() => { approveQuestion(selectedQuestion); viewDialog = false; }" />
          </template>
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
        <v-checkbox v-model="checklist.learning_outcome_check" label="6. قياس السؤال لمخرج التعلم المستهدف" hide-details density="compact" color="success" class="mb-2" />
        <v-checkbox v-model="checklist.bloom_check" label="7. صحة تصنيف مستوى بلوم المعرفي ودرجة الصعوبة" hide-details density="compact" color="success" class="mb-3" />

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
const filterInstitutionType = ref('all')
const institutionTypeOptions = [
  { text: 'الكل (مدارس، جامعات، معاهد)', value: 'all' },
  { text: '🏫 مدارس فقط', value: 'school' },
  { text: '🎓 جامعات فقط', value: 'university' },
  { text: '🏢 معاهد وتدريب مهني فقط', value: 'institute' },
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
  learning_outcome_check: true,
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
  { title: 'المؤلف', key: 'author', sortable: false },
  { title: 'السؤال', key: 'content', sortable: false },
  { title: 'المادة / المقرر', key: 'subject', sortable: false },
  { title: 'نوع السؤال', key: 'questionType', sortable: false },
  { title: 'الصعوبة', key: 'difficulty', sortable: false },
  { title: 'الحالة', key: 'status', sortable: true },
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
  filterInstitutionType.value = 'all'
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

const getAuthorName = (question) => {
  if (question?.author_name) return question.author_name
  const userId = typeof question === 'object' ? question?.createdBy : question
  if (!userId) return 'مؤلف غير معروف'
  const user = users.value.find(u => u.id === userId)
  return user ? (user.name || user.username || 'مؤلف غير معروف') : 'مؤلف غير معروف'
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

const viewQuestion = (question) => {
  if (!question) return
  selectedQuestion.value = question
  nextTick(() => {
    viewDialog.value = true
  })
}

const openChecklistDialog = (question) => {
  questionToApprove.value = question
  checklist.value = {
    linguistic_check: true,
    scientific_check: true,
    image_check: true,
    answer_check: true,
    curriculum_check: true,
    learning_outcome_check: true,
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
  const colors = { 1: 'emerald', 2: 'amber', 3: 'rose' }
  return colors[difficulty] || 'grey'
}

const getDifficultyText = (difficulty) => {
  const texts = { 1: 'سهل', 2: 'متوسط', 3: 'صعب' }
  return texts[difficulty] || difficulty
}

const getStatusColor = (status) => {
  switch (status) {
    case 'معتمد': return 'success';
    case 'مرفوض': return 'error';
    case 'قيد المراجعة': return 'warning';
    default: return 'grey';
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
  }
  return texts[level] || level
}

const getStatusText = (status) => {
  switch (status) {
    case 'معتمد': return 'معتمد';
    case 'مرفوض': return 'مرفوض';
    case 'قيد المراجعة': return 'بانتظار المراجعة';
    case 'مسودة': return 'مسودة';
    default: return status;
  }
}
</script>

<style scoped>
.qb-review-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

</style>
