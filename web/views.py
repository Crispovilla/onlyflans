from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactFormForm, FlanOfferForm
from .models import Flan, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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
            # Suponiendo que quieres actualizar el primer Flan en la base de datos
            flan = Flan.objects.first()  # Puedes ajustar esto para seleccionar el Flan adecuado
            flan.offer = form.cleaned_data['offer']
            flan.save()
            return redirect('admin_panel')  # Redirige para evitar reenvíos de formularios
    else:
        form = FlanOfferForm()

    flan = Flan.objects.first()  # Obtiene el primer objeto Flan para mostrar la oferta actual
    return render(request, 'admin.html', {'form': form, 'dscto': flan.offer})
