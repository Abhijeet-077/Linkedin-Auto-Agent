# InfluenceOS Deployment Guide

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

### Backend
```bash
cd Backend
vercel --prod
```

### Frontend
```bash
cd Frontend
# Update .env.production with backend URL
vercel --prod
```

### Environment Variables
Set in Vercel dashboard:
- `VITE_API_BASE_URL`: Your backend Vercel URL

## Features
- ✅ AI Content Generation Pipeline
- ✅ Analytics Dashboard  
- ✅ Profile Management
- ✅ Outreach Tools
- ✅ Content Scheduling
- ✅ Responsive Design
- ✅ Error Handling & Fallbacks
