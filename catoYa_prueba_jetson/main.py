import funciones
import numpy as np
import serial
import cv2 as cv

capture = cv.VideoCapture(0) # Leer webcam
# width = 300
# height = 300
# capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
# capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)

constante = 1
i = 0
p_anterior = 0
control = 0


while True:
    isTrue, frame = capture.read() # leer frames
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # convertir a escala de grises
    #cv.imshow('Gray', gray) # mostrar frame
    altura = frame.shape[0]
    anchura = frame.shape[1]
    threshold, thresh_inv = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV ) #Binarizar imagen
    thresh_inv = cv.cvtColor(thresh_inv, cv.COLOR_GRAY2RGB) #Volver a convetir a color para poder ver la lineas se utiliza el inverso para que los negros se hagan blancos
    blancosEnFila = thresh_inv[100].astype(np.int32) # detectar blancos en una fila
    x = np.arange(len(blancosEnFila)) # leer tamanio del array

    ## detectar el camino 
    if(255 in blancosEnFila):  ## si detecta blanco
        bordes = np.where(blancosEnFila == 255)[0]  # detectar bordes del camino


        cv.line(thresh_inv, (int(anchura/2),0), (int(anchura/2),int(altura)),(255,0,0), thickness=1) # graficar recta al centro de la imagen

        max = np.amax(bordes) # valor maximo
        min = np.amin(bordes) # valor minimo
        medio = (min+max)//2 # detectar el centro del camino


        final = thresh_inv.copy()


        cv.line(final, (min,0), (min,500),(0,255,0), thickness=1) # graficar recta en lacalle
        cv.line(final, (max,0), (max,500),(0,255,0), thickness=1) # graficar recta en la calle
        cv.line(final,(medio,0), (medio,500),(0,255,0), thickness=1) # graficar recta en el centro de la calle
        cv.imshow('detectar', final)

        # PID
        kp = 2
        ki = 0.8
        kd = 0.3

        #print(funciones.pid_control(x,medio,p_anterior,i, kp, ki, kd ))
        funciones.enviar_dato(funciones.pid_control(x,medio,p_anterior,i, kp, ki, kd ))

    else: # si no detecta blanco solo graficar imagen
        cv.imshow('detectar', thresh_inv)

    if cv.waitKey(50) & 0xFF== ord('d'):   # detener video con tecla 'd' y mostrar un frame cada 20 ms
        break
capture.release()
cv.destroyAllWindows()


