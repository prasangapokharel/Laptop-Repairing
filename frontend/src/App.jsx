import React from "react";
import LoginForm from "./components/LoginForm";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import CustomerDashboard from "./components/CustomerDashboard";
import LoginSignup from "./components/LoginForm";
import LandingPage from "./pages/LandingPage";
import ReceptionDashboard from "./components/ReceptionDashboard";

export default function App() {
  const pageRoute = createBrowserRouter([
    {
      path:"/customerdashboard",
      element:<CustomerDashboard/>
    }
    ,
    {
      path:"/receptiondashboard",
      element:<ReceptionDashboard/>

    },
    {
      path:"/createaccount",
      element:<LoginSignup/>
    },{
      path:"/",
      element:<LandingPage/>
    }
  ])
  return (
    <div className="text-4xl">
     <RouterProvider router={pageRoute}/>
    </div>
  );
}
