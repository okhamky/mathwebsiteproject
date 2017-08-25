from django.contrib import admin
from .models import Teacher, Student, Chapter, Book, PaceChapter
# Register your models here.

admin.site.register(Teacher)


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0

class BookAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]


admin.site.register(Book, BookAdmin)


class PaceChapterInline(admin.TabularInline):
    model = PaceChapter
    extra = 0

class StudentAdmin(admin.ModelAdmin):
    inlines = [PaceChapterInline]

admin.site.register(Student, StudentAdmin)