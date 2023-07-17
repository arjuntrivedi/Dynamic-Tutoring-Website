from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login as logins, logout as logouts

from .models import Student, Tutor, Course, CourseTutored, Notification, TimeFrame

from .forms import TutorPostCourseForm, TutorLookupForm, TutorPostRateForm, TutorRemoveCourseForm, StudentRequestTutorForm, TutorNotificationForm, StudentNotificationForm, TutorPostTimeFrameForm, StudentTimeFrameForm
from django.views.generic import ListView
from django.db.models import Q

from .decorators import allowed_users


def index(request):
    return render(request, 'base/index.html')


def is_student(user):
    return user.groups.filter(name='student').exists()


def is_tutor(user):
    return user.groups.filter(name='tutor').exists()


# -------------------------------------------------------

def loginPage(request):
    if request.user.is_active:
        if not is_student(request.user) and not is_tutor(
                request.user):  # if the logged in user is not a tutor or student, make them register to be one
            return registerPage(request)
        if is_student(request.user):
            return studentHome(request)
        if is_tutor(request.user):
            return tutorHome(request)
    return render(request, 'base/general_login.html')  # Puts person at the page where they can be recorded as a "user"


def logout(request):
    if request.method == "POST":
        logouts(request)
        return render(request, 'base/index.html')
    return render(request, 'base/general_logout.html')


def registerPage(request):
    if (request.GET.get('student')):  # add student group attribute
        group = Group.objects.get(name='student')
        request.user.groups.add(group)
        group = Group.objects.get(name='tutor')
        request.user.groups.remove(group)
        return register_student(request)
    elif (request.GET.get('tutor')):  # add tutor group attribute
        group = Group.objects.get(name='tutor')
        request.user.groups.add(group)
        group = Group.objects.get(name='student')
        request.user.groups.remove(group)
        return register_tutor(request)
    else:
        return render(request, 'base/register.html')


# -------------------------------------------------

# Creates student object if needed
def register_student(request):
    user_name = request.user.username
    s = Student(username=user_name)
    if not Student.objects.filter(username=user_name).exists():
        s.save()
    return render(request, 'base/student_home.html')


# Creates tutor object if needed
def register_tutor(request):
    user_name = request.user.username
    t = Tutor(username=user_name)
    if not Tutor.objects.filter(username=user_name).exists():
        t.save()
    return render(request, 'base/tutor_home.html')


# ------------------------------------------------

# Only lets users with "student" group access page
@allowed_users(allowed_roles=['student'])
def studentHome(request):
    return render(request, 'base/student_home.html')

@allowed_users(allowed_roles=['student'])
def studentCourseLookup(request):
    if request.method == "GET":
        query = request.GET.get("q")
        object_list = Course.objects.filter(
            Q(department=query) | Q(number = query) | Q(name = query)
        )
        return render(request, 'base/student_search_course.html', {'object_list': object_list})
    if request.method == "POST":
        form = TutorLookupForm(request.POST)
        if form.is_valid():
            department = str(form.cleaned_data['department'])  # first find the right course
            number = str(form.cleaned_data['number'])
            name = str(form.cleaned_data['name'])
            if Course.objects.filter(department=department, number=number, name=name).exists():  # Ensures that an incorrect course is not posted
                c = Course.objects.get(department=department, number=number, name=name)

                request.session['department'] = department
                request.session['number'] = number
                request.session['name'] = name
                request.session['tutors'] = list(c.course_all_tutors.values()) # store tutor search in user session
                return redirect('base:student-request-tutor')
    form = TutorLookupForm()
    return render(request, 'base/student_search_course.html', {'form': form})

@allowed_users(allowed_roles=['student'])
def studentTutorSearch(request):
    course = Course.objects.get(department=request.session['department'], number=request.session['number'], name=request.session['name'])
    if request.method == "POST":
        form = StudentRequestTutorForm(request.POST)
        if form.is_valid():
            tutor = str(form.cleaned_data['tutor'])
            request.session['tutor'] = tutor
            return redirect('base:student-submit-request')
    form = StudentRequestTutorForm(request.POST)

    print((request.session['tutors']))

    return render(request, 'base/student_tutors_available.html', {'form': form, 'course': course, 'tutors': request.session['tutors']})

@allowed_users(allowed_roles=['student'])
def studentSubmitRequest(request):
    course = Course.objects.get(department=request.session['department'], number=request.session['number'], name=request.session['name'])
    student = Student.objects.get(username=request.user.username)
    tutor = Tutor.objects.get(username=request.session['tutor'])
    info = "0"
    tutor_timeframes = TimeFrame.objects.filter(tutor = tutor)

    if request.method == "POST":
        request_form = StudentRequestTutorForm(request.POST)
        time_form = StudentTimeFrameForm(request.POST)

        if time_form.is_valid():
            print("time form valid")
            student_chosen_start_time = (time_form.cleaned_data['start_time'])
            student_chosen_end_time = (time_form.cleaned_data['end_time'])
            #User submits time
        
            #Need to go through all time frames to ensure this is a valid time
            for timeframe in tutor_timeframes:
                this_endTime = timeframe.end_time
                this_startTime = timeframe.start_time
                if student_chosen_start_time >= this_startTime and student_chosen_end_time <= this_endTime and student_chosen_start_time < student_chosen_end_time:
                    if not Notification.objects.filter(info=info, course=course, student=student,tutor=tutor).exists():
                        Notification(info=info, course=course, student=student,tutor=tutor).save()
                        return redirect('base:student-notification')

    request_form = StudentRequestTutorForm(request.POST)
    time_form = StudentTimeFrameForm(request.POST)


    return render(request, 'base/student_submit_request.html', {'form': request_form, 'time_form': time_form, 'course': course, 'student': student, 'tutor': tutor , 'tutor_timeframes': tutor_timeframes})

@allowed_users(allowed_roles=['student'])
def studentNotification(request):
    student = Student.objects.get(username=request.user.username)
    notifications = Notification.objects.filter(student=student)

    if request.method == "POST":
        form = StudentNotificationForm(request.POST)
        if form.is_valid():
            info = str(form.cleaned_data['info'])
            tutor = Tutor.objects.get(username=str(form.cleaned_data['tutor']))
            course = str(form.cleaned_data['course'])
            Notification.objects.get(info=info, course=course, student=student,tutor=tutor).delete()
            return redirect('base:student-notification')
    form = StudentNotificationForm()
    return render(request, 'base/student_notification.html', {'form': form, 'notifications': notifications})

# -----------------------------------------------

# Only lets users with "tutor" group access page
@allowed_users(allowed_roles=['tutor'])
def tutorHome(request):
    return render(request, 'base/tutor_home.html')

@allowed_users(allowed_roles=['tutor'])
def tutorCourseLookup(request):
    if request.method == "GET":
        query = request.GET.get("q")
        object_list = Course.objects.filter(
            Q(department=query) | Q(number = query) | Q(name = query)
        )
        return render(request, 'base/tutor_search_course.html', {'object_list': object_list})
    if request.method == "POST":
        form = TutorPostCourseForm(request.POST)
        if form.is_valid():
            t = Tutor.objects.get(username=request.user.username)  # find the right tutor model
            department = str(form.cleaned_data['department'])
            number = str(form.cleaned_data['number'])
            name = str(form.cleaned_data['name'])
            if Course.objects.filter(department=department, number=number, name=name).exists():  # Ensures that an incorrect course is not posted
                c = Course.objects.get(department=department, number=number, name=name)
                if not CourseTutored.objects.filter(tutor=t, course=c).exists():  # Ensures that we don't add duplicate Course-Tutor relationship
                    CourseTutored(tutor=t, course=c).save()  # adds course to tutor object and adds tutor to course object
                return redirect('base:tutor-view-courses')
    form = TutorPostCourseForm()
    return render(request, 'base/tutor_search_course.html', {'form': form})

# View courses function
@allowed_users(allowed_roles=['tutor'])
def tutorViewCourses(request):
    t = Tutor.objects.get(username=request.user.username)
    if request.method == "POST":
        form = TutorRemoveCourseForm(request.POST)
        if form.is_valid():
            t = Tutor.objects.get(username=request.user.username)  # find the right tutor model
            department = str(form.cleaned_data['department'])
            number = str(form.cleaned_data['number'])
            name = str(form.cleaned_data['name'])
            if Course.objects.filter(department=department, number=number, name=name).exists():  # Ensures that an incorrect course is not posted
                c = Course.objects.get(department=department, number=number, name=name)
                CourseTutored.objects.filter(tutor=t, course=c).delete()
                return redirect('base:tutor-view-courses')
    form = TutorRemoveCourseForm()
    return render(request, 'base/tutor_view_courses.html', {'form': form, 'tutor_courses': t.tutor_all_courses.values()})

# Hourly rate functions
@allowed_users(allowed_roles=['tutor'])
def tutorPostRate(request):
    if request.method == "POST":
        form = TutorPostRateForm(request.POST)
        if form.is_valid():
            t = Tutor.objects.get(username=request.user.username)  # find the right tutor model
            hr = str(form.cleaned_data['rate'])
            t.hourly_rate = hr
            t.save()
            print(hr)
            return tutorViewRate(request)
    form = TutorPostRateForm()
    return render(request, 'base/tutor_post_rate.html', {'form': form})


@allowed_users(allowed_roles=['tutor'])
def tutorViewRate(request):
    t = Tutor.objects.get(username=request.user.username)  # find the right tutor model

    return render(request, 'base/tutor_view_rate.html', {'rate': t.hourly_rate})


@allowed_users(allowed_roles=['tutor'])
def tutorNotification(request):
    tutor = Tutor.objects.get(username=request.user.username)
    notifications = Notification.objects.filter(tutor=tutor)

    if request.method == "POST":
        form = TutorNotificationForm(request.POST)
        if form.is_valid():
            info = str(form.cleaned_data['info'])
            student = Student.objects.get(username=str(form.cleaned_data['student']))
            course = str(form.cleaned_data['course'])
            if not Notification.objects.filter(info=info, course=course, student=student,tutor=tutor).exists():
                Notification(info=info, course=course, student=student,tutor=tutor).save()
            Notification.objects.get(info="0", course=course, student=student,tutor=tutor).delete()
            return redirect('base:tutor-notification')
    form = TutorNotificationForm()
    return render(request, 'base/tutor_notification.html', {'form': form, 'notifications': notifications})

@allowed_users(allowed_roles=['tutor'])
def tutorPostTimeFrame(request):
    if request.method == 'POST':
        form = TutorPostTimeFrameForm(request.POST)
        if form.is_valid():
            new_start = (form.cleaned_data['start_time'])
            new_end = (form.cleaned_data['end_time'])
            #find the tutor who owns this posted time frame
            t = Tutor.objects.get(username = request.user.username)
            print("tutor", t)
            if new_start < new_end:
                #Look for overlapping time frame
                all_timeframes = TimeFrame.objects.filter(tutor = t) #all the time frames for this tutor
                for timeframe in all_timeframes:
                    old_start = timeframe.start_time
                    old_end = timeframe.end_time
                    
                    #i.e: Old: 12PM to 4PM. New input: 1PM to 5PM. Result: update time frame to 12PM to 5PM
                    if new_start >= old_start and new_start <= old_end and new_end >= old_end:
                        timeframe.delete()
                        time_frame = TimeFrame(start_time = old_start, end_time = new_end, tutor = t).save()
                        return tutorViewTimeFrames(request)

                    #i.e: Old: 4AM to 8AM. New input: 3AM to 7AM. Result: update time frame to 3AM to 8AM
                    if new_start <= old_start and new_end <= old_end and new_start <= old_end:
                        timeframe.delete()
                        time_frame = TimeFrame(start_time = new_start, end_time = old_end, tutor = t).save()
                        return tutorViewTimeFrames(request)
                    
                    #i.e: Old: 5AM to 9AM. New input: 3AM to 10AM. Result: 3 AM to 10AM
                    if new_start <= old_start and new_end >= old_end and new_start <= old_end :
                        timeframe.delete()
                        time_frame = TimeFrame(start_time = new_start, end_time = new_end, tutor = t).save()
                        return tutorViewTimeFrames(request)
                    
                    #i.e: Old: 4AM to 9AM. New input: 5AM to 6AM. Result: 4AM to 9AM
                    if new_start >= old_start and new_end <= old_end:
                        return tutorViewTimeFrames(request)
                    
                #Make an entirely separate time frame
                time_frame = TimeFrame(start_time = new_start, end_time = new_end, tutor = t)
                time_frame.save()
                return tutorViewTimeFrames(request)
    form = TutorPostTimeFrameForm()
    return render(request, 'base/tutor_post_timeframe.html', {'form': form})

@allowed_users(allowed_roles=['tutor'])
def tutorViewTimeFrames(request):
    tutor = Tutor.objects.get(username = request.user.username)
    query = TimeFrame.objects.filter(tutor = tutor)

    return render(request, 'base/tutor_view_timeframes.html', {'tutor_timeframes': query})
# -------------------------------------------------------------------------------