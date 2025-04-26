import React, { useState, useEffect } from 'react';
import './modal.css'; 

const ExamenModal = ({ isOpen, onClose, examen, onSave }) => {
  const [formData, setFormData] = useState({
    type_examen: '',
    date: ''
  });

  useEffect(() => {
    if (examen) {
      setFormData({
        type_examen: examen.type_examen || '',
        date: examen.date || ''
      });
    }
  }, [examen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = () => {
    onSave({ ...examen, ...formData });
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Modifier l'Examen</h2>

        <label>
          Type d'examen:
          <select name="type_examen" value={formData.type_examen} onChange={handleChange}>
            <option value="">-- Sélectionner --</option>
            <option value="Partiel">Partiel</option>
            <option value="Final">Final</option>
            <option value="Rattrapage">Rattrapage</option>
          </select>
        </label>

        <label>
          Date:
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
          />
        </label>

        <div style={{ marginTop: '15px' }} className='modal-buttons'>
          <button onClick={handleSubmit} className='modal-valider-button'>Valider</button>
          <button className='modal-annuler-button' onClick={onClose} style={{ marginLeft: '10px' }}>Annuler</button>
        </div>
      </div>
    </div>
  );
};

export default ExamenModal;
