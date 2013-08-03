from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
		#url(r'^oauth2/', include('utils.oauth2_urls')),
		#url(r'^identity/', include('utils.identity_urls')),
		#url(r'^logout/', 'utils.logout.do_logout', name = 'logout'),
		#url(r'^login/', 'utils.login.do_login', name = 'login'),
		url(r'^test/', 'django_sensible.test.test', name = 'test'),
)
