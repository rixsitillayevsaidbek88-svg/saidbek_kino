from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Movie, Genre


def home(request):
    featured_movies = Movie.objects.filter(is_featured=True)[:6]
    latest_movies = Movie.objects.all()[:12]
    premium_movies = Movie.objects.filter(is_premium=True)[:6]
    genres = Genre.objects.all()
    return render(request, 'movies/home.html', {
        'featured_movies': featured_movies,
        'latest_movies': latest_movies,
        'premium_movies': premium_movies,
        'genres': genres,
    })


def movie_list(request):
    movies = Movie.objects.all()
    query = request.GET.get('q', '')
    genre_slug = request.GET.get('genre', '')
    movie_type = request.GET.get('type', '')

    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(original_title__icontains=query) |
            Q(director__icontains=query) |
            Q(actors__icontains=query)
        )
    if genre_slug:
        movies = movies.filter(genres__slug=genre_slug)
    if movie_type == 'premium':
        movies = movies.filter(is_premium=True)
    elif movie_type == 'free':
        movies = movies.filter(is_premium=False)

    genres = Genre.objects.all()
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'query': query,
        'genre_slug': genre_slug,
        'movie_type': movie_type,
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    # Premium kino tekshiruvi
    can_watch = True
    if movie.is_premium:
        if not request.user.is_authenticated:
            can_watch = False
        elif not request.user.active_premium:
            can_watch = False

    if can_watch:
        movie.views_count += 1
        movie.save(update_fields=['views_count'])

    is_saved = False
    if request.user.is_authenticated:
        is_saved = movie in request.user.saved_movies.all()

    similar_movies = Movie.objects.filter(
        genres__in=movie.genres.all()
    ).exclude(pk=pk).distinct()[:4]

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'can_watch': can_watch,
        'is_saved': is_saved,
        'similar_movies': similar_movies,
    })
