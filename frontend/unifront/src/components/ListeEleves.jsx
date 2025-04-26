import { useState, useEffect } from 'react';
import axios from 'axios';
import './user.css';
import EleveModal from './EleveModal';

const ListeEleves = () => {
    const [eleves, setEleves] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [deleteError, setDeleteError] = useState("");
    const [deleteSuccess, setDeleteSuccess] = useState("");

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedEleve, setSelectedEleve] = useState(null);

    const fetchEleves = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/eleves', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            });
            setEleves(response.data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEleves();
    }, []);

    const openModal = (eleve) => {
        setSelectedEleve(eleve);
        setIsModalOpen(true);
    };

    const handleSave = async (updatedEleve) => {
        await axios.put(`http://localhost:5000/api/eleve/${updatedEleve.id}`, updatedEleve, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        });
        fetchEleves();
    };


    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/eleve/${id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
            });
            setEleves(eleves.filter((eleve) => eleve.id !== id));
            setDeleteSuccess("Élève supprimé avec succès!");
            fetchEleves();
        } catch (error) {

            setDeleteError(error.message);
        }
    };

    return (
        <div className='liste-eleves'>
            <h2>Liste des élèves</h2>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <table className='table-eleves'>
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Prenom</th>
                            <th>Année</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {eleves.map((eleve) => (
                            <tr key={eleve.id}>
                                <td>{eleve.nom}</td>
                                <td>{eleve.prenom}</td>
                                <td>{eleve.annee}</td>
                                <td>
                                    <button onClick={() => openModal(eleve)} className='modifier'>Modifier</button>
                                    <button className='supprimer' onClick={() => handleDelete(eleve.id)}>Supprimer</button>
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

            <EleveModal 
                isOpen={isModalOpen} 
                onClose={() => setIsModalOpen(false)} eleve={selectedEleve} onSave={handleSave} 
            />
        
        </div>
    );
}

export default ListeEleves;