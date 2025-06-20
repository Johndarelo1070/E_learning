from django.urls import path
from .views import homepage,aboutpage,contactpage,signupview,loginview,custom_logout,lesson_detail,student_dashboard,course_detail, course_list,enroll_course_view,unfinished_lessons_view, take_lesson_view


urlpatterns = [
    path('',homepage,name='homepage'),
    path('about/',aboutpage,name='vflox-about-page'),
    path('signup/',signupview, name='vflox-signup-page'),
    path('login/',loginview,name='vflox-login-page'),
    path('logout/',custom_logout,name='logout'),
    path('lesson/',lesson_detail,name='vflox-lesson-page'),
    path('Contact/',contactpage,name='vflox-contact-page'),
    # path('dashboard',student_dashboard,name='vflox--page'),
    path('dashboard',student_dashboard,name='vflox-student_dashboard-page'),
    path('course/',course_detail,name='vflox-course-detail-page'),

    # path('courses/<int:pk>/', course_list_view, name='course_list-page'),
    
    path('courses/', course_list, name='course_list-page'),
    path('courses/enroll/<int:course_id>/', enroll_course_view, name='enroll_course-page'),
    path('lessons/unfinished/', unfinished_lessons_view, name='unfinished_lessons-page'),
    path('lessons/<int:lesson_id>/', take_lesson_view, name='take_lesson-page'),
]


