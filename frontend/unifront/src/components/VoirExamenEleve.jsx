import { useState, useEffect } from "react";
import axios from "axios";
import './creerexamen.css'


const VoirExamenEleve = () => {
    const [examens, setExamens] = useState([]);
    const [loading, setLoading] = useState(true);   
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchExamens = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/eleve/examens', {
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
            <h2>Mes examens</h2>
            <p style={{fontSize: '15px'}}>Mes examens de l'année</p>
            {
                loading ? (
                    <p>Loading...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : (
                    <div className='examens-table-div'>
                        <table className="table-examens">
                            <thead>
                                <tr>
                                    <th>Type d'examen</th>
                                    <th>Date</th>
                                    <th>Cours</th>
                                    <th>Etat</th>
                                </tr>
                            </thead>
                            <tbody>
                                {examens.map((examen) => (
                                    <tr key={examen.id}>
                                        <td>{examen.type_examen}</td>
                                        <td>{examen.date}</td>
                                        <td>{examen.cours.titre}</td>
                                        <td>
                                            {new Date(examen.date) < new Date() ? "Passé" : "À venir"}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                            
                        </table>
                    </div>
                )
            }
        </div>
    );
}

export default VoirExamenEleve;