'''Tyke django instrumentor module wrapper.''' # pylint: disable=R0401
from email import header
import logging
import traceback

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.trace import Span
from django.core.exceptions import PermissionDenied  # pylint:disable=C0415

from tyke.agent import constants
from tyke.agent.filter.registry import Registry, TYPE_HTTP
from tyke.agent.instrumentation import BaseInstrumentorWrapper


logger = logging.getLogger(__name__)  # pylint: disable=C0103


class DjangoInstrumentationWrapper(BaseInstrumentorWrapper):
    """wrapped class around django instrumentation"""
    def instrument(self):
        """configure django instrumentor w hooks"""
        DjangoInstrumentor().instrument(request_hook=self.request_hook,
                                        response_hook=self.response_hook)

    def uninstrument(self): # pylint:disable=R0201
        """need this to match wrapper interface for specs"""
        return

    def request_hook(self, span: Span, request):
        """django request hook before request is processed by app"""
        try:
            body = request.body
            headers = None
            if hasattr(request, "headers"):
                headers = request.headers
            elif hasattr(request, "_headers"):
                headers = request._headers
            span.update_name(f"{request.method} {span.name}")
            self.generic_request_handler(headers, body, span)
            full_url = request.build_absolute_uri()
            block_result = Registry().apply_filters(span,
                                                    full_url,
                                                    headers,
                                                    body,
                                                    TYPE_HTTP)
            if block_result:
                logger.debug('should block evaluated to true, aborting with 403')
                # since middleware chain is halted the status code is not set when blocked
                span.set_attribute('http.status_code', 403)
                span.end()
                raise PermissionDenied
        except PermissionDenied as permission_denied:
            raise permission_denied
        except Exception as err:  # pylint:disable=W0703
            logger.debug(constants.INST_RUNTIME_EXCEPTION_MSSG,
                         'django request hook',
                         err,
                         traceback.format_exc())


    def response_hook(self, span, _request, response):
        """django response hook before response is written out"""
        try:
            body = response.content
            headers = None
            if hasattr(response, "headers"):
                headers = response.headers
            elif hasattr(response, "_headers"):
                headers = response._headers
            self.generic_response_handler(headers, body, span)
        except Exception as err:  # pylint:disable=W0703
            logger.debug(constants.INST_RUNTIME_EXCEPTION_MSSG,
                         'django response hook',
                         err,
                         traceback.format_exc())
