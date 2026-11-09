<template>
  <div class="students-master-view">
    <!-- Add / Edit Student Drawer -->
    <add-students v-model="drawer" :data="data" :getData="getData" />

    <!-- ── Comprehensive Filters Bar ── -->
    <filter-fields label="خيارات التصفية الأكاديمية والهرمية لسجلات الطلاب" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
      <v-row dense class="align-center">
        <!-- 1. نوع المؤسسة التعليمية (مدارس / جامعات / معاهد / الكل) -->
        <v-col cols="12" md="12" class="mb-3">
          <v-btn-toggle
            v-model="filterInstitutionType"
            color="primary"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="w-100 d-flex flex-wrap institutional-toggle"
            @update:model-value="onInstitutionTypeChange"
          >
            <v-btn value="all" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="primary">mdi-asterisk</v-icon>
              كافة المؤسسات (الكل)
            </v-btn>
            <v-btn value="university" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="indigo">mdi-domain</v-icon>
              الجامعات والكليات
            </v-btn>
            <v-btn value="school" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="teal">mdi-school</v-icon>
              مدارس التعليم العام
            </v-btn>
            <v-btn value="institute" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="amber-darken-3">mdi-tools</v-icon>
              المعاهد ومراكز التدريب
            </v-btn>
          </v-btn-toggle>
        </v-col>

        <!-- 2. المحافظة والمديرية والمؤسسة التعليمية -->
        <v-col cols="12" sm="6" :md="isSchoolFilter ? 4 : 6">
          <auto-list
            v-model="filterGovernorate"
            name="Governorate"
            placeholder="المحافظة"
            label="المحافظة"
            cols="12"
            :add="false"
            @update:model-value="onGovernorateChange"
          />
        </v-col>

        <!-- المديرية: تظهر فقط للمدارس -->
        <v-col v-if="isSchoolFilter" cols="12" sm="6" md="4">
          <auto-list
            v-model="filterDirectorate"
            name="Directorate"
            :param="filterGovernorate"
            :placeholder="filterGovernorate ? 'اختر المديرية التابعة' : 'اختر المحافظة أولاً'"
            label="المديرية"
            cols="12"
            :add="false"
            :disabled="!filterGovernorate"
            @update:model-value="onDirectorateChange"
          />
        </v-col>

        <v-col cols="12" sm="6" :md="isSchoolFilter ? 4 : 6">
          <auto-list
            v-model="filterOrganization"
            name="Organization"
            :param="orgParam"
            :placeholder="orgPlaceholder"
            :label="orgFieldLabel"
            cols="12"
            :add="false"
            :disabled="isOrgDisabled"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- ── 4. التصنيف الأكاديمي التخصصي المشروط ── -->
        <!-- أ. فلاتر المدارس -->
        <template v-if="filterInstitutionType === 'school'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterStage"
              name="Stage"
              placeholder="المرحلة الدراسية"
              label="المرحلة الدراسية"
              cols="12"
              :add="false"
              @update:model-value="onStageChange"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterClassTrack"
              name="ClassTrackByStage"
              :param="filterStage"
              :placeholder="filterStage ? 'الصف والمسار' : 'اختر المرحلة أولاً'"
              label="الصف والمسار الدراسي"
              cols="12"
              :add="false"
              :disabled="!filterStage"
              @update:model-value="applyFilters"
            />
          </v-col>
        </template>

        <!-- ب. فلاتر الجامعات -->
        <template v-if="filterInstitutionType === 'university'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterCollege"
              name="College"
              placeholder="الكلية الجامعية"
              label="الكلية الجامعية"
              cols="12"
              :add="false"
              @update:model-value="onCollegeChange"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterDepartment"
              name="DepartmentByCollege"
              :param="filterCollege"
              :placeholder="filterCollege ? 'القسم الأكاديمي' : 'اختر الكلية أولاً'"
              label="القسم الأكاديمي"
              cols="12"
              :add="false"
              :disabled="!filterCollege"
              @update:model-value="onDepartmentChange"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterSpecialization"
              name="Specialization"
              :param="filterDepartment || filterCollege"
              :placeholder="filterCollege ? 'التخصص والبرنامج' : 'اختر الكلية أو القسم أولاً'"
              label="التخصص والبرنامج"
              cols="12"
              :add="false"
              :disabled="!filterCollege && !filterDepartment"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterEducationalLevel"
              name="EducationalLevels"
              placeholder="المستوى والدرجة الجامعية"
              label="المستوى والدرجة الجامعية"
              cols="12"
              :add="false"
              @update:model-value="applyFilters"
            />
          </v-col>
        </template>

        <!-- ج. فلاتر المعاهد -->
        <template v-if="filterInstitutionType === 'institute'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteField"
              name="InstituteField"
              placeholder="المجال المهني / التقني"
              label="المجال المهني / التقني"
              cols="12"
              :add="false"
              @update:model-value="onInstituteFieldChange"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteEducationSystem"
              name="InstituteEducationSystem"
              :param="filterInstituteField"
              placeholder="نظام التعليم والتدريب"
              label="نظام التعليم والتدريب"
              cols="12"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteSpecialization"
              name="InstituteSpecialization"
              :param="filterInstituteEducationSystem || filterInstituteField"
              :placeholder="filterInstituteField ? 'التخصص المهني' : 'اختر المجال أولاً'"
              label="التخصص المهني"
              cols="12"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteLevel"
              name="InstituteLevel"
              placeholder="المستوى التدريبي"
              label="المستوى التدريبي"
              cols="12"
              :add="false"
              @update:model-value="applyFilters"
            />
          </v-col>
        </template>

        <!-- 5. الجنس وحالة التفعيل وأزرار التحكم -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterGender"
            :items="genderOptions"
            item-title="text"
            item-value="value"
            placeholder="الجنس"
            label="الجنس"
            prepend-inner-icon="mdi-gender-male-female"
            clearable
            density="compact"
            variant="outlined"
            class="mb-3"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة التفعيل"
            label="الحالة"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-3"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- أزرار الإجراءات -->
        <v-col cols="12" sm="12" md="3" class="d-flex align-center justify-end gap-2 mb-3">
          <custom-btn
            type="show"
            label="تصفية النتائج"
            color="primary"
            icon="mdi-filter"
            class="font-weight-bold px-5"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ الفلاتر"
            icon="mdi-filter-off"
            class="font-weight-bold"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ── Data Table (الجدول الرئيسي - الحقول الأساسية والمهمة) ── -->
    <custom-data-table
      v-bind="{
        items,
        getData,
        headers,
        delItem: url,
        editItem,
        create: createStudent,
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- 1. معرف الطالب / الرقم الوطني -->
        <template v-if="key === 'student_id'">
          <span class="font-mono text-body-2" v-if="item.student_id">
            {{ item.student_id }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 2. الرقم الأكاديمي -->
        <template v-else-if="key === 'academic_number'">
          <span class="font-mono text-body-2" v-if="item.academic_number">
            {{ item.academic_number }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 3. اسم الطالب مع الصورة الرمزية وإمكانية النقر للعرض -->
        <template v-else-if="key === 'name_ar'">
          <div class="d-flex align-center gap-3 py-1 cursor-pointer" @click="openStudentDetailsModal(item)" title="انقر لعرض الملف الشامل للطالب">
            <v-avatar size="38" :color="item.gender === 2 ? 'pink' : 'primary'" variant="tonal" class="rounded-lg elevation-1 overflow-hidden flex-shrink-0">
              <v-img v-if="item.student_image" :src="getImageUrl(item.student_image)" cover />
              <v-icon v-else size="20">{{ item.gender === 2 ? 'mdi-account-heart-outline' : 'mdi-account-outline' }}</v-icon>
            </v-avatar>
            <div class="text-truncate" style="max-width: 200px;">
              <div class="font-weight-bold text-body-2 text-primary d-flex align-center gap-1 text-truncate">
                <span>{{ item.name_ar }}</span>
                <v-icon size="13" class="text-medium-emphasis">mdi-eye-outline</v-icon>
              </div>
              <div class="text-caption text-medium-emphasis font-mono text-truncate" v-if="item.name_en">{{ item.name_en }}</div>
            </div>
          </div>
        </template>

        <!-- 4. الجنس -->
        <template v-else-if="key === 'gender_display'">
          <v-chip
            size="small"
            :color="item.gender === 1 ? 'blue' : 'pink'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">{{ item.gender === 1 ? 'mdi-gender-male' : 'mdi-gender-female' }}</v-icon>
            {{ item.gender_display || (item.gender === 1 ? 'ذكر' : 'أنثى') }}
          </v-chip>
        </template>

        <!-- 5. الجنسية -->
        <template v-else-if="key === 'nationality_name'">
          <span class="text-body-2 font-weight-medium" v-if="item.nationality_name">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-flag-outline</v-icon>
            {{ item.nationality_name }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 6. تاريخ الميلاد -->
        <template v-else-if="key === 'birthdate'">
          <span class="text-body-2 font-mono font-weight-medium" v-if="item.birthdate">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-calendar-account-outline</v-icon>
            {{ item.birthdate }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 7. ولي الأمر -->
        <template v-else-if="key === 'parent_name'">
          <div v-if="item.parent_name" class="text-truncate" style="max-width: 190px;">
            <div class="text-body-2 text-truncate">
              {{ item.parent_name }}
            </div>
            <div class="text-caption text-medium-emphasis" v-if="item.parent_relation">
              ({{ item.parent_relation }})
            </div>
          </div>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 8. نوع المؤسسة -->
        <template v-else-if="key === 'institution_type'">
          <span class="text-body-2" v-if="item.institution_type === 'university'">
            جامعي
          </span>
          <span class="text-body-2" v-else-if="item.institution_type === 'institute'">
            معهد مهني
          </span>
          <span class="text-body-2" v-else>
            مدرسي
          </span>
        </template>

        <!-- 11. سنة التسجيل -->
        <template v-else-if="key === 'registration_year_name'">
          <span class="font-mono text-body-2" v-if="item.registration_year_name">
            {{ item.registration_year_name }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 12. المديرية والمحافظة -->
        <template v-else-if="key === 'directorate_name'">
          <div v-if="item.directorate_name || item.governorate_name">
            <div class="text-body-2 font-weight-medium">
              <v-icon size="14" class="me-1 text-medium-emphasis">mdi-map-marker-outline</v-icon>
              {{ item.directorate_name || item.governorate_name }}
            </div>
            <div class="text-caption text-medium-emphasis" v-if="item.directorate_name && item.governorate_name">
              {{ item.governorate_name }}
            </div>
          </div>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 13. الهاتف -->
        <template v-else-if="key === 'phone_number'">
          <span class="text-body-2 font-weight-medium font-mono" dir="ltr" v-if="item.phone_number">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-phone-outline</v-icon>
            {{ item.phone_number }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 14. الحالة -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            size="small"
            :color="item.is_active ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">{{ item.is_active ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
            {{ item.is_active ? 'مفعل' : 'معطل' }}
          </v-chip>
        </template>

        <!-- 15. العمليات والإجراءات (زر العين لإظهار الحقول المخفية + التعديل + الحذف) -->
        <template v-else-if="key === 'actions'">
          <div class="d-flex align-center justify-center gap-1">
            <!-- زر العين المميز - عرض الملف الشامل وكافة الحقول المخفية -->
            <v-btn
              icon
              size="small"
              variant="tonal"
              color="info"
              class="elevation-0"
              @click.stop="openStudentDetailsModal(item)"
            >
              <v-icon size="18">mdi-eye</v-icon>
              <v-tooltip activator="parent" location="top">عرض الملف الشامل والتفاصيل المخفية</v-tooltip>
            </v-btn>

            <!-- زر التعديل -->
            <v-btn
              icon
              size="small"
              variant="tonal"
              color="primary"
              class="elevation-0"
              @click.stop="editItem(item)"
            >
              <v-icon size="18">mdi-pencil-outline</v-icon>
              <v-tooltip activator="parent" location="top">تعديل بيانات الطالب</v-tooltip>
            </v-btn>

            <!-- زر الحذف -->
            <v-btn
              icon
              size="small"
              variant="tonal"
              color="error"
              class="elevation-0"
              @click.stop="confirmDeleteStudent(item)"
            >
              <v-icon size="18">mdi-delete-outline</v-icon>
              <v-tooltip activator="parent" location="top">حذف سجل الطالب</v-tooltip>
            </v-btn>
          </div>
        </template>
      </template>
    </custom-data-table>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- ── ديالوج الملف الشامل للطالب (زر العين - الحقول المخفية) ── -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <custom-dialog
      v-model="detailsDialog"
      width="1000"
      height="auto"
      title="الملف الشامل لبيانات الطالب"
      :subTitle="selectedStudent ? `${selectedStudent.name_ar} (رقم القيد: ${selectedStudent.academic_number || 'غير مسجل'})` : ''"
    >
      <div v-if="selectedStudent" class="pa-4">
        <!-- Profile Header Card (Zero-Gray Design) -->
        <v-card class="pa-5 mb-5 rounded-2xl border-subtle profile-header-card" elevation="0">
          <div class="d-flex flex-column flex-sm-row align-center gap-4">
            <v-avatar size="84" :color="selectedStudent.gender === 2 ? 'pink-lighten-4' : 'primary-lighten-4'" class="elevation-2 border overflow-hidden">
              <v-img
                v-if="selectedStudent.student_image"
                :src="getImageUrl(selectedStudent.student_image)"
                cover
              />
              <v-icon v-else size="44" :color="selectedStudent.gender === 2 ? 'pink' : 'primary'">
                {{ selectedStudent.gender === 2 ? 'mdi-account-heart-outline' : 'mdi-account-tie-outline' }}
              </v-icon>
            </v-avatar>

            <div class="flex-grow-1 text-center text-sm-start">
              <div class="d-flex flex-wrap align-center justify-center justify-sm-start gap-2 mb-1">
                <h2 class="text-h6 font-weight-black text-on-surface mb-0">{{ selectedStudent.name_ar }}</h2>
                <v-chip size="small" :color="selectedStudent.is_active ? 'success' : 'error'" variant="tonal" class="font-weight-bold">
                  <v-icon start size="14">{{ selectedStudent.is_active ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
                  {{ selectedStudent.is_active ? 'حساب مفعل' : 'حساب معطل' }}
                </v-chip>
                <v-chip size="small" :color="selectedStudent.gender === 2 ? 'pink' : 'primary'" variant="tonal" class="font-weight-bold">
                  <v-icon start size="14">{{ selectedStudent.gender === 2 ? 'mdi-gender-female' : 'mdi-gender-male' }}</v-icon>
                  {{ selectedStudent.gender_display || (selectedStudent.gender === 2 ? 'أنثى' : 'ذكر') }}
                </v-chip>
              </div>

              <div class="text-subtitle-2 text-medium-emphasis font-mono mb-2" v-if="selectedStudent.name_en">
                {{ selectedStudent.name_en }}
              </div>

              <div class="d-flex flex-wrap align-center justify-center justify-sm-start gap-2">
                <v-chip size="small" color="primary" variant="outlined" class="font-weight-bold font-mono">
                  <v-icon start size="14">mdi-card-account-details-outline</v-icon>
                  الرقم الأكاديمي: {{ selectedStudent.academic_number || '-' }}
                </v-chip>

                <v-chip size="small" color="indigo" variant="outlined" class="font-weight-bold font-mono" v-if="selectedStudent.student_id">
                  <v-icon start size="14">mdi-identifier</v-icon>
                  معرف الطالب / الرقم الوطني: {{ selectedStudent.student_id }}
                </v-chip>

                <v-chip size="small" :color="getInstitutionTypeColor(selectedStudent.institution_type)" variant="outlined" class="font-weight-bold">
                  <v-icon start size="14">{{ getInstitutionTypeIcon(selectedStudent.institution_type) }}</v-icon>
                  {{ getInstitutionTypeLabel(selectedStudent.institution_type) }}
                </v-chip>
              </div>
            </div>
          </div>
        </v-card>

        <!-- Tabs Navigation -->
        <v-tabs v-model="activeTab" color="primary" density="comfortable" class="mb-4 border-b">
          <v-tab value="personal" class="font-weight-bold">
            <v-icon start size="18">mdi-account-details</v-icon>
            البيانات الشخصية والهوية
          </v-tab>
          <v-tab value="guardian" class="font-weight-bold">
            <v-icon start size="18">mdi-account-child-circle</v-icon>
            ولي الأمر والتواصل
          </v-tab>
          <v-tab value="academic" class="font-weight-bold">
            <v-icon start size="18">mdi-school-outline</v-icon>
            المسار الأكاديمي والتسجيل
          </v-tab>
          <v-tab value="system" class="font-weight-bold">
            <v-icon start size="18">mdi-sync-circle</v-icon>
            بيانات المزامنة والحساب
          </v-tab>
        </v-tabs>

        <v-window v-model="activeTab">
          <!-- ── 1. البيانات الشخصية والهوية ── -->
          <v-window-item value="personal">
            <v-row dense>
              <!-- معرف الطالب / الرقم الوطني -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">معرف الطالب / الرقم الوطني (Student ID)</div>
                  <div class="text-body-1 font-weight-bold font-mono text-primary mt-1">
                    {{ selectedStudent.student_id || 'غير مسجل' }}
                  </div>
                </div>
              </v-col>

              <!-- الرقم الأكاديمي -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">الرقم الأكاديمي / رقم القيد</div>
                  <div class="text-body-1 font-weight-bold font-mono text-primary mt-1">
                    {{ selectedStudent.academic_number || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- الجنسية -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">الجنسية</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.nationality_name || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- الدولة ومحل الإقامة -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">الدولة ومحل الإقامة</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.country_name || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- تاريخ الميلاد -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">تاريخ الميلاد</div>
                  <div class="text-body-1 font-weight-bold font-mono mt-1">
                    {{ selectedStudent.birthdate || '-' }}
                    <span v-if="calculatedAge" class="text-caption text-medium-emphasis ms-1">({{ calculatedAge }})</span>
                  </div>
                </div>
              </v-col>

              <!-- مكان الميلاد -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">مكان الميلاد</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.birth_place || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- الديانة -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">الديانة</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.religion || 'غير محدد' }}
                  </div>
                </div>
              </v-col>

              <!-- الجنس -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">الجنس</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.gender_display || (selectedStudent.gender === 2 ? 'أنثى' : 'ذكر') }}
                  </div>
                </div>
              </v-col>

              <!-- العنوان التفصيلي -->
              <v-col cols="12" sm="12" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">العنوان السكني التفصيلي</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.address || '-' }}
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-window-item>

          <!-- ── 2. بيانات ولي الأمر والتواصل ── -->
          <v-window-item value="guardian">
            <v-row dense>
              <!-- اسم ولي الأمر -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">اسم ولي الأمر</div>
                  <div class="text-body-1 font-weight-bold text-primary mt-1">
                    {{ selectedStudent.parent_name || 'غير مسجل' }}
                  </div>
                </div>
              </v-col>

              <!-- صلة القرابة -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">صلة القرابة بولي الأمر</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.parent_relation || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- الهاتف المحمول -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">رقم هاتف الطالب / الجوال</div>
                  <div class="text-body-1 font-weight-bold font-mono mt-1 d-flex align-center gap-2" dir="ltr">
                    <v-icon size="16" color="teal">mdi-phone</v-icon>
                    <span>{{ selectedStudent.phone_number || '-' }}</span>
                    <v-btn
                      v-if="selectedStudent.phone_number"
                      icon="mdi-content-copy"
                      size="x-small"
                      variant="text"
                      @click="copyToClipboard(selectedStudent.phone_number)"
                      title="نسخ الرقم"
                    />
                  </div>
                </div>
              </v-col>

              <!-- هاتف المنزل -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">هاتف المنزل / الثابت</div>
                  <div class="text-body-1 font-weight-bold font-mono mt-1 d-flex align-center gap-2" dir="ltr">
                    <v-icon size="16" color="primary">mdi-deskphone</v-icon>
                    <span>{{ selectedStudent.home_number || '-' }}</span>
                    <v-btn
                      v-if="selectedStudent.home_number"
                      icon="mdi-content-copy"
                      size="x-small"
                      variant="text"
                      @click="copyToClipboard(selectedStudent.home_number)"
                      title="نسخ الرقم"
                    />
                  </div>
                </div>
              </v-col>

              <!-- المحافظة -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">المحافظة</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.governorate_name || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- المديرية -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">المديرية</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.directorate_name || '-' }}
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-window-item>

          <!-- ── 3. المسار الأكاديمي والتسجيل ── -->
          <v-window-item value="academic">
            <v-row dense>
              <!-- نوع المؤسسة -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">نوع المنظومة التعليمية</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ getInstitutionTypeLabel(selectedStudent.institution_type) }}
                  </div>
                </div>
              </v-col>

              <!-- المؤسسة التعليمية -->
              <v-col cols="12" sm="6" md="8">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">اسم المدرسة / المؤسسة التعليمية</div>
                  <div class="text-body-1 font-weight-bold text-primary mt-1">
                    {{ selectedStudent.organization_name || '-' }}
                  </div>
                </div>
              </v-col>

              <!-- التصنيف والقيد الأكاديمي -->
              <v-col cols="12" sm="12" md="12">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">القيد والتصنيف الأكاديمي التفصيلي</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.academic_info || '-' }}
                  </div>
                  <!-- تفاصيل تخصصية إضافية للجامعات والمعاهد -->
                  <div class="d-flex flex-wrap gap-2 mt-2" v-if="selectedStudent.institution_type === 'university'">
                    <v-chip size="small" variant="tonal" color="indigo" v-if="selectedStudent.university_college_name">
                      الكلية: {{ selectedStudent.university_college_name }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="indigo" v-if="selectedStudent.university_department_name">
                      القسم: {{ selectedStudent.university_department_name }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="indigo" v-if="selectedStudent.university_specialization_name">
                      التخصص: {{ selectedStudent.university_specialization_name }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="indigo" v-if="selectedStudent.university_level_name">
                      المستوى: {{ selectedStudent.university_level_name }}
                    </v-chip>
                  </div>
                  <div class="d-flex flex-wrap gap-2 mt-2" v-if="selectedStudent.institution_type === 'institute'">
                    <v-chip size="small" variant="tonal" color="amber-darken-3" v-if="selectedStudent.institute_field_name">
                      المجال: {{ selectedStudent.institute_field_name }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="amber-darken-3" v-if="selectedStudent.institute_education_system_name">
                      النظام: {{ selectedStudent.institute_education_system_name }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="amber-darken-3" v-if="selectedStudent.institute_specialization_name">
                      التخصص: {{ selectedStudent.institute_specialization_name }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="amber-darken-3" v-if="selectedStudent.institute_level_name">
                      المستوى: {{ selectedStudent.institute_level_name }}
                    </v-chip>
                  </div>
                </div>
              </v-col>

              <!-- سنة التسجيل -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">سنة / تاريخ التسجيل الأكاديمي</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.registration_year_name || 'غير محدد' }}
                  </div>
                </div>
              </v-col>

              <!-- نموذج التسجيل -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">استمارة / نموذج التسجيل</div>
                  <div class="mt-1" v-if="selectedStudent.registration_form">
                    <v-btn
                      size="small"
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-file-document-outline"
                      :href="getImageUrl(selectedStudent.registration_form)"
                      target="_blank"
                    >
                      عرض وتنزيل الاستمارة
                    </v-btn>
                  </div>
                  <div v-else class="text-body-2 text-medium-emphasis mt-1">
                    لم يتم إرفاق نموذج تسجيل
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-window-item>

          <!-- ── 4. بيانات المزامنة والحساب ── -->
          <v-window-item value="system">
            <v-row dense>
              <!-- كلمة المرور الأولية غير المشفرة -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis d-flex align-center justify-space-between">
                    <span>كلمة المرور الأولية (المهيأة عبر المزامنة)</span>
                    <v-chip size="x-small" color="warning" variant="tonal">سرية</v-chip>
                  </div>
                  <div class="d-flex align-center gap-2 mt-1">
                    <span class="font-mono font-weight-bold text-body-1">
                      {{ showPlainPassword ? (selectedStudent.plain_password || 'غير محددة') : '••••••••' }}
                    </span>
                    <v-btn
                      icon
                      size="x-small"
                      variant="text"
                      @click="showPlainPassword = !showPlainPassword"
                      :title="showPlainPassword ? 'إخفاء' : 'إظهار'"
                    >
                      <v-icon size="18">{{ showPlainPassword ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon>
                    </v-btn>
                    <v-btn
                      v-if="selectedStudent.plain_password"
                      icon="mdi-content-copy"
                      size="x-small"
                      variant="text"
                      @click="copyToClipboard(selectedStudent.plain_password)"
                      title="نسخ كلمة المرور"
                    />
                  </div>
                </div>
              </v-col>

              <!-- نظام المصدر -->
              <v-col cols="12" sm="6" md="6">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">نظام المصدر / جهة المزامنة</div>
                  <div class="text-body-1 font-weight-bold mt-1">
                    {{ selectedStudent.source_system || 'نظام الكنترول المركزي' }}
                  </div>
                </div>
              </v-col>

              <!-- معرّف السجل بالمصدر -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">معرف السجل بنظام المصدر (Portal ID)</div>
                  <div class="text-body-1 font-weight-bold font-mono mt-1">
                    {{ selectedStudent.portal_id || 'غير متوفر' }}
                  </div>
                </div>
              </v-col>

              <!-- تاريخ آخر مزامنة -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">تاريخ آخر مزامنة</div>
                  <div class="text-body-1 font-weight-bold font-mono mt-1">
                    {{ selectedStudent.last_synced_at ? formatDate(selectedStudent.last_synced_at) : 'لم تتم مزامنة سابقة' }}
                  </div>
                </div>
              </v-col>

              <!-- تاريخ الإنشاء في النظام -->
              <v-col cols="12" sm="6" md="4">
                <div class="info-card pa-3 rounded-xl border">
                  <div class="text-caption text-medium-emphasis">تاريخ إنشاء السجل</div>
                  <div class="text-body-1 font-weight-bold font-mono mt-1">
                    {{ selectedStudent.created_at ? formatDate(selectedStudent.created_at) : '-' }}
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-window-item>
        </v-window>

        <!-- Dialog Actions Footer -->
        <div class="d-flex align-center justify-end gap-2 mt-6 pt-4 border-t">
          <v-btn
            variant="tonal"
            color="primary"
            prepend-icon="mdi-pencil-outline"
            class="font-weight-bold px-4"
            @click="editStudentFromDetails"
          >
            تعديل بيانات الطالب
          </v-btn>
          <v-btn
            variant="outlined"
            color="secondary"
            class="font-weight-bold px-4"
            @click="detailsDialog = false"
          >
            إغلاق
          </v-btn>
        </div>
      </div>
    </custom-dialog>

    <!-- ── ديالوج تأكيد الحذف ── -->
    <custom-dialog
      v-model="deleteConfirmDialog"
      width="460"
      height="auto"
      title="تأكيد حذف سجل الطالب"
    >
      <div class="pa-4 text-center">
        <v-avatar size="64" color="error-lighten-4" class="mb-3">
          <v-icon size="36" color="error">mdi-alert-outline</v-icon>
        </v-avatar>
        <div class="text-subtitle-1 font-weight-bold mb-2">هل أنت متأكد من رغبتك في حذف هذا الطالب؟</div>
        <div class="text-body-2 text-medium-emphasis mb-4" v-if="studentToDelete">
          {{ studentToDelete.name_ar }} (رقم القيد: {{ studentToDelete.academic_number || '-' }})
        </div>
        <div class="d-flex justify-center gap-2">
          <v-btn
            color="error"
            variant="flat"
            :loading="deletingLoading"
            class="font-weight-bold px-5"
            @click="executeDeleteStudent"
          >
            نعم، حذف
          </v-btn>
          <v-btn
            variant="tonal"
            color="secondary"
            @click="deleteConfirmDialog = false"
          >
            إلغاء
          </v-btn>
        </div>
      </div>
    </custom-dialog>
  </div>
</template>

<script>
import AddStudents from './AddStudents.vue';

export default {
  name: 'StudentsView',
  components: {
    AddStudents,
  },
  data() {
    return {
      data: {},
      items: { count: 0, results: [] },
      drawer: false,
      loading: false,
      url: "api/academic/students/",

      // ── الديالوج الشامل لعرض تفاصيل الطالب (زر العين) ──
      detailsDialog: false,
      selectedStudent: null,
      activeTab: 'personal',
      showPlainPassword: false,

      // ── تأكيد الحذف ──
      deleteConfirmDialog: false,
      studentToDelete: null,
      deletingLoading: false,

      // ── إحصائيات سريعة للبطاقات ──
      statsCounts: {
        university: 0,
        school: 0,
        institute: 0,
      },

      // ── فلاتر الهيكلية والمؤسسة ──
      filterInstitutionType: 'all',
      filterGovernorate: null,
      filterDirectorate: null,
      filterOrganization: null,
      filterGender: null,
      filterActive: null,

      // ── فلاتر المدارس ──
      filterStage: null,
      filterClassTrack: null,

      // ── فلاتر الجامعات ──
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterEducationalLevel: null,

      // ── فلاتر المعاهد ──
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteLevel: null,

      genderOptions: [
        { text: "الكل", value: null },
        { text: "ذكور فقط", value: 1 },
        { text: "إناث فقط", value: 2 },
      ],
      activeOptions: [
        { text: "الكل", value: null },
        { text: "مفعل فقط", value: true },
        { text: "معطل فقط", value: false },
      ],
    };
  },
  computed: {
    isSchoolFilter() {
      return !this.filterInstitutionType || this.filterInstitutionType === 'all' || this.filterInstitutionType === 'school';
    },
    isOrgDisabled() {
      if (this.isSchoolFilter) {
        return !this.filterGovernorate || !this.filterDirectorate;
      }
      return !this.filterGovernorate;
    },
    orgFieldLabel() {
      if (this.filterInstitutionType === 'university') return 'الكلية / الجامعة';
      if (this.filterInstitutionType === 'institute') return 'المعهد / المركز التدريبي';
      return 'المدرسة التعليمية';
    },
    orgPlaceholder() {
      if (this.filterInstitutionType === 'university') {
        return this.filterGovernorate ? 'اختر الكلية / الجامعة' : 'اختر المحافظة أولاً...';
      }
      if (this.filterInstitutionType === 'institute') {
        return this.filterGovernorate ? 'اختر المعهد / المركز التدريبي' : 'اختر المحافظة أولاً...';
      }
      if (!this.filterGovernorate) return 'اختر المحافظة أولاً...';
      if (!this.filterDirectorate) return 'اختر المديرية أولاً...';
      return 'اختر المدرسة';
    },
    orgParam() {
      return {
        institution_type: (this.filterInstitutionType && this.filterInstitutionType !== 'all') ? this.filterInstitutionType : 'school',
        governorate: this.filterGovernorate || undefined,
        directorate: this.filterDirectorate || undefined,
      };
    },
    headers() {
      return [
        { title: "معرف الطالب / الرقم الوطني", key: "student_id", sortable: true },
        { title: "الرقم الأكاديمي", key: "academic_number", sortable: true },
        { title: "اسم الطالب", key: "name_ar", sortable: true },
        { title: "نوع المؤسسة", key: "institution_type", align: "center" },
        { title: "الجنس", key: "gender_display", align: "center" },
        { title: "الجنسية", key: "nationality_name" },
        { title: "تاريخ الميلاد", key: "birthdate", align: "center" },
        { title: "ولي الأمر", key: "parent_name" },
        { title: "سنة التسجيل", key: "registration_year_name", align: "center" },
        { title: "المديرية والمحافظة", key: "directorate_name" },
        { title: "الهاتف", key: "phone_number", align: "center" },
        { title: "الحالة", key: "is_active", align: "center" },
      ];
    },
    calculatedAge() {
      if (!this.selectedStudent?.birthdate) return null;
      try {
        const birth = new Date(this.selectedStudent.birthdate);في
        const now = new Date();
        let years = now.getFullYear() - birth.getFullYear();
        const m = now.getMonth() - birth.getMonth();
        if (m < 0 || (m === 0 && now.getDate() < birth.getDate())) {
          years--;
        }
        return years > 0 ? `${years} سنة` : null;
      } catch (e) {
        return null;
      }
    },
  },
  created() {
    this.getData();
    this.fetchSummaryStats();
  },
  methods: {
    async fetchSummaryStats() {
      try {
        const res = await this.$axios.get(this.url, { params: { page_size: 100 } });
        const list = res.data?.results || [];
        this.statsCounts = {
          university: list.filter(s => s.institution_type === 'university').length,
          school: list.filter(s => s.institution_type === 'school').length,
          institute: list.filter(s => s.institution_type === 'institute').length,
        };
      } catch (err) {
        console.error('Error fetching students stats:', err);
      }
    },

    async getData(params = this.$params) {
      this.loading = true;
      const queryParams = {
        ...(params?.params || params || {}),
      };

      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') {
        queryParams.institution_type = this.filterInstitutionType;
      }
      if (this.filterGovernorate) queryParams.governorate = this.filterGovernorate;
      if (this.filterDirectorate) queryParams.directorate = this.filterDirectorate;
      if (this.filterOrganization) queryParams.organization = this.filterOrganization;
      if (this.filterGender) queryParams.gender = this.filterGender;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      // School params
      if (this.filterInstitutionType === 'school') {
        if (this.filterStage) queryParams.stage = this.filterStage;
        if (this.filterClassTrack) queryParams.class_track = this.filterClassTrack;
      }

      // University params
      if (this.filterInstitutionType === 'university') {
        if (this.filterCollege) queryParams.college = this.filterCollege;
        if (this.filterDepartment) queryParams.department = this.filterDepartment;
        if (this.filterSpecialization) queryParams.specialization = this.filterSpecialization;
        if (this.filterEducationalLevel) queryParams.educational_level = this.filterEducationalLevel;
      }

      // Institute params
      if (this.filterInstitutionType === 'institute') {
        if (this.filterInstituteField) queryParams.institute_field = this.filterInstituteField;
        if (this.filterInstituteEducationSystem) queryParams.institute_education_system = this.filterInstituteEducationSystem;
        if (this.filterInstituteSpecialization) queryParams.institute_specialization = this.filterInstituteSpecialization;
        if (this.filterInstituteLevel) queryParams.institute_level = this.filterInstituteLevel;
      }

      try {
        const response = await this.$axios.get(this.url, { params: queryParams });
        this.items = response.data;
      } catch (err) {
        this.items = { count: 0, results: [] };
      } finally {
        this.loading = false;
      }
    },

    onInstitutionTypeChange() {
      this.filterOrganization = null;
      this.filterDirectorate = null;
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterEducationalLevel = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteLevel = null;
      this.getData();
    },

    onGovernorateChange(val) {
      this.filterGovernorate = val;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.getData();
    },

    onDirectorateChange(val) {
      this.filterDirectorate = val;
      this.filterOrganization = null;
      this.getData();
    },

    onStageChange(val) {
      this.filterStage = val;
      this.filterClassTrack = null;
      this.getData();
    },

    onCollegeChange(val) {
      this.filterCollege = val;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.getData();
    },

    onDepartmentChange(val) {
      this.filterDepartment = val;
      this.filterSpecialization = null;
      this.getData();
    },

    onInstituteFieldChange(val) {
      this.filterInstituteField = val;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.getData();
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterInstitutionType = 'all';
      this.filterGovernorate = null;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.filterGender = null;
      this.filterActive = null;

      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterEducationalLevel = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteLevel = null;

      this.getData();
    },

    createStudent() {
      this.data = {};
      this.drawer = true;
    },

    editItem(itemData) {
      this.data = { ...itemData };
      this.drawer = true;
    },

    // ── فتح نافذة التفاصيل الشاملة (زر العين) ──
    openStudentDetailsModal(student) {
      this.selectedStudent = student;
      this.activeTab = 'personal';
      this.showPlainPassword = false;
      this.detailsDialog = true;
    },

    editStudentFromDetails() {
      if (this.selectedStudent) {
        const itemToEdit = { ...this.selectedStudent };
        this.detailsDialog = false;
        this.editItem(itemToEdit);
      }
    },

    // ── تأكيد وحذف الطالب ──
    confirmDeleteStudent(item) {
      this.studentToDelete = item;
      this.deleteConfirmDialog = true;
    },

    async executeDeleteStudent() {
      if (!this.studentToDelete) return;
      this.deletingLoading = true;
      try {
        await this.$axios.delete(`${this.url}${this.studentToDelete.id}/`);
        this.deleteConfirmDialog = false;
        this.studentToDelete = null;
        this.getData();
      } catch (err) {
        console.error('Error deleting student:', err);
      } finally {
        this.deletingLoading = false;
      }
    },

    // ── Helpers ──
    getImageUrl(path) {
      if (!path) return '';
      if (path.startsWith('http://') || path.startsWith('https://')) return path;
      const base = (this.$settings?.url || this.$base_url || 'http://localhost:8000').replace(/\/+$/, '');
      return `${base}/${path.replace(/^\/+/, '')}`;
    },

    getInstitutionTypeLabel(type) {
      if (type === 'university') return 'تعليم جامعي';
      if (type === 'institute') return 'معاهد وتدريب مهني';
      return 'تعليم مدرسي';
    },

    getInstitutionTypeColor(type) {
      if (type === 'university') return 'indigo';
      if (type === 'institute') return 'amber-darken-3';
      return 'teal';
    },

    getInstitutionTypeIcon(type) {
      if (type === 'university') return 'mdi-domain';
      if (type === 'institute') return 'mdi-tools';
      return 'mdi-school';
    },

    formatDate(val) {
      if (!val) return '-';
      try {
        const d = new Date(val);
        return d.toLocaleDateString('ar-EG', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
      } catch (e) {
        return val;
      }
    },

    copyToClipboard(text) {
      if (!text) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(String(text));
        if (this.$toast?.success) {
          this.$toast.success('تم النسخ إلى الحافظة');
        }
      }
    },
  },
};
</script>

<style scoped>
.students-master-view {
  animation: fadeIn 0.3s ease-in-out;
  padding: 16px;
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.profile-header-card {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.04) 0%, rgba(var(--v-theme-surface), 1) 100%) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.15) !important;
}

.info-card {
  background: rgba(var(--v-theme-surface), 0.7);
  border-color: rgba(var(--v-border-color), 0.15) !important;
  transition: all 0.2s ease-in-out;
  min-height: 72px;
}

.info-card:hover {
  background: rgba(var(--v-theme-surface), 1);
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.cursor-pointer {
  cursor: pointer;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>