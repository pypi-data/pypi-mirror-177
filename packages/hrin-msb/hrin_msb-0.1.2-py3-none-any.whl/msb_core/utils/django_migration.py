import os

from django.core.management import call_command
from django.db import connections

from ._dto import DbVendorConfig
from ._constants import DJANGO_MIGRATION_DB_VENDOR_CONFIG
from ._funcs import log_to_console

class DjangoMigration():
	migration_dir: str = None
	__vendor_config: dict = None

	def __execute_cmd(self, *args):
		#print(f"""\n {f" executing {' '.join(args if len(args) > 0 else 'all')} ":#^100}""")
		log_to_console(msg=f" executing {' '.join(args if len(args) > 0 else 'all')} ")
		call_command(*args)

	def __db_query(self, db_connection, *queries):
		if db_connection and len(queries) > 0:
			with db_connection.cursor() as cursor:
				_result = []
				for query in queries:
					print(f"Executing Query = {query}\n")
					query_result = cursor.execute(query)
					if query.lstrip(' ').lower().startswith(('select', 'show')):
						_result.append(cursor.fetchall())
					else:
						_result.append(query_result)
				return _result[0] if len(_result) == 1 else _result

	def __init__(self, migration_dir):
		self.migration_dir = migration_dir
		self.__vendor_config = DJANGO_MIGRATION_DB_VENDOR_CONFIG

	def __get_db_vendor_config(self, db_connection) -> DbVendorConfig:
		if db_connection and hasattr(db_connection, 'vendor'):
			return self.__vendor_config.get(getattr(db_connection, 'vendor'))
		return None

	def remove_files(self):
		for miration_file in os.listdir(self.migration_dir):
			if miration_file not in ['__init__.py', '__pycache__']:
				os.remove(os.path.join(self.migration_dir, miration_file))
				print(f"Removed Migration File {miration_file}")

	def remove_tables(self, *db_list):
		for db in db_list:
			con = connections[db]
			db_config = self.__get_db_vendor_config(db_connection=con)
			if db_config:
				table_list = self.__db_query(con, db_config.query_to_list_tables)
				queries_to_drop_tables = db_config.queries_to_drop_multiple_tables(table_list, )

				self.__db_query(con, *[*queries_to_drop_tables])

	def build(self, *apps):
		return self.__execute_cmd(*["makemigrations", *apps])

	def migrate_databases(self, *db_list):
		for db in db_list:
			self.__execute_cmd("migrate", "--database", db)
