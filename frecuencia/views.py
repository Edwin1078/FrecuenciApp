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
        dato_h = request.POST.get('datoH')
        datos_f = request.POST.get('datos_f')
        valor = 0
        texto = ""
        if dato_h == "Q":
            valor = 4
            texto = "Cuartil"
        elif dato_h == "D":
            valor = 10
            texto = "Decil"
        else:
            valor = 100
            texto = "Percentil"
        k = request.POST.get('k')
        k = int(k)

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
            marca_clase = (num1 + num2) / 2

            frecuencia_absoluta = frecuencias[i] if i < len(frecuencias) else 0
            frecuencia_acumulada = frecuencia_absoluta if i == 0 else tabla[i-1]['frecuencia_acumulada'] + frecuencia_absoluta
            xf = marca_clase * frecuencia_absoluta
            total_frecuencia_absoluta += frecuencia_absoluta
            total_xf += xf
            n = total_frecuencia_absoluta
            

            

            tabla.append({
                'intervalo': (num1, num2),
                'amplitud': amplitud,
                'marca_clase': marca_clase,
                'frecuencia_absoluta': frecuencia_absoluta,
                'frecuencia_acumulada': frecuencia_acumulada,
                'xf': xf,
            })

           
            med = total_xf / total_frecuencia_absoluta
            pos = total_frecuencia_absoluta / 2

           

            # Encontrar la fila donde frecuencia acumulada sea mayor o igual a pos
            fila_encontrada = 0
            for fila in tabla:
                if fila['frecuencia_acumulada'] >= pos:
                    fila_encontrada = fila
                    break  # Salimos del bucle al encontrar la primera coincidencia
            
            if fila_encontrada is not 0 and 'frecuencia_absoluta' in fila:
                fi = fila_encontrada['frecuencia_absoluta']
                a = fila_encontrada['amplitud']

            total_f_x_m = 0

            # Segundo bucle para calcular x - m
            for fila in tabla:
                x_m = fila['marca_clase'] - med  # Calcular x - m
                fila['x_m'] = x_m  # Almacenar x - m
                fila['x_m_squared'] = x_m ** 2  # Almacenar (x - m)^2
                fila['f_x_m'] = fila['frecuencia_absoluta'] * fila['x_m_squared']

                total_f_x_m += fila['f_x_m']
               

            # Encontrar la fila anterior
            fila_anterior = 0
            if fila_encontrada:
                index_encontrado = tabla.index(fila_encontrada)
                if index_encontrado > 0:  # Asegúrate de que no sea la primera fila
                    fila_anterior = tabla[index_encontrado - 1]
                    
            if fila_anterior is not 0 and 'frecuencia_acumulada' in fila_anterior:
                fi_1 = fila_anterior['frecuencia_acumulada']
                op1 = 2 * fi_1
                op2 = n - op1
                op3 = 2 * fi
                op4 = op2 * a
                op5 = li * op3
                op6 = op5 + op4
                r = op6/op3
                varianza_p = total_f_x_m / n
                desviacion_estandar_p = varianza_p ** 0.5
                n_1 = n - 1
                varianza_m = total_f_x_m / n_1
                desviacion_estandar_m = varianza_m ** 0.5

            pos_q = ( k * n ) / valor


            
            # Encontrar la fila donde frecuencia acumulada sea mayor o igual a pos_q
            fila_encontrada_q = 0
            for fila in tabla:
                if fila['frecuencia_acumulada'] >= pos_q:
                    fila_encontrada_q = fila
                    break  # Salimos del bucle al encontrar la primera coincidencia
            
            if fila_encontrada_q is not 0 and 'frecuencia_absoluta' in fila:
                fi_q = fila_encontrada_q['frecuencia_acumulada']
                a_q = fila_encontrada_q['amplitud']

            
            # Encontrar la fila anterior
            fila_anterior_q = 0
            if fila_encontrada_q:
                index_encontrado_q = tabla.index(fila_encontrada_q)
                if index_encontrado_q > 0:  # Asegúrate de que no sea la primera fila
                    fila_anterior_q = tabla[index_encontrado_q - 1]

            fi_1_q = 0

            if fila_anterior_q is not 0 and 'frecuencia_acumulada' in fila_anterior_q:
                fi_1_q = fila_anterior_q['frecuencia_acumulada']
                
                
                
            if fila_encontrada is not 0 and 'frecuencia_absoluta' in fila:
                li = fila_encontrada['intervalo'][0]
                ls = fila_encontrada['intervalo'][1]

            if fila_encontrada_q is not 0 and 'frecuencia_absoluta' in fila:
                li_q = fila_encontrada_q['intervalo'][0]
                ls_q = fila_encontrada_q['intervalo'][1]
            
            

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
            for intervalo, fila in enumerate(tabla):
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

            op_q1 = pos_q - fi_1_q
            op_q2 = fi_q - fi_1_q
            op_q3 = op_q1 / op_q2
            op_q4 = a * op_q3
            r_q = li_q + op_q4

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
            'fi_1': fi_1,
            'li': li,
            'ls': ls,
            'fi':fi,
            'n': n,
            'a': a,
            'op1': op1,
            'op2': op2,
            'op3': op3,
            'op4': op4,
            'op5': op5,
            'op6': op6,
            'r': r,
            'total_f_x_m': total_f_x_m,
            'varianza_p': varianza_p,
            'desviacion_estandar_p': desviacion_estandar_p,
            'varianza_m': varianza_m,
            'desviacion_estandar_m': desviacion_estandar_m,
            'dato_h': dato_h,
            'k': k,
            'valor': valor,
            'texto':texto,
            'pos_q': pos_q,
            'li_q': li_q,
            'a_q': a_q,
            'fi_q': fi_q,
            'fi_1_q':fi_1_q,
            'datos_f':datos_f,
            'dato_h':dato_h,
            'op_q1':op_q1,
            'op_q2':op_q2,
            'op_q3':op_q3,
            'op_q4':op_q4,
            'r_q':r_q,

        })

    return redirect('ingresar_num_filas')

