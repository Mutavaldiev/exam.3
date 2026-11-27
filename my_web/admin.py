from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from .models import *




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ("id","username","email","phone","is_active","is_staff","is_superuser",)
    list_filter = ("is_active","is_staff","is_superuser","groups",)
    search_fields = ( "username", "email", "phone",)
    ordering = ("-date_joined",)
    fieldsets = UserAdmin.fieldsets + (("Additional Information", {"fields": ("phone",),}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional Information", {"fields": ("email", "phone"),}),)






@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ("id","user","role",)
    list_filter = ("role",)
    search_fields = ("user__username","user__email",)
    list_select_related = ( "user",)




@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):

    list_display = ("id","name","courses_count",)
    search_fields = ("name","description",)
    def get_queryset(self, request):
        return (super().get_queryset(request).annotate(total=Count("courses")))
    @admin.display(description="Total courses")
    def courses_count(self, obj):
        return obj.total





class CourseLessonInline(admin.TabularInline):
    model = CourseLesson
    extra = 1
    fields = ( "title", "day", "youtube_url", "content",)
    show_change_link = True




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ("id","title","category","mentor","price","level","views","created_at",)
    list_filter = ("category","level","created_at",)
    search_fields = ( "title", "description", "mentor__username", "mentor__email",)
    list_select_related = ("category","mentor",)
    filter_horizontal = ("students",)
    inlines = [CourseLessonInline,]
    readonly_fields = ("views","created_at",)
    ordering = ("-created_at",)
    fieldsets = (("Course Information", {"fields": ("title","category","mentor","description","photo",),}),
        ("Course Settings", {"fields": ("price","level","students",),}),
        ("Statistics", {"fields": ("views","created_at",),}),)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(mentor=request.user)






class LessonQuestionInline(admin.TabularInline):
    model = LessonQuestion
    extra = 3
    fields = ( "order", "question", "correct_answer", "points",)
    ordering = ("order",)





@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ("id","title","course","day","questions_count",)
    list_filter = ("course",)
    search_fields = ( "title", "course__title", "content",)
    list_select_related = ("course",)
    inlines = [LessonQuestionInline,]
    ordering = ("course","day",)

    @admin.display(description="Total questions")
    def questions_count(self, obj):
        return obj.questions.count()
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter( course__mentor=request.user)






@admin.register(LessonQuestion)
class LessonQuestionAdmin(admin.ModelAdmin):

    list_display = ("id","lesson","order","question_short","points",)
    list_filter = ("lesson__course",)
    search_fields = ("question","lesson__title","lesson__course__title",)
    list_select_related = ("lesson","lesson__course",)
    ordering = ( "lesson", "order",)
    @admin.display(description="Question")
    def question_short(self, obj):
        return obj.question[:70]






@admin.register(QuestionProgress)
class QuestionProgressAdmin(admin.ModelAdmin):

    list_display = ("id","user","question","points_earned","completed_at",)
    list_filter = ( "completed_at", "question__lesson__course",)
    search_fields = ("user__username","question__question",)
    list_select_related = ( "user", "question", "question__lesson",)
    readonly_fields = ("user","question","points_earned","completed_at",)
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False







@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):

    list_display = ("id","user","lesson","is_completed","points_earned","completed_at",)
    list_filter = ("is_completed","lesson__course",)
    search_fields = ("user__username","lesson__title",)
    list_select_related = ("user","lesson",)
    readonly_fields = ("user","lesson","is_completed","points_earned","completed_at",)
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False







@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):

    list_display = ("id","user","course","status","created_at",)
    list_filter = ("status","created_at",)
    search_fields = ("user__username","course__title","text",)
    list_select_related = ("user","course",)
    readonly_fields = ("user","course","created_at",)
    actions = ("approve_comments","reject_comments",)
    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Reject selected comments")
    def reject_comments(self, request, queryset):
        queryset.update(status="rejected")





