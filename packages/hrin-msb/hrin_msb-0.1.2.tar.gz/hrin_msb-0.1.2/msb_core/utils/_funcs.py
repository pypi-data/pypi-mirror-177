import sys, os
from unittest import _log


def add_paths_to_system(*path_list):
	for path in path_list:
		sys.path.append(path)


def init_django_app(settings_dir: str, **kwargs):
	import django
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{settings_dir}.settings")
	os.environ.setdefault("PYTHONUNBUFFERED", 1)

	if isinstance(kwargs.get('sys_pathlist'), list):
		add_paths_to_system(*kwargs.get('sys_pathlist'))
	django.setup()


def log_to_console(msg, format=False, **kwargs):
	_fill_char = "#"
	_fill_count = 100
	_log = msg
	if format:
		_log = """\n {msg}:{fill_char}^{fill_count}""".format(
			msg=msg, fill_char=_fill_char, fill_count=_fill_count
		)

	return print(_log)
