import { useState, useEffect } from "react";
import axios from "axios";
import './creerexercice.css';

const CreerExercice = () => {
    const [seanceId, setSeanceId] = useState("");
    const [contenu, setContenu] = useState("");
    const [type, setType] = useState("TD");
    const [seances, setSeances] = useState([]);
    const [message, setMessage] = useState("");

    const token = localStorage.getItem("token");

    useEffect(() => {
        // Charger les séances liées à l'enseignant connecté
        const fetchSeances = async () => {
            try {
                const res = await axios.get("http://localhost:5000/api/enseignant/seances", {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setSeances(res.data);
                console.log("Séances chargées :", res.data);
            } catch (err) {
                console.error("Erreur lors du chargement des séances", err);

                console.error("Réponse d'erreur : ", err.response);
                console.error("Statut HTTP : ", err.response.status);
                console.error("Message d'erreur : ", err.response.data);
            }
        };
        fetchSeances();
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://localhost:5000/api/exercices", {
                seance_id: seanceId,
                contenu,
                type
            }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setMessage("Exercice créé avec succès !");
            setContenu("");
            setSeanceId("");
            setType("TD");
        } catch (err) {
            setMessage("Erreur lors de la création : " + err.response?.data?.message || "Erreur inconnue");
        }
    };

    return (
        <div className="creer-exercice">
            <h2>Créer un Exercice</h2>
            <form onSubmit={handleSubmit} className="form-creer-exercice">
                <label>Séance :</label>
                <select value={seanceId} onChange={e => setSeanceId(e.target.value)} required>
                    <option value="">Sélectionner une séance</option>
                    {seances.map(seance => (
                        <option key={seance.id} value={seance.id}>
                            {`Séance ${seance.id} - ${seance.description || "Sans description"}`}
                        </option>
                    ))}
                </select>

                <label>Contenu :</label>
                <textarea
                    value={contenu}
                    onChange={e => setContenu(e.target.value)}
                    required
                />

                <label>Type :</label>
                <select value={type} onChange={e => setType(e.target.value)} required>
                    <option value="TD">TD</option>
                    <option value="TP">TP</option>
                    <option value="CM">CM</option>
                </select>

                <button type="submit">Créer l’exercice</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default CreerExercice;
