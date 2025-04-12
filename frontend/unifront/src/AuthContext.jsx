// src/AuthContext.js
import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { jwtDecode } from "jwt-decode";

const API_URL = 'http://localhost:5000';

const AuthContext = createContext();


export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [role, setRole] = useState(null);
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('token');
        const userRole = localStorage.getItem('role');
        if (token && userRole) {
            setIsLoggedIn(true);
            setRole(userRole);
            const decoded = jwtDecode(token);
            setUserData(decoded);
        }
    }, []);

    const login = async (email, password) => {
        try {
            const response = await axios.post(`${API_URL}/login`, { email, password });
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('role', response.data.role);
            setIsLoggedIn(true);
            setRole(response.data.role);

            const decoded = jwtDecode(response.data.access_token);
            setUserData(decoded);
            return response.data;
        } catch (error) {
            // console.error('Erreur lors de la connexion:', error);
            return error.response.data;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        setIsLoggedIn(false);
        setRole(null);
    };

    const register = async (prenom, nom, email, password, role, telephone, fonction, annee) => {
        try {
            await axios.post(`${API_URL}/inscription`, {userData: {prenom, nom, email, password, role, telephone, fonction, annee}});
            alert('Utilisateur inscrit avec succès!');
        } catch (error) {
            console.error('Erreur lors de l\'inscription:', error);
        }
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, role, login, logout, register, userData }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);