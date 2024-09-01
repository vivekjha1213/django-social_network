import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser):
    USER_ROLES = [
        ("Admin", "admin"),
        ("User", "user"),
        ("Guest", "guest"),
    ]

    # Using UUID for the primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=USER_ROLES)

    receiver_id = models.CharField(max_length=10)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
