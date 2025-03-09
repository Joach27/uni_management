import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const register = async (prenom, nom, email, password) => {
  try {
    const response = await axios.post(`${API_URL}/register/eleve`, {prenom, nom, email, password});
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

