import { EAGLE_OFFICIAL_BASE64 } from './eagleBase64'

// ── 1. Academic University Seal (SVG Data URL) ──────────────────────────
export const UNIVERSITY_SEAL_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 110" width="200" height="110">
  <!-- Double Circle Academic Crest -->
  <circle cx="100" cy="55" r="48" fill="none" stroke="#000000" stroke-width="2.2" />
  <circle cx="100" cy="55" r="44" fill="none" stroke="#000000" stroke-width="0.8" stroke-dasharray="2,2" />
  <circle cx="100" cy="55" r="36" fill="none" stroke="#000000" stroke-width="1.6" />
  <!-- 3 Stars at Top -->
  <polygon points="100,12 102,17 107,17 103,20 105,25 100,22 95,25 97,20 93,17 98,17" fill="#000000" />
  <polygon points="86,15 88,19 92,19 89,21 90,25 86,23 82,25 83,21 80,19 84,19" fill="#000000" />
  <polygon points="114,15 116,19 120,19 117,21 118,25 114,23 110,25 111,21 108,19 112,19" fill="#000000" />
  <!-- Flanking Laurel Wreaths -->
  <path d="M 40,55 C 40,78 65,96 100,98 C 68,95 48,78 48,55 C 48,36 62,24 75,18 C 60,26 40,38 40,55 Z" fill="#000000" opacity="0.88" />
  <path d="M 160,55 C 160,78 135,96 100,98 C 132,95 152,78 152,55 C 152,36 138,24 125,18 C 140,26 160,38 160,55 Z" fill="#000000" opacity="0.88" />
  <!-- Open Book of Knowledge -->
  <path d="M 100,68 C 93,63 80,62 72,66 L 72,48 C 80,45 92,46 100,51 C 108,46 120,45 128,48 L 128,66 C 120,62 107,63 100,68 Z" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  <path d="M 100,51 L 100,68" stroke="#000000" stroke-width="1.5" />
  <line x1="77" y1="52" x2="94" y2="54" stroke="#000000" stroke-width="0.9" />
  <line x1="77" y1="57" x2="94" y2="59" stroke="#000000" stroke-width="0.9" />
  <line x1="77" y1="62" x2="91" y2="63" stroke="#000000" stroke-width="0.9" />
  <line x1="106" y1="54" x2="123" y2="52" stroke="#000000" stroke-width="0.9" />
  <line x1="106" y1="59" x2="123" y2="57" stroke="#000000" stroke-width="0.9" />
  <line x1="109" y1="63" x2="123" y2="62" stroke="#000000" stroke-width="0.9" />
  <!-- Torch of Learning -->
  <path d="M 97,46 L 103,46 L 101,36 L 99,36 Z" fill="#000000" />
  <path d="M 100,34 C 103,31 104,27 100,24 C 96,28 98,31 100,34 Z" fill="#000000" />
  <!-- Bottom Ribbon with text -->
  <path d="M 52,94 Q 100,105 148,94 L 143,103 Q 100,112 57,103 Z" fill="#000000" />
  <text x="100" y="102" font-family="'Cairo', Arial, sans-serif" font-size="6.8" font-weight="bold" fill="#ffffff" text-anchor="middle">التعليم الجامعي والأكاديمي</text>
  <!-- Text inside seal -->
  <text x="100" y="32" font-family="'Cairo', Arial, sans-serif" font-size="5" font-weight="bold" fill="#000000" text-anchor="middle">الجمهورية اليمنية</text>
  <text x="100" y="79" font-family="'Cairo', Arial, sans-serif" font-size="4.6" font-weight="bold" fill="#000000" text-anchor="middle">وزارة التعليم العالي</text>
  <text x="100" y="86" font-family="'Cairo', Arial, sans-serif" font-size="4" font-weight="bold" fill="#000000" text-anchor="middle">شؤون الطلاب والامتحانات</text>
</svg>`

export const UNIVERSITY_SEAL_BASE64 = `data:image/svg+xml;utf8,${encodeURIComponent(UNIVERSITY_SEAL_SVG)}`

// ── 2. Technical & Vocational Institute Seal (SVG Data URL) ─────────────
export const INSTITUTE_SEAL_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 110" width="200" height="110">
  <!-- Outer Cogwheel (Gear) -->
  <g id="cogwheel" transform="translate(100, 52)">
    <circle cx="0" cy="0" r="41" fill="none" stroke="#000000" stroke-width="2.6" />
    <circle cx="0" cy="0" r="33" fill="none" stroke="#000000" stroke-width="1.2" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" />
    <rect x="-4" y="39" width="8" height="6" fill="#000000" rx="1" />
    <rect x="-45" y="-4" width="6" height="8" fill="#000000" rx="1" />
    <rect x="39" y="-4" width="6" height="8" fill="#000000" rx="1" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(30)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(60)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(120)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(150)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(210)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(240)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(300)" />
    <rect x="-4" y="-45" width="8" height="6" fill="#000000" rx="1" transform="rotate(330)" />
  </g>
  <!-- Flanking Tech / Laurel Leaves -->
  <path d="M 38,52 C 38,76 64,94 100,96 C 66,93 46,76 46,52 C 46,33 60,22 74,16 C 58,24 38,36 38,52 Z" fill="#000000" opacity="0.88" />
  <path d="M 162,52 C 162,76 136,94 100,96 C 134,93 154,76 154,52 C 154,33 140,22 126,16 C 142,24 162,36 162,52 Z" fill="#000000" opacity="0.88" />
  <!-- Technical Caliper & Torch -->
  <path d="M 97,42 L 103,42 L 101,33 L 99,33 Z" fill="#000000" />
  <path d="M 100,31 C 104,27 105,22 100,18 C 95,22 97,27 100,31 Z" fill="#000000" />
  <line x1="88" y1="58" x2="100" y2="38" stroke="#000000" stroke-width="2.2" stroke-linecap="round" />
  <line x1="112" y1="58" x2="100" y2="38" stroke="#000000" stroke-width="2.2" stroke-linecap="round" />
  <circle cx="100" cy="38" r="2.8" fill="#000000" />
  <path d="M 93,50 Q 100,53 107,50" fill="none" stroke="#000000" stroke-width="1.3" />
  <!-- Open Technical Handbook -->
  <path d="M 100,66 C 93,61 80,60 73,64 L 73,48 C 80,45 92,46 100,50 C 108,46 120,45 127,48 L 127,64 C 120,60 107,61 100,66 Z" fill="#ffffff" stroke="#000000" stroke-width="1.6" />
  <path d="M 100,50 L 100,66" stroke="#000000" stroke-width="1.4" />
  <!-- Circuit nodes -->
  <circle cx="83" cy="54" r="1.4" fill="#000000" />
  <circle cx="91" cy="58" r="1.4" fill="#000000" />
  <circle cx="117" cy="54" r="1.4" fill="#000000" />
  <circle cx="109" cy="58" r="1.4" fill="#000000" />
  <!-- Bottom Ribbon with text -->
  <path d="M 48,93 Q 100,104 152,93 L 147,103 Q 100,112 53,103 Z" fill="#000000" />
  <text x="100" y="102" font-family="'Cairo', Arial, sans-serif" font-size="6.4" font-weight="bold" fill="#ffffff" text-anchor="middle">التعليم الفني والتدريب المهني</text>
  <!-- Text inside seal -->
  <text x="100" y="28" font-family="'Cairo', Arial, sans-serif" font-size="4.8" font-weight="bold" fill="#000000" text-anchor="middle">الجمهورية اليمنية</text>
  <text x="100" y="78" font-family="'Cairo', Arial, sans-serif" font-size="4.4" font-weight="bold" fill="#000000" text-anchor="middle">المعاهد التقنية والمهنية</text>
  <text x="100" y="85" font-family="'Cairo', Arial, sans-serif" font-size="4" font-weight="bold" fill="#000000" text-anchor="middle">لجنة الاختبارات والتقويم الآلي</text>
</svg>`

export const INSTITUTE_SEAL_BASE64 = `data:image/svg+xml;utf8,${encodeURIComponent(INSTITUTE_SEAL_SVG)}`

// ── 3. Unified Emblem Definitions ───────────────────────────────────────
export interface EmblemOption {
  id: 'republic_eagle' | 'university_seal' | 'institute_seal' | 'custom' | 'none' | string
  name: string
  shortName: string
  icon: string
  description: string
  previewSrc: string
  institutionCategory: 'school' | 'university' | 'institute' | 'all'
}

export const EMBLEM_OPTIONS: EmblemOption[] = [
  {
    id: 'republic_eagle',
    name: 'شعار الجمهورية (طير الجمهورية الرسمي)',
    shortName: 'طير الجمهورية',
    icon: 'mdi-shield-crown-outline',
    description: 'الشعار الرسمي المعتمد لوزارة التربية والتعليم وامتحانات المدارس والشهادات العامة',
    previewSrc: EAGLE_OFFICIAL_BASE64,
    institutionCategory: 'school',
  },
  {
    id: 'university_seal',
    name: 'شعار الجامعات والتعليم العالي (الختم الأكاديمي)',
    shortName: 'شعار الجامعة',
    icon: 'mdi-school-outline',
    description: 'الختم الأكاديمي للجامعات والكليات ونيابات شؤون الطلاب والامتحانات',
    previewSrc: UNIVERSITY_SEAL_BASE64,
    institutionCategory: 'university',
  },
  {
    id: 'institute_seal',
    name: 'شعار التعليم الفني والتدريب المهني (المعاهد)',
    shortName: 'شعار المعهد',
    icon: 'mdi-cog-outline',
    description: 'الختم التقني والمهني للمعاهد الفنية ومراكز التدريب المهني الشامل',
    previewSrc: INSTITUTE_SEAL_BASE64,
    institutionCategory: 'institute',
  },
  {
    id: 'custom',
    name: 'شعار مخصص (رفع صورة أو ختم المؤسسة)',
    shortName: 'شعار مخصص',
    icon: 'mdi-cloud-upload-outline',
    description: 'رفع لوجو أو ختم مخصص بصيغة PNG أو JPG أو SVG خاص بالمؤسسة',
    previewSrc: '',
    institutionCategory: 'all',
  },
  {
    id: 'none',
    name: 'بدون شعار (إخفاء الشعار)',
    shortName: 'بدون شعار',
    icon: 'mdi-eye-off-outline',
    description: 'عدم إظهار أي شعار في ترويسة الورقة',
    previewSrc: '',
    institutionCategory: 'all',
  },
]

export interface ProfileLogos {
  university?: string
  institute?: string
  school?: string
}

export function resolveEmblemSrc(
  emblemType?: string,
  customLogo?: string,
  profileLogos?: ProfileLogos,
  institutionType?: string
): string {
  if (emblemType === 'none') {
    return ''
  }

  // 1. Explicit Custom Emblem Mode
  if (emblemType === 'custom') {
    return customLogo || ''
  }

  // 2. University Profile Emblem
  if (emblemType === 'university_seal' || institutionType === 'university') {
    return profileLogos?.university || (emblemType === 'university_seal' && customLogo ? customLogo : UNIVERSITY_SEAL_BASE64)
  }

  // 3. Technical Institute Profile Emblem
  if (emblemType === 'institute_seal' || institutionType === 'institute') {
    return profileLogos?.institute || (emblemType === 'institute_seal' && customLogo ? customLogo : INSTITUTE_SEAL_BASE64)
  }

  // 4. School / Official Ministry Profile Emblem (ALWAYS Republic Eagle unless school_logo is explicitly set)
  if (emblemType === 'republic_eagle' || institutionType === 'school') {
    return profileLogos?.school || EAGLE_OFFICIAL_BASE64
  }

  // Fallback default is always Republic Eagle
  return EAGLE_OFFICIAL_BASE64
}

export function getEmblemLabel(emblemType?: string): string {
  const opt = EMBLEM_OPTIONS.find((o) => o.id === emblemType)
  return opt ? opt.name : 'طير الجمهورية الرسمي'
}
