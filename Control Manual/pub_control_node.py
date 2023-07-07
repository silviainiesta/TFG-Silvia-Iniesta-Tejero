#!/usr/bin/env python2.7
#coding=utf-8
import rospy #interfaz necesaria para progrma python con ROS 
from std_msgs.msg import String #importar mensajes de tipo string
def pub_control(): #defincion funcion de nodo publicador 
	rospy.init_node('pub_control', anonymous =True) #inicializacion del nodo publicador
	pub = rospy.Publisher('comando', String, queue_size =10) #nodo publicador en topico comando
	rate = rospy.Rate(100) #tiempo de la funcion 
	while not rospy.is_shutdown(): #mientras que este el nodo activo
		comando = raw_input('Introduce un comando de movimiento: ') #Input del teclado
		pub.publish(comando) #publicar comando por el tópico
		rate.sleep() #dormir hasta cumplir el tiempo de la funcion

if __name__=='__main__': 
    try:
        pub_control()
    except rospy.ROSInterruptException:
        pass
        
