from copy import error
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpRequest
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from datetime import datetime
from .models import  Enrollment, Lesson,Course, Student,LessonProgress
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def homepage(request):
    return render(request, "user/home.html", {'year': datetime.now().year})
def aboutpage(request):
    return HttpResponse("<h2 align='center' style='color:green;>' ABOUT<h2/>")
def contactpage(request):
    return HttpResponse("<h2 align='center' style='color:green;>' CONTACT VFLOX </h2>")

def signupview(request:HttpRequest):
    if request.method == "POST":
        email=request.POST.get("email")
        username=request.POST.get("username")
        password1=request.POST.get("password")
        password2=request.POST.get("password1")
        if password1 != password2 or len (password1)<8:
            return render(request,"auth/signup.html",{"error":"password do not match or len of password is < 8"})
        if not username :
            return render(request,"auth/signup.html",{"error":"username required"})
        user_found = User.objects.filter(username = username)
        if user_found :
            return render(request,"auth/signup.html",{"error":"User with the given username already exist"})
        # user = User(username=username , email=email, password = password1)
        # user.save()
        user = User.objects.create_user(username=username,email=email, password=password1)
        Student.objects.create(user=user)
        print('User Saved and converted to a student ')
        return redirect("vflox-login-page")
    
    print("Get request for signup called upon")   
    return render(request,"auth/signup.html",{"error":None})
        
# def loginview(request: HttpRequest):
#     if  request.method=="POST":
#         username=request.POST.get("username")
#         pass1=request.POST.get("pass1")

def loginview(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        #validate input
        print(username,pass1) 
        if not username or not pass1:
            return render(request,"auth/login.html",{"error":"Both username and password are required.","success":""})
        try:
            User=authenticate(request, username=username, password=pass1)
            if User==None:
                return render(request,"auth/login.html",{"error":"Not a valid user."})
            
            login(request,User)
            return redirect('vflox-student_dashboard-page')
        except:
            return render (request,"auth/login.html",{"error":"Error occured.... Username or password required."})
    return render(request,"auth/login.html",{"error":"","success":""})
            

        # user = authenticate(request, username=username, pass1=pass1)

        # if user == None:
        #     login(request, user)
        #     try:
        #         profile = User.objects.get(user=user)
        #         if profile.role == 'instructor':
        #             return redirect('instructor_dashboard-page')
        #         elif profile.role == 'student':
        #             return redirect('student_dashboard-page')
        #         else:
        #             return redirect('homepage')
        #     except User.DoesNotExist:
        #         messages.error(request, "No profile found for this user.")
        #         return redirect('user/home.html')
        # else:
        #     messages.error(request, "Invalid username or password.")
    
        # return render(request,'user/login.html')

        
    # try:
    #     User = authenticate(request,username=username,password=pass1)
    #     if instructor_dashboard.role == 'instructor':
    #         return redirect(' user/instructor_dashboard.html')
    #     elif User.role == 'student':
    #         return redirect(' /user/student_dashboard.html')
    #     # else:
    #     #     return redirect('/vlfox/')
    # except:
    #     return render(request,"auth/login.html",{'error':"server Error","success":None})
    # return redirect('/vflox/')
    #     try:
    #         user = authenticate(request,username=username,password=pass1)
    #         if user == None:
    #             return render(request,"auth/login.html",{'error':"not a valid user"})
    #         login(request, user)
    #         return redirect("/vflox/homepage")
    #     except:
    #         return render(request,"auth/login.html",{'error':"server Error","success":None})
    # return render(request,"auth/login.html",{})

def custom_logout(request):
    logout(request)
    return redirect('homepage')

# def lesson_detail(request, slug):
#     lesson =get_object_or_404(Lesson, slug=slug)
#     previous_lesson = lesson.get_previous()
#     next_lesson = lesson.get_next()
#     return render(request, 'lesson_detail.html', {
#         'lesson': lesson,
#         'previous_lesson': previous_lesson,
#         'next_lesson': next_lesson,
#     })
    
# @login_required
# def student_dashboard(request):
#     # student = User= request.user
#     student=Student.objects.get(user=request.user)
#     enrollments = Enrollment.objects.filter(student=student).select_related('course').prefetch_related('course__lessons')
#     User.save()

#     data = []
#     next_lesson = None

#     for enrollment in enrollments:
#         course = enrollment.course
#         total = course.lessons.count()
#         completed = LessonProgress.objects.filter(student=student, lesson__course=course, completed=True).count()
#         percent = int((completed / total) * 100) if total > 0 else 0

#         # Find first unfinished lesson if not already found
#         if not next_lesson:
#             for lesson in course.lessons.all():
#                 if not LessonProgress.objects.filter(student=student, lesson=lesson, completed=True).exists():
#                     next_lesson = lesson
#                     break

#         data.append({
#             'enrollment': enrollment,
#             'total_lessons': total,
#             'completed_lessons': completed,
#             'progress_percent': percent,
#         })

#     return render(request, 'user/student_dashboard.html', {
#         'enrollments_data': data,
#         'next_lesson': next_lesson,
#     })
        
            
    
# # @login_required
@login_required(login_url='vflox-login-page')
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    courses = Course.objects.all()

    progress_data = []
    for course in courses:
        lessons = course.lessons.all()
        completed_lessons = LessonProgress.objects.filter(student=student, lesson__in=lessons, completed=True)
        unfinished_lessons = lessons.exclude(id__in=completed_lessons.values_list('lesson_id', flat=True))
        progress = calculate_progress(student, course)
        progress_data.append({
            'course': course,
            'progress': progress,
            'unfinished_lessons': unfinished_lessons,
        })

    return render(request, 'user/student_dashboard.html', {'progress_data': progress_data})

@login_required(login_url='vflox-login-page')
def calculate_progress(student, course):
    lessons = course.lessons.all()
    completed = LessonProgress.objects.filter(student=student, lesson__in=lessons, completed=True).count()
    total = lessons.count()
    if total == 0:
        return 0
    return int((completed / total) * 100)



# @login_required
# def student_dashboard(request):
#     student = get_object_or_404(Student, user=request.user)
#     enrollments = Enrollment.objects.filter(student=student).select_related('course')
#     return render(request, 'user/student_dashboard.html', {
#         'enrollments': enrollments
#     })

# @login_required
# def instructor_dashboard(request):
#     courses = Course.objects.filter(instructor=request.user)
#     return render(request, 'instructor_dashboard.html', {
#         'courses': courses
#     })

@login_required(login_url='vflox-login-page')
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'user/course_detail.html', {'course': course})

@login_required(login_url='vflox-login-page')
def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    return render(request, 'user/lesson_detail.html', {'lesson': lesson})

# def course_list_view(request):
#     courses = Course.objects.all()
#     return render(request, 'courses/course_list.html', {'courses': courses})

@login_required(login_url='vflox-login-page')
def course_list(request):
    student = get_object_or_404(Student, user=request.user)
    courses = Course.objects.filter.all()
    enrolled_course_ids = student.enrollments.values_list('course_id', flat=True)
    return render(request, 'user/course_list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_course_ids
    })

@login_required(login_url='vflox-login-page')
def enroll_course_view(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    # Check if already enrolled
    if not Enrollment.objects.get(student=student, course=course).exists():
        Enrollment.objects.create(student=student, course=course)
    return redirect('course_list-page')



    return redirect('student_dashboard-page')

# @login_required
# def enroll_course(request, course_id):
#     student, created = Student.objects.get_or_create(user=request.user)
#     course = get_object_or_404(Course, id=course_id)
#     student.enrolled_courses.add(course)
#     return redirect('student_dashboard')

@login_required(login_url='vflox-login-page')
def take_lesson_view(request, lesson_id):
    student = request.user.student
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        # Mark lesson as completed
        progress,create = LessonProgress.objects.get_or_create(student=student, lesson=lesson)
        progress.completed = True
        progress.completed_on = timezone.now()
        progress.save()
        return redirect('unfinished_lessons-page')  # or dashboard

    return render(request, 'user/take_lesson.html', {
        'lesson': lesson
    })
    
@login_required(login_url='vflox-login-page')
def unfinished_lessons_view(request):
    student = request.user.student  # Assumes custom Student model is linked
    enrollments = Enrollment.objects.filter(student=student)

    unfinished = []

    for enrollment in enrollments:
        course = enrollment.course
        lessons = course.lessons.all()
        for lesson in lessons:
            progress = LessonProgress.objects.filter(student=student, lesson=lesson).first()
            if not progress or not progress.completed:
                unfinished.append(lesson)

    return render(request, 'user/unfinished_lessons.html', {'unfinished_lessons':unfinished})



