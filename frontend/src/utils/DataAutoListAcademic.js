import shared from "external-components";

export default function DataAutoListAcademic(param) {
  return {
    // ═══════════════════════════════════════════════════════════════════════════════
    // 🏫 قوائم المدارس المستقلة (Independent School Lists)
    // ═══════════════════════════════════════════════════════════════════════════════
    Subject: {
      label: "المادة الدراسية",
      icon: "book-open-page-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw) {
          if (typeof raw === 'object') {
            if (raw.class_track || raw.classTrackId || raw.class_track_id) {
              queryParams.class_track = raw.class_track || raw.classTrackId || raw.class_track_id;
            }
            if (raw.stage || raw.stageId || raw.stage_id) {
              queryParams.stage = raw.stage || raw.stageId || raw.stage_id;
            }
            if (raw.level || raw.levelId || raw.level_id) {
              queryParams.level = raw.level || raw.levelId || raw.level_id;
            }
            if (!Object.keys(queryParams).length && raw.id) {
              queryParams.class_track = raw.id;
            }
          } else {
            queryParams.class_track = raw;
          }
        }
        
        // إذا تم تمرير كائن محدد فارغ، لا تجلب كافة المواد
        if (raw !== undefined && !Object.keys(queryParams).length) {
          return Promise.resolve([]);
        }

        return shared.getData({
          path: "api/academic/school-subjects/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    SchoolSubject: {
      label: "المادة الدراسية المدرسية",
      icon: "book-open-page-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === 'object') {
          if (raw.class_track || raw.classTrackId) queryParams.class_track = raw.class_track || raw.classTrackId;
          if (raw.stage || raw.stageId) queryParams.stage = raw.stage || raw.stageId;
          if (raw.level || raw.levelId) queryParams.level = raw.level || raw.levelId;
        } else if (raw) {
          queryParams.class_track = raw;
        }
        return shared.getData({
          path: "api/academic/school-subjects/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    SubjectByClassTrack: {
      label: "المادة الدراسية",
      icon: "book-open-page-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const trackId = (raw && typeof raw === 'object') ? (raw.class_track || raw.classTrackId || raw.id || raw.value) : raw;
        return trackId ?
          shared.getData({
            path: "api/academic/school-subjects/all/",
            params: { class_track: trackId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    SchoolSubjectByClassTrack: {
      label: "المادة الدراسية",
      icon: "book-open-page-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const trackId = (raw && typeof raw === 'object') ? (raw.class_track || raw.classTrackId || raw.id || raw.value) : raw;
        return trackId ? shared.getData({
          path: "api/academic/school-subjects/all/",
          params: { class_track: trackId }
        }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    SubjectByStage: {
      label: "المادة الدراسية",
      icon: "book-open-page-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const stageId = (raw && typeof raw === 'object') ? (raw.stage || raw.stageId || raw.id || raw.value) : raw;
        return stageId ?
          shared.getData({
            path: "api/academic/school-subjects/all/",
            params: { stage: stageId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    ClassSubjectByTrack: {
      label: "مادة مسار الصف",
      icon: "book-open-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const trackId = (raw && typeof raw === 'object') ? (raw.class_track || raw.classTrackId || raw.stage || raw.stageId || raw.id || raw.value) : raw;
        return trackId ?
          shared.getData({
            path: "api/academic/class-subjects/all/",
            params: (typeof raw === 'object' && raw.class_track) ? { class_track: raw.class_track } : { stage: trackId }
          }) : Promise.resolve([]);
      },
      title: "subject_name",
      value: "id",
    },

    ClassSubject: {
      label: "مادة مسار الصف",
      icon: "book-education-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const trackId = (raw && typeof raw === 'object') ? (raw.class_track || raw.classTrackId || raw.stage || raw.stageId || raw.id || raw.value) : raw;
        return trackId ?
          shared.getData({
            path: "api/academic/class-subjects/all/",
            params: (typeof raw === 'object' && raw.class_track) ? { class_track: raw.class_track } : { stage: trackId }
          }) : Promise.resolve([]);
      },
      title: "subject_name",
      value: "id",
    },

    ClassTrack: {
      label: "مسار الصف",
      icon: "book-education-outline",
      method: () =>
        shared.getData({
          path: "api/academic/class-tracks/all/",
        }),
      title: "full_name",
      value: "id",
    },

    ClassTrackByStage: {
      label: "الصف والمسار",
      icon: "source-branch",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const stageId = (raw && typeof raw === 'object') ? (raw.stage || raw.stageId || raw.id || raw.value) : raw;
        return stageId ?
          shared.getData({
            path: "api/academic/class-tracks/all/",
            params: { stage: stageId }
          }) : Promise.resolve([]);
      },
      title: "full_name",
      value: "id",
    },

    EducationalStage: {
      label: "المرحلة الدراسية",
      icon: "school",
      method: () =>
        shared.getData({
          path: "api/academic/educational-stages/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    Stage: {
      label: "المرحلة الدراسية",
      icon: "school",
      method: () =>
        shared.getData({
          path: "api/academic/educational-stages/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    Level: {
      label: "الصف الدراسي",
      icon: "stairs",
      method: () =>
        shared.getData({
          path: "api/academic/levels/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    LevelByStage: {
      label: "الصف الدراسي",
      icon: "stairs",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const stageId = (raw && typeof raw === 'object') ? (raw.stage || raw.stageId || raw.id || raw.value) : raw;
        return stageId ?
          shared.getData({
            path: "api/academic/levels/all/",
            params: { stage: stageId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    Track: {
      label: "المسار التعليمي",
      icon: "routes",
      method: () =>
        shared.getData({
          path: "api/academic/tracks/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    TrackByLevel: {
      label: "المسار التعليمي",
      icon: "routes",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const levelId = (raw && typeof raw === 'object') ? (raw.level || raw.levelId || raw.id || raw.value) : raw;
        return shared.getData({
          path: "api/academic/tracks/all/",
          params: levelId ? { level: levelId } : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    Unit: {
      label: "الوحدة الدراسية",
      icon: "folder-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        let isUniversity = false;
        if (raw) {
          if (typeof raw === 'object') {
            if (raw.semester_subject || raw.semesterSubjectId) {
              queryParams.semester_subject = raw.semester_subject || raw.semesterSubjectId;
              isUniversity = true;
            } else if (raw.course || raw.courseId) {
              queryParams.semester_subject = raw.course || raw.courseId;
              isUniversity = true;
            }
            if (raw.subject || raw.subjectId || raw.school_subject) {
              queryParams.subject = raw.subject || raw.subjectId || raw.school_subject;
            }
            if (raw.class_subject || raw.classSubjectId) {
              queryParams.class_subject = raw.class_subject || raw.classSubjectId;
            }
            if (raw.id && !queryParams.subject && !queryParams.semester_subject && !queryParams.class_subject) {
              queryParams.subject = raw.id;
            }
          } else {
            queryParams.subject = raw;
          }
        }
        if (isUniversity && queryParams.semester_subject) {
          return shared.getData({
            path: "api/academic/units/all/",
            params: { semester_subject: queryParams.semester_subject },
          });
        }
        return (queryParams.subject || queryParams.class_subject) ?
          shared.getData({
            path: "api/academic/units/all/",
            params: queryParams,
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    UnitBySubject: {
      label: "الوحدة الدراسية",
      icon: "folder-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        let isUniversity = false;
        if (raw) {
          if (typeof raw === 'object') {
            if (raw.semester_subject || raw.semesterSubjectId) {
              queryParams.semester_subject = raw.semester_subject || raw.semesterSubjectId;
              isUniversity = true;
            } else if (raw.course || raw.courseId) {
              queryParams.semester_subject = raw.course || raw.courseId;
              isUniversity = true;
            }
            if (raw.subject || raw.subjectId || raw.school_subject) {
              queryParams.subject = raw.subject || raw.subjectId || raw.school_subject;
            }
            if (raw.institute_subject || raw.instituteSubjectId) {
              queryParams.subject = raw.institute_subject || raw.instituteSubjectId;
            }
            if (raw.class_subject || raw.classSubjectId) {
              queryParams.class_subject = raw.class_subject || raw.classSubjectId;
            }
            if (raw.id && !queryParams.subject && !queryParams.semester_subject && !queryParams.class_subject) {
              queryParams.subject = raw.id;
            }
          } else {
            queryParams.subject = raw;
          }
        }
        if (isUniversity && queryParams.semester_subject) {
          return shared.getData({
            path: "api/academic/units/all/",
            params: { semester_subject: queryParams.semester_subject },
          });
        }
        return (queryParams.subject || queryParams.class_subject) ?
          shared.getData({
            path: "api/academic/units/all/",
            params: queryParams,
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    SchoolUnit: {
      label: "الوحدة المدرسية",
      icon: "folder-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === 'object') {
          if (raw.school_subject || raw.subject) queryParams.school_subject = raw.school_subject || raw.subject;
          if (raw.class_subject) queryParams.class_subject = raw.class_subject;
        } else if (raw) {
          queryParams.school_subject = raw;
        }
        return (queryParams.school_subject || queryParams.class_subject) ? shared.getData({
          path: "api/academic/school-units/all/",
          params: queryParams,
        }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    LessonByUnit: {
      label: "الدرس",
      icon: "file-document-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const unitId = (raw && typeof raw === 'object') ? (raw.unit || raw.unitId || raw.id || raw.value) : raw;
        return unitId ?
          shared.getData({
            path: "api/academic/lessons/all/",
            params: { unit: unitId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    SchoolLesson: {
      label: "الدرس المدرسي",
      icon: "file-document-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const unitId = (raw && typeof raw === 'object') ? (raw.unit || raw.unitId || raw.id || raw.value) : raw;
        return unitId ? shared.getData({
          path: "api/academic/school-lessons/all/",
          params: { unit: unitId }
        }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    LearningOutcome: {
      label: "مخرج التعلم",
      icon: "bullseye-arrow",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const unitId = (raw && typeof raw === 'object') ? (raw.unit || raw.unitId || raw.id || raw.value) : raw;
        return unitId ?
          shared.getData({
            path: "api/academic/learning-outcomes/all/",
            params: { unit: unitId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    SchoolLearningOutcome: {
      label: "مخرج التعلم المدرسي",
      icon: "bullseye-arrow",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const unitId = (raw && typeof raw === 'object') ? (raw.unit || raw.unitId || raw.id || raw.value) : raw;
        return unitId ? shared.getData({
          path: "api/academic/school-learning-outcomes/all/",
          params: { unit: unitId }
        }) : Promise.resolve([]);
      },
      title: "code",
      value: "id",
    },

    SchoolSection: {
      label: "الشعبة / الفصل",
      icon: "google-classroom",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === 'object') {
          if (raw.organization) queryParams.organization = raw.organization;
          if (raw.class_track) queryParams.class_track = raw.class_track;
          if (raw.level) queryParams.level = raw.level;
        }
        return shared.getData({
          path: "api/academic/school-sections/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    // ═══════════════════════════════════════════════════════════════════════════════
    // 🏛️ قوائم الجامعات المستقلة (Independent University Lists)
    // ═══════════════════════════════════════════════════════════════════════════════
    College: {
      label: "الكلية",
      icon: "school",
      method: () =>
        shared.getData({
          path: "api/academic/colleges/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    DepartmentByCollege: {
      label: "القسم الأكاديمي",
      icon: "domain",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const collegeId = (raw && typeof raw === 'object') ? (raw.college || raw.collegeId || raw.fk_college || raw.id || raw.value) : raw;
        return collegeId ?
          shared.getData({
            path: "api/academic/departments/all/",
            params: { college: collegeId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    Specialization: {
      label: "التخصص الأكاديمي",
      icon: "book-open-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw) {
          if (typeof raw === 'object') {
            if (raw.section || raw.department || raw.departmentId || raw.fk_section) {
              queryParams.section = raw.section || raw.department || raw.departmentId || raw.fk_section;
            }
            if (raw.college || raw.collegeId || raw.fk_college) {
              queryParams.college = raw.college || raw.collegeId || raw.fk_college;
            }
            if (!Object.keys(queryParams).length && raw.id) {
              queryParams.section = raw.id;
            }
          } else {
            queryParams.section = raw;
          }
        }
        return (queryParams.section || queryParams.college) ?
          shared.getData({
            path: "api/academic/specializations/all/",
            params: queryParams,
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    UniversityCourse: {
      label: "المقرر الجامعي",
      icon: "book-education",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === 'object') {
          if (raw.college || raw.collegeId || raw.fk_college) queryParams.college = raw.college || raw.collegeId || raw.fk_college;
          if (raw.department || raw.departmentId || raw.fk_section) queryParams.department = raw.department || raw.departmentId || raw.fk_section;
          if (raw.specialization || raw.specializationId || raw.fk_specialization) queryParams.specialization = raw.specialization || raw.specializationId || raw.fk_specialization;
        } else if (raw) {
          queryParams.specialization = raw;
        }
        return shared.getData({
          path: "api/academic/university-courses/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    UniversityCourseBySpecialization: {
      label: "المقرر الجامعي",
      icon: "book-education",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const specId = (raw && typeof raw === 'object') ? (raw.specialization || raw.specializationId || raw.fk_specialization || raw.id || raw.value) : raw;
        return specId ? shared.getData({
          path: "api/academic/university-courses/all/",
          params: { specialization: specId }
        }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    SemesterSubject: {
      label: "مقرر الفصل الجامعي",
      icon: "book-cog",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const specId = (raw && typeof raw === 'object') ? (raw.specialization || raw.specializationId || raw.fk_specialization || raw.id || raw.value) : raw;
        return specId ?
          shared.getData({
            path: "api/academic/semester-subjects/all/",
            params: { specialization: specId }
          }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    CourseTopic: {
      label: "موضوع / مفردة المقرر",
      icon: "file-tree",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const courseId = (raw && typeof raw === 'object') ? (raw.course || raw.courseId || raw.course_id || raw.id || raw.value) : raw;
        return courseId ? shared.getData({
          path: "api/academic/course-topics/all/",
          params: { course: courseId }
        }) : Promise.resolve([]);
      },
      title: "name_ar",
      value: "id",
    },

    CourseCLO: {
      label: "مخرج تعلم المقرر (CLO)",
      icon: "bullseye-arrow",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const courseId = (raw && typeof raw === 'object') ? (raw.course || raw.courseId || raw.course_id || raw.id || raw.value) : raw;
        return courseId ? shared.getData({
          path: "api/academic/course-clos/all/",
          params: { course: courseId }
        }) : Promise.resolve([]);
      },
      title: "clo_code",
      value: "id",
    },

    EducationalLevels: {
      label: "المستويات التعليمية والدرجات",
      icon: "certificate",
      method: () =>
        shared.getData({
          path: "api/academic/educational-levels/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    StudySystem: {
      label: "نظام الدراسة",
      icon: "cog-transfer",
      method: () =>
        shared.getData({
          path: "api/academic/study-systems/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    GradingSystem: {
      label: "نظام الدرجات",
      icon: "chart-box-outline",
      method: () =>
        shared.getData({
          path: "api/academic/grading-systems/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    TypeOfGrade: {
      label: "نوع الدرجة",
      icon: "format-list-numbered",
      method: () =>
        shared.getData({
          path: "api/academic/type-of-grades/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    TypeOfGradeChoices: {
      label: "طريقة إدخال الدرجة",
      icon: "format-list-checks",
      method: () => Promise.resolve([
        { name: "درجة صحيحة (رقم)", id: 1 },
        { name: "نظام التقديرات (رموز A, B...)", id: 2 },
      ]),
      title: "name",
      value: "id",
    },

    GradeSystemTypeChoices: {
      label: "نوع النظام التقديري",
      icon: "format-list-numbered",
      method: () => Promise.resolve([
        { name: "يونيو", id: 1 },
        { name: "اكتوبر", id: 2 },
        { name: "معفيين", id: 3 },
        { name: "المتنازلين", id: 4 },
      ]),
      title: "name",
      value: "id",
    },

    Period: {
      label: "الفترة الامتحانية",
      icon: "calendar-range",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const semId = (raw && typeof raw === 'object') ? (raw.semester || raw.semesterId || raw.fk_semester || raw.id || raw.value) : raw;
        return shared.getData({
          path: "api/academic/exam-periods/all/",
          params: semId ? { semester: semId } : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    ExamPeriod: {
      label: "الفترة الامتحانية",
      icon: "calendar-range",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const semId = (raw && typeof raw === 'object') ? (raw.semester || raw.semesterId || raw.fk_semester || raw.id || raw.value) : raw;
        return shared.getData({
          path: "api/academic/exam-periods/all/",
          params: semId ? { semester: semId } : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    // ═══════════════════════════════════════════════════════════════════════════════
    // 🌐 القوائم المشتركة والعامة (Common & General Lists)
    // ═══════════════════════════════════════════════════════════════════════════════
    AcademicYear: {
      label: "العام الدراسي / الأكاديمي",
      icon: "calendar-clock",
      method: () =>
        shared.getData({
          path: "api/academic/academic-years/all/",
        }),
      title: "name",
      value: "id",
    },

    Semester: {
      label: "الفصل الدراسي",
      icon: "calendar-range",
      method: () =>
        shared.getData({
          path: "api/academic/semesters/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    SemesterByStage: {
      label: "الفصل الدراسي",
      icon: "calendar-range",
      method: () =>
        shared.getData({
          path: "api/academic/semesters/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    Organization: {
      label: "المؤسسة / المدرسة",
      icon: "domain",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw) {
          if (typeof raw === 'object') {
            if (raw.institution_type === '__none__') {
              return Promise.resolve([]);
            }
            if (raw.institution_type && raw.institution_type !== 'all') {
              queryParams.institution_type = raw.institution_type;
            }
            if (raw.governorate) {
              queryParams.governorate = raw.governorate;
            }
            if (raw.directorate) {
              queryParams.directorate = raw.directorate;
            }
            if (raw.is_active !== undefined) {
              queryParams.is_active = raw.is_active;
            }
            if (raw.parent) {
              queryParams.parent = raw.parent;
            }
          } else if (typeof raw === 'string') {
            if (raw === '__none__') return Promise.resolve([]);
            if (raw !== 'all') queryParams.institution_type = raw;
          }
        }
        return shared.getData({
          path: "api/academic/organizations/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    Difficulty: {
      label: "مستوى الصعوبة",
      icon: "speedometer",
      method: () => Promise.resolve([
        { name: "سهل", id: 1 },
        { name: "متوسط", id: 2 },
        { name: "صعب", id: 3 },
      ]),
      title: "name",
      value: "id",
    },

    QuestionType: {
      label: "نوع السؤال",
      icon: "shape-outline",
      method: () => Promise.resolve([
        { name: "اختيار واحد", id: "single_choice" },
        { name: "اختيارات متعددة", id: "multiple_choice" },
        { name: "صواب/خطأ", id: "true_false" },
      ]),
      title: "name",
      value: "id",
    },

    Exam: {
      label: "الاختبار",
      icon: "file-document-edit-outline",
      method: async (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw) {
          if (typeof raw === 'object') {
            // معايير المدارس
            if (raw.subject || raw.subjectId || raw.subject_id) {
              queryParams.subject = raw.subject || raw.subjectId || raw.subject_id;
            } else if (raw.id) {
              queryParams.subject = raw.id;
            }
            if (raw.stage || raw.stageId || raw.stage_id) {
              queryParams.stage = raw.stage || raw.stageId || raw.stage_id;
            }
            if (raw.level || raw.levelId || raw.level_id) {
              queryParams.level = raw.level || raw.levelId || raw.level_id;
            }
            if (raw.class_track || raw.classTrackId) {
              queryParams.class_track = raw.class_track || raw.classTrackId;
            }

            // معايير الجامعات
            if (raw.course || raw.courseId || raw.course_id) {
              queryParams.course = raw.course || raw.courseId || raw.course_id;
            }
            if (raw.specialization || raw.specializationId) {
              queryParams.specialization = raw.specialization || raw.specializationId;
            }
            if (raw.college || raw.collegeId) {
              queryParams.college = raw.college || raw.collegeId;
            }
            if (raw.semester_subject || raw.semesterSubjectId) {
              queryParams.semester_subject = raw.semester_subject || raw.semesterSubjectId;
            }

            // معايير مشتركة
            if (raw.institution_type) {
              queryParams.institution_type = raw.institution_type;
            }
            if (raw.semester || raw.semesterId) {
              queryParams.semester = raw.semester || raw.semesterId;
            }
            if (raw.year || raw.yearId || raw.year_id) {
              queryParams.year = raw.year || raw.yearId || raw.year_id;
            }
          } else {
            queryParams.subject = raw;
          }
        }

        let res = await shared.getData({
          path: "api/exams/exams/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });

        let list = [];
        if (Array.isArray(res)) list = res;
        else if (res?.data && Array.isArray(res.data)) list = res.data;
        else if (res?.results && Array.isArray(res.results)) list = res.results;
        else {
          const fallback = await shared.getData({
            path: "api/exams/exams/",
            params: Object.keys(queryParams).length ? queryParams : undefined,
          });
          if (Array.isArray(fallback)) list = fallback;
          else if (fallback?.data && Array.isArray(fallback.data)) list = fallback.data;
          else if (fallback?.results && Array.isArray(fallback.results)) list = fallback.results;
        }

        return list.map(item => ({
          ...item,
          name: item.name || (item.title ? `${item.title} (${item.uniqueCode || item.id})` : `اختبار #${item.id}`),
          name_ar: item.name_ar || item.name || (item.title ? `${item.title} (${item.uniqueCode || item.id})` : `اختبار #${item.id}`),
        }));
      },
      title: "name_ar",
      value: "id",
    },

    // ═══════════════════════════════════════════════════════════════════════════════
    // 🏢 قوائم المعاهد ومراكز التدريب المهني (Institutes Auto Lists)
    // ═══════════════════════════════════════════════════════════════════════════════
    Institute: {
      label: "المعهد / المركز التعليمي",
      icon: "domain",
      method: () =>
        shared.getData({
          path: "api/academic/organizations/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    InstituteField: {
      label: "المجال المهني / التقني",
      icon: "shape-outline",
      method: () =>
        shared.getData({
          path: "api/academic/institutes/fields/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    InstituteEducationSystem: {
      label: "نظام التعليم والتدريب",
      icon: "cogs",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.field || raw.fieldId) queryParams.field = raw.field || raw.fieldId;
        } else if (raw) {
          queryParams.field = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/education-systems/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteSpecialization: {
      label: "التخصص المهني / التقني",
      icon: "school-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.field || raw.fieldId) queryParams.field = raw.field || raw.fieldId;
          if (raw.education_system || raw.educationSystemId) {
            queryParams.education_system = raw.education_system || raw.educationSystemId;
          }
        } else if (raw) {
          queryParams.education_system = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/specializations/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteCurriculum: {
      label: "الخطة الدراسية للمعهد",
      icon: "notebook-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.specialization || raw.specializationId) {
            queryParams.specialization = raw.specialization || raw.specializationId;
          }
          if (raw.academic_year || raw.academicYearId) {
            queryParams.academic_year = raw.academic_year || raw.academicYearId;
          }
        } else if (raw) {
          queryParams.specialization = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/curricula/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteBatch: {
      label: "الدفعة / الفوج",
      icon: "account-group-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.specialization || raw.specializationId) {
            queryParams.specialization = raw.specialization || raw.specializationId;
          }
        } else if (raw) {
          queryParams.specialization = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/batches/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteSubject: {
      label: "المادة الدراسية للمعهد",
      icon: "book-open-page-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.field || raw.fieldId) queryParams.field = raw.field || raw.fieldId;
        } else if (raw) {
          queryParams.field = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/subjects/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteLevel: {
      label: "المستوى الدراسي للمعهد",
      icon: "stairs",
      method: () =>
        shared.getData({
          path: "api/academic/institutes/levels/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    InstituteSemester: {
      label: "الفصل / الفترة الدراسية للمعهد",
      icon: "calendar-range",
      method: () =>
        shared.getData({
          path: "api/academic/institutes/semesters/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    InstituteShortCourse: {
      label: "الدورة التدريبية القصيرة",
      icon: "certificate-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.field || raw.fieldId) queryParams.field = raw.field || raw.fieldId;
        } else if (raw) {
          queryParams.field = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/short-courses/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteSpecialTrack: {
      label: "مسار تحقيق المهنة / المسار الخاص",
      icon: "shield-check-outline",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.field || raw.fieldId) queryParams.field = raw.field || raw.fieldId;
        } else if (raw) {
          queryParams.field = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/special-tracks/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    InstituteAdmissionRequirement: {
      label: "شروط وضوابط القبول",
      icon: "clipboard-check-outline",
      method: () =>
        shared.getData({
          path: "api/academic/institutes/admission-requirements/all/",
        }),
      title: "title",
      value: "id",
    },

    InstituteCurriculumSubject: {
      label: "مقرر الخطة الدراسية للمعهد",
      icon: "book-cog",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.curriculum || raw.curriculumId) {
            queryParams.curriculum = raw.curriculum || raw.curriculumId;
          }
        } else if (raw) {
          queryParams.curriculum = raw;
        }
        return shared.getData({
          path: "api/academic/institutes/curriculum-subjects/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    // ═══════════════════════════════════════════════════════════════════════════════
    // 🏫 أسماء مطابقة لمدخلات نماذج المدارس (Schools Aliases)
    // ═══════════════════════════════════════════════════════════════════════════════
    SchoolLevel: {
      label: "الصف الدراسي",
      icon: "bookshelf",
      method: () =>
        shared.getData({
          path: "api/academic/levels/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    SchoolTrack: {
      label: "المسار التعليمي",
      icon: "routes",
      method: () =>
        shared.getData({
          path: "api/academic/tracks/all/",
        }),
      title: "name_ar",
      value: "id",
    },

    SchoolClassTrack: {
      label: "مسار الصف",
      icon: "routes",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.level || raw.levelId) queryParams.level = raw.level || raw.levelId;
          if (raw.track || raw.trackId) queryParams.track = raw.track || raw.trackId;
        } else if (raw) {
          queryParams.level = raw;
        }
        return shared.getData({
          path: "api/academic/class-tracks/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    SchoolClassSubject: {
      label: "مادة مسار الصف",
      icon: "link-variant",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.class_track || raw.classTrackId) queryParams.class_track = raw.class_track || raw.classTrackId;
        } else if (raw) {
          queryParams.class_track = raw;
        }
        return shared.getData({
          path: "api/academic/class-subjects/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },

    SchoolSection: {
      label: "الشعبة المدرسية",
      icon: "google-classroom",
      method: (p) => {
        const raw = (p !== undefined && p !== null) ? p : param;
        const queryParams = {};
        if (raw && typeof raw === "object") {
          if (raw.class_track || raw.classTrackId) queryParams.class_track = raw.class_track || raw.classTrackId;
          if (raw.organization || raw.organizationId) queryParams.organization = raw.organization || raw.organizationId;
        } else if (raw) {
          queryParams.class_track = raw;
        }
        return shared.getData({
          path: "api/academic/school-sections/all/",
          params: Object.keys(queryParams).length ? queryParams : undefined,
        });
      },
      title: "name_ar",
      value: "id",
    },
  };
}
