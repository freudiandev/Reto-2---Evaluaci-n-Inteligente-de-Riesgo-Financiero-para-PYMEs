import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface VaporwaveLayoutProps {
  children: React.ReactNode;
}

const VaporwaveLayout: React.FC<VaporwaveLayoutProps> = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/companies', label: 'Empresas', icon: '🏢' },
    { path: '/applications', label: 'Solicitudes', icon: '📄' },
    { path: '/risk-analysis', label: 'Análisis', icon: '🎯' },
    { path: '/simulations', label: 'Simulaciones', icon: '🔮' },
  ];

  return (
    <div className="vaporwave-layout">
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
      
      <div className="layout-content">
        {children}
      </div>
      
      <div className="ambient-lights">
        <div className="light pink"></div>
        <div className="light blue"></div>
        <div className="light purple"></div>
      </div>
    </div>
  );
};

export default VaporwaveLayout;
