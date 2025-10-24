// You can set REACT_APP_API_URL in Vercel environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production'
    ? 'https://normalro-backend.vercel.app/api'  // Will need to be updated after backend is deployed
    : 'http://localhost:5000/api');

export default API_BASE_URL; 