import { NavLink, Outlet } from "react-router-dom";
import "./Layout.css";

export function Layout() {
  return (
    <div className="layout">
      <header className="layout-header">
        <div className="layout-header-inner">
          <NavLink to="/" className="layout-logo">
            Endo Advice
          </NavLink>
          <nav className="layout-nav">
            <NavLink
              to="/supplements"
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              Supplements
            </NavLink>
            <NavLink
              to="/symptoms"
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              By Symptom
            </NavLink>
          </nav>
        </div>
      </header>
      <main className="layout-main">
        <Outlet />
      </main>
    </div>
  );
}
