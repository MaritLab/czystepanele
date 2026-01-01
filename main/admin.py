from django.contrib import admin
from .models import (
    Category,
    Project,
    ProjectImage,
    Client,
    BlogCategory,
    BlogPost,
    BlogImage,
)

# ============================================================
# REALIZACJE
# ============================================================

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date")
    inlines = [ProjectImageInline]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)


# ============================================================
# KLIENCI
# ============================================================

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
    ordering = ("-created",)


# ============================================================
# BLOG
# ============================================================

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published")
    list_filter = ("category", "published")
    search_fields = ("title", "intro", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlogImageInline]
    date_hierarchy = "published"


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
