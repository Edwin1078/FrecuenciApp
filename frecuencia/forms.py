# generador_tabla/forms.py
from django import forms

class NumeroFilasForm(forms.Form):
    num_filas = forms.IntegerField(label='Número de filas', min_value=1)

class IntervaloFrecuenciaForm(forms.Form):
    intervalos = forms.CharField(label='Intervalos (formato: num1,num2; num1,num2; ...)', max_length=500)
    frecuencias = forms.CharField(label='Frecuencias (separadas por comas)', max_length=100)