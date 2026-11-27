from django.urls import path
from . import  views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("category/<int:pk>/", views.category_courses, name="category_courses"),
    path("course/create/", views.course_create, name="course_create"),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
    path("course/<int:pk>/update/", views.course_update, name="course_update"),
    path("course/<int:pk>/delete/", views.course_delete, name="course_delete"),
    path("course/<int:pk>/join/", views.course_join, name="course_join"),
    path("course/<int:pk>/comment/", views.comment_create, name="comment_create"),
    path("my-courses/", views.my_courses, name="my_courses"),
    path('register/', views.user_registration, name='register'),
    path("confirm-email/", views.confirm_email, name="confirm_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path( "lesson/<int:pk>/", views.lesson_detail, name="lesson_detail"),

]