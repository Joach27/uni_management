pip install flask



from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), unique=True, nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    tel = db.Column(db.String(15))
    fonction = db.Column(db.String(50), nullable=False)
    
    
    
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # vérification fictive
    if username == 'admin' and password == 'password':
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    return jsonify(msg="Identifiants invalides"), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)

if __name__ == '__main__':
    app.run(debug=True)
    

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Appel API avec Axios
    axios.get('https://jsonplaceholder.typicode.com/users')
      .then(response => {
        setUsers(response.data); 
      })
      .catch(error => {
        console.error('Erreur lors de la récupération des données :', error);
      });
  }, []);

  return (
    <div>
      <h1>Liste des utilisateurs</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name} – {user.email}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;


SELECT titre, heures FROM cours;

SELECT e.nom, e.prenom, c.titre, n.note
FROM note_examen n
JOIN examen ex ON n.examen_id = ex.id
JOIN cours_semestriel cs ON ex.cours_semestriel_id = cs.id
JOIN cours c ON cs.cours_id = c.id
JOIN eleve e ON n.eleve_id = e.id
WHERE e.id = :eleve_id;


SELECT AVG(note) as moyenne
FROM note_examen
WHERE eleve_id = :eleve_id;

SELECT MAX(note) as note_max
FROM note_examen
WHERE eleve_id = :eleve_id;

