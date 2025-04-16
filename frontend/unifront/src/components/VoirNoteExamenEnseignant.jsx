import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './note.css';

const VoirNoteExamenEnseignant = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const token = localStorage.getItem('token'); // Ton JWT
        const response = await axios.get('http://localhost:5000/api/notes', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setNotes(response.data);
      } catch (err) {
        console.error(err);
        setErreur("Erreur lors du chargement des notes");
      } finally {
        setLoading(false);
      }
    };

    fetchNotes();
  }, []);

  if (loading) return <p>Chargement des notes...</p>;
  if (erreur) return <p style={{ color: 'red' }}>{erreur}</p>;

  return (
    <div className='notes-examens-enseignant'>
      <h2>Notes des examens</h2>
      <table className='table-examens-enseignant'>
        <thead>
          <tr>
            <th>Élève</th>
            <th>Examen</th>
            <th>Titre du cours</th>
            <th>Note</th>
            <th>Explication</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {notes.map(note => (
            <tr key={note.note_id}>
              <td>{note.eleve.prenom} {note.eleve.nom}</td>
              <td>{note.examen.type}</td>
              <td>{note.examen.titre_cours}</td>
              <td>{note.note}</td>
              <td>{note.explication || '-'}</td>
              <td>
                <button className='modifier'>Modifier</button>
                <button className='supprimer'>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VoirNoteExamenEnseignant;
