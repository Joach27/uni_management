from flask import Flask, jsonify, request
from config import app, db
from models import Secretaire, Enseignant, Cours, CoursSemestriel, Eleve, Inscription, Seance, Examen, NoteExamen, Question, Exercice, SoumissionExercice, NoteExercice
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from datetime import timedelta



############### COURS ####################
# Routes pour afficher tous les cours
@app.route('/api/cours', methods=['GET'])
def get_cours():
    cours = Cours.query.all()
    return jsonify([cours.to_dict() for cours in cours])

# Routes pour afficher tous les cours semestriels
@app.route('/api/cours_semestriel', methods=['GET'])
def get_cours_semestriel():
    cours_semestriel = CoursSemestriel.query.all()
    return jsonify([cours_semestriel.to_dict() for cours_semestriel in cours_semestriel])

# Créer un cours
@app.route('/api/cours', methods=['POST'])
def create_cours():
    data = request.get_json()
    cours = Cours(titre=data['titre'], description=data['description'], heures=data['heures'], type=data['type'])
    db.session.add(cours)
    db.session.commit()
    
    return jsonify({'message': 'Cours créé avec succès'}) , 201

# Créer un cours semestriel
@app.route('/api/cours_semestriel', methods=['POST'])
def create_cours_semestriel():
    data = request.get_json()
    cours_semestriel = CoursSemestriel(cours_id=data['cours_id'], enseignant_id=data['enseignant_id'], semestre=data['semestre'], annee=data['annee'])
    db.session.add(cours_semestriel)
    db.session.commit()
    
    return jsonify({'message': 'Cours semestriel créé avec succès'}) , 201

# Route pour modifier un cours 
@app.route('/api/cours/<int:cours_id>', methods=['PUT'])
def update_cours(cours_id):
    data = request.get_json()
    cours = Cours.query.get(cours_id)
    if cours:
        cours.titre = data['titre']
        cours.description = data['description']
        cours.heures = data['heures']
        cours.type = data['type']
        db.session.commit()
        return jsonify({'message': 'Cours modifié avec succès'})
    else:
        return jsonify({'message': 'Cours non trouvé'}), 404
    
# Supprimer un cours 
@app.route('/api/cours/<int:cours_id>', methods=['DELETE'])
def delete_cours(cours_id):
    cours = Cours.query.get(cours_id)
    if cours:
        db.session.delete(cours)
        db.session.commit()
        return jsonify({'message': 'Cours supprimé avec succès'})
    else:
        return jsonify({'message': 'Cours non trouvé'}), 404

############### ELEVE ####################

# Route pour créer un eleve
@app.route('/api/eleve', methods=['POST'])
def create_eleve():
    data = request.get_json()
    eleve = Eleve(prenom=data['prenom'], nom=data['nom'], email=data['email'], password=data['password'])
    db.session.add(eleve)
    db.session.commit()
    
    return jsonify({'message': 'Eleve créé avec succès'}) , 201

# Routes pour afficher tous les eleves
@app.route('/api/eleve', methods=['GET'])
def get_eleves():
    eleves = Eleve.query.all()
    return jsonify([eleve.to_dict() for eleve in eleves])

# Route pour modifier un eleve
@app.route('/api/eleve/<int:eleve_id>', methods=['PUT'])
def update_eleve(eleve_id):
    data = request.get_json()
    eleve = Eleve.query.get(eleve_id)
    if eleve:
        eleve.prenom = data['prenom']
        eleve.nom = data['nom']
        eleve.email = data['email']
        db.session.commit()
        return jsonify({'message': 'Eleve modifié avec succès'})
    else:
        return jsonify({'message': 'Eleve non trouvé'}), 404

# Supprimer un eleve
@app.route('/api/eleve/<int:eleve_id>', methods=['DELETE'])
def delete_eleve(eleve_id):
    eleve = Eleve.query.get(eleve_id)
    if eleve:
        db.session.delete(eleve)
        db.session.commit()
        return jsonify({'message': 'Eleve supprimé avec succès'})
    else:
        return jsonify({'message': 'Eleve non trouvé'}), 404

# Inscription d'un eleve à un cours
@app.route('/api/eleve/<int:eleve_id>/inscription', methods=['POST'])
def inscription_eleve(eleve_id):
    data = request.get_json()
    inscription = Inscription(eleve_id=eleve_id, cours_semestriel_id=data['cours_semestriel_id'])
    db.session.add(inscription)
    db.session.commit()
    
    return jsonify({'message': 'Inscription effectuée avec succès'}) , 201

# Routes pour afficher tous les cours d'un eleve
@app.route('/api/eleve/<int:eleve_id>/cours', methods=['GET'])
def get_cours_eleve(eleve_id):
    cours = Inscription.query.filter_by(eleve_id=eleve_id).all()
    return jsonify([cours.to_dict() for cours in cours])

# Routes pour afficher toutes les notes d'un eleve
@app.route('/api/eleve/<int:eleve_id>/notes', methods=['GET'])
def get_notes_eleve(eleve_id):
    notes = NoteExamen.query.filter_by(eleve_id=eleve_id).all()
    return jsonify([note.to_dict() for note in notes])


############### ENSEIGNANT ####################
# Route pour créer un enseignant
@app.route('/api/enseignant', methods=['POST'])
def create_enseignant():
    data = request.get_json()
    enseignant = Enseignant(prenom=data['prenom'], nom=data['nom'], email=data['email'], password=data['password'], telephone=data['telephone'], fonction=data['fonction'])
    db.session.add(enseignant)
    db.session.commit()
    
    return jsonify({'message': 'Enseignant cree avec success'}) , 201

# Routes pour afficher tous les enseignants
@app.route('/api/enseignant', methods=['GET'])
def get_enseignants():
    enseignants = Enseignant.query.all()
    return jsonify([enseignant.to_dict() for enseignant in enseignants])

# Route pour modifier un enseignant
@app.route('/api/enseignant/<int:enseignant_id>', methods=['PUT'])
def update_enseignant(enseignant_id):
    data = request.get_json()
    enseignant = Enseignant.query.get(enseignant_id)    
    if enseignant:
        enseignant.prenom = data['prenom']
        enseignant.nom = data['nom']
        enseignant.email = data['email']
        enseignant.password = data['password']
        enseignant.telephone = data['telephone']
        enseignant.fonction = data['fonction']
        db.session.commit() 
        return jsonify({'message': 'Enseignant modifié avec succès'})
    else:
        return jsonify({'message': 'Enseignant non trouvé'}), 404
    
# Supprimer un enseignant
@app.route('/api/enseignant/<int:enseignant_id>', methods=['DELETE'])
def delete_enseignant(enseignant_id):
    enseignant = Enseignant.query.get(enseignant_id)
    if enseignant:
        db.session.delete(enseignant)
        db.session.commit()
        return jsonify({'message': 'Enseignant supprimé avec succès'})
    else:
        return jsonify({'message': 'Enseignant non retrouvé'}), 404

# Routes pour afficher tous les cours d'un enseignant
@app.route('/api/enseignant/<int:enseignant_id>/cours', methods=['GET'])
def get_cours_enseignant(enseignant_id):
    cours = CoursSemestriel.query.filter_by(enseignant_id=enseignant_id).all()
    return jsonify([cours.to_dict() for cours in cours])


############### EXAMEN ####################
# Route pour créer un examen*
@app.route('/api/examen', methods=['POST'])
def create_examen():
    data = request.get_json()
    examen = Examen(date=data['date'], cours_semestriel_id=data['cours_semestriel_id'])
    db.session.add(examen)
    db.session.commit()
    
    return jsonify({'message': 'Examen cree avec success'}) , 201

# Routes pour afficher tous les examens
@app.route('/api/examen', methods=['GET'])
def get_examens():
    examens = Examen.query.all()
    return jsonify([examen.to_dict() for examen in examens])

# Route attribuer une note à un examen
@app.route('/api/examen/<int:examen_id>/note', methods=['POST'])
def attribuer_note_examen(examen_id):
    data = request.get_json()
    note = NoteExamen(examen_id=examen_id, eleve_id=data['eleve_id'], note=data['note'], explication=data['explication'])
    db.session.add(note)
    db.session.commit()
    
    return jsonify({'message': 'Note attribuer avec success'})

############## NOTEEXAMEN ##################
# Route pour afficher toutes les notes d'un examen
@app.route('/api/examen/<int:examen_id>/notes', methods=['GET'])
def get_notes_examen(examen_id):
    notes = NoteExamen.query.filter_by(examen_id=examen_id).all()
    return jsonify([note.to_dict() for note in notes])

# Route pour afficher une la note d'examen d'un eleve particulier
@jwt_required()
@app.route('/api/examen/<int:examen_id>/notes/<int:eleve_id>', methods=['GET'])
def get_note_examen(examen_id, eleve_id):
    note = NoteExamen.query.filter_by(examen_id=examen_id, eleve_id=eleve_id).first()
    return jsonify(note.to_dict())

# Route pour modifier une note d'examen
@app.route('/api/examen/<int:examen_id>/notes/<int:eleve_id>', methods=['PUT'])
def update_note_examen(examen_id, eleve_id):
    data = request.get_json()
    note = NoteExamen.query.filter_by(examen_id=examen_id, eleve_id=eleve_id).first()
    if note:
        note.note = data['note']
        note.explication = data['explication']
        db.session.commit()
        return jsonify({'message': 'Note modifiee avec success'})
    else:
        return jsonify({'message': 'Note non trouvee'}), 404

# Route pour supprimer une note d'examen
@app.route('/api/examen/<int:examen_id>/notes/<int:eleve_id>', methods=['DELETE'])
def delete_note_examen(examen_id, eleve_id):
    note = NoteExamen.query.filter_by(examen_id=examen_id, eleve_id=eleve_id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note supprimee avec success'})
    else:
        return jsonify({'message': 'Note non trouvee'}), 404



############## EXERCICE ##################
# Route pour créer un exercice pour un cours
@app.route('/api/exercice', methods=['POST'])
def create_exercice():
    data = request.get_json()
    exercice = Exercice(titre=data['titre'], description=data['description'], cours_semestriel_id=data['cours_semestriel_id'])
    db.session.add(exercice)
    db.session.commit()
    
    return jsonify({'message': 'Exercice cree avec success'}) , 201

# Routes pour afficher tous les exercices
@app.route('/api/exercice', methods=['GET'])
def get_exercices():
    exercices = Exercice.query.all()
    return jsonify([exercice.to_dict() for exercice in exercices])

# route pour modifier un exercice
@app.route('/api/exercice/<int:exercice_id>', methods=['PUT'])
def modifier_exercice(exercice_id):
    data = request.get_json()
    exercice = Exercice.query.get(exercice_id)
    if exercice:
        exercice.titre = data['titre']
        exercice.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Exercice modifie avec success'})
    else:
        return jsonify({'message': 'Exercice non trouve'}), 404
    
# Supprimer un exercice
@app.route('/api/exercice/<int:exercice_id>', methods=['DELETE'])
def supprimer_exercice(exercice_id):
    exercice = Exercice.query.get(exercice_id)
    if exercice:
        db.session.delete(exercice)
        db.session.commit()
        return jsonify({'message': 'Exercice supprime avec success'})
    else:
        return jsonify({'message': 'Exercice non trouve'}), 404
    


################### NOTEEXERCICE ###################
# Route pour afficher toutes les notes d'un exercice
@app.route('/api/exercice/<int:exercice_id>/notes', methods=['GET'])
def get_notes_exercice(exercice_id):
    notes = NoteExercice.query.filter_by(exercice_id=exercice_id).all()
    return jsonify([note.to_dict() for note in notes])

# Route pour donner une note à un exercice à un étudiant
@app.route('/api/exercice/<int:exercice_id>/notes/<eleve_id>', methods=['POST'])
def attribuer_note_exercice(exercice_id, eleve_id):
    data = request.get_json()
    note = NoteExercice(exercice_id=exercice_id, eleve_id=eleve_id, note=data['note'], explication=data['explication'])
    db.session.add(note)
    db.session.commit()
    
    return jsonify({'message': 'Note attribuer avec success'})


# Route pour modifier une note d'exercice
@app.route('/api/exercice/<int:exercice_id>/notes/<int:eleve_id>', methods=['PUT'])
def update_note_exercice(exercice_id, eleve_id):
    data = request.get_json()
    note = NoteExercice.query.filter_by(exercice_id=exercice_id, eleve_id=eleve_id).first()
    if note:
        note.note = data['note']
        note.explication = data['explication']
        db.session.commit()
        return jsonify({'message': 'Note modifiee avec success'})
    else:
        return jsonify({'message': 'Note non trouvee'}), 404
    

# Route pour supprimer une note d'exercice
@app.route('/api/exercice/<int:exercice_id>/notes/<int:eleve_id>', methods=['DELETE'])    
def delete_note_exercice(exercice_id, eleve_id):    
    note = NoteExercice.query.filter_by(exercice_id=exercice_id, eleve_id=eleve_id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note supprimee avec success'})
    else:
        return jsonify({'message': 'Note non trouvee'}), 404
    
    
###################### SOUMISSION EXERCICE ####################
# Route pour soumettre un exercice
@app.route('/api/exercice/<int:exercice_id>/soumission', methods=['POST'])
def soumettre_exercice(exercice_id):
    data = request.get_json()
    soumission = SoumissionExercice(exercice_id=exercice_id, eleve_id=data['eleve_id'], fichier=data['fichier'])
    db.session.add(soumission)
    db.session.commit()
    return jsonify({'message': 'Exercice soumis avec success'})

# Route pour afficher toutes les soumissions d'un exercice
@app.route('/api/exercice/<int:exercice_id>/soumissions', methods=['GET'])
def get_soumissions_exercice(exercice_id):
    soumissions = SoumissionExercice.query.filter_by(exercice_id=exercice_id).all()
    return jsonify([soumission.to_dict() for soumission in soumissions])


################ QueQUESTIONSs ####################

# Route pour afficher toutes les questions d'une seance
@app.route('/api/seance/<int:seance_id>/questions', methods=['GET'])
def get_questions_seance(seance_id):
    questions = Question.query.filter_by(seance_id=seance_id).all()
    return jsonify([question.to_dict() for question in questions])  

# Route pour afficher toutes les questions d'un eleve dans une seance
@app.route('/api/eleve/<int:eleve_id>/seance/<int:seance_id>/questions', methods=['GET'])
def get_questions_pour_eleve(eleve_id, seance_id):
    questions = Question.query.filter_by(eleve_id=eleve_id, seance_id=seance_id).all()
    return jsonify([question.to_dict() for question in questions])



##################### LOGIN & REGISTER ###################

bcrypt = Bcrypt()
jwt = JWTManager()

@app.route('/register/eleve', methods=['POST'])
def register_eleve():
    data = request.get_json()
    print(data)
    eleve = Eleve.query.filter_by(email=data['email']).first()
    if eleve:
        return jsonify({'message': 'Un eleve avec cet email existe déjà!'}), 400

    nouveau_eleve = Eleve(prenom=data['prenom'], nom=data['nom'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    db.session.add(nouveau_eleve)
    db.session.commit()
    return jsonify({'message': 'Eleve enregistré avec succès!'}), 201

# @app.route('/register/enseignant', methods=['POST'])
# def register_enseignant():
#     data = request.get_json()
#     enseignant = Enseignant(prenom=data['prenom'], nom=data['nom'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
#     db.session.add(enseignant)
#     db.session.commit()
#     return jsonify({'message': 'Enseignant enregistré avec succès!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = Eleve.query.filter_by(email=email).first() or Enseignant.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email, expires_delta=timedelta(days=1))
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Invalid email or password'}), 401




if __name__ == '__main__':
    app.run(debug=True)