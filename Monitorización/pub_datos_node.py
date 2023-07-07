#!/usr/bin/env python2.7
#coding=utf-8
import rospy #interfaz necesaria para programar en Python con ROS 
from std_msgs.msg import Float32MultiArray #importar mensajes de tipo Float32MultiArray 
import serial, time

valor = [0,0,0,0,0,0,0,0,0,0]      #Se crea un vector vacío para almacenar los datos
sensor=''
global estado 
estado='no'
i=None
values=['0','0','0','0','0','0','0','0','0','0'] 

#-----------------------------------------DEFINICIÓN DE NODO PUBLICADOR------------------------------------------
def pub_datos(): #definición de la función de nodo publicador
    rospy.init_node('pub_datos', anonymous=True) #inicialización del nodo talker
    pub = rospy.Publisher('valores', Float32MultiArray, queue_size=10) #nodo publisher en el tópico 'valores'
    rate = rospy.Rate(100) #frecuencia de la función 
    
    while not rospy.is_shutdown(): #mientras que el nodo esté activo
        arduino = serial.Serial('/dev/ttyACM0', 115200) #Se inicia comunicación con el puerto serie de Arduino
        time.sleep(2)
        line = arduino.readline() #Leer los datos del puerto serie
        #print(line)
        
        if line.startswith('#1'): 
            cad_proc(line) 
	    #print(estado)
            if estado == 'permiso': #si se ha completado la función cad_proc()
                print(values)
		pub.publish(Float32MultiArray(data=[float(value)for value in values]))    #publicar valores por el tópico 
                time.sleep(1)
                #print('enviado')
                arduino.close() #Finalizamos la comunicación con Arduino
                rate.sleep() #dormir hasta cumplir el tiempo de la función	
        else:
            line = arduino.readline() #continua leyende el puerto serie

def cad_proc(cad): 
    global estado
    #print("\n\nInicio------------------------------------------------>" + cad)
    i = cad.find("@") #busca el principio de la cadena
    n = 0

    while i > 0:
        #Elimino primer #
        j = cad.find("#")
        cad = cad[j+1:]
        aux = cad

        #Cad avanza 1 bloque y aux se queda con el bloque anterior
        j = cad.find("#")
        if j < 0:
            j = cad.find("@") #Si entro en este condicional, he llegado al último bloque
        aux = aux[:j]
        cad = cad[j:]

        #Divido aux en ID y valor
        x = aux.find(":")
        sensor = aux[:x]
        value = aux[x+1:]
        values[int(sensor)-1] = value

        #info print
        print("sensor:" + sensor)
        print("value:" + value)
	
        i = cad.find("@")
        n = n + 1
	estado = 'permiso'
	#print(estado)
        

if __name__ == '__main__': 
    pub_datos()
