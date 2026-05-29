import { Route, Routes } from "react-router-dom"
import { Admin } from "./pages/admin"
import { Navbar } from "./navbar.jsx/Navbar"
import { Home } from "./pages/Home"
import { PrivateRoute } from "./Private_routes/Private_route"
import { Login } from "./pages/Login"


function App() {
  

  return (
 <>
<Navbar/>

 <Routes>
<Route path="/" element={<Home/>}/>
<Route path="/login" element={<Login/>}/>

<Route path="/admin_route"  element={<PrivateRoute><Admin/></PrivateRoute>}/>



 </Routes>
 </>
     
  )
}

export default App
