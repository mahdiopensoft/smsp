"""
Base Engine — Abstract class for all 11 pipeline engines.

Every engine in the system (Alignment, OMR, HTR, Judge, etc.) inherits from
this class. It enforces:
  - Standardized input/output contracts
  - Automatic logging with timing
  - Confidence scoring
  - Provider Pattern support (swap implementations at runtime)
"""

import abc
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class EngineResult:
    """
    Standardized result object returned by every engine.

    Every engine MUST return an EngineResult so the pipeline orchestrator
    can inspect confidence, timing, and errors uniformly.
    """
    engine_name: str
    status: str = "success"  # success | error | skipped
    confidence: float = 0.0  # 0.0 to 1.0
    data: dict = field(default_factory=dict)  # engine-specific output
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    processing_time_ms: float = 0.0
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider_used: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status == "success"

    def to_dict(self) -> dict:
        """Serialize for JSON storage in audit logs."""
        return {
            "engine_name": self.engine_name,
            "status": self.status,
            "confidence": self.confidence,
            "data": self.data,
            "errors": self.errors,
            "warnings": self.warnings,
            "processing_time_ms": self.processing_time_ms,
            "trace_id": self.trace_id,
            "provider_used": self.provider_used,
            "metadata": self.metadata,
        }


class BaseEngine(abc.ABC):
    """
    Abstract base class for all pipeline engines.

    Subclasses must implement:
      - engine_name (property): unique identifier
      - _process(input_data, context) -> EngineResult: core logic

    The public process() method wraps _process() with logging, timing,
    and error handling automatically.
    """

    def __init__(self):
        self.logger = logging.getLogger(f"apps.{self.engine_name}")

    @property
    @abc.abstractmethod
    def engine_name(self) -> str:
        """Unique name for this engine (e.g., 'alignment', 'omr')."""
        ...

    @abc.abstractmethod
    def _process(self, input_data: Any, context: Optional[dict] = None) -> EngineResult:
        """
        Core processing logic. Implemented by each engine.

        Args:
            input_data: Engine-specific input (image, text, etc.)
            context: Optional pipeline context (submission_id, template, etc.)

        Returns:
            EngineResult with status, confidence, and data.
        """
        ...

    def process(self, input_data: Any, context: Optional[dict] = None) -> EngineResult:
        """
        Public entry point. Wraps _process() with:
          - Timing measurement
          - Structured logging
          - Error catching
        """
        trace_id = str(uuid.uuid4())
        submission_id = (context or {}).get("submission_id", "unknown")

        self.logger.info(
            "Engine [%s] starting | submission=%s | trace=%s",
            self.engine_name, submission_id, trace_id
        )

        start_time = time.perf_counter()

        try:
            result = self._process(input_data, context)
            result.trace_id = trace_id
            result.processing_time_ms = (time.perf_counter() - start_time) * 1000

            self.logger.info(
                "Engine [%s] completed | status=%s | confidence=%.3f | time=%.1fms | trace=%s",
                self.engine_name, result.status, result.confidence,
                result.processing_time_ms, trace_id
            )

            return result

        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            self.logger.error(
                "Engine [%s] FAILED | error=%s | time=%.1fms | trace=%s",
                self.engine_name, str(exc), elapsed, trace_id,
                exc_info=True
            )

            return EngineResult(
                engine_name=self.engine_name,
                status="error",
                confidence=0.0,
                errors=[str(exc)],
                processing_time_ms=elapsed,
                trace_id=trace_id,
            )

    def validate_input(self, input_data: Any) -> bool:
        """
        Optional input validation. Override in subclasses for
        engine-specific validation logic.
        """
        return input_data is not None
