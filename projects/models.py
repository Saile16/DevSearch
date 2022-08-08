from django.db import models
import uuid
# Create your models here.

class Project(models.Model):
    title=models.CharField(max_length=200)
    #null decimos que no es requerido obligatoriamente y con blank que podemos dejarlo vacio
    description=models.TextField(null=True,blank=True)
    demo_link=models.CharField(max_length=600,null=True,blank=True)
    source_link=models.CharField(max_length=600,null=True,blank=True)
    tags=models.ManyToManyField('Tag',blank=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.FloatField(default=0,null=True,blank=True)
    #el autonowadd crea automaticamente el tiepo de creacion
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    VOTE_TYPE=(
        ('up','Up Vote'),
        ('down','Down Vote'),
    )
    #owner=
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=10,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.body


class Tag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self):
        return self.name