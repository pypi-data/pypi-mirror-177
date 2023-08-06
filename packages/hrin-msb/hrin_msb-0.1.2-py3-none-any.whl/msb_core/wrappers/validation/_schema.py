class RuleSchema(object):
	# type of the field
	_type: str

	# checks if value contains this.
	_contains: list

	# if the field is required
	_required: bool

	# validates if the value is empty

	_empty: bool

	# minmum value (if int)
	_min: int

	# maximum value (if int)
	_max: int

	# minmum length(if str)
	_minlength: int

	# maximum length(if str)
	_maxlength: int

	# list of allowed values
	_allowed: list

	# Opposite to allowed
	_forbidden: list

	# list of particaular types
	_items: list

	# value should match, this regex
	_regex: str

	# list of sub schemas
	_a_list: list

	# dict of sub schemas
	_a_dict: dict

	# if the value can be None
	_nullable: bool

	# exclude the field name (field names in the list wont be validated)
	_excludes: list

	# all of these must be present in order for the target field to be validated.
	_dependencies: list

	def __set_min(self, val: int):
		if val is not None:
			if self._type in ['number', 'int', 'float']:
				self._min = val
			else:
				self._minlength = val
		return self

	def __set_max(self, val: int):
		if val is not None:
			if self._type in ['number', 'int', 'float']:
				self._max = val
			else:
				self._maxlength = val
		return self

	def __set_empty(self, val: bool):
		if isinstance(val, bool):
			self._empty = val
		return self

	def __set_regex(self, val: str):
		if isinstance(val, str) and len(val.strip()) > 0:
			self._regex = val
		return self

	def __set_required(self, val: bool):
		self._required = (val == True)
		return self

	def __set_contains(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._contains = val
		return self

	def __set_allowed(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._allowed = val
		return self

	def __set_forbidden(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._forbidden = val
		return self

	def __set_items(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._items = val
		return self

	def __set_a_list(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._a_list = val
		return self

	def __set_excludes(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._excludes = val
		return self

	def __set_dependencies(self, val: list):
		if isinstance(val, list) and len(val) > 0:
			self._dependencies = val
		return self

	def __set_a_dict(self, val: dict):
		if isinstance(val, dict) and len(val.keys()) > 0:
			self._a_dict = val
		return self

	def __set_nullable(self, val: bool):
		if val is not None:
			self._nullable = val
		return self

	@property
	def schema(self):
		return {str(k).lstrip('_'): v for k, v in self.__dict__.items()}

	def __init__(self, **kwargs):
		self.__set_required(kwargs.get('required'))
		self.__set_min(kwargs.get('minimum'))
		self.__set_max(kwargs.get('maximum'))
		self.__set_empty(kwargs.get('empty'))
		self.__set_contains(kwargs.get('contains'))
		self.__set_allowed(kwargs.get('allowed'))
		self.__set_forbidden(kwargs.get('forbidden'))
		self.__set_items(kwargs.get('items'))
		self.__set_regex(kwargs.get('regex'))
		self.__set_a_list(kwargs.get('a_list'))
		self.__set_a_dict(kwargs.get('a_dict'))
		self.__set_nullable(kwargs.get('nullable'))
		self.__set_excludes(kwargs.get('excludes'))
		self.__set_dependencies(kwargs.get('dependencies'))

	def clone(self, **kwargs):
		import copy
		_copy = copy.deepcopy(self)
		_copy.__set_required(kwargs.get('required'))
		_copy.__set_min(kwargs.get('minimum'))
		_copy.__set_max(kwargs.get('maximum'))
		_copy.__set_empty(kwargs.get('empty'))
		_copy.__set_contains(kwargs.get('contains'))
		_copy.__set_allowed(kwargs.get('allowed'))
		_copy.__set_forbidden(kwargs.get('forbidden'))
		_copy.__set_items(kwargs.get('items'))
		_copy.__set_regex(kwargs.get('regex'))
		_copy.__set_a_list(kwargs.get('a_list'))
		_copy.__set_a_dict(kwargs.get('a_dict'))
		_copy.__set_nullable(kwargs.get('nullable'))
		_copy.__set_excludes(kwargs.get('excludes'))
		_copy.__set_dependencies(kwargs.get('dependencies'))
		return self


class InputField(object):
	# Python Types : string
	class String(RuleSchema):
		_type = 'string'

	# Python Types : float, int, excl. bool
	class Number(RuleSchema):
		_type = 'number'

	# Python Types : int
	class Integer(RuleSchema):
		_type = 'integer'

	# Python Types : float, int, excl. bool
	class Float(RuleSchema):
		_type = 'float'

	# Python Types : bool
	class Boolean(RuleSchema):
		_type = 'date'

	# Python Types : datetime.date
	class Date(RuleSchema):
		_type = 'date'

	# Python Types : datetime.date
	class Datetime(RuleSchema):
		_type = 'datetime'

	# Python Types : collections.abc.Mapping
	class Dictionary(RuleSchema):
		_type = 'dict'

	# Python Types : collections.abc.Sequence, excl. string
	class List(RuleSchema):
		_type = 'list'

	# Python Types : set
	class Set(RuleSchema):
		_type = 'set'

	# Python Types : bytes, bytearray
	class Binary(RuleSchema):
		_type = 'binary'
