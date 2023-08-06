class AppException(Exception):
	_message: str = ''
	_errors: list = []
	_code: int = 600

	def __init__(self, message: str = None, errors: list = None):
		super().__init__(message if message is not None else self._message)
		self._errors = errors if isinstance(errors, dict) else list()

	@property
	def message(self):
		return self._message

	@property
	def errors(self):
		return self._errors

	@property
	def code(self):
		return self._code

	def log(self):
		import logging
		logging.exception(self)


class ApiException(AppException):
	def __init__(self, message: str = None, errors: dict = None):
		super().__init__(message=message, errors=errors)
