from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Rasm")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografiya")
    is_premium = models.BooleanField(default=False, verbose_name="Premium a'zo")
    premium_until = models.DateTimeField(blank=True, null=True, verbose_name="Premium muddati")
    saved_movies = models.ManyToManyField(
        'movies.Movie',
        blank=True,
        related_name='saved_by',
        verbose_name="Saqlangan kinolar"
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.username} ({'Premium' if self.is_premium else 'Oddiy'})"

    def check_premium_status(self):
        """Premium muddati tugagan bo'lsa o'chiradi"""
        if self.is_premium and self.premium_until:
            if timezone.now() > self.premium_until:
                self.is_premium = False
                self.premium_until = None
                self.save()
        return self.is_premium

    @property
    def active_premium(self):
        return self.check_premium_status()
