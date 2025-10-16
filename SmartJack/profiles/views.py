from django.http import HttpResponse
from django.template import loader
from .models import Profile

def profiles(request):
    myprofiles = Profile.objects.all().values()
    template = loader.get_template('all_profiles.html')
    context = {
        'myprofiles': myprofiles,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myprofile = Profile.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myprofile': myprofile,
    }
    return HttpResponse(template.render(context, request))