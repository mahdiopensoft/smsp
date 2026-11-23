"""
Dedicated XSS sanitization middleware for endpoints exempted from the broad
SQL-keyword filter (e.g., /api/bank/ and /api/exams/).

Blocks dangerous XSS payloads (<script>, javascript:, vbscript:, inline on*=
event handlers, <iframe>, <object>, <embed>, data:text/html) while allowing
benign rich HTML, LaTeX/KaTeX math, CSS styles, entities (&nbsp;), and CS
questions containing SQL keywords like SELECT or semicolons.
"""
import json
import logging
import re

from django.http import JsonResponse

logger = logging.getLogger('security.input')

XSS_PATTERNS = [
    re.compile(r"<\s*script\b", re.IGNORECASE),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"vbscript\s*:", re.IGNORECASE),
    re.compile(r"\bon[a-z]+\s*=", re.IGNORECASE),
    re.compile(r"<\s*iframe\b", re.IGNORECASE),
    re.compile(r"<\s*object\b", re.IGNORECASE),
    re.compile(r"<\s*embed\b", re.IGNORECASE),
    re.compile(r"data\s*:\s*text/html", re.IGNORECASE),
]

TARGET_PATH_PREFIXES = ('/api/bank/', '/api/exams/')
WRITE_METHODS = ('POST', 'PUT', 'PATCH')


class BankXSSSanitizationMiddleware:
    """Reject XSS payloads on write operations to rich-text Question Bank and Exam APIs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._should_check(request):
            threat = self._scan_request(request)
            if threat:
                logger.warning(
                    "Blocked potential XSS payload on %s %s (%s)",
                    request.method,
                    request.path,
                    threat,
                )
                return JsonResponse(
                    {
                        "success": False,
                        "message": "محتوى HTML غير آمن مرفوض (XSS detected)",
                    },
                    status=400,
                )

        return self.get_response(request)

    def _should_check(self, request) -> bool:
        if request.method not in WRITE_METHODS:
            return False
        path = (request.path or '').lower()
        return path.startswith(TARGET_PATH_PREFIXES)

    def _scan_request(self, request) -> str:
        content_type = (request.content_type or '').lower()

        if 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
            for key, values in request.POST.lists():
                for val in values:
                    threat = self._check_value(val, f"form field '{key}'")
                    if threat:
                        return threat
            return ""

        raw_body = request.body
        if not raw_body:
            return ""

        try:
            body_text = raw_body.decode('utf-8', errors='ignore')
        except Exception:
            return ""

        if 'application/json' in content_type or body_text.lstrip().startswith(('{', '[')):
            try:
                parsed = json.loads(body_text)
                return self._scan_json(parsed, "json")
            except (ValueError, TypeError):
                pass

        return self._check_value(body_text, "request body")

    def _scan_json(self, obj, context: str) -> str:
        if isinstance(obj, str):
            return self._check_value(obj, context)
        if isinstance(obj, dict):
            for k, v in obj.items():
                threat = self._scan_json(v, f"{context}.{k}")
                if threat:
                    return threat
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                threat = self._scan_json(item, f"{context}[{idx}]")
                if threat:
                    return threat
        return ""

    def _check_value(self, value: str, context: str) -> str:
        if not value or not isinstance(value, str):
            return ""
        for pattern in XSS_PATTERNS:
            if pattern.search(value):
                return f"XSS pattern in {context}"
        return ""
