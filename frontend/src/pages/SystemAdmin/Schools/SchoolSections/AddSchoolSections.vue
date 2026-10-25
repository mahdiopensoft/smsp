<template>
  <drawer
    :data="data"
    :getData="getData"
    click="api/academic/school-sections/"
    :items="items"
    width="850"
  >
    <template v-slot>
      <div class="pa-2">
        <!-- ── فلاتر التبعية الجغرافية (المحافظة والمديرية) - تضاف في الشاشة لأنها خارج موديل الشعبة ── -->
        <v-row dense class="mb-1">
          <!-- 1. المحافظة -->
          <v-col cols="12" sm="6" md="6">
            <auto-list
              v-model="data.governorate"
              name="Governorate"
              placeholder="اختر المحافظة *"
              label="المحافظة *"
              cols="12"
              :add="false"
              @update:model-value="onGovernorateChange"
            />
          </v-col>

          <!-- 2. المديرية -->
          <v-col cols="12" sm="6" md="6">
            <auto-list
              v-model="data.directorate"
              name="Directorate"
              :param="data.governorate"
              :placeholder="data.governorate ? 'اختر المديرية التابعة *' : 'اختر المحافظة أولاً'"
              label="المديرية *"
              cols="12"
              :add="false"
              :disabled="!data.governorate"
              @update:model-value="onDirectorateChange"
            />
          </v-col>
        </v-row>

        <!-- ── حقول الموديل الرسمية من السكرين (المدرسة، مسار الصف، العام، الاسم، الكود، السعة، إلخ) ── -->
        <v-row dense>
          <fields
            :data="data"
            url="school-sections"
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
  name: 'AddSchoolSections',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  computed: {
    fieldsAttr() {
      return {
        // حقل المدرسة من السكرين: مربوط بفلتر المحافظة والمديرية ومُعطل حتى اختيارهما معاً
        organization: {
          cols: 12,
          md: 12,
          param: {
            institution_type: 'school',
            governorate: this.data?.governorate || undefined,
            directorate: this.data?.directorate || undefined,
          },
          disabled: !this.data?.governorate || !this.data?.directorate,
          placeholder: (!this.data?.governorate)
            ? 'اختر المحافظة أولاً...'
            : (!this.data?.directorate)
            ? 'اختر المديرية أولاً...'
            : 'اختر المدرسة *',
        },
        class_track: {
          cols: 12,
          md: 6,
        },
        academic_year: {
          cols: 12,
          md: 6,
        },
        name_ar: {
          cols: 12,
          md: 6,
        },
        name_en: {
          cols: 12,
          md: 6,
        },
        section_code: {
          cols: 12,
          md: 4,
        },
        gender: {
          cols: 12,
          md: 4,
        },
        max_capacity: {
          cols: 12,
          md: 4,
        },
        is_active: {
          cols: 12,
          md: 12,
        },
      };
    },
  },
  watch: {
    data: {
      immediate: true,
      handler(val) {
        if (!val) return;
        // القيم الافتراضية عند الإضافة
        if (val.is_active === undefined) {
          val.is_active = true;
        }
        if (val.gender === undefined) {
          val.gender = 1;
        }
        if (val.max_capacity === undefined) {
          val.max_capacity = 35;
        }

        // عند التعديل: إذا كانت المدرسة محددة والمحافظة/المديرية غير معبأة
        if (val.organization && (!val.governorate || !val.directorate)) {
          this.resolveOrgHierarchy(val.organization);
        }
      },
    },
  },
  methods: {
    onGovernorateChange() {
      if (this.data) {
        this.data.directorate = null;
        this.data.organization = null;
      }
    },
    onDirectorateChange() {
      if (this.data) {
        this.data.organization = null;
      }
    },
    async resolveOrgHierarchy(orgId) {
      if (!orgId) return;
      try {
        const res = await shared.getData({
          path: `api/academic/organizations/${orgId}/`,
        });
        const org = res?.data || res;
        if (org && this.data) {
          if (org.parent_id && !this.data.directorate) {
            this.data.directorate = org.parent_id;
          }
          if (org.parent?.parent_id && !this.data.governorate) {
            this.data.governorate = org.parent.parent_id;
          }
        }
      } catch (e) {
        // Fallback silently
      }
    },
  },
};
</script>
