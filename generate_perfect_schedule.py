import json

# Read data from the previous script setup
from generate_perfect_schedule import modules_data

total_screens = sum(len(m["screens"]) for m in modules_data)
total_minutes = sum(sum(s["duration"] for s in m["screens"]) for m in modules_data)
total_hours = round(total_minutes / 60, 1)
total_days = round(total_hours / 7, 1)
p1_count = sum(sum(1 for s in m["screens"] if s["priority"] == "P1") for m in modules_data)
p2_count = sum(sum(1 for s in m["screens"] if s["priority"] == "P2") for m in modules_data)
p3_count = sum(sum(1 for s in m["screens"] if s["priority"] == "P3") for m in modules_data)

html_template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>خطة الفحص والاختبار الشاملة لجميع شاشات ومنظومات المشروع (147 شاشة) - وثيقة التسليم الرسمية</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

        @page {{
            size: A4 landscape;
            margin: 5mm 6mm 6mm 6mm;
            @top-center {{ content: ""; }}
            @bottom-center {{ content: ""; }}
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: 'Cairo', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 8px;
            background-color: #ffffff;
            color: #1e293b;
            font-size: 9.5px;
            line-height: 1.35;
            direction: rtl;
        }}

        /* Print-specific button & toolbar hiding */
        @media print {{
            .no-print {{
                display: none !important;
            }}
            body {{
                padding: 0 !important;
                background: #ffffff !important;
            }}
            .page-break {{
                page-break-before: always;
            }}
            tr {{
                page-break-inside: avoid;
            }}
        }}

        .print-floating-bar {{
            position: fixed;
            top: 15px;
            left: 20px;
            z-index: 9999;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-radius: 8px;
            padding: 8px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .print-btn {{
            background: #1e40af;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            font-family: 'Cairo', sans-serif;
            font-weight: 700;
            font-size: 13px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .print-btn:hover {{
            background: #1d4ed8;
        }}

        /* Header / Official Letterhead Banner */
        .official-header {{
            border: 1px solid #cbd5e1;
            border-top: 5px solid #1e40af;
            border-radius: 8px;
            padding: 12px 16px;
            background: #ffffff;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}

        .header-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }}

        .header-col-right {{
            text-align: right;
            width: 32%;
        }}
        .header-col-center {{
            text-align: center;
            width: 36%;
        }}
        .header-col-left {{
            text-align: left;
            width: 32%;
            direction: ltr;
        }}

        .inst-title-1 {{
            font-size: 13px;
            font-weight: 800;
            color: #1e3a8a;
            margin: 0;
        }}
        .inst-title-2 {{
            font-size: 11px;
            font-weight: 700;
            color: #334155;
            margin: 2px 0;
        }}
        .inst-title-3 {{
            font-size: 10px;
            font-weight: 600;
            color: #64748b;
            margin: 0;
        }}

        .doc-badge-title {{
            font-size: 16px;
            font-weight: 900;
            color: #1e40af;
            margin: 0 0 3px 0;
        }}
        .doc-badge-sub {{
            font-size: 11px;
            font-weight: 700;
            color: #0284c7;
            margin: 0;
        }}

        .meta-pill {{
            display: inline-block;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 9px;
            font-weight: 600;
            color: #334155;
            margin: 1px 0;
        }}

        /* Summary KPI Cards */
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            margin-bottom: 12px;
        }}

        .kpi-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 6px;
            text-align: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }}
        .kpi-card.blue {{ border-top: 3px solid #1e40af; }}
        .kpi-card.indigo {{ border-top: 3px solid #4f46e5; }}
        .kpi-card.emerald {{ border-top: 3px solid #059669; }}
        .kpi-card.red {{ border-top: 3px solid #dc2626; }}
        .kpi-card.cyan {{ border-top: 3px solid #0284c7; }}
        .kpi-card.slate {{ border-top: 3px solid #64748b; }}

        .kpi-val {{
            font-size: 18px;
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 2px;
        }}
        .kpi-card.blue .kpi-val {{ color: #1e40af; }}
        .kpi-card.indigo .kpi-val {{ color: #4f46e5; }}
        .kpi-card.emerald .kpi-val {{ color: #059669; }}
        .kpi-card.red .kpi-val {{ color: #dc2626; }}
        .kpi-card.cyan .kpi-val {{ color: #0284c7; }}
        .kpi-card.slate .kpi-val {{ color: #475569; }}

        .kpi-lbl {{
            font-size: 8.5px;
            font-weight: 700;
            color: #64748b;
        }}

        /* Module Summary Matrix */
        .module-summary-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 14px;
            font-size: 8.5px;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            overflow: hidden;
        }}
        .module-summary-table th {{
            background: #f1f5f9;
            color: #1e3a8a;
            font-weight: 800;
            padding: 6px 8px;
            border: 1px solid #cbd5e1;
            text-align: center;
        }}
        .module-summary-table td {{
            padding: 5px 8px;
            border: 1px solid #e2e8f0;
            color: #334155;
        }}
        .module-summary-table tr:nth-child(even) {{
            background: #f8fafc;
        }}

        /* Main Master Screens Table */
        .main-table-card {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }}

        .main-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
            table-layout: fixed;
            background: #ffffff;
        }}

        .main-table thead th {{
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 800;
            font-size: 9.5px;
            padding: 8px 4px;
            border: 1px solid #cbd5e1;
            border-top: 3px solid #1e40af;
            text-align: center;
            vertical-align: middle;
            white-space: nowrap;
        }}

        .main-table tbody td {{
            padding: 5px 5px;
            border: 1px solid #e2e8f0;
            vertical-align: middle;
            color: #1e293b;
        }}

        .main-table tbody tr:nth-child(even) {{
            background-color: #fafbfc;
        }}

        .main-table tbody tr:hover {{
            background-color: #f1f5f9;
        }}

        /* Column specific styling */
        .col-idx {{
            width: 32px;
            text-align: center;
            font-weight: 800;
            color: #1e40af;
            background: #f8fafc;
        }}
        .col-name {{
            width: 150px;
            font-weight: 800;
            color: #0f172a;
            font-size: 9.5px;
        }}
        .col-tech {{
            width: 140px;
            direction: ltr;
            text-align: left;
        }}
        .col-subsys {{
            width: 130px;
            text-align: center;
        }}
        .col-scope {{
            width: auto;
            text-align: right;
            color: #334155;
            line-height: 1.35;
        }}
        .col-role {{
            width: 110px;
            text-align: center;
            font-weight: 600;
            color: #1e293b;
            font-size: 8.5px;
        }}
        .col-prio {{
            width: 58px;
            text-align: center;
        }}
        .col-dur {{
            width: 50px;
            text-align: center;
            font-weight: 700;
            color: #166534;
        }}
        .col-criteria {{
            width: 160px;
            text-align: right;
            color: #475569;
            font-size: 8.5px;
            line-height: 1.3;
        }}

        /* Badges */
        .badge-p1 {{
            display: inline-block;
            background-color: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fca5a5;
            font-weight: 800;
            border-radius: 4px;
            padding: 2px 5px;
            font-size: 8.5px;
        }}
        .badge-p2 {{
            display: inline-block;
            background-color: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #93c5fd;
            font-weight: 800;
            border-radius: 4px;
            padding: 2px 5px;
            font-size: 8.5px;
        }}
        .badge-p3 {{
            display: inline-block;
            background-color: #f8fafc;
            color: #475569;
            border: 1px solid #cbd5e1;
            font-weight: 700;
            border-radius: 4px;
            padding: 2px 5px;
            font-size: 8.5px;
        }}

        .code-box {{
            display: block;
            background-color: #f0f9ff;
            color: #0369a1;
            border: 1px solid #bae6fd;
            border-radius: 3px;
            padding: 1px 4px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 8px;
            font-weight: 600;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .route-box {{
            display: block;
            background-color: #f8fafc;
            color: #475569;
            border: 1px solid #e2e8f0;
            border-radius: 3px;
            padding: 1px 4px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 7.5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .subsys-tag {{
            display: inline-block;
            background: #f1f5f9;
            color: #334155;
            border: 1px solid #cbd5e1;
            border-radius: 3px;
            padding: 2px 5px;
            font-weight: 700;
            font-size: 8px;
        }}

        .dur-tag {{
            display: inline-block;
            background: #f0fdf4;
            color: #15803d;
            border: 1px solid #bbf7d0;
            border-radius: 3px;
            padding: 2px 4px;
            font-weight: 800;
            font-size: 8.5px;
        }}

        /* Module Section Divider Row */
        .module-divider-row {{
            background: #e2e8f0 !important;
            border-top: 2px solid #1e40af !important;
            border-bottom: 1px solid #cbd5e1 !important;
        }}
        .module-divider-cell {{
            padding: 6px 10px !important;
            font-weight: 900 !important;
            font-size: 10.5px !important;
            color: #1e3a8a !important;
            text-align: right !important;
        }}
        .module-badge-num {{
            display: inline-block;
            background: #1e40af;
            color: #ffffff;
            border-radius: 3px;
            padding: 1px 6px;
            margin-left: 6px;
            font-size: 9px;
        }}

        /* Signatures block */
        .signatures-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-top: 14px;
            margin-bottom: 10px;
            page-break-inside: avoid;
        }}
        .sig-card {{
            border: 1px solid #cbd5e1;
            border-top: 3px solid #1e40af;
            border-radius: 6px;
            padding: 10px;
            background: #ffffff;
            text-align: center;
        }}
        .sig-role {{
            font-size: 9.5px;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 4px;
        }}
        .sig-name {{
            font-size: 8.5px;
            color: #64748b;
            margin-bottom: 22px;
        }}
        .sig-line {{
            border-bottom: 1px dashed #94a3b8;
            margin-bottom: 4px;
        }}
        .sig-date {{
            font-size: 8px;
            color: #94a3b8;
        }}
    </style>
</head>
<body>

    <div class="print-floating-bar no-print">
        <button class="print-btn" onclick="window.print()">
            🖨️ طباعة الخطة الرسمية (أو حفظ بصيغة PDF)
        </button>
        <span style="font-size: 11px; color: #475569; font-weight: 600;">
            مقاس A4 أفقي Landscape — تم التنسيق بدون ألوان سوداء لتوفير الحبر وتسهيل القراءة الرسمية
        </span>
    </div>

    <!-- Official Header -->
    <div class="official-header">
        <div class="header-top-row">
            <div class="header-col-right">
                <div class="inst-title-1">الجمهورية اليمنية</div>
                <div class="inst-title-2">وزارة التربية والتعليم والبحث العلمي</div>
                <div class="inst-title-3">قطاع المناهج والتوجيه والتقويم — الإدارة العامة للاختبارات المركزية</div>
            </div>
            <div class="header-col-center">
                <div class="doc-badge-title">وثيقة خطة وجدول فحص واختبار شاشات المنظومة</div>
                <div class="doc-badge-sub">مشروع بنك الأسئلة الموحد وإدارة الامتحانات والتصحيح الآلي (OMR)</div>
            </div>
            <div class="header-col-left">
                <div class="meta-pill">وثيقة اعتماد رقم: QA-SYS-147-2026</div><br>
                <div class="meta-pill">تاريخ الإصدار: 19 نوفمبر 2026م</div><br>
                <div class="meta-pill">النطاق: 12 منظومة فرعية / 147 شاشة مكتملة</div>
            </div>
        </div>

        <!-- KPI Cards -->
        <div class="kpi-container">
            <div class="kpi-card blue">
                <div class="kpi-val">{total_screens}</div>
                <div class="kpi-lbl">إجمالي الشاشات والواجهات</div>
            </div>
            <div class="kpi-card indigo">
                <div class="kpi-val">{len(modules_data)}</div>
                <div class="kpi-lbl">المنظومات والوحدات الشاملة</div>
            </div>
            <div class="kpi-card emerald">
                <div class="kpi-val">{total_hours} <span style="font-size:11px;">ساعة</span></div>
                <div class="kpi-lbl">الزمن التقديري الإجمالي ({total_days} أيام عمل)</div>
            </div>
            <div class="kpi-card red">
                <div class="kpi-val">{p1_count}</div>
                <div class="kpi-lbl">شاشات حرجة أولوية قصوى (P1)</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-val">{p2_count}</div>
                <div class="kpi-lbl">شاشات أساسية أولوية متوسطة (P2)</div>
            </div>
            <div class="kpi-card slate">
                <div class="kpi-val">{p3_count}</div>
                <div class="kpi-lbl">شاشات مساندة وضبط (P3)</div>
            </div>
        </div>
    </div>

    <!-- Master Screen Table -->
    <div class="main-table-card">
        <table class="main-table">
            <thead>
                <tr>
                    <th class="col-idx">#</th>
                    <th class="col-name">اسم الشاشة بالعربية</th>
                    <th class="col-tech">المكون والمسار البرمجي</th>
                    <th class="col-subsys">المنظومة / الوحدة</th>
                    <th class="col-scope">نطاق وفحص الشاشة (Testing Scope)</th>
                    <th class="col-role">الدور المنفذ</th>
                    <th class="col-prio">الأولوية</th>
                    <th class="col-dur">المدة</th>
                    <th class="col-criteria">معيار القبول والنجاح</th>
                </tr>
            </thead>
            <tbody>
"""

screen_counter = 1
for m in modules_data:
    m_id = m["module_id"]
    m_name = m["name"]
    m_screens = m["screens"]
    m_dur = sum(s["duration"] for s in m_screens)
    m_hours = round(m_dur / 60, 1)

    html_template += f"""
                <tr class="module-divider-row">
                    <td colspan="9" class="module-divider-cell">
                        <span class="module-badge-num">المنظومة {m_id}</span>
                        {m_name} — ({len(m_screens)} شاشة | الزمن الإجمالي: {m_dur} دقيقة / {m_hours} ساعة)
                    </td>
                </tr>
    """

    for s in m_screens:
        p_class = "badge-p1" if s["priority"] == "P1" else ("badge-p2" if s["priority"] == "P2" else "badge-p3")
        html_template += f"""
                <tr>
                    <td class="col-idx">{screen_counter}</td>
                    <td class="col-name">{s["name"]}</td>
                    <td class="col-tech">
                        <span class="code-box">{s["code"]}</span>
                        <span class="route-box">{s["route"]}</span>
                    </td>
                    <td class="col-subsys"><span class="subsys-tag">{m_name.split('،')[0]}</span></td>
                    <td class="col-scope">{s["scope"]}</td>
                    <td class="col-role">{s["role"]}</td>
                    <td class="col-prio"><span class="{p_class}">{s["priority"]}</span></td>
                    <td class="col-dur"><span class="dur-tag">{s["duration"]} د</span></td>
                    <td class="col-criteria">{s["criteria"]}</td>
                </tr>
        """
        screen_counter += 1

html_template += f"""
            </tbody>
        </table>
    </div>

    <!-- Module Summary Table Matrix -->
    <div style="margin-top: 14px; page-break-inside: avoid;">
        <div style="font-weight: 800; font-size: 11px; color: #1e3a8a; margin-bottom: 6px;">
            📊 جدول توزيع أزمنة وأولويات الفحص حسب المنظومات الـ 12:
        </div>
        <table class="module-summary-table">
            <thead>
                <tr>
                    <th>م</th>
                    <th>المنظومة / الوحدة البرمجية</th>
                    <th>عدد الشاشات</th>
                    <th>P1 (حرجة)</th>
                    <th>P2 (أساسية)</th>
                    <th>P3 (مساندة)</th>
                    <th>إجمالي الدقائق</th>
                    <th>إجمالي الساعات</th>
                    <th>النسبة من الخطة</th>
                </tr>
            </thead>
            <tbody>
"""

for m in modules_data:
    m_id = m["module_id"]
    m_name = m["name"]
    cnt = len(m["screens"])
    p1 = sum(1 for s in m["screens"] if s["priority"] == "P1")
    p2 = sum(1 for s in m["screens"] if s["priority"] == "P2")
    p3 = sum(1 for s in m["screens"] if s["priority"] == "P3")
    mins = sum(s["duration"] for s in m["screens"])
    hrs = round(mins / 60, 1)
    pct = round((mins / total_minutes) * 100, 1)

    html_template += f"""
                <tr>
                    <td style="text-align:center; font-weight:700;">{m_id}</td>
                    <td style="font-weight:700;">{m_name}</td>
                    <td style="text-align:center; font-weight:800; color:#1e40af;">{cnt}</td>
                    <td style="text-align:center; color:#dc2626; font-weight:700;">{p1}</td>
                    <td style="text-align:center; color:#2563eb; font-weight:700;">{p2}</td>
                    <td style="text-align:center; color:#64748b; font-weight:700;">{p3}</td>
                    <td style="text-align:center; font-weight:700;">{mins} د</td>
                    <td style="text-align:center; font-weight:800; color:#059669;">{hrs} س</td>
                    <td style="text-align:center;">{pct}%</td>
                </tr>
    """

html_template += f"""
                <tr style="background:#f1f5f9; font-weight:900;">
                    <td colspan="2" style="text-align:center; color:#1e3a8a;">الإجمالي العام لكامل المنظومة</td>
                    <td style="text-align:center; color:#1e40af; font-size:10px;">{total_screens}</td>
                    <td style="text-align:center; color:#dc2626;">{p1_count}</td>
                    <td style="text-align:center; color:#2563eb;">{p2_count}</td>
                    <td style="text-align:center; color:#64748b;">{p3_count}</td>
                    <td style="text-align:center;">{total_minutes} د</td>
                    <td style="text-align:center; color:#059669; font-size:10px;">{total_hours} س</td>
                    <td style="text-align:center;">100%</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Official Signatures Block -->
    <div class="signatures-grid">
        <div class="sig-card">
            <div class="sig-role">مهندس جودة واختبار البرمجيات (QA Lead)</div>
            <div class="sig-name">فريق بناء واختبار المنظومة</div>
            <div class="sig-line"></div>
            <div class="sig-date">التوقيع: ........................ | التاريخ: ../../2026م</div>
        </div>
        <div class="sig-card">
            <div class="sig-role">رئيس قسم النظم والتطوير التقني</div>
            <div class="sig-name">فريق التطوير والبرمجة</div>
            <div class="sig-line"></div>
            <div class="sig-date">التوقيع: ........................ | التاريخ: ../../2026م</div>
        </div>
        <div class="sig-card">
            <div class="sig-role">مشرف المشروع الأكاديمي والتقني</div>
            <div class="sig-name">لجنة الإشراف والمتابعة</div>
            <div class="sig-line"></div>
            <div class="sig-date">التوقيع: ........................ | التاريخ: ../../2026م</div>
        </div>
        <div class="sig-card">
            <div class="sig-role">مدير عام الكنترول والاختبارات المركزية</div>
            <div class="sig-name">قطاع المناهج والتقويم</div>
            <div class="sig-line"></div>
            <div class="sig-date">التوقيع والختم: ........................ | التاريخ: ../../2026م</div>
        </div>
    </div>

</body>
</html>
"""

with open("docs/SCREEN_TEST_PLAN_SCHEDULE.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Saved docs/SCREEN_TEST_PLAN_SCHEDULE.html successfully!")
