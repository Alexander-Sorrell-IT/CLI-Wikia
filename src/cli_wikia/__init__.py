"""cli-wikia: offline reference wiki for AI coding CLIs."""

__version__ = "0.18.0"

# MODELS is derived from the registry (models.json + optional collective override)
# so adding a model to models.json automatically extends every wikia command.
from .registry import all_models as _all_models

MODELS = _all_models()
