
from .models import Apy
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ApyForm(forms.ModelForm):
    class Meta:
        model = Apy
        fields = ['titulo', 'descripcion', 'importancia', 'fecha']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un titulo...'
            }),


            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la descripcion....',
                'rows': 4
            }),

            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].input_formats = ['%Y-%m-%d']
        self.fields['importancia'].widget.attrs.update({'class': 'form-check-input'})


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(label="Nombre", required=True)
    apellido = forms.CharField(label="Apellido", required=True)
    identificacion = forms.CharField(label="Identificación", required=True)
    es_administrador = forms.BooleanField(required=False, label="¿Es administrador?")

    class Meta:
        model = CustomUser
        fields = ['username', 'nombre', 'apellido', 'email', 'identificacion', 'es_administrador', 'password1', 'password2' ]