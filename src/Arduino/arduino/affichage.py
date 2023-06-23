import serial
import time

def receive_data():
    # Configurer la communication série
    ser = serial.Serial('COM3', 9600) 

    # Créer un tableau 3x3 pour stocker les données
    data_array = [[0] * 3 for _ in range(3)]

    while True:
        if ser.in_waiting > 0:
            # Lire les données série
            data = ser.readline().decode().rstrip()
            
            # Extraire les valeurs individuelles du message
            values = data.split(';')
            
            for value in values:
                # Vérifier si la ligne de données contient les quatre éléments attendus
                if ',' in value:
                    # Extraire les indices, l'état et l'équipe de chaque case
                    i, j, etat, equipe = value.split(',')
                    try:
                        i = int(i)
                        j = int(j)
                        etat = int(etat)
                        equipe = int(equipe)
                        
                        # Vérifier si les indices sont dans la plage valide (0-2)
                        if 0 <= i < 3 and 0 <= j < 3:
                            # Stocker l'état et l'équipe dans le tableau
                            data_array[i][j] = (etat, equipe)
                    except ValueError:
                        # Ignorer les lignes de données incorrectes
                        pass

            # Afficher les données
            print(data_array)

        # Attendre une petite pause entre les lectures
        time.sleep(0.3)

receive_data()

