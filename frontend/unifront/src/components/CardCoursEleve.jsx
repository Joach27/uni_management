const CardCoursEleve = ({ cours }) => {
    return (
        <div className="card-cours">
            <div className="card-cours-content">
                <h3>{cours.cours.titre}</h3>
                <p>{cours.cours.description}</p>
            </div>
            <div className="card-cours-footer">
                <span>{cours.cours.type}</span>
                <span>{cours.cours.heures} Hrs</span>
            </div>
        </div>
    );
}

export default CardCoursEleve; 