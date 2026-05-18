from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Movie, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'movie_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def movie_count(self, obj):
        count = obj.movie_set.count()
        return format_html('<b>{}</b> ta kino', count)
    movie_count.short_description = "Kinolar soni"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'poster_thumbnail', 'title', 'year', 'quality_badge',
        'premium_badge', 'featured_badge', 'rating_display',
        'views_display', 'created_at'
    ]
    list_display_links = ['poster_thumbnail', 'title']
    list_filter = ['is_premium', 'is_featured', 'quality', 'year', 'genres']
    search_fields = ['title', 'original_title', 'director', 'actors']
    filter_horizontal = ['genres']
    ordering = ['-created_at']
    list_per_page = 20

    fieldsets = (
        ('Asosiy ma\'lumot', {
            'fields': ('title', 'original_title', 'description', 'poster')
        }),
        ('Video', {
            'fields': ('video_url', 'video_file', 'trailer_url'),
            'description': 'Video URL yoki fayl birini tanlang'
        }),
        ('Tafsilotlar', {
            'fields': ('genres', 'year', 'country', 'director', 'actors', 'duration', 'quality')
        }),
        ('Sozlamalar', {
            'fields': ('is_premium', 'is_featured', 'rating'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ['views_count', 'created_at', 'updated_at']

    def poster_thumbnail(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width:60px;height:85px;object-fit:cover;'
                'border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.3)"/>',
                obj.poster.url
            )
        return format_html(
            '<div style="width:60px;height:85px;background:#1a1a2e;border-radius:6px;'
            'display:flex;align-items:center;justify-content:center;color:#666;font-size:20px">🎬</div>'
        )
    poster_thumbnail.short_description = ""

    def quality_badge(self, obj):
        colors = {'SD': '#6b7280', 'HD': '#3b82f6', 'FHD': '#8b5cf6', '4K': '#f59e0b'}
        color = colors.get(obj.quality, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:11px;font-weight:700">{}</span>',
            color, obj.quality
        )
    quality_badge.short_description = "Sifat"

    def premium_badge(self, obj):
        if obj.is_premium:
            return format_html(
                '<span style="background:#f59e0b;color:#fff;padding:2px 8px;'
                'border-radius:4px;font-size:11px">⭐ Premium</span>'
            )
        return format_html(
            '<span style="background:#e5e7eb;color:#374151;padding:2px 8px;'
            'border-radius:4px;font-size:11px">Bepul</span>'
        )
    premium_badge.short_description = "Turi"

    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html('🔥')
        return ''
    featured_badge.short_description = "Tavsiya"

    def rating_display(self, obj):
        stars = '⭐' * int(obj.rating / 2)
        return format_html(
            '<span style="color:#f59e0b;font-weight:600">{}</span> {}',
            obj.rating, stars
        )
    rating_display.short_description = "Reyting"

    def views_display(self, obj):
        if obj.views_count >= 1000:
            return format_html('<span style="color:#10b981">{:.1f}K</span>', obj.views_count / 1000)
        return format_html('<span>{}</span>', obj.views_count)
    views_display.short_description = "Ko'rishlar"

    actions = ['make_premium', 'make_free', 'make_featured']

    def make_premium(self, request, queryset):
        count = queryset.update(is_premium=True)
        self.message_user(request, f"{count} ta kino Premium qilindi ⭐")
    make_premium.short_description = "Premium qilish"

    def make_free(self, request, queryset):
        count = queryset.update(is_premium=False)
        self.message_user(request, f"{count} ta kino bepul qilindi")
    make_free.short_description = "Bepul qilish"

    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} ta kino tavsiya etildi 🔥")
    make_featured.short_description = "Tavsiya etish"
