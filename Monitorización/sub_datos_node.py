#!/usr/bin/env python2.7
#coding=utf-8
import rospy #interfaz necesaria para progrma python con ROS 
from std_msgs.msg import Float32MultiArray #importar mensajes de tipo float32MultiArray para sensorica
import serial, time
import csv

def callback_valor(data): #funcion de calñback -> la funcion a la que va cuando recibe un mensaje(data) por el topico (datos)
    valores = data.data  #declaracion de variable que lleva los ID de sensorica
    tiempo=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('Coor x: ', valores[0]) #msg.data
    print('Coor y: ', valores[1]) #msg.data
    print('Coor z: ', valores[2]) #msg.data
    print('Temp: ', valores[3]) #msg.data
    print('HR: ', valores[4]) #msg.data
    print('TVOC: ', valores[5]) #msg.data
    print('eCO2: ', valores[6]) #msg.data
    print('H2: ', valores[7]) #msg.data
    print('Ethanol: ', valores[8]) #msg.data
    print('Dist 1: ', valores[9]) #msg.data
    print('Dist 2: ', valores[10]) #msg.data
    print('Dist 3: ', valores[11]) #msg.data
    print('Dist 4: ', valores[12]) #msg.data
    print('Dist 5: ', valores[13]) #msg.data
    with open('datos.csv', 'a') as file:
	writer = csv.writer(file)
	writer.writerow([valores[3], valores[4], valores[5], valores[6], valores[7], valores[8], valores[9], valores[10],valores[11],valores[12], valores[13],tiempo])

    #print('archivo')

def sub_datos():  #funcion de iniciacion nodo subscriptor 
    rospy.init_node('sub_datos', anonymous = True) #iniciacion de nodo subscriptor 
    rospy.Subscriber('valores', Float32MultiArray, callback_valor) #crea la suscripcion al tópico valores
    #print('estoy en el nodo')
    rospy.spin()  #el nodo se queda dormido siempre que este el progrma ejecuatndose


if __name__== '__main__':
    sub_datos() 

