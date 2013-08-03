from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from .models import *
import identity

@login_required
def do_login(request):
	try: f = FirstLogin.objects.get(user=request.user)
	except FirstLogin.DoesNotExist: f = FirstLogin.objects.create(user=request.user)
	if f.firstLogin:
		f.firstLogin = False
		f.save()
	#	return redirect('request_attributes')
	identity.getAttributes(request.user, ['first_name'])
	return redirect('home')
