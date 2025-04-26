import Navbar from "../components/Navbar";
import { useAuth } from '../AuthContext';
import { useState } from "react";

import Register from "./Register";
import CoursSemestrielPage from "./CoursSemestrielPage";
// import CoursPage from "./CoursPage";
import CreerCours from "./CreerCours";
import CreerCoursSemestriel from "./CreerCoursSemestriel";
import CreerSeance from "./CreerSeance";
import CreerExercice from "./CreerExercice";
import EleveCoursPage from "./EleveCoursPage";
import SeancesEleve from "./SeancesEleve";
import SeancesEnseignant from "./SeancesEnseignant";
import ExercicesEleve from "./ExercicesEleve";
import Examen from "../components/Examen";
import VoirExamen from "../components/VoirExamen";
import VoirExamenEleve from "../components/VoirExamenEleve";
import NoteExamen from "../components/NoteExamen";
import ExamenEtudiant from "../components/ExamenEtudiant";
import ListeEleves from "../components/ListeEleves";
import ListeEnseignants from "../components/ListeEnseignants";
import EtudiantImage from '../assets/étudiants-av.png';
import QuestionEnseignant from "../components/QuestionEnseignant";



const Dashboard = () => {
    const role = useAuth().role;
    const [selectedAction, setSelectedAction] = useState(""); 

    const handleNavClick = (action) => {
        setSelectedAction(action);  
    };

    const renderSelected = () => {  
        switch (selectedAction) {
            case "creerCours":
                return <CreerCours />;
            case "creerCoursSemestriel":
                return <CreerCoursSemestriel />;    
            case "noteExercice":
                return <p>Vous avez choisi de voir les notes d'un exercice.</p>;
            case "noteExamenEnseignant":
                return <NoteExamen />;
            case "creerSeance":
                return <CreerSeance />;
            // case "questions":
            //     return <QuestionEnseignant />;
            case "modifierNoteExamen":
                return <p>Vous avez choisi de modifier la note d'un examen.</p>;
            // case "voirCours":
            //     return <CoursPage />;
            case "voirMesCours":
                return <EleveCoursPage />;
            case "voirSeance":
                return <SeancesEleve />;
            case "voirSeanceEnseignant":
                return <SeancesEnseignant />;
            case "voirNote":
                return <ExamenEtudiant />;
            case "voirExercice":
                return <ExercicesEleve />;
            case "ajouterUtilisateur":
                return <Register />;
            case "voirUtilisateur":
                return <p>Vous avez choisi de voir les utilisateurs.</p>;
            case "creerExercice":
                return <CreerExercice />;   
            case "examen":
                return <Examen />;   
            case "coursSemestriel":
                return <CoursSemestrielPage />;
            case "voirExamens":
                return <VoirExamenEleve />;

            case "voirEleves":
                return <ListeEleves />;

            case "voirEnseignants":
                return <ListeEnseignants />;

            default:
                return (
                    <>
                        <h2>Bienvenue sur votre tableau de bord {role}.</h2>
                        <p>Là, vous pourrez effectuer des actions sur votre compte.</p>
                        <img  src={EtudiantImage} />
                    </>
                )
        }
    };

    return (
        <div className="dashboard">
            <Navbar role = {role} onNavClick={handleNavClick}/>
            {renderSelected()}
        </div>
    );
};

export default Dashboard;
