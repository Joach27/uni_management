from config import db

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('Admin', 'Secretaire', 'Enseignant', 'Eleve'), nullable=False)
    
    
class Secretaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), unique=True, nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(15))

class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), unique=True, nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(15))
    fonction = db.Column(db.Enum('Vacataire', 'ATER', 'MdC', 'Professeur'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'prenom': self.prenom,
            'nom': self.nom,
            'telephone': self.telephone,
            'fonction': self.fonction
        }

class Cours(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    heures = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum('CM', 'TP', 'TD'), nullable=False)
    
    cours_semestriels = db.relationship("CoursSemestriel", back_populates="cours")

    
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'heures': self.heures,
            'type': self.type
        }

class CoursSemestriel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignant.id'), nullable=False)
    semestre = db.Column(db.Enum('S1', 'S2'), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    
    cours = db.relationship("Cours", back_populates="cours_semestriels")

    
    def to_dict(self):
        return {
            'id': self.id,
            'cours_id': self.cours_id,
            'enseignant_id': self.enseignant_id,
            'semestre': self.semestre,
            'annee': self.annee
        }

class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), unique=True, nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'prenom': self.prenom,
            'nom': self.nom,
            'annee': self.annee
        }

class Inscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    cours_semestriel_id = db.Column(db.Integer, db.ForeignKey('cours_semestriel.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'eleve_id': self.eleve_id,
            'cours_semestriel_id': self.cours_semestriel_id
        }

class Seance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cours_semestriel_id = db.Column(db.Integer, db.ForeignKey('cours_semestriel.id'), nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    salle = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'cours_semestriel_id': self.cours_semestriel_id,
            'duree': self.duree,
            'description': self.description,
            'salle': self.salle
        }

class Examen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cours_semestriel_id = db.Column(db.Integer, db.ForeignKey('cours_semestriel.id'), nullable=False)
    type_examen = db.Column(db.Enum('Partiel', 'Final', 'Rattrapage'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    cours_semestriel = db.relationship("CoursSemestriel", backref="examens")

    
    def to_dict(self):
        return {
            'id': self.id,
            'cours_semestriel_id': self.cours_semestriel_id,
            'type_examen': self.type_examen,
            'date': self.date
        }

class NoteExamen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'), nullable=False)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    note = db.Column(db.Float, nullable=False)
    explication = db.Column(db.Text)
    
    examen = db.relationship("Examen", backref="notes")
    eleve = db.relationship("Eleve", backref="notes_examens")


class Exercice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seance_id = db.Column(db.Integer, db.ForeignKey('seance.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum('TD', 'TP', 'CM'), nullable=False)

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

