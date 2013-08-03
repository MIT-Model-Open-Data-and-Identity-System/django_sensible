from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
		url(r'^authorize/', 'django_sensible.oauth2.authorize', name='authorize'),
		url(r'^authorize_refreshed/', 'django_sensible.oauth2.authorizeRefreshedUser', name='authorize_refreshed'),
		url(r'^grant/', 'django_sensible.oauth2.grant', name='grant'),
		)
