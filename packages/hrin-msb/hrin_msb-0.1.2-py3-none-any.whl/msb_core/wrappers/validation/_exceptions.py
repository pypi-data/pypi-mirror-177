from msb_core.exceptions import ApiException



class InvalidPayloadException(ApiException):
	_message = 'Invalid Request Data.'


class InvalidParamsException(ApiException):
	_message = 'Invalid Request Parameters.'
