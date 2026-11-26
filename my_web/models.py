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


