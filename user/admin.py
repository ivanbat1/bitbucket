from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(General)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GeneralR._meta.fields]
    class Meta:
        model = GeneralR

admin.site.register(GeneralR, ProductCategoryAdmin)