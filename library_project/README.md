# 📚 Knižnica a evidencia výpožičiek (Django)

## 🎯 Cieľ projektu
Webová aplikácia na správu knižnice, ktorá umožňuje evidenciu kníh, autorov a výpožičiek.

---

## ⚙️ Použité technológie
- Python 3.12
- Django
- SQLite
- HTML (Django templates)

---

## 🧩 Funkcionality

### 📘 Knihy
- CRUD operácie (pridanie, zobrazenie, úprava, zmazanie)
- filtrovanie podľa žánru, autora a dostupnosti
- detail knihy

### ✍️ Autori
- CRUD operácie
- M:N vzťah s knihami

### 📖 Výpožičky
- požičanie knihy
- vrátenie knihy
- história výpožičiek

### 🔐 Používatelia
- login systém (Django auth)
- 2 roly:
  - knihovník (admin)
  - bežný používateľ

---

## 🗄️ Modely
- Book
- Author
- Loan
- User (Django auth)

---

## 🔗 Vzťahy
- Book ↔ Author (ManyToMany)
- User ↔ Loan (ForeignKey)
- Book ↔ Loan (ForeignKey)

---

## 🔎 Filtrovanie
- podľa autora
- podľa žánru
- podľa dostupnosti

---

## 🚀 Spustenie projektu
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

---

## 👤 Roly
- knihovník: správa kníh (CRUD)
- user: prezeranie a požičiavanie kníh

---

## 📌 Autor
Školský projekt – Django knižničný systém
## Úpravy dizajnu a funkcií
- Pridaný svetlomodrý štýl podľa dodaného PDF návrhu.
- Logo `logo.png` je v hlavičke vycentrované.
- Zoznam kníh zobrazuje obálky z poľa `cover_image`; ak obálka chýba, zobrazí sa náhradný box s názvom knihy.
- Kliknutie na obálku otvorí detail knihy.
- Prihlásení používatelia môžu požičať dostupnú knihu priamo zo zoznamu aj z detailu knihy.


## Render deployment

Use **Web Service**, not Static Site.

Build Command:

```bash
chmod +x build.sh && ./build.sh
```

Start Command:

```bash
gunicorn library_project.wsgi:application
```

Environment variables:

```text
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
```

For a school/demo project SQLite is included. For production, use PostgreSQL and persistent media storage.
