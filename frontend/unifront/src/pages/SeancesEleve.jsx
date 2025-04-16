import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../AuthContext";
import './seance.css';

const SeancesEleve = () => {
    const { userData } = useAuth();
    const user_mail = userData.sub; 
    const [user, setUser] = useState(null);
    const [seances, setSeances] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchEleveEtSeances = async () => {
            try {
                // 1. Récupération de l'élève par email
                const resUser = await axios.get(`http://localhost:5000/api/eleve/email/${user_mail}`);
                const eleve = resUser.data;
                setUser(eleve);

                // 2. Récupération des séances de l'élève
                const resSeances = await axios.get(`http://localhost:5000/api/eleve/${eleve.id}/seances`);
                setSeances(resSeances.data);
            } catch (err) {
                console.error(err);
                setError("Erreur lors de la récupération des données.");
            } finally {
                setLoading(false);
            }
        };

        fetchEleveEtSeances();
    }, [user_mail]);

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

export default SeancesEleve;
