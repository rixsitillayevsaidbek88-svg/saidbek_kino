from django.db import models
from django.conf import settings
import uuid


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('success', 'Muvaffaqiyatli'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('cancelled', 'Bekor qilindi'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Foydalanuvchi"
    )
    amount = models.IntegerField(verbose_name="Summa (so'm)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    card_last4 = models.CharField(max_length=4, blank=True, verbose_name="Karta (oxirgi 4 raqam)")
    transaction_id = models.CharField(max_length=200, blank=True, verbose_name="Tranzaksiya ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name="To'lov sanasi")
    notes = models.TextField(blank=True, verbose_name="Izoh")

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.amount:,} so'm ({self.get_status_display()})"
