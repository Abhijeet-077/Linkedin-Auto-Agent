# 🚀 Vercel Deployment Guide for LinkedIn Auto Agent

## 🎯 Quick Deployment (Recommended)

### **Method 1: Vercel Dashboard (Easiest)**

1. **Visit [vercel.com](https://vercel.com)** and sign in with GitHub
2. **Click "New Project"**
3. **Import your repository:**
   - Search for: `LinkedIn-Auto-Agent`
   - Click "Import"

4. **Configure Frontend Deployment:**
   ```
   Framework Preset: Vite
   Root Directory: Frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

5. **Add Environment Variables:**
   ```
   VITE_API_BASE_URL = https://your-backend-url.vercel.app
   VITE_USE_MOCK_API = false
   VITE_GITHUB_PAGES = false
   ```

6. **Click "Deploy"** 🚀

### **Method 2: Vercel CLI**

```bash
# 1. Login to Vercel
vercel login

# 2. Deploy Frontend Only (Recommended)
vercel --prod --local-config vercel-frontend-only.json

# 3. Deploy Backend Only (Optional)
vercel --prod --local-config vercel-backend-only.json

# 4. Deploy Full-Stack (Alternative)
vercel --prod
```

## 🔧 Configuration Details

### **Frontend Configuration**
- **Framework:** Vite (React + TypeScript)
- **Build Output:** `Frontend/dist/`
- **Environment:** Production optimized
- **Features:** SPA routing, responsive design, mock API support

### **Backend Configuration**
- **Framework:** FastAPI (Python)
- **Entry Point:** `Backend/api/index.py`
- **Features:** REST API, automatic documentation, CORS enabled

## 🌐 Expected URLs

After deployment, you'll get:
- **Frontend:** `https://linkedin-auto-agent.vercel.app`
- **Backend:** `https://linkedin-auto-agent-api.vercel.app`
- **API Docs:** `https://linkedin-auto-agent-api.vercel.app/docs`

## ✅ Post-Deployment Checklist

### **Frontend Testing:**
- [ ] Homepage loads correctly
- [ ] All navigation links work
- [ ] Content generation page functions
- [ ] Profile analysis page loads
- [ ] Outreach management works
- [ ] Analytics dashboard displays
- [ ] Mobile responsiveness

### **Backend Testing:**
- [ ] Health endpoint: `/health`
- [ ] Content generation: `/api/v1/pipeline/generate`
- [ ] Profile analysis: `/api/v1/profile/analysis`
- [ ] Outreach campaigns: `/api/v1/outreach/campaigns`
- [ ] Analytics: `/api/v1/analytics`
- [ ] API documentation: `/docs`

## 🐛 Troubleshooting

### **Common Issues:**

1. **Build Fails:**
   - Check all imports are correct
   - Verify all dependencies in package.json
   - Ensure environment variables are set

2. **404 Errors:**
   - Verify SPA routing configuration
   - Check vercel.json rewrites
   - Ensure all routes are properly configured

3. **API Errors:**
   - Check CORS configuration
   - Verify API URLs in environment variables
   - Test endpoints individually

### **Solutions:**

```bash
# Rebuild locally to test
npm run build

# Check for TypeScript errors
npm run type-check

# Test API endpoints
curl https://your-api-url.vercel.app/health
```

## 🔄 Continuous Deployment

Vercel automatically redeploys when you push to GitHub:

1. **Push changes to main branch**
2. **Vercel detects changes**
3. **Automatic rebuild and deployment**
4. **Live site updates**

## 📊 Monitoring

- **Vercel Dashboard:** Monitor deployments, analytics, and performance
- **Function Logs:** Debug API issues
- **Analytics:** Track usage and performance metrics

## 🎉 Success!

Once deployed, your LinkedIn Auto Agent will be live and accessible worldwide! 

Share your deployment:
- **Live Demo:** Your Vercel URL
- **GitHub:** https://github.com/Abhijeet-077/LinkedIn-Auto-Agent
- **Documentation:** Available in your repository
