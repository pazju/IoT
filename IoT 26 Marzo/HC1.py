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
impor timeGPIO.setmode(GPIO.BCM)

channel_id = 1663439
write_key = '7ZC2UDRZY2HB8WF4'
read_key = 'RPUE21BD1P8KXZ7Q'




TRIG = 23
ECHO = 24
V = 34300 	# Velocidad del sonido 34300cm/s


	

print "Medición de la distancia en curso"

GPIO.setup (TRIG,GPIO.OUT)  # TRIGGER - SALIDA
GPIO.setup (ECHO,GPIO.IN)	# ECHO - ENTRADA

# Estabilización del sensor
GPIO.output (TRIG,False)	# TRIGGER - BAJO
print "Establización del sensor"
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
	print "Distancia: ", distancia, "cm" # Imprime la distancia

else:
	print "Fuera de Rango"
	
GPIO.cleanup() # Limpia los pines


def measure (channel):
	try:
		distance = distancia
		# WRITE
		response = channel.update({'field1': distance})
		
		# READ
		read = channel.get({})
		print ("Read", read)
	
	except:
		print ("Failed Connection")

if __name__ == "__main__":
	channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
	while True:
		measure (channel)
		# Cuenta gratis tiene un limite de api de 15 segundos
		time.sleep (15)



	

# REFERENCIA: https://www.youtube.com/watch?v=wDCLn3dSHGw
