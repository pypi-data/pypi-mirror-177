class MsbDatabaseRouter:
	__app_labels: list = []
	_app_relations: list = __app_labels
	_db_for_read: str = 'default'
	_db_for_write: str = 'default'
	db_mapping: dict = {
		"default": dict(read="default", write="default")
	}

	"""Determine how to route database calls for an app's models (in this case, for an app named 
	Example). All other models will be routed to the next router in the DATABASE_ROUTERS setting 
	if applicable, or otherwise to the default data_base. """

	def db_for_read(self, model):
		"""Send all read operations on Example app models to `example_db`."""
		if model._meta.app_label in self.__app_labels:
			return self.__db_for_read(app_label=model._meta.app_label)
		return None

	def db_for_write(self, model):
		"""Send all write operations on Example app models to `example_db`."""
		if model._meta.app_label in self.__app_labels:
			return self.__db_for_write(app_label=model._meta.app_label)
		return None

	def allow_relation(self, obj1, obj2):
		"""Determine if relationship is allowed between two objects."""

		# Allow any relation between two models that are both in the Example app.
		if obj1._meta.app_label in self._app_relations and obj2._meta.app_label in self._app_relations:
			return True
		# No opinion if neither object is in the Example app (defer to default or other routers).
		elif obj1._meta.app_label not in self._app_relations and obj2._meta.app_label not in self._app_relations:
			return None

		# Block relationship if one object is in the Example app and the other isn't.
		return False

	def allow_migrate(self, db, app_label, model_name=None):
		"""Ensure that the Example app's models get created on the right data_base."""
		if app_label in self.__app_labels:
			# The Example app should be migrated only on the example_db data_base.
			return db == self._db_for_write
		elif db == '':
			# Ensure that all other apps don't get migrated on the example_db data_base.
			return False

		# No opinion for all other scenarios
		return None

	def __init__(self):
		self.__app_labels = self.db_mapping.keys()

	def __db_for_read(self, app_label) -> str:
		return self.db_mapping.get(app_label).get("read")

	def __db_for_write(self, app_label) -> str:
		return self.db_mapping.get(app_label).get("write")
