
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def loginUser(request):
    page='login'
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
    messages.info(request,'You have been logged out')
    return redirect('login')


def registerUser(request):
    page='register'
    form=CustomUserCreationForm()
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            #creamos la instancia sin hacer commit para normalizar el input
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'User created successfully')

            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,'An error has occurred during registration')

    context={
        'page':page,
        'form':form
    }
    return render(request, 'users/login_register.html',context)

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

@login_required(login_url='login')
def userAccount(request):
    #primero obtenemos el user logeado y lo guardamos en una variable
    profile=request.user.profile
    #filtramos y obtenemos tambien aqui los skills
    skills=profile.skill_set.all()
    projects=profile.project_set.all()
    context={
        'profile':profile,
        'skills':skills,
        'projects':projects
        
    }
    return render(request, 'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)
    if request.method=='POST':
        #obtenemos los datos del formulario
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save() 
            
            return redirect('account')
    context={
        'form':form
    }
    return render(request, 'users/profile_form.html',context)


@login_required(login_url='login')
def createSkill(request):
    profile=request.user.profile
    form=SkillForm()
    if request.method=='POST':
        form=SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill created successfully')
            return redirect('account')
    context={
        'form':form        
    }
    return render(request, 'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)
    if request.method=='POST':
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()            
            messages.success(request,'Skill was updated successfully')
            return redirect('account')
    context={
        'form':form        
    }
    return render(request, 'users/skill_form.html',context)

def deleteSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)    
    if request.method=='POST':
        skill.delete()        
        messages.success(request,'Skill was deleted successfully')
        return redirect('account')
    context={
        'object':skill
    }
    return render(request, 'delete_template.html',context)