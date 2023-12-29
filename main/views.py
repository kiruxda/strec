from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Teacher, Group, Student, Discipline, CompletedDisciplines, Syllabus
from .forms import LoginUserForm, RecordBookForm, StudentForm,DisciplineForm, CompletedDisciplinesForm, TeacherForm, GroupForm, SyllbusForm, UpdateStudentForm
from .resources import StudentResource
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='teacher group').exists() or self.request.user.is_superuser
class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.user.groups.filter(name='students group').exists() or self.request.user.is_superuser
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
def index(request):
    data={
        'title':'main page'
    }
    return render(request, 'main/index.html', data)
class LoginUser(LoginView):
    form_class=LoginUserForm
    template_name='main/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
def logout_user(request):
    logout(request)
    return redirect('home')
class AllTeachers(LoginRequiredMixin,ListView):
    model=Teacher
    template_name='main/teachers.html'
    context_object_name='teachers'
    extra_context={
        'title':'teachers page',
        'content':'teachers'
        }
    login_url='login'
class TeacherCreate(AdminRequiredMixin,CreateView):
    model=Teacher
    form_class = TeacherForm
    template_name = 'main/add.html' 
class OneTeacher(LoginRequiredMixin,DetailView):
    model=Teacher
    template_name='main/teacher.html'
    pk_url_kwarg='teacher_id'
    context_object_name='teacher'
    login_url='login'
class AllStudents(LoginRequiredMixin,ListView):
    model=Student
    template_name='main/students.html'
    context_object_name='students'
    extra_context={
        'title':'students page',
        'content':'students'
        }
    login_url='login'
class OneStudent(LoginRequiredMixin,DetailView):
    model=Student
    template_name='main/student.html'
    pk_url_kwarg='student_id'
    context_object_name='student'
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get(self.pk_url_kwarg)
        student = Student.objects.get(pk=student_id)
        if request.user == student.user or request.user.groups.filter(name='teacher group').exists() or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('student_id')
        student = Student.objects.get(pk=student_id)
        syllabus_disciplines = Discipline.objects.filter(
            syllabus__group=student.group
        )
        completed_disciplines = Discipline.objects.filter(
            completeddisciplines__recordbook__student=student,
        )
        debts = syllabus_disciplines.exclude(
            pk__in=completed_disciplines.values_list('pk', flat=True)
        )
        context['debts'] = debts
        return context
    login_url='login'
class StudentCreate(AdminRequiredMixin,CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'main/addstudent.html'
    success_url = reverse_lazy('students') 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'recordbook_form' not in context:
            context['recordbook_form'] = RecordBookForm()
        return context
    def form_valid(self, form):
        self.object = form.save()
        recordbook_form = RecordBookForm(self.request.POST)
        if recordbook_form.is_valid():
            record_book = recordbook_form.save(commit=False)
            record_book.student = self.object
            record_book.save()
        return redirect(self.get_success_url())
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        recordbook_form = RecordBookForm(request.POST)
        if form.is_valid() and recordbook_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_invalid(self, form):
        recordbook_form = RecordBookForm(self.request.POST)
        return self.render_to_response(self.get_context_data(form=form, recordbook_form=recordbook_form))
    redirect_field_name='home'
class DisciplineCreate(AdminRequiredMixin,CreateView):
    model=Discipline
    form_class = DisciplineForm
    template_name = 'main/add.html' 
class AddCompletedDiscipline(TeacherRequiredMixin, CreateView):
    model = CompletedDisciplines
    form_class = CompletedDisciplinesForm
    template_name = 'main/add.html'
    def form_valid(self, form):
        student = Student.objects.get(pk=self.kwargs['student_id'])
        discipline_to_add = form.cleaned_data['discipline']
        syllabuses = Syllabus.objects.filter(group=student.group)
        if not syllabuses.filter(course__lte=student.group.course, discipline=discipline_to_add).exists():
            form.add_error('discipline', 'Дисциплина не соответствует расписанию и курсу студента.')
            return self.form_invalid(form)
        self.object = form.save()
        student.recordbook.completed_disciplines.add(self.object)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('students')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.get(pk=self.kwargs['student_id'])
        return context
class UpdateStudent(AdminRequiredMixin,UpdateView):
    model=Student
    form_class=UpdateStudentForm
    template_name='main/add.html'
    pk_url_kwarg='student_id'
class DeleteStudent(AdminRequiredMixin,DeleteView):
    model=Student
    template_name='main/delete.html'
    pk_url_kwarg='student_id'
    success_url=reverse_lazy('students')
class DeleteTeacher(AdminRequiredMixin,DeleteView):
    model=Teacher
    template_name='main/delete.html'
    pk_url_kwarg='teacher_id'
    success_url=reverse_lazy('teachers')
class AllGroups(LoginRequiredMixin,ListView):
    model=Group
    template_name='main/groups.html'
    context_object_name='groups'
    extra_context={
        'title':'groups page',
        'content':'groups'
        }
    login_url='login'
class OneGroup(LoginRequiredMixin,DetailView):
    model=Group
    template_name='main/group.html'
    pk_url_kwarg='group_id'
    context_object_name='group'
    login_url='login'
class GroupCreate(AdminRequiredMixin,CreateView):
    model=Group
    form_class = GroupForm
    template_name = 'main/add.html' 
class SyllbusCreate(AdminRequiredMixin,CreateView):
    model=Syllabus
    form_class = SyllbusForm
    template_name = 'main/add.html' 
def export_data(request, format):
    student_resource = StudentResource()
    dataset = student_resource.export()
    if format=='CSV':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
        return response
    elif format=='JSON':
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
        return response