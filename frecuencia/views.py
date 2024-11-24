# generador_tabla/views.py
from django.shortcuts import render, redirect
from .forms import NumeroFilasForm, IntervaloFrecuenciaForm

def ingresar_num_filas(request):
    if request.method == 'POST':
        form = NumeroFilasForm(request.POST)
        if form.is_valid():
            num_filas = form.cleaned_data['num_filas']
            return render(request, 'ingresar_datos.html', {
                'num_filas': num_filas,
                'form': IntervaloFrecuenciaForm(),
            })
    else:
        form = NumeroFilasForm()

    return render(request, 'index.html', {'form': form})

def generar_tabla(request):
    if request.method == 'POST':
        intervalos = request.POST.get('intervalos').split(';')
        frecuencias = list(map(int, request.POST.get('frecuencias').split(',')))

        tabla = []
        total_frecuencia_absoluta = 0
        total_xf = 0

        for i, intervalo in enumerate(intervalos):
            try:
                # Asegúrate de que el intervalo tenga el formato correcto
                num1, num2 = map(int, intervalo.split(','))
            except ValueError:
                # Maneja el error si el formato no es correcto
                return render(request, 'error.html', {
                    'mensaje': 'Formato de intervalo incorrecto. Asegúrate de usar el formato num1,num2; num1,num2; ...'
                })

            amplitud = num2 - num1
            marca_columna = (num1 + num2) / 2

            frecuencia_absoluta = frecuencias[i] if i < len(frecuencias) else 0
            frecuencia_acumulada = frecuencia_absoluta if i == 0 else tabla[i-1]['frecuencia_acumulada'] + frecuencia_absoluta
            xf = marca_columna * frecuencia_absoluta
            longitud_tabla = len(tabla)

            tabla.append({
                'interno': (num1, num2),
                'amplitud': amplitud,
                'marca_columna': marca_columna,
                'frecuencia_absoluta': frecuencia_absoluta,
                'frecuencia_acumulada': frecuencia_acumulada,
                'xf': xf,
            })

            total_frecuencia_absoluta += frecuencia_absoluta
            total_xf += xf

            med = total_xf / total_frecuencia_absoluta
            pos = total_frecuencia_absoluta / 2

            # Encontrar la fila donde frecuencia acumulada sea mayor o igual a pos
            fila_encontrada = 0
            for fila in tabla:
                if fila['frecuencia_acumulada'] >= pos:
                    fila_encontrada = fila
                    break  # Salimos del bucle al encontrar la primera coincidencia

            # Encontrar la fila anterior
            fila_anterior = 0
            if fila_encontrada:
                index_encontrado = tabla.index(fila_encontrada)
                if index_encontrado > 0:  # Asegúrate de que no sea la primera fila
                    fila_anterior = tabla[index_encontrado - 1]

            # Encontrar la fila posterior
            fila_posterior = 0
            if fila_encontrada:
                index_encontrado = tabla.index(fila_encontrada)
                if index_encontrado < len(tabla) - 1:  # Asegúrate de que no sea la última fila
                    fila_posterior = tabla[index_encontrado + 1]

            # Encontrar el valor máximo de frecuencia absoluta
            max_frecuencia = max(fila['frecuencia_absoluta'] for fila in tabla)

            # Filtrar las filas que tienen el valor máximo
            #filas_con_maxima_frecuencia = [fila for fila in tabla if fila['frecuencia_absoluta'] == max_frecuencia]

            # Encontrar la fila donde frecuencia absoluta sea el valor mayor
            fila_encontrada_m = 0
            for indice, fila in enumerate(tabla):
                if fila['frecuencia_absoluta'] == max_frecuencia:
                    fila_encontrada_m = fila
                    break  # Salimos del bucle al encontrar la primera coincidencia

            # Encontrar la fila anterior
            fila_anterior_m = 0
            if fila_encontrada_m:
                index_encontrado = tabla.index(fila_encontrada_m)
                if index_encontrado > 0:  # Asegúrate de que no sea la primera fila
                    fila_anterior_m = tabla[index_encontrado - 1]['frecuencia_absoluta'] 

                   

            # Encontrar la fila posterior
            fila_posterior_m = 0
            if fila_encontrada_m:
                index_encontrado = tabla.index(fila_encontrada_m)
                if index_encontrado < len(tabla) - 1:  # Asegúrate de que no sea la última fila
                    fila_posterior_m = tabla[index_encontrado + 1]['frecuencia_absoluta'] 


        return render(request, 'generar_tabla.html', {
            'tabla': tabla,
            'total_frecuencia_absoluta': total_frecuencia_absoluta,
            'total_xf': total_xf,
            'media' : med,
            'posicion': pos,
            'fila_encontrada': fila_encontrada,
            'fila_anterior': fila_anterior,
            'fila_posterior': fila_posterior,
            'frecuencia_max': max_frecuencia,
            'fila_encontrada_m': fila_encontrada_m,
            'fila_anterior_m': fila_anterior_m,
            'fila_posterior_m': fila_posterior_m,
        })

    return redirect('ingresar_num_filas')