import { useState, useEffect } from "react";
import axios from "axios";
import './creerexamen.css';
import ExamenModal from "./ExamenModal";


const VoirExamen = () => {
    const [examens, setExamens] = useState([]);
    const [loading, setLoading] = useState(true);   
    const [error, setError] = useState(null);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedExamen, setSelectedExamen] = useState(null);

    const [modalError, setModalError] = useState(null);

    const fetchExamens = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/enseignant/examens', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            setExamens(response.data);
            setLoading(false);
        } catch (error) {
            setError(error.message);
            setLoading(false);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchExamens();
    }, []);

    const openModal = (examen) => {
        setSelectedExamen(examen);
        setIsModalOpen(true);
    };

    const handleSave = async (updatedExamen) => {
        try {
            await axios.put(`http://localhost:5000/api/examen/${updatedExamen.id}`, updatedExamen, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }       
            });
            fetchExamens(); // Refresh the list after saving    
        } catch (error) {
            setModalError(error.message);
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/examen/${id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            fetchExamens(); // Refresh the list after deleting
        } catch (error) {
            setModalError(error.message);
        }
    };  

    return (
        <div className="voir-examen-container">
            <h2>Les examens que j'ai crée</h2>
            <p style={{fontSize: '15px'}}>Les exames que vous avez crée</p>
            {
                loading ? (
                    <p>Loading...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : (
                    <table className="table-examens">
                        <thead>
                            <tr>
                                <th>Type d'examen</th>
                                <th>Date</th>
                                <th>Cours</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {examens.map((examen) => (
                                <tr key={examen.id}>
                                    <td>{examen.type_examen}</td>
                                    <td>{examen.date}</td>
                                    <td>{examen.cours.titre}</td>
                                    <td>
                                        <button onClick={() => openModal(examen)} className="modifier">Modifier</button>
                                        <button onClick={() => handleDelete(examen.id)} className="supprimer">Supprimer</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                        
                    </table>
                )
            }

            {modalError && <p className="error">{modalError}</p>}            

            <ExamenModal
                isOpen={isModalOpen}
                examen={selectedExamen}
                onClose={() => setIsModalOpen(false)}
                onSave={handleSave}
            />
        </div>
    );
};

export default VoirExamen;