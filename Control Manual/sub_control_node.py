#!/usr/bin/env python2.7
#coding=utf-8
import serial,time #importar puerto serie para la comunicacion con Arduino
import rospy  #importar la interfaz para programar con python en ROS
from std_msgs.msg import String #importar el tipo de mensaje string


def callback(data): 
   
    comando = data.data  #declaracion de variable que lleva el mensaje data 
    print(comando)
    if comando == 'W':      #Si se pulsa 'W' en robot avanza hacia delante
       print('Adelante')
    elif comando == 'S':    #Si se pulsa 'S' en robot avanza hacia detrás
       print('Atras')
    elif comando == 'D':    #Si se pulsa 'D' en robot gira a la derecha
       print('Derecha')
    elif comando == 'A':    #Si se pulsa 'A' en robot gira a la izquierda
       print('Izquierda')
    elif comando == 'E':    #Si se pulsa 'E' en robot hace una aproximación a la derecha
       print('Aproxderecha')
    elif comando == 'Q':    #Si se pulsa 'Q' en robot hace una paroximacion a la izquierda
       print('Aproxizquierda')
    elif comando == 'Z':    #Si se pulsa 'Z' en robot hace una aproximación a la izquierda y atrás
       print('Detrasizquierda')  
    elif comando == 'C':    #Si se pulsa 'C' en robot hace una aproximación a al derecha y atrás
       print('Detrasderecha') 
    elif comando == 'X':    #Si se pulsa 'X' en robot se para
       print('Parada')
    elif comando == 'T':    #Si se pulsa 'T' en robot avanza hacia delante más rápido
       print('Turbo')
    print(comando) #Imprimir comando por pantalla
    arduino=serial.Serial('/dev/ttyACM0', 9600) #conexión con Arduino por puerto serie
    time.sleep(2) #delay
    arduino.write(comando) #enviar comando por puerto serie
    arduino.close() #cerrar trasmisión con Arduino

def sub_control():  #funcion de iniciacion nodo subscriptor 
    rospy.init_node('sub_control', anonymous = True) #iniciacion de nodo subscriptor 
    rospy.Subscriber("comando", String, callback) #publico en el topico keyboard, mensaje tipo string y funcion que se incia cuando recibe mensaje callback
    #Se imprime el modo que se ejecuta	
    print("MODO MANUAL")
    rospy.spin()  #el nodo se queda dormido siempre que este el progrma ejecuatndose
    

if __name__== '__main__':
    sub_control() 
