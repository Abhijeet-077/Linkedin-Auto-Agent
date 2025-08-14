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

### ✅ Single Project Deployment (Recommended)

The project is now configured for **automatic deployment** from GitHub:

#### 1. GitHub Integration
- Connect your GitHub repository to Vercel
- Vercel will automatically detect the configuration
- Push to `main` branch triggers automatic deployment

#### 2. Manual Deployment
```bash
# From repository root
npm run build
vercel --prod
```

#### 3. Environment Variables (Optional)
Set in Vercel dashboard if using real backend:
- `VITE_API_BASE_URL`: Your backend API URL

### 🔧 Configuration Details
- **Build Command**: `npm run build` (builds Frontend from root)
- **Output Directory**: `Frontend/dist`
- **Framework**: Automatically detected as Vite/React
- **Routing**: SPA routing configured for React Router

## Features
- ✅ AI Content Generation Pipeline
- ✅ Analytics Dashboard  
- ✅ Profile Management
- ✅ Outreach Tools
- ✅ Content Scheduling
- ✅ Responsive Design
- ✅ Error Handling & Fallbacks
