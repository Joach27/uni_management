import "./nav.css";
import { Link } from "react-router-dom";

const Navbar = ({ role, onNavClick }) => {
  return (
    <div className="navbar">
      <div className="left-side">
        <Link to="/" style={{ textDecoration: "none" }}>
            <h2>UniViz</h2>
        </Link>
      </div>
      <div className="right-side">
        {role === "Enseignant" && (
          <ul className="menu-list">
            <li onClick={() => onNavClick("creerSeance")}>
              Créer une séance
            </li>
            <li onClick={() => onNavClick("voirSeanceEnseignant")}>
              Mes séances
            </li>
            <li onClick={() => onNavClick("creerExercice")}>
              Poser un exercice
            </li>
            <li onClick={() => onNavClick("examen")}>
              Examens
            </li>
            <li>
              Notes
            </li>
          </ul>
        )}

        {role === "Eleve" && (
          <ul className="menu-list">
            {/* <li onClick={() => onNavClick("voirCours")}>
              Cours
            </li> */}
            <li onClick={() => onNavClick("coursSemestriel")}>
              Cours du semestre
            </li>
            <li onClick={() => onNavClick("voirMesCours")}>
              Mes Cours
            </li>
            <li onClick={() => onNavClick("voirSeance")}>
              Séances
            </li>
            <li onClick={() => onNavClick("voirExercice")}>
              Exercices
            </li>
            <li onClick={() => onNavClick("voirExamens")}>
              Examens
            </li>
            <li>
              Notes
            </li>
          </ul>
        )}

        {role === "Secretaire" && (
          <ul className="menu-list">
            <li onClick={() => onNavClick("ajouterUtilisateur")}>Ajouter un utilisateur
            </li>
            <li onClick={() => onNavClick("creerCours")}>Créer un cours
            </li>
            <li onClick={() => onNavClick("creerCoursSemestriel")}>
              Créer un cours semestriel
            </li>
          </ul>
        )}

        {/* <button className="logout" onClick={() => {
      localStorage.removeItem("role");
      window.location.href = "/login";
  }}>Logout</button> */}
      </div>

      <button
        className="logout"
        onClick={() => {
          localStorage.removeItem("role");
          localStorage.removeItem("token");
          window.location.href = "/login";
        }}
      >
        Deconnexion
      </button>
    </div>
  );
};

export default Navbar;
