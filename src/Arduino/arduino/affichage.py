import serial
import time

def receive_data():
    # Configurer la communication série
    ser = serial.Serial('COM3', 9600) 

    while True:
        if ser.in_waiting > 0:
            # Lire les données série
            data = ser.readline().decode().rstrip()
            
            # Afficher les données
            print(data)

        # Attendre une petite pause entre les lectures
        time.sleep(1)

receive_data()