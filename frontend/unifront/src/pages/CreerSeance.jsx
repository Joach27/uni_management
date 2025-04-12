import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../AuthContext";

const CreerSeance = () => {
    const [courseSemestriels, setCourseSemestriels] = useState([]);
    const [formData, setFormData] = useState({
        cours_semestriel_id: "",
        duree: "",
        description: "",
        salle: ""
    });
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const  { userData } = useAuth();

    const user_email = userData.sub; // Récupérer l'ID de l'utilisateur connecté

    // Charger la liste des cours semestriels disponibles
    useEffect(() => {
        axios.get(`http://localhost:5000/api/enseignant/email/${user_email}/cours_semestriel`)
        .then(response => {
            setCourseSemestriels(response.data);
            console.log(response.data);
        })
        .catch(error => {
            console.error('Erreur lors de la chargement des cours semestriels', error);
        });
    }, [user_email]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:5000/api/seance', formData)
        .then(response => {
            setSuccessMessage('Séance crée avec succès!');
            setTimeout(() => setSuccessMessage(''), 2000);
            setFormData({
                cours_semestriel_id: "",
                duree: "",
                description: "",
                salle: ""
            });
        })
        .catch(error => {
            setErrorMessage('Erreur lors de la création de la séance');
            setTimeout(() => setErrorMessage(''), 2000);
        });
    };

    return (
        <div className="creer-seance">
            <h2>Créer une séance</h2>
            <form onSubmit={handleSubmit} className="form-creer-seance">
                <label htmlFor="cours_semestriel_id">Cours semestriel</label>
                <select name="cours_semestriel_id" value={formData.cours_semestriel_id} onChange={handleChange} required>
                    <option value="">-- Sélectionner un cours --</option>
                    {courseSemestriels.map((cours) => (
                        <option key={cours.id} value={cours.id}>{cours.titre}</option>
                    ))}
                </select>

                <label htmlFor="duree">Duree</label>
                <input type="text" name="duree" value={formData.duree} onChange={handleChange} required />

                <label htmlFor="description">Description</label>
                <input type="text" name="description" value={formData.description} onChange={handleChange} required />

                <label htmlFor="salle">Salle</label>
                <input type="text" name="salle" value={formData.salle} onChange={handleChange} required />

                <button type="submit">Créer la séance</button>
                {successMessage && <p className="success">{successMessage}</p>}
                {errorMessage && <p className="error">{errorMessage}</p>}
            </form>
        </div>
    );
}

export default CreerSeance;