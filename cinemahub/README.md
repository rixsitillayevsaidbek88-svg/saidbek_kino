# 🎬 CinemaHub — Kino Platformasi

Django asosida qurilgan to'liq kino platformasi.

## Xususiyatlar

- 🎬 Kinolar katalogi (qidirish, janr bo'yicha filter)
- 👤 Foydalanuvchi ro'yxatdan o'tish va profil
- ⭐ Premium a'zolik (12,000 so'm/oy, kartadan to'lov)
- ❤️ Kinolarni saqlash
- 📤 Do'stga kino yuborish
- 🔒 Premium kinolar uchun cheklash
- 🛠 Kuchli admin panel (dark theme)

## O'rnatish

```bash
# 1. Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Kutubxonalar o'rnatish
pip install -r requirements.txt

# 3. Migratsiyalar
python manage.py makemigrations
python manage.py migrate

# 4. Superuser yaratish (admin uchun)
python manage.py createsuperuser

# 5. Serverni ishga tushirish
python manage.py runserver
```

## URL manzillar

| URL | Tavsif |
|-----|--------|
| `/` | Bosh sahifa |
| `/movies/` | Barcha kinolar |
| `/movies/<id>/` | Kino sahifasi |
| `/users/register/` | Ro'yxatdan o'tish |
| `/users/login/` | Kirish |
| `/users/profile/` | Profil |
| `/payments/premium/` | Premium sahifa |
| `/payments/checkout/` | To'lov sahifasi |
| `/admin/` | Admin panel |

## Admin panelida nima qilish mumkin?

### Kinolar (Movies)
- Kino qo'shish, tahrirlash, o'chirish
- Poster yuklash
- Premium/bepul qilish
- Tavsiya etish (featured)
- Janr belgilash
- Video URL yoki fayl qo'shish

### Foydalanuvchilar (Users)
- Barcha foydalanuvchilarni ko'rish
- Premium berish/olish
- Profil ma'lumotlarini ko'rish
- Saqlangan kinolarni ko'rish

### To'lovlar (Payments)
- To'lov tarixini ko'rish
- To'lovni tasdiqlash (va avtomatik premium berish)
- To'lov holati o'zgartirish

## Loyiha strukturasi

```
cinemahub/
├── cinemahub/          # Asosiy sozlamalar
│   ├── settings.py
│   └── urls.py
├── movies/             # Kinolar app
│   ├── models.py       # Movie, Genre modeli
│   ├── views.py
│   └── admin.py
├── users/              # Foydalanuvchilar app
│   ├── models.py       # CustomUser modeli
│   ├── views.py
│   └── admin.py
├── payments/           # To'lovlar app
│   ├── models.py       # Payment modeli
│   ├── views.py
│   └── admin.py
├── templates/          # HTML shablonlar
└── static/             # CSS, JS, rasmlar
```
