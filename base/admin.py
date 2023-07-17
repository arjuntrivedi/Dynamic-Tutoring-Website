from django.contrib import admin

from .models import Course, Student, Tutor, CourseTutored, Notification, TimeFrame
#from .models import Profile

# Register your models here.

models = [Course, Student, Tutor, CourseTutored, Notification, TimeFrame]
admin.site.register(models)