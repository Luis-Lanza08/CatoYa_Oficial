import numpy as np
import time
from smbus import SMBus

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

def comunicacion_i2c(adress,error):
    bus = SMBus(1)
    if(error < 0):      # valor negativo
        registro = 0x00 # si registro es 0 el numero es negativo
        error_abs = error * (-1) # valor absoluto
        valor_bytes = [(error_abs >> 8) & 0xFF, error_abs & 0xFF] # dividir en 3 bytes
        bus.write_i2c_block_data(adress, registro, valor_bytes) #enviar a arduino por i2c
    elif(error >= 0): # valor positivo
        registro = 0x01 # si registro es 1 el numero es positivo
        valor_bytes = [(error >> 8) & 0xFF, error & 0xFF] #dividir en 3 bytes
        bus.write_i2c_block_data(adress, registro, valor_bytes) # enviar a arduino i2c

