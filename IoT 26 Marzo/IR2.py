# Conexiones:
# VCC -> 5V
# GND -> GND
# OUT -> GPIO 2 (Pin Físico 3)

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN) # GPIO 2 (DATOS I2C) es el Pin Físico 3

ledPin = 11 # Pin Físico 11, conexión LED
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)


while True:
	val = GPIO.input(3)
	#print (val)  	   # 1-> No hay objeto, 0-> Presencia de objeto
	if val == 1:
		IR = 1 # Indica que no hay objeto 
        GPIO.output(ledPin, GPIO.LOW) #APAGADO
	else:
		IR = 0 # Indica que hay objeto
        GPIO.output(ledPin, GPIO.HIGH) #ENCENDIDO
        LECT = 1
    GPIO.cleanup() ###
	
# Con el valor de IR luego se podrá hacer una condición que evalúe 
# su valor en un AND con el valor del Ultrasonido, luego de ser activados
# ambos sensores por el RFID.


# REFERENCIA: https://www.youtube.com/watch?v=qQTQcN44UWg
