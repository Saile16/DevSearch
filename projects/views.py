from django.shortcuts import render
from .models import Project,Review,Tag
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