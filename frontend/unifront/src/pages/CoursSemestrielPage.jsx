import React, { useEffect, useState } from "react";
import axios from "axios";
import CardCours from "../components/CardCours";

const CoursSemestrielPage = () => {
    const [cours, setCours] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchCours = async () => {
            const token = localStorage.getItem("token");
            try {
                const response = await axios.get("http://localhost:5000/api/cours_semestriel", {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    }
                });
                setCours(response.data);
                setLoading(false);
            } catch (error) {
                setError(error.message);
                setLoading(false);
            }
        };
        fetchCours();
    }, []);
    
    return (
        <div className="cours">
            <h2>Mes cours du semestre</h2>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <div className="cours-list">
                    {cours.map((cs) => (
                        <CardCours key={cs.id} cours={cs} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default CoursSemestrielPage;