from functools import wraps

import rest_framework.request

from ._exceptions import (InvalidPayloadException, InvalidParamsException)
from msb_core.api.request import ApiResponse


class Validate:

	@staticmethod
	def raw_schema(rules: dict = None, data=None, *args, **kwargs):
		if not isinstance(rules, dict) or data is None:
			return

		allow_unknown = kwargs.get('unknown') == True
		from cerberus.validator import Validator
		_validator = Validator(rules, allow_unknown=allow_unknown)
		_validator.validate(data)
		errors = _validator.errors
		return errors if len(errors.keys()) > 0 else None

	@staticmethod
	def request_data(rule: dict = None, params: dict = None, **opt):
		def outer_func(_func):
			@wraps(_func)
			def inner_func(cls, request: rest_framework.request.Request, *args, **kwargs):
				try:

					# validate paload data if payload rules are defined
					payload_validation_errors = Validate.raw_schema(rules=rule, data=request.data)
					if payload_validation_errors:
						raise InvalidPayloadException(errors=payload_validation_errors)

					# validate parameter data like from URL/Query string if parameter
					# validation rules are defined
					params_validation_errors = Validate.raw_schema(rules=params, data=kwargs)
					if params_validation_errors:
						raise InvalidParamsException(errors=params_validation_errors)

					return _func(cls, *args, **dict(request=request, **kwargs))

				except InvalidPayloadException as e:
					return ApiResponse.exception(e)

				except InvalidParamsException as e:
					return ApiResponse.exception(e)

				except Exception as e:
					return ApiResponse.exception(e)

			return inner_func

		return outer_func

	@staticmethod
	def access(group: list = None, action: str = '', **opt):
		def decorator_function(_decorated_function):
			@wraps(_decorated_function)
			def wrapper_function(cls, request: rest_framework.request.Request, *args, **kwargs):
				try:
					return _decorated_function(cls, *args, **dict(request=request, **kwargs))
				except Exception as e:
					ApiResponse.error(e)

			return wrapper_function

		return decorator_function
