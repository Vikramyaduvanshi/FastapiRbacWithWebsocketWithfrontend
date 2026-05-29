
import { createContext, useContext, useState } from "react";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    const [loading, setLoading] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const login = async (email, password) => {

        try {

            setLoading(true);

            const formdata = new FormData();

            formdata.append("email", email);
            formdata.append("password", password);

            const response = await axios.post("/api/auth/login", formdata, { withCredentials: true});

            if (response.data.success) {

                setIsAuthenticated(true);
            }

            return response.data;

        } catch (error) {

            console.log(error);

            return error.response.data;

        } finally {

            setLoading(false);
        }
    };

    const logout = () => {

        setIsAuthenticated(false);
    };

    return (

        <AuthContext.Provider value={{login, logout, loading, isAuthenticated}}>
            {children}
        </AuthContext.Provider>
    );
};

