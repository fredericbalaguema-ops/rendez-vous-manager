import tkinter as tk

from src.database.appointment_repository import AppointmentRepository
from src.services.appointment_service import AppointmentService
from src.ui.appointment_app import AppointmentApp


def main() -> None:
    repository = AppointmentRepository()
    service = AppointmentService(repository)

    root = tk.Tk()
    AppointmentApp(root, service)

    root.mainloop()


if __name__ == "__main__":
    main()