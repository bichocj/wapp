from django.contrib import admin
from core.models import (
    Person,
    Browser
)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "dni", "sex")
    ordering = ["name"]


admin.site.register(Person, PersonAdmin)
admin.site.register(Browser)
