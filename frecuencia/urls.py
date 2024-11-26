from django.urls import path
from frecuencia.views import generar_tabla, ingresar_num_filas, hallar

urlpatterns = [
    path('', ingresar_num_filas, name='ingresar_num_filas'),
    path('generar_tabla/', generar_tabla, name='generar_tabla'),
    path('hallar/', hallar, name='hallar'),
]