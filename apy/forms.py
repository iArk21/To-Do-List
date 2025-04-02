from django.forms import ModelForm
from .models import Apy

class ApyForm(ModelForm):
    class Meta:
        model = Apy
        fields = ['titulo', 'descripcion', 'importancia']
