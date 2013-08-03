from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.conf import settings

def quit(request):
	return redirect(settings.SERVICE_URL+'quit')

def logout_success(request):
	return render_to_response('logout_success.html', {}, context_instance=RequestContext(request))

def noscript(request):
	return render_to_response('js_disabled.html', {}, context_instance=RequestContext(request))

def openid_failed(request):
	return render_to_response('openid_failed.html', {}, context_instance=RequestContext(request))

def changebrowser(request):
	return render_to_response('changebrowser.html', {}, context_instance=RequestContext(request))
