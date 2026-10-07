import hashlib

from core.contracts import TemplateContract

class TemplateValidatorService:
    """Validates the geometric integrity and authenticity of the Template Manifest."""
    
    @staticmethod
    def validate(template: TemplateContract) -> bool:
        errors = []
        
        # 1. Ensure minimum fiducials for homography calculation
        if len(template.fiducial_marks) < 4:
            errors.append("Template must have at least 4 fiducial marks for perspective transform.")
            
        # 2. Authenticity Hash Check (Security/Auditability)
        dump = template.model_dump_json(exclude={"template_hash"}, indent=2)
        expected_hash = hashlib.sha256(dump.encode('utf-8')).hexdigest()
        if expected_hash != template.template_hash:
            errors.append(f"Security Alert: Template Hash mismatch! Expected {expected_hash}, got {template.template_hash}")
            
        # 3. Prevent Negative Coordinates
        if template.barcode_region:
            if template.barcode_region.dx_mm < 0 or template.barcode_region.dy_mm < 0:
                errors.append("Barcode region has negative coordinates relative to fiducial space.")
                
        if errors:
            raise ValueError(f"Template validation failed: {'; '.join(errors)}")
            
        return True
