import { useState } from 'react';
import CreerNoteExamen from './CreerNoteExamen';
import VoirNoteExamenEnseignant from './VoirNoteExamenEnseignant';
import './creerexamen.css';


const NoteExamen = () => {
    const [vueActive, setVueActive] = useState(null); // null, 'creer', ou 'voir'

    const renderVue = () => {
        if (vueActive === 'creer') {
            return <CreerNoteExamen />;
        } else if (vueActive === 'voir') {
            return <VoirNoteExamenEnseignant />;
        } else {
            return null;
        }
    };

    return (
        <div className="examen-container">
            <h2>Examens</h2>
            <p>Choisissez de créer une note d'examen ou de voir les notes déjà attribuées.</p>
            <div className='examen-buttons'>
                <button className='creer' onClick={() => setVueActive('creer')}>Donner une note</button>            
                <button className='voir' onClick={() => setVueActive('voir')}>Voir les notes</button>
            </div>

            <div style={{ marginTop: '20px' }}>
                {renderVue()}
            </div>
        </div>
    );
}
export default NoteExamen;