import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../usecontext/Authcontext";

export function PrivateRoute({ children }) {

    let { isAuthenticated } = useContext(AuthContext);

    if (!isAuthenticated) {

        return <Navigate to="/login" replace />;

    }

    return children;
}