#!/usr/bin/env python2.7
#coding=utf-8
import rospy #interfaz necesaria para programar en Python con ROS 
from std_msgs.msg import Float32MultiArray #importar mensajes de tipo Float32MultiArray
from sensor_msgs.msg import LaserScan
import math

def callback(data):
    valores = data.data  #declaracion de variable que lleva los ID de sensorica

    #Declaracion variables globales
    global scan_pub
    global frame_id
    pi = math.pi

    #Creacion del mensaje scan
    scan_msg=LaserScan()
    scan_msg.header.frame_id = 'base_link'
    scan_msg.angle_min = pi        # angulo inicio del escaneo [rad]
    scan_msg.angle_max = pi        # angulo final de escaneo [rad]
    scan_msg.angle_increment = math.radians(45)  # distancia angular entre medidas [rad]
    scan_msg.time_increment = 0.5  # tiempo entre medidas [seconds]
    scan_msg.scan_time = 1         # tiempo entre escaneos [seconds]
    scan_msg.range_min = 0.02      # rango minimo de medida [m]
    scan_msg.range_max = 150       # rango maximo de medida [m]
    scan_msg.ranges  = [valores[9], valores[10], valores[11], valores[12], valores[13]]       # datos tomados [m] 
    scan_pub.publish(scan_msg)  #publicacion del mensaje por el tópico scan
    
   
  
def scan_pub_node():
    global scan_pub
    rospy.init_node('scan_pub_node', anonymous=True) #Inicio del nodo
    # Crear un suscriptor para tópico scan
    rospy.Subscriber("valores", Float32MultiArray, callback)

    # Crear un publicador para un tema diferente
    scan_pub = rospy.Publisher('/scan',LaserScan, queue_size=10) #publicacion por el topico scan
    rate = rospy.Rate(1)  #frecuencia del nodo
    rospy.spin()  #el nodo se queda dormido siempre que este el progrma ejecuatndose

   
if __name__ == '__main__':
    try:
        pub_scan_node()
    except rospy.ROSInterruptException:
        pass
