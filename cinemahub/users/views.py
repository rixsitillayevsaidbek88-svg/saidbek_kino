from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import CustomUser


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}! Ro'yxatdan muvaffaqiyatli o'tdingiz 🎬")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name or user.username}! 👋")
            return redirect(request.GET.get('next', 'home'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqildi.")
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    user.check_premium_status()
    saved_movies = user.saved_movies.all()
    return render(request, 'users/profile.html', {
        'user': user,
        'saved_movies': saved_movies,
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi ✅")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def save_movie(request, movie_id):
    from movies.models import Movie
    movie = Movie.objects.get(pk=movie_id)
    user = request.user
    if movie in user.saved_movies.all():
        user.saved_movies.remove(movie)
        messages.info(request, f"'{movie.title}' saqlangan kinolardan olib tashlandi")
    else:
        user.saved_movies.add(movie)
        messages.success(request, f"'{movie.title}' saqlangan kinolarga qo'shildi ❤️")
    return redirect(request.META.get('HTTP_REFERER', 'profile'))


@login_required
def send_movie(request, movie_id):
    from movies.models import Movie
    movie = Movie.objects.get(pk=movie_id)
    users = CustomUser.objects.exclude(pk=request.user.pk)
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        try:
            recipient = CustomUser.objects.get(pk=recipient_id)
            # Real projectda email/SMS yuboriladi
            messages.success(request, f"'{movie.title}' kino {recipient.username} ga yuborildi 📤")
        except CustomUser.DoesNotExist:
            messages.error(request, "Foydalanuvchi topilmadi")
        return redirect('movie_detail', pk=movie_id)
    return render(request, 'users/send_movie.html', {
        'movie': movie,
        'users': users
    })
