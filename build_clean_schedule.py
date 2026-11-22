# -*- coding: utf-8 -*-
import json

from make_schedule import modules_data

# Filter out module 10 (Services)
clean_modules = [m for m in modules_data if "الخدمات" not in m["name"]]

for idx, m in enumerate(clean_modules, 1):
    m["module_id"] = idx

total_screens = sum(len(m["screens"]) for m in clean_modules)
total_minutes = sum(sum(s["duration"] for s in m["screens"]) for m in clean_modules)
total_hours = round(total_minutes / 60, 1)
total_days = round(total_hours / 7, 1)

p1_count = sum(sum(1 for s in m["screens"] if s["priority"] == "P1") for m in clean_modules)
p2_count = sum(sum(1 for s in m["screens"] if s["priority"] == "P2") for m in clean_modules)
p3_count = sum(sum(1 for s in m["screens"] if s["priority"] == "P3") for m in clean_modules)

html_template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>خطة الفحص والاختبار الشاملة لشاشات المنظومة ({total_screens} شاشة) - وثيقة التسليم الرسمية</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

        @page {{
            size: A4 landscape;
            margin: 5mm 6mm 5mm 6mm;
            @top-center {{ content: ""; }}
            @bottom-center {{ content: ""; }}
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: 'Cairo', 'Segoe UI', Tahoma, Arial, sans-serif;
            margin: 0;
            padding: 6px;
            background-color: #ffffff;
            color: #000000;
            font-size: 8.8px;
            line-height: 1.3;
            direction: rtl;
        }}

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
            top: 12px;
            left: 20px;
            z-index: 9999;
            background: #ffffff;
            border: 1px solid #333333;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            border-radius: 4px;
            padding: 8px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .print-btn {{
            background: #1e3a8a;
            color: #ffffff;
            border: none;
            padding: 6px 14px;
            font-family: 'Cairo', sans-serif;
            font-weight: 700;
            font-size: 13px;
            border-radius: 4px;
            cursor: pointer;
        }}
        .print-btn:hover {{
            background: #1d4ed8;
        }}

        /* ترويسة رسمية عادية وبسيطة */
        .official-header {{
            border: 1.5px solid #333333;
            border-radius: 4px;
            padding: 8px 14px;
            background: #ffffff;
            margin-bottom: 8px;
        }}

        .header-table {{
            width: 100%;
            border-collapse: collapse;
            border: none;
            margin-bottom: 6px;
        }}
        .header-table td {{
            border: none;
            padding: 1px 4px;
            vertical-align: middle;
        }}

        .inst-title-1 {{
            font-size: 13px;
            font-weight: 800;
            color: #000000;
        }}
        .inst-title-2 {{
            font-size: 11px;
            font-weight: 700;
            color: #222222;
        }}
        .inst-title-3 {{
            font-size: 9px;
            font-weight: 600;
            color: #444444;
        }}

        .doc-title-main {{
            font-size: 15px;
            font-weight: 800;
            color: #1e3a8a;
            text-align: center;
        }}
        .doc-title-sub {{
            font-size: 11px;
            font-weight: 700;
            color: #333333;
            text-align: center;
        }}

        .doc-meta {{
            font-size: 8.5px;
            line-height: 1.4;
            direction: ltr;
            text-align: left;
            color: #222222;
        }}

        /* شريط ملخص إحصائي بسيط */
        .summary-bar-table {{
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #333333;
            text-align: center;
            font-size: 8.5px;
            margin-top: 4px;
        }}
        .summary-bar-table th {{
            background: #e2e8f0;
            border: 1px solid #333333;
            padding: 3px;
            color: #000000;
            font-weight: 700;
        }}
        .summary-bar-table td {{
            border: 1px solid #333333;
            padding: 4px;
            font-weight: 700;
            color: #111111;
            background: #ffffff;
        }}

        /* تسطير الجدول الرئيسي العادي المعتمد */
        .main-schedule-table {{
            width: 100%;
            border-collapse: collapse;
            border: 1.5px solid #000000;
            font-size: 8.8px;
            background: #ffffff;
        }}

        .main-schedule-table th {{
            background-color: #f1f5f9;
            color: #000000;
            font-weight: 800;
            font-size: 9px;
            padding: 5px 3px;
            border: 1px solid #333333;
            text-align: center;
            vertical-align: middle;
        }}

        .main-schedule-table td {{
            border: 1px solid #475569;
            padding: 3px 4px;
            vertical-align: middle;
            color: #000000;
        }}

        /* تمييز صف عنوان المنظومة */
        .module-header-row td {{
            background-color: #e2e8f0 !important;
            color: #1e3a8a !important;
            font-weight: 800 !important;
            font-size: 9.5px !important;
            padding: 4px 6px !important;
            border: 1.5px solid #333333 !important;
            text-align: right !important;
        }}

        /* أعمدة الجدول */
        .col-id {{
            width: 30px;
            text-align: center;
            font-weight: 700;
        }}
        .col-title {{
            width: 160px;
            font-weight: 700;
        }}
        .col-code {{
            width: 155px;
            direction: ltr;
            text-align: left;
            font-family: Consolas, monospace;
            font-size: 8px;
        }}
        .col-subsystem {{
            width: 110px;
            text-align: center;
            font-size: 8.5px;
        }}
        .col-testing-scope {{
            width: auto;
            text-align: right;
            line-height: 1.35;
        }}
        .col-executor {{
            width: 110px;
            text-align: center;
            font-size: 8.5px;
        }}
        .col-priority {{
            width: 50px;
            text-align: center;
            font-weight: 700;
        }}
        .col-duration {{
            width: 45px;
            text-align: center;
            font-weight: 700;
        }}
        .col-acceptance {{
            width: 170px;
            text-align: right;
            font-size: 8.5px;
            line-height: 1.3;
        }}

        /* تسطير جدول التوزيع الإحصائي */
        .matrix-table {{
            width: 100%;
            border-collapse: collapse;
            border: 1.5px solid #000000;
            margin-top: 10px;
            margin-bottom: 14px;
            font-size: 9.5px;
            text-align: center;
        }}
        .matrix-table th {{
            background-color: #f1f5f9;
            border: 1px solid #333333;
            padding: 6px;
            font-weight: 800;
            color: #000000;
        }}
        .matrix-table td {{
            border: 1px solid #475569;
            padding: 6px;
            color: #000000;
        }}
        .matrix-table .total-row td {{
            background-color: #e2e8f0;
            font-weight: 800;
        }}

        /* تسطير بلوك التوقيعات */
        .signatures-table {{
            width: 100%;
            border-collapse: collapse;
            border: 1.5px solid #333333;
            margin-top: 10px;
            page-break-inside: avoid;
        }}
        .signatures-table th {{
            background: #f1f5f9;
            border: 1px solid #333333;
            padding: 6px;
            font-size: 9.5px;
            font-weight: 800;
            text-align: center;
            color: #1e3a8a;
        }}
        .signatures-table td {{
            border: 1px solid #333333;
            padding: 16px 8px;
            vertical-align: top;
            text-align: center;
            background: #ffffff;
            font-size: 9px;
            width: 25%;
        }}
    </style>
</head>
<body>

    <div class="print-floating-bar no-print">
        <button class="print-btn" onclick="window.print()">
            🖨️ طباعة جدول خطة الاختبار (أو حفظ بصيغة PDF)
        </button>
        <span style="font-size: 11px; color: #333333; font-weight: 600;">
            تسطير رسمي عادي واضح — مقاس A4 أفقي Landscape — خالٍ من التعقيدات والألوان السوداء
        </span>
    </div>

    <!-- الترويسة الرسمية -->
    <div class="official-header">
        <table class="header-table">
            <tr>
                <td style="width: 33%; text-align: right;">
                    <div class="inst-title-1">الجمهورية اليمنية</div>
                    <div class="inst-title-2">وزارة التربية والتعليم والبحث العلمي</div>
                    <div class="inst-title-3">قطاع المناهج والتوجيه والتقويم — الإدارة العامة للاختبارات المركزية</div>
                </td>
                <td style="width: 34%; text-align: center;">
                    <div class="doc-title-main">خطة وجدول فحص واختبار شاشات المنظومة</div>
                    <div class="doc-title-sub">مشروع بنك الأسئلة الموحد وإدارة الامتحانات والتصحيح الآلي (OMR)</div>
                </td>
                <td style="width: 33%; text-align: left;">
                    <div class="doc-meta">
                        <strong>Document No:</strong> QA-EXAM-117-2026<br>
                        <strong>Release Date:</strong> 19 November 2026<br>
                        <strong>Scope:</strong> 11 Systems / 117 Master Screens
                    </div>
                </td>
            </tr>
        </table>

        <!-- شريط الملخص الإحصائي البسيط -->
        <table class="summary-bar-table">
            <tr>
                <th>إجمالي الشاشات</th>
                <th>عدد المنظومات</th>
                <th>إجمالي زمن الفحص</th>
                <th>شاشات حرجة (P1)</th>
                <th>شاشات أساسية (P2)</th>
                <th>شاشات مساندة (P3)</th>
            </tr>
            <tr>
                <td style="font-size: 13px; color: #1e3a8a;">{total_screens} شاشة</td>
                <td style="font-size: 12px;">{len(clean_modules)} منظومات</td>
                <td style="font-size: 12px; color: #047857;">{total_hours} ساعة ({total_days} أيام عمل)</td>
                <td style="color: #b91c1c;">{p1_count} شاشة</td>
                <td style="color: #1d4ed8;">{p2_count} شاشة</td>
                <td style="color: #4b5563;">{p3_count} شاشات</td>
            </tr>
        </table>
    </div>

    <!-- الجدول الرئيسي بالتسطير العادي البسيط -->
    <table class="main-schedule-table">
        <thead>
            <tr>
                <th class="col-id">#</th>
                <th class="col-title">اسم الشاشة بالعربية</th>
                <th class="col-code">المكون والمسار البرمجي</th>
                <th class="col-subsystem">المنظومة / الوحدة</th>
                <th class="col-testing-scope">نطاق وفحص الشاشة (Testing Scope)</th>
                <th class="col-executor">الدور المنفذ</th>
                <th class="col-priority">الأولوية</th>
                <th class="col-duration">المدة</th>
                <th class="col-acceptance">معيار القبول والنجاح</th>
            </tr>
        </thead>
        <tbody>
"""

screen_idx = 1
for m in clean_modules:
    m_id = m["module_id"]
    m_name = m["name"]
    m_screens = m["screens"]
    m_mins = sum(s["duration"] for s in m_screens)
    m_hrs = round(m_mins / 60, 1)

    html_template += f"""
            <tr class="module-header-row">
                <td colspan="9">
                    المنظومة {m_id}: {m_name} — ({len(m_screens)} شاشة | إجمالي المدة: {m_mins} دقيقة / {m_hrs} ساعة)
                </td>
            </tr>
    """

    for s in m_screens:
        prio_color = "#b91c1c" if s["priority"] == "P1" else ("#1d4ed8" if s["priority"] == "P2" else "#374151")
        html_template += f"""
            <tr>
                <td class="col-id">{screen_idx}</td>
                <td class="col-title">{s["name"]}</td>
                <td class="col-code">
                    <strong>{s["code"]}</strong><br>
                    <span style="color:#4b5563;">{s["route"]}</span>
                </td>
                <td class="col-subsystem">{m_name.split('،')[0]}</td>
                <td class="col-testing-scope">{s["scope"]}</td>
                <td class="col-executor">{s["role"]}</td>
                <td class="col-priority" style="color:{prio_color};">{s["priority"]}</td>
                <td class="col-duration">{s["duration"]} د</td>
                <td class="col-acceptance">{s["criteria"]}</td>
            </tr>
        """
        screen_idx += 1

html_template += f"""
        </tbody>
    </table>

    <!-- صفحة الاعتماد والختام الرسمية -->
    <div class="page-break"></div>

    <div style="padding: 10px 4px;">
        <div style="border-bottom: 2px solid #1e3a8a; padding-bottom: 6px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 14px; font-weight: 800; color: #1e3a8a;">
                📊 جدول التوزيع الإحصائي للأزمنة والأولويات حسب المنظومات الـ 11
            </div>
            <div style="font-size: 10px; color: #475569; font-weight: 700;">
                الجمهورية اليمنية — قطاع المناهج والتوجيه والتقويم — الإدارة العامة للاختبارات المركزية
            </div>
        </div>

        <table class="matrix-table">
            <thead>
                <tr>
                    <th style="width: 35px;">م</th>
                    <th style="text-align: right; padding-right: 10px;">المنظومة / الوحدة البرمجية</th>
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

for m in clean_modules:
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
                    <td>{m_id}</td>
                    <td style="text-align: right; font-weight: 700; padding-right: 10px;">{m_name}</td>
                    <td style="font-weight: 700;">{cnt}</td>
                    <td style="color: #b91c1c; font-weight: 700;">{p1}</td>
                    <td style="color: #1d4ed8; font-weight: 700;">{p2}</td>
                    <td style="color: #4b5563;">{p3}</td>
                    <td>{mins} دقيقة</td>
                    <td style="font-weight: 700; color: #047857;">{hrs} ساعة</td>
                    <td>{pct}%</td>
                </tr>
    """

html_template += f"""
                <tr class="total-row">
                    <td colspan="2" style="text-align: center;">الإجمالي العام المعتمد لكافة شاشات المشروع</td>
                    <td>{total_screens} شاشة</td>
                    <td style="color: #b91c1c;">{p1_count}</td>
                    <td style="color: #1d4ed8;">{p2_count}</td>
                    <td style="color: #4b5563;">{p3_count}</td>
                    <td>{total_minutes} دقيقة</td>
                    <td style="color: #047857;">{total_hours} ساعة</td>
                    <td>100%</td>
                </tr>
            </tbody>
        </table>
    </div>

</body>
</html>
"""

with open("docs/SCREEN_TEST_PLAN_SCHEDULE.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Updated docs/SCREEN_TEST_PLAN_SCHEDULE.html successfully!")
