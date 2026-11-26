from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Course, CustomUser, UserProfile

MENTOR_PERMISSIONS = [
    "add_course", "change_course", "delete_course", "view_course",
    "add_courselesson", "change_courselesson", "delete_courselesson", "view_courselesson"]




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)




@receiver(post_save, sender=UserProfile)
def make_user_mentor(sender, instance, **kwargs):
    if instance.role == "mentor":
        group, _ = Group.objects.get_or_create(name="Mentor")
        group.permissions.set(Permission.objects.filter(codename__in=MENTOR_PERMISSIONS))
        instance.user.groups.add(group)
        CustomUser.objects.filter(pk=instance.user.pk).update(is_staff=True)





@receiver(m2m_changed, sender=Course.students.through)
def email_mentor_about_new_student(sender, instance, action, **kwargs):
    if action == "post_add":
        send_mail("New student",f"New student joined your course: {instance.title}",
            settings.DEFAULT_FROM_EMAIL,
            [instance.mentor.email],
            fail_silently=True,
        )