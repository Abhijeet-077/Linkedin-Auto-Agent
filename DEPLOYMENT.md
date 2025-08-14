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

### Important: Deploy as Separate Projects

#### 1. Deploy Backend First
```bash
cd Backend
vercel --prod
```
Note the deployed URL (e.g., https://your-backend.vercel.app)

#### 2. Deploy Frontend
```bash
cd Frontend
# Update .env.production with backend URL
echo "VITE_API_BASE_URL=https://your-backend.vercel.app" > .env.production
vercel --prod
```

### Environment Variables
Set in Vercel dashboard for Backend:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `HUGGINGFACE_TOKEN`: Your Hugging Face token
- `SECRET_KEY`: Random secret key

Set in Vercel dashboard for Frontend:
- `VITE_API_BASE_URL`: Your backend Vercel URL

### Deployment Steps:
1. Create two separate Vercel projects
2. Deploy Backend project from `/Backend` folder
3. Deploy Frontend project from `/Frontend` folder
4. Update Frontend environment variables with Backend URL

## Features
- ✅ AI Content Generation Pipeline
- ✅ Analytics Dashboard  
- ✅ Profile Management
- ✅ Outreach Tools
- ✅ Content Scheduling
- ✅ Responsive Design
- ✅ Error Handling & Fallbacks
