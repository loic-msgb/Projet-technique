#ifndef Case_h
#define Case_h

#include <Arduino.h>

class Case {
  public:
    int pinCapteurLumiere;
    int pinLed;
    int etat;
    int equipe;

    Case(int pinCapteurLumiere, int pinLed);

    void occuper(int equipe);
    void liberer();
};

#endif