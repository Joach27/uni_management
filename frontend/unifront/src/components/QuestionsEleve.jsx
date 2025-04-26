import { useState } from 'react';
import axios from 'axios';
import './questions.css'; // Crée un fichier CSS avec les styles décrits ci-dessous

const QuestionsEleve = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchParams, setSearchParams] = useState({
    nom: '',
    prenom: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!searchParams.nom) {
      setError('Le nom est requis pour effectuer la recherche');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');

      const queryParams = new URLSearchParams();
      queryParams.append('nom', searchParams.nom);
      if (searchParams.prenom) {
        queryParams.append('prenom', searchParams.prenom);
      }

      const response = await axios.get(`/api/eleve/questions?${queryParams.toString()}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setQuestions(response.data.questions);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la recherche des questions');
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

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
    <div className="conteneur-principal">
      <h1 className="titre-principal">Rechercher les questions d'un élève</h1>

      <form onSubmit={handleSubmit} className="formulaire-recherche">
        <div className="grille-formulaire">
          <div className="champ-formulaire">
            <label htmlFor="nom" className="etiquette-champ">
              Nom de l'élève *
            </label>
            <input
              type="text"
              id="nom"
              name="nom"
              value={searchParams.nom}
              onChange={handleChange}
              className="champ-texte"
              required
            />
          </div>

          <div className="champ-formulaire">
            <label htmlFor="prenom" className="etiquette-champ">
              Prénom de l'élève (optionnel)
            </label>
            <input
              type="text"
              id="prenom"
              name="prenom"
              value={searchParams.prenom}
              onChange={handleChange}
              className="champ-texte"
            />
          </div>
        </div>

        <div className="bouton-conteneur">
          <button
            type="submit"
            className="bouton-recherche"
            disabled={loading || !searchParams.nom}
          >
            {loading ? 'Recherche en cours...' : 'Rechercher'}
          </button>
        </div>
      </form>

      {error && (
        <div className="message-erreur">
          <p>{error}</p>
        </div>
      )}

      {questions.length > 0 && (
        <div className="tableau-conteneur">
          <h2 className="titre-tableau">Résultats ({questions.length})</h2>
          <table className="tableau-questions">
            <thead>
              <tr className="ligne-entete">
                <th>Séance</th>
                <th>Élève</th>
                <th>Question</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {questions.map((question) => (
                <tr key={question.id} className="ligne-tableau">
                  <td>{question.seance_description || `Séance #${question.seance_id}`}</td>
                  <td>{`${question.eleve_prenom} ${question.eleve_nom}`}</td>
                  <td>{question.contenu}</td>
                  <td>{formatDate(question.date_question)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && questions.length === 0 && searchParams.nom && (
        <div className="message-vide">
          <p>Aucune question trouvée pour cet élève.</p>
        </div>
      )}
    </div>
  );
};

export default QuestionsEleve;
