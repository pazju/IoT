import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 # Libreria que permite escribir y leer de forma sencilla en el RFID y entregar la información
import time
import thingspeak
import requests # Libreria que permite realizar peticiones HTTP para poder enviar los datos a THINGSPEAK utilizando el método get que incluye la libreria
import paho.mqtt.publish as publish # Ya no se usa requests (HTTP), se utiliza MQTT
import paho.mqtt.client as mqttClient
#import paho.mqtt.publish as publish
import sys
import os, urllib, urllib3

mqttHost = "mqtt3.thingspeak.com"
mqttPort = 1883
usr = "CysQMC4nHRwzFRMLLSIXKgU"		
pwd = "ZtlgrOK8bqfpGX1an/cSO09E"	
write_key = "NI2HXRHBR5Q93N7I"
channel_ID = "1751575"
channel=thingspeak.Channel(id=channel_ID, api_key=write_key)
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#IR
pin_IR=3 #En GPIO=2
#IR

#RFID
reader = SimpleMFRC522() 
# Conexiones:
# 3.3V -> 3.3v    (Pin Físico 1)
# RST  -> GPIO 25 (Pin Físico 22)
# GND  -> GND
# RQ   -> NADA
# MISO -> GPIO 9  (Pin Físico 21) (MISO)
# MOSI -> GPIO 10 (Pin Físico 19) (MOSI)
# SCK  -> GPIO 11 (Pin Físico 23) (SCLK)
# SDA  -> GPIO 8  (Pin Físico 24) (CE0) 
#RFID

#MOTOR DC
pin_DC=7
#MOTOR DC

# #LED1 - VERDE
pin_LED1=36

# #LED1

#LED2 - ROJO
pin_LED2=37

#LED2

#HC
TRIG = 16   #23
ECHO = 18 	#24
V = 34300 	# Velocidad del sonido 34300cm/s

#TOALLAS INICIALES
Toallas = 7
#
def ultrasonido():
	GPIO.setmode(GPIO.BOARD)#
	GPIO.setwarnings(False)#
	GPIO.setup (TRIG,GPIO.OUT)  # TRIGGER - SALIDA
	GPIO.setup (ECHO,GPIO.IN)	# ECHO - ENTRADA
	#print ("Medición de la distancia en curso")
	# Estabilización del sensor
	GPIO.output (TRIG,False)	# TRIGGER - BAJO
	#print ("Establización del sensor")
	time.sleep (0.5) 				# 0.5 segundos de estabilización (Tiempo de lectura por segundo, puede ser menos)	
	#HC
		
	# Envío señal de activación durante 10us
	GPIO.output (TRIG,True)		# TRIGGER - ALTO
	time.sleep(0.00001)			# Delay de 10us
	GPIO.output (TRIG,False)	# TRIGGER - BAJO
	
	# Obtención DELTA tiempo 
	while GPIO.input (ECHO) == 0: # Comprobación estado bajo ECHO
		pulse_start = time.time() # Guarda el tiempo transcurrido durante estado BAJO
		
	while GPIO.input (ECHO) == 1: # Comprobación estado alto ECHO
		pulse_end = time.time()   # Guarda el tiempo transcurrido durante estado ALTO
	
	t = pulse_end - pulse_start	  # Cálculo duración del pulso con el DELTA del tiempo
	
	# Cálculo distancia
	distancia = t * (V/2) 			# Duración se multiplica por 17150 cm/s para obtener distancia
	distancia = round (distancia,2) # Redondeo a dos decimales
	return distancia 

while True:
	
	try:
		#reader = SimpleMFRC522() 
		print("Ubique su carnet")
		id,delivery = reader.read()
		print (id)
		print ("Tome su toalla")
		#MOTOR DC
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)#
		GPIO.setup(pin_DC, GPIO.OUT)
		p = GPIO.PWM(pin_DC,207)
		p.start(0)
		try:	
			for i in range (40):
				p.ChangeDutyCycle(i)
				time.sleep(0.02)
			for i in range(1):
				p.ChangeDutyCycle(100-i)
				time.sleep(0.02)
		except KeyboardInterrupt:
				pass 
		p.stop()
		#MOTOR DC

		ACT = 1
	finally: 
		print()
		GPIO.cleanup() #Se limpian los pines GPIO

	Toallas-=1
	print("Toallas Disponibles: ", Toallas)
	if Toallas<=6:
		print ("Las Toallas se están agotando")
	
	while ACT == 1: 

		
		#IR
		
	
		GPIO.setmode(GPIO.BOARD)
		#GPIO.setwarnings(False)#
		GPIO.setup(pin_IR, GPIO.IN) # GPIO 2 (DATOS I2C) es el Pin Físico 3
		val = GPIO.input(pin_IR)
		GPIO.setup(pin_LED2, GPIO.OUT) #ROJO
		GPIO.setup(pin_LED1, GPIO.OUT) #VERDE
		# print (val)  	   # 1-> No hay objeto, 0-> Presencia de objeto
		toalla_dispensada=0
		if val == 1:
			IR = 1 # Indica que no hay objeto
			GPIO.output(pin_LED2, GPIO.HIGH) #ROJO ENCENDIDO
			GPIO.output(pin_LED1, GPIO.LOW) #VERDE APAGADO
			
		else:
			IR = 0 # Indica que hay objeto
			toalla_dispensada=1
			time.sleep(15) # Tiempo para lograr enviar a ThingSpeak
			ACT = 0
			GPIO.output(pin_LED1, GPIO.HIGH) #VERDE ENCENDIDO
			GPIO.output(pin_LED2, GPIO.LOW) #ROJO APAGADO
			
			#GPIO.cleanup()
				
		
		#IR
		
		

		distancia = ultrasonido()#0
		tPayload = "&field1=" + str(distancia) + "&field2=" + str(toalla_dispensada) + "&field3=" + str(Toallas)
		try:
		  channel.update({'field1': distancia,'field2': toalla_dispensada,'field3': Toallas})
		  print("Datos Enviados: "+tPayload)
		except:
		  print("Error enviando datos")


			


