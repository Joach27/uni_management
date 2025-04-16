import { useEffect, useState } from "react";
import axios from "axios";
import './seance.css';

const SeancesEnseignant = () => {
    const [seances, setSeances] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchEleveEtSeances = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/enseignant/seances', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    }
                });
                setSeances(response.data);
                setLoading(false);
            } catch (err) {
                console.error(err);
                setError("Erreur lors de la récupération des données.");
                setLoading(false);
            }
        };

        fetchEleveEtSeances();
    }, []);

    return (
        <div className="seances-eleve">  
            <h2>Mes séances</h2>
            {loading ? (
                <p>Chargement...</p>
            ) : error ? (
                <p style={{ color: "red" }}>{error}</p>
            ) : seances.length === 0 ? (
                <p>Vous n'avez aucune séance pour le moment.</p>
            ) : (
                <div className="seances-table-div">
                    <table className="table-seances">
                        <thead>
                            <tr>
                            <th>Description</th>
                            <th>Durée</th>
                            </tr>
                        </thead>
                        <tbody>
                            {seances.map(seance => (
                            <tr key={seance.id}>
                                <td>{seance.description}</td>
                                <td>{seance.duree} Hrs</td>
                            </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

            )}
        </div>
    );    
};

export default SeancesEnseignant;
