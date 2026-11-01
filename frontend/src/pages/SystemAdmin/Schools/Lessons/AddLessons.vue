<template>
  <drawer
    :data="data"
    :getData="getData"
    click="api/academic/school-lessons/"
    :items="items"
    width="850"
  >
    <template v-slot>
      <div class="pa-2">
        <!-- ── فلاتر التبعية الأكاديمية المتسلسلة (مرحلة -> صف ومسار -> مادة -> فصل -> وحدة) ── -->
        <v-card variant="tonal" color="primary" class="pa-4 mb-4 rounded-xl border">
          <div class="d-flex align-center mb-3">
            <v-icon color="primary" class="me-2" size="20">mdi-filter-variant</v-icon>
            <span class="text-subtitle-2 font-weight-bold text-primary">
              تحديد المسار والوحدة الدراسية للدرس
            </span>
          </div>

          <v-row dense>
            <!-- 1. المرحلة الدراسية -->
            <v-col cols="12" sm="6" md="4">
              <auto-list
                v-model="data.stage"
                name="Stage"
                placeholder="اختر المرحلة الدراسية *"
                label="المرحلة الدراسية *"
                cols="12"
                :add="false"
                @update:model-value="onStageChange"
              />
            </v-col>

            <!-- 2. الصف والمسار -->
            <v-col cols="12" sm="6" md="4">
              <auto-list
                v-model="data.class_track"
                name="ClassTrackByStage"
                :param="data.stage"
                :placeholder="data.stage ? 'اختر الصف والمسار *' : 'اختر المرحلة أولاً'"
                label="الصف والمسار *"
                cols="12"
                :add="false"
                :disabled="!data.stage"
                @update:model-value="onClassTrackChange"
              />
            </v-col>

            <!-- 3. المادة الدراسية -->
            <v-col cols="12" sm="6" md="4">
              <auto-list
                v-model="data.subject"
                name="SubjectByClassTrack"
                :param="data.class_track"
                :placeholder="data.class_track ? 'اختر المادة الدراسية *' : 'اختر الصف والمسار أولاً'"
                label="المادة الدراسية *"
                cols="12"
                :add="false"
                :disabled="!data.class_track"
                @update:model-value="onSubjectChange"
              />
            </v-col>

            <!-- 4. الفصل الدراسي -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.semester"
                name="Semester"
                placeholder="اختر الفصل الدراسي (اختياري لتصفية الوحدات)"
                label="الفصل الدراسي"
                cols="12"
                :add="false"
                @update:model-value="onSemesterChange"
              />
            </v-col>

            <!-- 5. الوحدة الدراسية -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.unit"
                name="SchoolUnit"
                :param="unitParam"
                :placeholder="data.subject ? 'اختر الوحدة الدراسية *' : 'اختر المادة الدراسية أولاً'"
                label="الوحدة الدراسية *"
                cols="12"
                :add="false"
                :disabled="!data.subject"
              />
            </v-col>
          </v-row>
        </v-card>

        <!-- ── الحقول الرسمية من السكرين (اسم الدرس، الترتيب، الحالة) ── -->
        <v-row dense>
          <fields
            :data="data"
            url="lessons"
            :attr="fieldsAttr"
          />
        </v-row>
      </div>
    </template>
  </drawer>
</template>

<script>
import shared from "external-components";

export default {
  name: 'AddLessons',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  computed: {
    unitParam() {
      const p = {};
      if (this.data?.subject) p.school_subject = this.data.subject;
      if (this.data?.class_track) p.class_track = this.data.class_track;
      if (this.data?.semester) p.semester = this.data.semester;
      return Object.keys(p).length ? p : null;
    },
    fieldsAttr() {
      return {
        // إخفاء حقلي المادة والوحدة من fields لأنهما معروضان أعلاه ضمن الفلاتر المتسلسلة
        subject: {
          depend: false,
        },
        unit: {
          depend: false,
        },
        name_ar: {
          cols: 12,
          md: 6,
        },
        name_en: {
          cols: 12,
          md: 6,
        },
        order: {
          cols: 12,
          md: 6,
        },
        is_active: {
          cols: 12,
          md: 6,
        },
      };
    },
  },
  watch: {
    data: {
      immediate: true,
      handler(val) {
        if (!val) return;
        if (val.is_active === undefined) {
          val.is_active = true;
        }
        if (val.order === undefined) {
          val.order = 1;
        }
        if (val.subject && !val.school_subject) {
          val.school_subject = val.subject;
        }

        // عند التعديل: إذا كانت الوحدة محددة ولكن الفلاتر الأبوية فارغة
        if (val.unit && (!val.stage || !val.class_track || !val.subject)) {
          this.resolveUnitHierarchy(val.unit);
        }
      },
    },
  },
  methods: {
    onStageChange() {
      if (this.data) {
        this.data.class_track = null;
        this.data.subject = null;
        this.data.school_subject = null;
        this.data.unit = null;
      }
    },
    onClassTrackChange() {
      if (this.data) {
        this.data.subject = null;
        this.data.school_subject = null;
        this.data.unit = null;
      }
    },
    onSubjectChange(val) {
      if (this.data) {
        this.data.subject = val;
        this.data.school_subject = val;
        this.data.unit = null;
      }
    },
    onSemesterChange() {
      if (this.data) {
        this.data.unit = null;
      }
    },
    async resolveUnitHierarchy(unitId) {
      if (!unitId || !this.data) return;
      try {
        const res = await shared.getData({
          path: `api/academic/school-units/${unitId}/`,
        });
        const unit = res?.data || res;
        if (unit && this.data) {
          if (!this.data.semester && unit.semester) {
            this.data.semester = unit.semester;
          }
          if (!this.data.subject) {
            this.data.subject = unit.school_subject || unit.class_subject?.school_subject || null;
            this.data.school_subject = this.data.subject;
          }
          if (!this.data.class_track && unit.class_subject?.class_track) {
            this.data.class_track = unit.class_subject.class_track;
          }
          if (!this.data.stage && unit.class_subject?.class_track_details?.stage) {
            this.data.stage = unit.class_subject.class_track_details.stage;
          }
        }
      } catch (e) {
        // Fallback silently
      }
    },
  },
};
</script>
