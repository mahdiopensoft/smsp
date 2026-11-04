<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="1040px"
    scrollable
    persistent
  >
    <v-card class="rounded-2xl overflow-hidden print-order-modal bg-surface elevation-6">
      <!-- ── Top Accent Stripe (هوية المنظومة المعتمدة) ── -->
      <div class="modal-top-stripe" />

      <!-- ── 1. Modal Header (رأس النافذة الرسمي الموحد) ── -->
      <div class="px-5 py-4 d-flex align-center justify-space-between border-b bg-surface">
        <div class="d-flex align-center gap-3">
          <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
            <v-icon size="24" color="primary">mdi-printer-clock-outline</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-subtitle-1 font-weight-black text-high-emphasis mb-0">إنشاء طلب طباعة رسمي للاختبار</h3>
            <span class="text-caption text-medium-emphasis">
              إصدار أمر إرسال رسمي للمطبعة مع التوزيع التلقائي للنماذج وتوثيق احتياط الطوارئ
            </span>
          </div>
        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          density="comfortable"
          color="medium-emphasis"
          rounded="lg"
          :disabled="submitting"
          @click="$emit('update:modelValue', false)"
        />
      </div>

      <!-- ── 2. Modal Body ── -->
      <v-card-text class="pa-5 overflow-y-auto bg-surface" style="max-height: 84vh;">
        <!-- Loading State -->
        <div v-if="loadingDetails" class="text-center py-10">
          <v-progress-circular indeterminate color="primary" size="46" class="mb-3" />
          <div class="text-subtitle-2 font-weight-black text-high-emphasis">جاري استرجاع بيانات الاختبار وتوزيع الطلاب والمراكز من قاعدة البيانات...</div>
          <div class="text-caption text-medium-emphasis">يتم احتساب النماذج والكميات الأساسية تلقائياً بنسبة 100%</div>
        </div>

        <div v-else>
          <!-- ════════════════════════════════════════════════════════════ -->
          <!-- شاشة تأكيد النجاح والخطوات التالية بعد الاعتماد الرسمي        -->
          <!-- ════════════════════════════════════════════════════════════ -->
          <div v-if="submitSuccess" class="pa-4 pa-sm-8 text-center animate-fade-in">
            <v-avatar color="primary" variant="tonal" size="68" rounded="2xl" class="mb-3">
              <v-icon size="36" color="primary">mdi-printer-check</v-icon>
            </v-avatar>
            <h3 class="text-h6 font-weight-black text-high-emphasis mb-1">
              تم توثيق وإرسال طلب الطباعة بنجاح!
            </h3>
            <p class="text-body-2 text-medium-emphasis mb-5">
              تم تسجيل طلب الطباعة رسمياً وإرساله للجنة برقم:
              <strong class="text-primary font-mono font-weight-black">{{ orderNumber }}</strong>
              <br />
              <span class="text-caption text-primary font-weight-bold">الطلب الآن في تبويب [الطلبات] وهو بانتظار الاعتماد والجدولة الرسمية</span>
            </p>

            <!-- ملخص الأمر المعتمد الموجه للمطبعة بأيقونات موحدة وتنسيق أنيق -->
            <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-6 mx-auto elevation-1" style="max-width: 650px;">
              <!-- 1. رقم أمر الطباعة -->
              <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
                <div class="summary-item-header">
                  <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                    <v-icon size="18" color="primary">mdi-barcode</v-icon>
                  </v-avatar>
                  <span class="text-body-2 font-weight-medium text-medium-emphasis">رقم طلب الطباعة:</span>
                </div>
                <div class="center-count-badge px-3 py-1 font-mono font-weight-black text-primary text-subtitle-2">
                  {{ orderNumber }}
                </div>
              </div>

              <!-- 2. إجمالي المطبوعات المطلوبة -->
              <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
                <div class="summary-item-header">
                  <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                    <v-icon size="18" color="primary">mdi-printer-check</v-icon>
                  </v-avatar>
                  <span class="text-body-2 font-weight-medium text-medium-emphasis">إجمالي المطبوعات المطلوبة:</span>
                </div>
                <div class="center-count-badge px-3 py-1 font-mono font-weight-black text-subtitle-2 text-high-emphasis">
                  {{ grandTotalToPrint }} ورقة/كراسة
                </div>
              </div>

              <!-- 3. الجهة المنفذة للطباعة -->
              <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
                <div class="summary-item-header">
                  <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                    <v-icon size="18" color="primary">mdi-domain</v-icon>
                  </v-avatar>
                  <span class="text-body-2 font-weight-medium text-medium-emphasis">الجهة المنفذة للطباعة:</span>
                </div>
                <span class="font-weight-bold text-body-2 text-high-emphasis">{{ form.targetFacility }}</span>
              </div>

              <!-- 4. المراكز والطلاب المشمولون -->
              <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
                <div class="summary-item-header">
                  <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                    <v-icon size="18" color="primary">mdi-school-outline</v-icon>
                  </v-avatar>
                  <span class="text-body-2 font-weight-medium text-medium-emphasis">المراكز والطلاب المشمولون:</span>
                </div>
                <div class="d-flex align-center gap-2">
                  <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold">
                    {{ filteredSchoolsCount }} مراكز
                  </div>
                  <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold font-mono">
                    {{ filteredTotalStudents }} طالباً
                  </div>
                </div>
              </div>

              <!-- 5. حصة الاحتياط المعتمدة -->
              <div class="d-flex align-center justify-space-between flex-wrap gap-2">
                <div class="summary-item-header">
                  <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                    <v-icon size="18" color="primary">mdi-shield-check-outline</v-icon>
                  </v-avatar>
                  <span class="text-body-2 font-weight-medium text-medium-emphasis">حصة الاحتياط المعتمدة:</span>
                </div>
                <div :class="totalReserveSum > 0 ? 'unified-badge-warning' : 'center-count-badge'" class="px-3 py-1 text-caption font-weight-black font-mono">
                  {{ totalReserveSum > 0 ? `+${totalReserveSum} (موثقة بتفويض رسمي)` : 'بدون احتياط (0)' }}
                </div>
              </div>
            </div>

            <!-- أزرار الإجراءات الفورية والمباشرة -->
            <div class="d-flex align-center justify-center gap-3 flex-wrap">
              <v-btn
                color="primary"
                variant="flat"
                rounded="lg"
                size="large"
                class="font-weight-bold px-6 shadow-sm"
                prepend-icon="mdi-format-list-bulleted"
                @click="goToRegistry"
              >
                الانتقال لسجل الطلبات لمتابعة واعتماد الطلب
              </v-btn>

              <v-btn
                color="secondary"
                variant="tonal"
                rounded="lg"
                size="large"
                class="font-weight-bold px-5"
                prepend-icon="mdi-file-document-outline"
                @click="manifestDialog = true"
              >
                معاينة وطباعة استمارة طلب الطباعة (A4)
              </v-btn>

              <v-btn
                variant="outlined"
                rounded="lg"
                size="large"
                class="font-weight-bold px-4"
                @click="$emit('update:modelValue', false)"
              >
                إغلاق
              </v-btn>
            </div>
          </div>

          <v-form v-else ref="formRef" @submit.prevent="submitPrintOrder">
            <!-- تنبيه في حال كان الطلب مرتجعاً للتعديل -->
            <v-alert
              v-if="examReturnReason"
              type="warning"
              variant="tonal"
              rounded="xl"
              class="mb-4 font-weight-medium border"
              icon="mdi-keyboard-return"
            >
              <div class="text-subtitle-2 font-weight-black mb-1">
                تم إرجاع طلب طباعة هذا الاختبار للتعديل من قِبل لجنة الاعتماد
              </div>
              <div class="text-body-2">
                <strong>سبب الإرجاع:</strong> {{ examReturnReason }}
              </div>
              <div v-if="examReturnNotes" class="text-caption text-medium-emphasis mt-1">
                <strong>ملاحظات اللجنة:</strong> {{ examReturnNotes }}
              </div>
            </v-alert>

            <!-- ════════════════════════════════════════════════════════════ -->
            <!-- بطاقة تعريف الاختبار المستهدف (Exam Header Banner)         -->
            <!-- ════════════════════════════════════════════════════════════ -->
            <div class="main-card pa-3 px-4 rounded-xl mb-4 border d-flex align-center justify-space-between flex-wrap gap-3">
              <div class="d-flex align-center gap-3">
                <v-avatar color="primary" variant="tonal" size="38" rounded="lg">
                  <v-icon size="20" color="primary">mdi-file-document-check-outline</v-icon>
                </v-avatar>
                <div>
                  <div class="font-weight-black text-body-2 text-high-emphasis">
                    {{ examTitle }}
                  </div>
                  <div class="exam-badges-bar mt-2">
                    <div class="center-count-badge badge-spaced">
                      <v-icon size="14" color="primary">mdi-school</v-icon>
                      <span>{{ displayStageName }}</span>
                    </div>
                    <div class="center-count-badge unified-badge-warning badge-spaced">
                      <v-icon size="14" color="amber-darken-3">mdi-book-open-outline</v-icon>
                      <span>{{ displaySubjectName }}</span>
                    </div>
                    <div class="center-count-badge unified-badge-default badge-spaced font-mono">
                      <v-icon size="14">mdi-identifier</v-icon>
                      <span>{{ examCode }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-flex align-center gap-4">
                <div class="text-left text-sm-right">
                  <div class="text-caption text-medium-emphasis">الطلاب المشمولون</div>
                  <div class="font-mono font-weight-black text-subtitle-1 text-primary lh-1">
                    {{ filteredTotalStudents }} <span class="text-caption font-weight-regular text-medium-emphasis">طالباً</span>
                  </div>
                </div>
                <div class="text-left text-sm-right border-s ps-4">
                  <div class="text-caption text-medium-emphasis">المراكز الامتحانية</div>
                  <div class="font-mono font-weight-black text-subtitle-1 text-secondary lh-1">
                    {{ filteredSchoolsCount }} <span class="text-caption font-weight-regular text-medium-emphasis">مركزاً</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- ════════════════════════════════════════════════════════════ -->
            <!-- 1. الفلاتر الموحدة ونطاق المراكز المستهدفة (filter-fields)     -->
            <!-- مع أيقونات رسمية ونافذة منبثقة موحدة وأنيقة لاختيار المراكز   -->
            <!-- ════════════════════════════════════════════════════════════ -->
            <filter-fields
              label="خيارات التصفية ونطاق المراكز الامتحانية المستهدفة"
              prepend-icon="mdi-filter-variant"
              class="main-card pa-4 rounded-xl mb-4 border"
            >
              <v-row class="align-start filter-fields-row">
                <!-- المحافظة (AutoList مع أيقونة رسمية وزر إلغاء X مدمج) -->
                <auto-list
                  v-model="filterGovernorate"
                  :objects="governorateSelectObjects"
                  name="Governorate"
                  label="المحافظة"
                  placeholder="المحافظة"
                  cols="4"
                  :add="false"
                  :hideDetails="true"
                  @update:modelValue="onGovernorateChange"
                />

                <!-- المديرية (AutoList مع أيقونة رسمية وزر إلغاء X مدمج) -->
                <auto-list
                  v-model="filterDirectorate"
                  :objects="directorateSelectObjects"
                  name="DirectorateByGovernorate"
                  label="المديرية"
                  placeholder="المديرية"
                  cols="4"
                  :add="false"
                  :hideDetails="true"
                  @update:modelValue="onDirectorateChange"
                />

                <!-- المراكز الامتحانية المستهدفة (حقل موحد بأيقونة وزر إلغاء X وزر تحديد) -->
                <v-col cols="12" sm="12" md="4" class="py-2">
                  <v-text-field
                    :model-value="centersFieldSummary"
                    label="المراكز الامتحانية المشمولة *"
                    readonly
                    clearable
                    variant="outlined"
                    density="compact"
                    rounded="lg"
                    color="primary"
                    :hide-details="true"
                    class="cursor-pointer"
                    @click="centersDialog = true"
                    @click:clear.stop="resetAllSchools"
                  >
                    <template #prepend-inner>
                      <v-icon size="20">mdi-domain</v-icon>
                    </template>
                    <template #append-inner>
                      <v-btn
                        size="x-small"
                        variant="tonal"
                        color="primary"
                        class="font-weight-bold rounded-lg px-2"
                        @click.stop="centersDialog = true"
                      >
                        <v-icon start size="14">mdi-tune-variant</v-icon>
                        تحديد ({{ selectedSchoolNames.length }})
                      </v-btn>
                    </template>
                  </v-text-field>
                </v-col>
              </v-row>
            </filter-fields>

            <!-- ════════════════════════════════════════════════════════════ -->
            <!-- 2. المواعيد الزمنية والجهة المنفذة                            -->
            <!-- مرتبة ومتناسقة في خط أفقي واحد بأيقونات وارتفاعات موحدة       -->
            <!-- ════════════════════════════════════════════════════════════ -->
            <div class="main-card pa-4 rounded-xl mb-4 border">
              <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
                <div class="d-flex align-center gap-2 text-subtitle-2 font-weight-bold text-high-emphasis">
                  <v-avatar color="primary" variant="tonal" size="30" rounded="lg">
                    <v-icon size="18" color="primary">mdi-calendar-clock</v-icon>
                  </v-avatar>
                  <span>بيانات الجدولة الزمنية والمطبعة المنفذة</span>
                </div>
                <div class="text-caption text-medium-emphasis">
                  تحديد مواعيد الطباعة والامتحان والجهة المسؤولة عن التنفيذ
                </div>
              </div>

              <v-row class="align-start filter-fields-row">
                <!-- موعد الطباعة المجدول (CustomDate) -->
                <custom-date
                  v-model="form.printDate"
                  label="موعد الطباعة المجدول"
                  cols="4"
                  :isRequired="true"
                  :hideDetails="true"
                />

                <!-- موعد الامتحان الفعلي (CustomDate) -->
                <custom-date
                  v-model="form.examDate"
                  label="موعد الامتحان الفعلي"
                  cols="4"
                  :isRequired="true"
                  :hideDetails="true"
                />

                <!-- الجهة المنفذة للطباعة (AutoList مع أيقونة المطبعة الرسمية وزر إلغاء X) -->
                <auto-list
                  v-model="form.targetFacility"
                  :objects="facilitySelectObjects"
                  name="Organization"
                  label="الجهة المنفذة للطباعة (المطبعة) *"
                  placeholder="الجهة المنفذة للطباعة (المطبعة)"
                  cols="4"
                  icon="printer"
                  :add="false"
                  :hideDetails="true"
                />
              </v-row>
            </div>

            <!-- ════════════════════════════════════════════════════════════ -->
            <!-- 3. المواد المطلوب طباعتها وتضمينها                           -->
            <!-- ════════════════════════════════════════════════════════════ -->
            <div class="main-card pa-4 rounded-xl mb-4 border">
              <div class="d-flex align-center gap-2 mb-2 text-subtitle-2 font-weight-bold text-high-emphasis">
                <v-icon size="18" color="primary">mdi-checkbox-multiple-marked-outline</v-icon>
                <span>المواد المطلوب طباعتها وتضمينها في أمر الطباعة</span>
              </div>
              <v-row dense class="align-center mt-1">
                <custom-check-box
                  v-model="form.includeBooklets"
                  label="كراسات الأسئلة الرسمية"
                  cols="3"
                />
                <custom-check-box
                  v-model="form.includeBubbleSheets"
                  label="أوراق الإجابة والتظليل OMR"
                  cols="3"
                />
                <custom-check-box
                  v-model="form.includeRosters"
                  label="كشوف المناداة والجلوس"
                  cols="3"
                />
                <custom-check-box
                  v-model="form.includeAnswerKeys"
                  label="مفاتيح الحل ومظاريف الكنترول"
                  cols="3"
                />
              </v-row>
            </div>

            <!-- ════════════════════════════════════════════════════════════ -->
            <!-- 4. جدول التوزيع التلقائي للطلاب على النماذج                   -->
            <!-- المكون الموحد <custom-data-table> مع الترويسة والببجنشن كاملاً  -->
            <!-- ════════════════════════════════════════════════════════════ -->
            <div class="main-card pa-4 rounded-xl mb-4 border">
              <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
                <div class="d-flex align-center gap-2 text-subtitle-2 font-weight-black text-high-emphasis">
                  <v-avatar color="primary" variant="tonal" size="30" rounded="lg">
                    <v-icon size="18" color="primary">mdi-account-group-outline</v-icon>
                  </v-avatar>
                  <span>التوزيع التلقائي للطلاب والاحتياط على النماذج</span>
                </div>
                <div class="center-count-badge px-3 py-1 text-caption font-weight-black d-flex align-center gap-1.5">
                  <v-icon size="14" color="primary">mdi-check-decagram</v-icon>
                  <span>توزيع آلي متكافئ 100%</span>
                </div>
              </div>

              <!-- تنبيه إيضاحي رسمي لآلية الطباعة -->
              <v-alert
                type="info"
                variant="tonal"
                density="compact"
                rounded="lg"
                class="mb-3 text-caption font-weight-medium"
              >
                <strong>آلية الطباعة المعتمدة:</strong>
                الكمية الأساسية تُطبع <u>مخصصة</u> (Personalized) بأسماء الطلاب وأرقام جلوسهم والباركود، بينما كمية احتياط الطوارئ تُطبع <u>نماذج عامة بيضاء</u> (Generic / Blank) موزعة آلياً على النماذج لتدوين وتظليل رقم الجلوس يدوياً في القاعة.
              </v-alert>

              <!-- المكون الموحد الرسمي مع الترويسة والأدوات والببجنشن كاملاً -->
              <custom-data-table
                :headers="versionTableHeaders"
                :items="versionTableItems"
                :pagination="true"
                :showTop="true"
                :showSelect="false"
                :numbering="false"
                :actions="false"
                :search="true"
                class="rounded-xl overflow-hidden border mb-2 print-order-table"
              >
                <template v-slot:item-slot="{ item, key }">
                  <!-- رمز النموذج -->
                  <template v-if="key === 'version_code'">
                    <div class="d-flex align-center justify-center">
                      <v-chip
                        size="small"
                        :color="getModelColor(item.version_code)"
                        variant="tonal"
                        class="font-weight-black px-3 rounded-md min-w-cell"
                      >
                        <v-icon start size="14">mdi-file-document-outline</v-icon>
                        النموذج {{ item.version_code }}
                      </v-chip>
                    </div>
                  </template>

                  <!-- الطلاب المقيدون (أساسي) -->
                  <template v-else-if="key === 'student_count'">
                    <div class="d-flex align-center justify-center">
                      <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono min-w-cell">
                        {{ item.student_count }}
                      </div>
                    </div>
                  </template>

                  <!-- كراسات الأسئلة -->
                  <template v-else-if="key === 'booklets'">
                    <div class="d-flex align-center justify-center">
                      <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono min-w-cell">
                        {{ item.booklets }}
                      </div>
                    </div>
                  </template>

                  <!-- أوراق إجابة OMR -->
                  <template v-else-if="key === 'sheets'">
                    <div class="d-flex align-center justify-center">
                      <div class="center-count-badge unified-badge-teal px-3 py-1 text-caption font-weight-black font-mono min-w-cell">
                        {{ item.sheets }}
                      </div>
                    </div>
                  </template>

                  <!-- حصة احتياط الطوارئ (عام) -->
                  <template v-else-if="key === 'reserve_quota'">
                    <div class="d-flex align-center justify-center">
                      <div
                        :class="item.reserve_quota > 0 ? 'unified-badge-warning' : 'center-count-badge'"
                        class="px-3 py-1 text-caption font-weight-black font-mono min-w-cell"
                        dir="ltr"
                      >
                        +{{ item.reserve_quota }}
                      </div>
                    </div>
                  </template>

                  <!-- نسبة التمثيل -->
                  <template v-else-if="key === 'percentage'">
                    <div class="d-flex align-center justify-center">
                      <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono min-w-cell" dir="ltr">
                        {{ item.percentage }}
                      </div>
                    </div>
                  </template>

                  <template v-else>
                    <div class="d-flex align-center justify-center">
                      <span>{{ item[key] }}</span>
                    </div>
                  </template>
                </template>
              </custom-data-table>

              <!-- شريط ملخص إجمالي النماذج الموحد النظيف -->
              <div class="table-summary-strip d-flex align-center justify-space-between flex-wrap gap-3 px-4 py-3 rounded-lg border mt-2">
                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">الإجمالي الأساسي:</span>
                  <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
                    {{ filteredTotalStudents }} طالب
                  </div>
                </div>

                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">كراسات الأسئلة:</span>
                  <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
                    {{ form.includeBooklets ? filteredTotalStudents : 0 }}
                  </div>
                </div>

                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">أوراق إجابة OMR:</span>
                  <div class="center-count-badge unified-badge-teal px-3 py-1 text-caption font-weight-black font-mono">
                    {{ form.includeBubbleSheets ? filteredTotalStudents : 0 }}
                  </div>
                </div>

                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">إجمالي الاحتياط:</span>
                  <div :class="totalReserveQuota > 0 ? 'unified-badge-warning' : 'center-count-badge'" class="px-3 py-1 text-caption font-weight-black font-mono" dir="ltr">
                    +{{ totalReserveQuota }}
                  </div>
                </div>

                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">نسبة التغطية:</span>
                  <div class="center-count-badge unified-badge-success px-3 py-1 text-caption font-weight-black font-mono">
                    100%
                  </div>
                </div>
              </div>
            </div>

            <!-- ════════════════════════════════════════════════════════════ -->
            <!-- 5. جدول الكميات الأساسية والاحتياط للطوارئ                     -->
            <!-- المكون الموحد <custom-data-table> وحقول CustomTextField       -->
            <!-- ════════════════════════════════════════════════════════════ -->
            <div class="main-card pa-4 rounded-xl mb-4 border">
              <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
                <div class="d-flex align-center gap-2 text-subtitle-2 font-weight-bold text-high-emphasis">
                  <v-avatar color="primary" variant="tonal" size="30" rounded="lg">
                    <v-icon size="18" color="primary">mdi-calculator-variant-outline</v-icon>
                  </v-avatar>
                  <span>تحديد الكميات الأساسية والاحتياط للطوارئ (حسب المواد)</span>
                </div>
              </div>

              <!-- المكون الموحد الرسمي مع الترويسة والأدوات والببجنشن كاملاً -->
              <custom-data-table
                :headers="quantitiesTableHeaders"
                :items="quantitiesTableItems"
                :pagination="true"
                :showTop="true"
                :showSelect="false"
                :numbering="false"
                :actions="false"
                :search="true"
                class="rounded-xl overflow-hidden border mb-2 print-order-table"
              >
                <template v-slot:item-slot="{ item, key }">
                  <!-- المادة المطلوب طباعتها -->
                  <template v-if="key === 'material_name'">
                    <div class="material-cell-item py-1">
                      <v-avatar :color="item.color" variant="tonal" size="34" rounded="lg" class="material-avatar me-3">
                        <v-icon size="20" :color="item.color">{{ item.icon }}</v-icon>
                      </v-avatar>
                      <div class="text-right">
                        <div class="font-weight-bold text-high-emphasis text-body-2">{{ item.material_name }}</div>
                        <div class="text-caption text-medium-emphasis mt-0.5">{{ item.sub_desc }}</div>
                      </div>
                    </div>
                  </template>

                  <!-- الكمية الأساسية (مخصصة للطلاب) -->
                  <template v-else-if="key === 'base_qty'">
                    <div class="d-flex align-center justify-center">
                      <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono min-w-cell">
                        {{ item.base_qty }}
                      </div>
                    </div>
                  </template>

                  <!-- كمية الاحتياط للطوارئ (نماذج عامة) عبر حقل إدخال أنيق وموحد -->
                  <template v-else-if="key === 'reserve_qty'">
                    <div class="d-flex align-center justify-center">
                      <div class="reserve-input-box mx-auto" style="width: 90px;">
                        <v-text-field
                          v-if="item.id === 'booklets'"
                          v-model.number="quantities.bookletReserve"
                          type="number"
                          min="0"
                          density="compact"
                          variant="outlined"
                          rounded="md"
                          placeholder="0"
                          :hide-details="true"
                          :disabled="!form.includeBooklets"
                          class="reserve-table-input"
                          color="primary"
                        />
                        <v-text-field
                          v-else-if="item.id === 'sheets'"
                          v-model.number="quantities.sheetReserve"
                          type="number"
                          min="0"
                          density="compact"
                          variant="outlined"
                          rounded="md"
                          placeholder="0"
                          :hide-details="true"
                          :disabled="!form.includeBubbleSheets"
                          class="reserve-table-input"
                          color="primary"
                        />
                        <v-text-field
                          v-else-if="item.id === 'rosters'"
                          v-model.number="quantities.rosterReserve"
                          type="number"
                          min="0"
                          density="compact"
                          variant="outlined"
                          rounded="md"
                          placeholder="0"
                          :hide-details="true"
                          :disabled="!form.includeRosters"
                          class="reserve-table-input"
                          color="primary"
                        />
                      </div>
                    </div>
                  </template>

                  <!-- إجمالي الكمية المعتمدة للطباعة -->
                  <template v-else-if="key === 'total_qty'">
                    <div class="d-flex align-center justify-center">
                      <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono min-w-cell">
                        {{ item.total_qty }}
                      </div>
                    </div>
                  </template>

                  <template v-else>
                    <div class="d-flex align-center justify-center">
                      <span>{{ item[key] }}</span>
                    </div>
                  </template>
                </template>
              </custom-data-table>

              <!-- شريط ملخص إجمالي المطبوعات المعتمدة -->
              <div class="table-summary-strip d-flex align-center justify-space-between flex-wrap gap-3 px-4 py-3 rounded-lg border mb-3">
                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">الإجمالي الأساسي:</span>
                  <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
                    {{ formBaseTotal }}
                  </div>
                </div>

                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">إجمالي الاحتياط للطوارئ:</span>
                  <div :class="totalReserveSum > 0 ? 'unified-badge-warning' : 'center-count-badge'" class="px-3 py-1 text-caption font-weight-black font-mono" dir="ltr">
                    +{{ totalReserveSum }}
                  </div>
                </div>

                <div class="d-flex align-center gap-1.5 text-caption font-weight-bold">
                  <span class="text-medium-emphasis">إجمالي المطبوعات المعتمدة:</span>
                  <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
                    {{ grandTotalToPrint }} ورقة/كراسة
                  </div>
                </div>
              </div>

              <!-- ════════════════════════════════════════════════════════════ -->
              <!-- 6. الشرط الرقابي: توثيق وتبرير سبب الزيادة (متناسق تماماً)   -->
              <!-- حقول متطابقة الأفق والارتفاع والأيقونات مع حقل التحميل الرسمي -->
              <!-- ════════════════════════════════════════════════════════════ -->
              <v-expand-transition>
                <div
                  v-if="hasSurplusQuantity"
                  class="main-card pa-4 rounded-xl mb-4 border bg-surface"
                >
                  <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pb-2 border-b">
                    <div class="d-flex align-center gap-2">
                      <v-avatar color="primary" variant="tonal" size="32" rounded="lg">
                        <v-icon size="18" color="primary">mdi-shield-check-outline</v-icon>
                      </v-avatar>
                      <div>
                        <div class="font-weight-bold text-subtitle-2 text-high-emphasis">
                          توثيق وتبرير سبب الزيادة عن عدد الطلاب المقيدين
                        </div>
                        <div class="text-caption text-medium-emphasis">
                          إلزامي لاعتماد أمر الطباعة عند وجود كميات احتياط إضافية
                        </div>
                      </div>
                    </div>
                    <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                      <v-icon start size="14">mdi-lock-outline</v-icon>
                      إجراء رقابي معتمد
                    </v-chip>
                  </div>

                  <v-row class="align-start filter-fields-row">
                    <!-- 1. سبب الزيادة المعتمد (AutoList مع أيقونة رسمية وزر إلغاء X) -->
                    <auto-list
                      v-model="form.surplusReason"
                      :objects="surplusReasonObjects"
                      name="ScreenTypeChoices"
                      label="سبب اعتماد الكمية الإضافية / الاحتياط *"
                      placeholder="اختر سبب اعتماد الكمية الإضافية"
                      cols="6"
                      icon="shield-check-outline"
                      :add="false"
                      :hideDetails="true"
                    />

                    <!-- 2. رقم وتاريخ مذكرة الاعتماد (CustomTextField مع محاذاة أفقية متطابقة) -->
                    <custom-text-field
                      v-model="form.surplusAuthDoc"
                      label="رقم وتاريخ مذكرة / تفويض الاعتماد"
                      placeholder="مثال: قرار وزاري رقم 1446/12 بتاريخ 10/28"
                      icon="file-certificate-outline"
                      cols="6"
                      :isRequired="true"
                      :hideDetails="true"
                    />

                    <!-- 3. حقل التحميل الرسمي (CustomFile) لمرفق الوثيقة والمذكرة -->
                    <custom-file
                      v-model="form.surplusFile"
                      label="مرفق وثيقة / مذكرة تفويض الاعتماد الرسمية (PDF أو صورة) *"
                      cols="12"
                      accept=".pdf,image/*"
                      :required="true"
                      :hideDetails="true"
                    />

                    <!-- 4. تفاصيل وملاحظات التوجيه (CustomTextNote) -->
                    <custom-text-note
                      v-model="form.notes"
                      label="توجيهات وملاحظات لجنة المطبعة بشأن الكمية الإضافية"
                      placeholder="مثال: تسليم الاحتياط في مظروف مستقل مشمع لرئيس الكنترول بالمركز الامتحاني..."
                      icon="comment-text-outline"
                      cols="12"
                      :rows="2"
                      :hideDetails="true"
                    />
                  </v-row>
                </div>
              </v-expand-transition>
            </div>
          </v-form>
        </div>
      </v-card-text>

      <!-- ── 3. Modal Footer (متوافق مع الثيمين) ── -->
      <div v-if="!submitSuccess" class="pa-4 bg-surface border-t d-flex align-center justify-space-between flex-wrap gap-2">
        <div class="text-caption text-medium-emphasis d-flex align-center gap-2">
          <v-icon size="18" color="primary">mdi-printer-check</v-icon>
          <span>إجمالي المطبوعات المعتمدة:</span>
          <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
            {{ grandTotalToPrint }} ورقة/كراسة
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <custom-btn
            type="cancel"
            variant="outlined"
            label="إلغاء"
            :disabled="submitting"
            :click="() => $emit('update:modelValue', false)"
          />

          <custom-btn
            type="save"
            label="اعتماد وإنشاء طلب الطباعة"
            color="primary"
            :loading="submitting"
            :disabled="isSubmitDisabled"
            class="font-weight-bold px-4"
            :click="submitPrintOrder"
          />
        </div>
      </div>
    </v-card>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- 7. النافذة المنبثقة الموحدة والأنيقة لاختيار المراكز الامتحانية -->
    <!-- تطابق كامل للترويسة الرسمية وتنسيق البطاقات وشارات الطلاب     -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <v-dialog
      v-model="centersDialog"
      max-width="720px"
      scrollable
    >
      <v-card class="rounded-2xl overflow-hidden bg-surface elevation-12 border">
        <!-- شريط علوي ملون للهوية -->
        <div class="modal-top-stripe" />

        <!-- ترويسة أنيقة موحدة مطابقة تماماً لنافذة النظام الرسمية -->
        <div class="px-5 py-4 d-flex align-center justify-space-between border-b bg-surface">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
              <v-icon size="24" color="primary">mdi-domain</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h3 class="text-subtitle-1 font-weight-black text-high-emphasis mb-0">تحديد نطاق المراكز الامتحانية</h3>
                <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
                  {{ selectedSchoolNames.length }} من {{ availableSchools.length }} مراكز
                </div>
              </div>
            </div>
          </div>

          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            density="comfortable"
            color="medium-emphasis"
            rounded="lg"
            @click="centersDialog = false"
          />
        </div>

        <v-card-text class="pa-4 bg-surface" style="max-height: 65vh;">
          <!-- شريط البحث السريع والتحكم الجماعي -->
          <div class="d-flex align-center gap-2 mb-3">
            <v-text-field
              v-model="schoolFilterText"
              placeholder="بحث سريع باسم المركز الامتحاني أو المدرسة..."
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              rounded="lg"
              clearable
              hide-details
              class="flex-grow-1"
            />

            <v-btn
              variant="tonal"
              color="primary"
              size="small"
              class="font-weight-bold rounded-lg px-3"
              style="height: 40px"
              @click="toggleSelectAllSchools"
            >
              <v-icon start size="16">
                {{ isAllSchoolsSelected ? 'mdi-checkbox-blank-outline' : 'mdi-checkbox-multiple-marked' }}
              </v-icon>
              {{ isAllSchoolsSelected ? 'إلغاء تحديد الكل' : 'تحديد الكل' }}
            </v-btn>
          </div>

          <!-- شريط معلومات التحديد المتوافق مع النمط الفاتح والداكن -->
          <div class="dialog-info-strip d-flex align-center justify-space-between px-3 py-2.5 rounded-lg mb-3 text-caption font-weight-bold">
            <div class="d-flex align-center gap-1.5">
              <v-icon size="16" color="primary">mdi-checkbox-marked-circle-outline</v-icon>
              <span>تم تحديد <strong class="text-primary font-weight-black">{{ selectedSchoolNames.length }}</strong> من أصل {{ availableSchools.length }} مراكز امتحانية</span>
            </div>
            <div class="d-flex align-center gap-1.5">
              <v-icon size="16" color="primary">mdi-account-group-outline</v-icon>
              <span>إجمالي الطلاب المشمولين: <strong class="text-primary font-mono text-body-2 font-weight-black">{{ filteredTotalStudents }}</strong> طالباً</span>
            </div>
          </div>

          <!-- قائمة المراكز الامتحانية ببطاقات مربعة برواند قليل وليس بيضاوي -->
          <div class="d-flex flex-column gap-2" style="max-height: 380px; overflow-y: auto;">
            <div
              v-for="sch in filteredDialogSchools"
              :key="sch.name"
              class="d-flex align-center justify-space-between p-3 px-4 rounded-lg border cursor-pointer transition-all"
              :class="selectedSchoolNames.includes(sch.name) ? 'border-primary bg-primary-subtle' : 'bg-surface'"
              @click="toggleSchoolSelection(sch.name)"
            >
              <div class="d-flex align-center gap-3">
                <v-checkbox-btn
                  :model-value="selectedSchoolNames.includes(sch.name)"
                  color="primary"
                  density="compact"
                  hide-details
                  @click.stop="toggleSchoolSelection(sch.name)"
                />
                <div>
                  <div class="font-weight-bold text-body-2 text-high-emphasis">{{ sch.name }}</div>
                  <div class="text-caption text-medium-emphasis">
                    {{ sch.directorate || sch.governorate || 'التحرير' }}
                  </div>
                </div>
              </div>

              <!-- شارة عدد الطلاب مربعة برواند خفيف وليس بيضاوية -->
              <div class="center-count-badge px-3 py-1 text-caption font-weight-black font-mono">
                {{ sch.count }} طالب
              </div>
            </div>
          </div>
        </v-card-text>

        <!-- تذييل النافذة المنبثقة بأزرار النظام الرسمية -->
        <div class="pa-4 bg-surface border-t d-flex align-center justify-end gap-2">
          <custom-btn
            type="cancel"
            variant="outlined"
            label="إغلاق"
            :click="() => centersDialog = false"
          />
          <custom-btn
            type="save"
            label="تأكيد واعتماد المراكز المحددة"
            color="primary"
            :click="() => centersDialog = false"
          />
        </div>
      </v-card>
    </v-dialog>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- 8. استمارة إذن الصرف وأمر الطباعة الرسمي (مكون منفصل ومتقن)  -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <PrintOrderManifestDialog
      v-model="manifestDialog"
      :order-data="manifestData"
    />
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/omr/client.js'
import FilterFields from '@/components/FilterFields.vue'
import PrintOrderManifestDialog from './PrintOrderManifestDialog.vue'

// ── استيراد مكونات الإدخال الرسمية والموحدة من مكتبة FormInput المعتمدة ──
import CustomDate from '@/components/FormInput/CustomDate.vue'
import AutoList from '@/components/FormInput/AutoList.vue'
import CustomTextField from '@/components/FormInput/CustomTextField.vue'
import CustomCheckBox from '@/components/FormInput/CustomCheckBox.vue'
import CustomFile from '@/components/FormInput/CustomFile.vue'
import CustomTextNote from '@/components/FormInput/CustomTextNote.vue'

// ── استيراد جدول البيانات المعتمد ──
import CustomDataTable from '@/components/Display/DataTable/CustomDataTable/CustomDataTable.vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  exam: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue', 'order-created'])

const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)
const submitSuccess = ref(false)
const loadingDetails = ref(false)

// Exam full detail object fetched from DB
const examDetails = ref(null)

const examReturnReason = computed(() => {
  const isRet = props.exam?.existing_order?.status === 'failed' || props.exam?.existing_order?.status === 'returned' || props.exam?.order_status === 'failed' || props.exam?.order_status === 'returned'
  if (!isRet) return ''
  return props.exam?.return_reason || props.exam?.existing_order?.return_reason || ''
})
const examReturnNotes = computed(() => {
  const isRet = props.exam?.existing_order?.status === 'failed' || props.exam?.existing_order?.status === 'returned' || props.exam?.order_status === 'failed' || props.exam?.order_status === 'returned'
  if (!isRet) return ''
  return props.exam?.return_notes || props.exam?.existing_order?.return_notes || ''
})

// ── Unified Hierarchical Filters State ──
const filterGovernorate = ref('all')
const filterDirectorate = ref('all')
const selectedSchoolNames = ref([])
const centersDialog = ref(false)
const schoolFilterText = ref('')

// ── Facility Options ──
const facilityOptions = [
  'المطبعة السرية المركزية (ديوان الوزارة)',
  'مطبعة مكتب التربية والتعليم بالمحافظة',
  'مطبعة الكنترول المركزي ولجنة النظام والمراقبة',
  'مطبعة معتمدة داخلية',
]

// ── Surplus Reasons ──
const surplusReasonOptions = [
  'احتياط طوارئ رسمي للمراكز الامتحانية الميدانية',
  'بدائل محتملة للتالف والخطأ أثناء التعبئة والشحن',
  'طلاب ملتحقون متأخرون بقرار من اللجنة العليا للاختبارات',
  'نماذج احتياطية مخصصة للجان الكنترول والتقدير',
  'أخرى (حسب تفويض الاعتماد المرفق)',
]

// ── Form State ──
const form = ref({
  printDate: '',
  examDate: '',
  targetFacility: facilityOptions[0],
  includeBooklets: true,
  includeBubbleSheets: true,
  includeRosters: true,
  includeAnswerKeys: true,
  surplusReason: surplusReasonOptions[0],
  surplusAuthDoc: '',
  surplusFile: null,
  notes: '',
})

// ── Flexible Reserve Quantities (Manual & Per Material) ──
const quantities = ref({
  bookletReserve: 0,
  sheetReserve: 0,
  rosterReserve: 0,
})

// Helper: Format Date
const toIsoDate = (d) => {
  if (!d) return ''
  const date = new Date(d)
  if (isNaN(date.getTime())) return ''
  return date.toISOString().split('T')[0]
}

// Order Number
const orderNumber = computed(() => {
  if (!props.exam?.id) return 'ORD-DRAFT'
  const prefix = props.exam.uniqueCode || `EXAM-${props.exam.id}`
  return `PRN-REQ-${prefix}`
})

// ── Exam Header Info ──
const examTitle = computed(() => {
  return examDetails.value?.exam?.title || props.exam?.title || 'اختبار غير محدد'
})

const displayStageName = computed(() => {
  let raw = examDetails.value?.exam?.stage_name || props.exam?.stage_name || 'عام'
  raw = raw.replace(/^الصف\s+الصف/g, 'الصف')
  if (!raw.includes('الصف') && raw !== 'عام') {
    raw = `الصف ${raw}`
  }
  return raw
})

const displaySubjectName = computed(() => {
  return examDetails.value?.exam?.subject_name || props.exam?.subject_name || props.exam?.subject?.name_ar || ''
})

const examCode = computed(() => {
  return props.exam?.uniqueCode || examDetails.value?.exam?.uniqueCode || 'YE-EXAM'
})

// ── All Registered Students from DB ──
const allStudents = computed(() => {
  return examDetails.value?.registered_students || []
})

// ── 1. Governorate Filter Options ──
const availableGovernorates = computed(() => {
  const set = new Set()
  allStudents.value.forEach(s => {
    if (s.governorate) set.add(s.governorate)
  })
  if (set.size === 0 && examDetails.value?.exam?.governorate) {
    set.add(examDetails.value.exam.governorate)
  }
  return Array.from(set)
})

const governorateSelectObjects = computed(() => {
  const list = availableGovernorates.value.map(gov => {
    const count = allStudents.value.filter(s => !s.governorate || s.governorate === gov).length
    return { id: gov, name: `${gov} (${count} طالب)`, name_ar: `${gov} (${count} طالب)` }
  })
  return [
    { id: 'all', name: `كافة المحافظات المشمولة (${availableGovernorates.value.length || 1})`, name_ar: `كافة المحافظات المشمولة (${availableGovernorates.value.length || 1})` },
    ...list
  ]
})

const onGovernorateChange = (val) => {
  if (!val) filterGovernorate.value = 'all'
  filterDirectorate.value = 'all'
  selectedSchoolNames.value = availableSchools.value.map(s => s.name)
}

// ── 2. Directorate Filter Options ──
const availableDirectorates = computed(() => {
  const set = new Set()
  allStudents.value.forEach(s => {
    const matchGov = filterGovernorate.value === 'all' || s.governorate === filterGovernorate.value
    if (matchGov && s.directorate) {
      set.add(s.directorate)
    }
  })
  if (set.size === 0 && examDetails.value?.exam?.directorate) {
    set.add(examDetails.value.exam.directorate)
  }
  return Array.from(set)
})

const directorateSelectObjects = computed(() => {
  const list = availableDirectorates.value.map(dir => {
    const count = allStudents.value.filter(s => {
      const matchGov = filterGovernorate.value === 'all' || s.governorate === filterGovernorate.value
      return matchGov && s.directorate === dir
    }).length
    return { id: dir, name: `${dir} (${count} طالب)`, name_ar: `${dir} (${count} طالب)` }
  })
  return [
    { id: 'all', name: `كافة المديريات (${availableDirectorates.value.length || 1})`, name_ar: `كافة المديريات (${availableDirectorates.value.length || 1})` },
    ...list
  ]
})

const onDirectorateChange = (val) => {
  if (!val) filterDirectorate.value = 'all'
  selectedSchoolNames.value = availableSchools.value.map(s => s.name)
}

const resetAllSchools = () => {
  selectedSchoolNames.value = availableSchools.value.map(s => s.name)
}

// ── 3. Schools Filter Options ──
const availableSchools = computed(() => {
  const map = new Map()
  allStudents.value.forEach(s => {
    const matchGov = filterGovernorate.value === 'all' || s.governorate === filterGovernorate.value
    const matchDir = filterDirectorate.value === 'all' || s.directorate === filterDirectorate.value
    if (matchGov && matchDir && s.school_name) {
      if (!map.has(s.school_name)) {
        map.set(s.school_name, {
          id: s.school_id,
          name: s.school_name,
          count: 0,
          governorate: s.governorate,
          directorate: s.directorate,
        })
      }
      map.get(s.school_name).count++
    }
  })
  return Array.from(map.values())
})

const filteredDialogSchools = computed(() => {
  if (!schoolFilterText.value) return availableSchools.value
  const q = schoolFilterText.value.trim().toLowerCase()
  return availableSchools.value.filter(s => s.name.toLowerCase().includes(q))
})

const isAllSchoolsSelected = computed(() => {
  if (availableSchools.value.length === 0) return true
  return selectedSchoolNames.value.length === availableSchools.value.length
})

const centersFieldSummary = computed(() => {
  if (isAllSchoolsSelected.value) {
    return `كافة المراكز المشمولة (${availableSchools.value.length} مراكز - ${filteredTotalStudents.value} طالباً)`
  }
  return `تم تحديد ${selectedSchoolNames.value.length} من ${availableSchools.value.length} مراكز (${filteredTotalStudents.value} طالباً)`
})

const toggleSchoolSelection = (schoolName) => {
  const idx = selectedSchoolNames.value.indexOf(schoolName)
  if (idx > -1) {
    if (selectedSchoolNames.value.length > 1) {
      selectedSchoolNames.value.splice(idx, 1)
    }
  } else {
    selectedSchoolNames.value.push(schoolName)
  }
}

const toggleSelectAllSchools = () => {
  if (isAllSchoolsSelected.value) {
    if (availableSchools.value.length > 0) {
      selectedSchoolNames.value = [availableSchools.value[0].name]
    }
  } else {
    selectedSchoolNames.value = availableSchools.value.map(s => s.name)
  }
}

const facilitySelectObjects = computed(() => {
  return facilityOptions.map(f => ({
    id: f,
    name: f,
    name_ar: f,
  }))
})

const surplusReasonObjects = computed(() => {
  return surplusReasonOptions.map(r => ({
    id: r,
    name: r,
    name_ar: r,
  }))
})

// ── Filtered Students based on all active filters ──
const filteredStudents = computed(() => {
  return allStudents.value.filter(s => {
    if (filterGovernorate.value !== 'all' && s.governorate && s.governorate !== filterGovernorate.value) {
      return false
    }
    if (filterDirectorate.value !== 'all' && s.directorate && s.directorate !== filterDirectorate.value) {
      return false
    }
    if (selectedSchoolNames.value.length > 0 && s.school_name) {
      return selectedSchoolNames.value.includes(s.school_name)
    }
    return true
  })
})

const filteredTotalStudents = computed(() => {
  if (filteredStudents.value.length) return filteredStudents.value.length
  return props.exam?.registered_students_count || props.exam?.submissions_total || 40
})

const filteredSchoolsCount = computed(() => {
  if (selectedSchoolNames.value.length > 0) {
    return selectedSchoolNames.value.length
  }
  return availableSchools.value.length || 5
})

// ── Active Scope Text Summary ──
const activeScopeSummary = computed(() => {
  const parts = []
  if (filterGovernorate.value === 'all') {
    parts.push('كافة المحافظات')
  } else {
    parts.push(`محافظة: ${filterGovernorate.value}`)
  }

  if (filterDirectorate.value === 'all') {
    parts.push('كافة المديريات')
  } else {
    parts.push(`مديرية: ${filterDirectorate.value}`)
  }

  if (isAllSchoolsSelected.value) {
    parts.push('كافة المراكز المشمولة')
  } else {
    parts.push(`${selectedSchoolNames.value.length} مراكز محددة`)
  }

  return parts.join(' | ')
})

// ── Models / Versions Distribution Logic ──
const versionDistributionTable = computed(() => {
  const versions = ['A', 'B', 'C', 'D']
  const vCount = versions.length
  const total = filteredTotalStudents.value
  const reserveTotal = Math.max(
    form.value.includeBooklets ? (quantities.value.bookletReserve || 0) : 0,
    form.value.includeBubbleSheets ? (quantities.value.sheetReserve || 0) : 0
  )

  // 1. حساب الطلاب حسب نموذج الاختبار المسجل في قاعدة البيانات (model_code / exam_model)
  const modelCounts = { A: 0, B: 0, C: 0, D: 0 }
  let assignedCount = 0

  if (filteredStudents.value.length > 0) {
    filteredStudents.value.forEach(s => {
      const rawModel = (s.model_code || s.exam_model || s.version_code || s.versionCode || s.model || '').toString().trim().toUpperCase()
      if (modelCounts[rawModel] !== undefined) {
        modelCounts[rawModel]++
        assignedCount++
      }
    })
  }

  // 2. إذا لم تكن النماذج مقسمة سلفاً في السجل، يتم التوزيع الآلي المتكافئ بنسبة 100%
  const useEvenDistribution = assignedCount === 0
  const basePerModel = Math.floor(total / vCount)
  const remainderStudents = total % vCount

  return versions.map((vCode, index) => {
    let count = 0
    if (useEvenDistribution) {
      count = basePerModel + (index < remainderStudents ? 1 : 0)
    } else {
      count = modelCounts[vCode] || 0
    }

    // Distribute reserve evenly across versions
    const baseQuota = Math.floor(reserveTotal / vCount)
    const remainderReserve = reserveTotal % vCount
    const modelReserve = baseQuota + (index < remainderReserve ? 1 : 0)

    return {
      versionCode: vCode,
      studentCount: count,
      bookletsAssigned: form.value.includeBooklets ? count : 0,
      sheetsAssigned: form.value.includeBubbleSheets ? count : 0,
      reserveQuota: modelReserve,
      totalForModel: count + modelReserve,
    }
  })
})

// ── Table 1 Headers & Items (CustomDataTable مع الترويسة والببجنشن) ──
const versionTableHeaders = [
  { title: 'رمز النموذج', key: 'version_code', align: 'center', width: '16%' },
  { title: 'الطلاب المقيدون (أساسي)', key: 'student_count', align: 'center', width: '18%' },
  { title: 'كراسات الأسئلة', key: 'booklets', align: 'center', width: '16%' },
  { title: 'أوراق إجابة OMR', key: 'sheets', align: 'center', width: '16%' },
  { title: 'حصة احتياط الطوارئ (عام)', key: 'reserve_quota', align: 'center', width: '18%' },
  { title: 'نسبة التمثيل', key: 'percentage', align: 'center', width: '16%' },
]

const versionDistributionRows = computed(() => {
  return versionDistributionTable.value.map(row => ({
    id: row.versionCode,
    version_code: row.versionCode,
    student_count: row.studentCount,
    booklets: form.value.includeBooklets ? row.bookletsAssigned : '—',
    sheets: form.value.includeBubbleSheets ? row.sheetsAssigned : '—',
    reserve_quota: row.reserveQuota,
    total_for_model: row.totalForModel,
    percentage: `${filteredTotalStudents.value > 0 ? ((row.studentCount / filteredTotalStudents.value) * 100).toFixed(0) : 0}%`,
  }))
})

// تغليف البيانات بهيكل الصفحة والترقيم المتوافق مع CustomDataTable
const versionTableItems = computed(() => ({
  results: versionDistributionRows.value,
  pagination: {
    count: versionDistributionRows.value.length,
    num_pages: 1,
    current_page: 1,
  },
}))

// ── Table 2 Headers & Items (CustomDataTable) ──
const quantitiesTableHeaders = [
  { title: 'المادة المطلوب طباعتها', key: 'material_name', align: 'start', width: '38%' },
  { title: 'الكمية الأساسية (مخصصة للطلاب)', key: 'base_qty', align: 'center', width: '20%' },
  { title: 'كمية الاحتياط للطوارئ (نماذج عامة)', key: 'reserve_qty', align: 'center', width: '22%' },
  { title: 'إجمالي الكمية المعتمدة للطباعة', key: 'total_qty', align: 'center', width: '20%' },
]

const quantitiesTableRows = computed(() => [
  {
    id: 'booklets',
    material_name: 'كراسة الأسئلة الرسمية',
    sub_desc: 'موزعة على النماذج A, B, C, D',
    icon: 'mdi-file-document-multiple-outline',
    color: 'primary',
    base_qty: form.value.includeBooklets ? filteredTotalStudents.value : 0,
    total_qty: form.value.includeBooklets ? (filteredTotalStudents.value + (quantities.value.bookletReserve || 0)) : 0,
  },
  {
    id: 'sheets',
    material_name: 'ورقة الإجابة والتظليل OMR',
    sub_desc: 'الأساسي مخصص + الاحتياط نماذج عامة بيضاء',
    icon: 'mdi-radiobox-marked',
    color: 'teal',
    base_qty: form.value.includeBubbleSheets ? filteredTotalStudents.value : 0,
    total_qty: form.value.includeBubbleSheets ? (filteredTotalStudents.value + (quantities.value.sheetReserve || 0)) : 0,
  },
  {
    id: 'rosters',
    material_name: 'كشوف المناداة والجلوس',
    sub_desc: 'كشف رسمي معتمد لكل مركز امتحاني',
    icon: 'mdi-account-school-outline',
    color: 'warning',
    base_qty: form.value.includeRosters ? `${filteredSchoolsCount.value} (مراكز)` : 0,
    total_qty: form.value.includeRosters ? (filteredSchoolsCount.value + (quantities.value.rosterReserve || 0)) : 0,
  },
])

const quantitiesTableItems = computed(() => ({
  results: quantitiesTableRows.value,
  pagination: {
    count: quantitiesTableRows.value.length,
    num_pages: 1,
    current_page: 1,
  },
}))

// ── Quantities Calculations ──
const formBaseTotal = computed(() => {
  let sum = 0
  if (form.value.includeBooklets) sum += filteredTotalStudents.value
  if (form.value.includeBubbleSheets) sum += filteredTotalStudents.value
  if (form.value.includeRosters) sum += filteredSchoolsCount.value
  return sum
})

const totalReserveQuota = computed(() => {
  return Math.max(
    form.value.includeBooklets ? (quantities.value.bookletReserve || 0) : 0,
    form.value.includeBubbleSheets ? (quantities.value.sheetReserve || 0) : 0
  )
})

const totalReserveSum = computed(() => {
  let sum = 0
  if (form.value.includeBooklets) sum += (quantities.value.bookletReserve || 0)
  if (form.value.includeBubbleSheets) sum += (quantities.value.sheetReserve || 0)
  if (form.value.includeRosters) sum += (quantities.value.rosterReserve || 0)
  return sum
})

const hasSurplusQuantity = computed(() => totalReserveSum.value > 0)

const isSubmitDisabled = computed(() => {
  if (submitting.value) return true
  if (filteredTotalStudents.value <= 0) return true
  if (hasSurplusQuantity.value) {
    if (!form.value.surplusReason || !form.value.surplusAuthDoc || !form.value.surplusAuthDoc.trim()) {
      return true
    }
  }
  return false
})

// ضمان عدم إدخال أرقام سالبة في كميات الاحتياط
watch(() => quantities.value.bookletReserve, (v) => {
  if (v < 0 || isNaN(v)) quantities.value.bookletReserve = 0
})
watch(() => quantities.value.sheetReserve, (v) => {
  if (v < 0 || isNaN(v)) quantities.value.sheetReserve = 0
})
watch(() => quantities.value.rosterReserve, (v) => {
  if (v < 0 || isNaN(v)) quantities.value.rosterReserve = 0
})

const grandTotalToPrint = computed(() => formBaseTotal.value + totalReserveSum.value)

// ── Model Badge Color ──
const getModelColor = (code) => {
  switch (code) {
    case 'A': return 'primary'
    case 'B': return 'secondary'
    case 'C': return 'success'
    case 'D': return 'purple'
    default: return 'primary'
  }
}

// ── Auto-fetch DB Data on Dialog Open ──
watch(() => props.modelValue, async (newVal) => {
  if (newVal && props.exam?.id) {
    submitSuccess.value = false
    loadingDetails.value = true
    filterGovernorate.value = 'all'
    filterDirectorate.value = 'all'

    try {
      const resp = await api.get(`/api/omr/exam-linking/${props.exam.id}/`)
      if (resp.data) {
        examDetails.value = resp.data
      }
    } catch (err) {
      console.error('Failed to fetch exam linking details for print order:', err)
      examDetails.value = null
    } finally {
      loadingDetails.value = false
    }

    // Default select all schools
    selectedSchoolNames.value = availableSchools.value.map(s => s.name)

    const now = new Date()
    const defaultPrintDate = toIsoDate(now)

    let defaultExamDate = ''
    if (props.exam.exam_date) {
      defaultExamDate = toIsoDate(props.exam.exam_date)
    } else if (examDetails.value?.exam?.exam_date) {
      defaultExamDate = toIsoDate(examDetails.value.exam.exam_date)
    } else {
      const examD = new Date(now)
      examD.setDate(examD.getDate() + 7)
      defaultExamDate = toIsoDate(examD)
    }

    form.value = {
      printDate: defaultPrintDate,
      examDate: defaultExamDate,
      targetFacility: facilityOptions[0],
      includeBooklets: true,
      includeBubbleSheets: true,
      includeRosters: true,
      includeAnswerKeys: true,
      surplusReason: surplusReasonOptions[0],
      surplusAuthDoc: '',
      surplusFile: null,
      notes: '',
    }

    quantities.value = {
      bookletReserve: 0,
      sheetReserve: 0,
      rosterReserve: 0,
    }
  }
})

// ── Submit Order ──
const submitPrintOrder = async () => {
  if (!props.exam?.id) return
  submitting.value = true

  try {
    const payload = {
      order_number: orderNumber.value,
      exam_id: props.exam.id,
      batch_id: orderNumber.value,
      scope: {
        governorate: filterGovernorate.value,
        directorate: filterDirectorate.value,
        selected_schools: selectedSchoolNames.value,
        summary: activeScopeSummary.value,
      },
      student_ids: 'all',
      print_date: form.value.printDate,
      exam_date: form.value.examDate,
      target_facility: form.value.targetFacility,
      materials: {
        include_booklets: form.value.includeBooklets,
        include_bubble_sheets: form.value.includeBubbleSheets,
        include_rosters: form.value.includeRosters,
        include_answer_keys: form.value.includeAnswerKeys,
      },
      distribution_by_version: versionDistributionTable.value,
      quantities: {
        base_students: filteredTotalStudents.value,
        centers_count: filteredSchoolsCount.value,
        booklets: {
          base: form.value.includeBooklets ? filteredTotalStudents.value : 0,
          reserve: quantities.value.bookletReserve || 0,
          total: form.value.includeBooklets ? (filteredTotalStudents.value + (quantities.value.bookletReserve || 0)) : 0,
        },
        bubble_sheets: {
          base: form.value.includeBubbleSheets ? filteredTotalStudents.value : 0,
          reserve: quantities.value.sheetReserve || 0,
          total: form.value.includeBubbleSheets ? (filteredTotalStudents.value + (quantities.value.sheetReserve || 0)) : 0,
        },
        rosters: {
          base: form.value.includeRosters ? filteredSchoolsCount.value : 0,
          reserve: quantities.value.rosterReserve || 0,
          total: form.value.includeRosters ? (filteredSchoolsCount.value + (quantities.value.rosterReserve || 0)) : 0,
        },
        grand_total: grandTotalToPrint.value,
      },
      surplus_justification: hasSurplusQuantity.value ? {
        reason: form.value.surplusReason,
        authorization_document: form.value.surplusAuthDoc,
        notes: form.value.notes,
        has_file: !!form.value.surplusFile,
      } : null,
    }

    // Call backend print-orders create-order endpoint to persist and document the official order in pending status!
    try {
      await api.post('/api/omr/print-orders/create-order/', {
        exam_id: props.exam.id,
        order_number: orderNumber.value,
        scheduled_print_date: form.value.scheduledPrintDate || null,
        press_name: form.value.pressName || 'المطبعة السرية المركزية (ديوان الوزارة)',
        responsible_officer: form.value.responsibleOfficer || 'مدير إدارة الامتحانات',
      })
    } catch (dbErr) {
      console.warn('Could not save in backend print-orders table:', dbErr)
    }

    // Save in localStorage for offline/client registry
    try {
      const existing = JSON.parse(localStorage.getItem('omr_print_orders') || '[]')
      existing.unshift(payload)
      localStorage.setItem('omr_print_orders', JSON.stringify(existing.slice(0, 50)))
    } catch (_) {}

    submitSuccess.value = true
    emit('order-created', payload)
  } catch (err) {
    console.error('Error submitting print order:', err)
  } finally {
    submitting.value = false
  }
}

const goToRegistry = () => {
  emit('update:modelValue', false)
  const target = `/omr-print-registry?view=orders&tab=exams&subtab=all`
  router.push(target).catch(() => {
    window.location.href = target
  })
}

// ── استمارة أمر الطباعة الرسمي (مكون منفصل ومتقن) ──
const manifestDialog = ref(false)

const manifestData = computed(() => ({
  orderNumber: orderNumber.value,
  examTitle: examTitle.value,
  stageName: displayStageName.value,
  subjectName: displaySubjectName.value,
  examCode: examCode.value,
  facility: form.value.targetFacility,
  printDate: form.value.printDate,
  examDate: form.value.examDate,
  scopeSummary: activeScopeSummary.value,
  schoolsCount: filteredSchoolsCount.value,
  studentsCount: filteredTotalStudents.value,
  versionsRows: versionDistributionRows.value,
  materialsRows: quantitiesTableRows.value.map(m => ({
    ...m,
    reserve_qty: m.id === 'booklets'
      ? (quantities.value.bookletReserve || 0)
      : m.id === 'sheets'
        ? (quantities.value.sheetReserve || 0)
        : (quantities.value.rosterReserve || 0),
  })),
  baseTotal: formBaseTotal.value,
  reserveTotal: totalReserveSum.value,
  grandTotal: grandTotalToPrint.value,
  hasSurplus: hasSurplusQuantity.value,
  surplusReason: form.value.surplusReason,
  surplusAuthDoc: form.value.surplusAuthDoc,
  notes: form.value.notes,
}))
</script>

<style scoped>
.modal-top-stripe {
  height: 4px;
  background: rgb(var(--v-theme-primary));
}

/* ══════════════════════════════════════════════════════
   FIELD ICONS (داكنة/افتراضية في الحالة العادية، وتتحول لأزرق عند التركيز والدخول)
══════════════════════════════════════════════════════ */
.print-order-modal :deep(.v-field:not(.v-field--focused) .v-field__prepend-inner .v-icon) {
  color: inherit !important;
  opacity: 0.55 !important;
  font-size: 20px !important;
  transition: color 0.2s ease, opacity 0.2s ease !important;
}

.print-order-modal :deep(.v-field.v-field--focused .v-field__prepend-inner .v-icon),
.print-order-modal :deep(.v-field:focus-within .v-field__prepend-inner .v-icon),
.print-order-modal :deep(.v-input--focused .v-field__prepend-inner .v-icon) {
  color: rgb(var(--v-theme-primary)) !important;
  opacity: 1 !important;
  font-size: 20px !important;
}

/* ══════════════════════════════════════════════════════
   CUSTOM DATA TABLE OVERRIDES FOR PRINT ORDER DIALOG
   (توزيع متكافئ ومنع تلاصق الأعمدة والخلايا وتوحيد الارتفاع)
══════════════════════════════════════════════════════ */
.print-order-table :deep(table) {
  width: 100% !important;
  table-layout: fixed !important;
  border-collapse: separate !important;
}

.print-order-table :deep(th) {
  font-weight: 800 !important;
  font-size: 0.82rem !important;
  padding: 12px 14px !important;
  white-space: nowrap !important;
  background-color: rgba(var(--v-theme-primary), 0.05) !important;
  color: rgb(var(--v-theme-on-surface)) !important;
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
}

.print-order-table :deep(td) {
  padding: 10px 14px !important;
  vertical-align: middle !important;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06) !important;
}

.print-order-table :deep(tr:last-child td) {
  border-bottom: none !important;
}

.print-order-table :deep(tr:hover td) {
  background-color: rgba(var(--v-theme-primary), 0.03) !important;
}

/* توحيد مقاس خلايا الشارات والأرقام داخل الجداول */
.min-w-cell {
  min-width: 56px !important;
  justify-content: center !important;
  text-align: center !important;
}

/* ══════════════════════════════════════════════════════
   TABLE SUMMARY STRIP (مطابق للمظهر العام الموحد)
══════════════════════════════════════════════════════ */
.table-summary-strip {
  background: rgba(var(--v-theme-primary), 0.05);
  border-color: rgba(var(--v-theme-primary), 0.12) !important;
}

/* ══════════════════════════════════════════════════════
   RESERVE INPUT BOX IN QUANTITIES TABLE
══════════════════════════════════════════════════════ */
.reserve-table-input :deep(.v-field) {
  border-radius: 6px !important;
  min-height: 32px !important;
  height: 32px !important;
  background: transparent !important;
}

.reserve-table-input :deep(.v-field__input) {
  text-align: center !important;
  font-weight: 800 !important;
  font-family: monospace, monospace !important;
  padding: 2px 6px !important;
  min-height: 32px !important;
  height: 32px !important;
  font-size: 0.875rem !important;
}

.reserve-table-input :deep(input::-webkit-outer-spin-button),
.reserve-table-input :deep(input::-webkit-inner-spin-button) {
  -webkit-appearance: none;
  margin: 0;
}
.reserve-table-input :deep(input[type=number]) {
  -moz-appearance: textfield;
}

/* ══════════════════════════════════════════════════════
   CENTERS POPUP STYLING (متناسق مع الوضع الفاتح والداكن)
══════════════════════════════════════════════════════ */
.dialog-info-strip {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.18) !important;
  color: rgb(var(--v-theme-on-surface)) !important;
}

.center-count-badge {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.22) !important;
  border-radius: 6px !important; /* مربع برواند خفيف وليس بيضاوي */
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.unified-badge-teal {
  background: rgba(0, 150, 136, 0.1) !important;
  color: #00897b !important;
  border: 1px solid rgba(0, 150, 136, 0.25) !important;
}

.unified-badge-warning {
  background: rgba(245, 124, 0, 0.1) !important;
  color: #e65100 !important;
  border: 1px solid rgba(245, 124, 0, 0.25) !important;
}

.unified-badge-success {
  background: rgba(46, 125, 50, 0.1) !important;
  color: #2e7d32 !important;
  border: 1px solid rgba(46, 125, 50, 0.25) !important;
}

.unified-badge-default {
  background: rgba(var(--v-theme-on-surface), 0.06) !important;
  color: rgb(var(--v-theme-on-surface)) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.18) !important;
}

.bg-primary-subtle {
  background: rgba(var(--v-theme-primary), 0.04) !important;
}

.font-mono {
  font-family: monospace, monospace;
}

/* ══════════════════════════════════════════════════════
   EXAM HEADER BADGES & ROW SPACING (تنظيم وتباعد مريح بدون تلاصق)
══════════════════════════════════════════════════════ */
.exam-badges-bar {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  flex-wrap: wrap !important;
}

.badge-spaced {
  padding: 5px 12px !important;
  gap: 8px !important;
  font-size: 0.8rem !important;
  line-height: 1.2 !important;
}

.badge-spaced .v-icon {
  margin-inline-end: 6px !important;
  flex-shrink: 0 !important;
}

.material-cell-item {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
}

.material-avatar {
  flex-shrink: 0 !important;
  margin-inline-end: 12px !important;
}

.summary-item-header {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
}

.summary-item-avatar {
  margin-inline-end: 12px !important;
  flex-shrink: 0 !important;
}

.filter-fields-row {
  margin-inline: -10px !important;
}

.filter-fields-row > [class*="v-col"] {
  padding-inline: 10px !important;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}
</style>
