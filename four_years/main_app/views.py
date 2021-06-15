from django.contrib import auth
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from .models import ApplicationForm


def index(request):
    return render(request, 'index.html', {'user': auth.get_user(request)})


def logout(request):
    template_name = 'logout.html'
    user = auth.get_user(request)
    if user.is_authenticated:
        auth.logout(request)
        return render(request, template_name, {'user': user})
    else:
        return redirect('main_app:index')


class AuthView(View):
    template_name = 'auth.html'
    form_class = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        if auth.get_user(request).is_authenticated:
            return redirect('main_app:index')
        else:
            form = self.form_class(initial={'key': 'value'})
            context = {'form': form}
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main_app:index')
            else:
                #TODO: Вернуть что пароль или логин неправильный
                pass
        return render(request, self.template_name, {'form': form})


class ApplicationView(View):
    template_name = 'application.html'

    def get(self, request, *args, **kwargs):
        pass


class AccountView(View):
    template_name = 'account.html'

    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if user.is_authenticated:
            try:
                application = ApplicationForm.objects.get(id_user=user.pk)
            except ApplicationForm.DoesNotExist:
                application = None
            context = {'application': application}
            return render(request, self.template_name, context)
        else:
            return redirect('main_app:index')


class RegistrationView(View):
    template_name = 'registration.html'
    form_class = CustomUserCreationForm

    def get(self, request):
        form = self.form_class(initial={'key': 'value'})
        context = {'form': form}
        print(form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            login(request, user)
            print('DONE!')
            return redirect('main_app:index')
        return render(request, self.template_name, {'form': form})

