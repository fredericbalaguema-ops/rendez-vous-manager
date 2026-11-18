from datetime import date, time, datetime, timedelta


class Appointment:
    """Modèle représentant un rendez-vous."""

    def __init__(
        self,
        name: str,
        date: date,
        description: str,
        appointment_id: int | None = None,
        start_time: time = time(9, 0),
        duration_minutes: int = 60
    ) -> None:

        self.id = appointment_id
        self.name = name
        self.date = date
        self.description = description
        self.start_time = start_time
        self.duration_minutes = duration_minutes

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Le nom doit être une chaîne.")

        value = value.strip()

        if not value:
            raise ValueError("Le nom ne peut pas être vide.")

        self._name = value

    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, value: date) -> None:
        if type(value) is not date:
            raise TypeError("La date doit être un objet datetime.date.")

        self._date = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("La description doit être une chaîne.")

        self._description = value.strip()

    @property
    def start_time(self) -> time:
        return self._start_time

    @start_time.setter
    def start_time(self, value: time) -> None:
        if type(value) is not time:
            raise TypeError("L'heure doit être un objet datetime.time.")

        self._start_time = value

    @property
    def duration_minutes(self) -> int:
        return self._duration_minutes

    @duration_minutes.setter
    def duration_minutes(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError("La durée doit être un entier.")

        if value <= 0:
            raise ValueError("La durée doit être positive.")

        self._duration_minutes = value

    @property
    def end_time(self) -> time:
        start = datetime.combine(date.min, self.start_time)
        end = start + timedelta(minutes=self.duration_minutes)

        if end.date() != date.min:
            raise ValueError("Le rendez-vous dépasse minuit.")

        return end.time()

    def __str__(self) -> str:
        return (
            f"{self.name} - "
            f"{self.date.strftime('%d/%m/%Y')} "
            f"à {self.start_time.strftime('%H:%M')}"
        )