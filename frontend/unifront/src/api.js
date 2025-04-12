import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const register = async (prenom, nom, email, password, role, telephone, fonction, annee) => {
  try {
    const response = await axios.post(`${API_URL}/inscription`, {prenom, nom, email, password, role, telephone, fonction, annee});
    return response.data;
  } catch (error) {
    return error.response.data;
  }
}

export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, {email, password});
    return response.data;
  } catch (error) {
    return error.response.data;
  }
}

