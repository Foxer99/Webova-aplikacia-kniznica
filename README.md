# 📚 Knižnica – webová aplikácia

Toto je školský projekt vytvorený v **Django**.
Aplikácia slúži na správu knižnice, kníh, autorov a výpožičiek.

## 🌐 Spustená aplikácia

Aplikácia je nasadená na Render:

```text
https://webova-aplikacia-kniznica-t36n.onrender.com
```

## 🎯 Cieľ projektu

Cieľom projektu je vytvoriť jednoduchú webovú aplikáciu, v ktorej sa dajú:

* prezerať knihy,
* pridávať a upravovať knihy,
* spravovať autorov,
* požičiavať knihy,
* vracať knihy,
* spravovať používateľov.

## ⚙️ Použité technológie

* Python
* Django
* SQLite
* HTML
* CSS
* GitHub
* Render

## 🧩 Hlavné funkcie

### Knihy

Používateľ môže vidieť zoznam kníh, detail knihy a obálku knihy.
Prihlásený používateľ si môže dostupnú knihu požičať.

Administrátor môže knihy pridávať, upravovať a mazať.

### Autori

Aplikácia umožňuje spravovať autorov.
Ku knihám môžu byť priradení autori.

### Výpožičky

Používateľ si môže knihu požičať a potom ju vrátiť.
Vie si pozrieť aj svoje výpožičky.

Administrátor vidí všetky výpožičky.

### Používatelia

Aplikácia obsahuje registráciu, prihlásenie a odhlásenie.
Používateľ má vlastný profil.

V aplikácii sú dve hlavné roly:

* bežný používateľ,
* administrátor / knihovník.

## 🗄️ Modely v projekte

V projekte sa používajú tieto hlavné modely:

* Book
* Author
* Loan
* User

## 🔗 Vzťahy medzi modelmi

* jedna kniha môže mať viacerých autorov,
* jeden autor môže mať viac kníh,
* používateľ môže mať viac výpožičiek,
* kniha môže byť vo viacerých výpožičkách.

## 🎨 Dizajn

Aplikácia má svetlomodrý dizajn.
V hlavičke sa nachádza logo.
Knihy sa zobrazujú spolu s obálkami.
Ak kniha nemá obálku, zobrazí sa náhradný obrázok.

## 🚀 Spustenie projektu lokálne

### 1. Stiahnutie projektu

```bash
git clone https://github.com/Foxer99/Webova-aplikacia-kniznica.git
cd Webova-aplikacia-kniznica/library_project
```

### 2. Vytvorenie virtuálneho prostredia

```bash
python -m venv .venv
```

### 3. Aktivovanie virtuálneho prostredia

Windows:

```bash
.venv\Scripts\activate
```

Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Inštalácia balíkov

```bash
pip install -r requirements.txt
```

### 5. Migrácie databázy

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Spustenie aplikácie

```bash
python manage.py runserver
```

Aplikácia bude dostupná na adrese:

```text
http://127.0.0.1:8000/
```

## ☁️ Nasadenie na Render

Na Renderi treba vytvoriť **Web Service**, nie Static Site.

Nastavenia:

```text
Root Directory: library_project
```

```text
Build Command: ./build.sh
```

```text
Start Command: gunicorn library_project.wsgi:application
```

Environment variables:

```text
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
```

## 🖼️ Obrázky

Obálky kníh sú uložené v priečinku:

```text
media/book_covers/
```

V nastaveniach projektu sa používajú:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 👤 Autori

Projekt vytvorili:

* Filip Michel
* Lukáš Padyšák

## 📌 Poznámka

Tento projekt bol vytvorený ako školská webová aplikácia na správu knižnice a evidenciu výpožičiek.
