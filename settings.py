INSTALLED_APPS = (
	'django_openid_auth',
	'bootstrap_toolkit',
	'south',
)

OPENID_SSO_SERVER_URL = "https://54.229.13.160/sensible-data/openid/xrds/"

#service config
SERVICE_URL = 'https://54.229.13.160/sensible-dtu/'
AUTH_ENDPOINT = 'authorization_manager/'
CONNECTOR = 'connector_questionnaire'
SERVICE_TOKEN_URL = SERVICE_URL + 'connectors/' + CONNECTOR + '/auth/token/'
SERVICE_REFRESH_TOKEN_URL = SERVICE_URL + 'connectors/' + CONNECTOR + '/auth/refresh_token/'
SERVICE_MY_REDIRECT_SUFFIX = 'oauth2/grant/'


#idp settings
IDP_URL = 'https://54.229.13.160/sensible-data/'
IDP_AUTHORIZATION_URL = IDP_URL+'oauth2/oauth2/authorize/?'
IDP_MY_REDIRECT_SUFFIX = 'identity/attributes_redirect/'

LOGIN_URL_SUFFIX = 'openid/login/'
OPENID_USE_EMAIL_FOR_USERNAME = False
AUTHENTICATION_BACKENDS = (
		'django_openid_auth.auth.OpenIDBackend',
		'django.contrib.auth.backends.ModelBackend',
)

def failure_handler_function(request, message, status=None, template_name=None, exception=None):
	from django.shortcuts import redirect
	from django.http import HttpResponse
	registration = request.REQUEST.get('registration', False)
	if registration: return redirect('login')
	return redirect('openid_failed')


OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = False
OPENID_RENDER_FAILURE = failure_handler_function
