# Aplikacja Kurier

Aplikacja Kurier to system umożliwiający zarządzanie paczkami i dostawcami. Pozwala użytkownikom na tworzenie, edycję i śledzenie przesyłek oraz obsługę kont kurierów.

## Wymagania

Aby uruchomić aplikację Kurier, potrzebujesz:

- Python 3.6 lub nowszy
- Django 3.2 lub nowszy

## Instalacja

1. Sklonuj repozytorium:

https://github.com/Faruu8/kurier


2. Przejdź do katalogu projektu:

cd ścieżka/do/aplikacji


3. Przeprowadź migracje bazy danych:

python manage.py makemigrations
python manage.py migrate


4. Uruchom serwer deweloperski:

python manage.py runserver



5. Aplikacja jest dostępna pod adresem http://localhost:8000/ w przeglądarce.

## Użytkowanie

### Rejestracja i logowanie

- Aby zarejestrować nowego użytkownika, przejdź do strony rejestracji i wypełnij formularz rejestracji.
- Aby zalogować się do istniejącego konta, przejdź do strony logowania i podaj swoje dane logowania.

### Dodawanie paczki

- Zalogowany użytkownik może dodać nową paczkę, wypełniając formularz dostępny na stronie dodawania paczki.

### Zarządzanie paczkami

- Zalogowany użytkownik może zarządzać swoimi paczkami, przeglądając listę paczek dostępnych na stronie zarządzania paczkami.
- Użytkownik może je usuwać.

### Obsługa kurierów

- Użytkownik może zarejestrować się jako kurier, podając swoje dane i numer telefonu.
- Kurierzy mogą logować się, wybierając odpowiednią opcję podczas logowania.
- Po zalogowaniu kurier może przeglądać dostępne paczki, przypisywać je do siebie i dostarczać je do odbiorców.
- Kurier moze zmieniac statusy paczek.
- Moze również przypisane paczki usuwac.

## Autorzy

- Dawid Faryński








