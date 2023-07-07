#!/usr/bin/env python2.7
#coding=utf-8
import rospy #interfaz necesaria para programar en Python con ROS 
from std_msgs.msg import Float32MultiArray #importar mensajes de tipo Float32MultiArray
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
import math
import serial, time

def callback(data):
    valores = data.data  #declaracion de variable que lleva los ID de sensorica

    #Definición de variables globales
    global x0, y0, z0, pub
    global time0, angulo0
    global frame_id

    #Posicion en [m]
    coorx=valores[0] / 1000
    coory=valores[1] / 1000
    coorz=valores[2] / 1000
    current_time = rospy.Time.now()
    time = current_time.to_sec()  
    
    #ODOMETRIA
    odom = Odometry()
    odom.header.stamp = rospy.Time.now()
    odom.header.frame_id = 'map' #marco de referencia padre
    
    angulo = math.atan2((coory- y0), (coorx-x0)) #calculo del angulo entre posiciones consecutivas
    
    quat = tf.transformations.quaternion_from_euler(0,0,angulo) #giro en eje vertical
    odom.pose.pose = Pose(Point(coorx, coory, coorz), Quaternion(*quat))
    dist = math.sqrt((x0 - coorx)**2 + (y0 - coory)**2)   #no podría navegar hacia atras porque la distancia va a salir siempre positiva al ser una raíz
    
    delta_time = (time - time0) #incremento de tiempo entre posiciones consecutivas
    velocidad = dist/delta_time #velocidad linear
    vel_ang = (angulo - angulo0)/delta_time #velocidad angular 
    odom.child_frame_id='base_link' #marco de referencia hijo  
    odom.twist.twist=Twist(Vector3(velocidad,0,0),Vector3(0,0,vel_ang))

    pub.publish(odom) #publicacion por el tópico
    print(odom)

    #Actualizacion de variables 
    x0 = coorx
    y0 = coory
    z0 = coorz
    time0 = time
    angulo0 = angulo

def pub_odom_node():
    #Declaracion variables globales
    global x0, y0, z0, time0, angulo0, pub
    x0 = 0
    y0 = 0
    z0 = 0
    time0 = 0
    angulo0 = 0

    rospy.init_node('publisher_subscriber_node', anonymous=True) #incio del nodo
    # Crear un suscriptor para odom
    rospy.Subscriber("valores", Float32MultiArray, callback)

    # Crear un publicador para un tema diferente
    pub = rospy.Publisher('odom', Odometry, queue_size=10) #publicador en topico odom
    rate = rospy.Rate(5)  
    rospy.spin()  #el nodo se queda dormido siempre que este el progrma ejecuatndose


if __name__ == '__main__':
    try:
        pub_odom_node()
    except rospy.ROSInterruptException:
        pass
