from django.contrib import admin
from .models import Member
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','username','grade', 'num_solved', 'score', 'target']
    list_per_page = 15
    search_fields = ['full_name', 'username']
    list_editable = ['target']
    sortable_by = ['target', 'score']
admin.site.register(Member, MemberAdmin)