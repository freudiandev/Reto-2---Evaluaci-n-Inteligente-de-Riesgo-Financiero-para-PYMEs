import { Route, Routes } from 'react-router-dom';
import CyberpunkNav from './components/CyberpunkNav';
import VaporwaveLayout from './components/VaporwaveLayout';
import Applications from './pages/Applications';
import Companies from './pages/Companies';
import Dashboard from './pages/Dashboard';
import RiskAnalysis from './pages/RiskAnalysis';
import Simulations from './pages/Simulations';
import './styles/vaporwave.css';

function App() {
  return (
    <div className="cyberpunk-app">
      <VaporwaveLayout>
        {/* Navegación cyberpunk */}
        <CyberpunkNav />
        
        <header className="hero-section">
          <div className="cyberpunk-grid-bg"></div>
          <h1 className="neon-title">
            The Orellana's Boyz: Reto Analiza crédito para las Pymes,
            <span className="subtitle-glow"> más allá del historial crediticio</span>
          </h1>
          <div className="neon-divider"></div>
        </header>

        <main className="content-sections">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/applications" element={<Applications />} />
            <Route path="/risk-analysis" element={<RiskAnalysis />} />
            <Route path="/risk-analysis/:applicationId" element={<RiskAnalysis />} />
            <Route path="/simulations" element={<Simulations />} />
            <Route path="/simulations/:applicationId" element={<Simulations />} />
          </Routes>
        </main>

        <footer className="cyberpunk-footer">
          <div className="footer-waves"></div>
          <section className="footer-content">
            <h3 className="footer-title neon-text">Reto para el Primer hackIAtón en Ecuador</h3>
            <p className="footer-subtitle glow-text">gracias a Viamática</p>
            <div className="dev-credits">
              <p className="credits-text">Esta página fue desarrollada por:</p>
              <div className="developer-names">
                <span className="dev-name neon-name">Mateo Almeida</span>
                <span className="dev-separator">•</span>
                <span className="dev-name neon-name">Kevin Martinez</span>
                <span className="dev-separator">•</span>
                <span className="dev-name neon-name">Alex Almeida</span>
              </div>
            </div>
          </section>
          <div className="footer-grid"></div>
        </footer>
        
        {/* Efectos ambientales */}
        <div className="ambient-lights">
          <div className="light pink"></div>
          <div className="light blue"></div>
          <div className="light purple"></div>
        </div>
      </VaporwaveLayout>
    </div>
  );
}

export default App;
