from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db.models.fields import TextField
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from stdimage.models import StdImageField
from mdeditor.fields import MDTextField
from markdownx.models import MarkdownxField





class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('メールアドレス', unique=True)
    user_id = models.CharField(('数字のみ入力可能です。'), max_length=10,null=True,unique=False)
    name = models.CharField(('名前'), max_length=20, null=True)
    myfollow = models.IntegerField(blank=True, default=0)
    icon = StdImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=False,
    variations={
        'size_1': (200, 100, True),
        'size_2': (400, 400),
        'size_3': (600, 600),
        'size_4': (800, 600),
        'size_5': (1000, 700),
    })
    content = models.TextField("自己紹介", max_length=200, blank=True)
    created = models.DateTimeField(('入会日'), default=timezone.now)
    myfollow = models.IntegerField(blank=True, default=0)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email