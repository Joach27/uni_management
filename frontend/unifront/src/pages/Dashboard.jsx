import { useNavigate } from "react-router-dom";

const Dashboard = () => {
    const navigate = useNavigate();


    const handleLogout = () => {
        const confirmLogout = window.confirm("Êtes-vous sûr de vouloir vous déconnecter ?");
        if (confirmLogout) {
            localStorage.removeItem("token");
            navigate("/login");  // Redirection après déconnexion
        }
    };

    return (
        <div className="dashboard">
            <h2>Tableau de bord</h2>
            <p>Dashboard content</p>
            <button onClick={handleLogout} className="logout-btn">
                Se déconnecter
            </button>
        </div>
    );
};

export default Dashboard;
