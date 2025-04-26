from operator import and_
from flask import Blueprint, current_app
from flask import jsonify, request
from models import db, NoteExamen
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import CoursSemestriel, Inscription, Examen, Eleve, Enseignant, Utilisateur, Question, Seance

from datetime import datetime

questions_bp = Blueprint('question', __name__)


questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/api/enseignant/questions', methods=['GET'])
@jwt_required()
def get_enseignant_questions():
    """
    Endpoint pour qu'un professeur puisse voir les questions posées lors de ses séances.
    Retourne les détails de chaque question: séance, nom de l'élève, contenu, date.
    """
    try:
        # Récupérer l'ID utilisateur depuis le token JWT
        current_user_email = get_jwt_identity()
        
        # Vérifier que l'utilisateur est bien un enseignant
        user = Utilisateur.query.get(email = current_user_email)
        if not user or user.role != 'Enseignant':
            return jsonify({'error': 'Accès refusé. Vous devez être un enseignant.'}), 403
        
        # Récupérer l'ID de l'enseignant
        enseignant = Enseignant.query.filter_by(utilisateur_id=user.id).first()
        if not enseignant:
            return jsonify({'error': 'Profil enseignant non trouvé.'}), 404
        
        # Récupérer les cours semestriels enseignés par ce prof
        cours_semestriels = CoursSemestriel.query.filter_by(enseignant_id=enseignant.id).all()
        cours_semestriels_ids = [cs.id for cs in cours_semestriels]
        
        # Récupérer les séances associées à ces cours
        seances = Seance.query.filter(Seance.cours_semestriel_id.in_(cours_semestriels_ids)).all()
        seances_ids = [seance.id for seance in seances]
        
        # Récupérer les questions posées pendant ces séances
        questions = db.session.query(
            Question, Seance, Eleve
        ).join(
            Seance, Question.seance_id == Seance.id
        ).join(
            Eleve, Question.eleve_id == Eleve.id
        ).filter(
            Question.seance_id.in_(seances_ids)
        ).all()
        
        # Formater les résultats
        questions_list = [{
            'id': question.id,
            'seance_id': question.seance_id,
            'seance_description': seance.description,
            'eleve_nom': eleve.nom,
            'eleve_prenom': eleve.prenom,
            'contenu': question.contenu,
            'date_question': question.date_question.strftime('%Y-%m-%d %H:%M:%S')
        } for question, seance, eleve in questions]
        
        return jsonify({
            'success': True,
            'questions': questions_list,
            'count': len(questions_list)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des questions: {str(e)}")
        return jsonify({'error': f'Une erreur est survenue: {str(e)}'}), 500


@questions_bp.route('/api/eleve/questions', methods=['GET'])
@jwt_required()
def get_eleve_questions_by_name():
    """
    Endpoint pour afficher les questions posées à un élève spécifique.
    Requiert un nom d'élève en paramètre de requête.
    """
    try:
        # Récupérer l'ID utilisateur depuis le token JWT
        current_user_email = get_jwt_identity()
        
        # Vérifier que l'utilisateur est soit un enseignant soit un admin
        user = Utilisateur.query.get(email = current_user_email)
        current_user_id = user.id if user else None
        
        if not user or user.role not in ['Enseignant', 'Admin']:
            return jsonify({'error': 'Accès refusé. Vous devez être un enseignant ou un administrateur.'}), 403
        
        # Récupérer les paramètres de recherche
        nom = request.args.get('nom')
        prenom = request.args.get('prenom')
        
        if not nom:
            return jsonify({'error': 'Le paramètre "nom" est requis.'}), 400
        
        # Construire la requête de base
        query = db.session.query(
            Question, Seance, Eleve
        ).join(
            Seance, Question.seance_id == Seance.id
        ).join(
            Eleve, Question.eleve_id == Eleve.id
        )
        
        # Filtrer par nom (et prénom si fourni)
        if prenom:
            query = query.filter(and_(Eleve.nom.ilike(f"%{nom}%"), Eleve.prenom.ilike(f"%{prenom}%")))
        else:
            query = query.filter(Eleve.nom.ilike(f"%{nom}%"))
        
        # Si c'est un enseignant, limiter aux séances qu'il enseigne
        if user.role == 'Enseignant':
            enseignant = Enseignant.query.filter_by(utilisateur_id=current_user_id).first()
            if not enseignant:
                return jsonify({'error': 'Profil enseignant non trouvé.'}), 404
            
            cours_semestriels = CoursSemestriel.query.filter_by(enseignant_id=enseignant.id).all()
            cours_semestriels_ids = [cs.id for cs in cours_semestriels]
            
            query = query.filter(Seance.cours_semestriel_id.in_(cours_semestriels_ids))
        
        # Exécuter la requête
        questions = query.all()
        
        # Formater les résultats
        questions_list = [{
            'id': question.id,
            'seance_id': question.seance_id,
            'seance_description': seance.description,
            'eleve_id': eleve.id,
            'eleve_nom': eleve.nom,
            'eleve_prenom': eleve.prenom,
            'contenu': question.contenu,
            'date_question': question.date_question.strftime('%Y-%m-%d %H:%M:%S')
        } for question, seance, eleve in questions]
        
        return jsonify({
            'success': True,
            'questions': questions_list,
            'count': len(questions_list)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la recherche des questions: {str(e)}")
        return jsonify({'error': f'Une erreur est survenue: {str(e)}'}), 500
    
    
# Route pour que l'enseignant puisse créer une question
@questions_bp.route('/api/enseignant/create-question', methods=['POST'])
@jwt_required()
def create_question():
    """
    Endpoint pour qu'un enseignant crée une question destinée à un étudiant spécifique.
    Requiert: seance_id, eleve_id, et contenu dans le corps de la requête.
    """
    try:
        # Récupérer l'ID utilisateur depuis le token JWT
        current_user_email = get_jwt_identity()
        
        # Vérifier que l'utilisateur est bien un enseignant
        user = Utilisateur.query.get(email = current_user_email)
        if not user or user.role != 'Enseignant':
            return jsonify({'error': 'Accès refusé. Vous devez être un enseignant.'}), 403
        
        # Récupérer l'ID de l'enseignant
        enseignant = Enseignant.query.filter_by(utilisateur_id=user.id).first()
        if not enseignant:
            return jsonify({'error': 'Profil enseignant non trouvé.'}), 404
        
        # Récupérer les données du corps de la requête
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Aucune donnée fournie.'}), 400
        
        seance_id = data.get('seance_id')
        eleve_id = data.get('eleve_id')
        contenu = data.get('contenu')
        
        # Vérifier que tous les champs requis sont présents
        if not all([seance_id, eleve_id, contenu]):
            return jsonify({'error': 'Tous les champs sont requis: seance_id, eleve_id, contenu'}), 400
        
        # Vérifier que la séance existe
        seance = Seance.query.get(seance_id)
        if not seance:
            return jsonify({'error': 'Séance non trouvée.'}), 404
        
        # Vérifier que l'enseignant est responsable de cette séance
        cours_semestriel = CoursSemestriel.query.get(seance.cours_semestriel_id)
        if not cours_semestriel or cours_semestriel.enseignant_id != enseignant.id:
            return jsonify({'error': 'Vous n\'êtes pas autorisé à créer des questions pour cette séance.'}), 403
        
        # Vérifier que l'élève existe
        eleve = Eleve.query.get(eleve_id)
        if not eleve:
            return jsonify({'error': 'Élève non trouvé.'}), 404
        
        # Vérifier que l'élève est inscrit à ce cours
        # Cette vérification est optionnelle et dépend de votre logique métier
        
        # Créer la nouvelle question
        nouvelle_question = Question(
            seance_id=seance_id,
            eleve_id=eleve_id,
            contenu=contenu,
            date_question=datetime.now()
        )
        
        # Ajouter et valider en base de données
        db.session.add(nouvelle_question)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Question créée avec succès.',
            'question': {
                'id': nouvelle_question.id,
                'seance_id': nouvelle_question.seance_id,
                'eleve_id': nouvelle_question.eleve_id,
                'contenu': nouvelle_question.contenu,
                'date_question': nouvelle_question.date_question.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur lors de la création de la question: {str(e)}")
        return jsonify({'error': f'Une erreur est survenue: {str(e)}'}), 500