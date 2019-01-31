from django.contrib import admin
from .models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'date']
    list_filter = ['date']
    search_fields = ['title', 'body']
    sortable_by = ['date']
admin.site.register(Post, PostAdmin)