from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
		url(r'^request_attributes/', 'django_sensible.identity.requestAttributes', name='request_attributes'),
		url(r'^attributes_redirect/', 'django_sensible.identity.attributesRedirect', name='attributes_redirect'),
		url(r'^test/', 'django_sensible.identity.test'),
		)
