from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from bank.models.AuditLog import AuditLog
from bank.serializers.AuditLog import AuditLogSerializer

class AuditLogMVS(AllMVS):
    """
    Dedicated ModelViewSet for Historical System Audit & Compliance Logs.
    Endpoint: /api/bank/audit-logs/
    Used by: AuditLogsView.vue
    Required for: System Accountability, Anti-tampering History, Security & User Audits.

    Backend Responsibilities:
    1. Server-side Query filtering (Action, Resource Type, User, Date range, IP address, Search query).
    2. Real-time Database Stats aggregation (Total operations, Creates, Updates, Deletions, Approvals).
    3. Immutability guarantee: Read-only querysets for non-superusers.
    4. Eager loading of User details.
    """
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        action_filter = self.request.query_params.get('action')
        if action_filter:
            qs = qs.filter(action=action_filter)

        resource_type = self.request.query_params.get('resource_type')
        if resource_type:
            qs = qs.filter(resource_type__icontains=resource_type)

        user_id = self.request.query_params.get('user') or self.request.query_params.get('user_id')
        if user_id:
            qs = qs.filter(user_id=user_id)

        date_from = self.request.query_params.get('date_from')
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(description__icontains=search) |
                Q(resource_type__icontains=search) |
                Q(resource_id__icontains=search) |
                Q(ip_address__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        return qs.order_by('-id')

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Calculates audit logs distribution summary."""
        qs = self.get_queryset()
        aggregates = qs.aggregate(
            total=Count('id'),
            creates=Count('id', filter=Q(action=AuditLog.ActionChoices.CREATE)),
            updates=Count('id', filter=Q(action=AuditLog.ActionChoices.UPDATE)),
            deletes=Count('id', filter=Q(action=AuditLog.ActionChoices.DELETE)),
            approvals=Count('id', filter=Q(action=AuditLog.ActionChoices.APPROVE))
        )
        return Response({
            "total_logs": aggregates['total'] or 0,
            "creates_count": aggregates['creates'] or 0,
            "updates_count": aggregates['updates'] or 0,
            "deletes_count": aggregates['deletes'] or 0,
            "approvals_count": aggregates['approvals'] or 0
        })
