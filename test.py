from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def test(request):
	return HttpResponse("dragons! "+request.user.username)
