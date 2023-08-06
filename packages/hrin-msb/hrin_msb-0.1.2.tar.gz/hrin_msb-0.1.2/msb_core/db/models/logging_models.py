import logging

from django.db.models import (manager, Model, DateTimeField, IntegerField, CharField, TextField)

from msb_core.conf.logging import (LOG_DB, LOG_TABLE, CHOICES_LOG_LEVELS)


class LoggingModelManager(manager.BaseManager):
	log_db = LOG_DB

	def get_queryset(self):
		return super().get_queryset().using(self.log_db)


class LoggingModel(Model):
	class Meta:
		abstract = True
		managed = False

	level = CharField(choices=CHOICES_LOG_LEVELS, max_length=255, default=logging.INFO)
	message = TextField(default=None, null=True)
	created_at = DateTimeField(auto_now_add=True, db_column='created_at')


class SystemLogModel(LoggingModel):
	class Meta:
		db_table = LOG_TABLE
		abstract = True
		managed = False

	logger = CharField(max_length=255, default='root')

	msg = TextField(default=None)
	module = CharField(max_length=255, default=None, null=True)
	func_name = CharField(max_length=255, default=None, null=True)
	thread_name = CharField(max_length=255, default=None, null=True)
	process_name = CharField(max_length=255, default=None, null=True)
	filename = CharField(max_length=255, default=None, null=True)

	args = TextField(default=None, null=True)
	pathname = TextField(default=None, null=True)
	exc_info = TextField(default=None, null=True)
	exc_text = TextField(default=None, null=True)
	stack_info = TextField(default=None, null=True)
	lineno = IntegerField(default=0, null=True)

	objects = LoggingModelManager()

	def __init__(self, *args, **logdetails):
		super(SystemLogModel, self).__init__(*args, **{})

		self.logger = logdetails.get('name')
		self.level = logdetails.get('levelname')
		self.msg = logdetails.get('msg')
		self.message = logdetails.get('message')
		self.module = logdetails.get('module')
		self.filename = logdetails.get('filename')

		self.func_name = logdetails.get('funcName')
		self.thread_name = logdetails.get('threadName')
		self.process_name = logdetails.get('processName')
		self.args = logdetails.get('args')
		self.pathname = logdetails.get('pathname')
		self.exc_info = logdetails.get('exc_info')
		self.exc_text = logdetails.get('exc_text')
		self.stack_info = logdetails.get('stack_info')
		self.lineno = logdetails.get('lineno')
