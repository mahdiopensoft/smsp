import { ref, computed } from 'vue'

const currentInstitutionType = ref('school') // 'school' | 'university'

export function useTerminology() {
    function setInstitutionType(type) {
        if (type === 'school' || type === 'university') {
            currentInstitutionType.value = type
        }
    }

    const isUniversity = computed(() => currentInstitutionType.value === 'university')
    const isSchool = computed(() => currentInstitutionType.value === 'school')

    const terms = computed(() => {
        if (isUniversity.value) {
            return {
                stage: 'الكلية',
                level: 'القسم الأكاديمي',
                branch: 'البرنامج الأكاديمي',
                subject: 'المقرر الدراسي',
                unit: 'الموضوع',
                lesson: 'المحاضرة',
                clo: 'مخرج التعلم (CLO)',
                author: 'عضو هيئة التدريس',
                exam: 'الاختبار الأكاديمي',
            }
        }
        return {
            stage: 'المرحلة الدراسية',
            level: 'الصف الدراسي',
            branch: 'المسار (علمي / أدبي)',
            subject: 'المادة الدراسية',
            unit: 'الوحدة الدراسية',
            lesson: 'الدرس الأكاديمي',
            clo: 'مخرج التعلم',
            author: 'المعلم / المؤلف',
            exam: 'الامتحان المدرسي',
        }
    })

    return {
        currentInstitutionType,
        isUniversity,
        isSchool,
        terms,
        setInstitutionType,
    }
}
