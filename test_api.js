// Test rápido de la API
const fetch = require('node-fetch');

async function testDashboard() {
    try {
        const response = await fetch('https://backend-riesgo-pymes-the-orellanas-boyz.onrender.com/api/v1/dashboard/summary');
        const data = await response.json();
        
        console.log('✅ Conexión exitosa!');
        console.log('📊 Datos recibidos:', JSON.stringify(data, null, 2));
        
        // Verificar campos requeridos
        const requiredFields = [
            'total_applications',
            'approved_applications', 
            'rejected_applications',
            'pending_applications',
            'average_risk_score',
            'total_credit_amount',
            'risk_level_distribution',
            'sector_distribution'
        ];
        
        const missing = requiredFields.filter(field => !(field in data));
        
        if (missing.length === 0) {
            console.log('✅ Todos los campos requeridos están presentes');
            console.log('🎯 El dashboard debería funcionar correctamente ahora');
        } else {
            console.log('❌ Campos faltantes:', missing);
        }
        
    } catch (error) {
        console.error('❌ Error de conexión:', error.message);
    }
}

testDashboard();
