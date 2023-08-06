import logging

from ._constants import (SIMPLE_LOG_FORMAT)


# custom log handler that emits to the database
class DatabaseLogger(logging.Handler):
	_db_model = None

	def __init__(self, db_model=None, *args, **kwargs):
		logging.Handler.__init__(self, *args, **kwargs)
		self.setFormatter(logging.Formatter(SIMPLE_LOG_FORMAT))
		self.level = logging.INFO
		self._db_model = db_model

	def emit(self, record):
		try:
			if self._db_model:
				log = self._db_model(**record.__dict__)
				log.save()
		except Exception:
			pass
