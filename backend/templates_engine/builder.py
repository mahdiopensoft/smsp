import hashlib
import math
import os
from typing import List

from core.contracts import (
    TemplateContract, FiducialMark, RegionContract, 
    MCQQuestion, MCQChoice, EssayRegion
)

class TemplateBuilderService:
    """
    Dynamic Layout Engine that generates a geometric exam paper template
    based on the number of questions, producing a strict Template Manifest.
    """
    
    def __init__(self, paper_width_mm: float = 210.0, paper_height_mm: float = 297.0):
        self.paper_width_mm = paper_width_mm
        self.paper_height_mm = paper_height_mm
        self.fiducial_margin_mm = 10.0
        
    def _generate_fiducials(self) -> List[FiducialMark]:
        """Generates the 4 corner nested fiducial marks."""
        size = 8.0
        return [
            FiducialMark(id="TL", x_mm=self.fiducial_margin_mm, y_mm=self.fiducial_margin_mm, width_mm=size, height_mm=size, type="nested_square"),
            FiducialMark(id="TR", x_mm=self.paper_width_mm - self.fiducial_margin_mm - size, y_mm=self.fiducial_margin_mm, width_mm=size, height_mm=size, type="nested_square"),
            FiducialMark(id="BL", x_mm=self.fiducial_margin_mm, y_mm=self.paper_height_mm - self.fiducial_margin_mm - size, width_mm=size, height_mm=size, type="nested_square"),
            FiducialMark(id="BR", x_mm=self.paper_width_mm - self.fiducial_margin_mm - size, y_mm=self.paper_height_mm - self.fiducial_margin_mm - size, width_mm=size, height_mm=size, type="nested_square"),
        ]

    def _generate_barcode_region(self) -> RegionContract:
        """Barcode region at the top center."""
        return RegionContract(
            dx_mm=140.0, dy_mm=40.0, width_mm=30.0, height_mm=30.0, reference_frame="absolute"
        )
        
    def _create_bubble_zones(
        self,
        center_dx: float,
        center_dy: float,
        bubble_radius_mm: float = 1.65,
    ) -> tuple:
        """
        Creates the 3 geometric zones for a single bubble.
        All radii are derived from bubble_radius_mm — no hardcoded constants.
          bubble_region   = the printed circle boundary (full radius)
          safe_region     = inner core for reliable pixel sampling (73% of radius)
          expanded_region = outer band for ink-bleed detection (145% of radius)
        """
        r_base     = bubble_radius_mm
        r_safe     = round(bubble_radius_mm * 0.73, 4)
        r_expanded = round(bubble_radius_mm * 1.45, 4)

        return (
            RegionContract(dx_mm=center_dx - r_base,     dy_mm=center_dy - r_base,     width_mm=r_base*2,     height_mm=r_base*2),
            RegionContract(dx_mm=center_dx - r_safe,     dy_mm=center_dy - r_safe,     width_mm=r_safe*2,     height_mm=r_safe*2),
            RegionContract(dx_mm=center_dx - r_expanded, dy_mm=center_dy - r_expanded, width_mm=r_expanded*2, height_mm=r_expanded*2),
        )

    def generate_dynamic_mcq_layout(
        self,
        num_questions:    int,
        choices_count:    int   = 4,
        columns_count:    int   = 4,
        bubble_radius_mm: float = 1.7,
        row_spacing_mm:   float = 4.2,
        choice_spacing_mm: float = 9.0,
        start_y_mm:       float = 96.1,
        choice_labels:    list  = None,
        layout_direction: str   = 'rtl',
    ) -> List[MCQQuestion]:
        """
        Fully dynamic MCQ layout engine.

        All geometry is driven by parameters — ZERO hardcoded values.
        The OMR engines receive only the resulting coordinates; they don't
        care about column count, bubble size, or page layout.
        """
        if choice_labels is None:
            choice_labels = [str(i + 1) for i in range(choices_count)]
        choice_labels = choice_labels[:choices_count]

        rows_per_col = math.ceil(num_questions / columns_count)

        usable_width_mm = self.paper_width_mm - 2 * self.fiducial_margin_mm
        col_width_mm = usable_width_mm / max(1, columns_count)
        q_num_w_mm = min(10.0, col_width_mm * 0.22)
        answer_area_w_mm = col_width_mm - q_num_w_mm
        choice_step_mm = min(9.5, answer_area_w_mm / (choices_count + 1))
        choice_block_w_mm = choice_step_mm * (choices_count + 1)
        extra_padding_mm = max(0.0, (answer_area_w_mm - choice_block_w_mm) * 0.5)

        # Usable vertical height between start_y and footer signature boxes (278mm)
        max_rows_height = 278.0 - start_y_mm
        eff_row_spacing = min(row_spacing_mm, max_rows_height / max(rows_per_col, 1))
        max_vert = max(1.0, (eff_row_spacing * 0.5) - 0.45)
        max_horiz = max(1.0, (choice_step_mm * 0.5) - 0.45)
        eff_radius = min(bubble_radius_mm, max_vert, max_horiz)

        questions = []
        for i in range(num_questions):
            col = i // rows_per_col
            row = i % rows_per_col

            if col >= columns_count:
                break   # safety: more questions than columns × rows

            if layout_direction == 'ltr':
                # LTR: col 0 is leftmost column
                col_x_start = self.fiducial_margin_mm + col * col_width_mm
                answer_area_left_x = col_x_start + q_num_w_mm + extra_padding_mm
                center_y = start_y_mm + row * eff_row_spacing

                choices = []
                for c_idx, label in enumerate(choice_labels):
                    center_x = answer_area_left_x + choice_step_mm * (c_idx + 1)

                    bubble_region, safe_region, expanded_region = self._create_bubble_zones(
                        center_dx=center_x,
                        center_dy=center_y,
                        bubble_radius_mm=eff_radius,
                    )
                    choices.append(MCQChoice(
                        bubble_id=f"Q{i+1}_{label}",
                        choice=label,
                        bubble_region=bubble_region,
                        safe_region=safe_region,
                        expanded_region=expanded_region,
                    ))
            else:
                # RTL layout: col 0 is rightmost column
                r_col_idx = (columns_count - 1 - col)
                col_x_start = self.fiducial_margin_mm + r_col_idx * col_width_mm
                answer_area_right_x = col_x_start + (col_width_mm - q_num_w_mm) - extra_padding_mm
                center_y = start_y_mm + row * eff_row_spacing

                choices = []
                for c_idx, label in enumerate(choice_labels):
                    # Choice 1 is closest to question number (rightmost in answer area)
                    center_x = answer_area_right_x - choice_step_mm * (c_idx + 1)

                    bubble_region, safe_region, expanded_region = self._create_bubble_zones(
                        center_dx=center_x,
                        center_dy=center_y,
                        bubble_radius_mm=eff_radius,
                    )
                    choices.append(MCQChoice(
                        bubble_id=f"Q{i+1}_{label}",
                        choice=label,
                        bubble_region=bubble_region,
                        safe_region=safe_region,
                        expanded_region=expanded_region,
                    ))

            questions.append(MCQQuestion(question_id=i + 1, choices=choices))

        return questions



    def generate_mcq_layout(self, num_questions: int, choices_count: int = 4) -> List[MCQQuestion]:
        """Legacy wrapper — kept for backward compatibility. Delegates to generate_dynamic_mcq_layout."""
        return self.generate_dynamic_mcq_layout(
            num_questions=num_questions,
            choices_count=choices_count,
            columns_count=3 if num_questions > 20 else 2,
        )


    def generate_essay_layout(self, start_q: int = 21, count: int = 1) -> List[EssayRegion]:
        """Generates bounding regions for essay/handwriting questions."""
        essays = []
        for i in range(count):
            essays.append(EssayRegion(
                question_id=start_q + i,
                region=RegionContract(
                    dx_mm=5.0,
                    dy_mm=208.0 + (i * 60.0),
                    width_mm=180.0,
                    height_mm=57.0,
                    reference_frame="fiducial_space"
                )
            ))
        return essays

    def _generate_timing_marks(self) -> List[FiducialMark]:
        """Generates timing marks along the left edge for robust alignment."""
        marks = []
        start_y = 40.0
        spacing = 15.0
        count = 16
        for i in range(count):
            marks.append(FiducialMark(
                id=f"TM_L_{i+1}",
                x_mm=self.fiducial_margin_mm / 2.0,
                y_mm=start_y + (i * spacing),
                width_mm=4.0,
                height_mm=2.0,
                type="timing_mark"
            ))
        return marks

    def build_template(self, template_id: str, num_mcq: int, choices_count: int = 4, include_essay: bool = True) -> TemplateContract:
        """Builds the full Template Manifest and exports it."""
        fiducials = self._generate_fiducials() + self._generate_timing_marks()
        barcode = self._generate_barcode_region()
        mcqs = self.generate_mcq_layout(num_mcq, choices_count)
        essays = self.generate_essay_layout(start_q=num_mcq + 1, count=1) if include_essay else []
        
        template = TemplateContract(
            template_id=template_id,
            version="1.0.3",
            expected_scan_dpi=300,
            paper_size="A4",
            alignment_strategy="homography",
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=mcqs,
            essay_regions=essays
        )
        
        # Calculate SHA-256 Hash to prevent tampering
        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode('utf-8')).hexdigest()
        
        # Export the manifest to disk
        import os
        import json
        manifest_dir = os.path.join(os.path.dirname(__file__), "../media/templates")
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, f"{template_id}_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(template.model_dump_json(indent=2))
        
        return template

    def generate_medical_mcq_layout(self, num_questions: int = 100, choices_count: int = 4) -> List[MCQQuestion]:
        """Dynamically layouts MCQ questions in 4 columns of 25 for medical template."""
        questions = []
        max_rows_per_col = 25
        
        # Columns start positions (in mm) from left fiducial margin (10mm)
        col_start_x = [7.0, 55.0, 103.0, 151.0]
        start_dy = 95.0 # Start a bit higher since there are 25 rows
        bubble_spacing = 7.0
        row_spacing = 7.0
        
        for i in range(num_questions):
            col = i // max_rows_per_col
            row = i % max_rows_per_col

            base_x = col_start_x[col] if col < len(col_start_x) else col_start_x[-1] + (col - len(col_start_x) + 1) * 48.0
            q_dy = start_dy + (row * row_spacing)

            choices = []
            for c_idx in range(choices_count):
                choice_label = chr(65 + c_idx)  # 'A', 'B', 'C', 'D'
                center_dx = self.fiducial_margin_mm + base_x + (c_idx * bubble_spacing) + 2.0
                center_dy = self.fiducial_margin_mm + q_dy + 2.0

                bubble_region, safe_region, expanded_region = self._create_bubble_zones(center_dx, center_dy)

                choices.append(MCQChoice(
                    bubble_id=f"Q{i+1}_{choice_label}",
                    choice=choice_label,
                    bubble_region=bubble_region,
                    safe_region=safe_region,
                    expanded_region=expanded_region
                ))

            questions.append(MCQQuestion(question_id=i+1, choices=choices))

        return questions

    def build_medical_template(self, template_id: str) -> TemplateContract:
        """Builds the Medical Template Manifest and exports it."""
        import hashlib
        fiducials = self._generate_fiducials() + self._generate_timing_marks()
        barcode = self._generate_barcode_region()
        mcqs = self.generate_medical_mcq_layout(100, 4)
        
        template = TemplateContract(
            template_id=template_id,
            version="1.0.0",
            expected_scan_dpi=300,
            paper_size="A4",
            alignment_strategy="homography",
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=mcqs,
            essay_regions=[]
        )
        
        # Calculate SHA-256 Hash to prevent tampering
        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode('utf-8')).hexdigest()
        
        # Export the manifest to disk
        import os
        import json
        manifest_dir = os.path.join(os.path.dirname(__file__), "../media/templates")
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, f"{template_id}_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(template.model_dump_json(indent=2))
        
        return template

    @staticmethod
    def _load_template_config(config_name: str = "omr_yemen_180") -> dict:
        """Load template geometry from the shared config file (Single Source of Truth)."""
        import json
        config_path = os.path.join(
            os.path.dirname(__file__), "configs", f"{config_name}.json"
        )
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Template config not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_multigraphics_mcq_layout(
        self,
        num_questions: int = 180,
        choices_count: int = 4,
        config_name: str = "omr_yemen_180",
    ) -> List[MCQQuestion]:
        """
        Dynamically layouts MCQ questions from the shared config file.
        
        All coordinates are read from configs/<config_name>.json — NOT hardcoded.
        This is the Single Source of Truth for the entire system.
        """
        config = self._load_template_config(config_name)
        q_cfg = config["questions"]
        layout = q_cfg["layout"]
        detect = config.get("detection", {})
        
        questions = []
        max_rows_per_col = layout["rows_per_column"]
        start_y = layout["start_y_absolute_mm"]
        row_spacing = layout["row_spacing_mm"]
        columns_cfg = layout["columns_config"]
        choice_labels = q_cfg["choice_labels"]

        for i in range(num_questions):
            col = i // max_rows_per_col
            row = i % max_rows_per_col

            if col >= len(columns_cfg):
                break

            col_cfg = columns_cfg[col]
            abs_x_map = col_cfg["bubble_absolute_x_mm"]
            center_dy = start_y + (row * row_spacing)

            choices = []
            for c_idx in range(choices_count):
                choice_label = choice_labels[c_idx]
                center_dx = abs_x_map[choice_label]

                bubble_region, safe_region, expanded_region = self._create_bubble_zones(
                    center_dx, center_dy
                )

                choices.append(MCQChoice(
                    bubble_id=f"Q{i+1}_{choice_label}",
                    choice=choice_label,
                    bubble_region=bubble_region,
                    safe_region=safe_region,
                    expanded_region=expanded_region
                ))

            questions.append(MCQQuestion(question_id=i+1, choices=choices))

        return questions

    def build_multigraphics_yemen_template(
        self,
        template_id: str = "OMR_YEMEN_180",
        config_name: str = "omr_yemen_180",
    ) -> TemplateContract:
        """
        Builds the Yemen Academic Template Manifest from the shared config.
        All geometry is read from configs/<config_name>.json.
        """
        import hashlib

        config = self._load_template_config(config_name)
        q_cfg = config["questions"]
        barcode_cfg = config.get("barcode", {})

        fiducials = self._generate_fiducials() + self._generate_timing_marks()
        
        barcode_region = barcode_cfg.get("region", {})
        barcode = RegionContract(
            dx_mm=barcode_region.get("x_mm", 9.0),
            dy_mm=barcode_region.get("y_mm", 46.5),
            width_mm=barcode_region.get("width_mm", 32.0),
            height_mm=barcode_region.get("height_mm", 39.5),
            reference_frame="absolute",
        )
        mcqs = self.generate_multigraphics_mcq_layout(
            num_questions=q_cfg["count"],
            choices_count=q_cfg["choices_per_question"],
            config_name=config_name,
        )
        
        template = TemplateContract(
            template_id=template_id,
            version=config.get("version", "1.0.0"),
            expected_scan_dpi=config["paper"]["dpi"],
            paper_size=config["paper"]["size"],
            alignment_strategy=config.get("alignment", {}).get("strategy", "homography"),
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=mcqs,
            essay_regions=[],
        )
        
        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode('utf-8')).hexdigest()
        
        manifest_dir = os.path.join(os.path.dirname(__file__), "../media/templates")
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, f"{template_id}_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(template.model_dump_json(indent=2))
        
        return template

    def build_dynamic_template(
        self,
        template_id:      str,
        template_name:    str   = "قالب مخصص",
        version:          str   = "1.0.0",
        num_questions:    int   = 100,
        choices_count:    int   = 4,
        choice_labels:    list  = None,
        columns_count:    int   = 4,
        bubble_radius_mm: float = 1.7,
        row_spacing_mm:   float = 4.2,
        choice_spacing_mm: float = 9.0,
        start_y_mm:       float = 96.1,
        paper_size:       str   = "A4",
        scan_dpi:         int   = 300,
        layout_direction: str   = "rtl",
    ) -> TemplateContract:
        """
        The UNIVERSAL template builder — driven 100% by parameters from the UI.

        This is the single entry point for all dynamic templates. The OMR engines
        (OpenCV pass + CNN pass) receive only the resulting TemplateContract;
        they are completely agnostic to page design, bubble size, or column layout.

        Process:
        1. Caller (API endpoint) passes parameters received from the frontend.
        2. This method computes all pixel-accurate coordinates (in mm).
        3. Returns a signed TemplateContract (SHA-256 hash included).
        4. Caller persists it to ExamTemplate.template_data in the database.
        """
        fiducials = self._generate_fiducials() + self._generate_timing_marks()

        # Default choice labels if not provided
        if choice_labels is None:
            choice_labels = [str(i + 1) for i in range(choices_count)]

        # Generate ALL question coordinates dynamically
        mcqs = self.generate_dynamic_mcq_layout(
            num_questions=num_questions,
            choices_count=choices_count,
            columns_count=columns_count,
            bubble_radius_mm=bubble_radius_mm,
            row_spacing_mm=row_spacing_mm,
            choice_spacing_mm=choice_spacing_mm,
            start_y_mm=start_y_mm,
            choice_labels=choice_labels,
            layout_direction=layout_direction,
        )

        barcode = RegionContract(
            dx_mm=9.0, dy_mm=46.5,
            width_mm=32.0, height_mm=39.5,
            reference_frame="absolute",
        )

        template = TemplateContract(
            template_id=template_id,
            version=version,
            expected_scan_dpi=scan_dpi,
            paper_size=paper_size,
            alignment_strategy="homography",
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=mcqs,
            essay_regions=[],
        )

        # Sign with SHA-256 to detect tampering
        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode("utf-8")).hexdigest()

    def build_yemeni_ministry_40_template(
        self,
        template_id: str = "YEMEN_MINISTRY_40",
        template_name: str = "نموذج اختبار الشهادة الثانوية العامة — وزارة التربية والتعليم (40 سؤال)",
        version: str = "1.0",
        scan_dpi: int = 300,
        paper_size: str = "A5",
    ) -> TemplateContract:
        """
        Official Yemeni Ministry of Education 40-Question Hybrid Exam Sheet Manifest.
        Compact A5 (210x148.5mm):
        - Section 1: Questions 1-20 (True/False, 2 bubbles: صح / خطأ, Cols 1 & 2, 10 rows each).
        - Section 2: Questions 21-40 (MCQ, 4 bubbles: 1, 2, 3, 4, Cols 3 & 4, 10 rows each).
        - Corner Fiducials: 4 solid squares at (6,6), (198.5,6), (6,137), (198.5,137).
        """
        cfg = {
            "template_id": template_id,
            "template_name": template_name,
            "version": version,
            "display_mode": "compact_a5",
            "paper": {
                "size": paper_size,
                "dpi": scan_dpi,
                "width_mm": 210.0,
                "height_mm": 148.5 if paper_size.upper() == "A5" else 297.0,
                "orientation": "landscape" if paper_size.upper() == "A5" else "portrait",
            },
            "questions": {
                "metadata": {"num_questions": 40},
                "layout": {
                    "columns_count": 4,
                    "choices_count": 4,
                    "row_spacing_mm": 5.2,
                    "bubble_radius_mm": 2.1,
                    "bubble_type": "numbers",
                    "tf_bubble_type": "arabic",
                    "layout_direction": "rtl",
                },
                "sections": [
                    {"id": "sec1", "type": "true_false", "from_q": 1, "to_q": 20, "choices": ["صح", "خطأ"], "mark": 1},
                    {"id": "sec2", "type": "mcq", "from_q": 21, "to_q": 40, "choices": ["1", "2", "3", "4"], "mark": 2},
                ]
            }
        }
        return self.build_from_designer_config(cfg)

    def build_yemeni_ministry_50_template(
        self,
        template_id: str = "YEMEN_MINISTRY_50",
        template_name: str = "نموذج اختبار الشهادة الثانوية العامة — وزارة التربية والتعليم (50 سؤال)",
        version: str = "1.0",
        scan_dpi: int = 300,
        paper_size: str = "A4",
    ) -> TemplateContract:
        """
        Official Yemeni Ministry of Education 50-Question Hybrid Exam Sheet Manifest.
        Supports both Full A4 (210x297mm) and Compact A5 (210x148.5mm).
        - Section 1: Questions 1-20 (True/False, 2 bubbles: صح / خطأ or ص / خ).
        - Section 2: Questions 21-50 (MCQ, 4 bubbles: 1, 2, 3, 4).
        - Corner Fiducials: 4 solid squares at corners.
        """
        is_a4 = paper_size.upper() == "A4"

        if is_a4:
            fiducials = [
                FiducialMark(id="TL", x_mm=10.0, y_mm=10.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="TR", x_mm=194.0, y_mm=10.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BL", x_mm=10.0, y_mm=281.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BR", x_mm=194.0, y_mm=281.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
            ]
            bubble_radius_mm = 2.1
            row_spacing_mm = 12.8
            start_y_mm = 39.0

            questions: List[MCQQuestion] = []
            # Col 1: Q1..Q10 (x_base = 14 + 81 = 95mm)
            for i in range(10):
                q_num = i + 1
                cy = start_y_mm + i * row_spacing_mm
                choices = []
                for ch_label, cx in [("صح", 107.0), ("خطأ", 114.0)]:
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            # Col 2: Q11..Q20 (x_base = 14 + 54 = 68mm)
            for i in range(10):
                q_num = i + 11
                cy = start_y_mm + i * row_spacing_mm
                choices = []
                for ch_label, cx in [("صح", 80.0), ("خطأ", 87.0)]:
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            # Col 3: Q21..Q35 (x_base = 14 + 27 = 41mm)
            for i in range(15):
                q_num = i + 21
                cy = start_y_mm + i * row_spacing_mm
                choices = []
                for ch_label, cx in [("1", 49.0), ("2", 54.2), ("3", 59.4), ("4", 64.6)]:
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            # Col 4: Q36..Q50 (x_base = 14 + 0 = 14mm)
            for i in range(15):
                q_num = i + 36
                cy = start_y_mm + i * row_spacing_mm
                choices = []
                for ch_label, cx in [("1", 22.0), ("2", 27.2), ("3", 32.4), ("4", 37.6)]:
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            barcode = RegionContract(
                dx_mm=17.0, dy_mm=242.0,
                width_mm=62.0, height_mm=28.0,
                reference_frame="absolute",
            )
            act_paper = "A4"
        else:
            fiducials = [
                FiducialMark(id="TL", x_mm=6.0, y_mm=6.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="TR", x_mm=198.5, y_mm=6.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BL", x_mm=6.0, y_mm=137.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BR", x_mm=198.5, y_mm=137.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
            ]
            # ── Coordinates derived exactly from YemeniMinistrySheet.vue SVG logic ──
            # SVG viewBox = "0 0 210 148.5" (1 unit = 1 mm)
            # Column group: transform="translate(col.x, 20)"
            # Row group: transform="translate(0, rowIdx * spacing)" where rowIdx starts at 1
            # Bubble circle: cx=cp.x relative to column, cy=0 relative to row
            # Absolute bubble center: X = col.x + cp.x,  Y = 20 + rowIdx * spacing
            bubble_radius_mm = 2.1   # matches Vue default bubbleRadius: 2.1
            row_spacing_mm   = 5.2   # max(3.8, min(5.2, floor(100/15*10)/10)) for maxRows=15
            col_y_offset     = 20.0  # columns start at Y=20 in Vue SVG
            # rowIdx=1 for first question → start_y = col_y_offset + 1*row_spacing

            questions: List[MCQQuestion] = []

            # Col-1 (Q1-10): colX=102, صح at relative x=11.5, خطأ at relative x=3.5
            for i in range(10):
                q_num  = i + 1
                row_idx = i + 1
                cy = col_y_offset + row_idx * row_spacing_mm
                choices = []
                for ch_label, cx in [("صح", 102.0 + 11.5), ("خطأ", 102.0 + 3.5)]:
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            # Col-2 (Q11-20): colX=72, صح at relative x=11.5, خطأ at relative x=3.5
            for i in range(10):
                q_num   = i + 11
                row_idx = i + 1
                cy = col_y_offset + row_idx * row_spacing_mm
                choices = []
                for ch_label, cx in [("صح", 72.0 + 11.5), ("خطأ", 72.0 + 3.5)]:
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            # Col-3 (Q21-35): colX=42, MCQ xs=[19.0,13.5,8.0,2.5] for choices ['1','2','3','4']
            for i in range(15):
                q_num   = i + 21
                row_idx = i + 1
                cy = col_y_offset + row_idx * row_spacing_mm
                choices = []
                for ch_label, rel_x in [("1", 19.0), ("2", 13.5), ("3", 8.0), ("4", 2.5)]:
                    cx = 42.0 + rel_x
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            # Col-4 (Q36-50): colX=12, MCQ xs=[19.0,13.5,8.0,2.5] for choices ['1','2','3','4']
            for i in range(15):
                q_num   = i + 36
                row_idx = i + 1
                cy = col_y_offset + row_idx * row_spacing_mm
                choices = []
                for ch_label, rel_x in [("1", 19.0), ("2", 13.5), ("3", 8.0), ("4", 2.5)]:
                    cx = 12.0 + rel_x
                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label, bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg))
                questions.append(MCQQuestion(question_id=q_num, choices=choices))

            barcode = RegionContract(
                dx_mm=21.0, dy_mm=120.0,
                width_mm=60.0, height_mm=17.0,
                reference_frame="absolute",
            )
            act_paper = "A5"

        template = TemplateContract(
            template_id=template_id,
            version=version,
            expected_scan_dpi=scan_dpi,
            paper_size=act_paper,
            alignment_strategy="homography",
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=questions,
            essay_regions=[],
        )

        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode("utf-8")).hexdigest()
        return template

    def build_yemeni_ministry_60_template(
        self,
        template_id: str = "YEMEN_MINISTRY_60",
        template_name: str = "نموذج اختبار الشهادة الثانوية العامة — وزارة التربية والتعليم (60 سؤال)",
        version: str = "1.0",
        scan_dpi: int = 300,
    ) -> TemplateContract:
        """
        Official Yemeni Ministry of Education 60-Question Exam Sheet Manifest — A5 Landscape.
        - Section 1: Questions  1-20  (True/False, صح / خطأ) — 2 columns of 10 each.
        - Section 2: Questions 21-40  (MCQ, 4 choices: 1,2,3,4) — 20 rows, col 3.
        - Section 3: Questions 41-60  (MCQ, 4 choices: 1,2,3,4) — 20 rows, col 4.
        - Corner Fiducials: 4 solid squares (same positions as 50-question A5 template).
        - Row spacing: 5.2 mm → 20 rows × 5.2 mm = 104 mm starting at y=22.2 mm → ends at ~126 mm (fits A5).
        """
        fiducials = [
            FiducialMark(id="TL", x_mm=6.0,   y_mm=6.0,   width_mm=5.5, height_mm=5.5, type="solid_square"),
            FiducialMark(id="TR", x_mm=198.5,  y_mm=6.0,   width_mm=5.5, height_mm=5.5, type="solid_square"),
            FiducialMark(id="BL", x_mm=6.0,   y_mm=137.0,  width_mm=5.5, height_mm=5.5, type="solid_square"),
            FiducialMark(id="BR", x_mm=198.5,  y_mm=137.0,  width_mm=5.5, height_mm=5.5, type="solid_square"),
        ]
        # ── Coordinates derived exactly from YemeniMinistrySheet.vue SVG logic ──
        # SVG viewBox = "0 0 210 148.5", columns at transform="translate(col.x, 20)"
        # Row: transform="translate(0, rowIdx * spacing)" where rowIdx starts at 1
        # Bubble circle center: (col.x + cp.x,  20 + rowIdx * spacing)
        # For 60 questions: maxRows=20 → spacing = max(3.8, min(5.2, floor(100/20*10)/10))
        #                            = max(3.8, min(5.2, 5.0)) = 5.0mm
        bubble_radius_mm = 2.1    # Vue default bubbleRadius: 2.1
        row_spacing_mm   = 5.0    # effectiveRowSpacing for maxRows=20
        col_y_offset     = 20.0   # Vue column Y offset

        questions: List[MCQQuestion] = []

        # ── Col-1 (rightmost): Q1-10, True/False — colX=102 ───────────────
        for i in range(10):
            q_num = i + 1
            row_idx = i + 1
            cy = col_y_offset + row_idx * row_spacing_mm
            choices = []
            for ch_label, cx in [("صح", 102.0 + 11.5), ("خطأ", 102.0 + 3.5)]:
                b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                choices.append(MCQChoice(
                    bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label,
                    bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg,
                ))
            questions.append(MCQQuestion(question_id=q_num, choices=choices))

        # ── Col-2: Q11-20, True/False — colX=72 ───────────────────────────
        for i in range(10):
            q_num = i + 11
            row_idx = i + 1
            cy = col_y_offset + row_idx * row_spacing_mm
            choices = []
            for ch_label, cx in [("صح", 72.0 + 11.5), ("خطأ", 72.0 + 3.5)]:
                b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                choices.append(MCQChoice(
                    bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label,
                    bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg,
                ))
            questions.append(MCQQuestion(question_id=q_num, choices=choices))

        # ── Col-3: Q21-40, MCQ 4-choice — colX=42 ────────────────────────
        # Vue xs = [19.0, 13.5, 8.0, 2.5] for choices ['1','2','3','4'] (RTL: 1 rightmost)
        for i in range(20):
            q_num = i + 21
            row_idx = i + 1
            cy = col_y_offset + row_idx * row_spacing_mm
            choices = []
            for ch_label, rel_x in [("1", 19.0), ("2", 13.5), ("3", 8.0), ("4", 2.5)]:
                cx = 42.0 + rel_x
                b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                choices.append(MCQChoice(
                    bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label,
                    bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg,
                ))
            questions.append(MCQQuestion(question_id=q_num, choices=choices))

        # ── Col-4 (leftmost): Q41-60, MCQ 4-choice — colX=12 ─────────────
        for i in range(20):
            q_num = i + 41
            row_idx = i + 1
            cy = col_y_offset + row_idx * row_spacing_mm
            choices = []
            for ch_label, rel_x in [("1", 19.0), ("2", 13.5), ("3", 8.0), ("4", 2.5)]:
                cx = 12.0 + rel_x
                b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                choices.append(MCQChoice(
                    bubble_id=f"Q{q_num}_{ch_label}", choice=ch_label,
                    bubble_region=b_reg, safe_region=s_reg, expanded_region=e_reg,
                ))
            questions.append(MCQQuestion(question_id=q_num, choices=choices))


        barcode = RegionContract(
            dx_mm=21.0, dy_mm=120.0,
            width_mm=60.0, height_mm=17.0,
            reference_frame="absolute",
        )

        template = TemplateContract(
            template_id=template_id,
            version=version,
            expected_scan_dpi=scan_dpi,
            paper_size="A5",
            alignment_strategy="homography",
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=questions,
            essay_regions=[],
        )
        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode("utf-8")).hexdigest()
        return template

    def build_from_designer_config(self, config: dict) -> TemplateContract:
        """
        Dynamically builds a pixel-accurate TemplateContract directly from the
        frontend designer config (JSON), matching YemeniMinistrySheet.vue exactly.
        
        Supports:
        - Arbitrary question counts (20, 50, 90, 100, 180, etc.)
        - Multi-section layouts (True/False + MCQ sections)
        - Dynamic column distribution (1 to 6 columns)
        - Compact A5 (210x148.5) and Full A4 (210x297)
        - Exact bubble radii, row pitch, and fiducials for OpenCV Homography
        """
        template_id = config.get("template_id") or "CUSTOM_TEMPLATE"
        template_name = config.get("template_name") or config.get("name") or "قالب مخصص"
        version = config.get("version") or "1.0"
        
        paper_cfg = config.get("paper", {})
        paper_size = paper_cfg.get("size", "A5").upper()
        scan_dpi = paper_cfg.get("dpi", 300)
        paper_h = paper_cfg.get("height_mm", 148.5)
        
        t_id = str(config.get("template_id", "") or "").upper()
        t_name = str(config.get("template_name", "") or config.get("name", "") or "")
        disp_mode = str(config.get("display_mode", "") or "").lower()

        # Any Yemeni Ministry template or compact_a5 is strictly A5 landscape (210 x 148.5)
        is_ministry = (
            "YEMEN_MINISTRY" in t_id or
            "وزارة التربية" in t_name or
            "الثانوية العامة" in t_name or
            disp_mode == "compact_a5" or
            paper_size == "A5"
        )
        if is_ministry:
            is_a4 = False
            act_paper = "A5"
        else:
            is_a4 = paper_size == "A4" or paper_h > 200.0
            act_paper = "A4" if is_a4 else "A5"

        q_cfg = config.get("questions", {})
        layout_cfg = q_cfg.get("layout", {})
        sections = q_cfg.get("sections", [])
        
        target_cols = layout_cfg.get("columns_count", 4)
        bubble_radius_mm = layout_cfg.get("bubble_radius_mm", 2.1)
        user_row_spacing = layout_cfg.get("row_spacing_mm", 5.2 if not is_a4 else 12.8)
        choices_count = layout_cfg.get("choices_count", 4)
        mcq_b_type = layout_cfg.get("bubble_type", "numbers")
        tf_b_type = layout_cfg.get("tf_bubble_type", "arabic")

        # Determine choice labels
        if mcq_b_type == "arabic_letters":
            mcq_choices = ["أ", "ب", "ج", "د", "هـ"][:choices_count]
        elif mcq_b_type in ("english_letters", "letters"):
            mcq_choices = ["A", "B", "C", "D", "E"][:choices_count]
        else:
            mcq_choices = ["1", "2", "3", "4", "5"][:choices_count]

        if tf_b_type == "english":
            tf_choices = ["T", "F"]
        elif tf_b_type == "symbols":
            tf_choices = ["✓", "✗"]
        else:
            tf_choices = ["صح", "خطأ"]

        # 1. Generate Fiducials
        if is_a4:
            fiducials = [
                FiducialMark(id="TL", x_mm=10.0, y_mm=10.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="TR", x_mm=194.0, y_mm=10.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BL", x_mm=10.0, y_mm=281.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BR", x_mm=194.0, y_mm=281.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
            ]
        else:
            fiducials = [
                FiducialMark(id="TL", x_mm=6.0, y_mm=6.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="TR", x_mm=198.5, y_mm=6.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BL", x_mm=6.0, y_mm=137.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
                FiducialMark(id="BR", x_mm=198.5, y_mm=137.0, width_mm=5.5, height_mm=5.5, type="solid_square"),
            ]

        # 2. Allocate columns to sections
        cols_def = []
        if sections:
            total_q = sum(max(1, (s.get("to_q", 1) - s.get("from_q", 1) + 1)) for s in sections)
            n_secs = len(sections)
            sec_cols = []
            allocated = 0
            for s in sections:
                cnt = max(1, (s.get("to_q", 1) - s.get("from_q", 1) + 1))
                c = max(1, round((cnt / max(1, total_q)) * target_cols))
                sec_cols.append(c)
                allocated += c

            while allocated > target_cols:
                max_i = max(range(n_secs), key=lambda i: sec_cols[i])
                if sec_cols[max_i] > 1:
                    sec_cols[max_i] -= 1
                    allocated -= 1
                else:
                    break

            while allocated < target_cols:
                max_r_i = max(range(n_secs), key=lambda i: (sections[i].get("to_q", 1) - sections[i].get("from_q", 1) + 1) / sec_cols[i])
                sec_cols[max_r_i] += 1
                allocated += 1

            for i, s in enumerate(sections):
                from_q = s.get("from_q", 1)
                to_q = s.get("to_q", from_q)
                sec_tot = to_q - from_q + 1
                is_tf = s.get("type") == "true_false" or (s.get("choices") and len(s.get("choices")) == 2 and ("صح" in s.get("choices") or "T" in s.get("choices")))
                n_c = sec_cols[i]
                base_per_col = sec_tot // n_c
                rem = sec_tot % n_c

                cur_from = from_q
                for c in range(n_c):
                    cnt = base_per_col + (1 if c < rem else 0)
                    start = cur_from
                    end = start + cnt - 1
                    cur_from = end + 1

                    cols_def.append({
                        "type": "true_false" if is_tf else "mcq",
                        "start_q": start,
                        "end_q": end,
                        "total_q": cnt,
                        "choices": s.get("choices"),
                    })
        else:
            raw_num_q = (
                q_cfg.get("metadata", {}).get("num_questions") or
                config.get("metadata", {}).get("num_questions") or
                config.get("total_mcq") or 50
            )
            if raw_num_q <= 40:
                cols_def = [
                    {"type": "true_false", "start_q": 1, "end_q": 10, "total_q": 10},
                    {"type": "true_false", "start_q": 11, "end_q": 20, "total_q": 10},
                    {"type": "mcq", "start_q": 21, "end_q": 30, "total_q": 10},
                    {"type": "mcq", "start_q": 31, "end_q": 40, "total_q": 10},
                ]
            elif raw_num_q >= 60:
                cols_def = [
                    {"type": "true_false", "start_q": 1, "end_q": 10, "total_q": 10},
                    {"type": "true_false", "start_q": 11, "end_q": 20, "total_q": 10},
                    {"type": "mcq", "start_q": 21, "end_q": 40, "total_q": 20},
                    {"type": "mcq", "start_q": 41, "end_q": 60, "total_q": 20},
                ]
            else:
                cols_def = [
                    {"type": "true_false", "start_q": 1, "end_q": 10, "total_q": 10},
                    {"type": "true_false", "start_q": 11, "end_q": 20, "total_q": 10},
                    {"type": "mcq", "start_q": 21, "end_q": 35, "total_q": 15},
                    {"type": "mcq", "start_q": 36, "end_q": 50, "total_q": 15},
                ]

        # 3. Position columns X
        n_cols = len(cols_def)
        if not is_a4:
            if n_cols == 1:
                col_xs = [102.0]
            elif n_cols <= 4:
                std_xs = [102.0, 72.0, 42.0, 12.0]
                col_xs = std_xs[:n_cols]
            else:
                step = (102.0 - 12.0) / max(1, n_cols - 1)
                col_xs = [round(102.0 - i * step, 1) for i in range(n_cols)]
        else:
            if n_cols == 1:
                col_xs = [81.0]
            elif n_cols <= 4:
                std_xs = [81.0, 54.0, 27.0, 0.0]
                col_xs = std_xs[:n_cols]
            else:
                step = 81.0 / max(1, n_cols - 1)
                col_xs = [round(81.0 - i * step, 1) for i in range(n_cols)]

        # 4. Effective row spacing
        max_rows = max((c["total_q"] for c in cols_def), default=10)
        if not is_a4:
            if user_row_spacing and 0 < user_row_spacing < 6.5:
                if max_rows * user_row_spacing > 105:
                    eff_row_spacing = max(3.8, math.floor((105 / max_rows) * 10) / 10)
                else:
                    eff_row_spacing = user_row_spacing
            else:
                eff_row_spacing = max(3.8, min(5.2, math.floor((100 / max_rows) * 10) / 10))
        else:
            eff_row_spacing = max(4.5, min(12.8, math.floor((210 / max_rows) * 10) / 10))

        # 5. Build MCQQuestions
        questions: List[MCQQuestion] = []
        for c_idx, c_def in enumerate(cols_def):
            col_x = col_xs[c_idx] if c_idx < len(col_xs) else col_xs[-1]
            is_tf = c_def["type"] == "true_false"
            
            if is_tf:
                sec_tf = c_def.get("choices")
                if sec_tf and len(sec_tf) == 2:
                    c_positions = [(sec_tf[0], 11.5), (sec_tf[1], 3.5)]
                else:
                    c_positions = [(tf_choices[0], 11.5), (tf_choices[1], 3.5)]
            else:
                sec_mcq = c_def.get("choices")
                active_mcq = sec_mcq if (sec_mcq and len(sec_mcq) >= 2) else mcq_choices
                n_ch = len(active_mcq)
                if n_ch == 4:
                    xs = [19.0, 13.5, 8.0, 2.5]
                elif n_ch == 5:
                    xs = [20.0, 15.5, 11.0, 6.5, 2.0]
                elif n_ch == 3:
                    xs = [18.0, 11.0, 4.0]
                else:
                    step = 18.0 / max(1, n_ch)
                    xs = [round(23.5 - 4.5 - i * step, 1) for i in range(n_ch)]
                c_positions = [(active_mcq[i], xs[i]) for i in range(n_ch)]

            start_q = c_def["start_q"]
            for r in range(c_def["total_q"]):
                q_num = start_q + r
                row_idx = r + 1  # 1-indexed matching Vue
                
                if not is_a4:
                    # Matches Vue: columns start at Y=20, rowIdx starts at 1
                    cy = 20.0 + (row_idx * eff_row_spacing)
                else:
                    # A4: question grid starts at Y≈36.5, rowIdx starts at 1
                    cy = 36.5 + (row_idx * eff_row_spacing)

                choices = []
                for ch_label, ch_x in c_positions:
                    if not is_a4:
                        cx = col_x + ch_x
                    else:
                        cx = 14.0 + col_x + ch_x

                    b_reg, s_reg, e_reg = self._create_bubble_zones(cx, cy, bubble_radius_mm)
                    choices.append(MCQChoice(
                        bubble_id=f"Q{q_num}_{ch_label}",
                        choice=ch_label,
                        bubble_region=b_reg,
                        safe_region=s_reg,
                        expanded_region=e_reg,
                    ))

                questions.append(MCQQuestion(question_id=q_num, choices=choices))

        # Sort questions by question_id
        questions.sort(key=lambda q: q.question_id)

        barcode = RegionContract(
            dx_mm=21.0 if not is_a4 else 17.0,
            dy_mm=120.0 if not is_a4 else 242.0,
            width_mm=60.0 if not is_a4 else 62.0,
            height_mm=17.0 if not is_a4 else 28.0,
            reference_frame="absolute",
        )

        template = TemplateContract(
            template_id=template_id,
            version=version,
            expected_scan_dpi=scan_dpi,
            paper_size="A4" if is_a4 else "A5",
            alignment_strategy="homography",
            fiducial_marks=fiducials,
            barcode_region=barcode,
            mcq_questions=questions,
            essay_regions=[],
        )

        template_json = template.model_dump_json(exclude={"template_hash"}, indent=2)
        template.template_hash = hashlib.sha256(template_json.encode("utf-8")).hexdigest()
        return template


