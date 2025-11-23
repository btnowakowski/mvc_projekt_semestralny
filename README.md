# mvc_projekt_semestralny

## Uruchomienie projektu lokalnie

### 1. Klonowanie repo

```bash
git clone <repo_url>
cd mvc_projekt_semestralny
```

### 2. Wirtualne środowisko i zależności

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/Mac

```bash
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Migracje bazy

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Superuser (admin)

```bash
python manage.py createsuperuser
```

### 5. Uruchomienie serwera

```bash
python manage.py runserver
```

Aplikacja działa pod:
[http://127.0.0.1:8000/]

Panel admina Django:
[http://127.0.0.1:8000/admin/]

Panel admina aplikacji:
[http://127.0.0.1:8000/admin-panel/]

### 6. Jeśli używasz grup

Po pierwszym uruchomieniu dodaj grupę "Admin" w /admin/ i przypisz użytkownika.
