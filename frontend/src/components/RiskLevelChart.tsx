interface RiskLevelChartProps {
  data: Record<string, number>;
}

export default function RiskLevelChart({ data }: RiskLevelChartProps) {
  const total = Object.values(data).reduce((sum, value) => sum + value, 0);
  
  const levels = [
    { key: 'low', label: 'Bajo', color: 'bg-green-500' },
    { key: 'medium', label: 'Medio', color: 'bg-yellow-500' },
    { key: 'high', label: 'Alto', color: 'bg-red-500' },
  ];

  return (
    <div className="space-y-3">
      {levels.map((level) => {
        const value = data[level.key] || 0;
        const percentage = total > 0 ? (value / total) * 100 : 0;
        
        return (
          <div key={level.key} className="flex items-center justify-between">
            <div className="flex items-center">
              <div className={`w-3 h-3 rounded-full ${level.color} mr-2`}></div>
              <span className="text-sm text-gray-600">{level.label}</span>
            </div>
            <div className="flex items-center">
              <div className="w-16 bg-gray-200 rounded-full h-2 mr-3">
                <div
                  className={`h-2 rounded-full ${level.color}`}
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
              <span className="text-sm font-medium text-gray-900 w-8">{value}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
