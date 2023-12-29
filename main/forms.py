from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group as AGroup

from .models import Teacher, Student, RecordBook, Discipline, CompletedDisciplines, Group, Syllabus
from random import randint
class StudentForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = ['name', 'group', 'password']
    def save(self, commit=True):
        student = super().save(commit=False)
        student.user = User.objects.create_user(
            username=f'student_{student.name}',
            password=self.cleaned_data['password'])
        if commit:
            student.save()
            student_group, created= AGroup.objects.get_or_create(name='students group')
            student.user.groups.add(student_group)
        return student
class UpdateStudentForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = ['name']
class TeacherForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = Teacher
        fields = ['name']
    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.user = User.objects.create_user(
            username=f'teacher_{teacher.name}',
            password=self.cleaned_data['password'])
        if commit:
            teacher.save()
            teacher_group, created= AGroup.objects.get_or_create(name='teacher group')
            teacher.user.groups.add(teacher_group)
        return teacher
class RecordBookForm(forms.ModelForm):
    class Meta:
        model = RecordBook
        fields = ['number']
class DisciplineForm(forms.ModelForm):
    types = ['Зачет', 'Диф. Зачет', 'Экзамен', 'Практика']
    type_of_assesment = forms.ChoiceField(choices=[(type, type) for type in types])
    class Meta:
        model = Discipline
        fields = '__all__'
class SyllbusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = '__all__'
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
class CompletedDisciplinesForm(forms.ModelForm):
    CHOICES = [('Зачет', 'Зачет')] + [(str(mark), str(mark)) for mark in range(3, 6)]
    mark = forms.ChoiceField(choices=CHOICES, required=True)
    class Meta:
        model = CompletedDisciplines
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        discipline = cleaned_data.get('discipline')
        mark = cleaned_data.get('mark')
        if discipline.type_of_assesment in ['Диф. Зачет', 'Экзамен', 'Практика'] and mark == 'Зачет'  or discipline.type_of_assesment == 'Зачет' and mark != 'Зачет':
            raise forms.ValidationError('Неверная оценка для данного типа оценивания')
        return cleaned_data
class LoginUserForm(AuthenticationForm):
    username=forms.CharField(label='Login',widget=forms.TextInput(attrs={'class':'form-input'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-input'}))