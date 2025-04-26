# uni_management

# Gestion des Cours Universitaires

## Description

Ce projet est une application web conçue pour la gestion des cours universitaires. Elle permet aux secrétaires, enseignants, et élèves de gérer efficacement les cours, les inscriptions, et les évaluations. L'application utilise Flask pour le backend et React pour le frontend, avec une authentification sécurisée basée sur les tokens JWT.

## Fonctionnalités

- **Inscription et Connexion :** Les utilisateurs peuvent s'inscrire et se connecter avec des rôles spécifiques (secrétaire, enseignant, élève).
- **Gestion des Cours :** Les enseignants peuvent créer et gérer des cours et des séances.
- **Notes et Évaluations :** Les élèves peuvent consulter leurs notes et les enseignants peuvent les attribuer.
- **Questions et Exercices :** Les élèves peuvent poser des questions et soumettre des exercices.
- **Barre de Navigation Dynamique :** Affiche des liens différents en fonction du rôle de l'utilisateur.

## Technologies Utilisées

- **Backend :** Flask, SQLAlchemy, Flask-JWT-Extended
- **Frontend :** React, Axios, React Router
- **Base de Données :** SQLite (pour le développement)

## Configuration et Exécution

### Backend (Flask)

1. **Cloner le Repository :**
   ```bash
   git clone https://github.com/votre-utilisateur/gestion-cours.git
   cd gestion-cours
   ```

2. **Créer un Environnement Virtuel :**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
   ```

3. **Installer les Dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Exécuter l'Application Flask :**
   ```bash
   python app.py
   ```

   L'application sera accessible à l'adresse `http://127.0.0.1:5000/`.

### Frontend (React)

1. **Naviguer vers le Répertoire Frontend :**
   ```bash
   cd gestion-cours-frontend
   ```

2. **Installer les Dépendances :**
   ```bash
   npm install
   ```

3. **Exécuter l'Application React :**
   ```bash
   npm run dev
   ```

   L'application sera accessible à l'adresse `http://localhost:3000/`.

## Structure du Projet

- **Backend (`app.py`, `models.py`) :** Contient la logique du serveur, les modèles de base de données, et les routes API.
- **Frontend (`gestion-cours-frontend`) :** Contient les composants React, les pages, et la logique d'authentification.

## Contribution

Les contributions sont les bienvenues ! Pour contribuer, veuillez suivre ces étapes :

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3. Commitez vos modifications (`git commit -m 'Ajout de la nouvelle fonctionnalité'`).
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`).
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
