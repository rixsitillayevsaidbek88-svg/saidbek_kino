from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Payment
from django.conf import settings


@login_required
def premium_page(request):
    user = request.user
    user.check_premium_status()
    payments = Payment.objects.filter(user=user).order_by('-created_at')[:5]
    return render(request, 'payments/premium.html', {
        'user': user,
        'payments': payments,
        'price': settings.PREMIUM_PRICE,
    })


@login_required
def checkout(request):
    if request.user.active_premium:
        messages.info(request, "Siz allaqachon Premium a'zosiz! ⭐")
        return redirect('profile')

    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')
        card_name = request.POST.get('card_name', '')
        card_expiry = request.POST.get('card_expiry', '')
        card_cvv = request.POST.get('card_cvv', '')

        # Validatsiya
        errors = []
        if len(card_number) < 16:
            errors.append("Karta raqami noto'g'ri")
        if not card_name:
            errors.append("Karta egasi ismi kiritilmadi")
        if not card_expiry:
            errors.append("Muddati kiritilmadi")
        if len(card_cvv) < 3:
            errors.append("CVV noto'g'ri")

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'payments/checkout.html', {'price': settings.PREMIUM_PRICE})

        # To'lovni saqlash (demo - haqiqiy loyihada payment gateway)
        payment = Payment.objects.create(
            user=request.user,
            amount=settings.PREMIUM_PRICE,
            status='success',
            card_last4=card_number[-4:],
            transaction_id=f"TXN-{timezone.now().strftime('%Y%m%d%H%M%S')}-{request.user.pk}",
            paid_at=timezone.now(),
        )

        # Foydalanuvchiga premium berish
        user = request.user
        user.is_premium = True
        if user.premium_until and user.premium_until > timezone.now():
            user.premium_until += timedelta(days=30)
        else:
            user.premium_until = timezone.now() + timedelta(days=30)
        user.save()

        messages.success(
            request,
            "🎉 Tabriklaymiz! Premium a'zolik muvaffaqiyatli faollashtirildi! "
            "Endi barcha premim kinolarni tomosha qilishingiz mumkin."
        )
        return redirect('premium_success')

    return render(request, 'payments/checkout.html', {'price': settings.PREMIUM_PRICE})


@login_required
def premium_success(request):
    return render(request, 'payments/success.html', {'user': request.user})
