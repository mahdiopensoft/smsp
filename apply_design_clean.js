const fs = require('fs');

const filePath = 'frontend/src/pages/ExamGenerator/ExamCreateView.vue';
let content = fs.readFileSync(filePath, 'utf8');

// 1. Update wizardSteps with subtitles in script
const oldWizardStepsStr = `const wizardSteps = [
  { value: 1, title: 'إعدادات الاختبار', icon: 'mdi-tune-variant' },
  { value: 2, title: 'مصفوفة المعايير', icon: 'mdi-chart-pie' },
  { value: 3, title: 'المعاينة والتأكيد', icon: 'mdi-clipboard-check-outline' },
  { value: 4, title: 'استعراض وضبط النماذج', icon: 'mdi-file-document-edit-outline' },
]`;

const newWizardStepsStr = `const wizardSteps = [
  { value: 1, title: 'إعدادات الاختبار', subtitle: 'البيانات والنطاق والنماذج', icon: 'mdi-tune-variant' },
  { value: 2, title: 'مصفوفة المعايير', subtitle: 'الوحدات والصعوبة والدرجات', icon: 'mdi-chart-pie' },
  { value: 3, title: 'المعاينة والتأكيد', subtitle: 'مطابقة ملخص المواصفات', icon: 'mdi-clipboard-check-outline' },
  { value: 4, title: 'استعراض وضبط النماذج', subtitle: 'المسودة التفاعلية والتحكيم', icon: 'mdi-file-document-edit-outline' },
]`;

if (content.includes(oldWizardStepsStr)) {
  content = content.replace(oldWizardStepsStr, newWizardStepsStr);
  console.log('1. wizardSteps updated with subtitles.');
} else {
  // If CRLF
  content = content.replace(oldWizardStepsStr.replace(/\n/g, '\r\n'), newWizardStepsStr.replace(/\n/g, '\r\n'));
  console.log('1. wizardSteps (CRLF) updated with subtitles.');
}

// 2. Enhance node-icon-wrapper in template
const oldNodeContent = `<div class="node-icon-wrapper">
              <v-icon v-if="step > s.value" size="22" color="white" class="node-icon">mdi-check</v-icon>
              <v-icon v-else size="22" class="node-icon" :color="step === s.value ? 'white' : 'primary'">{{ s.icon }}</v-icon>
            </div>

            <div class="node-content">
              <span class="node-title font-weight-black">{{ s.title }}</span>
            </div>`;

const newNodeContent = `<div class="node-icon-wrapper">
              <span class="node-step-number">{{ s.value }}</span>
              <v-icon v-if="step > s.value" size="20" color="white" class="node-icon">mdi-check</v-icon>
              <v-icon v-else size="20" class="node-icon" :color="step === s.value ? 'white' : 'primary'">{{ s.icon }}</v-icon>
            </div>

            <div class="node-content text-center">
              <span class="node-title font-weight-black">{{ s.title }}</span>
              <span v-if="s.subtitle" class="node-subtitle text-caption text-medium-emphasis d-none d-md-block">{{ s.subtitle }}</span>
            </div>`;

if (content.includes(oldNodeContent)) {
  content = content.replace(oldNodeContent, newNodeContent);
  console.log('2. node-icon-wrapper updated in template.');
} else {
  content = content.replace(oldNodeContent.replace(/\n/g, '\r\n'), newNodeContent.replace(/\n/g, '\r\n'));
  console.log('2. node-icon-wrapper (CRLF) updated in template.');
}

// 3. Replace 'grey' chip
content = content.replace(
  `:color="exam.exclude_previously_used ? 'warning' : 'grey'"`,
  `:color="exam.exclude_previously_used ? 'warning' : 'primary'"`
);

// 4. Replace entire <style scoped> block
const styleStart = content.indexOf('<style scoped>');
if (styleStart !== -1) {
  const newStyles = `<style scoped>
/* ==========================================================================
   EXECUTIVE ZERO-GRAY DESIGN SYSTEM — SMSP EXAM GENERATOR
   Standards: Modern Ministerial / Academic Portal Design
   Principles: Zero dull gray, high visual hierarchy, clean geometry, 4/8px grid
   ========================================================================== */

.qb-exam-create-v4 {
  color: rgb(var(--v-theme-on-surface));
  background: radial-gradient(ellipse at 50% 0%, rgba(var(--v-theme-primary), 0.04) 0%, transparent 70%);
}

/* ==========================================================================
   1. Main Container & Structural Cards (No Gray)
   ========================================================================== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
  box-shadow: 0 10px 30px rgba(var(--v-theme-primary), 0.04) !important;
}

.section-group-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.02) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-group-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.28) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.06) !important;
}

.border-subtle {
  border: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
  background: rgb(var(--v-theme-surface));
}

.border-b-subtle {
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
}

.border-t-subtle {
  border-top: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
}

/* ==========================================================================
   2. Connected Stepper Wizard (Executive 4-Step Progress)
   ========================================================================== */
.premium-wizard-wrapper {
  position: relative;
  padding: 28px 40px;
  background: linear-gradient(180deg, rgba(var(--v-theme-primary), 0.04) 0%, rgb(var(--v-theme-surface)) 100%) !important;
  border-bottom: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
}

.premium-wizard-container {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 980px;
  margin: 0 auto;
}

.wizard-progress-track {
  position: absolute;
  top: 26px;
  left: 60px;
  right: 60px;
  height: 4px;
  background: rgba(var(--v-theme-primary), 0.12) !important;
  z-index: 1;
  border-radius: 999px;
  overflow: hidden;
}

.wizard-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, rgb(var(--v-theme-primary)) 100%) !important;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 999px;
  box-shadow: 0 0 12px rgba(var(--v-theme-primary), 0.5);
}

.premium-wizard-node {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  width: 200px;
  transition: all 0.25s ease;
  user-select: none;
}

.node-icon-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(var(--v-theme-primary), 0.18) !important;
  background: rgb(var(--v-theme-surface)) !important;
  margin-bottom: 10px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.node-step-number {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  font-size: 11px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid rgb(var(--v-theme-surface));
  transition: all 0.2s ease;
}

.node-title {
  font-size: 0.94rem;
  color: rgb(var(--v-theme-on-surface));
  display: block;
  line-height: 1.35;
  font-weight: 800;
  transition: color 0.2s ease;
}

.node-subtitle {
  font-size: 0.76rem;
  color: rgba(var(--v-theme-on-surface), 0.65);
  margin-top: 2px;
}

/* Active Node State */
.premium-wizard-node.is-active .node-icon-wrapper {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1d4ed8 100%) !important;
  box-shadow: 0 6px 20px rgba(var(--v-theme-primary), 0.35) !important;
  transform: translateY(-2px);
}
.premium-wizard-node.is-active .node-icon-wrapper .node-step-number {
  background: #ffffff;
  color: rgb(var(--v-theme-primary));
}
.premium-wizard-node.is-active .node-title {
  color: rgb(var(--v-theme-primary)) !important;
  font-weight: 900;
}

/* Completed Node State */
.premium-wizard-node.is-completed .node-icon-wrapper {
  border-color: #10b981 !important;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
}
.premium-wizard-node.is-completed .node-icon-wrapper .node-step-number {
  background: #ffffff;
  color: #10b981;
}
.premium-wizard-node.is-completed .node-title {
  color: #10b981 !important;
}

/* Pending Node State */
.premium-wizard-node.is-pending {
  opacity: 0.85;
}
.premium-wizard-node.is-pending:hover .node-icon-wrapper {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
}

/* ==========================================================================
   3. Step 1 Master-Detail Sidebar Navigation
   ========================================================================== */
.step1-sidebar-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 20px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.03) !important;
  position: sticky;
  top: 24px;
  z-index: 10;
}

.step1-nav-item {
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-theme-primary), 0.1) !important;
  border-radius: 14px !important;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.step1-nav-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  transform: translateX(-2px);
  background: rgba(var(--v-theme-primary), 0.03) !important;
}

.step1-nav-item.is-active {
  background: linear-gradient(90deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  border-right: 4px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.1) !important;
}

.step1-nav-item.has-error {
  border-color: rgba(var(--v-theme-error), 0.4) !important;
  background: rgba(var(--v-theme-error), 0.04) !important;
  border-right: 4px solid rgb(var(--v-theme-error)) !important;
}

/* ==========================================================================
   4. Segmented Institution Type Controls (Zero Gray)
   ========================================================================== */
.segmented-control {
  background: rgba(var(--v-theme-primary), 0.04) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 16px !important;
  padding: 6px !important;
}

.segmented-control-btn {
  flex: 1 1 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 11px 18px;
  border-radius: 12px;
  border: none;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.75);
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.22s ease;
  min-width: 140px;
}

.segmented-control-btn:hover {
  color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.08);
}

.segmented-control-btn.is-active {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1d4ed8 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.3) !important;
}

/* ==========================================================================
   5. Interactive Selection & Model Mode Cards (Zero Gray)
   ========================================================================== */
.selection-card,
.model-mode-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 18px !important;
  padding: 18px 22px !important;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  user-select: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.selection-card:hover,
.model-mode-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.selection-card.is-active,
.model-mode-card.is-active {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.15) !important;
}

.model-mode-card.is-active-warning {
  border-color: #f59e0b !important;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  box-shadow: 0 4px 18px rgba(245, 158, 11, 0.15) !important;
}

/* ==========================================================================
   6. Scope Level Cards Grid (Zero Gray)
   ========================================================================== */
.scope-grid {
  display: flex;
  gap: 10px;
  width: 100%;
}

.scope-card {
  flex: 1 1 0;
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 14px !important;
  padding: 14px 10px !important;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease !important;
  user-select: none;
  min-width: 100px;
}

.scope-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(var(--v-theme-primary), 0.08) !important;
}

.scope-card.is-active {
  border-color: rgb(var(--v-theme-primary)) !important;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.18) !important;
}

/* ==========================================================================
   7. Matrix Specification Tabs & Navigation (Step 2)
   ========================================================================== */
.matrix-tabs-bar {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.04) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border-bottom: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  padding: 8px !important;
  gap: 8px !important;
}

.matrix-tab-btn {
  border-radius: 14px !important;
  border: 1.5px solid transparent !important;
  background: transparent !important;
  color: rgba(var(--v-theme-on-surface), 0.7) !important;
  font-weight: 800 !important;
  font-size: 0.92rem !important;
  min-width: 170px !important;
  padding: 12px 18px !important;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.matrix-tab-btn:hover {
  color: rgb(var(--v-theme-primary)) !important;
  background: rgba(var(--v-theme-primary), 0.06) !important;
}

.matrix-tab-btn.is-active {
  background: rgb(var(--v-theme-surface)) !important;
  border-color: rgba(var(--v-theme-primary), 0.28) !important;
  color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.12) !important;
}

.executive-table {
  background: rgb(var(--v-theme-surface)) !important;
}

.table-header-row {
  background: rgba(var(--v-theme-primary), 0.06) !important;
}

/* ==========================================================================
   8. Units Distribution Tab Executive Styles (Zero Gray)
   ========================================================================== */
.units-tab-header {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.06) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.16) !important;
  border-radius: 18px !important;
  padding: 18px 24px !important;
}

.units-header-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(var(--v-theme-primary), 0.12) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.12);
}

.model-groups-selector-hub {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.06) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.18) !important;
  border-radius: 18px !important;
  padding: 18px 22px !important;
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.04) !important;
}

.hub-bullet-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
  box-shadow: 0 0 8px rgba(var(--v-theme-primary), 0.6);
}

.group-pills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
}

.group-switch-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.16) !important;
  border-radius: 14px !important;
  padding: 12px 16px !important;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  user-select: none;
}

.group-switch-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(var(--v-theme-primary), 0.08) !important;
}

.group-switch-pill.is-active {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.14) 0%, rgba(var(--v-theme-primary), 0.04) 100%) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.22) !important;
}

.group-pill-title {
  font-size: 0.94rem;
  color: rgb(var(--v-theme-on-surface));
}

.pill-percentage-badge {
  padding: 3px 10px;
  border-radius: 8px;
  font-size: 0.8rem;
  display: inline-flex;
  align-items: center;
}

.pill-percentage-badge.is-complete {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.pill-percentage-badge.is-pending {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.active-group-hero-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12) 0%, rgba(var(--v-theme-primary), 0.03) 60%, rgb(var(--v-theme-surface)) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.2) !important;
  border-right: 5px solid rgb(var(--v-theme-primary)) !important;
  border-radius: 18px !important;
  padding: 18px 24px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.active-group-hero-avatar {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, #1d4ed8 100%) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.35);
  flex-shrink: 0;
}

.hero-total-badge {
  border: 1px solid transparent;
}

.hero-total-badge.badge-success {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.hero-total-badge.badge-warning {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.3);
  color: #f59e0b;
}

.modern-unit-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.modern-unit-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateY(-2px);
}

.modern-unit-card::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: rgb(var(--v-theme-primary));
  opacity: 0.85;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.modern-unit-card.is-excluded {
  background: rgba(var(--v-theme-error), 0.04) !important;
  border-color: rgba(var(--v-theme-error), 0.25) !important;
  opacity: 0.8;
}

.modern-unit-card.is-excluded::before {
  background: rgb(var(--v-theme-error));
}

.unit-stepper-box {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14);
  border-radius: 12px;
  padding: 4px 6px;
}

.unit-percentage-display {
  min-width: 62px;
  text-align: center;
  font-size: 1.05rem;
  font-weight: 800;
  color: rgb(var(--v-theme-primary));
  padding: 2px 6px;
  border-radius: 8px;
  background: rgba(var(--v-theme-primary), 0.08);
}

.unit-percentage-display.is-zero {
  color: rgba(var(--v-theme-on-surface), 0.5);
  background: transparent;
}

.unit-percentage-display.is-excluded {
  color: rgb(var(--v-theme-error));
}

.term-header-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-right: 4px solid rgb(var(--v-theme-primary)) !important;
  padding: 10px 18px !important;
  border-radius: 14px !important;
}

/* ==========================================================================
   9. Exam Total Marks Command Center & Question Types Cards (Zero Gray)
   ========================================================================== */
.exam-total-marks-card {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.2) !important;
  border-right: 5px solid rgb(var(--v-theme-primary)) !important;
  border-radius: 18px !important;
  padding: 18px 24px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.06) !important;
}

.total-marks-icon-box {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: rgba(245, 158, 11, 0.12) !important;
  border: 1.5px solid rgba(245, 158, 11, 0.3) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.score-input-wrapper {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25) !important;
}

.score-number-input {
  width: 64px;
  text-align: center;
  font-size: 1.2rem;
  font-weight: 900;
  color: rgb(var(--v-theme-primary));
  outline: none;
  border: none;
  background: transparent;
}

.modern-type-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
}

.modern-type-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateY(-2px);
}

.modern-type-card::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 4px;
  background: rgb(var(--v-theme-primary));
  opacity: 0.85;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.type-metrics-bar {
  background: rgba(var(--v-theme-primary), 0.04) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.12) !important;
  border-radius: 12px;
  padding: 8px 14px;
}

/* ==========================================================================
   10. Step 3 Executive KPI Certification Cards
   ========================================================================== */
.kpi-cert-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-radius: 18px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02) !important;
}

.kpi-cert-card:hover {
  transform: translateY(-3px);
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.kpi-title {
  font-size: 1rem;
  color: rgb(var(--v-theme-on-surface));
}

.kpi-metric {
  font-size: 1.6rem;
  line-height: 1.15;
}

/* ==========================================================================
   11. Step 4: Interactive Exam Staging Styles (Zero Gray)
   ========================================================================== */
.staged-hero-banner {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.18) !important;
  border-radius: 20px !important;
  box-shadow: 0 6px 24px rgba(var(--v-theme-primary), 0.05) !important;
}

.staged-hero-icon-box {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: rgba(var(--v-theme-primary), 0.12) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25) !important;
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.12);
}

.shadow-success {
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35) !important;
}

.staged-nav-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-radius: 14px !important;
  padding: 9px 18px !important;
  cursor: pointer;
  transition: all 0.22s ease !important;
  display: flex;
  align-items: center;
  gap: 8px;
}

.staged-nav-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(var(--v-theme-primary), 0.08);
}

.staged-nav-pill.is-active {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.18) !important;
}

.staged-version-pill {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-radius: 14px !important;
  padding: 8px 16px !important;
  cursor: pointer;
  transition: all 0.22s ease !important;
  display: flex;
  align-items: center;
  gap: 8px;
}

.staged-version-pill:hover {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  transform: translateY(-2px);
}

.staged-version-pill.is-active {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12) 0%, rgba(var(--v-theme-primary), 0.04) 100%) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.2) !important;
}

.staged-question-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.14) !important;
  border-right: 5px solid rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.staged-question-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateY(-1px);
}

.staged-option-item {
  background: rgba(var(--v-theme-primary), 0.03) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
  transition: all 0.2s ease;
}

.staged-option-item:hover {
  background: rgba(var(--v-theme-primary), 0.06) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
}

.staged-option-item.is-correct-option {
  background: rgba(16, 185, 129, 0.08) !important;
  border: 1.5px solid #10b981 !important;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.14);
}

/* ==========================================================================
   12. Sticky Wizard Footer
   ========================================================================== */
.wizard-footer {
  backdrop-filter: blur(12px) !important;
  background: rgba(var(--v-theme-surface), 0.96) !important;
  border-top: 1.5px solid rgba(var(--v-theme-primary), 0.12) !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .premium-wizard-wrapper {
    padding: 16px 12px;
  }
  .premium-wizard-container {
    flex-wrap: wrap;
    gap: 12px;
  }
  .wizard-progress-track {
    display: none;
  }
  .premium-wizard-node {
    width: 48%;
  }
}
</style>`;

  content = content.slice(0, styleStart) + newStyles;
  console.log('4. Style block replaced cleanly.');
}

fs.writeFileSync(filePath, content, 'utf8');
console.log('ExamCreateView.vue design upgrade applied cleanly!');

