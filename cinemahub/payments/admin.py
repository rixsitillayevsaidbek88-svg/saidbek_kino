from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'amount_display', 'status_badge',
        'card_last4', 'transaction_id', 'created_at', 'paid_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email', 'transaction_id', 'card_last4']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'paid_at']

    fieldsets = (
        ('To\'lov ma\'lumoti', {
            'fields': ('id', 'user', 'amount', 'status')
        }),
        ('Karta', {
            'fields': ('card_last4', 'transaction_id')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'paid_at')
        }),
        ('Izoh', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    def user_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:users_customuser_change', args=[obj.user.pk])
        premium_icon = "⭐" if obj.user.is_premium else ""
        return format_html(
            '<a href="{}" style="color:#3b82f6;font-weight:600">{} {}</a>',
            url, obj.user.username, premium_icon
        )
    user_link.short_description = "Foydalanuvchi"

    def amount_display(self, obj):
        return format_html(
            '<span style="color:#10b981;font-weight:700">{:,} so\'m</span>',
            obj.amount
        )
    amount_display.short_description = "Summa"

    def status_badge(self, obj):
        colors = {
            'pending': ('#f59e0b', '⏳ Kutilmoqda'),
            'success': ('#10b981', '✅ Muvaffaqiyatli'),
            'failed': ('#ef4444', '❌ Muvaffaqiyatsiz'),
            'cancelled': ('#6b7280', '🚫 Bekor qilindi'),
        }
        color, label = colors.get(obj.status, ('#6b7280', obj.status))
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:20px;font-size:11px;white-space:nowrap">{}</span>',
            color, label
        )
    status_badge.short_description = "Holat"

    actions = ['mark_success', 'mark_failed']

    def mark_success(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        count = 0
        for payment in queryset:
            payment.status = 'success'
            payment.paid_at = timezone.now()
            payment.save()
            # Foydalanuvchiga premium berish
            payment.user.is_premium = True
            payment.user.premium_until = timezone.now() + timedelta(days=30)
            payment.user.save()
            count += 1
        self.message_user(request, f"{count} ta to'lov tasdiqlandi va Premium berildi ✅")
    mark_success.short_description = "To'lovni tasdiqlash + Premium berish"

    def mark_failed(self, request, queryset):
        count = queryset.update(status='failed')
        self.message_user(request, f"{count} ta to'lov bekor qilindi")
    mark_failed.short_description = "Muvaffaqiyatsiz deb belgilash"
