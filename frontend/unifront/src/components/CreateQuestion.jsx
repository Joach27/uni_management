import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './questions.css';

const CreateQuestion = () => {
  const [formData, setFormData] = useState({
    seance_id: '',
    eleve_id: '',
    contenu: ''
  });

  const [seances, setSeances] = useState([]);
  const [eleves, setEleves] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingSeances, setLoadingSeances] = useState(true);
  const [loadingEleves, setLoadingEleves] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchSeances = async () => {
      try {
        setLoadingSeances(true);
        const response = await axios.get('/api/enseignant/seances', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setSeances(response.data.seances || []);
        setError(null);
      } catch (err) {
        setError('Erreur lors du chargement des séances.');
      } finally {
        setLoadingSeances(false);
      }
    };
    fetchSeances();
  }, [token]);

  useEffect(() => {
    const fetchEleves = async () => {
      if (!formData.seance_id) return;
      try {
        setLoadingEleves(true);
        const response = await axios.get(`/api/cours-semestriel/eleves?seance_id=${formData.seance_id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setEleves(response.data.eleves || []);
        setError(null);
      } catch (err) {
        setError('Erreur lors du chargement des élèves.');
      } finally {
        setLoadingEleves(false);
      }
    };
    fetchEleves();
  }, [formData.seance_id, token]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null);
    setSuccess(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.seance_id || !formData.eleve_id || !formData.contenu.trim()) {
      setError('Tous les champs sont obligatoires.');
      return;
    }

    try {
      setLoading(true);
      await axios.post('/api/enseignant/create-question', formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setFormData(prev => ({ ...prev, contenu: '' }));
      setSuccess('Question créée avec succès!');
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la création de la question.');
      setSuccess(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="formulaire-conteneur">
      <h1 className="formulaire-titre">Poser une question à un élève</h1>

      <form onSubmit={handleSubmit} className="formulaire-carte">
        {error && <div className="message-erreur"><p>{error}</p></div>}
        {success && <div className="message-succes"><p>{success}</p></div>}

        <div className="champ-formulaire">
          <label htmlFor="seance_id" className="etiquette-champ">Séance *</label>
          <select
            id="seance_id"
            name="seance_id"
            value={formData.seance_id}
            onChange={handleChange}
            className="champ-select"
            disabled={loadingSeances}
            required
          >
            <option value="">Sélectionnez une séance</option>
            {seances.map(seance => (
              <option key={seance.id} value={seance.id}>
                {seance.description || `Séance #${seance.id}`} - {seance.salle || 'Salle non définie'}
              </option>
            ))}
          </select>
          {loadingSeances && <p className="info-texte">Chargement des séances...</p>}
        </div>

        <div className="champ-formulaire">
          <label htmlFor="eleve_id" className="etiquette-champ">Élève *</label>
          <select
            id="eleve_id"
            name="eleve_id"
            value={formData.eleve_id}
            onChange={handleChange}
            className="champ-select"
            disabled={!formData.seance_id || loadingEleves}
            required
          >
            <option value="">Sélectionnez un élève</option>
            {eleves.map(eleve => (
              <option key={eleve.id} value={eleve.id}>
                {eleve.prenom} {eleve.nom}
              </option>
            ))}
          </select>
          {formData.seance_id && loadingEleves && <p className="info-texte">Chargement des élèves...</p>}
          {!formData.seance_id && <p className="info-texte">Veuillez d'abord sélectionner une séance</p>}
        </div>

        <div className="champ-formulaire">
          <label htmlFor="contenu" className="etiquette-champ">Question *</label>
          <textarea
            id="contenu"
            name="contenu"
            value={formData.contenu}
            onChange={handleChange}
            rows="4"
            className="champ-textarea"
            placeholder="Saisissez votre question ici..."
            required
          ></textarea>
        </div>

        <div className="formulaire-bouton-container">
          <button
            type="submit"
            className="bouton-soumettre"
            disabled={loading || !formData.seance_id || !formData.eleve_id || !formData.contenu.trim()}
          >
            {loading ? 'Envoi en cours...' : 'Poser la question'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateQuestion;
