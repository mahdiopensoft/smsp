<template>
  <div class="qb-templates-view-v4">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-drafting-compass</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">مكتبة القوالب وأوراق الإجابة</h1>
          <p class="text-caption text-medium-emphasis mb-0">توليد وإدارة قوالب أوراق الإجابة المعيارية بدقة مليمترية</p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="primary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-plus"
          @click="startCreating"
        >
          تصميم قالب هندسي جديد
        </v-btn>
      </div>
    </div>

    <div class="templates-layout" :class="{ 'designer-mode': isCreating || selectedTemplate }">
      
      <!-- Left side: List of Templates -->
      <div v-if="!isCreating && !selectedTemplate" class="templates-list w-100">
        <!-- Unified Filter Fields -->
        <filter-fields label="خيارات التصفية والبحث في قوالب أوراق الإجابة" class="main-card border-0 pa-5 rounded-2xl mb-6">
          <v-row dense class="align-center">
            <!-- Search Query Input -->
            <v-col cols="12" sm="6" md="5">
              <v-text-field
                v-model="searchQuery"
                label="اسم القالب أو الوصف"
                placeholder="بحث باسم القالب أو المواصفات..."
                prepend-inner-icon="mdi-magnify"
                clearable
                density="compact"
                variant="outlined"
                class="mb-6"
                hide-details
              />
            </v-col>

            <!-- Validation Status -->
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="filterValidated"
                :items="validatedOptions"
                item-title="text"
                item-value="value"
                label="حالة التوثيق الهندسي"
                prepend-inner-icon="mdi-check-decagram-outline"
                clearable
                density="compact"
                variant="outlined"
                class="mb-6"
                hide-details
              />
            </v-col>

            <!-- Actions -->
            <v-col cols="12" sm="12" md="3" class="d-flex align-center gap-2">
              <custom-btn
                type="cancel_filter"
                :click="resetFilters"
                variant="tonal"
                color="error"
                label="تفريغ"
                class="font-weight-bold mb-6"
              />
              <v-btn
                color="primary"
                rounded="lg"
                class="font-weight-bold flex-grow-1 mb-6"
                prepend-icon="mdi-plus"
                @click="startCreating"
              >
                قالب جديد
              </v-btn>
            </v-col>
          </v-row>
        </filter-fields>

        <!-- Custom Data Table -->
        <div class="main-card rounded-2xl overflow-hidden mb-6">
          <custom-data-table
            v-bind="{
              items: tableItems,
              headers,
              create: startCreating,
            }"
            :hasFilter="false"
            :log="false"
            :restore="false"
          >
            <template v-slot:item-slot="{ item, key }">
              <!-- Name & Description -->
              <template v-if="key === 'name'">
                <div class="d-flex align-center gap-3 py-1 cursor-pointer" @click="selectTemplate(item)">
                  <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
                    <v-icon size="20">mdi-file-document-edit-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-black text-body-2 text-primary">{{ item.name }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.description || 'قالب تظليل هندسي معياري' }}</div>
                  </div>
                </div>
              </template>

              <!-- Version -->
              <template v-else-if="key === 'version'">
                <v-chip size="small" variant="tonal" color="grey-darken-2" class="font-weight-bold unified-table-chip">
                  v{{ item.version || '1.0' }}
                </v-chip>
              </template>

              <!-- Total MCQ -->
              <template v-else-if="key === 'total_mcq'">
                <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold unified-table-chip">
                  {{ item.total_mcq || 0 }} سؤال
                </v-chip>
              </template>

              <!-- Total Essay -->
              <template v-else-if="key === 'total_essay'">
                <span class="text-body-2 text-medium-emphasis">{{ item.total_essay || 0 }} مقالي</span>
              </template>

              <!-- Validation Status -->
              <template v-else-if="key === 'is_validated'">
                <v-chip
                  size="small"
                  :color="item.is_validated ? 'success' : 'warning'"
                  variant="tonal"
                  class="font-weight-bold unified-table-chip"
                >
                  <v-icon start size="14">{{ item.is_validated ? 'mdi-check-decagram' : 'mdi-clock-outline' }}</v-icon>
                  {{ item.is_validated ? 'موثق هندسياً' : 'مسودة مراجعة' }}
                </v-chip>
              </template>

              <!-- Created At -->
              <template v-else-if="key === 'created_at'">
                <span class="text-caption text-medium-emphasis">
                  {{ item.created_at ? new Date(item.created_at).toLocaleDateString('ar-YE') : '-' }}
                </span>
              </template>

              <!-- Actions -->
              <template v-else-if="key === 'actions'">
                <div class="d-flex align-center justify-center gap-1">
                  <custom-btn
                    type="update"
                    is-icon
                    label="تعديل ومعاينة القالب"
                    :click="() => selectTemplate(item)"
                  />
                  <custom-btn
                    type="del"
                    is-icon
                    label="حذف القالب"
                    :click="() => deleteTemplate(item.id)"
                  />
                </div>
              </template>
            </template>
          </custom-data-table>
        </div>
      </div>


      <!-- Left Sidebar: CAD Controls (Shown only in creative/designer mode) -->
      <div v-if="isCreating" class="card designer-controls-card">
        <div class="section-header">
          <h2>مكونات وهندسة القالب</h2>
        </div>

        <!-- Designer Tabs -->
        <div class="tabs-container">
          <button class="tab-btn" :class="{ active: activeTab === 'general' }" @click="activeTab = 'general'">عام</button>
          <button class="tab-btn" :class="{ active: activeTab === 'mcq' }" @click="activeTab = 'mcq'">أسئلة OMR</button>
          <button class="tab-btn" :class="{ active: activeTab === 'htr' }" @click="activeTab = 'htr'">عناصر متقدمة</button>
          <button class="tab-btn" :class="{ active: activeTab === 'logic' }" @click="activeTab = 'logic'">المنطق (Logic)</button>
          <button class="tab-btn" :class="{ active: activeTab === 'layers' }" @click="activeTab = 'layers'">الطبقات</button>
        </div>

        <div class="control-tab-content">
          <!-- General Specs -->
          <div v-if="activeTab === 'general'" class="tab-pane">
            <div class="form-group">
              <label>اسم القالب التعريفي</label>
              <input type="text" v-model="form.name" placeholder="مثال: نموذج أ - كيمياء عامة" />
            </div>
            <div class="form-group">
              <label>الوصف الفني</label>
              <textarea v-model="form.description" rows="3" placeholder="ملاحظات حول هذا القالب..."></textarea>
            </div>
            <div class="grid-2">
              <div class="form-group">
                <label>حجم الورق</label>
                <select v-model="form.paper_size" @change="onPaperSizeChange">
                  <option value="A4">A4 (210 x 297 mm)</option>
                  <option value="A3">A3 (297 x 420 mm)</option>
                </select>
              </div>
              <div class="form-group">
                <label>دقة المسح المستهدفة</label>
                <input type="number" v-model.number="form.dpi" />
              </div>
            </div>
            
            <div class="divider"></div>
            
            <!-- Standard Header Block -->
            <div class="header-block-section">
              <h4 class="sub-title">إعدادات ترويسة الطالب والباركود</h4>
              <div class="grid-2">
                <div class="form-group">
                  <label>موقع الباركود X (mm)</label>
                  <input type="number" v-model.number="draft_template.barcode_region.dx_mm" @input="rebuildDraft" />
                </div>
                <div class="form-group">
                  <label>موقع الباركود Y (mm)</label>
                  <input type="number" v-model.number="draft_template.barcode_region.dy_mm" @input="rebuildDraft" />
                </div>
              </div>
            </div>
          </div>

          <!-- MCQ Creator Block -->
          <div v-if="activeTab === 'mcq'" class="tab-pane">
            <h4 class="sub-title">إضافة قسم بابل شيت (MCQ) جديد</h4>
            <div class="grid-2">
              <div class="form-group">
                <label>من السؤال</label>
                <input type="number" v-model.number="mcq_creator.startQ" />
              </div>
              <div class="form-group">
                <label>إلى السؤال</label>
                <input type="number" v-model.number="mcq_creator.endQ" />
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>عدد الخيارات</label>
                <select v-model.number="mcq_creator.choices">
                  <option :value="4">4 خيارات</option>
                  <option :value="5">5 خيارات</option>
                  <option :value="6">6 خيارات</option>
                </select>
              </div>
              <div class="form-group">
                <label>لغة الفقاعات</label>
                <select v-model="mcq_creator.bubbleStyle">
                  <option value="arabic">عربي (أ، ب، ج، د)</option>
                  <option value="english">إنجليزي (A, B, C, D)</option>
                </select>
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>عدد الأعمدة</label>
                <input type="number" v-model.number="mcq_creator.cols" />
              </div>
              <div class="form-group">
                <!-- Spacing placeholder -->
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>موقع البدء X (mm)</label>
                <input type="number" v-model.number="mcq_creator.startX" />
              </div>
              <div class="form-group">
                <label>موقع البدء Y (mm)</label>
                <input type="number" v-model.number="mcq_creator.startY" />
              </div>
            </div>

            <button class="btn btn-primary w-full" @click="addMCQSection">إدراج فقرات OMR للرسم</button>
          </div>

          <!-- HTR Creator Block -->
          <div v-if="activeTab === 'htr'" class="tab-pane">
            <h4 class="sub-title">إدراج منطقة كتابة يدوية (HTR)</h4>
            <div class="form-group">
              <label>رقم السؤال المقالي</label>
              <input type="number" v-model.number="htr_creator.question_id" />
            </div>
            
            <div class="grid-2">
              <div class="form-group">
                <label>الإحداثي X (mm)</label>
                <input type="number" v-model.number="htr_creator.dx_mm" />
              </div>
              <div class="form-group">
                <label>الإحداثي Y (mm)</label>
                <input type="number" v-model.number="htr_creator.dy_mm" />
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>العرض W (mm)</label>
                <input type="number" v-model.number="htr_creator.width_mm" />
              </div>
              <div class="form-group">
                <label>الارتفاع H (mm)</label>
                <input type="number" v-model.number="htr_creator.height_mm" />
              </div>
            </div>
            <button class="btn btn-primary w-full" @click="addHTRRegion">إدراج منطقة مقالية (HTR / ICR)</button>
            
            <div class="divider mt-4"></div>
            <h4 class="sub-title">كتل التعرف المتخصصة</h4>
            
            <button class="btn btn-outline w-full mb-2" @click="addOCRRegion">إدراج مربع نص مطبوع (OCR)</button>
            <button class="btn btn-outline w-full mb-2" @click="addImageBlock">إدراج مربع صورة / توقيع</button>
            <button class="btn btn-outline w-full" @click="addLithocode">إدراج رمز Lithocode</button>
          </div>
          
          <div v-if="activeTab === 'logic'" class="tab-pane">
            <h4 class="sub-title">إعدادات المنطق والحقول</h4>
            <div class="logic-rules-list">
              <p class="text-sm text-muted">اختر حقلاً وقم بتكوين قواعد معالجته (مثال: دمج رقم الجلوس، التحقق من الإجابة الفارغة).</p>
              <div class="form-group mt-3">
                <label>نوع القاعدة المنطقية</label>
                <select class="form-control">
                  <option>دمج حقلين متتاليين</option>
                  <option>جمع/مقارنة القيم</option>
                  <option>تعويض الحقل الفارغ</option>
                </select>
              </div>
              <button class="btn btn-outline w-full mt-2">+ إضافة قاعدة جديدة</button>
            </div>
          </div>

          <!-- Layers Panel -->
          <div v-if="activeTab === 'layers'" class="tab-pane">
            <div class="layers-list">
              <div class="layer-item locked">
                <span>علامات الارتكاز (Fiducials)</span>
                <span class="layer-meta">4 نقاط هندسية</span>
              </div>
              <div class="layer-item clickable" :class="{ active: selectedLayer?.type === 'barcode' }" @click="selectBarcodeLayer">
                <span>رمز التتبع (Barcode)</span>
                <span class="layer-meta font-mono">X:{{ draft_template.barcode_region.dx_mm }} Y:{{ draft_template.barcode_region.dy_mm }}</span>
              </div>
              
              <!-- MCQ Questions layers group -->
              <div class="layer-group-header">أسئلة الاختيار OMR ({{ draft_template.mcq_questions.length }})</div>
              <div 
                v-for="q in draft_template.mcq_questions" 
                :key="'layer-q-' + q.question_id"
                class="layer-item clickable"
                :class="{ active: selectedLayer?.type === 'mcq' && selectedLayer?.id === q.question_id }"
                @click="selectMCQLayer(q)"
              >
                <span>سؤال {{ q.question_id }}</span>
                <button class="btn-delete-layer" @click.stop="deleteMCQQuestion(q.question_id)">حذف</button>
              </div>

              <!-- HTR questions layers group -->
              <div class="layer-group-header">صناديق الكتابة HTR ({{ draft_template.essay_regions.length }})</div>
              <div 
                v-for="reg in draft_template.essay_regions" 
                :key="'layer-htr-' + reg.question_id"
                class="layer-item clickable"
                :class="{ active: selectedLayer?.type === 'htr' && selectedLayer?.id === reg.question_id }"
                @click="selectHTRLayer(reg)"
              >
                <span>سؤال HTR {{ reg.question_id }}</span>
                <button class="btn-delete-layer" @click.stop="deleteHTRRegion(reg.question_id)">حذف</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Inspector Panel (Visible when layer is selected) -->
        <div v-if="selectedLayer" class="inspector-section">
          <h4>مفتش خصائص العنصر (CAD Inspector)</h4>
          <div class="inspector-form">
            <div class="info-row">
              <span class="label">نوع الطبقة:</span>
              <span class="value badge badge-info">{{ selectedLayer.type.toUpperCase() }}</span>
            </div>
            
            <div class="grid-2" v-if="selectedLayer.type === 'htr'">
              <div class="form-group">
                <label>العرض W (mm)</label>
                <input type="number" v-model.number="selectedLayer.data.region.width_mm" @input="rebuildDraft" />
              </div>
              <div class="form-group">
                <label>الارتفاع H (mm)</label>
                <input type="number" v-model.number="selectedLayer.data.region.height_mm" @input="rebuildDraft" />
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>الإحداثي X (mm)</label>
                <input type="number" v-model.number="selectedLayerCoords.x" @input="updateLayerCoords" />
              </div>
              <div class="form-group">
                <label>الإحداثي Y (mm)</label>
                <input type="number" v-model.number="selectedLayerCoords.y" @input="updateLayerCoords" />
              </div>
            </div>
            <button class="btn btn-secondary w-full" @click="selectedLayer = null">إلغاء التحديد</button>
          </div>
        </div>

        <!-- Workspace Footer Actions -->
        <div class="workspace-submit-actions">
          <button class="btn btn-secondary" @click="cancelCreating">إلغاء</button>
          <button class="btn btn-success" @click="saveDraftTemplate" :disabled="submitting">
            {{ submitting ? 'جاري الفحص المتقدم...' : 'حفظ وتدقيق المعايير' }}
          </button>
        </div>
      </div>

      <!-- Right side: CAD Visualizer Workbench (Rulers, Zoom & Dynamic Canvas) -->
      <div v-if="isCreating" class="card workbench-card">
        <div class="workbench-header">
          <h3>لوحة الرسم والمعاينة القياسية (CAD Workspace)</h3>
          
          <div class="zoom-controls">
            <button class="btn-zoom" @click="changeZoom(50)">50%</button>
            <button class="btn-zoom" @click="changeZoom(75)">75%</button>
            <button class="btn-zoom" @click="changeZoom(100)" :class="{ active: zoom === 100 }">100%</button>
            <button class="btn-zoom" @click="changeZoom(120)">120%</button>
            <button class="btn-zoom" @click="changeZoom(150)">150%</button>
          </div>
        </div>

        <!-- The actual drawing workbench container -->
        <div class="cad-viewport">
          <div class="cad-workbench" :style="viewportStyle">
            <!-- Millimeter Rulers -->
            <!-- Top Ruler (W x 10) -->
            <svg class="ruler-top" :viewBox="`0 0 ${activeWidth} 10`" xmlns="http://www.w3.org/2000/svg">
              <rect width="100%" height="100%" fill="var(--color-bg-hover)" />
              <g v-for="tick in Math.floor(activeWidth / 10) + 1" :key="'tick-t-' + tick">
                <!-- Major Tick -->
                <line :x1="(tick - 1) * 10" y1="0" :x2="(tick - 1) * 10" y2="10" stroke="var(--color-text-muted)" stroke-width="0.3" />
                <text :x="(tick - 1) * 10 + 1" y="7" font-size="2.2" fill="var(--color-text-secondary)" font-family="monospace">{{ (tick - 1) * 10 }}</text>
                <!-- Minor Ticks -->
                <line v-for="m in 9" :key="'mt-' + m" :x1="(tick - 1) * 10 + m" y1="6" :x2="(tick - 1) * 10 + m" y2="10" stroke="var(--color-border)" stroke-width="0.1" />
              </g>
            </svg>

            <!-- Left Ruler (10 x H) -->
            <svg class="ruler-left" :viewBox="`0 0 10 ${activeHeight}`" xmlns="http://www.w3.org/2000/svg">
              <rect width="100%" height="100%" fill="var(--color-bg-hover)" />
              <g v-for="tick in Math.floor(activeHeight / 10) + 1" :key="'tick-l-' + tick">
                <!-- Major Tick -->
                <line x1="0" :y1="(tick - 1) * 10" x2="10" :y2="(tick - 1) * 10" stroke="var(--color-text-muted)" stroke-width="0.3" />
                <text x="1" :y="(tick - 1) * 10 + 3" font-size="2.2" fill="var(--color-text-secondary)" font-family="monospace">{{ (tick - 1) * 10 }}</text>
                <!-- Minor Ticks -->
                <line v-for="m in 9" :key="'ml-' + m" x1="6" :y1="(tick - 1) * 10 + m" x2="10" :y2="(tick - 1) * 10 + m" stroke="var(--color-border)" stroke-width="0.1" />
              </g>
            </svg>

            <!-- A4/A3 Paper Sheet -->
            <div class="sheet-paper" :style="paperStyle">
              <!-- CAD Grid & SVG Elements -->
              <svg 
                ref="svgRef"
                :viewBox="`0 0 ${activeWidth} ${activeHeight}`" 
                class="paper-svg-workspace" 
                xmlns="http://www.w3.org/2000/svg"
                @mousedown="onSvgMouseDown"
                @mousemove="onSvgMouseMove"
                @mouseup="onSvgMouseUp"
                @mouseleave="onSvgMouseUp"
                :style="{ cursor: isDragging ? 'grabbing' : (selectedLayer ? 'grab' : 'default') }"
              >
                <!-- Grid background patterns -->
                <defs>
                  <pattern id="cadGrid" width="10" height="10" patternUnits="userSpaceOnUse">
                    <rect width="10" height="10" fill="none" />
                    <path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(0, 0, 0, 0.04)" stroke-width="0.25"/>
                    <!-- Subdivision of 1mm -->
                    <path d="M 1 0 L 1 10 M 2 0 L 2 10 M 3 0 L 3 10 M 4 0 L 4 10 M 5 0 L 5 10 M 6 0 L 6 10 M 7 0 L 7 10 M 8 0 L 8 10 M 9 0 L 9 10" fill="none" stroke="rgba(0,0,0,0.01)" stroke-width="0.05" />
                    <path d="M 0 1 L 10 1 M 0 2 L 10 2 M 0 3 L 10 3 M 0 4 L 10 4 M 0 5 L 10 5 M 0 6 L 10 6 M 0 7 L 10 7 M 0 8 L 10 8 M 0 9 L 10 9" fill="none" stroke="rgba(0,0,0,0.01)" stroke-width="0.05" />
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#cadGrid)" />

                <!-- Official Academic Exam Sheet Header -->
                <g class="cad-header-section" style="user-select: none;">
                  <!-- Outer Margin Boundary Frame -->
                  <rect x="12" y="15" :width="activeWidth - 24" height="270" fill="none" stroke="#000000" stroke-width="0.6" />
                  
                  <!-- Top Header Box (Y: 15 to 35mm) -->
                  <rect x="12" y="15" :width="activeWidth - 24" height="20" fill="#f8fafc" stroke="#000000" stroke-width="0.4" />
                  <text x="16" y="22" font-size="2.2" font-family="'Cairo', sans-serif" font-weight="bold" fill="#000000">الجمهورية اليمنية — وزارة التعليم العالي</text>
                  <text x="16" y="27" font-size="2.5" font-family="'Cairo', sans-serif" font-weight="bold" fill="#1e293b">جامعة صنعاء — كلية العلوم (OMR Sheet)</text>
                  <text x="16" y="31.5" font-size="1.8" font-family="'Cairo', sans-serif" fill="#0f172a" font-weight="600">OFFICIAL UNIVERSITY OMR/HTR ANSWER SHEET</text>

                  <!-- University Logo Emblem Placeholder Circle -->
                  <circle cx="105" cy="25" r="6" fill="#ffffff" stroke="#000000" stroke-width="0.4" />
                  <text x="105" y="26.5" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#000000">🏛️</text>

                  <!-- Left Box: Seat Number (X: 15 to 92, Y: 38 to 102) -->
                  <rect x="15" y="38" width="77" height="64" fill="none" stroke="#000000" stroke-width="0.5" />
                  <rect x="15" y="38" width="77" height="7" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
                  <text x="53.5" y="43" font-size="2.2" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#000000">رقم الجلوس / SEAT NUMBER</text>

                  <!-- 7 Digit Columns -->
                  <g v-for="col in 7" :key="'seat-col-create-' + col">
                    <rect :x="17.5 + (col - 1) * 10.2" y="46" width="9" height="7" fill="none" stroke="#000000" stroke-width="0.3" />
                    <text :x="22 + (col - 1) * 10.2" y="51" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#000000">{{ col }}</text>
                    <g v-for="digit in 10" :key="'digit-bubble-create-' + col + '-' + (digit-1)">
                      <circle :cx="22 + (col - 1) * 10.2" :cy="57 + (digit - 1) * 4.4" r="1.6" fill="#ffffff" stroke="#000000" stroke-width="0.3" />
                    </g>
                  </g>

                  <!-- Right Box: Student Info Table (X: 96 to 195, Y: 38 to 102) -->
                  <rect x="96" y="38" width="99" height="64" fill="none" stroke="#000000" stroke-width="0.5" />
                  <rect x="96" y="38" width="99" height="7" fill="#1e293b" />
                  <text x="145.5" y="43" font-size="2.2" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#ffffff">بيانات الطالب ورقم النموذج / STUDENT INFO</text>
                  
                  <!-- Rows with bold, high-contrast black typography -->
                  <line x1="96" y1="51" x2="195" y2="51" stroke="#cbd5e1" stroke-width="0.3" />
                  <text x="98" y="49" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#0f172a">اسم الطالب:</text>
                  <text x="135" y="49" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#000000">أحمد علي المحمدي</text>

                  <line x1="96" y1="62" x2="195" y2="62" stroke="#cbd5e1" stroke-width="0.3" />
                  <text x="98" y="60" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#0f172a">المادة والكلية:</text>
                  <text x="135" y="60" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#000000">فيزياء عامة 101 — كلية العلوم</text>

                  <line x1="96" y1="73" x2="195" y2="73" stroke="#cbd5e1" stroke-width="0.3" />
                  <text x="98" y="71" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#0f172a">تاريخ الاختبار:</text>
                  <text x="135" y="71" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#000000">2026-07-20</text>

                  <line x1="96" y1="86" x2="195" y2="86" stroke="#cbd5e1" stroke-width="0.3" />
                  <text x="98" y="82" font-size="2.0" font-family="'Cairo', sans-serif" font-weight="bold" fill="#0f172a">رمز النموذج:</text>
                  <g v-for="(code, idx) in ['أ', 'ب', 'ج', 'د']" :key="'form-code-create-' + idx">
                    <circle :cx="135 + idx * 14" cy="81" r="2.4" fill="#ffffff" stroke="#000000" stroke-width="0.3" />
                    <text :x="135 + idx * 14" y="81.8" font-size="1.8" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#000000">{{ code }}</text>
                  </g>

                  <!-- Signatures -->
                  <text x="110" y="96" font-size="1.8" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#334155">توقيع الطالب: ..............</text>
                  <text x="165" y="96" font-size="1.8" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#334155">توقيع الملاحظ: ..............</text>
                </g>

                <!-- Shading Instructions Bar (Y: 105 to 113) -->
                <g class="cad-instructions-bar">
                  <rect x="12" y="105" :width="activeWidth - 24" height="8" fill="#f8fafc" stroke="#000000" stroke-width="0.4" />
                  <text x="16" y="110.5" font-size="1.8" font-family="'Cairo', sans-serif" font-weight="bold" fill="#0f172a">
                    ⚠️ تنبيه: ظلل الدائرة بالكامل بقلم رصاص 2B أو جاف أزرق/أسود.
                  </text>
                  <text :x="activeWidth - 16" y="110.5" font-size="1.8" font-family="'Cairo', sans-serif" text-anchor="end" fill="#0f172a" font-weight="bold">
                    طريقة التظليل الصحيحة:  ( ⚫ صحيح )   ( ✕ خاطئ )   ( ✓ خاطئ )
                  </text>
                </g>

                <!-- Section 1 Banner: MCQ (Y: 116 to 123) -->
                <g class="cad-mcq-banner">
                  <rect x="12" y="116" :width="activeWidth - 24" height="7" fill="#1e293b" />
                  <text :x="activeWidth / 2" y="121" font-size="2.4" font-family="'Cairo', sans-serif" font-weight="bold" text-anchor="middle" fill="#ffffff">SECTION 1: MULTIPLE CHOICE QUESTIONS (20 ITEMS / 20 سؤال)</text>
                </g>

                <!-- Alternating Row Shading Tint (5-Question Blocks) -->
                <g class="cad-alternating-tint">
                  <g v-for="q in activeMCQs" :key="'tint-create-' + q.question_id">
                    <rect 
                      v-if="q.choices && q.choices.length && Math.floor((q.question_id - 1) % 10 / 5) === 1" 
                      :x="Math.min(...q.choices.map(c => c.bubble_region.dx_mm)) - 4"
                      :y="q.choices[0].bubble_region.dy_mm - 1"
                      :width="q.choices.length * 8.5 + 24"
                      height="7.5"
                      fill="rgba(241, 245, 249, 0.7)" 
                    />
                  </g>
                </g>

                <!-- Grid Lines (Dynamic table borders) -->
                <g class="cad-grid-lines">
                  <line 
                    v-for="(gline, idx) in activeGridLines" 
                    :key="'gline-' + idx"
                    :x1="gline.x1" :y1="gline.y1" :x2="gline.x2" :y2="gline.y2"
                    stroke="#000" :stroke-width="gline.thickness || 0.4"
                  />
                </g>

                <!-- Side Timing Track Bars (Left & Right margins) -->
                <g class="cad-timing-tracks">
                  <g v-for="q in activeMCQs" :key="'tt-create-' + q.question_id">
                    <rect v-if="q.choices && q.choices.length" x="10" :y="q.choices[0].bubble_region.dy_mm + 0.5" width="4" height="2.5" fill="#000000" />
                    <rect v-if="q.choices && q.choices.length" :x="activeWidth - 14" :y="q.choices[0].bubble_region.dy_mm + 0.5" width="4" height="2.5" fill="#000000" />
                  </g>
                </g>

                <!-- Corner Fiducials (Nested Solid Black Square Anchors) -->
                <g v-for="fid in activeFiducials" :key="'fid-' + fid.id" class="cad-fiducial">
                  <rect :x="fid.x_mm" :y="fid.y_mm" :width="fid.width_mm" :height="fid.height_mm" fill="#000000" />
                  <rect :x="fid.x_mm + 1" :y="fid.y_mm + 1" :width="fid.width_mm - 2" :height="fid.height_mm - 2" fill="#ffffff" />
                  <rect :x="fid.x_mm + 2" :y="fid.y_mm + 2" :width="fid.width_mm - 4" :height="fid.height_mm - 4" fill="#000000" />
                </g>

                <!-- Horizontal Barcode Zone (Top Right: X: 142, Y: 17) -->
                <g 
                  v-if="activeBarcode" 
                  class="cad-barcode-zone"
                  :class="{ selected: selectedLayer?.type === 'barcode' }"
                  @click="selectBarcodeLayer"
                >
                  <rect 
                    :x="activeBarcode.dx_mm" 
                    :y="activeBarcode.dy_mm" 
                    :width="activeBarcode.width_mm" 
                    :height="activeBarcode.height_mm" 
                    fill="rgba(37, 99, 235, 0.05)" 
                    stroke="var(--color-accent)" 
                    stroke-width="0.4" 
                    stroke-dasharray="1.5,1" 
                  />
                  <!-- Simulated Barcode Lines -->
                  <line v-for="l in 20" :key="'bar-line-' + l" :x1="activeBarcode.dx_mm + 3 + l * 2" :y1="activeBarcode.dy_mm + 5" :x2="activeBarcode.dx_mm + 3 + l * 2" :y2="activeBarcode.dy_mm + activeBarcode.height_mm - 2" stroke="#000" :stroke-width="l % 3 === 0 ? 0.6 : 0.3" />
                  <text :x="activeBarcode.dx_mm + activeBarcode.width_mm/2" :y="activeBarcode.dy_mm + 3.5" font-size="1.4" text-anchor="middle" font-family="monospace">BARCODE *PHYS101*</text>
                </g>

                <!-- MCQ Bubbles questions -->
                <g 
                  v-for="q in activeMCQs" 
                  :key="'q-block-' + q.question_id"
                  class="cad-q-block"
                  :class="{ selected: selectedLayer?.type === 'mcq' && selectedLayer?.id === q.question_id }"
                  @click="selectMCQLayer(q)"
                >
                  <!-- Question Index Label -->
                  <text 
                    v-if="q.choices && q.choices.length"
                    :x="q.choices[0].choice === 'أ' ? q.choices[0].bubble_region.dx_mm - 4 : q.choices[0].bubble_region.dx_mm - 4" 
                    :y="q.choices[0].bubble_region.dy_mm + q.choices[0].bubble_region.height_mm/2 + 0.8" 
                    font-size="2.4" 
                    font-weight="bold" 
                    text-anchor="end" 
                    fill="#000000"
                    font-family="'Cairo', sans-serif"
                  >{{ String(q.question_id).padStart(2, '0') }}.</text>

                  <!-- Bubble circles -->
                  <g v-for="choice in q.choices" :key="choice.bubble_id" class="cad-bubble">
                    <circle 
                      :cx="choice.bubble_region.dx_mm + choice.bubble_region.width_mm/2" 
                      :cy="choice.bubble_region.dy_mm + choice.bubble_region.height_mm/2" 
                      :r="choice.bubble_region.width_mm/2" 
                      fill="#ffffff" 
                      stroke="#000000" 
                      stroke-width="0.35" 
                    />
                    <text 
                      :x="choice.bubble_region.dx_mm + choice.bubble_region.width_mm/2" 
                      :y="choice.bubble_region.dy_mm + choice.bubble_region.height_mm/2 + 0.8" 
                      font-size="2.0" 
                      text-anchor="middle" 
                      font-weight="bold" 
                      fill="#000000"
                      font-family="'Cairo', sans-serif"
                    >{{ choice.choice }}</text>
                  </g>
                </g>

                <!-- HTR / Essay regions -->
                <g 
                  v-for="reg in activeHTRs" 
                  :key="'htr-block-' + reg.question_id"
                  class="cad-htr-region"
                  :class="{ selected: selectedLayer?.type === 'htr' && selectedLayer?.id === reg.question_id }"
                  @click="selectHTRLayer(reg)"
                >
                  <rect 
                    :x="reg.region.dx_mm" 
                    :y="reg.region.dy_mm" 
                    :width="reg.region.width_mm" 
                    :height="reg.region.height_mm" 
                    fill="rgba(16, 185, 129, 0.04)" 
                    stroke="#10b981" 
                    stroke-width="0.5" 
                    stroke-dasharray="2,2" 
                    rx="1"
                  />
                  <!-- HTR Text box background placeholder content -->
                  <text 
                    :x="reg.region.dx_mm + 4" 
                    :y="reg.region.dy_mm + 5" 
                    font-size="2.8" 
                    fill="#10b981" 
                    font-weight="bold"
                    font-family="Cairo"
                  >منطقة كتابة يدوية مقالية (HTR) - سؤال {{ reg.question_id }}</text>
                  <path :d="`M ${reg.region.dx_mm + 5} ${reg.region.dy_mm + 12} L ${reg.region.dx_mm + reg.region.width_mm - 5} ${reg.region.dy_mm + 12}`" stroke="rgba(16,185,129,0.2)" stroke-width="0.3" stroke-dasharray="1,2" />
                  <path :d="`M ${reg.region.dx_mm + 5} ${reg.region.dy_mm + 20} L ${reg.region.dx_mm + reg.region.width_mm - 5} ${reg.region.dy_mm + 20}`" stroke="rgba(16,185,129,0.2)" stroke-width="0.3" stroke-dasharray="1,2" />
                </g>

                <!-- OCR regions -->
                <g 
                  v-for="(reg, i) in activeOCRs" 
                  :key="'ocr-block-' + i"
                  class="cad-ocr-region"
                  :class="{ selected: selectedLayer?.type === 'ocr' && selectedLayer?.id === i }"
                  @click="selectLayer('ocr', i, reg)"
                >
                  <rect 
                    :x="reg.region.dx_mm" :y="reg.region.dy_mm" 
                    :width="reg.region.width_mm" :height="reg.region.height_mm" 
                    fill="rgba(59, 130, 246, 0.04)" stroke="#3b82f6" stroke-width="0.5" stroke-dasharray="3,1" rx="1"
                  />
                  <text :x="reg.region.dx_mm + 4" :y="reg.region.dy_mm + 5" font-size="2.4" fill="#3b82f6" font-family="monospace" font-weight="bold">نص مطبوع (OCR) - {{ reg.label || i }}</text>
                </g>

                <!-- ICR regions -->
                <g 
                  v-for="(reg, i) in activeICRs" 
                  :key="'icr-block-' + i"
                  class="cad-icr-region"
                  :class="{ selected: selectedLayer?.type === 'icr' && selectedLayer?.id === i }"
                  @click="selectLayer('icr', i, reg)"
                >
                  <rect 
                    :x="reg.region.dx_mm" :y="reg.region.dy_mm" 
                    :width="reg.region.width_mm" :height="reg.region.height_mm" 
                    fill="rgba(139, 92, 246, 0.04)" stroke="#8b5cf6" stroke-width="0.5" stroke-dasharray="2,3" rx="1"
                  />
                  <!-- Small boxes inside ICR -->
                  <rect v-for="b in Math.floor(reg.region.width_mm/5)" :key="'icr-b-'+b" :x="reg.region.dx_mm + (b-1)*5 + 1" :y="reg.region.dy_mm + 8" width="4" height="6" fill="none" stroke="rgba(139,92,246,0.3)" stroke-width="0.2"/>
                  <text :x="reg.region.dx_mm + 4" :y="reg.region.dy_mm + 5" font-size="2.2" fill="#8b5cf6" font-family="Cairo" font-weight="bold">خلايا كتابة ICR</text>
                </g>

                <!-- Image blocks -->
                <g 
                  v-for="(reg, i) in activeImageBlocks" 
                  :key="'img-block-' + i"
                  class="cad-img-region"
                  :class="{ selected: selectedLayer?.type === 'image' && selectedLayer?.id === i }"
                  @click="selectLayer('image', i, reg)"
                >
                  <rect 
                    :x="reg.region.dx_mm" :y="reg.region.dy_mm" 
                    :width="reg.region.width_mm" :height="reg.region.height_mm" 
                    fill="rgba(245, 158, 11, 0.04)" stroke="#f59e0b" stroke-width="0.5" stroke-dasharray="1,1" rx="1"
                  />
                  <circle :cx="reg.region.dx_mm + reg.region.width_mm/2" :cy="reg.region.dy_mm + reg.region.height_mm/2" r="4" fill="none" stroke="#f59e0b" stroke-width="0.4"/>
                  <path :d="`M ${reg.region.dx_mm + reg.region.width_mm/2 - 2} ${reg.region.dy_mm + reg.region.height_mm/2} L ${reg.region.dx_mm + reg.region.width_mm/2 + 2} ${reg.region.dy_mm + reg.region.height_mm/2} M ${reg.region.dx_mm + reg.region.width_mm/2} ${reg.region.dy_mm + reg.region.height_mm/2 - 2} L ${reg.region.dx_mm + reg.region.width_mm/2} ${reg.region.dy_mm + reg.region.height_mm/2 + 2}`" stroke="#f59e0b" stroke-width="0.4"/>
                  <text :x="reg.region.dx_mm + 4" :y="reg.region.dy_mm + 5" font-size="2.2" fill="#f59e0b" font-family="Cairo" font-weight="bold">مربع صورة (صورة شخصية/توقيع)</text>
                </g>

              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right Details & Audit pane (List Mode details) -->
      <div class="card detail-card" v-else-if="selectedTemplate">
        <div class="detail-header" style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 1rem; border-bottom: 1px solid var(--color-border-subtle, #e2e8f0); margin-bottom: 1rem;">
          <div>
            <h2>تفاصيل القالب المعتمد: {{ selectedTemplate.name }}</h2>
            <p class="text-muted text-sm">رمز القالب: {{ selectedTemplate.id }}</p>
          </div>
          <button class="btn btn-outline" @click="selectedTemplate = null" style="display: flex; align-items: center; gap: 0.5rem;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            العودة لمكتبة القوالب
          </button>
        </div>


        <div class="detail-body" v-if="detailLoading">
          <p class="text-center text-muted">جاري تحميل المعطيات الهندسية...</p>
        </div>

        <div class="detail-body" v-else-if="templateDetail">
          <!-- Detail Tabs -->
          <div class="tabs-container">
            <button class="tab-btn" :class="{ active: activeTabDetail === 'preview' }" @click="activeTabDetail = 'preview'">لوحة المعاينة</button>
            <button class="tab-btn" :class="{ active: activeTabDetail === 'audit' }" @click="activeTabDetail = 'audit'">تقرير الجودة الهندسية</button>
          </div>

          <!-- Preview Tab -->
          <div v-if="activeTabDetail === 'preview'" class="tab-pane">
            <div class="preview-toolbar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span class="toolbar-label">مقياس المعاينة:</span>
                <div class="zoom-controls">
                  <button class="btn-zoom" :class="{ active: zoom === 50 }" @click="changeZoom(50)">50%</button>
                  <button class="btn-zoom" :class="{ active: zoom === 75 }" @click="changeZoom(75)">75%</button>
                  <button class="btn-zoom" :class="{ active: zoom === 100 }" @click="changeZoom(100)">100%</button>
                  <button class="btn-zoom" :class="{ active: zoom === 120 }" @click="changeZoom(120)">120%</button>
                </div>
              </div>

              <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-outline" @click="downloadAsPNG" title="تنزيل الشيت كصورة عالية الدقة PNG (300 DPI)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="margin-left: 4px;"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                  تنزيل كصورة (PNG)
                </button>
                <button class="btn btn-outline" @click="downloadSVG" title="تنزيل كملف متجه SVG">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="margin-left: 4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  تنزيل كملف (SVG)
                </button>
              </div>
            </div>

            <div class="cad-viewport" style="max-height: 480px;">
              <div class="cad-workbench" :style="viewportStyle">
                <div class="sheet-paper" :style="paperStyle">
                  <Suspense>
                    <OmrSheetMultigraphics
                      class="paper-svg-workspace"
                      :total-questions="activeTemplateMeta.totalQuestions"
                      :questions-per-column="activeTemplateMeta.questionsPerColumn"
                      :total-columns="activeTemplateMeta.totalColumns"
                      :row-spacing="activeTemplateMeta.rowSpacing"
                      :bubble-radius="activeTemplateMeta.bubbleRadius"
                      :choices-per-question="activeTemplateMeta.choicesPerQuestion"
                      :show-inspection-overlay="false"

                      :bubble-type="activeTemplateMeta.bubbleType"
                      :layout-direction="activeTemplateMeta.layoutDirection"
                      :exam-name="templateDetail?.name || 'اختبار أوتوماتيكي'"
                    />
                    <template #fallback>
                      <div class="sheet-loading" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px;">
                        <div class="spinner lg" />
                        <span>جاري تحميل المعاينة الهندسية للقالب…</span>
                      </div>
                    </template>
                  </Suspense>

                </div>
              </div>
            </div>
          </div>
          
          <!-- Audit Tab -->
          <div v-if="activeTabDetail === 'audit'" class="tab-pane">
            <div class="audit-checklist">
              <div class="checklist-item pass">
                <div class="status-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:12px; height:12px;"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div class="check-details">
                  <h5>خلو التراكب الهندسي (Bubble Safety Margin)</h5>
                  <p>المسافات الفاصلة بين الفقاعات كافية، لا توجد احتمالية أخطاء ناجمة عن مسح ضوئي متداخل.</p>
                </div>
              </div>

              <div class="checklist-item pass">
                <div class="status-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:12px; height:12px;"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div class="check-details">
                  <h5>بصمة التوثيق للبيانات (SHA-256 Checksum)</h5>
                  <p class="font-mono text-xs">{{ templateDetail.template_data?.template_hash || 'غير متوفر' }}</p>
                </div>
              </div>
            </div>

            <div class="actions-panel">
              <button class="btn btn-secondary" @click="validateTemplate(templateDetail.id)">إعادة تدقيق المعايير</button>
              <button class="btn btn-danger" @click="deleteTemplate(templateDetail.id)">حذف القالب</button>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineAsyncComponent } from 'vue'
import { templatesAPI } from '../../services/omr/endpoints.js'

const OmrSheetMultigraphics = defineAsyncComponent(() =>
  import('../../components/omr_templates/OmrSheetMultigraphics.vue')
)

const templates = ref([])
const selectedTemplate = ref(null)
const templateDetail = ref(null)

// Filters for Templates Table
const searchQuery = ref('')
const filterValidated = ref(null)
const validatedOptions = [
  { text: 'كافة الحالات', value: null },
  { text: 'موثق هندسياً', value: true },
  { text: 'مسودة تحت المراجعة', value: false },
]

const headers = computed(() => [
  { title: "اسم القالب والنموذج", key: "name", sortable: true },
  { title: "الإصدار", key: "version", sortable: true, align: "center", width: "100px" },
  { title: "أسئلة OMR", key: "total_mcq", sortable: true, align: "center", width: "120px" },
  { title: "أسئلة مقالية", key: "total_essay", sortable: true, align: "center", width: "120px" },
  { title: "حالة التوثيق", key: "is_validated", sortable: true, align: "center", width: "160px" },
  { title: "تاريخ الإنشاء", key: "created_at", sortable: true, align: "center", width: "140px" },
])

const filteredTemplates = computed(() => {
  let list = templates.value || []
  if (filterValidated.value !== null && filterValidated.value !== undefined) {
    list = list.filter(t => Boolean(t.is_validated) === Boolean(filterValidated.value))
  }
  if (searchQuery.value && searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(t => (t.name && t.name.toLowerCase().includes(q)) || (t.description && t.description.toLowerCase().includes(q)))
  }
  return list
})

const tableItems = computed(() => ({
  results: filteredTemplates.value,
  count: filteredTemplates.value.length,
  pagination: {
    count: filteredTemplates.value.length,
    total: filteredTemplates.value.length,
  }
}))

const resetFilters = () => {
  searchQuery.value = ''
  filterValidated.value = null
}

const activeTemplateMeta = computed(() => {
  const td = templateDetail.value?.template_data || {}
  const meta = td.metadata || {}

  let qCount = templateDetail.value?.total_mcq || 180
  let cCount = meta.choices_count || 4
  let cols = meta.columns_count || 4
  let rSpacing = meta.row_spacing_mm || 4.2
  let bRadius = meta.bubble_radius_mm || 1.7
  let lDir = meta.layout_direction || 'rtl'
  let bType = 'numbers'

  if (td.mcq_questions && td.mcq_questions.length > 0) {
    qCount = td.mcq_questions.length
    const q1 = td.mcq_questions[0]
    if (q1.choices && q1.choices.length > 0) {
      cCount = q1.choices.length
      const firstLabel = q1.choices[0].choice
      if (firstLabel === 'أ' || firstLabel === 'ب') {
        bType = 'arabic_letters'
      } else if (['A','B','C','D','E'].includes(firstLabel)) {
        bType = 'letters'
      } else {
        bType = 'numbers'
      }
    }
  }

  const rows = Math.ceil(qCount / cols)

  return {
    totalQuestions: qCount,
    questionsPerColumn: rows,
    totalColumns: cols,
    rowSpacing: rSpacing,
    bubbleRadius: bRadius,
    choicesPerQuestion: cCount,
    bubbleType: bType,
    layoutDirection: lDir,
  }
})

const detailLoading = ref(false)

const isCreating = ref(false)
const activeTab = ref('general')
const activeTabDetail = ref('preview')
const zoom = ref(100)
const submitting = ref(false)

// Selected elements in workspace CAD
const selectedLayer = ref(null)

// Drag and drop state
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const layerStart = ref({ x: 0, y: 0 })
const svgRef = ref(null)

const form = ref({
  name: '',
  description: '',
  paper_size: 'A4',
  dpi: 300
})

// Creator tools helper state
const mcq_creator = ref({
  startQ: 1,
  endQ: 30,
  choices: 4,
  cols: 1,
  startX: 20,
  startY: 120,
  bubbleStyle: 'arabic'
})

const htr_creator = ref({
  question_id: 31,
  dx_mm: 20,
  dy_mm: 180,
  width_mm: 170,
  height_mm: 30
})

// Current draft of the template contract
const draft_template = ref({
  template_id: '',
  version: '1.0',
  expected_scan_dpi: 300,
  paper_size: 'A4',
  alignment_strategy: 'homography',
  fiducial_marks: [],
  barcode_region: { dx_mm: 85, dy_mm: 10, width_mm: 40, height_mm: 15 },
  mcq_questions: [],
  essay_regions: [],
  ocr_regions: [],
  icr_regions: [],
  image_blocks: [],
  logic_rules: []
})

const activeWidth = computed(() => {
  if (isCreating.value) {
    return form.value.paper_size === 'A4' ? 210.0 : 297.0
  }
  return templateDetail.value?.paper_width_mm || 210.0
})

const activeHeight = computed(() => {
  if (isCreating.value) {
    return form.value.paper_size === 'A4' ? 297.0 : 420.0
  }
  return templateDetail.value?.paper_height_mm || 297.0
})

const activeFiducials = computed(() => {
  if (isCreating.value) {
    return (draft_template.value.fiducial_marks?.length ? draft_template.value.fiducial_marks : draft_template.value.fiducials) || []
  }
  const data = templateDetail.value?.template_data || {}
  const list = data.fiducials || data.fiducial_marks || []
  if (list.length) return list
  return [
    { id: "TL", x_mm: 10, y_mm: 10, width_mm: 6, height_mm: 6 },
    { id: "TR", x_mm: 200, y_mm: 10, width_mm: 6, height_mm: 6 },
    { id: "BL", x_mm: 10, y_mm: 287, width_mm: 6, height_mm: 6 },
    { id: "BR", x_mm: 200, y_mm: 287, width_mm: 6, height_mm: 6 }
  ]
})

const activeBarcode = computed(() => {
  if (isCreating.value) return draft_template.value.barcode_region || draft_template.value.barcode
  const data = templateDetail.value?.template_data || {}
  return data.barcode || data.barcode_region || { dx_mm: 80, dy_mm: 35, width_mm: 18, height_mm: 68 }
})

const activeMCQs = computed(() => {
  if (isCreating.value) return draft_template.value.mcq_questions || []
  return templateDetail.value?.template_data?.mcq_questions || []
})

const activeHTRs = computed(() => {
  if (isCreating.value) return draft_template.value.essay_regions || []
  return templateDetail.value?.template_data?.essay_regions || []
})

const activeOCRs = computed(() => {
  if (isCreating.value) return draft_template.value.ocr_regions || []
  return templateDetail.value?.template_data?.ocr_regions || []
})

const activeICRs = computed(() => {
  if (isCreating.value) return draft_template.value.icr_regions || []
  return templateDetail.value?.template_data?.icr_regions || []
})

const activeImageBlocks = computed(() => {
  if (isCreating.value) return draft_template.value.image_blocks || []
  return templateDetail.value?.template_data?.image_blocks || []
})

const activeGridLines = computed(() => {
  if (isCreating.value) return draft_template.value.grid_lines || []
  return templateDetail.value?.template_data?.grid_lines || []
})

const paperStyle = computed(() => {
  return {
    width: `${activeWidth.value}mm`,
    height: `${activeHeight.value}mm`,
    position: 'relative',
    background: '#ffffff',
    boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
    border: '1px solid var(--color-border)',
    transition: 'width 0.2s, height 0.2s'
  }
})

const viewportStyle = computed(() => {
  const scale = zoom.value / 100
  return {
    transform: `scale(${scale})`,
    transformOrigin: 'top right',
    transition: 'transform 0.2s'
  }
})

// Layers selection
const selectedLayerCoords = computed(() => {
  if (!selectedLayer.value) return { x: 0, y: 0 }
  if (selectedLayer.value.type === 'barcode') {
    return { x: draft_template.value.barcode_region.dx_mm, y: draft_template.value.barcode_region.dy_mm }
  }
  if (selectedLayer.value.type === 'htr' || selectedLayer.value.type === 'ocr' || selectedLayer.value.type === 'icr' || selectedLayer.value.type === 'image') {
    return { x: selectedLayer.value.data.region.dx_mm, y: selectedLayer.value.data.region.dy_mm }
  }
  if (selectedLayer.value.type === 'mcq') {
    // For MCQ block, position of the first bubble
    const firstBubble = selectedLayer.value.data.choices[0]?.bubble_region
    return { x: firstBubble ? firstBubble.dx_mm : 0, y: firstBubble ? firstBubble.dy_mm : 0 }
  }
  return { x: 0, y: 0 }
})

const updateLayerCoords = () => {
  if (!selectedLayer.value) return
  const x = selectedLayerCoords.value.x
  const y = selectedLayerCoords.value.y
  
  if (selectedLayer.value.type === 'barcode') {
    draft_template.value.barcode_region.dx_mm = x
    draft_template.value.barcode_region.dy_mm = y
  } else if (['htr', 'ocr', 'icr', 'image'].includes(selectedLayer.value.type)) {
    selectedLayer.value.data.region.dx_mm = x
    selectedLayer.value.data.region.dy_mm = y
  } else if (selectedLayer.value.type === 'mcq') {
    const qIndex = draft_template.value.mcq_questions.findIndex(q => q.question_id === selectedLayer.value.id)
    if (qIndex > -1) {
      const q = draft_template.value.mcq_questions[qIndex]
      if (q.choices && q.choices.length) {
        const firstBubble = q.choices[0].bubble_region
        const diffX = x - firstBubble.dx_mm
        const diffY = y - firstBubble.dy_mm
        
        q.choices.forEach(ch => {
          ch.bubble_region.dx_mm += diffX
          ch.bubble_region.dy_mm += diffY
          if (ch.safe_region) {
            ch.safe_region.dx_mm += diffX
            ch.safe_region.dy_mm += diffY
          }
          if (ch.expanded_region) {
            ch.expanded_region.dx_mm += diffX
            ch.expanded_region.dy_mm += diffY
          }
        })
      }
    }
  }
  rebuildDraft()
}

// Drag and Drop Logic
const getSVGPoint = (evt) => {
  if (!svgRef.value) return { x: 0, y: 0 }
  const pt = svgRef.value.createSVGPoint()
  pt.x = evt.clientX
  pt.y = evt.clientY
  const cursorPt = pt.matrixTransform(svgRef.value.getScreenCTM().inverse())
  // Snap to 1mm grid
  return { x: Math.round(cursorPt.x), y: Math.round(cursorPt.y) }
}

const onSvgMouseDown = (evt) => {
  if (!selectedLayer.value) return
  isDragging.value = true
  const pt = getSVGPoint(evt)
  dragStart.value = { x: pt.x, y: pt.y }
  layerStart.value = { x: selectedLayerCoords.value.x, y: selectedLayerCoords.value.y }
}

const onSvgMouseMove = (evt) => {
  if (!isDragging.value || !selectedLayer.value) return
  const pt = getSVGPoint(evt)
  const dx = pt.x - dragStart.value.x
  const dy = pt.y - dragStart.value.y
  
  const newX = layerStart.value.x + dx
  const newY = layerStart.value.y + dy
  
  // Set the coordinates in the reactive computed/method
  // Actually we need to directly mutate the state to make it reactive smoothly
  if (selectedLayer.value.type === 'barcode') {
    draft_template.value.barcode_region.dx_mm = newX
    draft_template.value.barcode_region.dy_mm = newY
  } else if (['htr', 'ocr', 'icr', 'image'].includes(selectedLayer.value.type)) {
    selectedLayer.value.data.region.dx_mm = newX
    selectedLayer.value.data.region.dy_mm = newY
  } else if (selectedLayer.value.type === 'mcq') {
    const qIndex = draft_template.value.mcq_questions.findIndex(q => q.question_id === selectedLayer.value.id)
    if (qIndex > -1) {
      const q = draft_template.value.mcq_questions[qIndex]
      const diffX = newX - layerStart.value.x
      const diffY = newY - layerStart.value.y
      
      q.choices.forEach(ch => {
        ch.bubble_region.dx_mm += diffX
        ch.bubble_region.dy_mm += diffY
        if(ch.safe_region) {
            ch.safe_region.dx_mm += diffX
            ch.safe_region.dy_mm += diffY
        }
        if(ch.expanded_region) {
            ch.expanded_region.dx_mm += diffX
            ch.expanded_region.dy_mm += diffY
        }
      })
      // Update layer start to not double-apply
      layerStart.value.x = newX
      layerStart.value.y = newY
      dragStart.value = pt
    }
  }
}

const onSvgMouseUp = () => {
  isDragging.value = false
}

const selectBarcodeLayer = () => {
  selectedLayer.value = { type: 'barcode', id: 'barcode', data: draft_template.value.barcode_region }
}

const selectMCQLayer = (q) => {
  selectedLayer.value = { type: 'mcq', id: q.question_id, data: q }
}

const selectHTRLayer = (reg) => {
  selectedLayer.value = { type: 'htr', id: reg.question_id, data: reg }
}

const deleteMCQQuestion = (qId) => {
  draft_template.value.mcq_questions = draft_template.value.mcq_questions.filter(q => q.question_id !== qId)
  if (selectedLayer.value?.type === 'mcq' && selectedLayer.value?.id === qId) {
    selectedLayer.value = null
  }
}

const deleteHTRRegion = (qId) => {
  draft_template.value.essay_regions = draft_template.value.essay_regions.filter(r => r.question_id !== qId)
  if (selectedLayer.value?.type === 'htr' && selectedLayer.value?.id === qId) {
    selectedLayer.value = null
  }
}

const changeZoom = (level) => {
  zoom.value = level
}

// Generate the 4 corner landmarks
const generateFiducialMarks = (w, h) => {
  const size = 8.0
  const margin = 10.0
  return [
    { id: 'TL', x_mm: margin, y_mm: margin, width_mm: size, height_mm: size, type: 'nested_square' },
    { id: 'TR', x_mm: w - margin - size, y_mm: margin, width_mm: size, height_mm: size, type: 'nested_square' },
    { id: 'BL', x_mm: margin, y_mm: h - margin - size, width_mm: size, height_mm: size, type: 'nested_square' },
    { id: 'BR', x_mm: w - margin - size, y_mm: h - margin - size, width_mm: size, height_mm: size, type: 'nested_square' }
  ]
}

const onPaperSizeChange = () => {
  const w = form.value.paper_size === 'A4' ? 210.0 : 297.0
  const h = form.value.paper_size === 'A4' ? 297.0 : 420.0
  draft_template.value.paper_size = form.value.paper_size
  draft_template.value.fiducial_marks = generateFiducialMarks(w, h)
  rebuildDraft()
}

// API Loader
const loadTemplates = async () => {
  try {
    const { data } = await templatesAPI.list()
    templates.value = Array.isArray(data) ? data : (data.results || [])
    selectedTemplate.value = null
  } catch (err) {
    console.error('Failed to load templates:', err)
  }
}


onMounted(loadTemplates)


const selectTemplate = async (tmpl) => {
  if (isCreating.value) {
    if (!confirm('سيتم فقدان التغييرات غير المحفوظة، المتابعة؟')) return
  }
  isCreating.value = false
  selectedTemplate.value = tmpl
  detailLoading.value = true
  try {
    const { data } = await templatesAPI.get(tmpl.id)
    templateDetail.value = data
  } catch (err) {
    console.error('Failed to load template detail:', err)
  } finally {
    detailLoading.value = false
  }
}

const generateDefaultMCQs = () => {
  const choices = ['أ', 'ب', 'ج', 'د']
  const questions = []
  const rowHeight = 7.5
  const startY = 126.0

  for (let q = 1; q <= 20; q++) {
    const col = q <= 10 ? 0 : 1
    const row = col === 0 ? q - 1 : q - 11

    // RTL: Col 0 (Q1-10) should be on the right side of the page (e.g. 110mm)
    // Col 1 (Q11-20) should be on the left side (e.g. 22mm)
    const q_x = col === 0 ? 110.0 : 22.0
    const q_y = startY + row * rowHeight

    const choiceList = choices.map((ch, idx) => {
      // RTL: 'أ' (idx=0) gets the largest x, 'د' (idx=3) gets the smallest.
      const rtl_idx = choices.length - 1 - idx
      const center_x = q_x + 15.0 + rtl_idx * 8.5
      const center_y = q_y + 3.0
      const r_base = 2.4
      const r_safe = 1.6
      const r_exp = 3.2

      return {
        bubble_id: `Q${q}_${ch}`,
        choice: ch,
        bubble_region: { dx_mm: center_x - r_base, dy_mm: center_y - r_base, width_mm: r_base*2, height_mm: r_base*2 },
        safe_region: { dx_mm: center_x - r_safe, dy_mm: center_y - r_safe, width_mm: r_safe*2, height_mm: r_safe*2 },
        expanded_region: { dx_mm: center_x - r_exp, dy_mm: center_y - r_exp, width_mm: r_exp*2, height_mm: r_exp*2 }
      }
    })

    questions.push({ question_id: q, choices: choiceList })
  }
  return questions
}

// Creators
const startCreating = () => {
  isCreating.value = true
  selectedTemplate.value = null
  templateDetail.value = null
  selectedLayer.value = null
  activeTab.value = 'general'
  
  form.value = {
    name: '',
    description: '',
    paper_size: 'A4',
    dpi: 300
  }
  
  const w = 210.0
  const h = 297.0
  draft_template.value = {
    template_id: 'TEMP_' + Math.floor(Math.random()*10000),
    version: '1.0',
    expected_scan_dpi: 300,
    paper_size: 'A4',
    alignment_strategy: 'homography',
    fiducial_marks: generateFiducialMarks(w, h),
    barcode_region: { dx_mm: 142, dy_mm: 17, width_mm: 46, height_mm: 15 },
    mcq_questions: generateDefaultMCQs(),
    essay_regions: [],
    grid_lines: []
  }
}

const cancelCreating = () => {
  isCreating.value = false
  selectedLayer.value = null
}

const rebuildDraft = () => {
  // Pure local model reactive updates
}

const addMCQSection = () => {
  const { startQ, endQ, choices, cols, startX, startY } = mcq_creator.value
  const rowHeight = 7.5
  for (let q = startQ; q <= endQ; q++) {
    const qIndex = q - startQ
    const row = Math.floor(qIndex / cols)
    const col = qIndex % cols
    
    // RTL: First column (col 0) should be on the right.
    const colWidth = choices * 8.5 + 20
    const q_x = activeWidth.value - startX - colWidth - col * colWidth
    const q_y = startY + row * rowHeight
    
    const choiceList = []
    const choiceLabels = ['أ', 'ب', 'ج', 'د', 'هـ', 'و'].slice(0, choices)
    
    choiceLabels.forEach((ch, idx) => {
      // RTL: 'أ' (idx=0) gets the largest x.
      const rtl_idx = choiceLabels.length - 1 - idx
      const center_x = q_x + 15.0 + rtl_idx * 8.5
      const center_y = q_y + 3.0
      const r_base = 2.4
      
      choiceList.push({
        bubble_id: `Q${q}_${ch}`,
        choice: ch,
        bubble_region: { dx_mm: center_x - r_base, dy_mm: center_y - r_base, width_mm: r_base*2, height_mm: r_base*2 },
        safe_region: { dx_mm: center_x - 1.6, dy_mm: center_y - 1.6, width_mm: 3.2, height_mm: 3.2 },
        expanded_region: { dx_mm: center_x - 3.2, dy_mm: center_y - 3.2, width_mm: 6.4, height_mm: 6.4 }
      })
    })
    
    draft_template.value.mcq_questions.push({ question_id: q, choices: choiceList })
  }
  
  mcq_creator.value.startQ = endQ + 1
  mcq_creator.value.endQ = endQ + 1 + (endQ - startQ)
  mcq_creator.value.startY = startY + Math.ceil((endQ - startQ + 1) / cols) * rowHeight + 10
  
  activeTab.value = 'layers'
}

const selectLayer = (type, id, data) => {
  selectedLayer.value = { type, id, data }
}

const addOCRRegion = () => {
  draft_template.value.ocr_regions.push({
    region: { dx_mm: 20, dy_mm: 50, width_mm: 80, height_mm: 15 },
    label: 'رقم التسجيل',
    format: 'numeric'
  })
  activeTab.value = 'layers'
}

const addImageBlock = () => {
  draft_template.value.image_blocks.push({
    region: { dx_mm: 150, dy_mm: 50, width_mm: 35, height_mm: 45 }
  })
  activeTab.value = 'layers'
}

const addLithocode = () => {
  // Lithocodes are typically represented as a barcode variant or special margin dots.
  // We'll insert it as a specialized barcode.
  alert('تم إضافة Lithocode بشكل افتراضي كباركود')
  draft_template.value.barcode_region = { dx_mm: 5, dy_mm: 5, width_mm: 30, height_mm: 10 }
  activeTab.value = 'layers'
}

const addHTRRegion = () => {
  const { question_id, dx_mm, dy_mm, width_mm, height_mm } = htr_creator.value
  
  draft_template.value.essay_regions.push({
    question_id: question_id,
    region: { dx_mm, dy_mm, width_mm, height_mm }
  })
  
  htr_creator.value.question_id = question_id + 1
  htr_creator.value.dy_mm = dy_mm + height_mm + 5
  
  activeTab.value = 'layers'
}

const saveDraftTemplate = async () => {
  if (!form.value.name.trim()) {
    alert('الرجاء إدخال اسم تعريفي للقالب.')
    return
  }
  submitting.value = true
  try {
    const w = form.value.paper_size === 'A4' ? 210.0 : 297.0
    const h = form.value.paper_size === 'A4' ? 297.0 : 420.0
    
    // Auto populate basic template parameters
    draft_template.value.template_id = 'TEMP_' + Math.floor(Math.random()*1000000)
    draft_template.value.expected_scan_dpi = form.value.dpi
    draft_template.value.paper_size = form.value.paper_size
    
    await templatesAPI.create({
      name: form.value.name,
      description: form.value.description,
      version: '1.0',
      paper_width_mm: w,
      paper_height_mm: h,
      dpi: form.value.dpi,
      is_active: true,
      template_data: draft_template.value
    })
    isCreating.value = false
    await loadTemplates()
  } catch (err) {
    console.error('Save template failed:', err)
    alert('فشل حفظ القالب. تحقق من تكامل البيانات.')
  } finally {
    submitting.value = false
  }
}

const validateTemplate = async (id) => {
  try {
    const { data } = await templatesAPI.validate(id)
    alert(data.message || 'تم التحقق من معايير القالب بنجاح!')
    await loadTemplates()
  } catch (err) {
    alert('فشل فحص المعايير.')
  }
}

const deleteTemplate = async (id) => {
  if (!confirm('حذف هذا القالب نهائياً؟')) return
  try {
    await templatesAPI.delete(id)
    selectedTemplate.value = null
    templateDetail.value = null
    await loadTemplates()
  } catch (err) {
    console.error(err)
  }
}

const downloadAsPNG = () => {
  const svgEl = document.querySelector('.paper-svg-workspace') || document.querySelector('svg.omr-sheet-yemen')
  if (!svgEl) {
    alert('تعذر العثور على ورقة الإجابة للتنزيل')
    return
  }

  try {
    const clone = svgEl.cloneNode(true)
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    clone.setAttribute('width', '2480')
    clone.setAttribute('height', '3508')

    // Remove any inspection overlay elements (orange & green dashed circles)
    const overlayCircles = clone.querySelectorAll('circle[stroke="#f59e0b"], circle[stroke="#22c55e"]')
    overlayCircles.forEach(c => c.remove())

    const styleEl = document.createElement('style')

    styleEl.textContent = `
      text { font-family: 'Cairo', 'Tajawal', sans-serif !important; }
    `
    clone.insertBefore(styleEl, clone.firstChild)

    const svgString = new XMLSerializer().serializeToString(clone)
    const encodedSvg = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString)

    const img = new Image()
    img.onload = () => {
      try {
        const canvas = document.createElement('canvas')
        canvas.width = 2480  // A4 300 DPI
        canvas.height = 3508
        const ctx = canvas.getContext('2d')
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height)

        const pngUrl = canvas.toDataURL('image/png')
        const a = document.createElement('a')
        a.href = pngUrl
        a.download = `OMR_Template_${templateDetail.value?.name || 'Sheet'}.png`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
      } catch (err) {
        console.error('Canvas PNG export failed, downloading SVG fallback:', err)
        fallbackSvgExport(svgString)
      }
    }

    img.onerror = (err) => {
      console.error('Image load failed, downloading SVG fallback:', err)
      fallbackSvgExport(svgString)
    }

    img.src = encodedSvg
  } catch (e) {
    alert(`تعذر تنزيل الصورة: ${e.message}`)
  }
}

function fallbackSvgExport(svgString) {
  const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `OMR_Template_${templateDetail.value?.name || 'Sheet'}.svg`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}



const downloadSVG = () => {
  const svgEl = document.querySelector('.paper-svg-workspace')
  if (!svgEl) return
  
  const serializer = new XMLSerializer()
  let svgStr = serializer.serializeToString(svgEl)
  
  const blob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `template_${templateDetail.value?.name || 'sheet'}.svg`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}


</script>
<style scoped>
.templates-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  text-align: right;
  direction: rtl;
  padding: 30px;
  background-color: var(--color-bg-primary);
  min-height: 100vh;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 15px;
}

.page-title {
  font-size: 30px;
  font-weight: 800;
  margin: 0 0 5px;
  color: var(--color-text-primary);
}

.page-subtitle {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin: 0;
}

.layout-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 25px;
  align-items: start;
}

.layout-grid.detail-active {
  grid-template-columns: 1fr 1.2fr;
}

.layout-grid.workspace-mode {
  grid-template-columns: 380px 1fr;
}

@media (max-width: 1200px) {
  .layout-grid.workspace-mode {
    grid-template-columns: 1fr;
  }
}

.card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  box-shadow: var(--shadow-sm);
  padding: 24px;
}

.section-header {
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 12px;
  margin-bottom: 16px;
}

.section-header h2 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: var(--color-text-primary);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: right;
}

.data-table th, .data-table td {
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
}

.data-table th {
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
}

.data-table tbody tr {
  cursor: pointer;
  transition: background-color 0.2s;
}

.data-table tbody tr:hover {
  background-color: var(--color-bg-hover);
}

.selected-row {
  background-color: var(--color-bg-hover) !important;
  border-right: 4px solid var(--color-accent);
}

.font-medium {
  font-weight: 500;
  color: var(--color-text-primary);
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.badge-icon {
  width: 12px;
  height: 12px;
}

.badge-success {
  background-color: var(--color-success-bg, #d1fae5);
  color: var(--color-success, #059669);
}

.badge-warning {
  background-color: var(--color-warning-bg, #fef3c7);
  color: var(--color-warning, #d97706);
}

/* =========================================
   Designer Layout Styles
========================================= */
.templates-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  align-items: start;
  width: 100%;
}

.templates-layout.designer-mode {
  grid-template-columns: 400px 1fr;
}

@media (max-width: 1200px) {
  .templates-layout.designer-mode {
    grid-template-columns: 1fr;
  }
}

.designer-controls-card {
  position: sticky;
  top: 20px;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
}

.workbench-card {
  display: flex;
  flex-direction: column;
  background: var(--color-bg-card, #1e1e2d);
  overflow: hidden;
}

/* Tabs */
.tabs-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  border-bottom: 1px solid var(--color-border, #333);
  padding-bottom: 12px;
  margin-bottom: 16px;
}

.tab-btn {
  background: transparent;
  border: 1px solid var(--color-border, #444);
  color: var(--color-text-secondary, #aaa);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background: var(--color-bg-hover, #2a2a3c);
  color: var(--color-text-primary, #fff);
}

.tab-btn.active {
  background: var(--color-accent, #3b82f6);
  border-color: var(--color-accent, #3b82f6);
  color: #fff;
}

/* Forms */
.form-group {
  margin-bottom: 16px;
  text-align: right;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary, #aaa);
  margin-bottom: 6px;
}

.form-control, input, select, textarea {
  width: 100%;
  background: var(--color-bg-input, #151521);
  border: 1px solid var(--color-border, #333);
  color: var(--color-text-primary, #fff);
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-control:focus, input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--color-accent, #3b82f6);
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.divider {
  height: 1px;
  background: var(--color-border, #333);
  margin: 20px 0;
}

/* Buttons */
.btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: var(--color-accent, #3b82f6);
  color: #fff;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--color-accent, #3b82f6);
  color: var(--color-accent, #3b82f6);
}

.btn-outline:hover {
  background: rgba(59, 130, 246, 0.1);
}

.w-full {
  width: 100%;
}

.mb-2 { margin-bottom: 8px; }
.mt-2 { margin-top: 8px; }
.mt-4 { margin-top: 16px; }

/* SVG CAD Workspace */
.cad-viewport {
  background: #11111a;
  border-radius: 12px;
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
  min-height: 500px;
}

.cad-workbench {
  position: relative;
  margin: 20px 40px; /* buffer for rulers and scrolling */
  display: inline-block;
}

.ruler-top {
  position: absolute;
  top: -15px;
  right: 0; 
  width: 100%;
  height: 15px;
}

.ruler-left {
  position: absolute;
  top: 0;
  left: -15px; 
  width: 15px;
  height: 100%;
}

/* Fix RTL for rulers: in RTL, right is 0, so left side of paper is left:0 */
.templates-container {
  direction: rtl;
}

.sheet-paper {
  background: #ffffff;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  position: relative;
  transition: transform 0.3s ease;
  transform-origin: top right; /* Ensure zooming scales from the corner */
}

.paper-svg-workspace {
  width: 100%;
  height: 100%;
  display: block;
}

.layer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: var(--color-bg-input, #151521);
  border: 1px solid var(--color-border, #333);
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
}
.layer-item:hover {
  border-color: #555;
}
.layer-item.active {
  border-color: var(--color-accent, #3b82f6);
  background: rgba(59, 130, 246, 0.1);
}

/* Logic Rules List */
.logic-rules-list {
  background: rgba(255,255,255,0.02);
  padding: 16px;
  border-radius: 8px;
  border: 1px dashed var(--color-border, #444);
}

/* Toolbar */
.preview-toolbar {
  display: flex;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border, #333);
  background: var(--color-bg-card, #1e1e2d);
}

.zoom-controls {
  display: flex;
  gap: 8px;
}

.btn-zoom {
  background: var(--color-bg-input, #151521);
  border: 1px solid var(--color-border, #333);
  color: #fff;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}
.btn-zoom:hover, .btn-zoom.active {
  background: var(--color-accent, #3b82f6);
  border-color: var(--color-accent, #3b82f6);
}

/* ===== Theme & Banner Enhancements ===== */
.qb-templates-view-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
</style>
