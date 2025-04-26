import React, { useState, useEffect } from 'react';
import './modal.css'; // pour un peu de style

const EleveModal = ({ isOpen, onClose, eleve, onSave }) => {
  const [formData, setFormData] = useState({
    prenom: '',
    nom: '',
    annee: ''
  });

  useEffect(() => {
    if (eleve) {
      setFormData({
        prenom: eleve.prenom || '',
        nom: eleve.nom || '',
        annee: eleve.annee || ''
      });
    }
  }, [eleve]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = () => {
    onSave({ ...eleve, ...formData }); // callback vers le parent
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Modifier Elève</h2>
        <label>
          Prénom:
          <input name="prenom" value={formData.prenom} onChange={handleChange} />
        </label>
        <label>
          Nom:
          <input name="nom" value={formData.nom} onChange={handleChange} />
        </label>
        <label>
          Année:
          <input name="annee" value={formData.telephone} onChange={handleChange} />
        </label>

        <div style={{ marginTop: '15px' }} className='modal-buttons'>
          <button onClick={handleSubmit} className='modal-valider-button'>Valider</button>
          <button onClick={onClose} style={{ marginLeft: '10px' }} className='.modal-annuler-button'>Annuler</button>
        </div>
      </div>
    </div>
  );
};

export default EleveModal;
