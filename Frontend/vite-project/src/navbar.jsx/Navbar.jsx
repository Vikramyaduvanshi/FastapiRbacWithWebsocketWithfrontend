import { useContext } from "react";
import { AuthContext } from "../usecontext/Authcontext";
import { Link } from "react-router-dom";
import "./Navbar.css";

export function Navbar() {

    let { isAuthenticated } = useContext(AuthContext);

    return (
        <div className="navbar">

            <h2 className="logo">Trading App</h2>

            <div className="links">

                {isAuthenticated ? (

                    <Link to="/admin_route">Admin Route</Link>

                ) : (

                    <>
                        <Link to="/home">Home</Link>
                        <Link to="/admin_route">Admin</Link>
                    </>
                )}

            </div>

        </div>
    );
}