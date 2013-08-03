from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
		url(r'^openid/', include('django_openid_auth.urls')),
		url(r'^oauth2/', include('django_sensible.oauth2_urls')),
		url(r'^identity/', include('django_sensible.identity_urls')),
		url(r'^logout/', 'django_sensible.logout.do_logout', name = 'logout'),
		url(r'^login/', 'django_sensible.login.do_login', name = 'login'),
		url(r'^quit/', 'django_sensible.views.quit', name = 'quit'),
		url(r'^logout_success', 'django_sensible.views.logout_success', name='logout_success'),
		url(r'^openid_failed', 'django_sensible.views.openid_failed', name='openid_failed'),
		url(r'^changebrowser','django_sensible.views.changebrowser',name='changebrowser'),
		url(r'^noscript','django_sensible.views.noscript', name='noscript'),
		url(r'^test/', 'django_sensible.test.test', name = 'test'),
)
