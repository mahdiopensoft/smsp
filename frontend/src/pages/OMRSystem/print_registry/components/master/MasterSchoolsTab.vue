<template>
  <custom-data-table
    :key="'schools-tbl-' + filteredCount + '-' + filterKey"
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
    :search="false"
    class="bg-transparent"
  >
    <template v-slot:item-slot="{ item, key, index }">
      <template v-if="key === 'numbering'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
        </div>
      </template>

      <template v-else-if="key === 'name'">
        <div class="d-flex align-center py-2" style="min-width: 280px;">
          <v-avatar color="indigo" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
            <v-icon color="indigo" size="20">mdi-school-outline</v-icon>
          </v-avatar>
          <div>
            <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.name }}</div>
          </div>
        </div>
      </template>

      <template v-else-if="key === 'institution_type'">
        <div class="d-flex justify-center align-center">
          <v-chip size="x-small" :color="item.institution_type === 'university' ? 'purple' : (item.institution_type === 'institute' ? 'amber' : 'primary')" variant="tonal" class="font-weight-bold">
            {{ item.institution_type === 'university' ? 'جامعي' : (item.institution_type === 'institute' ? 'مهني/معهد' : 'مدرسي') }}
          </v-chip>
        </div>
      </template>

      <template v-else-if="key === 'directorate_name'">
        <div class="d-flex justify-center align-center">
          <span class="text-body-2">{{ item.directorate_name }} • {{ item.governorate_name }}</span>
        </div>
      </template>

      <template v-else-if="key === 'subject_name'">
        <div class="d-flex align-center justify-center flex-wrap gap-1 py-1" style="min-width: 150px;">
          <template v-if="item.subjects && item.subjects.length > 0">
            <v-chip
              v-for="(subj, sIdx) in item.subjects.slice(0, 2)"
              :key="sIdx"
              size="x-small"
              color="teal"
              variant="tonal"
              class="font-weight-bold"
            >
              {{ subj }}
            </v-chip>
            <v-tooltip v-if="item.subjects.length > 2" location="top">
              <template #activator="{ props: tProps }">
                <v-chip
                  v-bind="tProps"
                  size="x-small"
                  color="primary"
                  variant="flat"
                  class="font-weight-bold cursor-pointer"
                  @click.stop="$emit('open-exams-dialog', item)"
                >
                  +{{ item.subjects.length - 2 }}
                </v-chip>
              </template>
              <span>{{ item.subjects.slice(2).join('، ') }}</span>
            </v-tooltip>
          </template>
          <span v-else class="text-caption text-medium-emphasis">{{ item.subject_name || '—' }}</span>
        </div>
      </template>

      <template v-else-if="key === 'exams_count'">
        <div class="d-flex justify-center align-center">
          <v-tooltip location="top" text="انقر لمعاينة قائمة الاختبارات والمواد لهذا المركز">
            <template #activator="{ props }">
              <v-chip
                v-bind="props"
                size="small"
                color="primary"
                variant="tonal"
                class="font-weight-bold cursor-pointer elevation-0"
                prepend-icon="mdi-format-list-bulleted"
                @click.stop="$emit('open-exams-dialog', item)"
              >
                {{ item.exams_count }} اختبار
              </v-chip>
            </template>
          </v-tooltip>
        </div>
      </template>

      <template v-else-if="key === 'total_students'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-subtitle-2">{{ item.total_students }} طالب</span>
        </div>
      </template>

      <template v-else-if="key === 'printed_count'">
        <div class="d-flex justify-center align-center">
          <span class="font-weight-bold text-indigo">{{ item.printed_count || 0 }} ورقة</span>
        </div>
      </template>

      <template v-else-if="key === 'printed_rate'">
        <div class="d-flex align-center justify-center gap-2 px-1">
          <v-progress-linear
            :model-value="item.printed_rate || 0"
            :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'indigo')"
            height="8"
            rounded
            style="min-width: 60px; max-width: 80px;"
          />
          <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
        </div>
      </template>

      <template v-else-if="key === 'print_status'">
        <div class="d-flex justify-center align-center">
          <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
            {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
          </v-chip>
        </div>
      </template>

      <template v-else-if="key === 'actions'">
        <div class="d-flex align-center justify-center gap-1">
          <v-tooltip location="top" text="استعراض تفاصيل الاختبارات والمواد">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                size="small"
                color="secondary"
                variant="tonal"
                icon="mdi-format-list-text"
                rounded="lg"
                @click.stop="$emit('open-exams-dialog', item)"
              />
            </template>
          </v-tooltip>
          <v-btn
            size="small"
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer-check"
            @click="$emit('open-studio', item)"
          >
            سحب وطباعة
          </v-btn>
        </div>
      </template>
    </template>
  </custom-data-table>
</template>

<script setup lang="ts">
defineProps<{
  items: any
  getData: (params?: any) => Promise<any>
  headers: any[]
  loading?: boolean
  selectedRows: any[]
  filteredCount: number
  filterKey: string
}>()

defineEmits<{
  (e: 'update:selectedRows', val: any[]): void
  (e: 'open-exams-dialog', item: any): void
  (e: 'open-studio', item: any): void
}>()
</script>
