from django.urls import path
from . import views, models

urlpatterns=[
    path('',views.index, name='home'),
    path('login/', views.LoginUser.as_view(),name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('students/',views.AllStudents.as_view(),name='students'),
    path('students/export/<format>',views.export_data,name='students_export'),
    path('students/addstudent',views.StudentCreate.as_view(), name='add_student'),
    path('students/<student_id>/update', views.UpdateStudent.as_view(), name='update_student'),
    path('student/<student_id>/add_discipline/', views.AddCompletedDiscipline.as_view(), name='add_completed_discipline'),
    path('students/<student_id>/delete', views.DeleteStudent.as_view(), name='delete_student'),
    path('students/<student_id>',views.OneStudent.as_view(), name='student'),
    path('groups/',views.AllGroups.as_view(), name='groups'),
    path('groups/add_group',views.GroupCreate.as_view(), name='add_group'),
    path('discipline_add/', views.DisciplineCreate.as_view(), name='add_discipline'),
    path('groups/<group_id>',views.OneGroup.as_view(), name='group'),
    path('teachers/',views.AllTeachers.as_view(),name='teachers'),
    path('teachers/addteacher',views.TeacherCreate.as_view(), name='add_teacher'),
    path('teachers/<teacher_id>',views.OneTeacher.as_view(), name='teacher'),
    path('teachers/<teacher_id>/delete', views.DeleteTeacher.as_view(), name='delete_teacher'),
]