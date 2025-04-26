import { useState } from 'react';
import axios from 'axios';
import './creercours.css';

const CreerCours = () => {
    const [coursInfo, setCoursInfo] = useState({
        titre: "",
        description: "",
        heures: 0,
        type: ""
    });
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    // Gérer le changement des champs
    const handleChange = (e) => {
        setCoursInfo({
            ...coursInfo,
            [e.target.name]: e.target.value
        });
    }

    // Fonction pour gérer la soumission du formulaire
    const handleSubmit = async (e) => {
        e.preventDefault();  // Empêche le rechargement de la page par défaut

        try {
            const response = await axios.post("http://localhost:5000/api/cours", coursInfo, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                }
            });
            setSuccess("Cours créé avec succès !");
            setTimeout(() => setSuccess(""), 2000);  // Efface le message après 2 secondes
            // Réinitialiser les champs du formulaire
            setCoursInfo({
                titre: "",
                description: "",
                heures: 0,
                type: ""
            });
        } catch (error) {
            setError(error.response ? error.response.data.message : error.message);
        }
    };

    return (
        <div className="creer-cours">
            <h2>Créer un cours</h2>
            <form className="form-creation-cours" onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    name="titre" 
                    placeholder="Titre du cours" 
                    value={coursInfo.titre} 
                    required 
                    onChange={handleChange} 
                />
                <textarea 
                    type="text" 
                    name="description" 
                    placeholder="Description" 
                    value={coursInfo.description} 
                    required 
                    onChange={handleChange} 
                />
                <label htmlFor='heures'>Nombre d'heures</label>
                <input 
                    type="number" 
                    name="heures" 
                    placeholder="Heures" 
                    value={coursInfo.heures} 
                    required 
                    onChange={handleChange} 
                />
                <input 
                    type="text" 
                    name="type" 
                    placeholder="Type" 
                    value={coursInfo.type} 
                    required 
                    onChange={handleChange} 
                />

                <button className="btn-creer-cours" type="submit">Créer le cours</button>

                {success && <p style={{ color: "blue", fontSize: "14px" }}>{success}</p>}
                {error && <p style={{ color: "red", fontSize: "14px" }}>{error}</p>}
            </form>
        </div>
    );
};

export default CreerCours;
