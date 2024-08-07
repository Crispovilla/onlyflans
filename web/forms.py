from django import forms
from django.forms import ModelForm
from .models import ContactForm, Flan
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
class ContactFormForm(forms.Form):
    customer_email = forms.EmailField(label='Correo')
    customer_name = forms.CharField(max_length=64, label='Nombre')
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)

    class ContactFormModelForm(ModelForm):
        class Meta:
            model = ContactForm
            fields = ['customer_email', 'customer_name', 'message']

class FlanOfferForm(forms.ModelForm):
    class Meta:
        model = Flan
        fields = ['actual_offer'] 

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user