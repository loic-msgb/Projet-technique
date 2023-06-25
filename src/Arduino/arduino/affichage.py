import serial
import tkinter as tk

# Définir les paramètres de communication série
port = 'COM3'  # Remplacez par le port série approprié
baudrate = 9600  # Assurez-vous que cela correspond à la vitesse série définie dans votre code Arduino

# Créer la fenêtre principale de l'interface graphique
window = tk.Tk()
window.title("MorpionGéant")

# Ajouter une étiquette pour le texte de bienvenue
welcome_label = tk.Label(window, text="Bienvenue sur notre MorpionGéant ! Amusez-vous bien", font=('Arial', 14))
welcome_label.grid(row=0, column=0, padx=10, pady=10)

# Créer une grille pour représenter le plateau de morpion
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

# Créer des boutons pour représenter les cases du morpion
buttons = [[tk.Button(window, width=10, height=5, font=('Arial', 20, 'bold'), bg='white') for _ in range(3)] for _ in range(3)]

# Placer les boutons dans la grille
for i in range(3):
    for j in range(3):
        buttons[i][j].grid(row=i+1, column=j, padx=5, pady=5)

# Ouvrir la connexion série
ser = serial.Serial(port, baudrate, timeout=1)

# Variable pour contrôler l'exécution du jeu
jeuEnCours = False

# Fonction pour mettre à jour l'état des cases
def update_case_state(data):
    # Nettoyer le plateau de morpion
    for i in range(3):
        for j in range(3):
            board[i][j] = None
            buttons[i][j].config(text="", state=tk.NORMAL, bg='white')

    # Analyser les données
    case_data = data.split(";")
    for case_info in case_data:
        case_info_parts = case_info.split(",")
        if len(case_info_parts) == 4:
            i, j, etat, equipe = map(int, case_info_parts)

            # Mettre à jour l'état de la case sur le plateau de morpion
            board[i][j] = equipe
            buttons[i][j].config(text=str(equipe), state=tk.DISABLED)
            buttons[i][j].config(bg='red' if equipe == 1 else 'blue')

            # Vérifier la victoire
            if check_victory(equipe):
                stop_game()

# Fonction pour vérifier la victoire
def check_victory(equipe):
    # Vérifier les lignes, les colonnes et les diagonales
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] == equipe) or \
           (board[0][i] == board[1][i] == board[2][i] == equipe):
            return True
    if (board[0][0] == board[1][1] == board[2][2] == equipe) or \
       (board[0][2] == board[1][1] == board[2][0] == equipe):
        return True
    return False

# Fonction pour arrêter le jeu
def stop_game():
    global jeuEnCours
    jeuEnCours = False
    ser.write(b'STOP\n')  # Envoyer l'instruction STOP via la communication série

# Fonction pour démarrer le jeu
def start_game():
    global jeuEnCours
    jeuEnCours = True
    ser.write(b'START\n')  # Envoyer l'instruction START via la communication série

# Créer les boutons de contrôle du jeu
start_button = tk.Button(window, text="Démarrer le jeu", font=('Arial', 12), command=start_game)
start_button.grid(row=4, column=0, padx=10, pady=5)

stop_button = tk.Button(window, text="Arrêter le jeu", font=('Arial', 12), command=stop_game)
stop_button.grid(row=4, column=1, padx=10, pady=5)

# Fonction pour lire les données série et mettre à jour l'interface
def read_serial():
    while True:
        data = ser.readline().decode().strip()  # Lire une ligne de données série et décoder en tant que chaîne de caractères
        if data:
            update_case_state(data)
        window.update()

# Démarrer la lecture des données série dans un thread séparé
import threading
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

# Définir les options d'espacement des widgets dans la grille
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(4, weight=1)

# Définir l'espacement entre les boutons de contrôle
window.grid_columnconfigure(0, minsize=150)
window.grid_columnconfigure(1, minsize=150)

# Démarrer la boucle principale de l'interface graphique
window.mainloop()

# Fermer la connexion série
ser.close()