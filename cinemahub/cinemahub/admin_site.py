from django.contrib import admin
from django.utils.html import format_html


class CinemaHubAdminSite(admin.AdminSite):
    site_header = format_html('🎬 CinemaHub Admin Panel')
    site_title = 'CinemaHub Admin'
    index_title = 'Boshqaruv paneli'
    site_url = '/'
