import csv
import tkinter as tk

from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime

from tkcalendar import DateEntry

from src.models.appointment import Appointment
from src.services.appointment_service import AppointmentService


class AppointmentApp:
    """Interface graphique de gestion des rendez-vous."""

    def __init__(
        self,
        root: tk.Tk,
        service: AppointmentService
    ) -> None:

        self.root = root
        self.service = service
        self.selected_id = None

        self.root.title("RendezVous Manager")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)

        self._configure_style()
        self._create_widgets()
        self._load_appointments()

    def _configure_style(self) -> None:
        """Configure les styles des composants."""

        style = ttk.Style()

        style.configure(
            "Title.TLabel",
            font=("Arial", 19, "bold")
        )

        style.configure(
            "Stats.TLabel",
            font=("Arial", 12, "bold")
        )

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def _create_widgets(self) -> None:
        """Construit l'interface complète."""

        # Titre
        title = ttk.Label(
            self.root,
            text="RENDEZVOUS MANAGER",
            style="Title.TLabel"
        )
        title.pack(pady=15)

        # Tableau de bord statistique
        self._create_dashboard()

        # Formulaire
        self._create_form()

        # Barre de recherche et filtres
        self._create_search_bar()

        # Tableau
        self._create_table()

        # Barre d'actions
        self._create_action_bar()

    def _create_dashboard(self) -> None:
        """Crée les indicateurs statistiques."""

        dashboard = ttk.LabelFrame(
            self.root,
            text="Tableau de bord",
            padding=10
        )
        dashboard.pack(fill="x", padx=20, pady=5)

        self.total_label = ttk.Label(
            dashboard,
            text="Total : 0",
            style="Stats.TLabel"
        )

        self.upcoming_label = ttk.Label(
            dashboard,
            text="À venir : 0",
            style="Stats.TLabel"
        )

        self.ongoing_label = ttk.Label(
            dashboard,
            text="En cours : 0",
            style="Stats.TLabel"
        )

        self.completed_label = ttk.Label(
            dashboard,
            text="Terminés : 0",
            style="Stats.TLabel"
        )

        labels = [
            self.total_label,
            self.upcoming_label,
            self.ongoing_label,
            self.completed_label
        ]

        for index, label in enumerate(labels):
            label.grid(
                row=0,
                column=index,
                padx=30,
                pady=5
            )

    def _create_form(self) -> None:
        """Crée le formulaire de rendez-vous."""

        form = ttk.LabelFrame(
            self.root,
            text="Informations du rendez-vous",
            padding=12
        )
        form.pack(fill="x", padx=20, pady=8)

        # Nom
        ttk.Label(form, text="Nom :").grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.name_entry = ttk.Entry(
            form,
            width=35
        )
        self.name_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        # Date
        ttk.Label(form, text="Date :").grid(
            row=0,
            column=2,
            sticky="w"
        )

        self.date_entry = DateEntry(
            form,
            width=18,
            date_pattern="dd/mm/yyyy",
            locale="fr_FR"
        )
        self.date_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=5
        )

        # Heure
        ttk.Label(form, text="Heure (HH:MM) :").grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.time_entry = ttk.Entry(
            form,
            width=35
        )
        self.time_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # Durée
        ttk.Label(form, text="Durée (minutes) :").grid(
            row=1,
            column=2,
            sticky="w"
        )

        self.duration_entry = ttk.Entry(
            form,
            width=20
        )
        self.duration_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=5
        )

        # Description
        ttk.Label(form, text="Description :").grid(
            row=2,
            column=0,
            sticky="nw"
        )

        self.description_entry = tk.Text(
            form,
            width=75,
            height=3
        )
        self.description_entry.grid(
            row=2,
            column=1,
            columnspan=3,
            padx=10,
            pady=5
        )

    def _create_search_bar(self) -> None:
        """Crée la recherche et les filtres."""

        search_frame = ttk.LabelFrame(
            self.root,
            text="Recherche et filtres",
            padding=10
        )
        search_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ttk.Label(
            search_frame,
            text="Recherche :"
        ).pack(side="left", padx=5)

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35
        )
        self.search_entry.pack(
            side="left",
            padx=5
        )

        ttk.Label(
            search_frame,
            text="Statut :"
        ).pack(side="left", padx=5)

        self.status_var = tk.StringVar(value="Tous")

        self.status_combo = ttk.Combobox(
            search_frame,
            textvariable=self.status_var,
            values=[
                "Tous",
                "À venir",
                "En cours",
                "Terminé"
            ],
            state="readonly",
            width=15
        )
        self.status_combo.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Réinitialiser",
            command=self._reset_filters
        ).pack(
            side="left",
            padx=5
        )

        self.search_var.trace_add(
            "write",
            self._apply_filters
        )

        self.status_combo.bind(
            "<<ComboboxSelected>>",
            self._apply_filters
        )

    def _create_table(self) -> None:
        """Crée le tableau des rendez-vous."""

        table_frame = ttk.LabelFrame(
            self.root,
            text="Liste des rendez-vous",
            padding=10
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=8
        )

        columns = (
            "id",
            "name",
            "date",
            "start",
            "duration",
            "end",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "name": "Nom",
            "date": "Date",
            "start": "Début",
            "duration": "Durée",
            "end": "Fin",
            "status": "Statut"
        }

        widths = {
            "id": 45,
            "name": 230,
            "date": 120,
            "start": 90,
            "duration": 90,
            "end": 90,
            "status": 120
        }

        for column in columns:
            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.tree.tag_configure(
            "upcoming",
            foreground="blue"
        )

        self.tree.tag_configure(
            "ongoing",
            foreground="darkgreen"
        )

        self.tree.tag_configure(
            "completed",
            foreground="gray"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self._select_appointment
        )

    def _create_action_bar(self) -> None:
        """Crée les boutons d'action."""

        buttons = ttk.Frame(self.root)
        buttons.pack(pady=10)

        actions = [
            ("Ajouter", self._add_appointment),
            ("Modifier", self._update_appointment),
            ("Supprimer", self._delete_appointment),
            ("Vider", self._clear_form),
            ("Actualiser", self._load_appointments),
            ("Exporter CSV", self._export_csv)
        ]

        for text, command in actions:
            ttk.Button(
                buttons,
                text=text,
                command=command
            ).pack(
                side="left",
                padx=5
            )

    def _get_form_data(self) -> Appointment:
        """Récupère les données du formulaire."""

        name = self.name_entry.get().strip()

        appointment_date = self.date_entry.get_date()

        start_time = datetime.strptime(
            self.time_entry.get().strip(),
            "%H:%M"
        ).time()

        duration = int(
            self.duration_entry.get().strip()
        )

        description = self.description_entry.get(
            "1.0",
            "end"
        ).strip()

        return Appointment(
            name=name,
            date=appointment_date,
            description=description,
            start_time=start_time,
            duration_minutes=duration
        )

    def _add_appointment(self) -> None:
        """Ajoute un rendez-vous."""

        try:
            appointment = self._get_form_data()

            self.service.create_appointment(appointment)

            self._load_appointments()
            self._clear_form()

            messagebox.showinfo(
                "Succès",
                "Rendez-vous ajouté avec succès."
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Erreur",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Erreur inattendue",
                str(error)
            )

    def _update_appointment(self) -> None:
        """Modifie un rendez-vous."""

        if self.selected_id is None:
            messagebox.showwarning(
                "Sélection requise",
                "Sélectionne un rendez-vous."
            )
            return

        try:
            appointment = self._get_form_data()
            appointment.id = self.selected_id

            self.service.update_appointment(appointment)

            self._load_appointments()
            self._clear_form()

            messagebox.showinfo(
                "Succès",
                "Rendez-vous modifié."
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Erreur",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Erreur inattendue",
                str(error)
            )

    def _delete_appointment(self) -> None:
        """Supprime un rendez-vous."""

        if self.selected_id is None:
            messagebox.showwarning(
                "Sélection requise",
                "Sélectionne un rendez-vous."
            )
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            "Veux-tu vraiment supprimer ce rendez-vous ?"
        )

        if not confirmation:
            return

        try:
            self.service.delete_appointment(self.selected_id)

            self._load_appointments()
            self._clear_form()

            messagebox.showinfo(
                "Succès",
                "Rendez-vous supprimé."
            )

        except Exception as error:
            messagebox.showerror(
                "Erreur",
                str(error)
            )

    def _update_dashboard(self) -> None:
        """Actualise les statistiques."""

        stats = self.service.get_statistics()

        self.total_label.config(
            text=f"Total : {stats['total']}"
        )

        self.upcoming_label.config(
            text=f"À venir : {stats['upcoming']}"
        )

        self.ongoing_label.config(
            text=f"En cours : {stats['ongoing']}"
        )

        self.completed_label.config(
            text=f"Terminés : {stats['completed']}"
        )

    def _load_appointments(self) -> None:
        """Recharge les rendez-vous et les statistiques."""

        self._update_dashboard()
        self._apply_filters()

    def _apply_filters(self, *args) -> None:
        """Applique la recherche et le filtre de statut."""

        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_var.get()

        status = self.status_var.get()

        appointments = self.service.get_filtered_appointments(
            search_text=search_text,
            status=status
        )

        status_tags = {
            "À venir": "upcoming",
            "En cours": "ongoing",
            "Terminé": "completed"
        }

        for appointment in appointments:

            appointment_status = (
                self.service.get_appointment_status(appointment)
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    appointment.id,
                    appointment.name,
                    appointment.date.strftime("%d/%m/%Y"),
                    appointment.start_time.strftime("%H:%M"),
                    f"{appointment.duration_minutes} min",
                    appointment.end_time.strftime("%H:%M"),
                    appointment_status
                ),
                tags=(status_tags[appointment_status],)
            )

    def _reset_filters(self) -> None:
        """Réinitialise les filtres."""

        self.search_var.set("")
        self.status_var.set("Tous")

    def _select_appointment(self, event=None) -> None:
        """Charge un rendez-vous dans le formulaire."""

        selection = self.tree.selection()

        if not selection:
            return

        values = self.tree.item(
            selection[0],
            "values"
        )

        self.selected_id = int(values[0])

        appointment = self.service.get_appointment(
            self.selected_id
        )

        if appointment is None:
            return

        self._clear_form(clear_selection=False)

        self.name_entry.insert(
            0,
            appointment.name
        )

        self.date_entry.set_date(
            appointment.date
        )

        self.time_entry.insert(
            0,
            appointment.start_time.strftime("%H:%M")
        )

        self.duration_entry.insert(
            0,
            str(appointment.duration_minutes)
        )

        self.description_entry.insert(
            "1.0",
            appointment.description
        )

    def _clear_form(self, clear_selection=True) -> None:
        """Vide le formulaire."""

        self.name_entry.delete(0, "end")

        self.date_entry.set_date(date.today())

        self.time_entry.delete(0, "end")
        self.duration_entry.delete(0, "end")

        self.description_entry.delete(
            "1.0",
            "end"
        )

        if clear_selection:
            self.selected_id = None

            self.tree.selection_remove(
                self.tree.selection()
            )

    def _export_csv(self) -> None:
        """Exporte tous les rendez-vous dans un fichier CSV."""

        appointments = self.service.get_all_appointments()

        if not appointments:
            messagebox.showinfo(
                "Exportation",
                "Aucun rendez-vous à exporter."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Exporter les rendez-vous",
            defaultextension=".csv",
            filetypes=[
                ("Fichier CSV", "*.csv"),
                ("Tous les fichiers", "*.*")
            ],
            initialfile="rendez_vous.csv"
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(
                    file,
                    delimiter=";"
                )

                writer.writerow([
                    "ID",
                    "Nom",
                    "Date",
                    "Heure de début",
                    "Durée (minutes)",
                    "Heure de fin",
                    "Description",
                    "Statut"
                ])

                for appointment in appointments:

                    status = (
                        self.service.get_appointment_status(
                            appointment
                        )
                    )

                    writer.writerow([
                        appointment.id,
                        appointment.name,
                        appointment.date.strftime("%d/%m/%Y"),
                        appointment.start_time.strftime("%H:%M"),
                        appointment.duration_minutes,
                        appointment.end_time.strftime("%H:%M"),
                        appointment.description,
                        status
                    ])

            messagebox.showinfo(
                "Exportation réussie",
                f"Les rendez-vous ont été exportés vers :\n{file_path}"
            )

        except OSError as error:
            messagebox.showerror(
                "Erreur d'exportation",
                str(error)
            )