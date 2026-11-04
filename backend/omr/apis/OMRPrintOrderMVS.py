from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions, status
from django.utils import timezone
from datetime import datetime

from exams.models.Exam import Exam
from omr.models.OMRPrintOrder import OMRPrintOrder

class OMRPrintOrderMVS(ViewSet):
    """
    ViewSet for managing official OMR print orders, approval, scheduling, and stage transitions.
    Endpoint: /api/omr/print-orders/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        orders = OMRPrintOrder.objects.filter(is_deleted=False).select_related('exam')
        results = []
        for o in orders:
            results.append({
                "id": o.id,
                "order_number": o.order_number,
                "exam_id": o.exam_id,
                "exam_title": o.exam.title if o.exam else "",
                "exam_code": o.exam.uniqueCode if o.exam else "",
                "status": o.status,
                "scheduled_print_date": o.scheduled_print_date.strftime("%Y-%m-%d") if o.scheduled_print_date else "",
                "press_name": o.press_name,
                "return_reason": o.return_reason or "",
                "return_notes": o.return_notes or "",
                "advance_reason": o.advance_reason or "",
                "advance_auth_doc": o.advance_auth_doc or "",
                "batch_id": o.batch_id or "",
                "printed_at": o.printed_at.strftime("%Y-%m-%d %H:%M:%S") if o.printed_at else "",
                "reprinted_count": o.reprinted_count,
                "responsible_officer": o.responsible_officer or "",
                "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else "",
            })
        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request):
        """
        Create or update a print order in 'pending' status (awaiting committee approval).
        Payload: {
            exam_id: 3,
            order_number: 'PRN-REQ-...',
            scheduled_print_date: '...',
            press_name: '...',
            responsible_officer: '...',
        }
        """
        exam_id = request.data.get('exam_id')
        if not exam_id:
            return Response({"success": False, "message": "معرف الاختبار مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Exam.objects.get(pk=exam_id, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        scheduled_date_str = request.data.get('scheduled_print_date')
        press_name = request.data.get('press_name') or 'المطبعة السرية المركزية (ديوان الوزارة)'
        responsible_officer = request.data.get('responsible_officer') or 'مدير إدارة الامتحانات'

        sched_date = None
        if scheduled_date_str:
            try:
                sched_date = datetime.strptime(scheduled_date_str, "%Y-%m-%d").date()
            except ValueError:
                sched_date = None

        order_num = request.data.get('order_number') or f"PRN-REQ-{exam.uniqueCode or exam.id}"
        order, created = OMRPrintOrder.objects.get_or_create(
            exam=exam,
            defaults={
                "order_number": order_num,
                "scheduled_print_date": sched_date,
                "press_name": press_name,
                "status": OMRPrintOrder.Status.PENDING,
                "responsible_officer": responsible_officer,
            }
        )

        if not created:
            order.order_number = order_num
            order.status = OMRPrintOrder.Status.PENDING
            order.scheduled_print_date = sched_date
            order.press_name = press_name
            order.responsible_officer = responsible_officer
            order.return_reason = None
            order.return_notes = None
            order.save()

        return Response({
            "success": True,
            "message": f"تم تسجيل وإرسال طلب طباعة الاختبار {exam.title} بنجاح برقم {order.order_number}، وهو بانتظار الاعتماد الرسمي",
            "order": {
                "id": order.id,
                "order_number": order.order_number,
                "exam_id": exam.id,
                "status": order.status,
                "scheduled_print_date": str(order.scheduled_print_date) if order.scheduled_print_date else "",
                "press_name": order.press_name,
            }
        })

    @action(detail=False, methods=['post'], url_path='approve')
    def approve_order(self, request):
        """
        Approve and schedule an exam print order.
        Payload: { exam_id: 3, scheduled_print_date: '2026-11-02', press_name: '...' }
        """
        exam_id = request.data.get('exam_id')
        if not exam_id:
            return Response({"success": False, "message": "معرف الاختبار مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Exam.objects.get(pk=exam_id, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        scheduled_date_str = request.data.get('scheduled_print_date')
        press_name = request.data.get('press_name') or 'المطبعة السرية المركزية (ديوان الوزارة)'

        sched_date = None
        if scheduled_date_str:
            try:
                sched_date = datetime.strptime(scheduled_date_str, "%Y-%m-%d").date()
            except ValueError:
                sched_date = timezone.now().date()
        else:
            sched_date = timezone.now().date()

        today = timezone.now().date()
        target_status = OMRPrintOrder.Status.SCHEDULED if sched_date > today else OMRPrintOrder.Status.READY

        order_num = request.data.get('order_number') or f"PRN-REQ-{exam.uniqueCode or exam.id}"
        responsible_officer = request.data.get('responsible_officer') or 'مدير إدارة الامتحانات'
        order, created = OMRPrintOrder.objects.get_or_create(
            exam=exam,
            defaults={
                "order_number": order_num,
                "scheduled_print_date": sched_date,
                "press_name": press_name,
                "status": target_status,
                "responsible_officer": responsible_officer,
            }
        )

        if not created:
            order.status = target_status
            order.scheduled_print_date = sched_date
            order.press_name = press_name
            order.responsible_officer = responsible_officer
            order.return_reason = None
            order.return_notes = None
            order.save()

        return Response({
            "success": True,
            "message": f"تم اعتماد وجدولة طلب الطباعة بنجاح للاختبار {exam.title}",
            "order": {
                "order_number": order.order_number,
                "exam_id": exam.id,
                "status": order.status,
                "scheduled_print_date": str(order.scheduled_print_date),
                "press_name": order.press_name,
            }
        })

    @action(detail=False, methods=['post'], url_path='return-order')
    def return_order(self, request):
        """
        Return a print order for modification.
        Payload: { exam_id: 3, return_reason: '...', return_notes: '...' }
        """
        exam_id = request.data.get('exam_id')
        if not exam_id:
            return Response({"success": False, "message": "معرف الاختبار مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Exam.objects.get(pk=exam_id, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        return_reason = request.data.get('return_reason') or 'كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض'
        return_notes = request.data.get('return_notes') or ''

        order_num = f"PRN-REQ-{exam.uniqueCode or exam.id}"
        order, created = OMRPrintOrder.objects.get_or_create(
            exam=exam,
            defaults={
                "order_number": order_num,
                "status": OMRPrintOrder.Status.FAILED,
                "return_reason": return_reason,
                "return_notes": return_notes,
            }
        )

        if not created:
            order.status = OMRPrintOrder.Status.FAILED
            order.return_reason = return_reason
            order.return_notes = return_notes
            order.save()

        return Response({
            "success": True,
            "message": f"تم إرجاع طلب طباعة الاختبار {exam.title} للتعديل والمراجعة",
            "order": {
                "order_number": order.order_number,
                "status": order.status,
                "return_reason": order.return_reason,
            }
        })

    @action(detail=False, methods=['post'], url_path='advance')
    def advance_schedule(self, request):
        """
        Advance scheduled print date to today with authorization.
        Payload: { exam_id: 3, advance_reason: '...', advance_auth_doc: '...' }
        """
        exam_id = request.data.get('exam_id')
        if not exam_id:
            return Response({"success": False, "message": "معرف الاختبار مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Exam.objects.get(pk=exam_id, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        advance_reason = request.data.get('advance_reason') or ''
        advance_auth_doc = request.data.get('advance_auth_doc') or ''
        today = timezone.now().date()

        order_num = f"PRN-REQ-{exam.uniqueCode or exam.id}"
        order, created = OMRPrintOrder.objects.get_or_create(
            exam=exam,
            defaults={
                "order_number": order_num,
                "status": OMRPrintOrder.Status.READY,
                "scheduled_print_date": today,
                "advance_reason": advance_reason,
                "advance_auth_doc": advance_auth_doc,
            }
        )

        if not created:
            order.status = OMRPrintOrder.Status.READY
            order.scheduled_print_date = today
            order.advance_reason = advance_reason
            order.advance_auth_doc = advance_auth_doc
            order.return_reason = None
            order.return_notes = None
            order.save()

        return Response({
            "success": True,
            "message": f"تم تقديم موعد طباعة الاختبار {exam.title} لليوم بنجاح ({today})",
            "order": {
                "order_number": order.order_number,
                "status": order.status,
                "scheduled_print_date": str(order.scheduled_print_date),
            }
        })
