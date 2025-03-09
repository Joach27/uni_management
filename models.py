from config import db

class Secretaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(15))

class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(15))
    fonction = db.Column(db.Enum('Vacataire', 'ATER', 'MdC', 'Professeur'), nullable=False)

class Cours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    heures = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum('CM', 'TP', 'TD'), nullable=False)

class CoursSemestriel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignant.id'), nullable=False)
    semestre = db.Column(db.Enum('S1', 'S2'), nullable=False)
    annee = db.Column(db.Integer, nullable=False)

class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Inscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    cours_semestriel_id = db.Column(db.Integer, db.ForeignKey('cours_semestriel.id'), nullable=False)

class Seance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cours_semestriel_id = db.Column(db.Integer, db.ForeignKey('cours_semestriel.id'), nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    salle = db.Column(db.String(20))

class Examen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cours_semestriel_id = db.Column(db.Integer, db.ForeignKey('cours_semestriel.id'), nullable=False)
    type_examen = db.Column(db.Enum('Partiel', 'Final', 'Rattrapage'), nullable=False)
    date = db.Column(db.Date, nullable=False)

class NoteExamen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'), nullable=False)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    note = db.Column(db.Float, nullable=False)
    explication = db.Column(db.Text)

class Exercice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seance_id = db.Column(db.Integer, db.ForeignKey('seance.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)

class NoteExercice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercice_id = db.Column(db.Integer, db.ForeignKey('exercice.id'), nullable=False)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    note = db.Column(db.Float, nullable=False)
    explication = db.Column(db.Text)
    
    
class SoumissionExercice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercice_id = db.Column(db.Integer, db.ForeignKey('exercice.id'), nullable=False)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    fichier = db.Column(db.String(255), nullable=False)
    date_soumission = db.Column(db.DateTime, default=db.func.current_timestamp())

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seance_id = db.Column(db.Integer, db.ForeignKey('seance.id'), nullable=False)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_question = db.Column(db.DateTime, default=db.func.current_timestamp())

