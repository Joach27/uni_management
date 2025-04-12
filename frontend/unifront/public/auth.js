import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Création du contexte Auth
const AuthContext = createContext();

// Provider pour envelopper l'application
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Vérifier si un utilisateur est déjà connecté à chaque chargement de la page
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));  // Récupérer les données utilisateur stockées
    }
  }, []);

  const register = async (prenom, nom, email, password, role, telephone, fonction, annee) => {
    try {
      const response = await axios.post(`${API_URL}/inscription`, {prenom, nom, email, password, role, telephone, fonction, annee});
      return response.data;
    } catch (error) {
      return error.response.data;
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API_URL}/login`, {email, password});
      localStorage.setItem("role", response.data.role);
      localStorage.setItem("user", JSON.stringify(response.data)); // Stocker l'utilisateur dans le localStorage
      setUser(response.data);  // Mettre à jour l'état local de l'utilisateur
      return response.data;
    } catch (error) {
      return error.response.data;
    }
  };

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("role");
    setUser(null);  // Supprimer l'utilisateur de l'état local
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook personnalisé pour accéder au contexte Auth
export const useAuth = () => {
  return useContext(AuthContext);
};



{/* <button onClick={handleLogout} className="logout-btn">
                Se déconnecter
            </button>
const handleLogout = () => {
  const confirmLogout = window.confirm("Êtes-vous sûr de vouloir vous déconnecter ?");
  if (confirmLogout) {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      alert("Vous êtes déconnecté !");
      navigate("/login");  // Redirection après déconnexion
  }
} */}


// from flask_jwt_extended import jwt_required, get_jwt_identity

// # Route pour afficher les cours semestriels de l'enseignant connecté
// @app.route('/api/enseignant/cours_semestriel', methods=['GET'])
// @jwt_required()
// def get_cours_semestriel_par_token():
//     # Récupérer l'identifiant de l'utilisateur depuis le JWT
//     user_id = get_jwt_identity()
    
//     # Trouver l'utilisateur
//     utilisateur = Utilisateur.query.get(user_id)
//     if not utilisateur or utilisateur.role != 'Enseignant':
//         return jsonify({"message": "Utilisateur non autorisé"}), 403

//     # Trouver l'enseignant lié à cet utilisateur
//     enseignant = Enseignant.query.filter_by(utilisateur_id=utilisateur.id).first()
//     if not enseignant:
//         return jsonify({"message": "Enseignant non trouvé"}), 404

//     # Récupérer les cours semestriels de cet enseignant
//     cours_semestriels = (
//         db.session.query(CoursSemestriel, Cours)
//         .join(Cours, Cours.id == CoursSemestriel.cours_id)
//         .filter(CoursSemestriel.enseignant_id == enseignant.id)
//         .all()
//     )

//     # Formater le résultat
//     result = []
//     for cours_semestriel, cours in cours_semestriels:
//         result.append({
//             'id': cours_semestriel.id,
//             'cours_id': cours_semestriel.cours_id,
//             'enseignant_id': cours_semestriel.enseignant_id,
//             'semestre': cours_semestriel.semestre,
//             'annee': cours_semestriel.annee,
//             'titre': cours.titre
//         })
    
//     return jsonify(result)
