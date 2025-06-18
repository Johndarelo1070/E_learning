from django.test import TestCase,Client
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Student, Course, Lesson, Enrollment, LessonProgress

class LessonProgressTests(TestCase):
        def setUp(self):
                self.user = User.objects.create_user(username='student1', password='pass')
                self.student = Student.objects.create(user=self.user)
                self.course = Course.objects.create(title='Test Course')
                self.lesson1 = Lesson.objects.create(course=self.course, title='Lesson 1', content='...')
                self.lesson2 = Lesson.objects.create(course=self.course, title='Lesson 2', content='...')
                Enrollment.objects.create(student=self.student, course=self.course)
                self.client = Client()
                self.client.login(username='student1', password='pass')
        def test_mark_lesson_complete(self):
                response = self.client.post(f'/ajax/complete-lesson/{self.lesson1.id}/')
                self.assertEqual(response.status_code, 200)
                self.assertTrue(LessonProgress.objects.filter(student=self.student, lesson=self.lesson1, completed=True).exists())

        def test_dashboard_progress(self):
                LessonProgress.objects.create(student=self.student, lesson=self.lesson1, completed=True)
                response = self.client.get('/student_dashboard-page/') 
                self.assertContains(response, '50%')

        # Create your tests here.
