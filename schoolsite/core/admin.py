from django.contrib import admin
from .models import Course, MediaItem, Comment, Like, ContactInfo

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','created_at')
    search_fields = ('title',)

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('id','type','event_name','date','created_at')
    list_filter = ('type','date')
    search_fields = ('event_name','description')

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(ContactInfo)
