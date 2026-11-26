from django.contrib import admin
from django.db.models import Count
from .models import *





@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("username", "email")
    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.set_password(obj.password)
        obj.save()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "courses_count")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total=Count("courses"))

    def courses_count(self, obj):
        return obj.total


class CourseLessonInline(admin.TabularInline):
    model = CourseLesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "mentor", "price", "level", "views")
    list_filter = ("category", "level")
    search_fields = ("title", "mentor__username")
    list_select_related = ("category", "mentor")
    filter_horizontal = ("students",)
    inlines = [CourseLessonInline]

    def get_queryset(self, request):
        courses = super().get_queryset(request)
        if request.user.is_superuser:
            return courses
        return courses.filter(mentor=request.user)


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "day")
    list_filter = ("course",)


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "status", "created_at")
    list_filter = ("status",)
    actions = ["approve_comments", "reject_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(status="approved")

    def reject_comments(self, request, queryset):
        queryset.update(status="rejected")



@admin.register(EmailConfirmCode)
class EmailConfirmCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "code", "is_used", "created_at")