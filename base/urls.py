from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.registerPage, name = "register"),

    path('student-home', views.studentHome, name='student-home'),
    path('student-course-lookup', views.studentCourseLookup, name='student-course-lookup'),
    path('student-request-tutor', views.studentTutorSearch, name='student-request-tutor'),
    path('student-submit-request', views.studentSubmitRequest, name='student-submit-request'),
    path('student-notification', views.studentNotification, name='student-notification'),

    path('tutor-home', views.tutorHome, name = 'tutor-home'),
    path('tutor-course-lookup', views.tutorCourseLookup, name='tutor-course-lookup'),
    path('tutor-post-rate', views.tutorPostRate, name='post-rate'),
    path('tutor-view-rate', views.tutorViewRate, name='view-rate'),
    path('tutor-view-courses', views.tutorViewCourses, name='tutor-view-courses'),
    path('tutor-notification', views.tutorNotification, name='tutor-notification'),
    path('tutor-post-timeframe', views.tutorPostTimeFrame, name='tutor-post-timeframe'),
    path('tutor-view-timeframes', views.tutorViewTimeFrames, name='tutor-view-timeframes'),


]