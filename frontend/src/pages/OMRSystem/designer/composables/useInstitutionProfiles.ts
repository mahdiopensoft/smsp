export interface InstitutionProfile {
  id: 'school' | 'university' | 'institute' | string
  name: string
  fullName: string
  icon: string
  color: string
  themeColor: string
  defaultDisplayMode: 'compact_a5' | 'audit_a4' | 'university_180'
  defaultEmblem: 'republic_eagle' | 'university_seal' | 'institute_seal' | 'custom' | 'none' | string
  emblemLabel: string
  labels: {
    institution: string
    subTitle: string
    examStage: string
    examSubject: string
    academicYear: string
    area1: string
    area2: string
    centerName: string
    centerCode: string
    seatNumber: string
    serialNumber: string
  }
  sheetLabels: {
    examSubject: string
    area1: string
    area2: string
    centerName: string
    centerCode: string
    seatNumber: string
    serialNumber: string
  }
  defaults: {
    institution_name: string
    sub_title: string
    exam_stage_title: string
    academic_year: string
    governorate: string
    directorate: string
    center_name: string
    center_code: string
    exam_name: string
    primary_color: string
    emblem_type?: 'republic_eagle' | 'university_seal' | 'institute_seal' | 'custom' | 'none' | string
  }
}

export const INSTITUTION_PROFILES: InstitutionProfile[] = [
  {
    id: 'school',
    name: 'مدرسي',
    fullName: 'التعليم الأساسي والثانوي — المدارس',
    icon: 'mdi-school',
    color: 'primary',
    themeColor: '#000000',
    defaultDisplayMode: 'compact_a5',
    defaultEmblem: 'republic_eagle',
    emblemLabel: 'طير الجمهورية (وزارة التربية والتعليم)',
    labels: {
      institution: 'اسم الدولة والوزارة',
      subTitle: 'القطاع / لجنة الاختبارات',
      examStage: 'المرحلة / الصف الدراسي',
      examSubject: 'اسم المادة الدراسية',
      academicYear: 'العام الدراسي',
      area1: 'المحافظة',
      area2: 'المديرية',
      centerName: 'اسم المركز الاختباري / المدرسة',
      centerCode: 'رقم المركز',
      seatNumber: 'رقم الجلوس',
      serialNumber: 'الرقم التسلسلي / السري',
    },
    sheetLabels: {
      examSubject: 'المادة',
      area1: 'المحافظة',
      area2: 'المديرية',
      centerName: 'المركز',
      centerCode: 'رقم المركز',
      seatNumber: 'رقم الجلوس',
      serialNumber: 'رقم تسلسلي',
    },
    defaults: {
      institution_name: 'الجمهورية اليمنية — وزارة التربية والتعليم',
      sub_title: 'قطاع المناهج والتوجيه — لجان الاختبارات',
      exam_stage_title: 'اختبار الشهادة العامة (المرحلة الأساسية / الثانوية)',
      academic_year: '1446هـ — 2024-2025م',
      governorate: 'أمانة العاصمة',
      directorate: 'معين',
      center_name: 'سالم قطن — معين',
      center_code: '164',
      exam_name: 'القرآن الكريم',
      primary_color: '#000000',
      emblem_type: 'republic_eagle',
    },
  },
  {
    id: 'university',
    name: 'جامعي',
    fullName: 'التعليم الجامعي والأكاديمي — الجامعات والكليات',
    icon: 'mdi-domain',
    color: 'purple',
    themeColor: '#1976D2',
    defaultDisplayMode: 'university_180',
    defaultEmblem: 'university_seal',
    emblemLabel: 'شعار الجامعات والتعليم العالي (الختم الأكاديمي)',
    labels: {
      institution: 'اسم الدولة والجامعة',
      subTitle: 'الكلية / نيابة شؤون الطلاب والامتحانات',
      examStage: 'المستوى / التخصص الأكاديمي',
      examSubject: 'اسم المقرر الأكاديمي',
      academicYear: 'العام الجامعي / الفصل',
      area1: 'المدينة / الفرع',
      area2: 'الحرم الجامعي / المبنى',
      centerName: 'قاعة الاختبارات / المعمل',
      centerCode: 'رقم الشعبة / المجموعة',
      seatNumber: 'الرقم الأكاديمي / القيد',
      serialNumber: 'رقم المقعد / التسلسلي',
    },
    sheetLabels: {
      examSubject: 'المقرر',
      area1: 'الفرع',
      area2: 'المبنى',
      centerName: 'القاعة',
      centerCode: 'الشعبة',
      seatNumber: 'الرقم الأكاديمي',
      serialNumber: 'رقم المقعد',
    },
    defaults: {
      institution_name: 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي',
      sub_title: 'جامعة صنعاء — كلية الحاسوب وتكنولوجيا المعلومات',
      exam_stage_title: 'اختبارات المفاضلة والقبول / الاختبارات النهائية',
      academic_year: 'العام الجامعي 2024-2025م',
      governorate: 'صنعاء',
      directorate: 'الحرم الجامعي الرئيسي',
      center_name: 'قاعة الاختبارات المركزية',
      center_code: 'A1',
      exam_name: 'هياكل البيانات والخوارزميات',
      primary_color: '#1976D2',
      emblem_type: 'university_seal',
    },
  },
  {
    id: 'institute',
    name: 'معاهد',
    fullName: 'التعليم الفني والتدريب المهني — المعاهد التقنية ومراكز التدريب',
    icon: 'mdi-certificate-outline',
    color: 'teal',
    themeColor: '#00796B',
    defaultDisplayMode: 'compact_a5',
    defaultEmblem: 'institute_seal',
    emblemLabel: 'شعار التعليم الفني والتدريب المهني (المعاهد التقنية)',
    labels: {
      institution: 'اسم الدولة والوزارة / الهيئة',
      subTitle: 'المعهد / قسم شؤون المتدربين والتقويم',
      examStage: 'الدبلوم / المسار الفني والمهني',
      examSubject: 'اسم المادة التدريبية / الكورس',
      academicYear: 'العام التدريبي / الدفعة',
      area1: 'المحافظة / الفرع',
      area2: 'القسم الفني / الورشة',
      centerName: 'معمل الحاسوب / مركز التدريب',
      centerCode: 'رقم الفترة / الدفعة',
      seatNumber: 'رقم القيد التدريبي / الجلوس',
      serialNumber: 'رقم الحافظة / التسلسلي',
    },
    sheetLabels: {
      examSubject: 'المادة',
      area1: 'الفرع',
      area2: 'القسم',
      centerName: 'المعمل',
      centerCode: 'الفترة',
      seatNumber: 'رقم القيد',
      serialNumber: 'رقم الحافظة',
    },
    defaults: {
      institution_name: 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني',
      sub_title: 'المعهد التقني الصناعي — إدارة الاختبارات والتقويم الآلي',
      exam_stage_title: 'اختبارات الدبلوم التقني والتدريب المهني الشامل',
      academic_year: 'العام التدريبي 2024-2025م',
      governorate: 'أمانة العاصمة',
      directorate: 'شعبة التدريب والتأهيل',
      center_name: 'مختبر التقنيات والشبكات',
      center_code: 'T-01',
      exam_name: 'شبكات الحاسوب والتقنيات الرقمية',
      primary_color: '#00796B',
      emblem_type: 'institute_seal',
    },
  },
]

export function getProfileById(typeId?: string): InstitutionProfile {
  const found = INSTITUTION_PROFILES.find((p) => p.id === typeId)
  return found || INSTITUTION_PROFILES[0]
}
