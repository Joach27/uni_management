import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import './creerexamen.css';


const CreerExamen = () => {
    const [coursList, setCoursList] = useState([]); // Liste des cours semestriels disponibles
    const [successMessage, setSuccessMessage] = useState("");
    const { userData } = useAuth();
    const user_mail = userData.sub;
    const [error, setError] = useState("");
    const [examInfo, setExamInfo] = useState({
        cours_semestriel_id: "",
        type_examen: "",
        date: ""
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(""); // Réinitialise l'erreur
        try {
            const response = await axios.post("http://localhost:5000/api/examen/creer", examInfo, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                }
            });

            setSuccessMessage(response.data.message);
            setTimeout(() => setSuccessMessage(""), 3000);
            setExamInfo({
                cours_semestriel_id: "",
                type_examen: "",
                date: ""
            });
        } catch (error) {
            setError(error?.response?.data?.message || "Une erreur s'est produite");
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setExamInfo((prevState) => ({
            ...prevState,
            [name]: value
        }));
    };

    useEffect(() => {
        const fetchCours = async () => {
            try {
                const response = await axios.get("http://localhost:5000/api/enseignant/email/" + user_mail + "/cours_semestriel", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`
                    }
                });
                setCoursList(response.data); // On suppose que c'est une liste de cours semestriels
            } catch (err) {
                setError("Erreur lors du chargement des cours.");
            }
        };

        fetchCours();
    }, [user_mail]);

    return (
        <div className="creer-examen">
            <h2>Créer un examen</h2>

            <form className="creer-examen-form" onSubmit={handleSubmit}>
                <label htmlFor="cours_semestriel_id">Choisir un cours</label>
                <select 
                    name="cours_semestriel_id" 
                    value={examInfo.cours_semestriel_id}
                    onChange={handleChange}
                    required
                >
                    <option value="">Sélectionner un cours</option>
                    {coursList.map((cours) => (
                        <option key={cours.id} value={cours.id}>
                            {cours.titre}
                        </option>
                    ))}
                </select>

                <label htmlFor="type_examen">Type d'examen</label>
                <select 
                    name="type_examen"
                    value={examInfo.type_examen}
                    onChange={handleChange}
                    required
                >
                    <option value="">Sélectionner le type</option>
                    <option value="partiel">Partiel</option>
                    <option value="final">Final</option>
                    <option value="final">Rattrapage</option>
                </select>

                <label htmlFor="date">Date de l'examen</label>
                <input 
                    type="date" 
                    name="date" 
                    value={examInfo.date} 
                    onChange={handleChange} 
                    required 
                />

                <button type="submit" className="creer-examen-button">Créer l'examen</button>
            </form>

            {successMessage && <p className="success-message">{successMessage}</p>}
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

export default CreerExamen;
