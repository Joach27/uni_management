import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './questions.css';

// Composant pour afficher les questions posées lors des séances d'un enseignant
const QuestionEnseignant = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeacherQuestions = async () => {
      try {
        setLoading(true);
        // Récupérer le token JWT du localStorage
        const token = localStorage.getItem('token');
        
        const response = await axios.get('/api/enseignant/questions', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        console.log('Réponse:', response.data);
        // setQuestions(response.data.questions);
        setQuestions(Array.isArray(response.data.questions) ? response.data.questions : []);
        setError(null);
      } catch (err) {
        setError(err.response?.data?.error || 'Erreur lors de la récupération des questions');
        console.error('Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTeacherQuestions();
  }, []);

  // Fonction pour formater la date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('fr-FR', {
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <div className="questions-enseignants">
      <h2>Questions posées lors de mes séances</h2>
      
      {loading ? (
        <p> Loading...</p>
      ) : error ? (
          <p>{error}</p>
      ) : questions.length === 0 ? (
          <p>Aucune question n'a été posée lors de vos séances.</p>
      ) : (
        <div className="questions-enseignants-table-container">
          <table className="questions-enseignants-table">
            <thead>
              <tr>
                <th>Séance</th>
                <th>Élève</th>
                <th>Question</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {questions.map((question) => (
                <tr key={question.id}>
                  <td>{question.seance_description}</td>
                  <td>{`${question.eleve_prenom} ${question.eleve_nom}`}</td>
                  <td>{question.contenu}</td>
                  <td>{formatDate(question.date_question)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div> 
      )}
    </div>
  );
};

export default QuestionEnseignant;