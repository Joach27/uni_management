from flask import Flask, jsonify, request
from config import app, db
from models import Secretaire, Enseignant, Cours, CoursSemestriel, Eleve, Inscription, Seance, Examen, NoteExamen, Question, Exercice, SoumissionExercice, NoteExercice, Utilisateur
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
    
    results = []
    for cs in cours_semestriel:
        results.append({
        'id': cs.id,
        'annee': cs.annee,
        'semestre': cs.semestre,
        'cours':{
            'id': cs.cours.id,
            'titre': cs.cours.titre,
            'description': cs.cours.description,
            'heures': cs.cours.heures,
            'type': cs.cours.type
        }
        })
    return jsonify(results)


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
    eleve = Eleve(utilisateur_id=data['utilisateur_id'], prenom=data['prenom'], nom=data['nom'], annee=data['annee'])
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
        eleve.utilisateur_id = data['utilisateur_id']
        eleve.prenom = data['prenom']
        eleve.nom = data['nom']
        eleve.annee = data['annee']
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
    
    if 'cours_semestriel_id' not in data:
        return jsonify({"error": "cours_semestriel_id manquant"}), 400
    
    # Vérifier si l'inscription existe déjà
    exist = Inscription.query.filter_by(
        eleve_id=eleve_id,
        cours_semestriel_id=data['cours_semestriel_id']
    ).first()
    if exist:
        return jsonify({"error": "Déjà inscrit à ce cours"}), 409
    
    inscription = Inscription(eleve_id=eleve_id, cours_semestriel_id=data['cours_semestriel_id'])
    db.session.add(inscription)
    db.session.commit()
    
    return jsonify({'message': 'Inscription effectuée avec succès'}) , 201

# Routes pour afficher tous les cours d'un eleve
@app.route('/api/eleve/<int:eleve_id>/cours', methods=['GET'])
def get_cours_eleve(eleve_id):
    cours = Inscription.query.filter_by(eleve_id=eleve_id).all()
    # return jsonify([cours.to_dict() for cours in cours])
    results = []
    for c in cours:
        cours_semestriel = CoursSemestriel.query.get(c.cours_semestriel_id)
        cours_semestriel_dict = cours_semestriel.to_dict()
        cours_semestriel_dict['cours'] = Cours.query.get(cours_semestriel.cours_id).to_dict()
        results.append(cours_semestriel_dict)
    return jsonify(results), 200

# Routes pour afficher toutes les notes d'un eleve
@app.route('/api/eleve/<int:eleve_id>/notes', methods=['GET'])
def get_notes_eleve(eleve_id):
    notes = NoteExamen.query.filter_by(eleve_id=eleve_id).all()
    return jsonify([note.to_dict() for note in notes])

# Route pour rechercher un élève par son email
@app.route('/api/eleve/email/<string:email>', methods=['GET'])
def get_eleve_by_email(email):
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur:
        eleve = Eleve.query.filter_by(utilisateur_id=utilisateur.id).first()
        if eleve:
            return jsonify(eleve.to_dict()), 200
    return jsonify({'message': 'Eleve non trouvé'}), 404

############### ENSEIGNANT ####################
# Route pour créer un enseignant
@app.route('/api/enseignant', methods=['POST'])
def create_enseignant():
    data = request.get_json()
    enseignant = Enseignant(utilisateur_id=data['utilisateur_id'], prenom=data['prenom'], nom=data['nom'], telephone=data['telephone'], fonction=data['fonction'])
    db.session.add(enseignant)
    db.session.commit()
    
    return jsonify({'message': 'Enseignant cree avec success'}) , 201

# Routes pour afficher tous les enseignants
@app.route('/api/enseignants', methods=['GET'])
def get_enseignants():
    enseignants = Enseignant.query.all()
    return jsonify([enseignant.to_dict() for enseignant in enseignants])

# Route pour modifier un enseignant
@app.route('/api/enseignant/<int:enseignant_id>', methods=['PUT'])
def update_enseignant(enseignant_id):
    data = request.get_json()
    enseignant = Enseignant.query.get(enseignant_id)    
    if enseignant:
        enseignant.utilisateur_id = data['utilisateur_id']
        enseignant.prenom = data['prenom']
        enseignant.nom = data['nom']
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


# Route pour afficher les cours semestriels d'un ensignant avec le titre du cours
@app.route('/api/enseignant/<int:enseignant_id>/cours_semestriel', methods=['GET'])
def get_cours_semestriel_enseignant(enseignant_id):
    # Effectuer une jointure entre CoursSemestriel et Cours pour obtenir le titre du cours
    cours_semestriels = db.session.query(CoursSemestriel, Cours).join(Cours, Cours.id == CoursSemestriel.cours_id).filter(CoursSemestriel.enseignant_id == enseignant_id).all()
    
    # Retourner les données sous forme de JSON, avec le titre du cours
    result = []
    for cours_semestriel, cours in cours_semestriels:
        result.append({
            'id': cours_semestriel.id,
            'cours_id': cours_semestriel.cours_id,
            'enseignant_id': cours_semestriel.enseignant_id,
            'semestre': cours_semestriel.semestre,
            'annee': cours_semestriel.annee,
            'titre': cours.titre  # Ajout du titre du cours
        })
    
    return jsonify(result)

# Route pour reécupérer un enseignant par son email 
@app.route('/api/enseignant/email/<string:email>', methods=['GET'])
def get_enseignant_par_email(email):
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur:
        enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
        if enseignant:
            return jsonify(enseignant.to_dict()), 200
    return jsonify({'message': 'Enseignant non trouvé'}), 404


# Route pour afficher les cours semestriels d'un enseignant à partir de son email
@app.route('/api/enseignant/email/<string:email>/cours_semestriel', methods=['GET'])
# @jwt_required
def get_cours_semestriel_par_email(email):
    # Trouver l'enseignant à partir de l'email de l'utilisateur
    enseignant = db.session.query(Enseignant).join(Utilisateur).filter(Utilisateur.email == email).first()
    
    if not enseignant:
        return jsonify({"message": "Enseignant non trouvé pour cet email"}), 404

    # Si l'enseignant est trouvé, récupérer ses cours semestriels
    cours_semestriels = db.session.query(CoursSemestriel, Cours).join(Cours, Cours.id == CoursSemestriel.cours_id).filter(CoursSemestriel.enseignant_id == enseignant.id).all()

    # Retourner les résultats avec les titres des cours
    result = []
    for cours_semestriel, cours in cours_semestriels:
        result.append({
            'id': cours_semestriel.id,
            'cours_id': cours_semestriel.cours_id,
            'enseignant_id': cours_semestriel.enseignant_id,
            'semestre': cours_semestriel.semestre,
            'annee': cours_semestriel.annee,
            'titre': cours.titre  # Ajouter le titre du cours
        })
    
    return jsonify(result)



#Route pour créer une séance
@app.route('/api/seance', methods=['POST'])
def create_seance():
    data = request.get_json()
    seance = Seance(cours_semestriel_id=data['cours_semestriel_id'], duree=data['duree'], description=data['description'], salle=data['salle'])
    
    db.session.add(seance)
    db.session.commit()
    
    return jsonify({'message': 'Séance cree avec success'}) , 201

 


############### EXAMEN ####################
# Route pour créer un examen*
@app.route('/api/examen', methods=['POST'])
def create_examen():
    data = request.get_json()
    examen = Examen(cours_semestriel_id=data['cours_semestriel_id'], type_examen=data['type_examen'], date=data['date'])
    db.session.add(examen)
    db.session.commit()
    
    return jsonify({'message': 'Examen cree avec success'}) , 201

# Un enseignant crée un examen
@app.route('/api/examen/creer', methods=['POST'])
@jwt_required()
def create_exam_by_teacher():
    # Récupérer l'email de l'utilisateur à partir du token JWT
    email = get_jwt_identity()
    
    # Trouver l'utilisateur correspondant
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    # Vérifier que l'utilisateur existe et est bien un enseignant
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    # Trouver l'enseignant correspondant à cet utilisateur
    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not enseignant:
        return jsonify({'message': 'Enseignant non trouvé'}), 404
    
    # Récupérer les données de la requête
    data = request.get_json()
    
    # Valider les données requises
    if not all(key in data for key in ['cours_semestriel_id', 'date', 'type_examen']):
        return jsonify({'message': 'Données incomplètes. Besoin de cours_semestriel_id, date et type_examen'}), 400
    
    # Vérifier que le cours semestriel existe et appartient à cet enseignant
    cours_semestriel = CoursSemestriel.query.get(data['cours_semestriel_id'])
    if not cours_semestriel:
        return jsonify({'message': 'Cours semestriel non trouvé'}), 404
    
    if cours_semestriel.enseignant_id != enseignant.id:
        return jsonify({'message': 'Ce cours semestriel ne vous appartient pas'}), 403
    
    # Récupérer les cours pour pourvoir afficher le titre du cours semestriel
    cours = Cours.query.get(cours_semestriel.cours_id)
    if not cours:
        return jsonify({'message': 'Cours non trouvé'}), 404
    
    # Créer l'examen
    try:
        examen = Examen(
            cours_semestriel_id=data['cours_semestriel_id'],
            type_examen=data['type_examen'],
            date=data['date']
        )
        db.session.add(examen)
        db.session.commit()
        
        # Retourner les informations de l'examen créé
        return jsonify({
            'message': 'Examen créé avec succès',
            'examen': {
                'id': examen.id,
                'cours_semestriel_id': examen.cours_semestriel_id,
                'cours': {
                    'id': cours.id,
                    'titre': cours.titre
                },
                'date': examen.date,
                'type_examen': examen.type_examen
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la création de l\'examen: {str(e)}'}), 500

# Routes pour afficher tous les examens
@app.route('/api/examen', methods=['GET'])
def get_examens():
    examens = Examen.query.all()
    return jsonify([examen.to_dict() for examen in examens])

# Endpoint pour que l'enseignant puisse voir tous ses examens
@app.route('/api/enseignant/examens', methods=['GET'])
@jwt_required()
def get_examens_enseignant():
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not enseignant:
        return jsonify({'message': 'Enseignant non trouvé'}), 404
    
    # Récupérer les cours semestriels de l'enseignant
    cours_semestriels = CoursSemestriel.query.filter_by(enseignant_id=enseignant.id).all()
    cours_ids = [cs.id for cs in cours_semestriels]
    
    # Récupérer les examens associés à ces cours
    examens = Examen.query.filter(Examen.cours_semestriel_id.in_(cours_ids)).all()
    
    # Préparer les données de réponse avec des informations enrichies
    result = []
    for examen in examens:
        cours_sem = CoursSemestriel.query.get(examen.cours_semestriel_id)
        cours = Cours.query.get(cours_sem.cours_id)
        
        result.append({
            'id': examen.id,
            'date': examen.date,
            'type_examen': examen.type_examen,
            'cours': {
                'id': cours.id,
                'titre': cours.titre,
                'type': cours.type
            },
            'semestre': cours_sem.semestre,
            'annee': cours_sem.annee
        })
    
    return jsonify(result), 200


# Endpoint pour que l'eleve puisse voir tous ses examens
@app.route('/api/eleve/examens', methods=['GET'])
@jwt_required()
def get_examens_eleve():
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    if not utilisateur or utilisateur.role != 'Eleve':
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    eleve = Eleve.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not eleve:
        return jsonify({'message': 'Enseignant non trouvé'}), 404
    
    # Récupérer les inscription de l'eleve
    inscription_eleve = Inscription.query.filter_by(eleve_id=eleve.id).all()
    cours_ids = [ie.cours_semestriel_id for ie in inscription_eleve]
    
    # Récupérer les examens associés à ces cours
    examens = Examen.query.filter(Examen.cours_semestriel_id.in_(cours_ids)).all()
    
    # Préparer les données de réponse avec des informations enrichies
    result = []
    for examen in examens:
        cours_sem = CoursSemestriel.query.get(examen.cours_semestriel_id)
        cours = Cours.query.get(cours_sem.cours_id)
        
        result.append({
            'id': examen.id,
            'date': examen.date,
            'type_examen': examen.type_examen,
            'cours': {
                'id': cours.id,
                'titre': cours.titre,
                'type': cours.type
            },
            'semestre': cours_sem.semestre,
            'annee': cours_sem.annee
        })
    
    return jsonify(result), 200




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
    
# Route pour qu'un enseignant donne une note à un élève
# @app.route("/api/enseignant/note/eleve" , methods=['POST'])
# @jwt_required
# def attribuer_note_eleve():
#     email = get_jwt_identity()
#     utilisateur = Utilisateur.query.filter_by(email=email).first()
#     if utilisateur.role != "Enseignant":
#         return jsonify({'message': 'Accès non autorisé'}), 403
#     cours_semestriels = CoursSemestriel.query.filter_by(enseignant_id=utilisateur.id).all()
    
#     cours_semestriels_ids = [cours_semestriel.id for cours_semestriel in cours_semestriels]
    
#     cours_eleve_inscrit = []
   

############## EXERCICE ##################
# Route pour créer un exercice pour un cours
@app.route('/api/exercice', methods=['POST'])
def create_exercice():
    data = request.get_json()
    exercice = Exercice(seance_id=data['seance_id'], contenu=data['contenu'], type=data['type'])
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
        exercice.seance_id = data['seance_id']
        exercice.contenu = data['contenu']
        exercice.type = data['type']
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
    
# Endpoint pour récupérer les détails d'un exercice spécifique
@app.route('/api/exercice/<int:exercice_id>/details', methods=['GET'])
def get_exercice_details(exercice_id):
    exercice = Exercice.query.get(exercice_id)
    if not exercice:
        return jsonify({'message': 'Exercice non trouvé'}), 404
    
    seance = Seance.query.get(exercice.seance_id)
    cours_semestriel = CoursSemestriel.query.get(seance.cours_semestriel_id)
    cours = Cours.query.get(cours_semestriel.cours_id)
    enseignant = Enseignant.query.get(cours_semestriel.enseignant_id)
    
    return jsonify({
        'id': exercice.id,
        'contenu': exercice.contenu,
        'type': exercice.type,
        'seance': seance.to_dict(),
        'cours_semestriel': cours_semestriel.to_dict(),
        'cours': cours.to_dict(),
        'enseignant': enseignant.to_dict()
    }), 200


    
# Route pour afficher les exercices des séances d'un eleve
@app.route('/api/eleve/<int:eleve_id>/exercices', methods=['GET'])
def get_exercices_eleve(eleve_id):
    # Vérifier si l'élève existe
    eleve = Eleve.query.get(eleve_id)
    if not eleve:
        return jsonify({'message': 'Eleve non trouvé'}), 404
    
    # Récupérer toutes les inscriptions de l'élève
    inscriptions = Inscription.query.filter_by(eleve_id=eleve_id).all()
    
    # Récupérer les IDs de cours semestriels auxquels l'élève est inscrit
    cours_semestriels_ids = [inscription.cours_semestriel_id for inscription in inscriptions]
    
    # Récupérer toutes les séances de ces cours
    seances = Seance.query.filter(Seance.cours_semestriel_id.in_(cours_semestriels_ids)).all()
    seances_ids = [seance.id for seance in seances]
    
    # Récupérer tous les exercices liés à ces séances
    exercices = Exercice.query.filter(Exercice.seance_id.in_(seances_ids)).all()
    
    # Préparer les résultats avec des informations enrichies
    result = []
    for exercice in exercices:
        seance = Seance.query.get(exercice.seance_id)
        cours_semestriel = CoursSemestriel.query.get(seance.cours_semestriel_id)
        cours = Cours.query.get(cours_semestriel.cours_id)
        enseignant = Enseignant.query.get(cours_semestriel.enseignant_id)
        
        # Vérifier si l'élève a déjà soumis cet exercice
        soumission = SoumissionExercice.query.filter_by(
            exercice_id=exercice.id, 
            eleve_id=eleve_id
        ).first()
        
        # Vérifier si l'élève a déjà une note pour cet exercice
        note = NoteExercice.query.filter_by(
            exercice_id=exercice.id,
            eleve_id=eleve_id
        ).first()
        
        result.append({
            'id': exercice.id,
            'contenu': exercice.contenu,
            'type': exercice.type,
            'seance': {
                'id': seance.id,
                'description': seance.description,
                'duree': seance.duree,
                'salle': seance.salle
            },
            'cours': {
                'id': cours.id,
                'titre': cours.titre,
                'description': cours.description,
                'type': cours.type,
                'semestre': cours_semestriel.semestre,
                'annee': cours_semestriel.annee
            },
            'enseignant': {
                'id': enseignant.id,
                'nom': enseignant.nom,
                'prenom': enseignant.prenom
            },
            'soumission': {
                'soumis': soumission is not None,
                'date': soumission.date_soumission.strftime('%Y-%m-%d %H:%M:%S') if soumission else None,
                'fichier': soumission.fichier if soumission else None
            },
            'note': {
                'valeur': note.note if note else None,
                'explication': note.explication if note else None
            }
        })
    
    return jsonify(result), 200

# Version avec authentification JWT pour que l'élève puisse voir ses propres exercices
@app.route('/api/eleve/exercices', methods=['GET'])
@jwt_required()
def get_exercices_eleve_jwt():
    # Récupérer l'email de l'utilisateur à partir du token JWT
    email = get_jwt_identity()
    
    # Trouver l'utilisateur correspondant
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    # Vérifier que l'utilisateur existe et est bien un élève
    if not utilisateur or utilisateur.role != 'Eleve':
        return jsonify({'message': 'Accès non autorisé'}), 403
    
    # Trouver l'élève correspondant à cet utilisateur
    eleve = Eleve.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not eleve:
        return jsonify({'message': 'Élève non trouvé'}), 404
    
    # Utiliser la fonction existante pour récupérer les exercices
    return get_exercices_eleve(eleve.id)


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

# @app.route('/register/eleve', methods=['POST'])
# def register_eleve():
#     data = request.get_json()
#     eleve = Eleve.query.filter_by(email=data['email']).first()
#     if eleve:
#         return jsonify({'message': 'Un eleve avec cet email existe déjà!'}), 400

#     nouveau_eleve = Eleve(prenom=data['prenom'], nom=data['nom'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
#     db.session.add(nouveau_eleve)
#     db.session.commit()
#     return jsonify({'message': 'Eleve enregistré avec succès!'}), 201

@app.route('/inscription', methods=['POST'])
def inscrire():
    data = request.get_json()
    user = Utilisateur.query.filter_by(email=data['email']).first()
    
    if user: 
        return jsonify({'message': 'Un utilisateur avec cet email existe déjà!'}), 400
    
    nouveau_utilisateur = Utilisateur(email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'), role=data['role'])
    db.session.add(nouveau_utilisateur)
    db.session.commit()
    
    if data['role'] == "Secretaire":
        nouveau_secreataire = Secretaire(utilisateur_id=nouveau_utilisateur.id, nom=data['nom'], prenom=data['prenom'], telephone=data['telephone'])
        db.session.add(nouveau_secreataire)
    
    if data['role'] == "Enseignant":
        nouvel_enseignant = Enseignant(utilisateur_id=nouveau_utilisateur.id, prenom=data['prenom'], nom=data['nom'], telephone=data['telephone'], fonction=data['fonction'])
        db.session.add(nouvel_enseignant)
        
    elif data['role'] == "Eleve":
        nouvel_eleve = Eleve(utilisateur_id=nouveau_utilisateur.id, prenom=data['prenom'], nom=data['nom'], annee=data['annee'])
        db.session.add(nouvel_eleve)
        
    db.session.commit()
    return jsonify({'message': 'Utilisateur enregistré avec succès!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = Utilisateur.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email, expires_delta=timedelta(days=1))
        return jsonify({'access_token': access_token, 'role': user.role}), 200
    return jsonify({'message': 'Mot de passe ou Email incorrect'}), 401

# @app.route('/register/enseignant', methods=['POST'])
# def register_enseignant():
#     data = request.get_json()
#     enseignant = Enseignant(prenom=data['prenom'], nom=data['nom'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
#     db.session.add(enseignant)
#     db.session.commit()
#     return jsonify({'message': 'Enseignant enregistré avec succès!'})



################### SEANCES ###################
# Creer un exercice pour une seance
@app.route('/api/exercices', methods=['POST'])
@jwt_required()
def creer_exercice():
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()

    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'message': 'Accès non autorisé'}), 403

    data = request.get_json()
    seance_id = data.get('seance_id')
    contenu = data.get('contenu')
    type_exercice = data.get('type')

    if not all([seance_id, contenu, type_exercice]):
        return jsonify({'message': 'Champs manquants'}), 400

    # Vérification que l'enseignant est bien lié à la séance
    seance = Seance.query.get(seance_id)
    if not seance:
        return jsonify({'message': 'Séance non trouvée'}), 404

    cours_sem = CoursSemestriel.query.get(seance.cours_semestriel_id)
    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    
    if not enseignant or cours_sem.enseignant_id != enseignant.id:
        return jsonify({'message': 'Cette séance ne vous appartient pas'}), 403

    exercice = Exercice(
        seance_id=seance_id,
        contenu=contenu,
        type=type_exercice
    )
    db.session.add(exercice)
    db.session.commit()

    return jsonify({'message': 'Exercice créé avec succès'}), 201


# Route pour afficher les séances d'un enseignant
@app.route("/api/enseignant/seances", methods=["GET"])
@jwt_required()
def get_seances_enseignant():
    email = get_jwt_identity()
    
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({"message": "Accès non autorisé"}), 403

    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not enseignant:
        return jsonify({"message": "Enseignant introuvable"}), 404

    # Récupération des cours semestriels de cet enseignant
    cours_semestriels = CoursSemestriel.query.filter_by(enseignant_id=enseignant.id).all()
    cours_ids = [cs.id for cs in cours_semestriels]

    # Récupération des séances de ces cours
    seances = Seance.query.filter(Seance.cours_semestriel_id.in_(cours_ids)).all()

    return jsonify([s.to_dict() for s in seances]), 200

# Routes pour afficher les séances d'un élève
@app.route('/api/eleve/<int:eleve_id>/seances', methods=['GET'])
def get_seances_eleve(eleve_id):
    inscriptions = Inscription.query.filter_by(eleve_id=eleve_id).all()
    
    cours_semestriels_ids = [inscription.cours_semestriel_id for inscription in inscriptions]
    
    seances = []
    for cs_id in cours_semestriels_ids:
        seances.extend(Seance.query.filter_by(cours_semestriel_id=cs_id).all())
    
    return jsonify([s.to_dict() for s in seances]), 200




if __name__ == '__main__':
    app.run(debug=True)