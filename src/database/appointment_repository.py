import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import date, time
from collections.abc import Iterator

from src.models.appointment import Appointment


class AppointmentRepository:
    """Gère la persistance des rendez-vous dans SQLite."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[2]

        self.db_path = Path(
            db_path or project_root / "database" / "rendez_vous.db"
        )

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize_database(self) -> None:
        """Crée la table et applique les migrations nécessaires."""

        with self._connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL CHECK(TRIM(name) <> ''),
                    appointment_date TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    start_time TEXT NOT NULL DEFAULT '09:00',
                    duration_minutes INTEGER NOT NULL DEFAULT 60
                )
            """)

            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(appointments)"
                )
            }

            if "start_time" not in columns:
                connection.execute("""
                    ALTER TABLE appointments
                    ADD COLUMN start_time TEXT NOT NULL DEFAULT '09:00'
                """)

            if "duration_minutes" not in columns:
                connection.execute("""
                    ALTER TABLE appointments
                    ADD COLUMN duration_minutes INTEGER NOT NULL DEFAULT 60
                """)

    @staticmethod
    def _row_to_appointment(row: sqlite3.Row) -> Appointment:
        return Appointment(
            appointment_id=row["id"],
            name=row["name"],
            date=date.fromisoformat(row["appointment_date"]),
            description=row["description"],
            start_time=time.fromisoformat(row["start_time"]),
            duration_minutes=row["duration_minutes"]
        )

    def add(self, appointment: Appointment) -> Appointment:
        with self._connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO appointments (
                    name, appointment_date, description,
                    start_time, duration_minutes
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    appointment.name,
                    appointment.date.isoformat(),
                    appointment.description,
                    appointment.start_time.isoformat(),
                    appointment.duration_minutes
                )
            )

            appointment.id = cursor.lastrowid

        return appointment

    def get_all(self) -> list[Appointment]:
        with self._connection() as connection:
            rows = connection.execute("""
                SELECT * FROM appointments
                ORDER BY appointment_date, start_time, id
            """).fetchall()

        return [self._row_to_appointment(row) for row in rows]

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM appointments WHERE id = ?",
                (appointment_id,)
            ).fetchone()

        return self._row_to_appointment(row) if row else None

    def update(self, appointment: Appointment) -> bool:
        if appointment.id is None:
            return False

        with self._connection() as connection:
            cursor = connection.execute(
                """
                UPDATE appointments
                SET name = ?,
                    appointment_date = ?,
                    description = ?,
                    start_time = ?,
                    duration_minutes = ?
                WHERE id = ?
                """,
                (
                    appointment.name,
                    appointment.date.isoformat(),
                    appointment.description,
                    appointment.start_time.isoformat(),
                    appointment.duration_minutes,
                    appointment.id
                )
            )

        return cursor.rowcount > 0

    def delete(self, appointment_id: int) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM appointments WHERE id = ?",
                (appointment_id,)
            )

        return cursor.rowcount > 0