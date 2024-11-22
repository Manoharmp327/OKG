from django.contrib import admin
from .models import Course, Subtitle, Video, PDF, Notes
from ckeditor.widgets import CKEditorWidget
from django.db import models

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ('file', 'title')

class PDFInline(admin.TabularInline):
    model = PDF
    extra = 1
    fields = ('file', 'title')

class NotesInline(admin.TabularInline):
    model = Notes
    extra = 1
    fields = ('title', 'content')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

class SubtitleAdmin(admin.ModelAdmin):
    inlines = [VideoInline, PDFInline, NotesInline]
    list_display = ('name', 'course')

class SubtitleInline(admin.StackedInline):
    model = Subtitle
    extra = 1
    show_change_link = True

class CourseAdmin(admin.ModelAdmin):
    inlines = [SubtitleInline]
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Subtitle, SubtitleAdmin)
