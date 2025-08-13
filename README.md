# 🚀 InfluenceOS - AI-Powered LinkedIn Content Generation Platform

A comprehensive, secure AI-driven platform for LinkedIn content creation, featuring local LLM models (Mistral 7B, Qwen), professional image generation via OpenRouter API, and automated content optimization.

## ✨ **Key Features**
- 🤖 **Local LLM Models**: Mistral 7B & Qwen for free content generation
- 🎨 **AI Image Generation**: Professional images via OpenRouter API with DALL-E
- 📊 **Analytics Dashboard**: Real-time content performance tracking
- 👤 **Profile Optimization**: LinkedIn profile analysis and enhancement
- 📧 **Outreach Automation**: Campaign management and networking tools
- 🔐 **Secure Configuration**: Environment-based API key management

## 🏗️ **Architecture**

### **Frontend** (React + TypeScript + Vite)
- Modern React 18 with TypeScript
- Tailwind CSS + Framer Motion for animations
- Radix UI components for accessibility
- Real-time updates via Server-Sent Events
- Vercel-optimized deployment

### **Backend** (FastAPI + Python)
- FastAPI for high-performance API
- Local LLM integration (Mistral 7B, Qwen)
- OpenRouter API for image generation
- Secure environment-based configuration
- Comprehensive error handling and fallbacks

## 🔐 **Security Features**
- ✅ **No Hardcoded API Keys**: All sensitive data in environment variables
- ✅ **Secure Configuration**: Environment-based settings management
- ✅ **Git Protection**: Comprehensive .gitignore for sensitive files
- ✅ **Error Handling**: Secure logging without exposing credentials
- ✅ **Validation**: Proper API key format and availability checks

## 🚀 **Quick Start**

### **1. Backend Setup**
```bash
cd Backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenRouter API key

# Start server
python start_server.py
```

### **2. Frontend Setup**
```bash
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Or build for production
npm run build
```

### **3. Environment Configuration**
Create `Backend/.env` with:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
HOST=0.0.0.0
PORT=8000
DEBUG=false
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
```

## 🎯 **Usage**

### **Content Generation**
1. Visit the Pipeline page
2. Enter your topic
3. Watch real-time AI generation:
   - Text content (local LLM models)
   - Professional images (OpenRouter + DALL-E)
   - Relevant hashtags
   - Engagement optimization

### **Analytics Dashboard**
- View content performance metrics
- Track engagement rates
- Generate new posts with AI
- Monitor growth trends

### **Profile Optimization**
- Connect LinkedIn account
- Run comprehensive profile analysis
- Get AI-powered improvement suggestions
- Track optimization progress

### **Outreach Campaigns**
- Create targeted outreach campaigns
- Use AI-generated message templates
- Track response rates and engagement
- Manage networking activities

## 🔧 **API Endpoints**

### **Content Generation**
- `POST /api/v1/pipeline/generate` - Start content generation
- `GET /api/v1/pipeline/stream/{id}` - Real-time updates
- `POST /api/v1/generate-image` - Generate images
- `POST /api/v1/posts/create` - Create new posts

### **Analytics & Management**
- `GET /api/v1/analytics` - Get analytics data
- `GET /api/v1/profile/analyze` - Profile analysis
- `POST /api/v1/profile/connect-linkedin` - LinkedIn integration
- `GET /api/v1/outreach/campaigns` - Outreach campaigns

## 🧪 **Testing**

### **Backend Tests**
```bash
cd Backend

# Test API endpoints
python test_api.py

# Test image generation
python test_image_generation.py

# Test security configuration
python test_security.py
```

### **Frontend Tests**
```bash
cd Frontend

# Build test
npm run build

# Type checking
npm run type-check
```

## 📦 **Deployment**

### **Frontend (Vercel)**
1. Connect GitHub repository to Vercel
2. Set root directory to `Frontend`
3. Configure environment variables:
   - `VITE_API_BASE_URL=https://your-backend-domain.com`
4. Deploy automatically

### **Backend (Any Platform)**
1. Set environment variables
2. Install dependencies: `pip install -r requirements.txt`
3. Start server: `python start_server.py`
4. Ensure port 8000 is accessible

## 🔍 **Troubleshooting**

### **Common Issues**
- **API Key Not Found**: Check `.env` file exists and contains `OPENROUTER_API_KEY`
- **Import Errors**: Install dependencies with `pip install -r requirements.txt`
- **CORS Issues**: Update `CORS_ORIGINS` in `.env` file
- **Build Failures**: Clear cache and reinstall dependencies

### **Security Checklist**
- ✅ `.env` file not committed to version control
- ✅ API keys loaded from environment variables
- ✅ No sensitive data in source code
- ✅ Proper error handling without exposing credentials

## 📄 **License**
MIT License - See LICENSE file for details

## 🤝 **Contributing**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 **Support**
For issues and questions:
1. Check the troubleshooting section
2. Run the test scripts to diagnose issues
3. Review the security audit report
4. Open an issue on GitHub

---

**🎯 InfluenceOS: Secure, AI-powered LinkedIn content generation with local models and professional image creation!**
