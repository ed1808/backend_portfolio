from django.urls import path

from .views import ProjectsListView, ProjectDetailView

urlpatterns = [
    path("projects/", ProjectsListView.as_view(), name="projects"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project"),
]
