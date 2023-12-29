from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Teacher, Student, Syllabus, Group, RecordBook, Discipline, CompletedDisciplines
#from import_export.admin import ImportExportModelAdmin
#class TeacherAdmin(ImportExportModelAdmin,admin.ModelAdmin):

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Syllabus)
admin.site.register(Group)
admin.site.register(RecordBook)
admin.site.register(Discipline)
admin.site.register(CompletedDisciplines)
