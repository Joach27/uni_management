import { useState } from "react";
// import { login } from "../api";
import { useAuth } from "../AuthContext";
import './login.css';
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

// const Login = () => {
//     const [email, setEmail] = useState("");  
//     const [password, setPassword] = useState("");
//     const [message, setMessage] = useState("");

//     const navigate = useNavigate();
//     // const [token, setToken] = useState("");
    

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             const response = await login(email, password);
//             // setToken(response.access_token);
//             setMessage("Connexion réussie");
//             localStorage.setItem("token", response.access_token);
//             localStorage.setItem("role", response.role);
//             setTimeout(() => {
//                 navigate("/dashboard");
//             }, 1000);
//         }
//         catch (error) {
//             setMessage(error.response.data || "Erreur lors de la connexion");
//         }
//     }

//     return (
//         <div className="login">
//             <h2>Connexion</h2>
//             <form onSubmit={handleSubmit} className="login-form">
//                 <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
//                 <input type="password" placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} />
//                 <button type="submit">Se connecter</button>
//             </form>
//             {message && <p>{message}</p>}
//         </div>
//     )
// }

// export default Login;

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const { login } = useAuth();
    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
            setMessage("Connexion réussie");
            setTimeout(() => {
                navigate("/dashboard");
            }, 1000);
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
                <button type="submit" className="login-button">Se connecter</button>
            </form>
            {message && <p>{message}</p>}

            
            <Link to="/" className="login_link_home">   
                <span className="retour">Retourner à l'accueil</span>
            </Link>
        </div>
    )
}

export default Login;