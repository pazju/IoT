# Conexiones:
# VCC  -> 5V
# TRIG -> GPIO 23 (Pin Físico 16) (En este se transmite el tren de pulsos de activación, durante aprox 10us)

## USAR RESISTENCIAS PARA ESTOS PINES
# ECHO -> GPIO 24 (Pin Físico 18) (Aquí regresan los pulsos). Sale 1kohm de Echo, se conecta al pin y otra resistencia de 2kohm hacía GND
##

# GND  -> GND

# EN CONSOLA:
# sudo apt-get install python.rpi.gpio

# CHANNEL ID: 1663439
# API KEYS
# WRITE: 7ZC2UDRZY2HB8WF4
# READ: RPUE21BD1P8KXZ7Q 

import RPi.GPIO as GPIO
import time
import thingspeak
import requests # Libreria que permite realizar peticiones HTTP para poder enviar los datos a THINGSPEAK utilizando el método get que incluye la libreria
import paho.mqtt.publish as publish # Ya no se usa requests (HTTP), se utiliza MQTT

GPIO.setmode(GPIO.BCM)

channel_id = 1663439
write_key = '7ZC2UDRZY2HB8WF4'
read_key = 'RPUE21BD1P8KXZ7Q'

URL = 'https://api.thingspeak.com/update?api_key=7ZC2UDRZY2HB8WF4&field1='

### Métodos de conexión MQTT

useUnsecuredTCP = False			# TCP

useUnsecuredWebsockets = False	# WEBSOCKETS

useSSLWebsockets = True			# SSL - CONEXIÓN SEGURA (ENCRIPTADA)

mqttHost = "mqtt.thingspeak.com"

### Métodos de conexión MQTT

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

TRIG = 23
ECHO = 24
V = 34300 	# Velocidad del sonido 34300cm/s
GPIO.setup (TRIG,GPIO.OUT)  # TRIGGER - SALIDA
GPIO.setup (ECHO,GPIO.IN)	# ECHO - ENTRADA


print ("Medición de la distancia en curso")



# Estabilización del sensor
GPIO.output (TRIG,False)	# TRIGGER - BAJO
print ("Establización del sensor")
time.sleep (2) 				# 2 segundos de estabilización (Tiempo de lectura por segundo, puede ser menos)

def ultrasonido():

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

# # Comprobación rango distancia
# # En esta sección se pueden establecer los rangos para la medición. 
# # Las distancias en que se deben recargar las toallas, en las que se debe girar el motor, etc.
	# if distancia > 2 and distancia < 400:	 # Comprueba si distancia se encuentra dentro del rango de medición del sensor
		# print ("Distancia: ", distancia, "cm") # Imprime la distancia

	# else:
		# print ("Fuera de Rango")
	
	# GPIO.cleanup() # Limpia los pines
	
	
	return distancia 




while True:
	
	distancia = ultrasonido()
	print ("Distancia=", distancia)
	DisPayload = "field1=" + str(distancia)
	
	try: 
		publish.single(topic, payload=DisPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
	except (KeyboardINterrupt):
		break
	except:
		print ("Hubo un error en la publicación de los datos")
	
	
	
	
	
	



	

# REFERENCIA: https://www.youtube.com/watch?v=wDCLn3dSHGw

# MQTT THINGSPEAK -> https://nothans.com/thingspeak-tutorials/update-a-thingspeak-channel-using-mqtt-on-a-raspberry-pi
# https://www.youtube.com/watch?v=exMmLutRAR0
