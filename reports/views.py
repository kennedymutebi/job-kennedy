from django.db import models
from rest_framework import serializers
from models import notes


class notes (models.model):
    title=models.charField(max_length=10)
    content=model.TextField(max_length=100,null=true,black=true)
    created_at=models.DateTimeField(auto_add_now=true)

    def __str__(self):
        return self.notes

 #        
class notesSerializers(serializers.modelserializer):
    class meta
             model=notes
             fields= "_all_" 
from rest_framework import viewsets
from models import notes
from serializers import notesSerializers
class notesviewset(viewsets.ModelVewset)
   gueryset=notes.object.all()
   serializer_class=notesSerializers

from django.urls import path, include
from rest_framework.routers import DefaltRouter
from .views import notesviewset

routers=DefaltRouter()
routers.register(r"notes", notesviewset )

urlpatterns=[
    path("",include(routers.urls))
]



