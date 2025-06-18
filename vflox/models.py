from django.db import models
from django.contrib.auth.models import User

LEVEL_CHOICES = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('professional', 'Professional'),
)

LESSON_CONTENT_TYPE = (
    ('text', 'Text'),
    ('video', 'Video'),
    ('online', 'Online'),
)

# Student Profile model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# Course Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=15, choices=LESSON_CONTENT_TYPE)
    content = models.TextField(blank=True)  # Text content
    video_url = models.URLField(blank=True)  # Video content
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"
    
class LessonProgress(models.Model): 
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, )    
    
    class Meta:
        unique_together = ('student', 'lesson')