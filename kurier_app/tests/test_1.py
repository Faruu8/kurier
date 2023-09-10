import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from kurier_app.models import Customer, Package, Courier
from django.test import Client

from kurier_app.views import LoginView


@pytest.mark.django_db
def test_registration_view(client):
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'password_confirm': 'testpassword',
        'email': 'test@example.com',
        'address': 'Test Address',
    }

    response = client.post(reverse('Rejestracja'), data, follow=True)

    assert response.status_code == 200  # Sprawdź, czy widok zakończył się sukcesem
    assert User.objects.filter(username='testuser').exists()  # Sprawdź, czy użytkownik został utworzony
    assert Customer.objects.filter(email='test@example.com').exists()  # Sprawdź, czy klient został utworzony



@pytest.mark.django_db
def test_invalid_registration(client):
    # Dane do formularza rejestracji (hasła nie pasują)
    invalid_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'address': 'Test Address',
        'password': 'testpassword',
        'password_confirm': 'wrongpassword',  # Hasła się nie zgadzają
    }

    # Wysłanie żądania POST z danymi nieprawidłowej rejestracji
    response = client.post(reverse('Rejestracja'), data=invalid_data)

    # Sprawdzenie, czy odpowiedź ma kod 200 (rejestracja nie powiodła się)
    assert response.status_code == 200

    # Sprawdzenie, czy formularz rejestracji jest w kontekście
    assert 'form' in response.context

    # Sprawdzenie, czy formularz zawiera błędy walidacji
    form = response.context['form']
    assert form.errors

    # Sprawdzenie, czy użytkownik nie został utworzony
    assert not User.objects.filter(username=invalid_data['username']).exists()


@pytest.fixture
def user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.mark.django_db
def test_login_view_authenticated_user(user, client):
    # Logowanie użytkownika za pomocą klienta testowego
    response = client.post('/Login/', {'username': 'testuser', 'password': 'testpassword'})

    # Sprawdzenie, czy odpowiedź ma kod 200
    assert response.status_code == 200

    # Sprawdzenie, czy użytkownik jest zalogowany
    user = User.objects.get(username='testuser')
    assert user.is_authenticated


@pytest.mark.django_db
def test_login_view_invalid_credentials(client):
    # Próba logowania z błędnymi danymi za pomocą klienta testowego
    response = client.post('/Login/', {'username': 'wronguser', 'password': 'wrongpassword'})

    # Sprawdzenie, czy odpowiedź ma kod 200
    assert response.status_code == 200

    # Sprawdzenie, czy użytkownik nie jest zalogowany
    assert not response.wsgi_request.user.is_authenticated



@pytest.fixture
def logged_in_client():
    client = Client()
    user = User.objects.create(username='testuser')
    customer = Customer.objects.create(user=user, email='test@example.com', address='Test Address')
    user.customer = customer
    user.set_password('testpassword')
    user.save()
    client.login(username='testuser', password='testpassword')
    return client


@pytest.mark.django_db
def test_create_package(logged_in_client):
    package_data = {
        'weight': '5.0',
        'description': 'Test package',
    }
    recipient_data = {
        'name': 'LOLO',
        'address': 'WestStreat',
        'city': 'TextCity',
        'postal_code': '78-956',
    }

    # Wysłanie żądania POST z danymi tworzenia paczki
    response = logged_in_client.post(reverse('Tworzenie_paczki'), data={**package_data, **recipient_data})

    # Sprawdzenie, czy odpowiedź ma kod 302 (przekierowanie)
    assert response.status_code == 302

    # Sprawdzenie, czy paczka została utworzona
    assert Package.objects.filter(
        weight=package_data['weight'],
        description=package_data['description'],
        recipient__name=recipient_data['name'],
    ).exists()

@pytest.mark.django_db

def test_courier_registration(client):
    data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'phone': '123456789',  # Dodaj numer telefonu, który jest wymagany w formularzu
    }

    response = client.post(reverse('courier_registration'), data, follow=True)

    assert response.status_code == 200  # Sprawdź, czy widok zakończył się sukcesem
    assert User.objects.filter(username='testuser').exists()  # Sprawdź, czy użytkownik został utworzony
    assert Courier.objects.filter(user__username='testuser').exists()  # Sprawdź, czy kurier został utworzony



