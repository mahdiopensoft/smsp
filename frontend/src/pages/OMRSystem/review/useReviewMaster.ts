/**
 * Master Table Headers & Hierarchy Helper Configuration for OMR Human Review
 */

export const officeMasterHeaders = [
  { title: 'مكتب التربية (المحافظة)', key: 'office_name', sortable: true },
  { title: 'عدد المديريات', key: 'directorates_count', sortable: true, align: 'center', width: '120px' },
  { title: 'عدد المدارس', key: 'schools_count', sortable: true, align: 'center', width: '120px' },
  { title: 'عدد الاختبارات', key: 'exams_count', sortable: true, align: 'center', width: '120px' },
  { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '120px' },
  { title: 'الأوراق الممسوحة', key: 'scanned_count', sortable: true, align: 'center', width: '130px' },
  { title: 'تتطلب تدقيق يدوي', key: 'needs_review_count', sortable: true, align: 'center', width: '140px' },
  { title: 'أوراق معتمدة', key: 'completed_count', sortable: true, align: 'center', width: '130px' },
  { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '170px' },
]

export const directorateMasterHeaders = [
  { title: 'إدارة التربية (المديرية)', key: 'name', sortable: true },
  { title: 'عدد المدارس', key: 'schools_count', sortable: true, align: 'center', width: '120px' },
  { title: 'عدد الاختبارات', key: 'exams_count', sortable: true, align: 'center', width: '120px' },
  { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '120px' },
  { title: 'الأوراق الممسوحة', key: 'scanned_count', sortable: true, align: 'center', width: '130px' },
  { title: 'تتطلب تدقيق يدوي', key: 'needs_review_count', sortable: true, align: 'center', width: '140px' },
  { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '170px' },
]

export const schoolMasterHeaders = [
  { title: 'المدرسة / المركز الامتحاني', key: 'name', sortable: true },
  { title: 'عدد الاختبارات', key: 'exams_count', sortable: true, align: 'center', width: '120px' },
  { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '120px' },
  { title: 'الأوراق الممسوحة', key: 'scanned_count', sortable: true, align: 'center', width: '130px' },
  { title: 'تتطلب تدقيق يدوي', key: 'needs_review_count', sortable: true, align: 'center', width: '140px' },
  { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '140px' },
]

export const examMasterHeaders = [
  { title: 'الاختبار والمادة', key: 'title', sortable: true },
  { title: 'عدد المدارس', key: 'schools_count', sortable: true, align: 'center', width: '120px' },
  { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '120px' },
  { title: 'الأوراق الممسوحة', key: 'total_scanned', sortable: true, align: 'center', width: '130px' },
  { title: 'تتطلب تدقيق يدوي', key: 'needs_review_count', sortable: true, align: 'center', width: '150px' },
  { title: 'أوراق معتمدة', key: 'completed_count', sortable: true, align: 'center', width: '130px' },
  { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '180px' },
]

export const detailHeaders = [
  { title: 'بيانات الطالب والورقة', key: 'student_info', sortable: true },
  { title: 'الاختبار والمادة', key: 'exam_title', sortable: false },
  { title: 'نسبة الثقة', key: 'confidence', sortable: true, align: 'center', width: '110px' },
  { title: 'ملتبسة', key: 'ambiguous_count', sortable: true, align: 'center', width: '110px' },
  { title: 'الدرجة', key: 'score', sortable: true, align: 'center', width: '100px' },
  { title: 'الحالة', key: 'status', sortable: true, align: 'center', width: '130px' },
  { title: 'إجراءات التدقيق', key: 'actions', sortable: false, align: 'center', width: '200px' },
]

export function sliceForPagination(allList: any[], params: any = {}) {
  const p = params?.params || params || {}
  const page = Number(p.page) || 1
  const pageSize = Number(p.page_size) || 20
  const all = allList || []
  const start = (page - 1) * pageSize
  return {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
      page_size: pageSize,
    },
  }
}
