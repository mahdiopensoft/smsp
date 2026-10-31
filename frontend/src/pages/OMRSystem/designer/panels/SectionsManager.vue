<template>
  <div class="sections-manager">
    <!-- 1. Question Architecture Overview & Live Summary & Steppers -->
    <SectionQuickControls
      :total-questions-count="totalQuestionsCount"
      :total-exam-marks="totalExamMarks"
      :is-yemeni-preset="isYemeniPreset"
      :tf-count="tfCount"
      :mcq-count="mcqCount"
      :tf-section="tfSection"
      :mcq-section="mcqSection"
      @apply-ministry-40="applyMinistry40"
      @apply-ministry-50="applyYemeniMinistry50"
      @apply-ministry-60="applyMinistry60"
      @apply-institute-60="applyInstitute60"
      @apply-general-100="applyGeneral100"
      @apply-university-180="applyUniversity180"
      @adjust-tf="adjustTfCount"
      @set-tf="setTfCount"
      @adjust-mcq="adjustMcqCount"
      @set-mcq="setMcqCount"
    />

    <!-- 2. Detailed Sections List (Add / Edit / Delete / Reorder) -->
    <SectionCardList
      :config="config"
      :sections-list="sectionsList"
      :has-duplicate-section-types="hasDuplicateSectionTypes"
      :get-section-count="getSectionCount"
      @merge-sections="mergeToStandardTwoSections"
      @add-section="addNewSection"
      @remove-section="removeSection"
      @move-section="moveSection"
      @change-type="onSectionTypeChange"
      @update-count="updateSectionCount"
    />

    <!-- 3. Layout Columns, Spacing & Sizing -->
    <SectionLayoutSettings
      :config="config"
      @auto-fit-spacing="autoFitRowSpacing"
    />
  </div>
</template>

<script setup lang="ts">
import { useSectionManager } from '../composables/useSectionManager'
import SectionQuickControls from './sections/SectionQuickControls.vue'
import SectionCardList from './sections/SectionCardList.vue'
import SectionLayoutSettings from './sections/SectionLayoutSettings.vue'

const props = defineProps<{
  config: any
}>()

const {
  sectionsList,
  totalQuestionsCount,
  totalExamMarks,
  tfCount,
  mcqCount,
  tfSection,
  mcqSection,
  isYemeniPreset,
  hasDuplicateSectionTypes,
  getSectionCount,
  updateSectionCount,
  onSectionTypeChange,
  adjustTfCount,
  setTfCount,
  adjustMcqCount,
  setMcqCount,
  addNewSection,
  removeSection,
  moveSection,
  mergeToStandardTwoSections,
  applyMinistry40,
  applyYemeniMinistry50,
  applyMinistry60,
  applyUniversity180,
  applyGeneral100,
  autoFitRowSpacing,
} = useSectionManager(props)
</script>
