import React from 'react';

interface VaporwaveLayoutProps {
  children: React.ReactNode;
}

const VaporwaveLayout: React.FC<VaporwaveLayoutProps> = ({ children }) => {
  return (
    <div className="vaporwave-layout">
      {children}
    </div>
  );
};

export default VaporwaveLayout;
