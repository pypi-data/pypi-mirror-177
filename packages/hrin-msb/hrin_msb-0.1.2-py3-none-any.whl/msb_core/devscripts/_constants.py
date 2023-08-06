
REGEX_CONFIG_VARIABLE_SELECT_PATTERN = r"(\r\n|\r|\n|\s)*?([\w_]*)=(['\"])?([\w\d()\-:/*?=@.+!%$_#^&,]*)(['\"])?([\s\r\n]*)"

REGEX_CONFIG_VARIABLE_REPLACEMENT_PATTERN = r'\1\2=\3\2_VALUE\5\6'
