from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from random import randint
import datetime
class Teacher(models.Model):
    name = models.CharField('ФИО преподавателя', max_length=100) #varchar(100) NOT NULLL
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('teacher',kwargs={'teacher_id':self.id})
    def delete(self):
        self.user.delete() 
        return reverse('home')
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
class Syllabus(models.Model):
    course = models.IntegerField('Расписание на курс', default=1)
    set_date = models.DateField('Дата утверждения', default=datetime.date.today())
    discipline=models.ManyToManyField('Discipline')
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
class Group(models.Model):
    name = models.CharField('Название группы', max_length=100, unique=True) #varchar(100) not null unique
    syllabus = models.ManyToManyField('Syllabus') #references syllabus
    course = models.IntegerField('Номер курса',default=1)#int not null default(1)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    def get_absolute_url(self):
        return reverse_lazy('groups')
class Student(models.Model):
    name = models.CharField('ФИО студента', max_length=100) #varchar(100) not null
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE) #references study_group
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('students')
    def delete(self):
        self.user.delete() 
        return reverse('home')
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
class RecordBook(models.Model):
    number = models.PositiveBigIntegerField('Номер зачетной книжки')
    student = models.OneToOneField('Student', on_delete=models.CASCADE, primary_key=True) #references student
    completed_disciplines=models.ManyToManyField('CompletedDisciplines')
    class Meta:
        verbose_name = 'Зачетная книжка'
        verbose_name_plural = 'Зачетные книжки'
class Discipline(models.Model):
    name = models.CharField('Название дисциплины', max_length=100) #varchar(100) not null
    teacher=models.ManyToManyField('Teacher')
    type_of_assesment=models.CharField('Вид оценивания', max_length=50, default='Зачет')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
    def get_absolute_url(self):
        return reverse_lazy('home')
class CompletedDisciplines(models.Model):
    hours = models.IntegerField('Количество часов', default=100)#int not null
    mark = models.CharField('Оценка', max_length=10, default='Зачет')
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE) #references discipline
    class Meta:
        verbose_name = 'Завершенная дисциплина'
        verbose_name_plural = 'Завершенные дисциплины'