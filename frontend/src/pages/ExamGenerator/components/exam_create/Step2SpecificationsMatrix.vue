<template>
  <div>
            <!-- Integrated Flush Tabs inside a single card -->
            <div class="section-group-card rounded-2xl overflow-hidden mb-6 border-subtle">
              <div class="matrix-tabs-bar border-b-subtle d-flex" style="overflow-x: auto;">
                <button v-for="(tab, tIdx) in matrixTabItems" :key="tIdx"
                  class="matrix-tab-btn flex-1-1-100 pa-4 text-center cursor-pointer font-weight-bold d-flex align-center justify-center gap-2"
                  :class="{ 'is-active': activeTab === tIdx }"
                  @click="$emit('update:activeTab', tIdx)">
                  <v-icon size="20">{{ tab.icon }}</v-icon>
                  <span>{{ tab.label }}</span>
                </button>
              </div>

              <v-window :model-value="activeTab" @update:model-value="$emit('update:activeTab', $event)" class="pa-6 bg-transparent">
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
                                      {{ unit.lessonsCount ?? getUnitLessonsCount(unit.id) }} {{ exam.institution_type === 'university' ? 'محاضرة' : 'درس' }}
                                    </v-chip>
                                    <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold">
                                      <v-icon start size="12">mdi-check-circle-outline</v-icon>
                                      {{ unit.approvedQuestionsCount ?? getUnitApprovedQuestionsCount(unit.id) }} سؤال معتمد
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
                                  <div v-if="Number(exam.questionsCount) > 0" class="d-flex align-center gap-2 flex-wrap text-caption mt-1">
                                    <span class="text-medium-emphasis">المطلوب: <strong class="text-primary">{{ getUnitRequiredQuestions(unit) }}</strong></span>
                                    <span>•</span>
                                    <span :class="getUnitRemainingQuestions(unit) >= 0 ? 'text-medium-emphasis' : 'text-error font-weight-bold'">
                                      المتبقي غير المختار: <strong :class="getUnitRemainingQuestions(unit) > 0 ? 'text-success' : (getUnitRemainingQuestions(unit) === 0 ? 'text-medium-emphasis' : 'text-error')">{{ Math.max(0, getUnitRemainingQuestions(unit)) }}</strong>
                                    </span>
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
                                  {{ unit.lessonsCount ?? getUnitLessonsCount(unit.id) }} {{ exam.institution_type === 'university' ? 'محاضرة' : 'درس' }}
                                </v-chip>
                                <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold">
                                  <v-icon start size="12">mdi-check-circle-outline</v-icon>
                                  {{ unit.approvedQuestionsCount ?? getUnitApprovedQuestionsCount(unit.id) }} سؤال معتمد
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
                              <div v-if="Number(exam.questionsCount) > 0" class="d-flex align-center gap-2 flex-wrap text-caption mt-1">
                                <span class="text-medium-emphasis">المطلوب: <strong class="text-primary">{{ getUnitRequiredQuestions(unit) }}</strong></span>
                                <span>•</span>
                                <span :class="getUnitRemainingQuestions(unit) >= 0 ? 'text-medium-emphasis' : 'text-error font-weight-bold'">
                                  المتبقي غير المختار: <strong :class="getUnitRemainingQuestions(unit) > 0 ? 'text-success' : (getUnitRemainingQuestions(unit) === 0 ? 'text-medium-emphasis' : 'text-error')">{{ Math.max(0, getUnitRemainingQuestions(unit)) }}</strong>
                                </span>
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
                        :model-value="bloomEnabled" @update:model-value="$emit('update:bloomEnabled', $event)"
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

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { difficultyColor, difficultyLabel } from '../../composables/examHelpers'

const props = defineProps({
  exam: {
    type: Object,
    required: true
  },
  activeTab: {
    type: Number,
    default: 0
  },
  matrixTabItems: {
    type: Array,
    required: true
  },
  blueprint: {
    type: Object,
    required: true
  },
  modelsMode: {
    type: String,
    default: 'uniform'
  },
  modelGroups: {
    type: Array,
    default: () => []
  },
  bloomEnabled: {
    type: Boolean,
    default: false
  },
  theme: {
    type: Object,
    default: () => ({})
  },
  activeUnitGroupIndex: {
    type: Number,
    default: 0
  },
  currentUnitGroup: {
    type: Object,
    default: null
  },
  currentGroupUnitsTotal: {
    type: Number,
    default: 100
  },
  currentActiveUnitsList: {
    type: Array,
    default: () => []
  },
  activeTypeGroupIndex: {
    type: Number,
    default: 0
  },
  currentTypeGroup: {
    type: Object,
    default: null
  },
  currentGroupTypesTotal: {
    type: Number,
    default: 100
  },
  currentGroupDistributedMarks: {
    type: Number,
    default: 100
  },
  currentActiveTypesList: {
    type: Array,
    default: () => []
  },
  totalDifficultyPercentage: {
    type: Number,
    default: 100
  },
  totalBloomPercentage: {
    type: Number,
    default: 100
  },
  hasTermSeparation: {
    type: Function,
    required: true
  },
  isUnitInTerm: {
    type: Function,
    required: true
  },
  selectUnitGroup: {
    type: Function,
    required: true
  },
  selectTypeGroup: {
    type: Function,
    required: true
  },
  getGroupVersionCodes: {
    type: Function,
    required: true
  },
  getGroupTargetNames: {
    type: Function,
    required: true
  },
  getGroupUnitsTotal: {
    type: Function,
    required: true
  },
  getGroupTypesTotal: {
    type: Function,
    required: true
  },
  getUnitLessonsCount: {
    type: Function,
    required: true
  },
  getUnitApprovedQuestionsCount: {
    type: Function,
    required: true
  },
  getUnitRequiredQuestions: {
    type: Function,
    required: true
  },
  getUnitRemainingQuestions: {
    type: Function,
    required: true
  },
  adjustUnitPercentage: {
    type: Function,
    required: true
  },
  updateUnitPercentage: {
    type: Function,
    required: true
  },
  autoDistributeCurrentGroupUnits: {
    type: Function,
    required: true
  },
  autoDistributeAllGroupsUnits: {
    type: Function,
    required: true
  },
  copyCurrentGroupUnitsToAll: {
    type: Function,
    required: true
  },
  adjustTypePercentage: {
    type: Function,
    required: true
  },
  updateTypePercentage: {
    type: Function,
    required: true
  },
  adjustTypeMark: {
    type: Function,
    required: true
  },
  setTotalMarks: {
    type: Function,
    required: true
  },
  autoBalanceMarks: {
    type: Function,
    required: true
  },
  getTypeQuestionsCount: {
    type: Function,
    required: true
  },
  getTypeTotalMarks: {
    type: Function,
    required: true
  },
  autoDistributeCurrentGroupTypes: {
    type: Function,
    required: true
  },
  autoDistributeAllGroupsTypes: {
    type: Function,
    required: true
  },
  copyCurrentGroupTypesToAll: {
    type: Function,
    required: true
  },
  updateDistribution: {
    type: Function,
    required: true
  },
  autoDistribute: {
    type: Function,
    required: true
  },
  openUnitDetails: {
    type: Function,
    required: true
  }
})

defineEmits([
  'update:activeTab',
  'update:bloomEnabled',
  'update:activeUnitGroupIndex',
  'update:activeTypeGroupIndex'
])
</script>
