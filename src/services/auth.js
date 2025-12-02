import api from '../utils/api';

export const loginUser = async (credentials) => {
    try {
        const response = await api.post('/auth/login', credentials);
        const { token } = response.data;
        if (token) {
            localStorage.setItem('authToken', token);
        }
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const registerUser = async (userData) => {
    try {
        const response = await api.post('/auth/register', userData);
        return response.data;
    } catch (error) {
        throw error;
    }
};
