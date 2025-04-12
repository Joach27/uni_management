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
    const [role, setRole] = useState("");
    const [telephone, setTelephone] = useState("");
    const [fonction, setFonction] = useState("");
    const [annee, setAnnee] = useState("");

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(prenom, nom, email, password, role, telephone, fonction, annee);
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
                <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />

                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                <select name="role" value={role} onChange={(e) => setRole(e.target.value)} required>
                    <option value="">--- Role ---</option>
                    <option value="Enseignant">Enseignant</option>
                    <option value="Eleve">Eleve</option>
                    <option value="Secretaire">Secretaire</option>
                </select>

                {role === "Enseignant" && (
                    <>
                    <input type="text" placeholder="Nom" value={nom} onChange={(e) => setNom(e.target.value)} />

                    <input type="text" placeholder="Prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)} />

                    <input type="text" placeholder="Telephone" value={telephone} onChange={(e) => setTelephone(e.target.value)} />

                    <input type="text" placeholder="Fonction" value={fonction} onChange={(e) => setFonction(e.target.value)} />
                    </>
                )}

                {role === "Eleve" && (
                    <>
                    <input type="text" placeholder="Nom" value={nom} onChange={(e) => setNom(e.target.value)} />

                    <input type="text" placeholder="Prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)} />

                    <input type="text" placeholder="Annee" value={annee} onChange={(e) => setAnnee(e.target.value)} />
                    </>
                )}

                {role === "Secretaire" && (
                    <>
                    <input type="text" placeholder="Nom" value={nom} onChange={(e) => setNom(e.target.value)} />

                    <input type="text" placeholder="Prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)} />

                    <input type="text" placeholder="Telephone" value={telephone} onChange={(e) => setTelephone(e.target.value)} />
                    </>
                )}

                <button type="submit">S'inscrire</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    )

}

export default Register;