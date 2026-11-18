# RendezVous Manager

**RendezVous Manager** est une application de bureau développée en Python permettant de gérer simplement des rendez-vous. Elle repose sur une architecture orientée objet, une interface graphique Tkinter et une base de données SQLite.

Ce projet est développé dans une démarche d'apprentissage, de mise en pratique des bonnes pratiques de programmation Python et de conception logicielle.

## Fonctionnalités

- Création de rendez-vous.
- Consultation de la liste des rendez-vous.
- Modification et suppression de rendez-vous.
- Enregistrement persistant des données avec SQLite.
- Gestion des dates, heures de début et durées.
- Calcul automatique de l'heure de fin.
- Détection des conflits horaires.
- Gestion des statuts : à venir, en cours et terminé.
- Recherche et filtrage des rendez-vous.
- Tableau de bord avec statistiques.
- Exportation des rendez-vous au format CSV.
- Tests unitaires des principales fonctionnalités.

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Langage de programmation |
| Tkinter | Interface graphique |
| SQLite | Stockage des données |
| tkcalendar | Calendrier et sélection des dates |
| unittest | Tests unitaires |
| Git | Gestion du versionnement |
| GitHub | Hébergement du code source |

## Architecture du projet

Le projet suit une architecture organisée en plusieurs couches afin de séparer les responsabilités.

```text
rendez-vous-manager/
│
├── src/
│   ├── models/
│   │   └── appointment.py
│   │
│   ├── database/
│   │   └── appointment_repository.py
│   │
│   ├── services/
│   │   └── appointment_service.py
│   │
│   ├── ui/
│   │   └── appointment_app.py
│   │
│   ├── utils/
│   └── main.py
│
├── database/
├── assets/
├── docs/
├── tests/
│   ├── test_appointment.py
│   ├── test_appointment_repository.py
│   └── test_appointment_service.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### Organisation des couches

- **models/** : contient les modèles et les règles de validation des objets.
- **database/** : assure la communication avec la base de données SQLite.
- **services/** : centralise les règles métier et les opérations sur les rendez-vous.
- **ui/** : contient les composants de l'interface graphique.
- **utils/** : accueille les fonctions utilitaires.
- **tests/** : contient les tests unitaires.

## Prérequis

- Python 3.10 ou supérieur.
- Git.
- Tkinter.
- pip.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/fredericbalaguema-ops/rendez-vous-manager.git
cd rendez-vous-manager
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
```

### 3. Activer l'environnement virtuel

Sur Ubuntu/Linux :

```bash
source .venv/bin/activate
```

Sur Windows :

```bash
.venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Sur Ubuntu, si Tkinter n'est pas installé :

```bash
sudo apt install python3-tk
```

## Lancer l'application

Depuis la racine du projet :

```bash
python -m src.main
```

## Exécuter les tests

Pour lancer l'ensemble des tests unitaires :

```bash
python -m unittest discover -s tests -v
```

Les tests couvrent notamment :

- La création et la validation des rendez-vous.
- Le calcul de l'heure de fin.
- La persistance des données dans SQLite.
- Les opérations du service.
- La détection des chevauchements horaires.
- La modification et la suppression.
- Le calcul des statuts.
- La recherche et les statistiques.

**État actuel : 28 tests unitaires réussis.**

## Base de données

L'application utilise SQLite pour assurer la persistance des rendez-vous.

La base de données est créée automatiquement au lancement de l'application dans le dossier `database/`.

Les fichiers de base de données locaux sont exclus du suivi Git afin de ne pas publier les données personnelles ou de test.

## Licence

Ce projet est distribué sous licence MIT.

Consultez le fichier [LICENSE](LICENSE) pour découvrir les conditions d'utilisation, de modification et de redistribution.

Les bibliothèques tierces conservent leurs propres licences.

## Auteur

**Frédéric BALAGUEMA**

Étudiant en Mathématiques et Informatique | Développeur Python.

- GitHub : [fredericbalaguema-ops](https://github.com/fredericbalaguema-ops)
- Dépôt du projet : [rendez-vous-manager](https://github.com/fredericbalaguema-ops/rendez-vous-manager)

---

**Statut du projet :** En cours de développement.

De nouvelles fonctionnalités et améliorations seront ajoutées progressivement.