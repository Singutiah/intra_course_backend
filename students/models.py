from django.db import models
from django.contrib.auth.models import User

import sys
sys.path.append("..")

from chatbot.models import Responses
from courses.models import Course

class Student(models.Model):
    # student
    reg_no = models.CharField(max_length=255, null=False)
    firstname = models.CharField(max_length=255, null=False)
    middlename = models.CharField(max_length=255, null=False)
    lastname = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


    def __str__(self):
        return "{} - {}".format(self.firstname, self.middlename)



class StudentCourse(models.Model):
    # subject
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


    def __str__(self):
        return "{} - {}".format(self.course, self.user)




