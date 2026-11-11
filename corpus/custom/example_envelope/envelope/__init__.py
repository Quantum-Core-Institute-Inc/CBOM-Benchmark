"""Internal envelope library. Applications call seal(data, profile=...) and never pick algorithms."""
from envelope.core import seal

__all__ = ["seal"]
