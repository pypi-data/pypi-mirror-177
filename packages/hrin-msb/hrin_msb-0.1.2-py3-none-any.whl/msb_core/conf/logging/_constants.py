import logging

CHOICES_LOG_LEVELS = (
	(logging.INFO, 'INFO'),
	(logging.DEBUG, 'DEBUG'),
	(logging.WARNING, 'WARNING'),
	(logging.ERROR, 'ERROR'),
	(logging.CRITICAL, 'CRITICAL'),
)

LOG_DB = "logs"
LOG_TABLE = "system_logs"

DEBUG_REQUIRED_FILTER_CLASS = "django.utils.log.RequireDebugTrue"
DEBUG_REQUIRED_FILTER_NAME = 'require_debug_true'

SIMPLE_LOG_FORMAT = '[%(levelname)s] : %(message)s '
SIMPLE_LOG_FILE_FORMAT = '[%(levelname)s] %(asctime)s : %(message)s '
VERBOSE_LOG_FORMAT = "%(levelname)s %(asctime)s %(module)s %(process:d)s %(thread:d)s %(message)s "

LOG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_FILTERS = {
	DEBUG_REQUIRED_FILTER_NAME: {"()": DEBUG_REQUIRED_FILTER_CLASS}
}
