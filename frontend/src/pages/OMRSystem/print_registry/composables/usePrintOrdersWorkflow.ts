import { ref, computed, watch, type Ref } from 'vue'
import api from '@/services/omr/client.js'

export interface UsePrintOrdersWorkflowOptions {
  filteredMasterExamsTable: Ref<any[]>
  batchPrintNotification: Ref<{ show: boolean; message: string; color: string }>
  loadMasterData: () => Promise<void> | void
  onSelectExam?: (exam: any) => void
}

export function usePrintOrdersWorkflow(options: UsePrintOrdersWorkflowOptions) {
  const {
    filteredMasterExamsTable,
    batchPrintNotification,
    loadMasterData,
  } = options

  // ── Sub-tabs for "الاختبارات المعتمدة للطباعة" (الطلبات / المجدولة / المستحقة / المكتملة / الملغية / السجل الشامل) ──
  const examSubTab = ref<'orders' | 'scheduled' | 'due' | 'completed' | 'cancelled' | 'all'>('orders')
  const savedPrintOrders = ref<any[]>([])
  const manifestDialog = ref(false)
  const selectedManifestOrder = ref<any>(null)

  // ── In-Flight Request Deduplication & Cache for Print Orders ──
  let printOrdersPromise: Promise<any[]> | null = null
  let lastPrintOrdersFetchTime = 0
  const PRINT_ORDERS_CACHE_TTL = 8000 // 8 ثوانٍ كحد أقصى لمنع الطلبات المكررة

  const loadSavedPrintOrders = async (force = false) => {
    const now = Date.now()
    if (!force && savedPrintOrders.value.length > 0 && (now - lastPrintOrdersFetchTime < PRINT_ORDERS_CACHE_TTL)) {
      return savedPrintOrders.value
    }
    if (printOrdersPromise) {
      return printOrdersPromise
    }

    printOrdersPromise = (async () => {
      try {
        const res = await api.get('/api/omr/print-orders/', { skipInterceptor: true })
        if (res.data && res.data.success) {
          savedPrintOrders.value = res.data.results || []
          lastPrintOrdersFetchTime = Date.now()
        }
      } catch (err: any) {
        console.error('[OMR Registry API Error] فشل في تحميل أوامر الطباعة المحفوظة:', {
          operation: 'loadSavedPrintOrders',
          endpoint: '/api/omr/print-orders/',
          error: err?.message || err,
        })
      } finally {
        printOrdersPromise = null
      }
      return savedPrintOrders.value
    })()

    return printOrdersPromise
  }

  // ── Indexed Map for O(1) Strict Print Order Matching ──
  const savedPrintOrdersMap = computed(() => {
    const map = new Map<string, any>()
    for (const o of (savedPrintOrders.value || [])) {
      if (!o) continue
      if (o.exam_id !== undefined && o.exam_id !== null) {
        map.set(String(o.exam_id), o)
      }
      if (o.exam_code) {
        map.set(`code_${String(o.exam_code).trim().toLowerCase()}`, o)
      }
    }
    return map
  })

  const getPrintOrderForExam = (exam: any) => {
    if (!exam) return null
    const map = savedPrintOrdersMap.value
    if (exam.id !== undefined && exam.id !== null && map.has(String(exam.id))) {
      return map.get(String(exam.id))
    }
    if (exam.uniqueCode && map.has(`code_${String(exam.uniqueCode).trim().toLowerCase()}`)) {
      return map.get(`code_${String(exam.uniqueCode).trim().toLowerCase()}`)
    }
    return null
  }

  // ── Robust Calendar Date Parsing & Comparison ──
  const parseCalendarDate = (dateVal: any): number | null => {
    if (!dateVal) return null
    if (dateVal instanceof Date) {
      return isNaN(dateVal.getTime()) ? null : new Date(dateVal.getFullYear(), dateVal.getMonth(), dateVal.getDate()).getTime()
    }
    const str = String(dateVal).trim()
    const isoMatch = str.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/)
    if (isoMatch) {
      return new Date(Number(isoMatch[1]), Number(isoMatch[2]) - 1, Number(isoMatch[3])).getTime()
    }
    const d = new Date(str)
    return isNaN(d.getTime()) ? null : new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime()
  }

  const getTodayIso = (): string => {
    const d = new Date()
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  const previewOrderManifest = (exam: any) => {
    const order = getPrintOrderForExam(exam)
    if (order) {
      selectedManifestOrder.value = {
        ...order,
        exam_title: exam.title || order.exam_title || '',
        subject_name: exam.subject_name || order.subject_name || '',
        grand_total: exam.total_registered || exam.total_students || order.grand_total || 0,
        actual_exam_date: exam.exam_date || order.actual_exam_date || '',
      }
    } else {
      selectedManifestOrder.value = {
        order_number: exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id}`,
        exam_id: exam.id,
        exam_title: exam.title || '',
        exam_code: exam.uniqueCode || '',
        subject_name: exam.subject_name || '',
        press_name: exam.press_name || '',
        scheduled_print_date: exam.scheduled_print_date || getTodayIso(),
        actual_exam_date: exam.exam_date || exam.actual_exam_date || getTodayIso(),
        status: exam.order_status || 'approved',
        grand_total: exam.total_registered || exam.total_students || 0,
      }
    }
    manifestDialog.value = true
  }

  const enrichedMasterExamsList = computed(() => {
    try {
      const baseList = filteredMasterExamsTable.value || []
      const todayTs = parseCalendarDate(new Date())

      return baseList.filter(Boolean).map(exam => {
        try {
          const order = getPrintOrderForExam(exam)

          const rawStatus = order?.status || (exam.order_status || 'pending')
          const scheduledDate = order?.scheduled_print_date || exam.scheduled_print_date || null
          const examDate = order?.actual_exam_date || exam.exam_date || null
          const orderNumber = order?.order_number || exam.order_number || null
          const pressName = order?.press_name || exam.press_name || null
          const grandTotal = order?.grand_total || (exam.total_registered || exam.total_students || 0)
          const returnReason = order?.return_reason || exam.return_reason || ''
          const returnNotes = order?.return_notes || exam.return_notes || ''

          const isFullyPrinted = (Number(exam.printed_rate) >= 100) || (exam.print_status === 'full') || (exam.print_status === 'printed') || rawStatus === 'completed'
          const isFailed = rawStatus === 'failed' || rawStatus === 'returned'
          const isCancelled = rawStatus === 'cancelled'

          // 1. Completed: 100% printed or status completed
          const isCompleted = isFullyPrinted

          // 2. Returned / Failed
          const isReturned = !isCompleted && isFailed

          // 3. Pending: incoming request not yet approved by committee
          const isPending = !isCompleted && !isReturned && !isCancelled && (rawStatus === 'pending')

          // 4. Scheduled: approved with future print date (> today)
          const schedTs = parseCalendarDate(scheduledDate)
          const isSchedInFuture = schedTs !== null && todayTs !== null && schedTs > todayTs
          const isScheduled = !isCompleted && !isReturned && !isCancelled && !isPending && (rawStatus === 'scheduled' || isSchedInFuture)

          // 5. Due: approved with print date today or earlier (<= today), or in active printing
          const isSchedDue = schedTs !== null && todayTs !== null && schedTs <= todayTs
          const isDue = !isCompleted && !isReturned && !isCancelled && !isPending && !isScheduled && (rawStatus === 'ready' || rawStatus === 'printing' || isSchedDue || rawStatus === 'approved')

          const effectiveStatus = isCompleted ? 'completed' :
                                 (isReturned ? 'failed' :
                                 (isScheduled ? 'scheduled' :
                                 (isDue ? (rawStatus === 'printing' ? 'printing' : 'ready') :
                                 (isCancelled ? 'cancelled' : 'pending'))))

          return {
            ...exam,
            has_order: !!order || !!exam.order_number,
            order_status: effectiveStatus,
            raw_order_status: rawStatus,
            return_reason: returnReason,
            return_notes: returnNotes,
            order_number: orderNumber,
            scheduled_print_date: scheduledDate,
            actual_exam_date: examDate,
            press_name: pressName,
            total_to_print: grandTotal,
            is_pending: isPending,
            is_returned: isReturned,
            is_approved: !isPending && !isReturned && !isCancelled,
            is_scheduled: isScheduled,
            is_due: isDue,
            is_completed: isCompleted,
          }
        } catch (itemErr) {
          console.error('Error enriching exam item:', exam, itemErr)
          return exam
        }
      })
    } catch (err) {
      console.error('Error in enrichedMasterExamsList:', err)
      return filteredMasterExamsTable.value || []
    }
  })

  // ── Dialog States & Handlers for Print Orders Workflow ──
  const approveOrderDialog = ref(false)
  const targetExamForApproval = ref<any>(null)
  const actionLoading = ref(false)

  const getCurrentUserOfficerName = () => {
    try {
      const raw = localStorage.getItem('auth_user') || localStorage.getItem('profile')
      if (raw) {
        const u = JSON.parse(raw)
        return u.full_name || u.name || u.username || 'مدير إدارة الامتحانات والكنترول'
      }
    } catch (e) {}
    return 'مدير إدارة الامتحانات والكنترول'
  }

  const openApproveDialog = (exam: any) => {
    targetExamForApproval.value = exam
    approveOrderDialog.value = true
  }

  const onOrderApproved = async (payload: any) => {
    await loadSavedPrintOrders(true)
    await loadMasterData()

    const schedTs = parseCalendarDate(payload.scheduledDate)
    const todayTs = parseCalendarDate(new Date())
    const isFuture = schedTs !== null && todayTs !== null && schedTs > todayTs
    if (isFuture) {
      examSubTab.value = 'scheduled'
      batchPrintNotification.value = {
        show: true,
        color: 'info',
        message: `تم اعتماد وتوثيق أمر الطباعة بنجاح للاختبار "${payload.exam.title}"! تم نقله إلى تبويب [المجدولة] بموعد طباعة (${payload.scheduledDate}).`,
      }
    } else {
      examSubTab.value = 'due'
      batchPrintNotification.value = {
        show: true,
        color: 'success',
        message: `تم اعتماد وتوثيق أمر الطباعة بنجاح للاختبار "${payload.exam.title}"! تم نقله إلى تبويب [المستحقة] وهو جاهز للتنفيذ الفوري الآن.`,
      }
    }

    if (payload.openManifest) {
      previewOrderManifest(payload.exam)
    }
  }

  const returnOrderDialog = ref(false)
  const targetExamForReturn = ref<any>(null)
  const returnReasonSelected = ref('كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض')
  const returnNotesText = ref('')
  const predefinedReturnReasons = [
    'كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض',
    'نقص أو عدم تطابق في كشوفات الطلاب لبعض المراكز الامتحانية',
    'نماذج الأسئلة بحاجة لإعادة تدقيق ومراجعة فنية',
    'تعارض موعد الطباعة مع جدول تشغيل المطبعة المركزية',
    'أخرى (توضيح في الملاحظات أدناه)',
  ]

  const returnReasonsObjects = computed(() => {
    return predefinedReturnReasons.map(r => ({
      id: r,
      value: r,
      name: r,
      title: r,
    }))
  })

  const advanceScheduleDialog = ref(false)
  const targetExamForAdvance = ref<any>(null)
  const advanceReasonSelected = ref('شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)')
  const advanceAuthDoc = ref('')
  const advanceReasonsList = [
    'شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)',
    'توزيع أحمال ماكينات المطبعة المركزية وتفادي ضغط الأيام الأخيرة',
    'توجيه وزاري استثنائي لتقديم موعد الاختبار',
    'إجازة رسمية أو طارئ مناخي/أمني يستوجب الترحيل المبكر',
    'أخرى (مبرر إداري استثنائي)',
  ]

  const openReturnDialog = (exam: any) => {
    targetExamForReturn.value = exam
    returnReasonSelected.value = predefinedReturnReasons[0]
    returnNotesText.value = ''
    returnOrderDialog.value = true
  }

  const confirmOrderReturn = async () => {
    if (!targetExamForReturn.value) return
    actionLoading.value = true
    try {
      const exam = targetExamForReturn.value

      await api.post('/api/omr/print-orders/return-order/', {
        exam_id: exam.id,
        return_reason: returnReasonSelected.value,
        return_notes: returnNotesText.value,
      })

      await loadSavedPrintOrders(true)
      await loadMasterData()
      returnOrderDialog.value = false

      batchPrintNotification.value = {
        show: true,
        color: 'warning',
        message: `تم إرجاع طلب طباعة الاختبار "${exam.title}" للتعديل بنجاح: (${returnReasonSelected.value}). سيظهر كمرتجع في السجل وشاشة إدارة الاختبارات.`,
      }
    } catch (e: any) {
      console.error('[OMR Registry API Error] فشل في إرجاع طلب طباعة الاختبار:', {
        operation: 'confirmOrderReturn',
        examId: targetExamForReturn.value?.id,
        error: e,
      })
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: `تعذر إرجاع طلب الطباعة على الخادم: ${e?.response?.data?.message || e?.message || 'خطأ في الاتصال'}`,
      }
    } finally {
      actionLoading.value = false
    }
  }

  const openAdvanceScheduleDialog = (exam: any) => {
    targetExamForAdvance.value = exam
    advanceReasonSelected.value = advanceReasonsList[0]
    advanceAuthDoc.value = ''
    advanceScheduleDialog.value = true
  }

  const onConfirmAdvanceSchedule = async ({ exam, reason, authDoc }: any) => {
    const target = exam || targetExamForAdvance.value
    if (!target) return
    actionLoading.value = true
    try {
      await api.post('/api/omr/print-orders/advance/', {
        exam_id: target.id,
        advance_reason: reason || advanceReasonSelected.value,
        advance_auth_doc: authDoc || advanceAuthDoc.value,
      })

      await loadSavedPrintOrders(true)
      await loadMasterData()
      advanceScheduleDialog.value = false
      examSubTab.value = 'due'

      batchPrintNotification.value = {
        show: true,
        color: 'success',
        message: `تم تقديم موعد طباعة "${target.title}" لليوم وتوثيق التفويض رسمياً! تم نقله إلى تبويب [المستحقة] وهو جاهز للتنفيذ الفوري الآن.`,
      }
    } catch (e: any) {
      console.error('[OMR Registry API Error] فشل في تقديم موعد الطباعة:', {
        operation: 'onConfirmAdvanceSchedule',
        examId: target?.id,
        error: e,
      })
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: `تعذر تقديم موعد الطباعة على الخادم: ${e?.response?.data?.message || e?.message || 'خطأ في الاتصال'}`,
      }
    } finally {
      actionLoading.value = false
    }
  }

  // ── Cancel Print Order Handlers ──
  const cancelOrderDialog = ref(false)
  const targetExamForCancel = ref<any>(null)

  const openCancelOrderDialog = (exam: any) => {
    targetExamForCancel.value = exam
    cancelOrderDialog.value = true
  }

  const onConfirmCancelOrder = async ({ exam, reason, notes }: any) => {
    const target = exam || targetExamForCancel.value
    if (!target) return
    actionLoading.value = true
    try {
      const fullReason = (reason || 'تم إلغاء الاختبار بقرار من إدارة الامتحانات والكنترول') + (notes ? ` (${notes})` : '')

      await api.post('/api/omr/print-orders/cancel-order/', {
        exam_id: target.id,
        cancel_reason: fullReason,
      })

      target.order_status = 'cancelled'
      target.raw_order_status = 'cancelled'
      target.is_cancelled = true
      target.is_due = false
      target.is_scheduled = false
      target.return_reason = fullReason

      await Promise.all([
        loadSavedPrintOrders(),
        loadMasterData(),
      ])

      cancelOrderDialog.value = false
      examSubTab.value = 'cancelled'

      batchPrintNotification.value = {
        show: true,
        color: 'info',
        message: `تم إلغاء أمر طباعة "${target.title}" بنجاح وتوثيق القرار رسمياً! تم نقله إلى تبويب [الملغية].`,
      }
    } catch (err) {
      console.error('Failed to cancel order:', err)
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: 'تعذر إلغاء أمر الطباعة، يرجى المحاولة لاحقاً.',
      }
    } finally {
      actionLoading.value = false
    }
  }

  // ── Sub-tabs categorization lists and counts ──
  const allExamsList = computed(() => enrichedMasterExamsList.value || [])
  const pendingAndActiveOrdersList = computed(() => (enrichedMasterExamsList.value || []).filter(e => !e.is_completed && !e.is_cancelled && e.order_status !== 'cancelled'))
  const scheduledExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_scheduled))
  const dueExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_due))
  const completedExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_completed))
  const cancelledExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.order_status === 'cancelled' || e.raw_order_status === 'cancelled' || e.is_cancelled))

  const allExamsCount = computed(() => allExamsList.value.length)
  const pendingAndActiveOrdersCount = computed(() => pendingAndActiveOrdersList.value.length)
  const scheduledExamsCount = computed(() => scheduledExamsList.value.length)
  const dueExamsCount = computed(() => dueExamsList.value.length)
  const completedExamsCount = computed(() => completedExamsList.value.length)
  const cancelledExamsCount = computed(() => cancelledExamsList.value.length)

  const currentExamSubTabList = computed(() => {
    if (examSubTab.value === 'orders') return pendingAndActiveOrdersList.value
    if (examSubTab.value === 'scheduled') return scheduledExamsList.value
    if (examSubTab.value === 'due') return dueExamsList.value
    if (examSubTab.value === 'completed') return completedExamsList.value
    if (examSubTab.value === 'cancelled') return cancelledExamsList.value
    return allExamsList.value
  })

  // ── Master Table Items for custom-data-table ──
  const examMasterTableItems = ref({
    results: [] as any[],
    count: 0,
    pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
  })

  const examMasterSearchTerm = ref('')

  const getExamMasterData = async (params: any = {}) => {
    const p = params?.params || params || {}
    if (p.search !== undefined) {
      examMasterSearchTerm.value = (p.search || '').trim().toLowerCase()
    }
    const page = p.page || 1
    const pageSize = p.page_size || 20
    let all = currentExamSubTabList.value || []

    if (examMasterSearchTerm.value) {
      const q = examMasterSearchTerm.value
      all = all.filter(e => 
        (e.title && e.title.toLowerCase().includes(q)) ||
        (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
        (e.subject_name && e.subject_name.toLowerCase().includes(q)) ||
        (e.order_number && e.order_number.toLowerCase().includes(q)) ||
        (e.institution_name && e.institution_name.toLowerCase().includes(q)) ||
        (e.directorate_name && e.directorate_name.toLowerCase().includes(q)) ||
        (e.governorate_name && e.governorate_name.toLowerCase().includes(q))
      )
    }

    const start = (page - 1) * pageSize
    examMasterTableItems.value = {
      results: all.slice(start, start + pageSize),
      count: all.length,
      pagination: {
        count: all.length,
        total: all.length,
        num_pages: Math.ceil(all.length / pageSize) || 1,
        current_page: page,
      },
    }
    return examMasterTableItems.value
  }

  watch([currentExamSubTabList, examSubTab], () => {
    getExamMasterData()
  }, { immediate: true })

  return {
    examSubTab,
    savedPrintOrders,
    manifestDialog,
    selectedManifestOrder,
    loadSavedPrintOrders,
    savedPrintOrdersMap,
    getPrintOrderForExam,
    parseCalendarDate,
    getTodayIso,
    previewOrderManifest,
    enrichedMasterExamsList,
    approveOrderDialog,
    targetExamForApproval,
    actionLoading,
    getCurrentUserOfficerName,
    openApproveDialog,
    onOrderApproved,
    returnOrderDialog,
    targetExamForReturn,
    returnReasonSelected,
    returnNotesText,
    returnReasonsObjects,
    advanceScheduleDialog,
    targetExamForAdvance,
    advanceReasonSelected,
    advanceAuthDoc,
    advanceReasonsList,
    openReturnDialog,
    confirmOrderReturn,
    openAdvanceScheduleDialog,
    onConfirmAdvanceSchedule,
    cancelOrderDialog,
    targetExamForCancel,
    openCancelOrderDialog,
    onConfirmCancelOrder,
    allExamsList,
    pendingAndActiveOrdersList,
    scheduledExamsList,
    dueExamsList,
    completedExamsList,
    cancelledExamsList,
    allExamsCount,
    pendingAndActiveOrdersCount,
    scheduledExamsCount,
    dueExamsCount,
    completedExamsCount,
    cancelledExamsCount,
    currentExamSubTabList,
    examMasterTableItems,
    examMasterSearchTerm,
    getExamMasterData,
  }
}
