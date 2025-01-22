from django.urls import path
from .views import ListCreateStudentView, StudentDetailView, StudentCourseDetailView, ListCreateStudentCourseView, StudentCourseDetailView

urlpatterns = [
    path('student/', ListCreateStudentView.as_view(), name="Student-list-create"),
    path('student/<int:pk>/', StudentDetailView.as_view(), name="Student-detail"),


    path('student-course/', ListCreateStudentCourseView.as_view(), name="student-course-list-create"),
    path('student-course/<int:pk>/', StudentCourseDetailView.as_view(), name="student-course-detail"),

]
