"""
URL configuration for kurier_tech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from kurier_app.views import RegistrationView, LoginView, HomeView, WelcomePageView, CreatePackageView, PackListView, \
    DeletePackageView, CourierRegView, CourierLoginView, CourierListView, CourierPack, MoveToMyPackagesView, \
    RemovePackageView, ChangeStatusView


class ChangePackageStatusView:
    pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WelcomePageView.as_view()),
    path('Rejestracja/', RegistrationView.as_view(), name='Rejestracja'),
    path('Login/', LoginView.as_view(), name='Login'),
    path('Home/', HomeView.as_view(), name='home'),
    path('Tworzenie_paczki/', CreatePackageView.as_view(), name='Tworzenie_paczki'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('Pack_list/', PackListView.as_view(), name='Pack_list'),
    path('usun_paczke/<int:package_id>/', DeletePackageView.as_view(), name='usun_paczke'),
    path('rejestracja_kuriera/', CourierRegView.as_view(), name='courier_registration'),
    path('logowanie_kuriera/', CourierLoginView.as_view(), name='courier_login'),
    path('panel_kuriera/', CourierListView.as_view(), name='Courier_List'),
    path('Moje_paczki/', CourierPack.as_view(), name='Courier_pack'),
    path('move_to_my_packages/<int:package_id>/', MoveToMyPackagesView.as_view(), name='przenies_paczke'),
    path('usun_paczke/<int:package_id>/', RemovePackageView.as_view(), name='Remove_Package'),
    path('change_package_status/<int:package_id>/', ChangeStatusView.as_view(), name='Change_Package_Status'),

]



