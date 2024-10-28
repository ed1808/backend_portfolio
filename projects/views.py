from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination

from .models import Project
from .serializers import ProjectSerializer


class ProjectsListView(ListAPIView):
    queryset = Project.objects.all().order_by("-created_at")
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
