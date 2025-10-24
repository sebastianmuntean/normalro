# Quick Vercel Setup Guide

## 📦 Two Separate Vercel Projects

You need to create **TWO** separate projects on Vercel from the same repository:

### 1️⃣ Frontend Project

| Setting | Value |
|---------|-------|
| **Root Directory** | `frontend` |
| **Framework** | Create React App (auto-detected) |
| **Build Command** | `npm run build` |
| **Output Directory** | `build` |

**Environment Variables:**
- `REACT_APP_API_URL` = `https://your-backend-name.vercel.app/api`

---

### 2️⃣ Backend Project

| Setting | Value |
|---------|-------|
| **Root Directory** | `backend` |
| **Framework** | Python (auto-detected) |

**Environment Variables:**
- `ALLOWED_ORIGINS` = `https://your-frontend-name.vercel.app,http://localhost:3000`

---

## 🚀 Deployment Steps

### Step 1: Deploy Backend First

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your repository
4. **Set Root Directory to `backend`**
5. Deploy
6. Copy the backend URL (e.g., `https://normalro-backend.vercel.app`)

### Step 2: Configure Backend CORS

1. Go to backend project → Settings → Environment Variables
2. Add `ALLOWED_ORIGINS` with your frontend URL (you'll update this in Step 4)
3. For now, use: `http://localhost:3000`

### Step 3: Deploy Frontend

Your frontend is already deployed! Just need to configure it.

### Step 4: Connect Frontend to Backend

1. Go to frontend project → Settings → Environment Variables
2. Add `REACT_APP_API_URL` = `https://your-backend-name.vercel.app/api`
3. Redeploy frontend

### Step 5: Update Backend CORS

1. Go to backend project → Settings → Environment Variables
2. Update `ALLOWED_ORIGINS` to: `https://your-frontend-name.vercel.app,http://localhost:3000`
3. Redeploy backend

---

## ✅ Verify It Works

Visit your frontend URL and test a tool (e.g., Word Counter or Slug Generator)

---

## 📝 Files Created

- ✅ `backend/vercel.json` - Vercel configuration for Python
- ✅ `backend/index.py` - Entry point for Vercel
- ✅ `backend/app.py` - Updated CORS to use environment variables
- ✅ `frontend/vercel.json` - SPA routing configuration
- ✅ `frontend/src/config/api.js` - Updated to use environment variable

---

## 🔧 Troubleshooting

**Frontend shows CORS errors:**
- Check backend `ALLOWED_ORIGINS` includes your frontend URL
- Redeploy backend after changing env vars

**Backend returns 404:**
- Verify Root Directory is set to `backend`
- Check `backend/vercel.json` exists

**Tools don't work:**
- Check browser console for errors
- Verify `REACT_APP_API_URL` is set correctly in frontend
- Test backend directly: `https://your-backend.vercel.app/api/health`

