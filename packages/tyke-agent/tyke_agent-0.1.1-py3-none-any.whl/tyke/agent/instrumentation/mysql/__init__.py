'''Tyke wrapper around OTel MySQL Instrumentor''' # pylint: disable=R0801
import logging
from opentelemetry.instrumentation.mysql import MySQLInstrumentor
from tyke.agent.instrumentation import BaseInstrumentorWrapper

# Initialize logger with local module name
logger = logging.getLogger(__name__) # pylint: disable=C0103

# The main entry point
class MySQLInstrumentorWrapper(MySQLInstrumentor, BaseInstrumentorWrapper):
    '''Tyke wrapper around OTel MySQL Instrumentor class'''
