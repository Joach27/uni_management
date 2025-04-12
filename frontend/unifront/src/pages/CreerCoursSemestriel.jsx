import { useState, useEffect } from 'react';
import axios from 'axios';

const CreerCoursSemestriel = () => {
    const [coursList, setCoursList] = useState([]); // Liste des cours disponibles
    const [enseignants, setEnseignants] = useState([]); // Liste des enseignants disponibles
    const [formData, setFormData] = useState({
        cours_id: "",
        enseignant_id: "",
        semestre: "S1", // Valeur par défaut
        annee: new Date().getFullYear(), // Valeur par défaut
    });
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // Charger la liste des cours et des enseignants
    useEffect(() => {
        // Récupérer les cours disponibles
        axios.get('http://localhost:5000/api/cours')
            .then(response => setCoursList(response.data))
            .catch(error => setErrorMessage('Erreur lors du chargement des cours'));

        // Récupérer les enseignants disponibles
        axios.get('http://localhost:5000/api/enseignants')
            .then(response => setEnseignants(response.data))
            .catch(error => setErrorMessage('Erreur lors du chargement des enseignants'));
    }, []);

    // Gérer les changements dans les champs du formulaire
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    // Soumettre le formulaire pour créer un cours semestriel
    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:5000/api/cours_semestriel', formData, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        })
        .then(response => {
            setSuccessMessage('Cours semestriel créé avec succès!');
            setTimeout(() => setSuccessMessage(''), 2000);
            setFormData({
                cours_id: "",
                enseignant_id: "",
                semestre: "S1", // Valeur par défaut
                annee: new Date().getFullYear(), // Valeur par défaut
            });
        })
        .catch(error => {
            setErrorMessage('Erreur lors de la création du cours semestriel');
            setTimeout(() => setErrorMessage(''), 2000);
        });
    };

    return (
        <div className="creer-cours-semestriel">
            <h2>Créer un cours semestriel</h2>
            <form onSubmit={handleSubmit} className='form-creation-cours-semestriel'>
               
               <div>
                    <label htmlFor="cours_id">Choisir un cours</label>
                    <select
                        name="cours_id"
                        value={formData.cours_id}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Sélectionner un cours</option>
                        {coursList.map(cours => (
                            <option key={cours.id} value={cours.id}>{cours.titre}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="enseignant_id">Choisir un enseignant  </label>
                    <select
                        name="enseignant_id"
                        value={formData.enseignant_id}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Sélectionner un enseignant</option>
                        {enseignants.map(enseignant => (
                            <option key={enseignant.id} value={enseignant.id}>
                                {enseignant.nom} {enseignant.prenom}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="semestre">Semestre</label>
                    <select
                        name="semestre"
                        value={formData.semestre}
                        onChange={handleChange}
                        required
                    >
                        <option value="S1">S1</option>
                        <option value="S2">S2</option>
                    </select>
                </div>

                <div>
                    <label htmlFor="annee">Année :</label>
                    <input
                        type="number"
                        name="annee"
                        value={formData.annee}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit">Créer le cours semestriel</button>

                {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
                {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            </form>
        </div>
    );
};

export default CreerCoursSemestriel;
