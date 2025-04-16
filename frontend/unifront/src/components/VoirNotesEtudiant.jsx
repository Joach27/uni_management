import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './note.css'; // Assurez-vous d'avoir ce fichier CSS pour le style

const VoirNotesEtudiant = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const fetchMesNotes = async () => {
      try {
        const token = localStorage.getItem('token'); // JWT de l'étudiant
        const response = await axios.get('http://localhost:5000/api/mes-notes', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setNotes(response.data);
      } catch (err) {
        console.error(err);
        setErreur("Impossible de charger les notes.");
      } finally {
        setLoading(false);
      }
    };

    fetchMesNotes();
  }, []);

  if (loading) return <p>Chargement de vos notes...</p>;
  if (erreur) return <p style={{ color: 'red' }}>{erreur}</p>;

  return (
    <div className='notes-examen-eleve'>
      <h2>Mes Notes d'Examen</h2>
      {notes.length === 0 ? (
        <p>Vous n'avez pas encore de notes.</p>
      ) : (
        <table className='table-examens-eleve'>
          <thead>
            <tr>
              <th>Cours</th>
              <th>Type d'examen</th>
              <th>Date</th>
              <th>Note</th>
              <th>Explication</th>
            </tr>
          </thead>
          <tbody>
            {notes.map(note => (
              <tr key={note.note_id}>
                <td>{note.examen.cours.titre}</td>
                <td>{note.examen.type}</td>
                <td>{note.examen.date}</td>
                <td>{note.note}</td>
                <td>{note.explication || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default VoirNotesEtudiant;
