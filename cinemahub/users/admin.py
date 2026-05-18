from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'get_full_name', 'email', 'phone',
        'premium_badge', 'premium_until', 'date_joined', 'is_staff'
    ]
    list_filter = ['is_premium', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumot', {
            'fields': ('phone', 'avatar', 'bio')
        }),
        ('Premium a\'zolik', {
            'fields': ('is_premium', 'premium_until'),
            'classes': ('collapse',),
        }),
        ('Saqlangan kinolar', {
            'fields': ('saved_movies',),
            'classes': ('collapse',),
        }),
    )

    filter_horizontal = ('saved_movies', 'groups', 'user_permissions')

    readonly_fields = ['date_joined', 'last_login']

    def premium_badge(self, obj):
        if obj.is_premium:
            if obj.premium_until and timezone.now() < obj.premium_until:
                days_left = (obj.premium_until - timezone.now()).days
                return format_html(
                    '<span style="background:#f59e0b;color:#fff;padding:3px 10px;'
                    'border-radius:20px;font-size:11px;font-weight:600">'
                    '⭐ PREMIUM ({} kun)</span>', days_left
                )
            return format_html(
                '<span style="background:#ef4444;color:#fff;padding:3px 10px;'
                'border-radius:20px;font-size:11px">⚠️ Muddati tugagan</span>'
            )
        return format_html(
            '<span style="background:#6b7280;color:#fff;padding:3px 10px;'
            'border-radius:20px;font-size:11px">Oddiy</span>'
        )
    premium_badge.short_description = "Premium holati"

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = "To'liq ism"

    actions = ['grant_premium_30_days', 'revoke_premium']

    def grant_premium_30_days(self, request, queryset):
        from datetime import timedelta
        count = 0
        for user in queryset:
            user.is_premium = True
            user.premium_until = timezone.now() + timedelta(days=30)
            user.save()
            count += 1
        self.message_user(request, f"{count} ta foydalanuvchiga 30 kunlik Premium berildi ✅")
    grant_premium_30_days.short_description = "30 kunlik Premium berish"

    def revoke_premium(self, request, queryset):
        count = queryset.update(is_premium=False, premium_until=None)
        self.message_user(request, f"{count} ta foydalanuvchidan Premium olindi")
    revoke_premium.short_description = "Premiumni bekor qilish"
