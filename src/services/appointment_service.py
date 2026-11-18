from datetime import datetime, timedelta

from src.models.appointment import Appointment
from src.database.appointment_repository import AppointmentRepository


class AppointmentService:
    """Centralise les règles métier des rendez-vous."""

    def __init__(self, repository: AppointmentRepository) -> None:
        self.repository = repository

    def check_conflict(
        self,
        appointment: Appointment,
        exclude_id: int | None = None
    ) -> bool:
        """Vérifie si un rendez-vous chevauche un rendez-vous existant."""

        appointment.end_time

        new_start = datetime.combine(
            appointment.date,
            appointment.start_time
        )
        new_end = new_start + timedelta(
            minutes=appointment.duration_minutes
        )

        for existing in self.repository.get_all():
            if existing.id == exclude_id:
                continue

            if existing.date != appointment.date:
                continue

            existing_start = datetime.combine(
                existing.date,
                existing.start_time
            )
            existing_end = existing_start + timedelta(
                minutes=existing.duration_minutes
            )

            if new_start < existing_end and new_end > existing_start:
                return True

        return False

    def create_appointment(
        self,
        appointment: Appointment
    ) -> Appointment:
        """Enregistre un nouveau rendez-vous après vérification."""

        if self.check_conflict(appointment):
            raise ValueError(
                "Ce rendez-vous chevauche un rendez-vous existant."
            )

        return self.repository.add(appointment)

    def get_all_appointments(self) -> list[Appointment]:
        """Retourne tous les rendez-vous."""

        return self.repository.get_all()

    def get_appointment(
        self,
        appointment_id: int
    ) -> Appointment | None:
        """Recherche un rendez-vous par son identifiant."""

        return self.repository.get_by_id(appointment_id)

    def update_appointment(
        self,
        appointment: Appointment
    ) -> Appointment:
        """Modifie un rendez-vous après vérification."""

        if appointment.id is None:
            raise ValueError(
                "Impossible de modifier un rendez-vous non enregistré."
            )

        if self.repository.get_by_id(appointment.id) is None:
            raise ValueError("Rendez-vous introuvable.")

        if self.check_conflict(appointment, exclude_id=appointment.id):
            raise ValueError(
                "La modification provoque un chevauchement."
            )

        self.repository.update(appointment)
        return appointment

    def delete_appointment(self, appointment_id: int) -> bool:
        """Supprime un rendez-vous."""

        return self.repository.delete(appointment_id)

    @staticmethod
    def get_appointment_status(
        appointment: Appointment,
        current_time: datetime | None = None
    ) -> str:
        """Détermine le statut temporel d'un rendez-vous."""

        now = current_time or datetime.now()

        start = datetime.combine(
            appointment.date,
            appointment.start_time
        )
        end = datetime.combine(
            appointment.date,
            appointment.end_time
        )

        if now < start:
            return "À venir"

        if start <= now < end:
            return "En cours"

        return "Terminé"

    def get_statistics(self) -> dict[str, int]:
        """Calcule les statistiques des rendez-vous."""

        appointments = self.get_all_appointments()
        now = datetime.now()

        statistics = {
            "total": len(appointments),
            "upcoming": 0,
            "ongoing": 0,
            "completed": 0
        }

        for appointment in appointments:
            status = self.get_appointment_status(appointment, now)

            if status == "À venir":
                statistics["upcoming"] += 1
            elif status == "En cours":
                statistics["ongoing"] += 1
            else:
                statistics["completed"] += 1

        return statistics

    def get_filtered_appointments(
        self,
        search_text: str = "",
        status: str = "Tous"
    ) -> list[Appointment]:
        """Filtre les rendez-vous par texte et par statut."""

        appointments = self.get_all_appointments()
        search_text = search_text.strip().casefold()

        filtered_appointments = []

        for appointment in appointments:
            searchable_text = " ".join([
                appointment.name,
                appointment.description,
                appointment.date.strftime("%d/%m/%Y"),
                appointment.start_time.strftime("%H:%M")
            ]).casefold()

            if search_text and search_text not in searchable_text:
                continue

            appointment_status = self.get_appointment_status(appointment)

            if status != "Tous" and appointment_status != status:
                continue

            filtered_appointments.append(appointment)

        return filtered_appointments
