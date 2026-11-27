from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class CustomUser(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.username





class UserProfile(models.Model):
    ROLE = [("student", "Student"),("mentor", "Mentor")]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE, default="student")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username






class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Course categories"







class Course(models.Model):
    LEVEL = [
        ("beginner", "Beginner"),
        ("middle", "Middle"),
        ("advanced", "Advanced"),
        ]
    title = models.CharField(max_length=200)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name="courses")
    mentor = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name="mentor_courses")
    students = models.ManyToManyField(CustomUser, related_name="joined_courses", blank=True)
    description = models.TextField()
    
    photo = models.ImageField(upload_to="courses")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    level = models.CharField(max_length=20, choices=LEVEL, default="beginner")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]





class CourseLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    day = models.PositiveIntegerField(default=1)
    content = models.TextField(blank=True)
    youtube_url = models.URLField(blank=True,verbose_name="YouTube video URL")
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["day"]





class CourseComment(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-created_at"]








class EmailConfirmCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="email_codes")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username









class LessonProgress(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="lesson_progress")
    lesson = models.ForeignKey(CourseLesson,on_delete=models.CASCADE,related_name="progress")
    is_completed = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [ models.UniqueConstraint(fields=["user", "lesson"],name="unique_user_lesson_progress")]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"







class LessonQuestion(models.Model):
    lesson = models.ForeignKey(CourseLesson,on_delete=models.CASCADE,related_name="questions")
    question = models.TextField()
    correct_answer = models.CharField(max_length=500)
    points = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.lesson.title} - Question {self.order}"

    class Meta:
        ordering = ["order"]





class QuestionProgress(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="question_progress")
    question = models.ForeignKey(LessonQuestion,on_delete=models.CASCADE,related_name="answers")
    points_earned = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "question"],name="unique_user_lesson_question")]

    def __str__(self):
        return f"{self.user.username} - {self.question}"
