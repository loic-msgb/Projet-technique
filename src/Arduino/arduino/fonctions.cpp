#include "fonctions.h"


bool verifierVictoire(Case cases[3][3]) {
  // Vérifier les lignes
  for (int i = 0; i < 3; i++) {
    if (cases[i][0].equipe != 0 && cases[i][0].equipe == cases[i][1].equipe && cases[i][0].equipe == cases[i][2].equipe) {
      return true;
    }
  }

  // Vérifier les colonnes
  for (int j = 0; j < 3; j++) {
    if (cases[0][j].equipe != 0 && cases[0][j].equipe == cases[1][j].equipe && cases[0][j].equipe == cases[2][j].equipe) {
      return true;
    }
  }

  // Vérifier les diagonales
  if (cases[0][0].equipe != 0 && cases[0][0].equipe == cases[1][1].equipe && cases[0][0].equipe == cases[2][2].equipe) {
    return true;
  }
  if (cases[0][2].equipe != 0 && cases[0][2].equipe == cases[1][1].equipe && cases[0][2].equipe == cases[2][0].equipe) {
    return true;
  }

  return false;
}