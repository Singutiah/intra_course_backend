from django.db import models

class College(models.Model):
    college_code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.category)


class School(models.Model):
    school_code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=True)
    college = models.ForeignKey(College, related_name='schools', on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.name, self.category)


class Department(models.Model):
    department_code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=True)
    school = models.ForeignKey(School, related_name='departments', on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.name, self.category)


class Course(models.Model):
    course_code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=False)
    years = models.CharField(max_length=255, null=True)
    sem_count = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.name, self.category)
