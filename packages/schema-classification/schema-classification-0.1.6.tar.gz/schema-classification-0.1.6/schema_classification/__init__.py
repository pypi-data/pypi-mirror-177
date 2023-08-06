from .bp import *
from .svc import *
from .dmo import *
from .dto import *


def classify(d_schema: dict,
             input_tokens: list) -> dict:
    """ Run the Schema Orchestrator

    Args:
        d_schema (dict): the schema JSON
        input_tokens (list): a flat list of tokens extracted from text
            Sample Input:
                ['network_topology', 'user', 'customer']
    """
    run = SchemaOrchestrator(d_schema).run

    svcresult = run(input_tokens)

    return svcresult
