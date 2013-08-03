from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import uuid
import hashlib
from .models import *
import SECURE_CONFIG
from django.shortcuts import redirect
import urllib, urllib2
import json
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import json
from datetime import datetime
from django.conf import settings

def authorize(request):
	try:
		sessions = Session.objects.filter(expire_date__gte=datetime.now())
		for session in sessions:
			data = session.get_decoded()
			try: user = User.objects.filter(id=data.get('_auth_user_id', None))[0]
			except: continue
			if request.user == user:
				session.delete()
	except: pass

	return redirect(settings.SENSIBLE_URL+'oauth2/authorize_refreshed/')

@login_required
def authorizeRefreshedUser(request):
	state = generateState(request.user)
	url = settings.SERVICE_URL + settings.AUTH_ENDPOINT + settings.CONNECTOR
	url += '/auth/grant/?'
	url += 'scope='+','.join([s.scope for s in Scope.objects.filter(type=Type.objects.get(type='data'))])
	url += '&client_id='+SECURE_CONFIG.CLIENT_ID
	url += "&response_type=code"
	url += '&state='+state
	return redirect(url)
	#return HttpResponse(url)


def generateState(user):
	return State.objects.create(user=user).nonce


@csrf_exempt
@login_required
def grant(request):
	error = request.GET.get('error', '')
	if not error == '':
		return redirect(settings.ROOT_URL+'quit/&status=auth_error')
	token = exchangeCodeForToken(request, SECURE_CONFIG.CLIENT_ID, SECURE_CONFIG.CLIENT_SECRET, redirect_uri=settings.SERVICE_MY_REDIRECT, request_uri=settings.SERVICE_TOKEN_URL)
	if 'error' in token:
				r = redirect('form')
				r['Location'] += '?status=error&message='+token['error']
				return r

	if saveToken(request.user, token):
		return redirect('home')
	else:
		r = redirect('form')
		r['Location'] += '?status=error&message=something went wrong in the process (code 5784)'
		return r

def exchangeCodeForToken(request, client_id, client_secret, redirect_uri, request_uri):
	state = request.REQUEST.get('state', '')
	code = request.REQUEST.get('code', '')
	scope = request.REQUEST.get('scope', '')
	if not validateState(request.user, state): return {'error': 'something went wrong in the process (code 8438)'}
	try: Scope.objects.get(scope=scope)
	except Scope.DoesNotExist: return {'error':'something went wrong in the process (code 7843)'}
	values = {}
	values['code'] = code
	values['grant_type'] = 'authorization_code'
	values['client_id'] = client_id
	values['client_secret'] = client_secret
	values['redirect_uri'] = redirect_uri
	data = urllib.urlencode(values)
		
	req = urllib2.Request(request_uri, data)
	try:
		response = urllib2.urlopen(req).read()
	except urllib2.HTTPError as e:
		response = e.read()
		return response

	return json.loads(response)

def exchangeRefreshTokenForToken(refresh_token, scopes, client_id, client_secret, redirect_uri, request_uri):
	values = {}
	values['refresh_token'] = refresh_token
	values['grant_type'] = 'refresh_token'
	values['client_id'] = client_id
        values['client_secret'] = client_secret
        values['redirect_uri'] = redirect_uri
        values['scope'] = ','.join([x.scope for x in scopes])
        data = urllib.urlencode(values)

        req = urllib2.Request(request_uri, data)
        try:
                response = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
                response = e.read()
                return response

        return json.loads(response)
	

def validateState(user, state):
	try: state_user = State.objects.get(nonce=state).user
	except State.DoesNotExist: return False
	if not user == state_user: return False
	return True

def saveToken(user, token):
	for scope in token['scope'].split(','):
		try: 
			a = AccessToken.objects.get(user=user, scope=Scope.objects.get(scope=scope))
			a.token = token['access_token']
			a.refresh_token = token['refresh_token']
		except AccessToken.DoesNotExist:
			a = AccessToken.objects.create(user=user, token=token['access_token'], refresh_token=token['refresh_token'])
			a.scope.add(Scope.objects.get(scope=scope))
		except Scope.DoesNotExist:
			a = AccessToken.objects.create(user=user, token=token['access_token'], refresh_token=token['refresh_token'])
			a.scope.add(Scope.objects.get(scope=scope))
		a.save()

	return True
	
def getToken(user, scope):
	try: a = AccessToken.objects.get(user=user, scope=Scope.objects.get(scope=scope))
	except AccessToken.DoesNotExist: return None
	return a.token


def query(request_uri, token, params, client_id, client_secret, redirect_uri, refresh_uri):
	tokens = AccessToken.objects.filter(token=token)
	scopes = set()
	response = {}
	for t in tokens:
		for s in t.scope.all():
			scopes.add(s)

	try:
		token = AccessToken.objects.filter(token=token)[0]
	except IndexError: return {'error':'no access token found'}
	url = request_uri
	url += '?bearer_token='+token.token
	url += params
	try: response = urllib2.urlopen(url).read()
	except urllib2.HTTPError as e:
		if not e.getcode() == 401:
			#something went wrong but we don't know how to recover
			return {'error': e.getcode(), 'body': e.read()}
		#401, let's try to refresh token
		new_token = exchangeRefreshTokenForToken(token.refresh_token, scopes, client_id, client_secret, redirect_uri, refresh_uri)
		if 'error' in new_token: 
			return new_token
		saveToken(token.user, new_token)


		url = request_uri
		url += '?bearer_token='+new_token['access_token']
		url += params

		try: response = urllib2.urlopen(url).read()
		except urllib2.HTTPError as e: return {'error': e.getcode(), 'body': e.read()}
	
	return json.loads(response)

