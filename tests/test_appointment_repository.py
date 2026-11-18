import unittest
import tempfile
from datetime import date, time
from pathlib import Path

from src.models.appointment import Appointment
from src.database.appointment_repository import AppointmentRepository


class TestAppointmentRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "test.db"
        self.repository = AppointmentRepository(db_path)

        self.rdv = Appointment(
            name="Jean Dupont",
            date=date(2026, 12, 15),
            description="Consultation"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ajout_rendez_vous(self):
        rdv = self.repository.add(self.rdv)
        self.assertIsNotNone(rdv.id)

    def test_recuperation_rendez_vous(self):
        rdv = self.repository.add(self.rdv)
        resultat = self.repository.get_by_id(rdv.id)

        self.assertEqual(resultat.name, "Jean Dupont")
        self.assertEqual(resultat.date, date(2026, 12, 15))

    def test_modification_rendez_vous(self):
        rdv = self.repository.add(self.rdv)
        rdv.name = "Paul Martin"

        self.assertTrue(self.repository.update(rdv))
        self.assertEqual(
            self.repository.get_by_id(rdv.id).name,
            "Paul Martin"
        )

    def test_suppression_rendez_vous(self):
        rdv = self.repository.add(self.rdv)

        self.assertTrue(self.repository.delete(rdv.id))
        self.assertIsNone(self.repository.get_by_id(rdv.id))

    def test_recuperation_tous_les_rendez_vous(self):
        self.repository.add(self.rdv)

        rendez_vous = self.repository.get_all()

        self.assertEqual(len(rendez_vous), 1)
    def test_persistance_horaires(self):
        self.rdv.start_time = time(14, 30)
        self.rdv.duration_minutes = 90

        rdv = self.repository.add(self.rdv)
        resultat = self.repository.get_by_id(rdv.id)

        self.assertEqual(resultat.start_time, time(14, 30))
        self.assertEqual(resultat.duration_minutes, 90)
        self.assertEqual(resultat.end_time, time(16, 0))


    def test_modification_horaires(self):
        rdv = self.repository.add(self.rdv)

        rdv.start_time = time(15, 0)
        rdv.duration_minutes = 45

        self.repository.update(rdv)
        resultat = self.repository.get_by_id(rdv.id)

        self.assertEqual(resultat.start_time, time(15, 0))
        self.assertEqual(resultat.duration_minutes, 45)

if __name__ == "__main__":
    unittest.main()