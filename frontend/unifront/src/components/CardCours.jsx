import './cardcours.css';
import { useAuth } from '../AuthContext';   
import React, { useEffect, useState } from 'react'; 
import axios from 'axios';

const CardCours = ({cours}) => {
    const { userData } = useAuth(); 
    const user_mail = userData.sub;
    const [user, setUser] = useState({});
    const [isInscrit, setIsInscrit] = useState(cours.inscrit === 'oui');

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    useEffect(() => {
        const fecthUserByMail = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/api/eleve/email/${user_mail}`);
                setUser(response.data);
            } catch (error) {
                console.error(error);
            }
        };
        fecthUserByMail();
    }, [user_mail]);


    const handleInscription = async () => {
        try {
            const response = await axios.post(`http://localhost:5000/api/eleve/${user.id}/inscription`, {
                eleve_id: user.id,
                cours_semestriel_id: cours.id,
            });
            setSuccess("Inscription réussie!");
            setError("");
            setIsInscrit(true);
        } catch (error) {
            console.error(error);
            setError("Erreur lors de l'inscription!");
        }
    };

    return (
        <div className="card-cours">
            <div className="card-cours-content">
                <h3>{cours.cours.titre}</h3>
                <p>{cours.cours.description}</p>
            </div>
            <div className="card-cours-footer">
                <span>{cours.cours.type}</span>
                {isInscrit ? (
                    <span className='inscrit'>Inscrit</span>
                ) : (
                    <button onClick={handleInscription} disabled={success !== ""}>S'inscrire</button>
                )}
                <span>{cours.cours.heures} Hrs</span>
            </div>
             {/* Affichage des alertes si elles existent */}
            {error && <p className="error">{error}</p>}
            {success && <p className="success">{success}</p>}
        </div>
    );
};

export default CardCours;