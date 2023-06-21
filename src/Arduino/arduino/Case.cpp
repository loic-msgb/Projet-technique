#include "Case.h"

Case::Case(int pinCapteurLumiere, int pinLed) {
  this->pinCapteurLumiere = pinCapteurLumiere;
  this->pinLed = pinLed;
  this->etat = 0;
  this->equipe = 0;
}

void Case::occuper(int equipe) {
  this->etat = 1;
  this->equipe = equipe;
  digitalWrite(this->pinLed, HIGH);
}

void Case::liberer() {
  this->etat = 0;
  this->equipe = 0;
  digitalWrite(this->pinLed, LOW);
}