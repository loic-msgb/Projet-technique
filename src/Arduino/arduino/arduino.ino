#include "Case.h"
#include "fonctions.h"

// Définir les seuils de détection de la lumière
// <200 = lumière torche du téléphone
const int valeurMaxLumiere = 200;
// <230 = lumière du jour
const int valeurLumiereJour = 230;
// <450 = lumière plexiglass
const int valeurLumierePlexiMax = 450;
// >700 = lumière minimum Carton
const int valeurLumiereCartonMin = 700;

Case cases[3][3] = {
  {Case(A0, 13), Case(A1, 12), Case(A2, 11)},
  {Case(A3, 10), Case(A4, 9), Case(A5, 8)},
  {Case(A3, 7), Case(A3, 6), Case(A3, 5)}
};

bool jeuEnCours = false; // Variable pour contrôler l'exécution du jeu

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(11, OUTPUT);
  for (size_t i = 0; i < 3; i++) {
    for (size_t j = 0; j < 3; j++) {
      pinMode(cases[i][j].pinLed, OUTPUT);
    }
  }
}

void loop() {
  if (jeuEnCours) {
    // Code du jeu à exécuter uniquement si le jeu est en cours

    String data; // Chaîne de caractères pour stocker les données sérialisées

    for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
        int valeurAnalogique = analogRead(cases[i][j].pinCapteurLumiere);

        if (valeurAnalogique <= valeurLumiereJour) {
          cases[i][j].liberer();
          digitalWrite(cases[i][j].pinLed, HIGH);
        }
        else if (valeurAnalogique <= valeurLumierePlexiMax) {
          cases[i][j].occuper(2);
          digitalWrite(cases[i][j].pinLed, LOW);
        }
        else if (valeurAnalogique >= valeurLumiereCartonMin) {
          cases[i][j].occuper(1);
          digitalWrite(cases[i][j].pinLed, LOW);
        }

        // Ajouter les informations de la case à la chaîne de données
        data += String(i) + "," + String(j) + "," + String(cases[i][j].etat) + "," + String(cases[i][j].equipe) + ";";
      }
      delay(100);
    }

    // Envoyer les données sérialisées via la communication série
    Serial.println(data);
    // Effacer la chaîne de données pour la prochaine itération
    data = "";
  }
  else {
    // Attendre une instruction START pour démarrer le jeu
    while (Serial.available() > 0) {
      String instruction = Serial.readStringUntil('\n');
      if (instruction == "START") {
        jeuEnCours = true;
        break;
      }
    }
  }

  // Vérifier si l'instruction STOP a été reçue pour arrêter le jeu
  while (Serial.available() > 0) {
    String instruction = Serial.readStringUntil('\n');
    if (instruction == "STOP") {
      jeuEnCours = false;
      break;
    }
  }

  // Attendre 100ms avant de recommencer la boucle
  delay(100);
}