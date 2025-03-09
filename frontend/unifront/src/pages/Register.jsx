import { useState } from "react";
import './register.css';
import { register } from "../api";
import { useNavigate } from "react-router-dom";


const Register = () => {
    const [email, setEmail] = useState("");  
    const [password, setPassword] = useState("");
    const [nom, setNom] = useState("");
    const [prenom, setPrenom] = useState("");
    const [message, setMessage] = useState("");

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(prenom, nom, email, password);
            setMessage("Inscription réussie");
            setTimeout(() => {
                navigate("/login");
            }, 2000);
        }
        catch (error) {
            setMessage(error.response.data || "Erreur lors de l'incription");
        }
    }

    return (
        <div className="register">
            <h2>Inscription</h2>
            <form onSubmit={handleSubmit} className="register-form">
                <input type="text" placeholder="Prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)} />

                <input type="text" placeholder="Nom" value={nom} onChange={(e) => setNom(e.target.value)} />
                <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />

                <input type="password" placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} />

                <button type="submit">S'inscrire</button>
            </form>
            {message && <p>{message}</p>}

            <p className="login-link">Vous avez déjà un compte ? <a href="/login">Connectez-vous</a></p>
        </div>
    )

}

export default Register;