import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Companies from './pages/Companies';
import Applications from './pages/Applications';
import RiskAnalysis from './pages/RiskAnalysis';
import Simulations from './pages/Simulations';

function App() {
  return (
    <Layout>
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
    </Layout>
  );
}

export default App;
