import tkinter as tk
import serial
import threading
import time

# Configurer la communication série
ser = serial.Serial('COM3', 9600)

# Créer une fenêtre Tkinter
window = tk.Tk()
window.title("Affichage du tableau")

# Créer une étiquette pour le texte de bienvenue centré en haut de la fenêtre
welcome_label = tk.Label(window, text="Bienvenue dans le Morpion Géant", font=("Arial", 16))
welcome_label.pack(pady=20)

# Créer un cadre pour le plateau de morpion
board_frame = tk.Frame(window)
board_frame.pack()

# Créer une grille de boutons pour représenter le tableau
buttons = []
for i in range(3):
    row = []
    for j in range(3):
        button = tk.Button(board_frame, text=" ", width=10, height=5)
        button.grid(row=i, column=j, padx=5, pady=5)
        row.append(button)
    buttons.append(row)

def update_gui():
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
                        # Mettre à jour le texte du bouton correspondant avec le numéro de l'équipe
                        buttons[i][j].configure(text=str(equipe))
                except ValueError:
                    # Ignorer les lignes de données incorrectes
                    pass

    # Rafraîchir la fenêtre Tkinter
    window.update()

def update_gui_periodic():
    while True:
        update_gui()
        time.sleep(0.3)

# Lancer la mise à jour périodique de l'interface graphique dans un thread séparé
update_thread = threading.Thread(target=update_gui_periodic)
update_thread.start()

# Centrer la fenêtre au milieu de l'écran
window.eval('tk::PlaceWindow . center')

# Démarrer la boucle principale Tkinter
window.mainloop()
