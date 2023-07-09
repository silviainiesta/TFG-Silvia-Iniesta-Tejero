# -*- coding: utf-8 -*-
"""
Created on May 24 17:57:07 2023

@author: Silvia Iniesta Tejero
"""

import cv2
import numpy as np

# Cargar modelo pre-entrenado
model = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Cargar archivo .txt con las clases
with open('yolov3.txt', 'r') as f:
    clases = [line.strip() for line in f.readlines()]

# Inicializar captura de webcam
cap = cv2.VideoCapture(0)

# Bucle para cada frame de la webcam
while True:
    # Leer los frames de la webcam
    ret, frame = cap.read()
    
    # Parar de procesar si no se pudo capturar el frame
    if not ret:
        break
    
    # Preparar imagen para la entrada a la red neuronal
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
    model.setInput(blob)
    
    # Paso de la imagen por el modelo
    output_layers = model.getUnconnectedOutLayersNames()
    outputs = model.forward(output_layers)
    
    # Detección de objetos y dibujo de cajas
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            fiabilidad = scores[class_id]
            if fiabilidad > 0.5:
                # Calcular los bordes y las coordenadas de la caja
                centro_x = int(detection[0] * frame.shape[1])
                centro_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                x = int(centro_x - width/2)
                y = int(centro_y - height/2)
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                
                # Añadir el texto de la clase a la detección (a la caja)
                etiqueta = f'{clases[class_id]}: {fiabilidad:.2f}'
                cv2.putText(frame, etiqueta, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Mostrar el video obtenido
    cv2.imshow('Webcam', frame)
    
    # Presionar 'q' para salir de la vista de video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
