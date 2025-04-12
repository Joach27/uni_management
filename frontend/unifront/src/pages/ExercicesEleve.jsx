import { useState, useEffect } from "react";
import axios from "axios";
import './seance.css'

const ExercicesEleve = () => {
  const [exercices, setExercices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExercices = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          "http://localhost:5000/api/eleve/exercices", 
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );
        setExercices(response.data);
        console.log(response.data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };
    fetchExercices();
  }, []);

  return (
    <div className="exercices-eleve">
      <h2>Mes exercices</h2>
      {loading ? (
        <p>Chargement...</p>
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : exercices.length === 0 ? (
        <p>Vous n'avez aucun exercice à rendre.</p>
      ) : (
        <div className="exercices-table-div">
          <table className="table-exercices">
            <thead>
              <tr>
                <th>Cours</th>
                <th>Description</th>
                <th>Type</th>
                <th>Séance</th>
                <th>Soumission</th>
              </tr>
            </thead>
            <tbody>
              {exercices.map((exercice) => (
                <tr key={exercice.id}>
                  <td>{exercice.cours.titre}</td>
                  <td>{exercice.contenu}</td>
                  <td>{exercice.type}</td>
                  <td>{exercice.seance.description}</td>
                  <td>
                    {exercice.soumission.soumis ? (
                      "Soumis"
                    ) : (
                      <button className="btn-soumettre">Soumettre</button>
                    )}
                  </td>

                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ExercicesEleve;
