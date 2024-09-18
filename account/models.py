from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Base user
class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^09\d{9}",
        message="{}\n{}".format(
            _("Phone number must be entered in the format: '09999999999'."),
            _("Up to 11 digits allowed."),
        ),
    )

    user_type_choices = (
        ("student", "student"),
        ("institute", "institute"),
        ("freelance", "freelance"),
        ("admin", "admin"),
        ("unknown", "unknown"),
    )

    username = models.CharField(max_length=128, unique=True, blank=True, null=True)
    user_type = models.CharField(
        max_length=10, default="unknown", choices=user_type_choices
    )
    national_code = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=11, unique=True
    )
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return (
            str(self.phone_number)
            + " | "
            + str(self.first_name)
            + " | "
            + str(self.last_name)
        )

    def is_profile_fill(self):
        if (
            self.first_name is not None
            and self.last_name is not None
            and self.phone_number is not None
            and self.national_code is not None
            and self.birth_date is not None
        ):
            return True
        else:
            return False


# INstitute
class InstituteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    provinces = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="institute_logo", blank=True, null=True)
    cover = models.ImageField(upload_to="institute_cover", blank=True, null=True)
    slogan = models.CharField(max_length=500, blank=True, null=True)
    economic_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=6000, blank=True, null=True)
    ZP_MERCHANT_ID = models.CharField(
        max_length=256,
        default="00000000-0000-0000-0000-000000000000",
        blank=True,
        null=True,
    )
    primary_color = models.CharField(max_length=100, blank=True, null=True)
    secondary_color = models.CharField(max_length=100, blank=True, null=True)
    memory_mirror_price = models.IntegerField(blank=True, null=True)
    audio_scripter_price = models.IntegerField(blank=True, null=True)
    wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.user.phone_number


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        InstituteProfile.objects.create(user=instance)


# student
class StudentProfile(models.Model):
    gender_type_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather-not-say", "Rather-not-say"),
    )

    english_level_choices = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_IELTS_student = models.BooleanField(default=False)
    institute = models.ForeignKey(
        InstituteProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    gender = models.CharField(
        max_length=20, default="Male", choices=gender_type_choices
    )
    english_level = models.CharField(
        max_length=10, default="A1", choices=english_level_choices
    )
    description = models.TextField(max_length=4000, blank=True, null=True)

    def __str__(self):
        return self.user.phone_number


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)


# freelance
class FreelanceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    provinces = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="institute_logo", blank=True, null=True)
    cover = models.ImageField(upload_to="institute_cover", blank=True, null=True)
    slogan = models.CharField(max_length=500, blank=True, null=True)
    economic_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=6000, blank=True, null=True)
    ZP_MERCHANT_ID = models.CharField(
        max_length=256,
        default="00000000-0000-0000-0000-000000000000",
        blank=True,
        null=True,
    )
    primary_color = models.CharField(max_length=100, blank=True, null=True)
    secondary_color = models.CharField(max_length=100, blank=True, null=True)
    memory_mirror_price = models.IntegerField(blank=True, null=True)
    audio_scripter_price = models.IntegerField(blank=True, null=True)
    wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.user.phone_number


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FreelanceProfile.objects.create(user=instance)
