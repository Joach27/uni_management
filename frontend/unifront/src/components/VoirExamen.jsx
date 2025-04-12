import { useState, useEffect } from "react";
import axios from "axios";
import './creerexamen.css'


const VoirExamen = () => {
    const [examens, setExamens] = useState([]);
    const [loading, setLoading] = useState(true);   
    const [error, setError] = useState(null);

    useEffect(() => {
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
            }
        };
        fetchExamens();
    }, []);

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
                                        <button className="modifier">Modifier</button>
                                        <button className="supprimer">Supprimer</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                        
                    </table>
                )
            }
        </div>
    );
}

export default VoirExamen;