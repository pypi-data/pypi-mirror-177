'''Tyke wrapper around OTel botocore Instrumentor''' # pylint: disable=R0801
import logging
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor # pylint:disable=E0611,E0401
from tyke.agent.instrumentation import BaseInstrumentorWrapper


# Initialize logger with local module name
logger = logging.getLogger(__name__) # pylint: disable=C0103

class BotocoreInstrumentationWrapper(BotocoreInstrumentor, BaseInstrumentorWrapper):
    '''Tyke wrapper around OTel Botocore Instrumentor class'''
