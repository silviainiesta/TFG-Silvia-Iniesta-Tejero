#!/usr/bin/env python2.7
#coding=utf-8
import rospy #interfaz necesaria para programar en Python con ROS 
from std_msgs.msg import Float32MultiArray #importar mensajes de tipo Float32MultiArray
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
import math
import tf
import time
import tf2_ros

def callback(data):
    valores = data.data  #declaracion de variable que lleva los ID de sensorica
    
    #Declaracion variables globales
    global x0, y0, z0, pub
    global time0, angulo0
    
    #Posicion en metros
    coorx = valores[0] / 1000
    coory = valores[1] / 1000
    coorz = valores[2] / 1000
    angulo = math.atan2((coory - y0), (coorx - x0)) 
    
    quat = tf.transformations.quaternion_from_euler(0,0,angulo) #giro en eje vertical

    tf_broadcaster_2 = tf2_ros.TransformBroadcaster()
    transform2=TransformStamped()
    transform2.header.stamp= rospy.Time.now()
    transform2.header.frame_id = 'map' #marco de referencia padre
    transform2.child_frame_id= 'base_link' #marco de referencia hijo

    transform2.transform.translation.x = x0 #traslacion en x
    transform2.transform.translation.y = y0 #traslacion en y
    transform2.transform.translation.z = z0 #traslacion en z

    transform2.transform.rotation.x = quat[0] #rotacion en x
    transform2.transform.rotation.y = quat[1] #rotacion en y
    transform2.transform.rotation.z = quat[2] #rotacion en z
    transform2.transform.rotation.w = quat[3] #rotacion en w
    
    print(transform2)

    tf_broadcaster_2.sendTransform(transform2) #publicacion por tf

    #Actualizacion de variables
    x0 = coorx
    y0 = coory
    z0 = coorz
  
def tf_pub_node():
    #Declaracion de variables globales
    global x0, y0, z0, pub
    x0 = 0
    y0 = 0
    z0 = 0
    rospy.init_node('tf_pub_node', anonymous=True) #inicio del nodo 
    # Crear un suscriptor para otro tema
    rospy.Subscriber("valores", Float32MultiArray, callback)

   
    rate = rospy.Rate(10)  # Frecuencia del nodo
    rospy.spin()  #el nodo se queda dormido siempre que este el progrma ejecuatndose


if __name__ == '__main__':
    try:
        tf_pub_node()
    except rospy.ROSInterruptException:
        pass
