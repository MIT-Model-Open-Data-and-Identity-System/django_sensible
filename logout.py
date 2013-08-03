from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

def do_logout(request):
	if request.user.is_authenticated():
		logout(request)
		#TODO ping platform to see if it is alive, otherwise don't redirect
		return redirect(settings.IDP_URL+'accounts/logout/?next='+settings.SENSIBLE_URL+'logout/')	
	return redirect('logout_success')	
