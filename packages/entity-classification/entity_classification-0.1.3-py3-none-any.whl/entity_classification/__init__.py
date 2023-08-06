from .bp import *
from .svc import *
from .dmo import *

from .bp.entity_orchestrator import EntityOrchestrator


def classify(entity_names: list,
             input_tokens: list) -> dict:
    return EntityOrchestrator(entity_names).run(input_tokens)
