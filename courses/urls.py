from django.urls import path
from .views import ListCreateCourseView, CourseDetailView,ListCreateCheckNameView

urlpatterns = [
    path('course/', ListCreateCourseView.as_view(), name="Course-list-create"),
    path('check_name/', ListCreateCheckNameView.as_view(), name="checkname-list-view"),
    path('course/<int:pk>/', CourseDetailView.as_view(), name="Course-detail"),
]
