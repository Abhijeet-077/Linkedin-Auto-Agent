# LinkedIn Forge AutoAgent - Deployment Guide

## Local Development

### Quick Start
```bash
# Run both servers
start.bat

# Or manually:
# Terminal 1 - Backend
cd Backend
python working_server.py

# Terminal 2 - Frontend
cd Frontend
npm run dev
```

### URLs
- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Vercel Deployment

### 🚀 Frontend-Only Deployment (Recommended)

This configuration deploys only the Frontend as a static site with mock API data.

#### Step 1: Vercel Project Setup
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. **Important**: Set Root Directory to `Frontend`
5. Framework Preset: `Vite`
6. Build Command: `npm run build`
7. Output Directory: `dist`

#### Step 2: Environment Variables (Optional)
In Vercel Dashboard → Settings → Environment Variables:
```
VITE_API_BASE_URL=https://your-backend-url.com
```

#### Step 3: Deploy
- Push to `main` branch for automatic deployment
- Or use Vercel CLI: `vercel --prod`

### 🔧 Manual Deployment with Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from Frontend directory
cd Frontend
vercel --prod
```

### ⚙️ Build Configuration
- **Framework**: Vite + React + TypeScript
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Node Version**: 18.x or higher
- **Package Manager**: npm

## Features
- ✅ AI Content Generation Pipeline
- ✅ Analytics Dashboard
- ✅ Profile Management
- ✅ Outreach Tools
- ✅ Content Scheduling
- ✅ Responsive Design
- ✅ Error Handling & Fallbacks
