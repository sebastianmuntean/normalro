import React from 'react';
import { Box } from '@mui/material';

const Logo = ({ size = 40, color = '#1976d2' }) => {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background circle */}
        <circle cx="20" cy="20" r="18" fill={color} fillOpacity="0.1" stroke={color} strokeWidth="2"/>
        
        {/* Document/Page icon */}
        <rect x="10" y="8" width="16" height="20" rx="2" fill={color} fillOpacity="0.2"/>
        <rect x="8" y="10" width="16" height="20" rx="2" fill={color} fillOpacity="0.4"/>
        <rect x="6" y="12" width="16" height="20" rx="2" fill={color}/>
        
        {/* Text lines */}
        <line x1="9" y1="16" x2="17" y2="16" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
        <line x1="9" y1="19" x2="15" y2="19" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
        <line x1="9" y1="22" x2="16" y2="22" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
        <line x1="9" y1="25" x2="14" y2="25" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
      
      <Box sx={{ 
        fontFamily: 'Georgia, serif', 
        fontSize: '1.25rem', 
        fontWeight: 'bold',
        color: color,
        letterSpacing: '0.5px'
      }}>
        CMS Times
      </Box>
    </Box>
  );
};

export default Logo; 