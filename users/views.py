
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from django.contrib.auth.models import User
from .models import Profile
# Create your views here.


def loginUser(request):
    #tambien podriamos usar decorators
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        #probamos si el usuario existe
        try:
            user=User.objects.get(username=username)
        except:
            print('User does not exist')
            messages.error(request,'User does not exist')
        # si no existia el usuario pasamos a autenticarlo y verificara en la db si 
        #los datos son correctos
        user=authenticate(request,username=username,password=password)

        # si el usuario es correcto lo logueamos
        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            print('Username or password is incorrect')
            messages.error(request,'Username or password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request,'You have been logged out')
    return redirect('login')

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
