from django.shortcuts import render,redirect
from .models import Project,Review,Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def projects(request):
    projects=Project.objects.all()
    context={
        'projects':projects
    }
    return render(request, 'projects/projects.html',context)

def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    #los tag los podemos pedir desde aqui o desde el mismo template
    # tags=projectObj.tags.all()
    context={
        'project':projectObj,
        # 'tags':tags
        
    }
    return render(request, 'projects/single-project.html',context)


@login_required(login_url='login')
def createProject(request):
    #obtenemos el usuario logueado
    profile=request.user.profile
    form = ProjectForm()
    if request.method=='POST':
        # print(ProjectForm(request.POST))
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            #y lo guardamos en la base de datos project.owner diciendo que es el usuario logueado
            project.owner=profile
            project.save()
            return redirect('account')
    context={
        'form':form
    }
    return render(request, 'projects/project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    profile=request.user.profile
    #esto lo hacemos para queel usuario solo pueda editar/eliminar sus proyectos
    #y no de otros a pesar de sber las url
    project=profile.project_set.get(id=pk)
    # project=Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={
        'form':form
    }
    return render(request, 'projects/project_form.html',context)
    
@login_required(login_url='login')
def deleteProject(request,pk):
    project=Project.objects.get(id=pk)
    if request.method=='POST':
        project.delete()
        return redirect('projects')
    context={
        'object':project
    }
    return render(request, 'delete_template.html',context)