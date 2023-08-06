from ._schema import InputField


class DefaultRules:
	date = InputField.Date(regex="^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$")
	pk = InputField.String(required=True)
	gender = InputField.String(allowed=['M', 'F', 'O'])
