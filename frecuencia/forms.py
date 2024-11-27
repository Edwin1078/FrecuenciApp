# generador_tabla/forms.py
from django import forms

class NumeroFilasForm(forms.Form):
    num_filas = forms.IntegerField(label='Número de filas', min_value=1)

class IntervaloFrecuenciaForm(forms.Form):
    DATOS_CHOICES = [
        ('Q', 'Quartil'),
        ('P', 'Percentil'),
        ('D', 'Decil'),
    ]
    intervalos = forms.CharField(label='Intervalos (formato: num1,num2; num1,num2; ...)', max_length=500)
    frecuencias = forms.CharField(label='Frecuencias (separadas por comas)', max_length=100)
    datos_f = forms.CharField(label='Escriba a que hace referencia los datos', max_length=50)

    datoH = forms.ChoiceField(label = 'Hallar',choices=DATOS_CHOICES )
    k = forms.IntegerField(label='Número', min_value=0, required=True )
    