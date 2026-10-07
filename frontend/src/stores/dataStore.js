import { reactive, computed } from 'vue'
import { academicService } from '@/services/academicService'
import { bankService } from '@/services/bankService'
import { usersService } from '@/services/usersService'
import { studentsService } from '@/services/studentsService'
import { examsService } from '@/services/examsService'

const state = reactive({
    users: [], years: [], organizations: [], stages: [], levels: [], subjects: [], branches: [],
    tracks: [], classTracks: [], classSubjects: [], semesters: [],
    levelSubjectBranches: [], units: [], learningOutcomes: [], lessons: [], questions: [], answers: [],
    examGenerationSettings: [], exams: [], examVersions: [], examQuestionOrders: [], students: [],
    levelStudentYears: [], studentExamRegistrations: [], auditLogs: [], examSchedules: [],
    examPeriods: [],
    loading: {}, errors: {}
})

export function useDataStore() {
    return {
        users: computed(() => state.users),
        years: computed(() => state.years),
        organizations: computed(() => state.organizations),
        stages: computed(() => state.stages),
        levels: computed(() => state.levels),
        subjects: computed(() => state.subjects),
        branches: computed(() => state.branches),
        tracks: computed(() => state.tracks),
        classTracks: computed(() => state.classTracks),
        classSubjects: computed(() => state.classSubjects),
        semesters: computed(() => state.semesters),
        levelSubjectBranches: computed(() => state.levelSubjectBranches),
        units: computed(() => state.units),
        learningOutcomes: computed(() => state.learningOutcomes),
        lessons: computed(() => state.lessons),
        questions: computed(() => state.questions),
        answers: computed(() => state.answers),
        exams: computed(() => state.exams),
        students: computed(() => state.students),
        examSchedules: computed(() => state.examSchedules),
        examPeriods: computed(() => state.examPeriods),
        
        getAll(entity) { return state[entity] || [] },
        getById(entity, id) {
            const items = state[entity]
            if (!items) return null
            return items.find(item => item.id == id)
        },
        update(entity, id, updatedItem) {
            const items = state[entity]
            if (!items) return
            const index = items.findIndex(item => item.id == id)
            if (index !== -1) {
                items[index] = { ...items[index], ...updatedItem }
            }
        },
        remove(entity, id) {
            if (state[entity]) {
                state[entity] = state[entity].filter(item => item.id != id)
            }
        },
        add(entity, item) {
            if (state[entity]) state[entity].push(item)
        },
        create(entity, item) {
            const newItem = { id: Date.now() + Math.floor(Math.random() * 1000), ...item }
            if (state[entity]) state[entity].push(newItem)
            return newItem
        },
        
        async _fetchAndCache(entity, fetchFn) {
            state.loading[entity] = true
            state.errors[entity] = null
            try { 
                const res = await fetchFn()
                state[entity] = (Array.isArray(res) ? res : (res?.results || res?.data)) || []
            } 
            catch (e) { state.errors[entity] = e.message || 'Error loading data' } 
            finally { state.loading[entity] = false }
        },

        async fetchUsers() { await this._fetchAndCache('users', () => usersService.getAll()) },
        async fetchOrganizations() { await this._fetchAndCache('organizations', () => academicService.getOrganizations()) },
        async fetchYears() { await this._fetchAndCache('years', () => academicService.getAcademicYears()) },
        async fetchTracks() { await this._fetchAndCache('tracks', () => academicService.getTracks()) },
        async fetchClassTracks() { await this._fetchAndCache('classTracks', () => academicService.getClassTracks()) },
        async fetchClassSubjects() { await this._fetchAndCache('classSubjects', () => academicService.getClassSubjects()) },
        async fetchSemesters() { await this._fetchAndCache('semesters', () => academicService.getSemesters()) },
        async fetchBranches() { await this._fetchAndCache('branches', () => academicService.getTracks()) },
        async fetchStages() { await this._fetchAndCache('stages', () => academicService.getStages()) },
        async fetchLevels() { await this._fetchAndCache('levels', () => academicService.getLevels()) },
        async fetchSubjects() { await this._fetchAndCache('subjects', () => academicService.getSubjects()) },
        async fetchLevelSubjectBranches() { await this._fetchAndCache('levelSubjectBranches', () => academicService.getClassSubjects()) },
        async fetchUnits() { await this._fetchAndCache('units', () => academicService.getUnits()) },
        async fetchLearningOutcomes() { await this._fetchAndCache('learningOutcomes', () => academicService.getLearningOutcomes()) },
        async fetchLessons() { await this._fetchAndCache('lessons', () => academicService.getLessons()) },
        async fetchQuestions() { await this._fetchAndCache('questions', () => bankService.getQuestions({ page_size: 1000 })) },
        async fetchAnswers() { await this._fetchAndCache('answers', () => bankService.getAnswers()) },
        async fetchStudents() { await this._fetchAndCache('students', () => academicService.getStudents()) },
        async fetchExams() { await this._fetchAndCache('exams', () => examsService.getExams()) },
        async fetchExamSchedules() { await this._fetchAndCache('examSchedules', () => examsService.getExamSchedules()) },
        async fetchExamPeriods() { await this._fetchAndCache('examPeriods', () => academicService.getExamPeriods()) },
        async fetchExamVersions() { await this._fetchAndCache('examVersions', () => examsService.getExamVersions()) },
        async fetchExamQuestionOrders() { await this._fetchAndCache('examQuestionOrders', () => examsService.getExamQuestionOrders()) },
        async fetchStudentExamRegistrations() { await this._fetchAndCache('studentExamRegistrations', () => examsService.getStudentExamRegistrations()) },
        async fetchExamGenerationSettings() { await this._fetchAndCache('examGenerationSettings', () => examsService.getExamSettings()) },

        async loadAcademicData() {
            await Promise.all([
                this.fetchStages(), this.fetchLevels(), this.fetchSubjects(), this.fetchTracks(),
                this.fetchClassTracks(), this.fetchClassSubjects(), this.fetchSemesters(),
                this.fetchUnits(), this.fetchLearningOutcomes(), this.fetchLessons(),
                this.fetchYears(), this.fetchExamPeriods()
            ])
        }
    }
}
