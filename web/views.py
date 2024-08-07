from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactFormForm, FlanOfferForm
from .models import Flan, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.urls import reverse
from .forms import RegisterForm
# Create your views here.
def indice(request):
    flanes = Flan.objects.all()    
    flanes_publicos = Flan.objects.filter(is_private=False)    
    return render(request, 'index.html', {'flanes_publicos': flanes_publicos} )

def acerca(request):
    return render(request, 'about.html', {} )

@login_required
def bienvenido(request):
    flanes_privados = Flan.objects.filter(is_private = True)
    for flan in flanes_privados:
        flan.discounted_price = int(flan.price - (flan.price * flan.actual_offer / 100))
    return render(request, 'wellcome.html', {'flanes_privados': flanes_privados} )

# Manejo del cierre se Sesion
def logout(request):
    auth_logout(request)
    return redirect('/logout_done')
    
def logout_done(request):
    return render(request, 'registration/logout.html',{})

def contacto(request):
    if request.method =='POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/exito')
    else:
        form = ContactFormForm()
    return render(request, 'contacto.html', {'form': form})

def exito(request):
    return render(request, 'success.html', {})


def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bienvenido')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def admin_panel(request):
    if request.method == 'POST':
        form = FlanOfferForm(request.POST)
        if form.is_valid():
            actual_offer = form.cleaned_data['actual_offer']
            # Actualizar todos los objetos Flan con el nuevo descuento
            Flan.objects.all().update(actual_offer=actual_offer)
            return redirect('bienvenido')  # Redirige para evitar reenvíos de formularios
    else:
        form = FlanOfferForm()

    flan = Flan.objects.first()  # Obtiene el primer objeto Flan para mostrar la oferta actual
    return render(request, 'admin.html', {'form': form, 'dscto': flan.offer if flan else []})
