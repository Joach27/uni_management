import React, { useState } from 'react';
import CreerExamen from './CreerExamen';
import VoirExamen from './VoirExamen';
import './creerexamen.css'

const Examen = () => {
    const [vueActive, setVueActive] = useState(null); // null, 'creer', ou 'voir'

    const renderVue = () => {
        if (vueActive === 'creer') {
            return <CreerExamen />;
        } else if (vueActive === 'voir') {
            return <VoirExamen />;
        } else {
            return null;
        }
    };

    return (
        <div className="examen-container">
            <h2>Examens</h2>
            <p>Choisissez de créer un nouvel examen ou de voir les examens existants.</p>
            <div className='examen-buttons'>
                <button className='creer' onClick={() => setVueActive('creer')}>Créer un examen</button>            
                <button className='voir' onClick={() => setVueActive('voir')}>Voir les examens</button>
            </div>

            <div style={{ marginTop: '20px' }}>
                {renderVue()}
            </div>
        </div>
    );
};

export default Examen;
