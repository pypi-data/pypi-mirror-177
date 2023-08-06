from msb_core.auth import TokenUser

import rest_framework_simplejwt.authentication as jwtauth


class JwtTokenAuthentication(jwtauth.JWTTokenUserAuthentication):
	"""
	This class overrides the "JWTTokenUserAuthentication", so that we can implement
	custom authentication rules over the default system

	"""

	def __validate_token_integrity(self, request=None, token: TokenUser = None) -> bool:
		return token.is_authenticated

	def authenticate(self, request):
		auth_result = super(jwtauth.JWTTokenUserAuthentication, self).authenticate(request=request)
		if auth_result:
			token_user: TokenUser = auth_result[0]
			token_user.set_validation_status(
				self.__validate_token_integrity(request=request, token=token_user)
			)
		return auth_result
