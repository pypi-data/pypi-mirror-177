from msb_core.exceptions import AppException
from msb_core.db.models import MsbModel
from dataclasses import dataclass


@dataclass
class SearchParameter:
	def __init__(self):
		self._filters = dict()
		self._fields = []
		self._order_by = 'ASC'
		self._limit = 50
		self._offset = 0
		self._order_field = None
		self._db_model = None

	@property
	def filters(self) -> dict:
		return self._filters

	@property
	def fields(self) -> list:
		return self._fields

	@property
	def order_by(self) -> str:
		return self._order_by

	@property
	def limit(self) -> int:
		return self._limit

	@property
	def offset(self) -> int:
		return self._offset

	@property
	def order_field(self) -> str:
		return self._order_field

	@property
	def db_model(self) -> MsbModel:
		return self._db_model

	@filters.setter
	def filters(self, value: dict):
		if value is not None:
			self._filters = value

	@fields.setter
	def fields(self, value: list):
		if value is not None:
			self._fields = value

	@order_by.setter
	def order_by(self, value: str):
		if value is not None:
			self._order_by = value

	@limit.setter
	def limit(self, value: int):
		if value is not None:
			self._limit = value

	@offset.setter
	def offset(self, value: int):
		if value is not None:
			self._offset = value

	@order_field.setter
	def order_field(self, value: str):
		if value is not None:
			self._order_field = value

	@db_model.setter
	def db_model(self, value: MsbModel):
		self._db_model = value

	@property
	def search(self):
		try:
			if self.db_model is None:
				raise AppException(self.__error_msg)
			return self._db_model.objects.only(*self._fields).filter(**self._filters).all()[
			       self._offset:self._offset + self._limit]
		except Exception as e:
			self.handle_exception(e)
			return False
