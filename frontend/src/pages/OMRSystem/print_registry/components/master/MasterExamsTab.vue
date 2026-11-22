<template>
  <div class="master-exams-tab-component">
    <!-- ── شريط التبويبات الفرعية الأربعة: الطلبات / المجدولة / المستحقة / المكتملة ── -->
    <div class="d-flex align-center justify-space-between flex-wrap gap-2 px-4 py-2 border-b bg-surface-variant-subtle">
      <v-tabs
        :model-value="subTab"
        @update:model-value="$emit('update:subTab', $event)"
        color="primary"
        density="compact"
        class="sub-stage-tabs"
      >
        <!-- 1. الطلبات (الطلبات الجارية وغير المكتملة) -->
        <v-tab value="orders" class="font-weight-bold">
          <v-icon start size="18" color="primary">mdi-format-list-bulleted</v-icon>
          الطلبات ({{ pendingAndActiveOrdersCount }})
        </v-tab>

        <!-- 2. المجدولة (المستقبلية) -->
        <v-tab value="scheduled" class="font-weight-bold">
          <v-icon start size="18" color="info">mdi-calendar-clock</v-icon>
          المجدولة ({{ scheduledExamsCount }})
        </v-tab>

        <!-- 3. المستحقة (قائمة انتظار الطباعة الجاهزة للتنفيذ) -->
        <v-tab value="due" class="font-weight-bold">
          <v-icon start size="18" color="warning">mdi-clock-alert-outline</v-icon>
          المستحقة ({{ dueExamsCount }})
        </v-tab>

        <!-- 4. المكتملة (الاختبارات التي تم سحب وثائقها بالكامل) -->
        <v-tab value="completed" class="font-weight-bold">
          <v-icon start size="18" color="primary">mdi-check-decagram</v-icon>
          المكتملة ({{ completedExamsCount }})
        </v-tab>

        <!-- 5. الملغية (أوامر ملغاة رسمياً من الكنترول) -->
        <v-tab value="cancelled" class="font-weight-bold">
          <v-icon start size="18" color="secondary">mdi-cancel</v-icon>
          الملغية ({{ cancelledExamsCount }})
        </v-tab>

        <!-- 6. السجل الشامل (كافة الاختبارات لكافة الحالات) -->
        <v-tab value="all" class="font-weight-bold">
          <v-icon start size="18" color="medium-emphasis">mdi-archive-outline</v-icon>
          السجل الشامل ({{ allExamsCount }})
        </v-tab>
      </v-tabs>

      <div class="d-flex align-center gap-2">
        <v-chip
          size="small"
          variant="tonal"
          :color="subTab === 'due' ? 'warning' : (subTab === 'scheduled' ? 'info' : (subTab === 'cancelled' ? 'secondary' : (subTab === 'all' ? 'default' : 'primary')))"
          class="font-weight-medium"
        >
          <v-icon start size="14">
            {{ subTab === 'due' ? 'mdi-clock-fast' : (subTab === 'scheduled' ? 'mdi-calendar-range' : (subTab === 'completed' ? 'mdi-check-all' : (subTab === 'cancelled' ? 'mdi-cancel' : (subTab === 'all' ? 'mdi-archive-outline' : 'mdi-file-document-multiple-outline')))) }}
          </v-icon>
          {{ subTab === 'due' ? 'المستحقة للتنفيذ' : (subTab === 'scheduled' ? 'أوامر مجدولة' : (subTab === 'completed' ? 'مكتملة 100%' : (subTab === 'cancelled' ? 'طلبات ملغاة' : (subTab === 'all' ? 'السجل الشامل (الكل)' : 'الطلبات النشطة')))) }}
        </v-chip>
      </div>
    </div>

    <!-- عرض الجدول المركزي للاختبارات حسب التبويب النشط -->
    <custom-data-table
      :key="'exams-tbl-' + subTab"
      :model-value="selectedRows"
      @update:model-value="$emit('update:selectedRows', $event)"
      :items="items"
      :getData="getData"
      :headers="headers"
      :customLoading="loading"
      :hasFilter="false"
      :log="false"
      :restore="false"
      :numbering="true"
      :showSelect="true"
      :actions="false"
      :search="true"
      class="bg-transparent"
    >
      <template v-slot:item-slot="{ item, key, index }">
        <template v-if="key === 'numbering'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </div>
        </template>

        <template v-else-if="key === 'uniqueCode'">
          <div class="d-flex justify-center align-center">
            <span class="font-mono font-weight-bold text-caption px-2 py-1 rounded bg-grey-lighten-4 border">
              {{ item.uniqueCode }}
            </span>
          </div>
        </template>

        <template v-else-if="key === 'title'">
          <div class="py-2" style="min-width: 280px;">
            <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.title }}</div>
            <div class="d-flex align-center flex-wrap gap-2 text-caption text-medium-emphasis mt-0.5">
              <span class="font-weight-medium">المادة: {{ item.subject_name || 'عام' }}</span>
              <span v-if="item.order_number" class="text-primary font-mono font-weight-bold">
                <v-icon size="12" class="me-0.5">mdi-barcode</v-icon>
                {{ item.order_number }}
              </span>
              <span v-if="item.exam_date" class="text-medium-emphasis">
                <v-icon size="12" class="me-0.5" color="teal">mdi-calendar-check</v-icon>
                الامتحان: {{ item.exam_date }}
              </span>
              <span v-if="item.scheduled_print_date" class="text-medium-emphasis">
                <v-icon size="12" class="me-0.5" color="indigo">mdi-calendar-clock</v-icon>
                الطباعة: {{ item.scheduled_print_date }}
              </span>
            </div>

            <!-- شريط توضيح سبب الإرجاع إذا كان الطلب مرتجعاً -->
            <div
              v-if="item.order_status === 'returned' || item.is_returned"
              class="mt-1 d-inline-flex align-center gap-1 px-2 py-0.5 rounded-lg bg-error-lighten-5 text-error border border-error-subtle text-caption font-weight-bold"
            >
              <v-icon size="14" color="error">mdi-alert-circle-outline</v-icon>
              <span>سبب الإرجاع: {{ item.return_reason || 'يحتاج مراجعة وتعديل فني' }}</span>
              <span v-if="item.return_notes" class="text-medium-emphasis ms-1 font-weight-regular">({{ item.return_notes }})</span>
            </div>
          </div>
        </template>

        <template v-else-if="key === 'schools_count'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-subtitle-2">{{ item.schools_count ?? 0 }}</span>
          </div>
        </template>

        <template v-else-if="key === 'total_registered'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-subtitle-2">{{ item.total_registered || item.total_students || 0 }}</span>
          </div>
        </template>

        <template v-else-if="key === 'printed_count'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
          </div>
        </template>

        <template v-else-if="key === 'printed_rate'">
          <div class="d-flex align-center justify-center gap-2 px-1">
            <v-progress-linear
              :model-value="item.printed_rate || 0"
              :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
              height="8"
              rounded
              style="min-width: 60px; max-width: 80px;"
            />
            <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
          </div>
        </template>

        <template v-else-if="key === 'print_status'">
          <div class="d-flex justify-center align-center">
            <!-- 1. مكتمل (Completed) -->
            <div
              v-if="item.is_completed || item.order_status === 'completed'"
              class="center-count-badge unified-badge-primary px-2.5 py-1 text-caption font-weight-bold"
            >
              <v-icon size="14" color="primary" class="me-1">mdi-check-decagram</v-icon>
              <span>مكتمل</span>
            </div>

            <!-- 2. قيد الطباعة (Printing - سحب جزئي جارٍ) -->
            <div
              v-else-if="item.order_status === 'printing'"
              class="center-count-badge unified-badge-warning px-2.5 py-1 text-caption font-weight-bold"
            >
              <v-icon size="14" color="warning" class="me-1">mdi-printer-play</v-icon>
              <span>قيد الطباعة</span>
            </div>

            <!-- 3. بانتظار الموعد (Scheduled - مجدول لموعد قادم) -->
            <div
              v-else-if="item.is_scheduled || item.order_status === 'scheduled'"
              class="center-count-badge unified-badge-info px-2.5 py-1 text-caption font-weight-bold"
            >
              <v-icon size="14" color="info" class="me-1">mdi-calendar-clock</v-icon>
              <span>بانتظار الموعد</span>
            </div>

            <!-- 4. فشل أو يحتاج معالجة (Failed - تعثر أو مرتجع) -->
            <div
              v-else-if="item.is_returned || item.order_status === 'failed' || item.order_status === 'returned'"
              class="center-count-badge unified-badge-error px-2.5 py-1 text-caption font-weight-bold"
              :title="item.return_reason || 'مرتجع للتعديل'"
            >
              <v-icon size="14" color="error" class="me-1">mdi-alert-circle-outline</v-icon>
              <span>فشل أو يحتاج معالجة</span>
            </div>

            <!-- 5. ملغى (Cancelled) -->
            <div
              v-else-if="item.order_status === 'cancelled'"
              class="center-count-badge unified-badge-grey px-2.5 py-1 text-caption font-weight-bold"
            >
              <v-icon size="14" class="me-1">mdi-cancel</v-icon>
              <span>ملغى</span>
            </div>

            <!-- 6. بانتظار الاعتماد والمراجعة (Pending) -->
            <div
              v-else-if="item.is_pending || item.order_status === 'pending'"
              class="center-count-badge unified-badge-warning px-2.5 py-1 text-caption font-weight-bold"
            >
              <v-icon size="14" color="warning" class="me-1">mdi-clock-alert-outline</v-icon>
              <span>بانتظار الاعتماد</span>
            </div>

            <!-- 7. جاهز للتنفيذ (Ready - مستحق التنفيذ اليوم) -->
            <div
              v-else
              class="center-count-badge unified-badge-primary px-2.5 py-1 text-caption font-weight-bold"
            >
              <v-icon size="14" color="primary" class="me-1">mdi-clock-fast</v-icon>
              <span>جاهز للتنفيذ</span>
            </div>
          </div>
        </template>

        <template v-else-if="key === 'actions'">
          <div class="d-flex align-center justify-center gap-1 flex-nowrap table-actions-cell">
            <!-- 1. في تبويب "المستحقة" (Due Queue): تنفيذ فوري عبر الطباعة المباشرة واستوديو الطباعة -->
            <template v-if="subTab === 'due'">
              <!-- زر الطباعة المباشرة الفورية -->
              <v-btn
                size="small"
                density="compact"
                color="primary"
                variant="flat"
                rounded="lg"
                class="font-weight-bold table-action-btn px-2"
                prepend-icon="mdi-printer"
                @click="$emit('direct-print', item)"
                title="أمر الطباعة المباشر الفوري لكافة وثائق الاختبار"
              >
                طباعة مباشرة
              </v-btn>

              <!-- زر استوديو الطباعة التفصيلي -->
              <v-btn
                size="small"
                density="compact"
                icon="mdi-printer-eye"
                color="primary"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('open-studio', item)"
                title="فتح استوديو الطباعة التفصيلي لتأكيد وتنفيذ السحب"
              />

              <!-- زر إذن الصرف الرسمي A4 -->
              <v-btn
                v-if="item.has_order"
                size="small"
                density="compact"
                icon="mdi-file-document-check-outline"
                color="secondary"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('preview-manifest', item)"
                title="معاينة إذن الصرف وأمر الطباعة الرسمي A4"
              />

              <!-- زر إلغاء أمر الطباعة رسمياً -->
              <v-btn
                size="small"
                density="compact"
                icon="mdi-cancel"
                color="error"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('cancel-order', item)"
                title="إلغاء أمر الطباعة رسمياً"
              />
            </template>

            <!-- 2. في تبويب "المجدولة" (Scheduled): تقديم الموعد استثنائياً -->
            <template v-else-if="subTab === 'scheduled'">
              <v-btn
                size="small"
                density="compact"
                color="warning"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold table-action-btn px-2"
                prepend-icon="mdi-fast-forward"
                @click="$emit('advance-schedule', item)"
                title="تقديم موعد الطباعة استثنائياً لليوم ونقله للمستحقة"
              >
                تقديم الموعد
              </v-btn>
              <v-btn
                v-if="item.has_order"
                size="small"
                density="compact"
                icon="mdi-file-document-outline"
                color="secondary"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('preview-manifest', item)"
                title="معاينة إذن الصرف وأمر الطباعة الرسمي A4"
              />
              <v-btn
                size="small"
                density="compact"
                icon="mdi-cancel"
                color="error"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('cancel-order', item)"
                title="إلغاء أمر الطباعة رسمياً"
              />
            </template>

            <!-- 3. في تبويب "المكتملة" (Completed): أرشفة وتوثيق فقط -->
            <template v-else-if="subTab === 'completed'">
              <v-btn
                v-if="item.has_order"
                size="small"
                density="compact"
                color="secondary"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold table-action-btn px-2"
                prepend-icon="mdi-file-document-check-outline"
                @click="$emit('preview-manifest', item)"
                title="معاينة إذن الصرف ومحضر التسليم الرسمي A4"
              >
                إذن الصرف والتسليم
              </v-btn>
              <v-btn
                size="small"
                density="compact"
                icon="mdi-history"
                color="info"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('view-history', item)"
                title="عرض سجل وتاريخ دفعات السحب المطبوعة لهذا الاختبار"
              />
            </template>

            <!-- 4. في تبويب "الملغية" (Cancelled): استعراض إذن الصرف أو إعادة التفعيل -->
            <template v-else-if="subTab === 'cancelled'">
              <v-btn
                size="small"
                density="compact"
                color="primary"
                variant="flat"
                rounded="lg"
                class="font-weight-bold table-action-btn px-2 text-white"
                prepend-icon="mdi-restore"
                @click="$emit('approve-order', item)"
                title="إعادة تفعيل واعتماد وجدولة طلب الطباعة الملغى"
              >
                إعادة التفعيل
              </v-btn>
              <v-btn
                v-if="item.has_order"
                size="small"
                density="compact"
                icon="mdi-file-document-outline"
                color="secondary"
                variant="tonal"
                rounded="lg"
                class="table-action-icon-btn ms-1"
                @click="$emit('preview-manifest', item)"
                title="معاينة إذن الصرف المحفوظ في الأرشيف"
              />
            </template>

            <!-- 5. في تبويب "الطلبات" (All Orders): إجراءات مركزة دون تكرار شارات الحالة -->
            <template v-else>
              <!-- أ. مكتمل 100% -->
              <template v-if="item.is_completed">
                <v-btn
                  v-if="item.has_order"
                  size="small"
                  density="compact"
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  class="font-weight-bold table-action-btn px-2"
                  prepend-icon="mdi-file-document-check-outline"
                  @click="$emit('preview-manifest', item)"
                  title="معاينة إذن الصرف ومحضر التسليم الرسمي A4"
                >
                  إذن الصرف والتسليم
                </v-btn>
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-history"
                  color="info"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('view-history', item)"
                  title="عرض سجل وتاريخ دفعات السحب المطبوعة لهذا الاختبار"
                />
              </template>

              <!-- ب. طلب بانتظار الاعتماد والمراجعة -->
              <template v-else-if="item.is_pending">
                <v-btn
                  size="small"
                  density="compact"
                  color="primary"
                  variant="flat"
                  rounded="lg"
                  class="font-weight-bold table-action-btn px-2 text-white"
                  prepend-icon="mdi-check-decagram-outline"
                  @click="$emit('approve-order', item)"
                  title="مراجعة واعتماد وجدولة طلب الطباعة رسمياً"
                >
                  تأكيد واعتماد
                </v-btn>
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-keyboard-return"
                  color="warning"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('return-order', item)"
                  title="إرجاع طلب الطباعة للتعديل مع توثيق السبب"
                />
                <v-btn
                  v-if="item.has_order"
                  size="small"
                  density="compact"
                  icon="mdi-file-document-outline"
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('preview-manifest', item)"
                  title="معاينة إذن الصرف واستمارة الطلب الرسمية"
                />
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-cancel"
                  color="error"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('cancel-order', item)"
                  title="إلغاء أمر الطباعة رسمياً"
                />
              </template>

              <!-- ج. طلب مرتجع للتعديل -->
              <template v-else-if="item.is_returned">
                <v-btn
                  size="small"
                  density="compact"
                  color="primary"
                  variant="flat"
                  rounded="lg"
                  class="font-weight-bold table-action-btn px-2 text-white"
                  prepend-icon="mdi-check-decagram-outline"
                  @click="$emit('approve-order', item)"
                  title="إعادة فحص واعتماد الطلب بعد التعديل"
                >
                  إعادة الاعتماد
                </v-btn>
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-alert-circle-outline"
                  color="error"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('return-order', item)"
                  :title="item.return_reason ? ('سبب الإرجاع: ' + item.return_reason) : 'عرض سبب الإرجاع'"
                />
                <v-btn
                  v-if="item.has_order"
                  size="small"
                  density="compact"
                  icon="mdi-file-document-outline"
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('preview-manifest', item)"
                  title="معاينة إذن الصرف الرسمي A4"
                />
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-cancel"
                  color="error"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('cancel-order', item)"
                  title="إلغاء أمر الطباعة رسمياً"
                />
              </template>

              <!-- د. طلب مجدول لموعد قادم -->
              <template v-else-if="item.is_scheduled">
                <v-btn
                  size="small"
                  density="compact"
                  color="warning"
                  variant="tonal"
                  rounded="lg"
                  class="font-weight-bold table-action-btn px-2"
                  prepend-icon="mdi-fast-forward"
                  @click="$emit('advance-schedule', item)"
                  title="تقديم موعد الطباعة استثنائياً ونقله للمستحقة"
                >
                  تقديم الموعد
                </v-btn>
                <v-btn
                  v-if="item.has_order"
                  size="small"
                  density="compact"
                  icon="mdi-file-document-outline"
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('preview-manifest', item)"
                  title="معاينة إذن الصرف الرسمي A4"
                />
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-cancel"
                  color="error"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('cancel-order', item)"
                  title="إلغاء أمر الطباعة رسمياً"
                />
              </template>

              <!-- هـ. طلب معتمد ومستحق جاهز للتنفيذ -->
              <template v-else-if="item.is_due">
                <v-btn
                  size="small"
                  density="compact"
                  color="primary"
                  variant="tonal"
                  rounded="lg"
                  class="font-weight-bold table-action-btn px-2"
                  prepend-icon="mdi-printer"
                  @click="$emit('update:subTab', 'due')"
                  title="الانتقال إلى تبويب المستحقة لتنفيذ الطباعة"
                >
                  تنفيذ الطباعة
                </v-btn>
                <v-btn
                  v-if="item.has_order"
                  size="small"
                  density="compact"
                  icon="mdi-file-document-outline"
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('preview-manifest', item)"
                  title="معاينة إذن الصرف الرسمي A4"
                />
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-cancel"
                  color="error"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('cancel-order', item)"
                  title="إلغاء أمر الطباعة رسمياً"
                />
              </template>

              <!-- و. في أي حالة أخرى -->
              <template v-else>
                <v-btn
                  size="small"
                  density="compact"
                  color="success"
                  variant="flat"
                  rounded="lg"
                  class="font-weight-bold table-action-btn px-2"
                  prepend-icon="mdi-check-circle-outline"
                  @click="$emit('approve-order', item)"
                  title="اعتماد وجدولة طلب الطباعة"
                >
                  تأكيد واعتماد
                </v-btn>
                <v-btn
                  size="small"
                  density="compact"
                  icon="mdi-keyboard-return"
                  color="warning"
                  variant="tonal"
                  rounded="lg"
                  class="table-action-icon-btn ms-1"
                  @click="$emit('return-order', item)"
                  title="إرجاع الطلب للتعديل"
                />
              </template>
            </template>
          </div>
        </template>
      </template>
    </custom-data-table>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  items: any
  getData: (params?: any) => Promise<any>
  headers: any[]
  loading?: boolean
  selectedRows: any[]
  subTab: string
  pendingAndActiveOrdersCount: number
  scheduledExamsCount: number
  dueExamsCount: number
  completedExamsCount: number
  cancelledExamsCount: number
  allExamsCount: number
}>()

defineEmits<{
  (e: 'update:selectedRows', val: any[]): void
  (e: 'update:subTab', val: string): void
  (e: 'direct-print', item: any): void
  (e: 'open-studio', item: any): void
  (e: 'preview-manifest', item: any): void
  (e: 'approve-order', item: any): void
  (e: 'return-order', item: any): void
  (e: 'advance-schedule', item: any): void
  (e: 'cancel-order', item: any): void
  (e: 'view-history', item: any): void
}>()
</script>
