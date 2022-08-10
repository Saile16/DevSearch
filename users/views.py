from multiprocessing import context
from django.shortcuts import render
from .models import Profile
# Create your views here.

def profiles(request):
    profiles=Profile.objects.all()
    context={
        'profiles':profiles
    }
    return render(request, 'users/profiles.html',context)


def userProfile(request,pk):
    profile=Profile.objects.get(id=pk)
    #aqui decimos que nos entreguen y que excluyan los skills que tengan '' 
    #mejor dicho que esten vacios
    topSkills=profile.skill_set.exclude(description__exact='')
    #aqui por otro lado filtramos y nos entregan aquellos skills que esten vacios
    otherSkills=profile.skill_set.filter(description='')
    context={
        'profile':profile,
        'topSkills':topSkills,
        'otherSkills':otherSkills
    }
    return render(request, 'users/user-profile.html',context)
