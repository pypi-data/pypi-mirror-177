import json
import socket
from dataclasses import dataclass
import sys
import traceback
import requests
from IPython import get_ipython
from IPython.core.ultratb import AutoFormattedTB

from streaminglogs import StreamingLogsServiceContext, ActivityLog, ExceptionLog


@dataclass
class LoggingHandler:

    __context: StreamingLogsServiceContext
    __is_debug: bool
    __origin: str
    __ip_address: str

    @classmethod
    def __init__(cls,
                 context: StreamingLogsServiceContext,
                 is_debug,
                 enable_ipynb_unhandled_exceptions_tracing=False):
        cls.__context = context
        cls.__is_debug = is_debug
        cls.__origin = cls.__context.origin + '.debug' if cls.__is_debug else cls.__context.origin
        cls.__ip_address = cls.__get_ip()
        if enable_ipynb_unhandled_exceptions_tracing:
            get_ipython().set_custom_exc((Exception,), cls.trace_unhandled_exception)

    @classmethod
    def trace_unhandled_exception(cls, shell, etype, evalue, tb, tb_offset=None):
        shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)

        itb = AutoFormattedTB(mode='Plain', tb_offset=1)
        stb = itb.structured_traceback(etype, evalue, tb)
        sstb = itb.stb2text(stb)

        cls.trace_exception(evalue, sstb)

    @classmethod
    def trace_activity(cls, message: str, tags=None, additional_info=None, console_only: bool = False):

        if cls.__is_debug:
            print(message)

        activity_log = ActivityLog(cls.__origin,
                                   message, cls.__ip_address,
                                   json.dumps(additional_info, indent=4, sort_keys=True, default=str),
                                   tags or [])
        message = {
            'payload': activity_log.as_legacy_dict(),
            'routingKey': cls.__build_routing_key(activity_log.origin, activity_log.input_type, console_only, tags)
        }
        response = requests.post(
            cls.__context.endpoint,
            data=json.dumps(message, indent=4, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            # raise NameError('Streaming Logs API Error {}'.format(response.content.decode('utf-8')))
            print(f'Streaming Logs API Error {response.content.decode("utf-8")}')

    @classmethod
    def trace_exception(cls, ex: Exception, stacktrace=None, tags=None, additional_info=None, console_only: bool = False):

        if cls.__is_debug:
            print(ex)

        ex_log = ExceptionLog(cls.__origin,
                              None,
                              stacktrace or ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)),
                              ex,
                              None,
                              cls.__ip_address,
                              json.dumps(additional_info, indent=4, sort_keys=True, default=str),
                              tags or [])
        message = {
            'payload': ex_log.as_legacy_dict(),
            'routingKey': cls.__build_routing_key(ex_log.origin, ex_log.input_type, console_only, tags)
        }
        response = requests.post(
            cls.__context.endpoint,
            data=json.dumps(message, indent=4, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            # raise NameError('Streaming Logs API Error {}'.format(response.content.decode('utf-8')))
            print(f'Streaming Logs API Error {response.content.decode("utf-8")}')

    @classmethod
    def trace_execution_side_effects(cls, extras_payload, fn, *fn_params):

        try:

            result = fn(*fn_params)

        except Exception as e:

            try:
                fn_name = fn.__qualname__
            except:
                fn_name = ''

            additional_info = {}

            if extras_payload:
                additional_info['extras'] = extras_payload

            additional_info['called_from'] = sys._getframe(1).f_code.co_name,
            additional_info['service_name'] = fn_name
            additional_info['params'] = fn_params
            additional_info['error_stack_trace'] = traceback.format_exc()

            cls.trace_exception(e, additional_info=additional_info)

            raise e

        return result

    @staticmethod
    def __build_routing_key(origin, input_type, console_only: bool, tags: [str]):
        if tags is not None:
            return '{}.{}.{}.{}'.format('ConsoleOnly' if console_only else 'Storable', origin, input_type, '.'.join(tags))
        return '{}.{}.{}'.format('ConsoleOnly' if console_only else 'Storable', origin, input_type)

    @staticmethod
    def __get_ip():
        try:
            # This cause problems on some environments like for example Airflow
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception as ex:
            print(ex)
            ip_address = '127.0.0.1'
        return ip_address
