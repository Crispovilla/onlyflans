from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ContactFormForm, FlanOfferForm, FlanForm
from .models import Flan, ContactForm, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import RegisterForm, ReviewForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User


# Vista Inicio
def indice(request):
    flanes = Flan.objects.all()    
    flanes_publicos = Flan.objects.filter(is_private=False)    
    return render(request, 'index.html', {'flanes_publicos': flanes_publicos} )

def acerca(request):
    resenas = Review.objects.select_related('user').all()
    return render(request, 'about.html', {'resenas': resenas} )

@login_required
def bienvenido(request):
    flanes_privados = Flan.objects.filter(is_private = True)
    for flan in flanes_privados:
        flan.discounted_price = int(flan.price - (flan.price * flan.actual_offer / 100))
    return render(request, 'wellcome.html', {'flanes_privados': flanes_privados} )

def resena(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Asignar el usuario autenticado directamente
            review.save()
            return redirect('/exito_resena')  # Redirigir después de guardar
    else:
        form = ReviewForm()
    return render(request, 'resena.html', {'form': form})

def exito_resena(request):
    return render(request, 'review_success.html')


# Manejo del cierre se Sesion
def logout(request):
    auth_logout(request)
    return redirect('/logout_done')
    
def logout_done(request):
    return render(request, 'registration/logout.html',{})

# Formulario de contacto
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

# Funcionalidad de Registro de Usuario
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

# Funcionalidad de Panel de Administracion
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
    flan = Flan.objects.first()
    flanes = Flan.objects.all()
    resenas = Review.objects.select_related('user').all()
    usuarios = User.objects.exclude(is_superuser=True)
    return render(request, 'admin.html', {
        'form': form, 
        'dscto': flan.offer if flan else [],
        'flanes': flanes,
        'resenas': resenas,
        'usuarios': usuarios,
        })
# Función para agregar un nuevo flan
def agregar_flan(request):
    if request.method == 'POST':
        form = FlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin')
        else:
            print(form.errors)
    else:
        form = FlanForm()    
    return render(request, 'agregar_flan.html', {'form': form})

# Función para editar un nuevo flan
def editar_flan(request, flan_id):
    flan = get_object_or_404(Flan, id=flan_id)
    print(flan) 
    if request.method == 'POST':
        form = FlanForm(request.POST, instance=flan)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = FlanForm(instance=flan)
        print(form)
    return render(request, 'editar_flan.html', {'form': form})
    
# Función para eliminar un nuevo flan
def eliminar_flan(request, flan_id):
    flan = get_object_or_404(Flan, id=flan_id)
    flan.delete()
    return redirect('admin')
    
def eliminar_resena(request, resena_id):
    resena = get_object_or_404(Review, id=resena_id)
    resena.delete()
    return redirect('admin')

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    return redirect('admin') 