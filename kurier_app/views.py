from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from kurier_app import custom_auth_backends

from .models import Customer, Package
from .forms import RegistrationForm, PackageForm, CustomerLocationForm, RecipientForm, CourierRegistrationForm, \
    CourierLoginForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class WelcomePageView(View):
    def get(self,request):
        return render(request,'StronaGlowna.html')
class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'RejestracjaUzyt.html', {'form': form})


    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if password == password_confirm:
                print("Poprawne hasło i potwierdzenie hasła.")

                username = form.cleaned_data['username']
                user = User.objects.create_user(username=username, password=password)

                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                customer = Customer.objects.create(user=user, email=email, address=address)
                user.customer = customer
                user.save()
                print("Utworzono nowego użytkownika.")

                return redirect('Login')
            else:
                print("Błędne hasło lub potwierdzenie hasła.")

        else:
            print("Formularz niepoprawny:", form.errors)

        return render(request, 'RejestracjaUzyt.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'LoginUzyt.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Zalogowano pomyślnie.')
            return render(request,'Home.html')
        else:
            messages.error(request, 'Błędna nazwa użytkownika lub hasło.')
            return render(request, 'LoginUzyt.html')

class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'Home.html')





#
#
# class CreatePackageView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         package_form = PackageForm()
#         location_form = CustomerLocationForm()
#         recipient_form = RecipientForm()
#         return render(request, 'newpaq.html', {'package_form': package_form, 'recipient_form': recipient_form})
#
#
#     @method_decorator(login_required)
#     def post(self, request):
#         package_form = PackageForm(request.POST)
#         location_form = CustomerLocationForm(request.POST)
#         recipient_form = RecipientForm(request.POST)
#
#         if (package_form.is_valid() and location_form.is_valid()
#                 and recipient_form.is_valid() and hasattr(request.user, 'customer')):
#             package = package_form.save(commit=False)
#             package.customer = request.user.customer
#             package.save()
#
#             location = location_form.save(commit=False)
#             location.customer = request.user.customer
#             location.save()
#
#             recipient = recipient_form.save(commit=False)
#             recipient.customer = request.user.customer
#             recipient.save()
#
#             if not hasattr(request.user, 'customer'):
#                 customer = Customer.objects.create(user=request.user, email=request.user.email, address="")
#                 customer.save()
#
#             return redirect('package_list')
#
#         else:
#             print("Form errors:", package_form.errors, location_form.errors, recipient_form.errors)
#
#         return render(request, 'newpaq.html', {'package_form': package_form, 'recipient_form': recipient_form})

class CreatePackageView(View):

    def get(self, request):
        package_form = PackageForm()
        recipient_form = RecipientForm()
        return render(request, 'newpaq.html', {'package_form': package_form, 'recipient_form': recipient_form})

    def post(self, request):
        package_form = PackageForm(request.POST)
        recipient_form = RecipientForm(request.POST)
        if package_form.is_valid() and recipient_form.is_valid():

            recipient = recipient_form.save(commit=False)
            recipient.customer = request.user.customer
            recipient.save()  # Zapisuje nowego odbiorcę


            package = package_form.save(commit=False)
            package.customer = request.user.customer
            package.recipient = recipient  # Przypisuje odbiorcę do paczki
            package.save()
            return redirect('home')
        return render(request, 'newpaq.html', {'package_form': package_form, 'recipient_form': recipient_form})



class PackListView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user  # Pobierz zalogowanego użytkownika
        packages = Package.objects.filter(customer__user=user)  # Pobierz paczki przypisane do użytkownika

        context = {'user_packages': packages}
        return render(request, 'PackList.html', context)


class DeletePackageView(View):
    @method_decorator(login_required)
    def post(self, request, package_id):
        package = get_object_or_404(Package, id=package_id, customer=request.user.customer)
        package.delete()
        return redirect('Pack_list')

class CourierRegView(View):
    def get(self, request):
        form = CourierRegistrationForm()
        return render(request, 'RejestracjaKur.html', {'form': form})

    def post(self, request):
        form = CourierRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Courier_List')

class CourierLoginView(View):

    def get(self, request):
        form = CourierLoginForm()
        return render(request, 'LoginKur.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        user = authenticate(username=username, password=password, phone=phone)
        if user and user.is_courier:
            login(request, user)
            print("Użytkownik zalogowany:", user.username)
            return redirect('Courier_List')


        else:
            error_message = 'Błąd logowania'

            return render(request, 'LoginKur.html', {'error_message': error_message})

class CourierListView(View):

    @method_decorator(login_required)
    def get(self,request):
        if request.user.courier:
            packages = Package.objects.all()  # Pobierz wszystkie paczki
            return render(request, 'Panel_Kuriera.html', {'packages': packages})
        else:
            return redirect('home')
