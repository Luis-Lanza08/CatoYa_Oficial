import funciones # funciones encapsuladas
import numpy as np
import time
import cv2 as cv
from smbus import SMBus
# i2c
adress = 0x30 # direccion de i2c
registro = 0x00 

capture = cv.VideoCapture(0) # Leer webcam
constante = 1 # valor que determina el peso del error
i = 0 # valor integral
p_anterior = 0 # error anterior
control = 0 #

control_err = 0

fila_blancos = 450
while True:
    isTrue, frame = capture.read() # leer frames
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # convertir a escala de grises
    #cv.imshow('Gray', gray) # mostrar frame
    altura = frame.shape[0]
    anchura = frame.shape[1]
    threshold, thresh_inv = cv.threshold(gray, 190, 255, cv.THRESH_BINARY_INV ) #Binarizar imagen
    thresh_inv = cv.cvtColor(thresh_inv, cv.COLOR_GRAY2RGB) #Volver a convetir a color para poder ver la lineas se utiliza el inverso para que los negros se hagan blancos
    thresh_inv = cv.bitwise_not(thresh_inv)
    blancosEnFila = thresh_inv[fila_blancos].astype(np.int32) # detectar blancos en una fila
    x = np.arange(len(blancosEnFila)) # leer tamanio del array
    
    ## detectar el camino 
    if(255 in blancosEnFila):  ## si detecta blanco
        bordes = np.where(blancosEnFila == 255)[0]  # detectar bordes del camino


        cv.line(thresh_inv, (int(anchura/2),0), (int(anchura/2),int(altura)),(255,0,0), thickness=1) # graficar recta al centro de la imagen

        max = np.amax(bordes) # valor maximo
        min = np.amin(bordes) # valor minimo
        medio = (min+max)//2 # detectar el centro del camino


        final = thresh_inv.copy()

        cv.line(final,(0,fila_blancos), (1000,fila_blancos), (0,0,255), thickness=1) # recta para detectar blancos
        cv.line(final, (min,0), (min,500),(0,255,0), thickness=1) # graficar recta en lacalle
        cv.line(final, (max,0), (max,500),(0,255,0), thickness=1) # graficar recta en la calle
        cv.line(final,(medio,0), (medio,500),(0,255,0), thickness=1) # graficar recta en el centro de la calle
        cv.putText(final, str(control_err), (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), thickness = 1)
        cv.imshow('detectar', final)

        # PID
        kp = 1
        ki = 0.5
        kd = 0.01
    
        control_err = int(funciones.pid_control(x,medio,p_anterior,i, kp, ki, kd))  # calcula el error por medio de un control PID
		
        rango = 400
        rango_nuevo = 254	

        control_err = funciones.convertir_rango(control_err,-rango,rango,-rango_nuevo, rango_nuevo)   # nomraliza los valores a rangos de -254 a 254 
        funciones.comunicacion_i2c(adress, control_err)
        funciones.enviar_dato(funciones.pid_control(x,medio,p_anterior,i, kp, ki, kd ))
        print(control_err)


    else: # si no detecta blanco solo graficar imagen
        cv.imshow('detectar', thresh_inv)

    if cv.waitKey(50) & 0xFF== ord('d'):   # detener video con tecla 'd' y mostrar un frame cada 20 ms
        break
capture.release()
cv.destroyAllWindows()

