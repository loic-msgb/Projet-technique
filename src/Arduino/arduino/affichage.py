import serial
import tkinter as tk
import threading

# Définir les paramètres de communication série
port = 'COM3'  # Remplacer par le port série approprié
baudrate = 9600  # Assurer que cela correspond à la vitesse série définie dans le code Arduino

# Créer la fenêtre principale de l'interface graphique
window = tk.Tk()
window.title("MorpionGéant")

# Créer une grille pour représenter le plateau de morpion
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

# Créer des boutons pour représenter les cases du morpion
buttons = [[tk.Button(window, width=10, height=5, font=('Arial', 20, 'bold'), bg='white') for _ in range(3)] for _ in range(3)]

# Placer les boutons dans la grille
for i in range(3):
    for j in range(3):
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

# Ouvrir la connexion série
ser = serial.Serial(port, baudrate, timeout=1)

# Variable pour indiquer si le jeu est en pause
game_paused = False

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
            i = int(case_info_parts[0])
            j = int(case_info_parts[1])
            etat = int(case_info_parts[2])
            equipe = int(case_info_parts[3])

            # Mettre à jour l'état de la case sur le plateau de morpion
            board[i][j] = equipe
            buttons[i][j].config(text=str(equipe), state=tk.DISABLED)
            if equipe == 1:
                buttons[i][j].config(bg='red')
            elif equipe == 2:
                buttons[i][j].config(bg='blue')

    # Vérifier si une équipe a gagné
    winner = check_winner()
    if winner:
        display_winner(winner)
        pause_game()

# Fonction pour vérifier s'il y a un gagnant
def check_winner():
    # Vérifier les lignes
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]

    # Vérifier les colonnes
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != None:
            return board[0][j]

    # Vérifier les diagonales
    if (board[0][0] == board[1][1] == board[2][2] != None) or (board[2][0] == board[1][1] == board[0][2] != None):
        return board[1][1]

    # Aucun gagnant
    return None

# Fonction pour afficher le message de victoire
def display_winner(winner):
    # Rendre les boutons transparents
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)
            buttons[i][j].config(bg=buttons[i][j].cget('bg'), relief=tk.SUNKEN)

    # Afficher le message de victoire
    if winner == 1:
        message = "Victoire de l'équipe rouge !"
    elif winner == 2:
        message = "Victoire de l'équipe bleue !"
    else:
        message = "Match nul !"
    label_winner = tk.Label(window, text=message, font=('Arial', 20, 'bold'), bg='white')
    label_winner.grid(row=3, columnspan=3)

    # Ajouter le bouton "Nouvelle partie"
    button_new_game = tk.Button(window, text="Nouvelle partie", font=('Arial', 12, 'bold'), bg='green', fg='white', command=new_game)
    button_new_game.grid(row=4, columnspan=3, pady=10)

# Fonction pour mettre en pause le jeu
def pause_game():
    global game_paused
    game_paused = True

# Fonction pour relancer une nouvelle partie
def new_game():
    global game_paused
    game_paused = False

    # Supprimer le message de victoire et le bouton "Nouvelle partie"
    for widget in window.grid_slaves():
        if isinstance(widget, tk.Label) and widget.cget('text') != '':
            widget.grid_forget()
        if isinstance(widget, tk.Button) and widget.cget('text') == 'Nouvelle partie':
            widget.grid_forget()

    # Réinitialiser le plateau de morpion
    for i in range(3):
        for j in range(3):
            board[i][j] = None
            buttons[i][j].config(text="", state=tk.NORMAL, bg='white')

# Fonction pour lire les données série et mettre à jour l'interface
def read_serial():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()  # Lire une ligne de données série et décoder en tant que chaîne de caractères
            if data and not game_paused:
                update_case_state(data)
        window.update()

# Démarrer la collecte des données en temps réel dans un thread séparé
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# Définir les options d'espacement des widgets dans la grille
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Démarrer la boucle principale de l'interface graphique
window.mainloop()

# Fermer la connexion série
ser.close()
