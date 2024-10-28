from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ["name", "email", "created_at"]


admin.site.register(Contact, ContactAdmin)
