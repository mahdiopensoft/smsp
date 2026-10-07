from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from templates_engine.models.ExamTemplate import ExamTemplate
from templates_engine.serializers.ExamTemplate import ExamTemplateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import os
import re
import json
import hashlib
from core.contracts import TemplateContract
from templates_engine.builder import TemplateBuilderService
from templates_engine.validator import TemplateValidatorService

from rest_framework import permissions

class ExamTemplateMVS(AllMVS):
    permission_classes = [permissions.AllowAny]
    queryset = ExamTemplate.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExamTemplateSerializer
    enable_actions = ['all', 'select', 'list', 'second_list', 'filter', 'filter_paginate', 'retrieve', 'create', 'update', 'partial_update', 'destroy']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'page' in request.query_params:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "results": serializer.data,
            "data": serializer.data,
            "count": len(serializer.data)
        })

    def _prepare_data_with_geometry(self, data):
        if 'template_data' in data and isinstance(data['template_data'], dict):
            td = data['template_data']
            try:
                builder = TemplateBuilderService()
                contract = builder.build_from_designer_config(td)
                c_dict = contract.model_dump()
                td['fiducial_marks'] = c_dict.get('fiducial_marks', [])
                td['mcq_questions'] = c_dict.get('mcq_questions', [])
                td['barcode_region'] = c_dict.get('barcode_region')
                td['paper_size'] = c_dict.get('paper_size', 'A5')
                data['total_mcq'] = len(c_dict.get('mcq_questions', []))
                if c_dict.get('paper_size') == 'A5':
                    data['paper_width_mm'] = 210.0
                    data['paper_height_mm'] = 148.5
                    if 'paper' not in td:
                        td['paper'] = {}
                    td['paper']['size'] = 'A5'
                    td['paper']['width_mm'] = 210.0
                    td['paper']['height_mm'] = 148.5
                elif c_dict.get('paper_size') == 'A4':
                    data['paper_width_mm'] = 210.0
                    data['paper_height_mm'] = 297.0
                    if 'paper' not in td:
                        td['paper'] = {}
                    td['paper']['size'] = 'A4'
                    td['paper']['width_mm'] = 210.0
                    td['paper']['height_mm'] = 297.0
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning("Failed to auto-compile template geometry: %s", e)
        return data

    def create(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        data = self._prepare_data_with_geometry(data)
        name = str(data.get('name', '')).strip()
        version = str(data.get('version', '1.0')).strip()

        if not name:
            return Response({"error": "اسم القالب مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if an active template with this name and version exists
        existing = ExamTemplate.objects.filter(name=name, version=version, is_deleted=False).first()
        if existing:
            # If explicit overwrite or same db_id passed: update existing
            if data.get('overwrite', False) or (data.get('db_id') and str(data.get('db_id')) == str(existing.id)):
                serializer = self.get_serializer(existing, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    "success": True,
                    "message": "✅ تم تحديث القالب الحالي بنجاح",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                # Auto-bump version (e.g. 1.0 -> 1.1, 1.2, etc.)
                parts = version.split('.')
                try:
                    minor = int(parts[-1]) + 1
                    new_version = '.'.join(parts[:-1] + [str(minor)])
                except (ValueError, IndexError):
                    new_version = f"{version}.1"

                v_num = 1
                while ExamTemplate.objects.filter(name=name, version=new_version, is_deleted=False).exists():
                    v_num += 1
                    new_version = f"{version.split('.')[0]}.{v_num}"

                data['version'] = new_version
                if 'template_data' in data and isinstance(data['template_data'], dict):
                    data['template_data']['version'] = new_version

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "success": True,
            "message": "✅ تم إنشاء وحفظ القالب بنجاح",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        data = self._prepare_data_with_geometry(data)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "success": True,
            "message": "✅ تم تحديث القالب بنجاح",
            "data": serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def validate(self, request, pk=None):
        """Validate template data (check fiducials, no overlaps, integrity, etc.)."""
        template = self.get_object()
        if not template.template_data:
            return Response({"success": False, "issues": ["No template data provided"]}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            contract = TemplateContract(**template.template_data)
            TemplateValidatorService.validate(contract)
            template.is_validated = True
            template.save(update_fields=["is_validated"])
            return Response({"success": True, "message": "Template is valid"})
        except Exception as e:
            template.is_validated = False
            template.save(update_fields=["is_validated"])
            return Response({"success": False, "issues": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate a geometric template manifest on-the-fly without saving it yet."""
        num_mcq = request.data.get("num_mcq")
        if num_mcq is None:
            return Response({"error": "num_mcq is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            num_mcq = int(num_mcq)
        except ValueError:
            return Response({"error": "num_mcq must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
            
        choices_count = request.data.get("choices_count", 4)
        try:
            choices_count = int(choices_count)
        except ValueError:
            choices_count = 4
            
        template_id = request.data.get("template_id", "TEMP_" + str(num_mcq))
        paper_width = float(request.data.get("paper_width_mm", 210.0))
        paper_height = float(request.data.get("paper_height_mm", 297.0))
        
        builder = TemplateBuilderService(paper_width_mm=paper_width, paper_height_mm=paper_height)
        template_contract = builder.build_template(template_id=template_id, num_mcq=num_mcq, choices_count=choices_count)
        
        return Response(template_contract.model_dump())

    @action(detail=False, methods=["post"], url_path="generate-and-save")
    def generate_and_save(self, request):
        """
        Receives UI parameters from TemplateBuilderView, computes ALL bubble coordinates via
        build_dynamic_template(), persists to ExamTemplate in the database,
        and returns the template_id and db_id so the frontend can use it.
        """
        data = request.data

        name = str(data.get("name", "")).strip()
        if not name:
            return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)

        template_id = str(data.get("template_id", "")).strip()
        if not template_id:
            template_id = re.sub(r"[^A-Za-z0-9_]", "_", name).upper()[:30] or "CUSTOM"

        try:
            num_questions     = int(data.get("num_questions", 100))
            choices_count     = int(data.get("choices_count", 4))
            columns_count     = int(data.get("columns_count", 4))
            bubble_radius_mm  = float(data.get("bubble_radius_mm", 1.7))
            row_spacing_mm    = float(data.get("row_spacing_mm", 4.2))
            choice_spacing_mm = float(data.get("choice_spacing_mm", 9.0))
            start_y_mm        = float(data.get("start_y_mm", 96.1))
            scan_dpi          = int(data.get("scan_dpi", 300))
            version           = str(data.get("version", "1.0.0"))
            paper_size        = str(data.get("paper_size", "A4"))
            choice_labels     = data.get("choice_labels", None)
            if isinstance(choice_labels, str):
                choice_labels = json.loads(choice_labels)
        except (ValueError, TypeError) as e:
            return Response({"error": f"Invalid parameter: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            builder = TemplateBuilderService()
            template_contract = builder.build_dynamic_template(
                template_id=template_id,
                template_name=name,
                version=version,
                num_questions=num_questions,
                choices_count=choices_count,
                choice_labels=choice_labels,
                columns_count=columns_count,
                bubble_radius_mm=bubble_radius_mm,
                row_spacing_mm=row_spacing_mm,
                choice_spacing_mm=choice_spacing_mm,
                start_y_mm=start_y_mm,
                paper_size=paper_size,
                scan_dpi=scan_dpi,
                layout_direction=data.get("layout_direction", "rtl"),
            )
        except Exception as e:
            return Response({"error": f"Template generation failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            paper_dims = {"A4": (210, 297), "A3": (297, 420), "Letter": (216, 279)}
            pw, ph = paper_dims.get(paper_size, (210, 297))

            user_desc = str(data.get("description", "")).strip()
            final_desc = user_desc if user_desc else f"Dynamic template — {num_questions}q × {choices_count}c × {columns_count}col"

            t_data = template_contract.model_dump()
            t_data["metadata"] = {
                "num_questions": num_questions,
                "choices_count": choices_count,
                "choice_labels": choice_labels,
                "columns_count": columns_count,
                "bubble_radius_mm": bubble_radius_mm,
                "row_spacing_mm": row_spacing_mm,
                "layout_direction": data.get("layout_direction", "rtl"),
            }

            db_id = data.get("db_id")
            if db_id and ExamTemplate.objects.filter(id=db_id).exists():
                obj = ExamTemplate.objects.get(id=db_id)
                obj.name = name
                obj.version = version
                obj.description = final_desc
                obj.template_data = t_data
                obj.paper_width_mm = pw
                obj.paper_height_mm = ph
                obj.dpi = scan_dpi
                obj.save()
                created = False
            else:
                obj, created = ExamTemplate.objects.update_or_create(
                    name=name,
                    version=version,
                    defaults={
                        "description": final_desc,
                        "template_data": t_data,
                        "paper_width_mm": pw,
                        "paper_height_mm": ph,
                        "dpi": scan_dpi,
                        "is_active": True,
                        "is_validated": True,
                        "created_by": request.user if request.user.is_authenticated else None,
                    },
                )
        except Exception as e:
            return Response({"error": f"Database save failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        total_bubbles = sum(len(q["choices"]) for q in template_contract.model_dump()["mcq_questions"])

        return Response({
            "db_id":           str(obj.id),
            "template_id":     template_id,
            "name":            name,
            "version":         version,
            "total_questions": num_questions,
            "total_bubbles":   total_bubbles,
            "columns_count":   columns_count,
            "bubble_radius_mm": bubble_radius_mm,
            "hash":            template_contract.template_hash,
            "created":         created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="config/(?P<config_name>[^/.]+)")
    def get_config(self, request, config_name=None):
        """GET /api/templates-engine/exam-templates/config/<config_name>/"""
        try:
            config = TemplateBuilderService._load_template_config(config_name)
            return Response(config)
        except FileNotFoundError:
            return Response(
                {"error": f"Template config '{config_name}' not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"], url_path="configs")
    def list_configs(self, request):
        """GET /api/templates-engine/exam-templates/configs/"""
        configs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
        if not os.path.exists(configs_dir):
            return Response({"configs": []})
        
        configs = []
        for f in os.listdir(configs_dir):
            if f.endswith(".json"):
                config_name = f.replace(".json", "")
                try:
                    config = TemplateBuilderService._load_template_config(config_name)
                    configs.append({
                        "config_name": config_name,
                        "template_id": config.get("template_id", ""),
                        "template_name": config.get("template_name", ""),
                        "version": config.get("version", ""),
                        "total_questions": config.get("questions", {}).get("count", 0),
                        "paper_size": config.get("paper", {}).get("size", "A4"),
                    })
                except Exception:
                    pass
        return Response({"configs": configs})

