import { useState, useEffect } from 'react';
import axios from 'axios';
import './user.css';
import EnseignantModal from './EnseignantModal';

const ListeEnseignants = () => {
    const [enseignants, setEseignants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [deleteError, setDeleteError] = useState("");
    const [deleteSuccess, setDeleteSuccess] = useState("");

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedEnseignant, setSelectedEnseignant] = useState(null);

    const fetchEnseignants = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/enseignants', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            });
            setEseignants(response.data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEnseignants();
    }, []);


    const openModal = (enseignant) => {
        setSelectedEnseignant(enseignant);
        setIsModalOpen(true);
    };

    const handleSave = async (updatedEnseignant) => {
        await axios.put(`http://localhost:5000/api/enseignant/${updatedEnseignant.id}`, updatedEnseignant, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        });
        fetchEnseignants();
    };
    

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/enseignant/${id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            });
            setEseignants(enseignants.filter((eleve) => eleve.id !== id));
            setDeleteSuccess("Enseignant supprimé avec succès!");
        } catch (error) {
            setDeleteError(error.message);
        }
    };

    return (
        <div className='liste-enseignants'>
            <h2>Liste des enseignants</h2>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <table className='table-enseignants'>
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Prenom</th>
                            <th>Téléphone</th>
                            <th>Fonction</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {enseignants.map((enseignant) => (
                            <tr key={enseignant.id}>
                                <td>{enseignant.nom}</td>
                                <td>{enseignant.prenom}</td>
                                <td>{enseignant.telephone}</td>
                                <td>{enseignant.fonction}</td>
                                <td>
                                    <button onClick={() => openModal(enseignant)} className='modifier'>Modifier</button>
                                    <button className='supprimer' onClick={() => handleDelete(enseignant.id)}>Supprimer</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            {deleteError && (
                <p style={{ color: 'red' }}>{deleteError}</p>
            )}
            {deleteSuccess && (
                <p style={{ color: 'green' }}>{deleteSuccess}</p>
            )}

            <EnseignantModal 
                isOpen={isModalOpen} 
                onClose={() => setIsModalOpen(false)} enseignant={selectedEnseignant} onSave={handleSave} 
            />
        
        </div>
    );
}

export default ListeEnseignants;