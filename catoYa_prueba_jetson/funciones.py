import numpy as np
#import serial
import time

def pid_control(x, medio,p_anterior, i, kp, ki, kd):
    vector_zeros = np.zeros(len(x))
    p = np.zeros(len(x))
    pesos = np.linspace(-((x.shape[0]/2)-1) , (x.shape[0]/2), num = x.shape[0])
    vector_zeros[medio] = 1  # valor constante que varia la dimension del error
    
    # CALCULAR EL ERROR
    p = pesos * vector_zeros
    i = i + p[medio]
        
    if ((p[medio]*i)<0): # CORREGIR OVERSHOOTING
        i = 0
    d = p[medio] - p_anterior
    p_anterior = p[medio]
    error_final = kp*p[medio] + ki*i + kd*d    #control PID
    return error_final
    
def convertir_rango(numero, rango_minimo, rango_maximo, nuevo_minimo, nuevo_maximo):
    rango_actual = rango_maximo - rango_minimo
    nuevo_rango = nuevo_maximo - nuevo_minimo
    valor_normalizado = (numero - rango_minimo) / rango_actual
    nuevo_valor = nuevo_minimo + (valor_normalizado * nuevo_rango)
    return int(nuevo_valor)
