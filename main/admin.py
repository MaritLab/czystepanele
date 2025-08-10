from django.contrib import admin
from .models import Category, Project, ProjectImage, Client

# Register your models here.
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    inlines = [ProjectImageInline]

admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    ordering = ['-created']
