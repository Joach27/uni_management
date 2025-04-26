import { useState } from 'react';
import './questions.css';
import TeacherQuestions from './TeacherQuestions'; // Assurez-vous que ces imports sont corrects
import StudentQuestionSearch from './StudentQuestionSearch';

const Questions = () => {
  const [activeTab, setActiveTab] = useState('teacher');

  return (
    <div className="conteneur-principal">
      <div className="onglets-conteneur">
        <div className="onglets-ligne">
          <button
            className={`bouton-onglet ${activeTab === 'teacher' ? 'onglet-actif' : 'onglet-inactif'}`}
            onClick={() => setActiveTab('teacher')}
          >
            Mes questions
          </button>
          <button
            className={`bouton-onglet ${activeTab === 'student' ? 'onglet-actif' : 'onglet-inactif'}`}
            onClick={() => setActiveTab('student')}
          >
            Rechercher par élève
          </button>
        </div>
      </div>

      <div className="contenu-onglet">
        {activeTab === 'teacher' ? <TeacherQuestions /> : <StudentQuestionSearch />}
      </div>
    </div>
  );
};

export default Questions;
