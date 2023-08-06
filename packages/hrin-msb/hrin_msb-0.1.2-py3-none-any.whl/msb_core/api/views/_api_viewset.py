from . import _constants as API_CONST
from msb_core.wrappers.validation import DefaultRules, Validate

from ..wrappers import (ApiResponse, RestResponse)
from ..services import ApiService
from ._api_view import ApiView





class ApiViewset(ApiView):
	service_class: ApiService = None
	validation_rules = None
	allowed_crud = []

	@classmethod
	def crud_routes(cls, actions=None, **initkwargs):
		from django.urls import path
		return [
			path("", cls.as_view(actions={"post": "create"})),
			path("/list", cls.as_view(actions={"get": "list"})),
			path(
				"/<str:pk>",
				cls.as_view({"get": "retrieve", "put": "update", "delete": "delete"})
			),
		]

	@Validate.request_data(params=dict(pk=DefaultRules.pk.schema))
	def retrieve(self, *args, **kwargs) -> RestResponse:
		if self.service_class is None or API_CONST.RETRIEVE_ACTION not in self.allowed_crud:
			return self.api_response.method_not_allowed()
		try:
			pk = kwargs.get('pk')
			result = self.service_class.retrieve(pk=pk)
			return self.api_response.success(data=self.serializer(data=[result]))
		except Exception as e:
			return self.api_response.exception(e=e)

	@Validate.request_data(params=dict(pk=DefaultRules.pk.schema))
	def delete(self, *args, **kwargs) -> RestResponse:
		if self.service_class is None or API_CONST.DELETE_ACTION not in self.allowed_crud:
			return self.api_response.method_not_allowed()
		try:
			pk = kwargs.get('pk')
			result = self.service_class.delete(pk=pk)
			return self.api_response.success() if result else self.api_response.error()
		except Exception as e:
			return self.api_response.exception(e=e)

	def create(self, *args, **kwargs) -> RestResponse:
		if self.service_class is None or API_CONST.CREATE_ACTION not in self.allowed_crud:
			return self.api_response.method_not_allowed()
		try:
			rule = self.validation_rules.create if \
				hasattr(self.validation_rules, API_CONST.CREATE_ACTION) else {}
			data, *_ = self.validate_data(rule=rule, data=self.payload)
			data['created_by'] = self.user.id
			result = self.service_class.create(**data)
			return self.api_response.success() if result else self.api_response.error()
		except Exception as e:
			return self.api_response.exception(e)

	@Validate.request_data(params=dict(pk=DefaultRules.pk.schema))
	def update(self, *args, **kwargs) -> RestResponse:
		if self.service_class is None or API_CONST.UPDATE_ACTION not in self.allowed_crud:
			return self.api_response.method_not_allowed()
		try:
			pk = kwargs.get('pk')
			rule = self.validation_rules.update if \
				hasattr(self.validation_rules, API_CONST.UPDATE_ACTION) else {}
			data, *_ = self.validate_data(rule=rule, data=self.payload)
			data['updated_by'] = self.user.id
			res = self.service_class.update(pk=pk, **data)
			if not res:
				raise Exception
			return self.api_response.success()
		except Exception as e:
			return self.api_response.exception(e=e)

	@Validate.request_data(params=None)
	def list(self, *args, **kwargs) -> RestResponse:
		if self.service_class is None or API_CONST.LIST_ACTION not in self.allowed_crud:
			return self.api_response.method_not_allowed()
		try:
			requested_fields = self.payload.get('fields')
			requested_filters = self.payload.get('filters')
			result = self.service_class.list(fields=requested_fields, filters=requested_filters)
			return self.api_response.success(data=self.serializer(data=result))
		except Exception as e:
			return self.api_response.exception(e=e)
