import React, { useState } from 'react';
import VoirNotesEtudiant from './VoirNotesEtudiant';
import VoirNotesExercicesEtudiant from './VoirNotesExercicesEtudiant';
import './creerexamen.css';

const ExamenEtudiant = () => {
    const [vueActive, setVueActive] = useState(null); // null, 'creer', ou 'voir'

    const renderVue = () => {
        if (vueActive === 'voirExamen') {
            return <VoirNotesEtudiant />;
        } else if (vueActive === 'voirExercice') {
            return <VoirNotesExercicesEtudiant />;
        } else {
            return null;
        }
    };

    return (
        <div className="examen-container">
            <h2>Notes</h2>
            <p>Vous pouvez consulter les notes des examens et des exerices</p>
            <div className='examen-buttons'>
                <button className='creer' onClick={() => setVueActive('voirExamen')}>Notes d'examens</button>            
                <button className='voirExercice' onClick={() => setVueActive('voir')}>Notes d'exercices</button>
            </div>

            <div style={{ marginTop: '20px' }}>
                {renderVue()}
            </div>
        </div>
    );
};

export default ExamenEtudiant;
