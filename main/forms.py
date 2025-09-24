from django import forms
from .models import Visitante
from django.contrib.auth.models import User

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['nome', 'idade', 'email', 'cidade', 'estado']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sua idade'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sua cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UF'}),
        }


class RegistrationForm(forms.ModelForm):
    # Campo de senha
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    # Campo de confirmação de senha
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email') # Usaremos o email como username
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
        }

    def clean_password2(self):
        # Validação para garantir que as duas senhas são iguais
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não são iguais.')
        return cd['password2']

    def clean_email(self):
        # Validação para garantir que o email ainda não foi cadastrado
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email