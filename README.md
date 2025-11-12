## SSL Certificates
These certificates are self-signed and intended **only for local development**.
Do not use them in production.

# 🧠 Noesis — Backend Systemu do Analizy EEG

Serwerowa część aplikacji do analizy fal mózgowych EEG, zbudowana jako API wspierające logikę biznesową, autoryzację i komunikację z bazą danych.

## 🚀 Uruchomienie aplikacji (Docker Compose)

 
Aby uruchomić cały system (frontend + backend + baza danych):

Upewnij się, że masz oba repozytoria:
```bash
WebEEG-backend/
WebEEG-front/
```

Oba katalogi muszą znajdować się w tym samym folderze nadrzędnym.

Przejdź do folderu WebEEG-backend:
```bash
cd WebEEG-backend
```

Uruchom środowisko:

```bash
docker compose up -d
```

W obu repozytoriach znajdują się pliki Dockerfile, które powodują zbudowanie obrazów z odpowiednimi zależnościami. Po dodaniu nowej zależności należy zbudować obraz na nowo np: 

```bash
docker compose build backend
```

## 🔧 Migracje bazy danych (Alembic)


Aby dodać nowe migracje po zmianach w modelach SQLAlchemy:

1. Dodaj nowe modele lub zmodyfikuj istniejące w module models/.

2. Zarejestruj nowy model w pliku models \_\_init\_\_.py, aby Alembic mógł go wykryć:

```bash
from my_new_model import MyNewModel
```

3. Wygeneruj migrację:

```bash
alembic revision --autogenerate -m "Opis zmian"
```

4. Zastosuj migracje:
```bash
alembic upgrade head
```
Przy stacie kontenera migracje automatycznie się wykonują.


# 🧠 Noesis — Backend for EEG Analysis System

The server-side component of the EEG brainwave analysis application, built as an API supporting business logic, authentication, and database communication.

## 🚀 Running the Application (Docker Compose)

To launch the entire system (frontend + backend + database):

Make sure you have both repositories:
```bash
WebEEG-backend/
WebEEG-front/
```

Both directories must be located in the same parent folder.

Navigate to the WebEEG-backend folder:
```bash
cd WebEEG-backend
```
Start the environment:
```bash
docker compose build backend
```
Both repositories include Dockerfiles that build images with all required dependencies. If you add a new dependency, rebuild the image as follows:

```bash
docker compose build backend
```

## 🔧 Database Migrations (Alembic)

To create new migrations after making changes to SQLAlchemy models:

1.Add or modify models in the models/ module.

2.Register the new model in models/\_\_init\_\_.py so Alembic can detect it:

```bash
from my_new_model import MyNewModel
```

3.Generate a migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

4.Apply the migration:
```bash
alembic upgrade head
```
Migrations are applied automatically when the container starts.

