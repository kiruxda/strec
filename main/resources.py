from import_export import resources
from .models import Teacher, Syllabus, Group, Student, RecordBook, Discipline, CompletedDisciplines

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
class SyllabusResource(resources.ModelResource):
    class Meta:
        model = Syllabus
class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
class RecordBookResource(resources.ModelResource):
    class Meta:
        model = RecordBook
class DisciplineResource(resources.ModelResource):
    class Meta:
        model = Discipline
class CompletedDisciplinesResource(resources.ModelResource):
    class Meta:
        model = CompletedDisciplines
