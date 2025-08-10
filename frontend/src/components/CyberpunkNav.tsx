import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const CyberpunkNav: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/companies', label: 'Empresas', icon: '🏢' },
    { path: '/applications', label: 'Solicitudes', icon: '📄' },
    { path: '/risk-analysis', label: 'Análisis', icon: '🎯' },
    { path: '/simulations', label: 'Simulaciones', icon: '🔮' },
  ];

  return (
    <nav className="cyberpunk-nav">
      <div className="nav-grid"></div>
      <div className="nav-content">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
            <div className="nav-glow"></div>
          </Link>
        ))}
      </div>
      <div className="nav-pulse"></div>
    </nav>
  );
};

export default CyberpunkNav;
