from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import Project


class ProjectSerializer(ModelSerializer):
    technologies = StringRelatedField(many=True)
    
    class Meta:
        model = Project
        exclude = ["created_at"]
