from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactFormForm
from .models import Flan, ContactForm
# Create your views here.
def indice(request):
    flanes = Flan.objects.all()
    
    flanes_publicos = Flan.objects.filter(is_private=False)
    
    return render(request, 'index.html', {'flanes_publicos': flanes_publicos} )

def acerca(request):
    return render(request, 'about.html', {} )

def bienvenido(request):
    flanes_privados = Flan.objects.filter(is_private = True)
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
