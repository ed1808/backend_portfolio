from django.contrib import admin

from .models import Project, Technology


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ["name", "description", "url", "project_status"]
    search_fields = ["name", "url", "project_status"]


class TechnologyAdmin(admin.ModelAdmin):
    model = Technology
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.site_header = "Portfolio API"
admin.site.site_title = "Portfolio API"
