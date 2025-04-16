import "./nav.css";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Navbar = ({ role, onNavClick }) => {
  const navigate = useNavigate();

  return (
    <div className="navbar">
      <div className="left-side">
        <Link to="/" style={{ textDecoration: "none" }}>
            <h2>UniVersity</h2>
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
            <li onClick={() => onNavClick("noteExamenEnseignant")}>
              Notes examens
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
            <li onClick={() => onNavClick("voirNote")}>
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
            <li onClick={() => onNavClick("voirEleves")}>
              Elèves
            </li>
            <li onClick={() => onNavClick("voirEnseignants")}>
              Enseignants
            </li>
          </ul>
        )}

      </div>

      <button
        className="logout"
        onClick={() => {
          localStorage.removeItem("role");
          localStorage.removeItem("token");
          navigate("/login");
        }}
      >
        Deconnexion
      </button>
    </div>
  );
};

export default Navbar;
