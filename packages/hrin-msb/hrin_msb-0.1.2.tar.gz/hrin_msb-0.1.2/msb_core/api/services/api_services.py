from msb_core.classes import Singleton
from msb_core.exceptions import CustomExceptionHandler,AppException
from msb_core.wrappers.encryption import Cipher


class ApiService(CustomExceptionHandler, metaclass=Singleton):
	__error_msg = 'BaseService.db_model not found.'
	db_model = None

	@property
	def cipher(self):
		return Cipher

	def create(self, **model_data):
		try:
			if self.db_model is None:
				raise AppException(self.__error_msg)

			model = self.db_model(**model_data)
			model.save()
			return model
		except Exception as e:
			return False

	def update(self, pk=None, **model_data):
		try:
			if self.db_model is None:
				raise AppException(self.__error_msg)
			res = self.db_model.objects.filter(pk=pk).update(**model_data)
			if not res:
				raise Exception
			return True
		except Exception as e:
			raise Exception('Update Operation Failed')

	def retrieve(self, pk=None):
		try:
			if self.db_model is None:
				raise AppException(self.__error_msg)
			return self.db_model.objects.get(pk=pk)
		except Exception:
			return False

	def delete(self, pk=None):
		try:
			if self.db_model is None:
				raise AppException(self.__error_msg)
			status = self.db_model.objects.get(pk=pk).delete()
			if not status:
				raise Exception
			return status
		except Exception as e:
			raise Exception('Delete Operation Failed')

	def list(self, fields: list = None, filters: dict = None):
		try:
			if self.db_model is None:
				raise AppException(self.__error_msg)
			fields = fields if type(fields) == list else []
			filters = filters if type(filters) == dict else dict()
			data_list = self.db_model.objects.only(*fields).filter(**filters).all()
			return data_list
		except Exception as e:
			self.handle_exception(e)
			return False
