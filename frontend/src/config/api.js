const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'  // Production: relative URL
  : 'http://localhost:5000/api';  // Development: absolute URL

export default API_BASE_URL; 