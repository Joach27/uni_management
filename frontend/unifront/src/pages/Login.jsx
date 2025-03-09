import { useState } from "react";
import { login } from "../api";
import './login.css';
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [email, setEmail] = useState("");  
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const navigate = useNavigate();
    // const [token, setToken] = useState("");
    

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await login(email, password);
            // setToken(response.access_token);
            setMessage("Connexion réussie");
            localStorage.setItem("token", response.access_token);

            setTimeout(() => {
                navigate("/dashboard");
            }, 2000);
        }
        catch (error) {
            setMessage(error.response.data || "Erreur lors de la connexion");
        }
    }

    return (
        <div className="login">
            <h2>Connexion</h2>
            <form onSubmit={handleSubmit} className="login-form">
                <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <input type="password" placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} />
                <button type="submit">Se connecter</button>
            </form>
            {message && <p>{message}</p>}

            <span className="register-link">Pas de compte? <a href="/register">Inscrivez-vous</a></span>
        </div>
    )
}

export default Login;