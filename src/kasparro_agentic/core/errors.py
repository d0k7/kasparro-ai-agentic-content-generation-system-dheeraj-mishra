from __future__ import annotations


class PipelineError(RuntimeError):
    """Base class for pipeline-related failures."""


class ValidationError(PipelineError):
    """Raised when a state or output payload fails validation."""
