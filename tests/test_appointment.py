import unittest
from datetime import date, time

from src.models.appointment import Appointment


class TestAppointment(unittest.TestCase):

    def setUp(self):
        self.rdv = Appointment(
            name="Jean Dupont",
            date=date(2026, 12, 15),
            description="Consultation médicale"
        )

    def test_creation_rendez_vous(self):
        self.assertEqual(self.rdv.name, "Jean Dupont")
        self.assertEqual(self.rdv.date, date(2026, 12, 15))
        self.assertEqual(
            self.rdv.description,
            "Consultation médicale"
        )

    def test_identifiant_initial(self):
        self.assertIsNone(self.rdv.id)

    def test_representation_textuelle(self):
        self.assertEqual(
        str(self.rdv),
        "Jean Dupont - 15/12/2026 à 09:00"
    )

    def test_nom_vide_interdit(self):
        with self.assertRaises(ValueError):
            self.rdv.name = "   "

    def test_date_invalide(self):
        with self.assertRaises(TypeError):
            self.rdv.date = "15/12/2026"

    def test_description_invalide(self):
        with self.assertRaises(TypeError):
            self.rdv.description = 123
    def test_heure_debut_par_defaut(self):
        self.assertEqual(self.rdv.start_time, time(9, 0))

    def test_duree_par_defaut(self):
        self.assertEqual(self.rdv.duration_minutes, 60)

    def test_calcul_heure_fin(self):
        self.assertEqual(self.rdv.end_time, time(10, 0))

    def test_duree_invalide(self):
        with self.assertRaises(ValueError):
            self.rdv.duration_minutes = 0

    def test_heure_invalide(self):
        with self.assertRaises(TypeError):
            self.rdv.start_time = "09:00"


if __name__ == "__main__":
    unittest.main()