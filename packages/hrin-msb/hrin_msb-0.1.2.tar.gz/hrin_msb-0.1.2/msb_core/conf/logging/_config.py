import logging
import os
from datetime import datetime

from ._constants import (LOG_DATETIME_FORMAT)


def make_log_file_name(dir: str = '', filename: str = None):
	filename = filename if filename not in ['', None] else f"{datetime.today().strftime('%Y-%m-%d')}.log"
	return os.path.join(dir, filename)


class LogConfig:
	_registered_loggers: list
	_registered_handlers: list
	_default_log_level: str
	_default_format_str: str

	def __init__(self, **kwargs):
		self._registered_loggers = list()
		self._registered_handlers = list()
		self._default_log_level = kwargs.get('default_level') or logging.WARNING
		self._default_format_str = None

	def add_formatter(self, name: str, format: str = '', style: str = None):
		self.formatters[name] = {"format": format}

	def add_filters(self, name: str, handler_class: str, **kwargs):
		self.filters[name] = {
			'()': 'django.utils.log.RequireDebugTrue',
		}

	def add_logger(self, name: str, level: str = None, handlers: list = None, filters: list = None, **kwargs):
		try:
			log_handlers = handlers if isinstance(handlers, list) else []
			_logger = logging.getLogger(name=name)
			log_level = level if level is not None else self._default_log_level

			_logger.setLevel(level=log_level)
			_logger.propagate = kwargs.get('propagate') == True

			for log_handler in log_handlers:
				_logger.addHandler(log_handler)

			self._registered_loggers.append(name)
		except Exception as e:
			print(f"Logger registration failed for '{name}' :\n{e}")

	def get_file_handler(self, name, logs_dir: str, filename: str = None, handler_class=None, **kwargs):
		from logging.handlers import TimedRotatingFileHandler
		handler_class = handler_class if callable(handler_class) else TimedRotatingFileHandler
		init_kwargs = dict(filename=make_log_file_name(dir=logs_dir, filename=filename), when='midnight')
		return self.__build_log_handler(
			name=name, log_handler=handler_class, init_kwargs=init_kwargs, level=kwargs.get('level'),
			formatter=kwargs.get("formatter"), filters=kwargs.get('filters')
		)

	def get_email_handler(self, name, email_backend, handler_class: str = None, **kwargs):
		from django.utils.log import AdminEmailHandler
		handler_class = handler_class if callable(handler_class) else AdminEmailHandler
		init_kwargs = dict(
			include_html=kwargs.get('include_html') == True,
			email_backend=email_backend,
			reporter_class=kwargs.get('reporter_class')
		)
		return self.__build_log_handler(
			name=name, log_handler=handler_class, init_kwargs=init_kwargs, level=kwargs.get('level'),
			formatter=kwargs.get("formatter"), filters=kwargs.get('filters')
		)

	def get_console_handler(self, name, handler_class: str = None, **kwargs):
		handler_class = handler_class if callable(handler_class) else logging.StreamHandler
		init_kwargs = {}
		return self.__build_log_handler(
			name=name, log_handler=handler_class, init_kwargs=init_kwargs,
			level=kwargs.get('level'), formatter=kwargs.get("formatter"), filters=kwargs.get('filters')
		)

	def get_database_handler(self, name, db_model, **kwargs):
		from ._handlers import DatabaseLogger
		init_kwargs = dict(db_model=db_model)
		return self.__build_log_handler(
			name=name, log_handler=DatabaseLogger, init_kwargs=init_kwargs,
			level=kwargs.get('level'), formatter=kwargs.get("formatter"), filters=kwargs.get('filters')
		)

	def __build_log_handler(self, name, log_handler: logging.Handler, init_kwargs: dict = None, **kwargs):
		init_kwargs = init_kwargs if isinstance(init_kwargs, dict) else {}
		log_filters = kwargs.get("filters") or []
		log_formatter = kwargs.get("formatter") or self._default_format_str
		log_level = kwargs.get("level") or self._default_log_level

		_handler = log_handler(**init_kwargs)
		_handler.setLevel(level=log_level)
		_handler.setFormatter(logging.Formatter(log_formatter, datefmt=LOG_DATETIME_FORMAT))
		for log_filter in log_filters:
			_handler.addFilter(log_filter)
		self._registered_handlers.append(name)
		return _handler



