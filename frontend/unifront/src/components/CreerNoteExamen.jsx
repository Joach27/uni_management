import React, { useEffect, useState } from 'react';
import axios from 'axios';
// import { useAuth } from '../AuthContext';
import './note.css';

const CreerNoteExamen= () => {
    // const { userData } = useAuth(); 
    const [examens, setExamens] = useState([]);
    const [eleves, setEleves] = useState([]);
    const [selectedExamen, setSelectedExamen] = useState('');
    const [selectedEleve, setSelectedEleve] = useState('');
    const [valeur, setValeur] = useState('');
    const [explication, setExplication] = useState('');
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');

    // const enseignant_id = userData.id;

    useEffect(() => {
        const fetchExamens = async () => {
            try {
                const res = await axios.get('http://localhost:5000/api/enseignant/examens', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`
                    }
                });
                setExamens(res.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchExamens();
    }, []);

    const handleExamenChange = async (e) => {
        const examenId = e.target.value;
        setSelectedExamen(examenId);
        setSelectedEleve('');
        try {
            const res = await axios.get(`http://localhost:5000/api/examen/${examenId}/eleves`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                }
            });
            setEleves(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`http://localhost:5000/api/examen/${selectedExamen}/notes`, {
                eleve_id: selectedEleve,
                examen_id: selectedExamen,
                note: parseFloat(valeur),
                explication: explication
            } , {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                }
            });
            setSuccess('Note ajoutée avec succès.');
            setError('');
            setExplication('');
            setValeur('');
            setSelectedEleve('');
            setSelectedExamen('');

        } catch (err) {
            setError(err.response.data.message);
            setSuccess('');
        }
    };

    return (
        <div className="attribution-note">
            <h2>Attribuer une note à un élève</h2>

            <form onSubmit={handleSubmit} className='form-creation-note'>
                <label>Examen :</label>
                <select value={selectedExamen} onChange={handleExamenChange} required>
                    <option value="">-- Choisir un examen --</option>
                    {examens.map(ex => (
                        <option key={ex.id} value={ex.id}>
                            {ex.type_examen} - {ex.cours.titre}
                        </option>
                    ))}
                </select>

                <label>Élève :</label>
                <select value={selectedEleve} onChange={(e) => setSelectedEleve(e.target.value)} required>
                    <option value="">-- Choisir un élève --</option>
                    {eleves.map(e => (
                        <option key={e.id} value={e.id}>
                            {e.nom} {e.prenom}
                        </option>
                    ))}
                </select>

                <label>Note :</label>
                <input
                    type="number"
                    value={valeur}
                    min={0}
                    max={20}
                    step={0.1}
                    onChange={(e) => setValeur(e.target.value)}
                    required
                />

                <label>Explication :</label>                
                <input
                    type="text"
                    value={explication}
                    onChange={(e) => setExplication(e.target.value)}
                />

                <button type="submit">Attribuer</button>
            </form>

            {success && <p className="success">{success}</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default CreerNoteExamen;