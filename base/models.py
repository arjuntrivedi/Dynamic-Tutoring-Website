from django.conf import settings
from django.db import models
from django.forms import DateInput
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Student(models.Model):
    full_name = models.CharField(max_length = 80)
    username = models.CharField(max_length = 80)

    student_all_tutors = models.ManyToManyField('Tutor', through = 'Notification')

    def __str__(self):
        return self.username
    
class Tutor(models.Model):
    username = models.CharField(max_length = 80)
    hourly_rate = models.CharField(max_length = 40)
    #Represents the list of courses for a particular tutor (courses the tutor has posted)
    tutor_all_courses = models.ManyToManyField('Course', through = 'CourseTutored')
    tutor_all_students = models.ManyToManyField('Student', through = 'Notification')

    def __str__(self):
        return self.username
    
class Course(models.Model):
    department = models.CharField(max_length=8) #Example: 'APMA'
    number = models.CharField(max_length = 8, default = "0000") #Example: '3080'
    name = models.CharField(max_length=200) #Example: 'Linear Algebra'
    #Represents the list of tutors for a particular course (allows students to view tutors for that course)
    course_all_tutors = models.ManyToManyField('Tutor', through = 'CourseTutored')

    def __str__(self):
        return self.department + " " + self.number + " " + self.name

#Django "Through" tables that establishes direct connection between Tutors and Courses
class CourseTutored(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.course) + " tutored by " + str(self.tutor.username)


class Notification(models.Model):
    info = models.CharField(max_length=200, default="0")
    course = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete = models.CASCADE)

    def __str__(self):
        return self.course + " " + self.student.username + " " + self.tutor.username
    
class TimeFrame(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    tutor = models.ForeignKey(Tutor, on_delete = models.CASCADE)

    def __str__(self):
        return self.tutor.username + ":  " + str(self.start_time) + " to " + str(self.end_time)