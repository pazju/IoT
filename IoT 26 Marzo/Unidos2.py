import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 # Libreria que permite escribir y leer de forma sencilla en el RFID y entregar la información
import time
import thingspeak
import requests # Libreria que permite realizar peticiones HTTP para poder enviar los datos a THINGSPEAK utilizando el método get que incluye la libreria
import paho.mqtt.publish as publish # Ya no se usa requests (HTTP), se utiliza MQTT

GPIO.setmode(GPIO.BOARD)


#IR
pin_IR=3 #En GPIO=2
#IR

#RFID
reader = SimpleMFRC522() 
#RFID

#HC
TRIG = 16   #23
ECHO = 18 	#24
V = 34300 	# Velocidad del sonido 34300cm/s


#THINGSPEAK
channel_id = '1663439'
write_key = '7ZC2UDRZY2HB8WF4'
read_key = 'RPUE21BD1P8KXZ7Q'

URL = 'https://api.thingspeak.com/update?api_key=7ZC2UDRZY2HB8WF4&field1='

### Métodos de conexión MQTT

useUnsecuredTCP = False			# TCP

useUnsecuredWebsockets = False	# WEBSOCKETS

useSSLWebsockets = True			# SSL - CONEXIÓN SEGURA (ENCRIPTADA)

mqttHost = "mqtt.thingspeak.com"



if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443


topic = "channels/" + channel_id + "/publish/" + write_key

### Métodos de conexión MQTT
#THINGSPEAK
while True:
	
	try:
		
		print("Ubique su carnet")
		id,delivery = reader.read()
		print (id)
		print ("Tome su toalla")
		ACT = 1
	finally: 
		GPIO.cleanup() #Se limpian los pines GPIO


	while ACT == 1: 
		GPIO.setmode(GPIO.BOARD)
		#IR
		
		GPIO.setup(pin_IR, GPIO.IN) # GPIO 2 (DATOS I2C) es el Pin Físico 3
		val = GPIO.input(pin_IR)
		# print (val)  	   # 1-> No hay objeto, 0-> Presencia de objeto
		if val == 1:
			IR = 1 # Indica que no hay objeto 
		else:
			IR = 0 # Indica que hay objeto
			ACT = 0
			
		#IR
		
		#HC
		
		def ultrasonido():
				
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
			#HC
			
			
		#THINGSPEAK
		distancia = ultrasonido()
		print ("Distancia=", distancia)
		DisPayload = "field1=" + str(distancia)
			
		try: 
			publish.single(topic, payload=DisPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
		except (KeyboardINterrupt):
			break
		except:
			print ("Hubo un error en la publicación de los datos")
			#THINGSPEAK
