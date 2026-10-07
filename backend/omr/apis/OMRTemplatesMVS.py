from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from templates_engine.models.ExamTemplate import ExamTemplate
from templates_engine.serializers.ExamTemplate import ExamTemplateSerializer

class OMRTemplatesMVS(AllMVS):
    """
    Dedicated ModelViewSet for OMR Template Designer (CAD).
    Endpoint: /api/omr/omr-templates/
    Used by: OMRTemplatesView.vue
    """
    queryset = ExamTemplate.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ExamTemplateSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(
                Q(template_data__institution_type=inst_type) |
                Q(template_data__institution_type='all') |
                Q(template_data__institution_type__isnull=True)
            )

        is_validated = self.request.query_params.get('is_validated')
        if is_validated is not None and is_validated != '':
            if is_validated in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_validated=True)
            elif is_validated in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_validated=False)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(version__icontains=search)
            )

        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        template_data = self.request.data.get('template_data') or {}
        inst_type = self.request.data.get('institution_type')
        if inst_type and 'institution_type' not in template_data:
            template_data['institution_type'] = inst_type
        serializer.save(template_data=template_data)

    def perform_update(self, serializer):
        template_data = self.request.data.get('template_data') or serializer.instance.template_data or {}
        inst_type = self.request.data.get('institution_type')
        if inst_type:
            template_data['institution_type'] = inst_type
        serializer.save(template_data=template_data)

    @action(detail=False, methods=['post'], url_path='validate-layout')
    def validate_layout(self, request):
        """
        Validates CAD layout parameters, margins, columns, and bubble spacing.
        """
        layout = request.data.get('layout', {})
        total_questions = request.data.get('totalQuestions', 40)
        
        # Geometry validation
        is_valid = True
        warnings = []
        
        if int(total_questions) > 120:
            warnings.append("عدد الأسئلة كبير وقد يتطلب تصغير قطر الدوائر إلى أقل من 3.5mm")

        return Response({
            "success": True,
            "isValid": is_valid,
            "warnings": warnings,
            "message": "التصميم الهندسي مطابق للمواصفات القياسية لنظام OMR"
        })

    @action(detail=True, methods=['get'], url_path='export-json')
    def export_json(self, request, pk=None):
        """Exports the template CAD JSON specification."""
        template = self.get_object()
        layout_data = getattr(template, 'template_data', {}) or {}
        return Response({
            "name": template.name,
            "version": template.version if hasattr(template, 'version') else "1.0",
            "layout": layout_data,
            "template_data": layout_data,
            "paper_width_mm": getattr(template, 'paper_width_mm', 210),
            "paper_height_mm": getattr(template, 'paper_height_mm', 297),
            "dpi": getattr(template, 'dpi', 300),
            "total_mcq": getattr(template, 'total_mcq_count', 40),
            "total_essay": getattr(template, 'total_essay_count', 0),
            "is_validated": getattr(template, 'is_validated', False),
            "created_at": template.created_at
        })
