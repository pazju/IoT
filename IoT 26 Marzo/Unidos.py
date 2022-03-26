########################################################################
# RFID
# Conexiones:
# 3.3V -> 3.3v    (Pin Físico 1)
# RST  -> GPIO 25 (Pin Físico 22)
# GND  -> GND
# RQ   -> NADA
# MISO -> GPIO 9  (Pin Físico 21) (MISO)
# MOSI -> GPIO 10 (Pin Físico 19) (MOSI)
# SCK  -> GPIO 11 (Pin Físico 23) (SCLK)
# SDA  -> GPIO 8  (Pin Físico 24) (CE0) 

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 # Libreria que permite escribir y leer de forma sencilla en el RFID y entregar la información

reader = SimpleMFRC522()

try:
	
	print("Ubique su carnet")
	id,delivery = reader.read()
	print (id)
	print ("Tome su toalla")
finally: 
	GPIO.cleanup() #Se limpian los pines GPIO

########################################################################
# Ultrasonido

# Conexiones:
# VCC  -> 5V
# TRIG -> GPIO 23 (Pin Físico 16) (En este se transmite el tren de pulsos de activación, durante aprox 10us)

## USAR RESISTENCIAS PARA ESTOS PINES
# ECHO -> GPIO 24 (Pin Físico 18) (Aquí regresan los pulsos). Sale 1kohm de Echo, se conecta al pin y otra resistencia de 2kohm hacía GND
##

# GND  -> GND

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
V = 34300 	# Velocidad del sonido 34300cm/s

print ("Medición de la distancia en curso")

GPIO.setup (TRIG,GPIO.OUT)  # TRIGGER - SALIDA
GPIO.setup (ECHO,GPIO.IN)	# ECHO - ENTRADA

# Estabilización del sensor
GPIO.output (TRIG,False)	# TRIGGER - BAJO
print ("Establización del sensor")
time.sleep (2) 				# 2 segundos de estabilización (Tiempo de lectura por segundo, puede ser menos)

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

# Comprobación rango distancia
# En esta sección se pueden establecer los rangos para la medición. 
# Las distancias en que se deben recargar las toallas, en las que se debe girar el motor, etc.
if distancia > 2 and distancia < 400:	 # Comprueba si distancia se encuentra dentro del rango de medición del sensor
	print ("Distancia: ", distancia, "cm") # Imprime la distancia

else:
	print ("Fuera de Rango")

GPIO.cleanup() # Limpia los pines

########################################################################
# IR

# Conexiones:
# VCC -> 5V
# GND -> GND
# OUT -> GPIO 2 (Pin Físico 3)

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.IN) # GPIO 2 (DATOS I2C) es el Pin Físico 3

while True:
	val = GPIO.input(3)
	print (val)  	   # 1-> No hay objeto, 0-> Presencia de objeto
	if val == 1:
		IR = 1 # Indica que no hay objeto 
	else:
		IR = 0 # Indica que hay objeto
		GPIO.cleanup()
		
########################################################################
