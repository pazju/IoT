#EN TERMINAL:
# cd Desktop
# cd RFID-PRUEBA
# python3 rfid.py # SE EJECUTA EL CÓDIGO ESCRITO

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


# REFERENCIA: https://www.youtube.com/watch?v=Q99N0AdifgY
