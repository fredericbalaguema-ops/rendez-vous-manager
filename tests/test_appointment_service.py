import unittest
import tempfile

from pathlib import Path
from datetime import date, time, datetime

from src.models.appointment import Appointment
from src.database.appointment_repository import AppointmentRepository
from src.services.appointment_service import AppointmentService


class TestAppointmentService(unittest.TestCase):
    """Tests unitaires du service des rendez-vous."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "test.db"

        self.repository = AppointmentRepository(db_path)
        self.service = AppointmentService(self.repository)

    def tearDown(self):
        self.temp_dir.cleanup()

    def creer_rendez_vous(
        self,
        nom="Rendez-vous test",
        jour=None,
        heure=time(9, 0),
        duree=60,
        description="Description test"
    ):
        """Crée un rendez-vous pour les tests."""

        return Appointment(
            name=nom,
            date=jour or date(2026, 12, 10),
            description=description,
            start_time=heure,
            duration_minutes=duree
        )

    def test_creation_rendez_vous(self):
        appointment = self.creer_rendez_vous()

        resultat = self.service.create_appointment(appointment)

        self.assertIsNotNone(resultat.id)

    def test_detection_chevauchement(self):
        premier = self.creer_rendez_vous(
            heure=time(9, 0)
        )

        deuxieme = self.creer_rendez_vous(
            heure=time(9, 30)
        )

        self.service.create_appointment(premier)

        with self.assertRaises(ValueError):
            self.service.create_appointment(deuxieme)

    def test_rendez_vous_consecutifs_autorises(self):
        premier = self.creer_rendez_vous(
            heure=time(9, 0)
        )

        deuxieme = self.creer_rendez_vous(
            heure=time(10, 0)
        )

        self.service.create_appointment(premier)

        resultat = self.service.create_appointment(deuxieme)

        self.assertIsNotNone(resultat.id)

    def test_modification_sans_faux_conflit(self):
        appointment = self.creer_rendez_vous()

        self.service.create_appointment(appointment)

        appointment.name = "Rendez-vous modifié"

        resultat = self.service.update_appointment(appointment)

        self.assertEqual(
            resultat.name,
            "Rendez-vous modifié"
        )

    def test_suppression_rendez_vous(self):
        appointment = self.creer_rendez_vous()

        self.service.create_appointment(appointment)

        resultat = self.service.delete_appointment(
            appointment.id
        )

        self.assertTrue(resultat)

        self.assertIsNone(
            self.service.get_appointment(appointment.id)
        )

    def test_statut_rendez_vous_a_venir(self):
        appointment = self.creer_rendez_vous()

        instant = datetime(2026, 12, 10, 8, 0)

        statut = self.service.get_appointment_status(
            appointment,
            instant
        )

        self.assertEqual(statut, "À venir")

    def test_statut_rendez_vous_en_cours(self):
        appointment = self.creer_rendez_vous()

        instant = datetime(2026, 12, 10, 9, 30)

        statut = self.service.get_appointment_status(
            appointment,
            instant
        )

        self.assertEqual(statut, "En cours")

    def test_statut_rendez_vous_termine(self):
        appointment = self.creer_rendez_vous()

        instant = datetime(2026, 12, 10, 10, 0)

        statut = self.service.get_appointment_status(
            appointment,
            instant
        )

        self.assertEqual(statut, "Terminé")

    def test_recherche_rendez_vous(self):
        premier = self.creer_rendez_vous(
            nom="Consultation médicale"
        )

        deuxieme = self.creer_rendez_vous(
            nom="Réunion professionnelle",
            heure=time(11, 0)
        )

        self.service.create_appointment(premier)
        self.service.create_appointment(deuxieme)

        resultat = self.service.get_filtered_appointments(
            search_text="consultation"
        )

        self.assertEqual(len(resultat), 1)

        self.assertEqual(
            resultat[0].name,
            "Consultation médicale"
        )

    def test_statistiques_rendez_vous(self):
        """Vérifie le calcul des statistiques générales."""

        appointment = self.creer_rendez_vous(
            jour=date.today(),
            heure=time(12, 0),
            duree=60
        )

        self.service.create_appointment(appointment)

        statistiques = self.service.get_statistics()

        self.assertEqual(statistiques["total"], 1)

        total_statuts = (
            statistiques["upcoming"]
            + statistiques["ongoing"]
            + statistiques["completed"]
        )

        self.assertEqual(total_statuts, 1)
if __name__ == "__main__":
    unittest.main()