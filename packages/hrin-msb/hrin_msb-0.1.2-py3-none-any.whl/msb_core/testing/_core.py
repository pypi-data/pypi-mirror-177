import django
import django.test.testcases
from django.core.servers.basehttp import WSGIServer


class ApiTestResult:
	data = None
	message: str = ''
	code: int = 0
	success: bool = False

	def __init__(self, success=None, code=None, message='', data=None):
		self.data = data if data is not None else []
		self.message = message
		self.code = code
		self.success = success

	@property
	def dict(self):
		return self.__dict__


class LiveServerThreadWithReuse(django.test.testcases.LiveServerThread):
	"""
	This miniclass overrides _create_server to allow port reuse. This avoids creating
	"address already in use" errors for tests that have been run subsequently.
	"""

	def _create_server(self):
		return WSGIServer(
			(self.host, self.port),
			django.test.testcases.QuietWSGIRequestHandler,
			allow_reuse_address=True,
		)


from msb_core.classes import Singleton
from os import environ


class TestConfig(metaclass=Singleton):

	def get(self, key: str = None, default=None):
		return environ.get(f"TEST_{str(key).upper()}", default=default)

	@property
	def base_url(self):
		return self.get('BASE_URL', default=environ.get('BASE_URL', default='')).rstrip('/')

	def make_url(self, app_label: str = '', endpoint: str = '', api_version: int = 1):
		return f"{self.base_url}/{app_label.lower()}/v{api_version}/{endpoint.replace('.', '/')}"

	@property
	def default_headers(self):
		_headers = {
			'Content-Type': 'application/json'
		}
		if self.user_agent:
			_headers['HTTP_USER_AGENT'] = self.user_agent

		return _headers

	@property
	def user_agent(self):
		return self.get('USER_AGENT_STRING', default='Test User Agent 1.0')

	@property
	def request_content_type(self):
		return "application/json"

	@property
	def auth_url(self):
		return self.get('AUTH_ENDPOINT', default='')

	@property
	def auth_credentials(self):
		return dict(user=self.get('AUTH_USER'), password=self.get('AUTH_PASSWORD'), auth_type=self.get('AUTH_TYPE'))
