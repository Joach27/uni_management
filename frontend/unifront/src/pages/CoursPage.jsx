import React, { useEffect, useState } from "react";
import axios from "axios";
import CardCours from "../components/CardCours";
import '../components/cardcours.css'

const CoursPage = () => {
    const [cours, setCours] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchCours = async () => {
            const token = localStorage.getItem("token");
            try {
                const response = await axios.get("http://localhost:5000/api/cours", {
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
            <h2>Mes cours</h2>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <div className="cours-list">
                    {cours.map((cours) => (
                        <CardCours key={cours._id} cours={cours} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default CoursPage;