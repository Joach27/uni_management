import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CardCoursEleve from '../components/CardCoursEleve';
import { useAuth } from '../AuthContext';

const EleveCoursPage = () => {
    const { userData } = useAuth(); 
    const user_mail = userData.sub;

    const [user, setUser] = useState(null);
    const [cours, setCours] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchEleveEtCours = async () => {
            try {
                // 1. Récupérer l'élève via son email
                const resUser = await axios.get(`http://localhost:5000/api/eleve/email/${user_mail}`);
                const eleve = resUser.data;
                setUser(eleve);

                // 2. Récupérer ses cours
                const resCours = await axios.get(`http://localhost:5000/api/eleve/${eleve.id}/cours`);
                setCours(resCours.data);
                console.log(resCours.data);
            } catch (err) {
                console.error(err);
                setError("Impossible de charger les données. Veuillez réessayer.");
            } finally {
                setLoading(false);
            }
        };

        fetchEleveEtCours();
    }, [user_mail]);

    return (
        <div className='cours-inscrit'>
            <h2>Mes Cours</h2>
            <p>Ici, vous trouverez les cours auxquels vous êtes inscrit.</p>

            {loading ? (
                <p>Chargement des cours...</p>
            ) : error ? (
                <p style={{ color: 'red' }}>{error}</p>
            ) : cours.length === 0 ? (
                <p>Vous n'êtes inscrit à aucun cours pour le moment.</p>
            ) : (
                <div className="cours-list">
                    {cours.map((cs) => (
                        <CardCoursEleve key={cs.id} cours={cs} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default EleveCoursPage;
