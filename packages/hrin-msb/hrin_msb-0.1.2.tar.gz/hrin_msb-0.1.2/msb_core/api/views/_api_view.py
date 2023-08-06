import logging

from django.db.models import QuerySet
from rest_framework import (viewsets)
from msb_core.auth import TokenUser

from ..wrappers import (ApiResponse, RequestInfo, RequestHeaders)
from msb_core.wrappers.validation import (Validate, InvalidPayloadException)


def api_details(request=None, ver='', name=''):
	return ApiResponse.success(
		data=dict(method=request.method, version=ver, name=name)
	)


class ApiView(viewsets.GenericViewSet):
	permission_classes = ()
	serializer_class = ''

	"""
	TODO : implement following code :
	
	@staticmethod
	@renderer_classes((JSONRenderer))
	def my_exception_handler(exc, context):
		# response = exception_handler(exc, context)  # <-- this is the default exception_handler
		import logging
		logging.exception(exc)
		return ApiResponse.internal_server_error()

	def get_exception_handler(self):
		return self.my_exception_handler
	"""

	def validate_data(self, rule: None, data=None):
		validation_errors = Validate.raw_schema(rules=rule, data=data)
		if validation_errors:
			raise InvalidPayloadException(errors=validation_errors)
		return data, validation_errors

	@property
	def request_info(self) -> RequestInfo:
		return RequestInfo(meta=self.request.META)

	@property
	def request_headers(self) -> RequestHeaders:
		return RequestHeaders(headers=self.request.headers)

	@property
	def user(self) -> TokenUser:
		return self.request.user

	@property
	def payload(self) -> dict:
		return self.request.data

	@property
	def logger(self):
		return logging.getLogger('root')

	@property
	def api_response(self):
		return ApiResponse

	def serializer(self, data: list = None):
		return (
			[item.dict() if hasattr(item, 'dict') else item for item in data]
		) if (type(data) in [list, QuerySet]) else []
