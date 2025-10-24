# Backend Deployment Guide (Vercel)

## Step 1: Deploy Backend to Vercel

1. **Create a new Vercel project for the backend:**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your repository again (yes, the same repo)
   - **Important:** Set **Root Directory** to `backend`
   - Click "Deploy"

2. **Configure Environment Variables:**
   After deployment, go to:
   - Project Settings → Environment Variables
   - Add the following variable:
     - **Name:** `ALLOWED_ORIGINS`
     - **Value:** `https://normalro-git-main-samkingat-3886s-projects.vercel.app/` (replace with your actual frontend URL)
   - Click "Save"
   - Redeploy the project

3. **Get your Backend URL:**
   - After deployment, copy the URL (e.g., `https://normalro-backend.vercel.app/`)

## Step 2: Update Frontend to Use Backend

1. **Update the frontend API configuration:**
   
   Edit `frontend/src/config/api.js`:
   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_URL || 
     (process.env.NODE_ENV === 'production'
       ? 'https://normalro-backend.vercel.app/api'
       : 'http://localhost:5000/api');
   
   export default API_BASE_URL;
   ```

2. **Add environment variable to frontend Vercel project:**
   - Go to your frontend Vercel project
   - Settings → Environment Variables
   - Add:
     - **Name:** `REACT_APP_API_URL`
     - **Value:** `https://normalro-backend.vercel.app/api`
   - Click "Save"
   - Redeploy the frontend

## Step 3: Update CORS

Once you have both URLs, update the backend CORS:

1. Go to backend Vercel project → Settings → Environment Variables
2. Update `ALLOWED_ORIGINS` to include both:
   - Value: `https://normalro-git-main-samkingat-3886s-projects.vercel.app,http://localhost:3000`
3. Redeploy the backend

## Quick Setup Summary

### Frontend Vercel Project:
- **Root Directory:** `frontend`
- **Framework:** Create React App
- **Environment Variables:**
  - `REACT_APP_API_URL` = `https://normalro-backend.vercel.app/api`

### Backend Vercel Project:
- **Root Directory:** `backend`
- **Framework:** Python (auto-detected)
- **Environment Variables:**
  - `ALLOWED_ORIGINS` = `https://normalro-git-main-samkingat-3886s-projects.vercel.app,http://localhost:3000`

## Testing

1. Visit your frontend URL
2. Try any tool (e.g., Word Counter, Slug Generator)
3. It should now communicate with your backend API

## Troubleshooting

### CORS Errors:
- Make sure `ALLOWED_ORIGINS` in backend includes your frontend URL
- Redeploy backend after changing environment variables

### 404 Errors on Backend:
- Check that the Root Directory is set to `backend`
- Verify `vercel.json` exists in the backend folder

### Build Errors:
- Check the build logs in Vercel
- Ensure `requirements.txt` has all dependencies

