from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "header",
        "description",
        "views_count",
        "created_at",
    )
    search_fields = (
        "header",
        "description",
    )
