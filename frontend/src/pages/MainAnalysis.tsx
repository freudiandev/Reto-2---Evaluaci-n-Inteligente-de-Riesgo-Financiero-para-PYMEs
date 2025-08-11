import axios from 'axios';
import React, { useEffect, useRef, useState } from 'react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  analysisData?: any;
}

interface CompanyAnalysis {
  company_info: {
    ruc: string;
    name: string;
    sector: string;
  };
  integrated_risk_assessment: {
    final_risk_score: number;
    risk_level: string;
    recommendation: string;
    component_scores: any;
    confidence_level: number;
  };
  hackathon_score: {
    score: number;
    classification: string;
    color: string;
  };
  recommendations: string[];
}

const API_BASE_URL = 'http://localhost:8000';

const MainAnalysis: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '¡Hola! 👋 Soy tu asistente de análisis de riesgo crediticio para PyMEs. Puedes preguntarme sobre cualquier empresa escribiendo su RUC o nombre. También puedo ayudarte con:\n\n🔍 Búsqueda en Super de Compañías\n📱 Análisis de huella digital\n📊 Simulaciones de escenarios\n⚡ Scoring alternativo con IA\n\n¿Qué empresa te gustaría analizar?',
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  
  const [inputText, setInputText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState<CompanyAnalysis | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const addMessage = (text: string, sender: 'user' | 'ai', analysisData?: any) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender,
      timestamp: new Date(),
      analysisData
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const performComprehensiveAnalysis = async (companyName: string, ruc?: string) => {
    try {
      setIsAnalyzing(true);
      
      // Preparar datos para el análisis
      const analysisRequest = {
        company_ruc: ruc || `${Date.now()}001`, // RUC simulado si no se proporciona
        company_name: companyName,
        sector: "Comercial", // Sector por defecto
        social_media_urls: [],
        include_supercias_data: true,
        include_digital_footprint: true,
        include_scenario_analysis: true
      };

      addMessage('🔍 Iniciando análisis integral...', 'ai');
      
      const response = await axios.post(
        `${API_BASE_URL}/api/v2/hackathon/comprehensive-analysis`,
        analysisRequest,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      const analysisResult = response.data.analysis_result;
      setCurrentAnalysis(analysisResult);
      
      // Crear mensaje de respuesta con los resultados
      const resultMessage = formatAnalysisResults(analysisResult);
      addMessage(resultMessage, 'ai', analysisResult);
      
    } catch (error) {
      console.error('Error en análisis:', error);
      addMessage('❌ Error al realizar el análisis. Intentando con datos de demostración...', 'ai');
      
      // Fallback con datos demo
      try {
        const demoResponse = await axios.get(`${API_BASE_URL}/api/v2/hackathon/demo-data`);
        const demoMessage = `📊 Datos de demostración disponibles:\n\n${demoResponse.data.demo_companies.map((company: any, index: number) => 
          `${index + 1}. ${company.name} (${company.ruc}) - ${company.sector}`
        ).join('\n')}`;
        addMessage(demoMessage, 'ai');
      } catch (demoError) {
        addMessage('❌ No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose en http://localhost:8000', 'ai');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const formatAnalysisResults = (analysis: CompanyAnalysis): string => {
    const { company_info, integrated_risk_assessment, hackathon_score, recommendations } = analysis;
    
    return `🎯 **ANÁLISIS INTEGRAL COMPLETADO**
    
**🏢 Empresa:** ${company_info.name}
**📋 RUC:** ${company_info.ruc}
**🏭 Sector:** ${company_info.sector}

**📊 SCORING DE RIESGO:**
• **Score Final:** ${integrated_risk_assessment.final_risk_score}/100
• **Nivel de Riesgo:** ${integrated_risk_assessment.risk_level.toUpperCase()}
• **Confianza:** ${(integrated_risk_assessment.confidence_level * 100).toFixed(1)}%

**🏆 SCORE HACKATHON:**
• **Puntuación:** ${hackathon_score.score}/100
• **Clasificación:** ${hackathon_score.classification}

**💡 RECOMENDACIÓN:**
${integrated_risk_assessment.recommendation}

**📋 RECOMENDACIONES ESPECÍFICAS:**
${recommendations.map(rec => `• ${rec}`).join('\n')}

¿Te gustaría ver simulaciones de escenarios o análisis más detallado?`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = inputText.trim();
    addMessage(userMessage, 'user');
    setInputText('');

    // Detectar si es un RUC (11 dígitos) o nombre de empresa
    const rucPattern = /^\d{10,13}$/;
    const isRUC = rucPattern.test(userMessage.replace(/\s+/g, ''));

    if (isRUC) {
      // Buscar por RUC en Super de Compañías
      try {
        addMessage('🔍 Buscando empresa en Super de Compañías...', 'ai');
        const response = await axios.get(`${API_BASE_URL}/api/v2/hackathon/company-search/${userMessage}`);
        
        if (response.data.found) {
          const companyData = response.data.company_data;
          await performComprehensiveAnalysis(companyData.company_name || 'Empresa Encontrada', userMessage);
        } else {
          addMessage(`❌ No se encontró empresa con RUC: ${userMessage}. Intentando análisis con datos simulados...`, 'ai');
          await performComprehensiveAnalysis(`Empresa RUC ${userMessage}`, userMessage);
        }
      } catch (error) {
        addMessage('❌ Error al buscar en Super de Compañías. Realizando análisis con datos simulados...', 'ai');
        await performComprehensiveAnalysis(`Empresa RUC ${userMessage}`, userMessage);
      }
    } else {
      // Buscar por nombre de empresa
      await performComprehensiveAnalysis(userMessage);
    }
  };

  const handleQuickAction = async (action: string) => {
    switch (action) {
      case 'demo':
        addMessage('📊 Mostrar datos de demostración', 'user');
        try {
          const response = await axios.get(`${API_BASE_URL}/api/v2/hackathon/demo-data`);
          const demoMessage = `📊 **DATOS DE DEMOSTRACIÓN:**\n\n${response.data.demo_companies.map((company: any, index: number) => 
            `${index + 1}. **${company.name}**\n   RUC: ${company.ruc}\n   Sector: ${company.sector}\n   Descripción: ${company.description}\n`
          ).join('\n')}`;
          addMessage(demoMessage, 'ai');
        } catch (error) {
          addMessage('❌ Error al obtener datos de demostración', 'ai');
        }
        break;
      
      case 'techstart':
        addMessage('TechStart Ecuador S.A.', 'user');
        await performComprehensiveAnalysis('TechStart Ecuador S.A.', '1791234567001');
        break;
      
      case 'comercial':
        addMessage('Comercial Los Andes', 'user');
        await performComprehensiveAnalysis('Comercial Los Andes', '0987654321001');
        break;
        
      case 'manufactura':
        addMessage('Manufactura Moderna S.A.', 'user');
        await performComprehensiveAnalysis('Manufactura Moderna S.A.', '1122334455001');
        break;
    }
  };

  return (
    <div className="main-analysis-container">
      <div className="analysis-grid">
        
        {/* Panel izquierdo - Chat */}
        <div className="chat-panel cyberpunk-panel">
          <div className="panel-header">
            <h2 className="neon-text">💬 Chat de Análisis Crediticio</h2>
            <div className="status-indicator online"></div>
          </div>
          
          <div className="messages-container">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.sender}`}>
                <div className="message-content">
                  <pre className="message-text">{message.text}</pre>
                  <span className="message-time">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
            {isAnalyzing && (
              <div className="message ai">
                <div className="message-content">
                  <div className="analyzing-animation">
                    <span className="neon-text">🤖 Analizando</span>
                    <div className="dots">
                      <span>.</span><span>.</span><span>.</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <form onSubmit={handleSubmit} className="chat-input-form">
            <div className="input-group">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Escribe el RUC o nombre de la empresa..."
                className="cyberpunk-input"
                disabled={isAnalyzing}
              />
              <button 
                type="submit" 
                className="submit-btn neon-btn"
                disabled={isAnalyzing || !inputText.trim()}
              >
                {isAnalyzing ? '⏳' : '🚀'}
              </button>
            </div>
          </form>
          
          {/* Acciones rápidas */}
          <div className="quick-actions">
            <button 
              onClick={() => handleQuickAction('demo')} 
              className="quick-btn"
              disabled={isAnalyzing}
            >
              📊 Datos Demo
            </button>
            <button 
              onClick={() => handleQuickAction('techstart')} 
              className="quick-btn"
              disabled={isAnalyzing}
            >
              🏢 TechStart
            </button>
            <button 
              onClick={() => handleQuickAction('comercial')} 
              className="quick-btn"
              disabled={isAnalyzing}
            >
              🛒 Comercial
            </button>
            <button 
              onClick={() => handleQuickAction('manufactura')} 
              className="quick-btn"
              disabled={isAnalyzing}
            >
              🏭 Manufactura
            </button>
          </div>
        </div>

        {/* Panel derecho - Dashboard de resultados */}
        <div className="results-panel cyberpunk-panel">
          <div className="panel-header">
            <h2 className="neon-text">📊 Dashboard Financiero Personalizado</h2>
          </div>
          
          {currentAnalysis ? (
            <div className="analysis-dashboard">
              {/* Header de la empresa */}
              <div className="company-header">
                <h3 className="company-name neon-title">
                  {currentAnalysis.company_info.name}
                </h3>
                <div className="company-details">
                  <span className="ruc">RUC: {currentAnalysis.company_info.ruc}</span>
                  <span className="sector">Sector: {currentAnalysis.company_info.sector}</span>
                </div>
              </div>

              {/* Score principal */}
              <div className="main-score">
                <div className="score-circle">
                  <div className={`score-value ${currentAnalysis.hackathon_score.color}`}>
                    {currentAnalysis.hackathon_score.score}
                  </div>
                  <div className="score-label">Score de Riesgo</div>
                </div>
                <div className="score-classification">
                  <span className={`classification ${currentAnalysis.hackathon_score.color}`}>
                    {currentAnalysis.hackathon_score.classification}
                  </span>
                  <div className="confidence">
                    Confianza: {(currentAnalysis.integrated_risk_assessment.confidence_level * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* Indicadores por componentes */}
              <div className="component-scores">
                <h4 className="section-title">📈 Análisis por Componentes</h4>
                <div className="scores-grid">
                  {Object.entries(currentAnalysis.integrated_risk_assessment.component_scores).map(([key, value]) => (
                    <div key={key} className="score-card">
                      <div className="score-name">{key.replace('_score', '').toUpperCase()}</div>
                      <div className="score-bar">
                        <div 
                          className="score-fill" 
                          style={{ width: `${value as number}%` }}
                        ></div>
                      </div>
                      <div className="score-number">{(value as number).toFixed(1)}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recomendaciones */}
              <div className="recommendations">
                <h4 className="section-title">💡 Recomendaciones</h4>
                <div className="recommendation-main neon-text">
                  {currentAnalysis.integrated_risk_assessment.recommendation}
                </div>
                <ul className="recommendation-list">
                  {currentAnalysis.recommendations.map((rec, index) => (
                    <li key={index} className="recommendation-item">{rec}</li>
                  ))}
                </ul>
              </div>

              {/* Acciones adicionales */}
              <div className="additional-actions">
                <button className="action-btn">📈 Ver Simulaciones</button>
                <button className="action-btn">🌐 Análisis Digital</button>
                <button className="action-btn">📊 Comparar Sector</button>
              </div>
            </div>
          ) : (
            <div className="no-analysis">
              <div className="placeholder-content">
                <div className="placeholder-icon">🎯</div>
                <h3>Análisis de Riesgo Crediticio</h3>
                <p>Inicia una consulta en el chat para ver el dashboard personalizado con:</p>
                <ul>
                  <li>🔍 Búsqueda en Super de Compañías</li>
                  <li>📱 Análisis de huella digital</li>
                  <li>🧠 Scoring con IA alternativa</li>
                  <li>📊 Comparación sectorial</li>
                  <li>🎯 Simulaciones de escenarios</li>
                  <li>💡 Recomendaciones personalizadas</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MainAnalysis;
