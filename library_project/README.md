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