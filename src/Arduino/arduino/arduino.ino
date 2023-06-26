#include "Case.h"

// Définir les seuils de détection de la lumière
const int valeurMaxLumiere = 200;      // <200 = lumière torche du téléphone
const int valeurLumiereJour = 230;     // <230 = lumière du jour
const int valeurLumierePlexiMax = 450; // <450 = lumière plexiglass
const int valeurLumiereCartonMin = 700; // >700 = lumière minimum Carton

Case cases[3][3] = {
  {Case(A0, 13), Case(A1, 12), Case(A2, 11)},
  {Case(A3, 10), Case(A4, 9), Case(A5, 8)},
  {Case(A5, 7), Case(A5, 6), Case(A5, 5)}
};

void setup() {
  Serial.begin(9600);

  // Configurer les broches des LEDs pour chaque case
  for (size_t i = 0; i < 3; i++) {
    for (size_t j = 0; j < 3; j++) {
      pinMode(cases[i][j].pinLed, OUTPUT);
    }
  }
}

void loop() {
  String data; // Chaîne de caractères pour stocker les données sérialisées

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      int valeurAnalogique = analogRead(cases[i][j].pinCapteurLumiere);

      if (valeurAnalogique <= valeurLumiereJour) {
        cases[i][j].liberer();
        digitalWrite(cases[i][j].pinLed, HIGH);
      } else if (valeurAnalogique <= valeurLumierePlexiMax) {
        cases[i][j].occuper(2);
        digitalWrite(cases[i][j].pinLed, LOW);
      } else if (valeurAnalogique >= valeurLumiereCartonMin) {
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
  delay(1000); // Attendre 1 seconde avant de recommencer la boucle
}
