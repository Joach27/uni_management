import React from "react";
import { Link } from "react-router-dom";
import "./home.css"; // Importation du fichier CSS

const Home = () => {
    return (
        <div className="home-container">
            <div className="content">
                <h1>Bienvenue sur notre plateforme</h1>
                <p>Apprenez, explorez et développez vos compétences en ligne.</p>
                <div className="buttons">
                    <Link to="/login">
                        <button className="btn primary">Connexion</button>
                    </Link>
                    <Link to="/dashboard">  
                        <button className="btn secondary">Dashboard</button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Home;
