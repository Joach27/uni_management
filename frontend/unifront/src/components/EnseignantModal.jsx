import React, { useState, useEffect } from 'react';
import './modal.css'; // pour un peu de style

const EnseignantModal = ({ isOpen, onClose, enseignant, onSave }) => {
  const [formData, setFormData] = useState({
    prenom: '',
    nom: '',
    telephone: '',
    fonction: ''
  });

  useEffect(() => {
    if (enseignant) {
      setFormData({
        prenom: enseignant.prenom || '',
        nom: enseignant.nom || '',
        telephone: enseignant.telephone || '',
        fonction: enseignant.fonction || ''
      });
    }
  }, [enseignant]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = () => {
    onSave({ ...enseignant, ...formData }); // callback vers le parent
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Modifier Enseignant</h2>
        <label>
          Prénom:
          <input name="prenom" value={formData.prenom} onChange={handleChange} />
        </label>
        <label>
          Nom:
          <input name="nom" value={formData.nom} onChange={handleChange} />
        </label>
        <label>
          Téléphone:
          <input name="telephone" value={formData.telephone} onChange={handleChange} />
        </label>
        <label>
          Fonction:
          <select name="fonction" value={formData.fonction} onChange={handleChange}>
            <option value="Vacataire">Vacataire</option>
            <option value="ATER">ATER</option>
            <option value="MdC">MdC</option>
            <option value="Professeur">Professeur</option>
          </select>
        </label>

        <div style={{ marginTop: '15px' }} className='modal-buttons'>
          <button onClick={handleSubmit} className='modal-valider-button' >Valider</button>
          <button onClick={onClose} style={{ marginLeft: '10px'}} id='modal-annuler' className='modal-annuler-button'>Annuler</button>
        </div>
      </div>
    </div>
  );
};

export default EnseignantModal;
