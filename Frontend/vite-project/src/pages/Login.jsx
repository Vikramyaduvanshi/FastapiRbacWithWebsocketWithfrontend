import { useContext, useState } from "react";
import { AuthContext } from "../usecontext/Authcontext";
import { useNavigate } from "react-router-dom";


export function Login() {
let navigate=useNavigate()
    const { login, loading } = useContext(AuthContext);

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handlesubmit = async (e) => {

        e.preventDefault();

        const data = await login(email, password);

        console.log(data,"login in login page");

        if (data.success) {
            navigate("/admin_route")


            alert("Login Successfully");

        } else {

            alert(data.detail || "Login Failed");
        }
    };

    return (

        <div style={{ width: "100%", height: "100vh", display: "flex", justifyContent: "center", alignItems: "center" }}>

            <form onSubmit={handlesubmit} style={{ width: "350px", display: "flex", flexDirection: "column", gap: "15px", padding: "30px", border: "1px solid gray", borderRadius: "10px" }}>

                <h2>Login</h2>

                <input type="email" placeholder="Enter Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ padding: "10px" }}/>

                <input type="password" placeholder="Enter Password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ padding: "10px" }}/>

                <button type="submit" style={{ padding: "10px", cursor: "pointer" }}>

                    {loading ? "Loading..." : "Login"}

                </button>

            </form>

        </div>
    );
}