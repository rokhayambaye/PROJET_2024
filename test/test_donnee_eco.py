import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ajouter le chemin du dossier contenant p.py pour l'import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bike/Base_des_donnees')))
from gestionnaire_donnees_eco import GestionnaireDonnees
import unittest
from unittest.mock import mock_open, patch


class TestGestionnaireDonnees(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"intensity": 10, "laneId": 1, "dateObserved": "2023-05-01T12:00:00Z", "location": {"coordinates": [3.0, 43.0]}, "id": 1, "type": "bike", "vehicleType": "bike", "reversedLane": false}')
    def test_lire_donnees(self, mock_file):
        # Instance de la classe à tester
        gestionnaire = GestionnaireDonneesEco()

        # Lecture des données
        resultat = gestionnaire.lire_donnees("fichier_test.json")
        
        # Vérifications
        self.assertEqual(resultat["intensity"], 10)
        self.assertEqual(resultat["laneId"], 1)
        self.assertEqual(resultat["type"], "bike")
        self.assertEqual(resultat["vehicleType"], "bike")
        self.assertEqual(resultat["location"]["coordinates"], [3.0, 43.0])

    @patch('base_des_donnees.gestionnaire_donnees_eco.requests.get')
    def test_telecharger_donnees(self, mock_get):
        # Simuler une réponse JSON de l'API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "intensity": 20, "type": "bike"}]

        # Instance de la classe à tester
        gestionnaire = GestionnaireDonneesEco()

        # Téléchargement des données
        resultat = gestionnaire.telecharger_donnees("https://api.fakeurl.com")

        # Vérifications
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]["id"], 1)
        self.assertEqual(resultat[0]["intensity"], 20)
        self.assertEqual(resultat[0]["type"], "bike")

if __name__ == '__main__':
    unittest.main()
