from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Janr nomi")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Janr"
        verbose_name_plural = "Janrlar"

    def __str__(self):
        return self.name


class Movie(models.Model):
    QUALITY_CHOICES = [
        ('SD', 'SD'),
        ('HD', 'HD'),
        ('FHD', 'Full HD'),
        ('4K', '4K Ultra HD'),
    ]

    title = models.CharField(max_length=200, verbose_name="Kino nomi")
    original_title = models.CharField(max_length=200, blank=True, verbose_name="Asl nomi")
    description = models.TextField(verbose_name="Tavsif")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Poster")
    trailer_url = models.URLField(blank=True, null=True, verbose_name="Trailer URL")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Video fayl")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL (YouTube/embed)")

    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Janrlar")
    year = models.IntegerField(verbose_name="Yili")
    country = models.CharField(max_length=100, blank=True, verbose_name="Mamlakat")
    director = models.CharField(max_length=200, blank=True, verbose_name="Rejissor")
    actors = models.TextField(blank=True, verbose_name="Aktyorlar")
    duration = models.IntegerField(blank=True, null=True, verbose_name="Davomiyligi (daqiqa)")
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='HD', verbose_name="Sifat")

    is_premium = models.BooleanField(default=False, verbose_name="Premium kino")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etilgan")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Reyting")
    views_count = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kino"
        verbose_name_plural = "Kinolar"
        ordering = ['-created_at']

    def __str__(self):
        premium_mark = " ⭐" if self.is_premium else ""
        return f"{self.title} ({self.year}){premium_mark}"

    def get_embed_url(self):
        """YouTube URL ni embed formatiga o'tkazadi"""
        if self.video_url and 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url
