from flask import Blueprint
from flask import jsonify, request
from models import db, NoteExamen
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import CoursSemestriel, Inscription, Examen, Eleve, Enseignant, Utilisateur

examen_bp = Blueprint('examen', __name__)

# Route pour afficher les notes d'examen d'un élève
@examen_bp.route('/api/examens/notes', methods=['GET'])
def get_notes_examen_eleve():
    return None

# Route pour qu'un enseignant ajoute une note d'examen
@examen_bp.route('/api/note_examen', methods=['POST'])
def noter_examen():
    data = request.get_json()
    note = NoteExamen(
        eleve_id=data['eleve_id'],
        examen_id=data['examen_id'],
        valeur=data['valeur']
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note attribuée avec succès'}), 201

# # Endpoint pour voir les élèves d'un examen spécifique
# @examen_bp.route('/api/examen/<int:examen_id>/eleves', methods=['GET'])
# @jwt_required()
# def get_eleves_examen(examen_id):
#     email = get_jwt_identity()
#     utilisateur = Utilisateur.query.filter_by(email=email).first()
    
#     if not utilisateur or utilisateur.role != 'Enseignant':
#         return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
#     enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
#     if not enseignant:
#         return jsonify({'success': False, 'message': 'Enseignant non trouvé'}), 404
    
#     # Vérifier que l'examen existe
#     examen = Examen.query.get(examen_id)
#     if not examen:
#         return jsonify({'success': False, 'message': 'Examen non trouvé'}), 404
    
#     # Vérifier que l'enseignant est bien responsable de cet examen
#     cours_sem = CoursSemestriel.query.get(examen.cours_semestriel_id)
#     if not cours_sem or cours_sem.enseignant_id != enseignant.id:
#         return jsonify({'success': False, 'message': 'Vous n\'êtes pas autorisé à accéder à cet examen'}), 403
    
#     # Récupérer tous les élèves inscrits au cours avec jointure pour optimiser
#     eleves_inscrits = db.session.query(
#         Eleve
#     ).join(
#         Inscription, Eleve.id == Inscription.eleve_id
#     ).filter(
#         Inscription.cours_semestriel_id == examen.cours_semestriel_id
#     ).all()
    
#     # Récupérer les notes déjà attribuées pour cet examen
#     notes = {
#         note.eleve_id: note 
#         for note in NoteExamen.query.filter_by(examen_id=examen_id).all()
#     }
    
#     # Préparer les données avec les élèves et leurs notes (si existantes)
#     eleves_list = []
#     for eleve in eleves_inscrits:
#         eleve_data = eleve.to_dict()
        
#         # Ajouter la note si elle existe
#         if eleve.id in notes:
#             note = notes[eleve.id]
#             eleve_data['note'] = {
#                 'id': note.id,
#                 'valeur': note.note,
#                 'explication': note.explication
#             }
#         else:
#             eleve_data['note'] = None
            
#         eleves_list.append(eleve_data)
    
#     return jsonify({
#         'success': True,
#         'count': len(eleves_list),
#         'examen': {
#             'id': examen.id,
#             'type': examen.type_examen,
#             'date': examen.date.strftime('%Y-%m-%d') if examen.date else None
#         },
#         'eleves': eleves_list
#     }), 200
    
# Endpoint pour attribuer une nouvelle note (création)
@examen_bp.route('/api/examen/<int:examen_id>/notes', methods=['POST'])
@jwt_required()
def creer_note_examen(examen_id):
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not enseignant:
        return jsonify({'success': False, 'message': 'Enseignant non trouvé'}), 404
    
    # Récupérer les données du corps de la requête
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Aucune donnée fournie'}), 400
    
    # Vérifier la présence des champs obligatoires
    required_fields = ['eleve_id', 'note']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'success': False, 'message': f'Champs manquants: {", ".join(missing_fields)}'}), 400
    
    eleve_id = data['eleve_id']
    note_valeur = data['note']
    explication = data.get('explication', '')
    
    # Vérifier que la note est dans une plage valide (0-20)
    if not (isinstance(note_valeur, (int, float)) and 0 <= note_valeur <= 20):
        return jsonify({'success': False, 'message': 'La note doit être un nombre compris entre 0 et 20'}), 400
    
    # Vérifier que l'examen existe
    examen = Examen.query.get(examen_id)
    if not examen:
        return jsonify({'success': False, 'message': 'Examen non trouvé'}), 404
    
    # Vérifier que l'enseignant est bien responsable du cours
    cours_sem = CoursSemestriel.query.get(examen.cours_semestriel_id)
    if not cours_sem or cours_sem.enseignant_id != enseignant.id:
        return jsonify({'success': False, 'message': 'Vous n\'êtes pas autorisé à attribuer des notes pour cet examen'}), 403
    
    # Vérifier que l'élève existe
    eleve = Eleve.query.get(eleve_id)
    if not eleve:
        return jsonify({'success': False, 'message': 'Élève non trouvé'}), 404
    
    # Vérifier que l'élève est inscrit au cours
    inscription = Inscription.query.filter_by(
        eleve_id=eleve_id,
        cours_semestriel_id=examen.cours_semestriel_id
    ).first()
    
    if not inscription:
        return jsonify({'success': False, 'message': 'L\'élève n\'est pas inscrit à ce cours'}), 400
    
    # Vérifier si une note existe déjà pour cet élève et cet examen
    note_existante = NoteExamen.query.filter_by(
        examen_id=examen_id,
        eleve_id=eleve_id
    ).first()
    
    if note_existante:
        return jsonify({
            'success': False,
            'message': 'Une note existe déjà pour cet élève. Utilisez la méthode PUT pour la modifier.',
            'note_id': note_existante.id
        }), 409  # Conflict HTTP status
    
    # Créer une nouvelle note
    nouvelle_note = NoteExamen(
        examen_id=examen_id,
        eleve_id=eleve_id,
        note=note_valeur,
        explication=explication
    )
    
    # Sauvegarder la nouvelle note
    try:
        db.session.add(nouvelle_note)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Note attribuée avec succès',
            'note': {
                'id': nouvelle_note.id,
                'examen_id': examen_id,
                'eleve_id': eleve_id,
                'note': note_valeur,
                'explication': explication
            }
        }), 201  # Created HTTP status
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de l\'attribution de la note: {str(e)}'
        }), 500


# Endpoint pour modifier une note existante
@examen_bp.route('/<int:examen_id>/notes/<int:eleve_id>', methods=['PUT'])
@jwt_required()
def modifier_note_examen(examen_id, eleve_id):
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not enseignant:
        return jsonify({'success': False, 'message': 'Enseignant non trouvé'}), 404
    
    # Récupérer les données du corps de la requête
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Aucune donnée fournie'}), 400
    
    # Vérifier la présence des champs obligatoires
    if 'note' not in data:
        return jsonify({'success': False, 'message': 'La note est obligatoire'}), 400
    
    note_valeur = data['note']
    explication = data.get('explication')  # Optionnel - peut être None
    
    # Vérifier que la note est dans une plage valide (0-20)
    if not (isinstance(note_valeur, (int, float)) and 0 <= note_valeur <= 20):
        return jsonify({'success': False, 'message': 'La note doit être un nombre compris entre 0 et 20'}), 400
    
    # Vérifier que l'examen existe
    examen = Examen.query.get(examen_id)
    if not examen:
        return jsonify({'success': False, 'message': 'Examen non trouvé'}), 404
    
    # Vérifier que l'enseignant est bien responsable du cours
    cours_sem = CoursSemestriel.query.get(examen.cours_semestriel_id)
    if not cours_sem or cours_sem.enseignant_id != enseignant.id:
        return jsonify({'success': False, 'message': 'Vous n\'êtes pas autorisé à modifier des notes pour cet examen'}), 403
    
    # Vérifier que l'élève existe
    eleve = Eleve.query.get(eleve_id)
    if not eleve:
        return jsonify({'success': False, 'message': 'Élève non trouvé'}), 404
    
    # Rechercher la note existante
    note_existante = NoteExamen.query.filter_by(
        examen_id=examen_id,
        eleve_id=eleve_id
    ).first()
    
    if not note_existante:
        return jsonify({
            'success': False,
            'message': 'Aucune note existante trouvée pour cet élève et cet examen'
        }), 404
    
    # Mettre à jour la note
    note_existante.note = note_valeur
    if explication is not None:  # Ne mettre à jour que si fourni
        note_existante.explication = explication
    
    # Sauvegarder les modifications
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Note modifiée avec succès',
            'note': {
                'id': note_existante.id,
                'examen_id': examen_id,
                'eleve_id': eleve_id,
                'note': note_valeur,
                'explication': note_existante.explication
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la modification de la note: {str(e)}'
        }), 500
        
    
# Afficher les eleves qui ont passé un examen
# Endpoint pour afficher les élèves d'un examen spécifique
@examen_bp.route('/api/examen/<int:examen_id>/eleves', methods=['GET'])
def get_eleves_by_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)
    cours_id = examen.cours_semestriel_id

    inscriptions = Inscription.query.filter_by(cours_semestriel_id=cours_id).all()
    if not inscriptions:
        return jsonify({'message': 'Aucun élève inscrit pour cet examen'}), 404

    eleves_ids = [inscription.eleve_id for inscription in inscriptions]
    
    eleves = Eleve.query.filter(Eleve.id.in_(eleves_ids)).all()
    if not eleves:
        return jsonify({'message': 'Aucun élève trouvé pour cet examen'}), 404

    return jsonify([eleve.to_dict() for eleve in eleves]), 200

# Route pour que l'enseignant voit ses notes d'examen
@examen_bp.route('/api/notes', methods=['GET'])
@jwt_required()
def get_notes_par_enseignant():
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not enseignant:
        return jsonify({'success': False, 'message': 'Enseignant non trouvé'}), 404

    examens = Examen.query.join(CoursSemestriel).filter(CoursSemestriel.enseignant_id == enseignant.id).all()
    examens_ids = [ex.id for ex in examens]

    notes = NoteExamen.query.filter(NoteExamen.examen_id.in_(examens_ids)).all()
    
    result = []
    for note in notes:
        eleve = note.eleve
        examen = note.examen
        cours_semestriel = examen.cours_semestriel
        cours = cours_semestriel.cours

        result.append({
            'note_id': note.id,
            'note': note.note,
            'explication': note.explication,
            'eleve': {
                'id': eleve.id,
                'nom': eleve.nom,
                'prenom': eleve.prenom
            },
            'examen': {
                'id': examen.id,
                'type': examen.type_examen,
                'titre_cours': cours.titre
            }
        })
    
    return jsonify(result), 200


# Notes de l'étudiant
@examen_bp.route('/api/mes-notes', methods=['GET'])
@jwt_required()
def get_notes_etudiant():
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()

    if not utilisateur or utilisateur.role != 'Eleve':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403

    eleve = Eleve.query.filter_by(utilisateur_id=utilisateur.id).first()
    if not eleve:
        return jsonify({'success': False, 'message': 'Élève non trouvé'}), 404

    notes = NoteExamen.query.filter_by(eleve_id=eleve.id).all()

    result = []
    for note in notes:
        examen = note.examen
        cours_semestriel = examen.cours_semestriel
        cours = cours_semestriel.cours

        result.append({
            'note_id': note.id,
            'note': note.note,
            'explication': note.explication,
            'examen': {
                'id': examen.id,
                'type': examen.type_examen,
                'date': examen.date.strftime('%Y-%m-%d'),
                'cours': {
                    'id': cours.id,
                    'titre': cours.titre
                }
            }
        })

    return jsonify(result), 200

# Route pour qu'un enseignant modifie un examen
@examen_bp.route('/api/examen/<int:id>', methods=['PUT'])
@jwt_required()
def modifier_examen(id):
    data = request.get_json()
    
    email = get_jwt_identity()
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    
    if not utilisateur or utilisateur.role != 'Enseignant':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403

    examen = Examen.query.get_or_404(id)

    nouveau_type = data.get('type_examen')
    nouvelle_date = data.get('date')

    if nouveau_type:
        if nouveau_type not in ['Partiel', 'Final', 'Rattrapage']:
            return jsonify({'success': False, 'message': 'Type d\'examen invalide'}), 400
        examen.type_examen = nouveau_type

    if nouvelle_date:
        try:
            from datetime import datetime
            examen.date = datetime.strptime(nouvelle_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Format de date invalide. Utiliser YYYY-MM-DD.'}), 400

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Examen modifié',
        'examen': {
            'id': examen.id,
            'type_examen': examen.type_examen,
            'date': examen.date.strftime('%Y-%m-%d')
        }
    }), 200
