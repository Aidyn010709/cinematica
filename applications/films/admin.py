from django.contrib import admin
from applications.films.models import Film


@admin.register(Film)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'like_count']
    list_filter = ['owner__email']
    search_fields = ['title']

    def like_count(self, obj):
        return obj.likes.filter(is_like=True).count()