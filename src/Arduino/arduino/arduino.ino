#include "Case.h"
#include "fonctions.h"

// Définir les seuils de détection de la lumière
// <200 = lumière torche du telephone
const int valeurMaxLumiere = 200;
// <230 = lumière du jour
const int valeurLumiereJour = 230;
// <450 = lumière plexiglass
const int valeurLumierePlexiMax = 450;
// >700 = lumière minimunm Carton
const int valeurLumiereCartonMin = 700;

Case cases[3][3] = {
  {Case(A0, 13), Case(A1, 12), Case(A2, 11)},
  {Case(A3, 10), Case(A4, 9), Case(A5, 8)},
  {Case(A5, 7), Case(A5, 6), Case(A5, 5)}
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (size_t i = 0; i < 3; i++)
  {
    for (size_t j = 0; j < 3; j++)
    {
      pinMode(cases[i][j].pinLed, OUTPUT);
    }
  }

}

void loop() {
  // Mettez votre code principal ici, à exécuter en boucle :

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      int valeurAnalogique = analogRead(cases[i][j].pinCapteurLumiere);
      
      if (valeurAnalogique <= valeurLumiereJour) {
        cases[i][j].liberer();
        digitalWrite(cases[i][j].pinLed, LOW);
      }
      else if (valeurAnalogique <= valeurLumierePlexiMax) {
        cases[i][j].occuper(2);
        digitalWrite(cases[i][j].pinLed, HIGH);
      }
      else if (valeurAnalogique >= valeurLumiereCartonMin) {
        cases[i][j].occuper(1);
        digitalWrite(cases[i][j].pinLed, HIGH);
      } 

      // Afficher le numéro de la case
      Serial.print("Case [");
      Serial.print(i);
      Serial.print("][");
      Serial.print(j);
      Serial.println("]");

      // Afficher la valeur analogique
      Serial.print("Valeur analogique : ");
      Serial.println(valeurAnalogique);
      // Afficher l'état de la case
      Serial.print("Etat : ");
      Serial.println(cases[i][j].etat);
      // Afficher l'équipe de la case
      Serial.print("Equipe : ");
      Serial.println(cases[i][j].equipe);
      Serial.println();



      delay(2000);
    }
  }
}
