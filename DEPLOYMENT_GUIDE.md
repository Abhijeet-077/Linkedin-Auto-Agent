# 🚀 LinkedIn Auto Agent - Deployment Guide

## 🌐 Deployment Options

### 1. Vercel (Full-Stack) - Recommended

#### Option A: Full-Stack Deployment (Frontend + Backend)
```bash
# Deploy from root directory
vercel --prod
```

#### Option B: Frontend Only
```bash
# Deploy from Frontend directory
cd Frontend
vercel --prod
```

#### Option C: Backend Only
```bash
# Deploy from Backend directory  
cd Backend
vercel --prod
```

### 2. GitHub Pages (Frontend Only)

GitHub Pages automatically deploys when you push to the main branch.

**Setup Steps:**
1. Go to repository Settings → Pages
2. Source: "GitHub Actions"
3. The workflow will automatically deploy on push to main

**Access URL:** `https://abhijeet-077.github.io/LinkedIn-Auto-Agent/`

## 🔧 Configuration

### Environment Variables

#### For Vercel (Production)
```env
VITE_API_BASE_URL=https://linkedin-auto-agent.vercel.app
VITE_USE_MOCK_API=false
VITE_GITHUB_PAGES=false
```

#### For GitHub Pages
```env
VITE_USE_MOCK_API=true
VITE_API_BASE_URL=https://linkedin-auto-agent.vercel.app
VITE_GITHUB_PAGES=true
```

## 🐛 Troubleshooting

### Vercel Build Errors
- Ensure all imports use correct paths
- Check that all dependencies are in package.json
- Verify environment variables are set

### GitHub Pages Issues
- Check that GitHub Actions workflow completed successfully
- Ensure Pages is configured to use "GitHub Actions" as source
- Verify the base path in vite.config.ts matches repository name

### Common Issues
1. **404 on refresh**: Ensure SPA routing is configured
2. **API errors**: Check CORS settings and API URLs
3. **Build failures**: Check for missing dependencies or import errors

## 📋 Deployment Checklist

### Before Deploying:
- [ ] All tests pass locally
- [ ] Environment variables configured
- [ ] Build completes without errors
- [ ] API endpoints tested

### After Deploying:
- [ ] Frontend loads correctly
- [ ] API endpoints respond
- [ ] All pages navigate properly
- [ ] Mobile responsiveness works

## 🔗 Live URLs

- **Vercel (Full-Stack)**: https://linkedin-auto-agent.vercel.app
- **GitHub Pages (Frontend)**: https://abhijeet-077.github.io/LinkedIn-Auto-Agent/
- **API Documentation**: https://linkedin-auto-agent.vercel.app/docs
