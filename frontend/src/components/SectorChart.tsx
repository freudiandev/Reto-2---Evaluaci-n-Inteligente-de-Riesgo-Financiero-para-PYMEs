interface SectorChartProps {
  data: Record<string, number>;
}

export default function SectorChart({ data }: SectorChartProps) {
  // Tomar los top 5 sectores
  const sortedSectors = Object.entries(data)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5);

  const total = Object.values(data).reduce((sum, value) => sum + value, 0);

  return (
    <div className="space-y-2">
      {sortedSectors.map(([sector, value]) => {
        const percentage = total > 0 ? (value / total) * 100 : 0;
        const shortSector = sector.length > 20 ? `${sector.substring(0, 20)}...` : sector;
        
        return (
          <div key={sector} className="flex items-center text-sm">
            <div className="w-32 truncate text-gray-600">{shortSector}</div>
            <div className="flex-1 mx-3">
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-primary-500 h-1.5 rounded-full"
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
            </div>
            <div className="w-8 text-right text-gray-900 font-medium">{value}</div>
          </div>
        );
      })}
      {sortedSectors.length === 0 && (
        <div className="text-sm text-gray-500 text-center py-4">
          No hay datos de sectores disponibles
        </div>
      )}
    </div>
  );
}
