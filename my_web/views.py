from random import randint
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import *






def course_list(request):
    search = request.GET.get("search", "")
    courses = (Course.objects.filter(
            Q(title__icontains=search) | 
            Q(mentor__username__icontains=search))
        .select_related("category", "mentor")
        .annotate(students_count=Count("students")) )
    categories = CourseCategory.objects.annotate(courses_count=Count("courses"))
    return render(request, "course_list.html", { "courses": courses, "categories": categories, "search": search,})






def category_courses(request, pk):
    category = get_object_or_404(CourseCategory, pk=pk)
    courses = category.courses.select_related("mentor").annotate(students_count=Count("students"))
    return render(request, "category_courses.html", {"category": category, "courses": courses})







def course_detail(request, pk):
    course = get_object_or_404( Course.objects
    .select_related("category", "mentor")
    .prefetch_related("lessons"), pk=pk, )
    Course.objects.filter(pk=pk)
    comments = course.comments.filter(status="approved").select_related("user")
    students = course.students.aggregate(total=Count("id"))
    return render(request, "course_detail.html", { "course": course, "comments": comments, "students_total": students["total"],})







@login_required
@permission_required("my_web.add_course", raise_exception=True)
def course_create(request):
    if request.method == "POST":
        Course.objects.create(
            title=request.POST["title"],
            category_id=request.POST["category"],
            mentor=request.user,
            description=request.POST["description"],
            price=request.POST["price"],
            level=request.POST["level"],
            photo=request.FILES["photo"],
        )
        messages.success(request, "Course created")
        return redirect("course_list")
    return render(request, "course_form.html", {"categories": CourseCategory.objects.all()})







@login_required
@permission_required("my_web.add_course", raise_exception=True)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, mentor=request.user)
    if request.method == "POST":
        course.title = request.POST["title"]
        course.category_id = request.POST["category"]
        course.description = request.POST["description"]
        course.price = request.POST["price"]
        course.level = request.POST["level"]
        course.photo = request.FILES.get("photo", course.photo)
        course.save()
        messages.success(request, "Course updated")
        return redirect("course_detail", pk=pk)
    return render(request, "course_form.html", {"course": course,"categories": CourseCategory.objects.all()})





@login_required
@permission_required("my_web.add_course", raise_exception=True)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, mentor=request.user)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted")
        return redirect("course_list")
    return render(request, "course_delete.html", {"course": course})







@login_required
@require_POST
def course_join(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.students.add(request.user)
    messages.success(request, "You joined this course")
    return redirect("course_detail", pk=pk)





@login_required
def my_courses(request):
    courses = request.user.joined_courses.select_related("category", "mentor")
    return render(request, "my_courses.html", {"courses": courses})






@login_required
@require_POST
def comment_create(request, pk):
    CourseComment.objects.create(course_id=pk, user=request.user, text=request.POST["text"])
    messages.success(request, "Comment sent waiting for approval")
    return redirect("course_detail", pk=pk)





def send_confirm_code(user):
    code = str(randint(100000, 999999))
    EmailConfirmCode.objects.create(user=user, code=code)
    send_mail("Confirm your email", f"Your code {code}", settings.DEFAULT_FROM_EMAIL, [user.email])





def user_registration(request):
    if request.method == "POST":
        user = CustomUser.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"],
            is_active=False,
        )
        send_confirm_code(user)
        request.session["user_id"] = user.id
        return redirect("confirm_email")
    return render(request, "registration.html")





def confirm_email(request):
    if request.method == "POST":
        user = get_object_or_404(CustomUser, id=request.session.get("user_id"), is_active=False)
        code_obj = EmailConfirmCode.objects.filter(user=user,code=request.POST["code"],is_used=False).first()
        if code_obj:
            user.is_active = True
            user.save()
            code_obj.is_used = True
            code_obj.save()
            login(request, user, backend="main.backends.LoginByUsernameBackend")
            return redirect("course_list")
        return render(request, "confirm_email.html", {"error": "Invalid or expired code"})
    return render(request, "confirm_email.html")






def user_login(request):
    if request.method == "POST":
        user = authenticate(request,username=request.POST["username"],password=request.POST["password"],)
        if user:
            login(request, user)
            return redirect("course_list")
        return render(request, "login.html", {"error": "Wrong username or password"})
    return render(request, "login.html")






@login_required
@require_POST
def user_logout(request):
    logout(request)
    return redirect("course_list")











def get_youtube_embed_url(url):
    if not url:
        return ""
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":")[0]
    video_id = ""
    if host in ("youtu.be", "www.youtu.be"):
        video_id = parsed.path.strip("/").split("/")[0]
    elif host in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtube-nocookie.com",
        "www.youtube-nocookie.com",
    ):
        if parsed.path == "/watch":
            video_id = parse_qs(
                parsed.query
            ).get("v", [""])[0]

        elif parsed.path.startswith(
            ("/embed/", "/shorts/", "/live/")
        ):
            video_id = parsed.path.split("/")[2]

    if len(video_id) != 11:
        return ""
    if not all(char.isalnum() or char in "_-"for char in video_id):
        return ""
    return (f"https://www.youtube-nocookie.com/embed/"f"{video_id}")








@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(CourseLesson.objects.select_related("course"),pk=pk)
    if not (lesson.course.students.filter(pk=request.user.pk).exists()or request.user.is_staff):
        messages.warning(request, "First join this course.")
        return redirect("course_detail", pk=lesson.course.pk)
    error = None
    success = False
    success_points = 0
    questions = lesson.questions.all().order_by("order")
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        answer = request.POST.get("answer", "").strip()
        question = get_object_or_404(LessonQuestion,pk=question_id,lesson=lesson)
        already_answered = QuestionProgress.objects.filter(user=request.user,question=question).exists()
        if already_answered:
            error = "You have already answered this question."
        elif not answer:
            error = "Please enter your answer."
        elif answer.casefold() == question.correct_answer.strip().casefold():
            QuestionProgress.objects.create(user=request.user,question=question,points_earned=question.points)
            success = True
            success_points = question.points
            total_questions = questions.count()
            answered_questions = QuestionProgress.objects.filter(user=request.user,question__lesson=lesson).count()
            if total_questions > 0 and answered_questions == total_questions:
                total_lesson_points = QuestionProgress.objects.filter(user=request.user,question__lesson=lesson).aggregate(total=Count("id"))["total"]
                total_lesson_points = sum(
                    QuestionProgress.objects.filter(user=request.user,question__lesson=lesson).values_list("points_earned", flat=True))
                LessonProgress.objects.update_or_create(user=request.user,lesson=lesson,defaults={"is_completed": True,"points_earned": total_lesson_points})
        else:
            error = "Incorrect answer. Try again!"
    question_items = []
    for question in questions:
        question_progress = QuestionProgress.objects.filter(user=request.user,question=question).first()
        question_items.append({ "question": question, "progress": question_progress})
    lesson_progress = LessonProgress.objects.filter(user=request.user,lesson=lesson,is_completed=True).first()
    total_points = sum(
        request.user.question_progress.values_list("points_earned",flat=True))
    return render( request,"lesson_detail.html",{
            "lesson": lesson,
            "course": lesson.course,
            "embed_url": get_youtube_embed_url(lesson.youtube_url),
            "questions": question_items,
            "progress": lesson_progress,
            "error": error,
            "success": success,
            "success_points": success_points,
            "total_points": total_points,
        }
    )
