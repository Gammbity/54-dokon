# 54-dokon 🛍️

## 📌 Loyiha haqida
**54-dokon** - bu ko‘p do‘konlarni o‘z ichiga olgan e-commerce platformasi bo‘lib, foydalanuvchilar mahsulotlarni ko‘rish, buyurtma berish va to‘lovlarni amalga oshirishlari mumkin.

Loyiha **Django REST Framework**, **PostgreSQL**, **Docker**, **Celery**, **AWS**, va **aiogram** yordamida yaratilgan.

## 🚀 Xususiyatlari
✅ Mahsulotlarni boshqarish (CRUD)
✅ Foydalanuvchilar autentifikatsiyasi
✅ Buyurtmalarni boshqarish
✅ Telegram bot integratsiyasi
✅ AWS bilan bog‘langan bazaviy ma’lumotlar bazasi
✅ Celery yordamida asinxron vazifalarni bajarish
✅ Docker yordamida konteynerizatsiya qilingan arxitektura

## 🛠️ Foydalanilgan texnologiyalar
- **Python 3.10+**
- **Django REST Framework**
- **PostgreSQL**
- **Celery & Redis**
- **Docker & Docker Compose**
- **AWS RDS** (ma’lumotlar bazasi)
- **aiogram** (Telegram bot)

## 🔧 O‘rnatish

Loyihani ishga tushirish uchun quyidagi qadamlarni bajaring:

```bash
# Repository-ni klonlash
git clone https://github.com/Gammbity/54-dokon.git
cd 54-dokon

# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # (Windows uchun: venv\Scripts\activate)

# Kerakli kutubxonalarni o‘rnatish
pip install -r requirements.txt
```

## 🚀 Ishga tushirish

### 1. Django serverni ishga tushirish

```bash
python manage.py migrate
python manage.py createsuperuser  # Admin foydalanuvchi yaratish
python manage.py runserver
```

### 2. Celery-ni ishga tushirish

```bash
celery -A config worker --loglevel=info
```

### 3. Docker bilan ishlash

```bash
docker-compose up -d
```

## 📖 API hujjatlari
Swagger orqali API hujjatlarini ko‘rish uchun:

```
http://127.0.0.1:8000/docs/
```

## 🤝 Hissa qo‘shish
Agar loyihaga hissa qo‘shmoqchi bo‘lsangiz:
1. **Fork qiling** 🚀
2. **Yangi branch yarating** (`feature/new-feature`)
3. **O‘zgarishlar kiriting va commit qiling**
4. **Pull Request yuboring**

## 📞 Aloqa
Agar savollaringiz bo‘lsa, quyidagi manzil orqali bog‘laning:
📧 **Email:** abduboriyabdusamadov66@gmail.com

---
🛍️ **54-dokon** - e-commerce dunyosiga xush kelibsiz!

