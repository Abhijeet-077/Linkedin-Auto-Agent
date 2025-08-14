# 🚀 LinkedIn Forge AutoAgent

> **AI-Powered LinkedIn Content Generation & Management Platform**

[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com)
[![React](https://img.shields.io/badge/React-18.3.1-blue?style=for-the-badge&logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.2-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org)
[![Vite](https://img.shields.io/badge/Vite-5.4.19-purple?style=for-the-badge&logo=vite)](https://vitejs.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🌐 Deployment](#-deployment)
- [🔧 Configuration](#-configuration)
- [📱 Screenshots](#-screenshots)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### 🎯 **Core Functionality**
- **🤖 AI Content Pipeline**: Intelligent content generation with trend analysis
- **📊 Analytics Dashboard**: Comprehensive engagement metrics and insights
- **📅 Content Calendar**: Smart scheduling and optimal posting times
- **👤 Profile Management**: LinkedIn profile optimization and analysis
- **📧 Outreach Tools**: Automated campaign management and templates
- **🎨 Visual Content**: AI-powered image generation for posts

### 🔥 **Advanced Features**
- **📈 Real-time Analytics**: Live engagement tracking and performance metrics
- **🎯 A/B Testing**: Content optimization through intelligent testing
- **🏷️ Smart Hashtags**: AI-optimized hashtag recommendations
- **🌟 Brand Voice**: Consistent brand voice across all content
- **📱 Responsive Design**: Seamless experience across all devices
- **⚡ Real-time Updates**: Live pipeline progress and instant feedback

## 🛠️ Tech Stack

### **Frontend**
- **React 18.3.1** - Modern UI library with hooks
- **TypeScript 5.6.2** - Type-safe development
- **Vite 5.4.19** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Radix UI** - Accessible component primitives

### **Backend**
- **FastAPI 0.115.6** - High-performance Python API
- **OpenRouter API** - AI model integration
- **Hugging Face** - ML model hosting
- **Pydantic** - Data validation
- **HTTPX** - Async HTTP client

### **Deployment & DevOps**
- **Vercel** - Serverless deployment platform
- **GitHub Actions** - CI/CD automation
- **ESLint** - Code quality enforcement
- **PostCSS** - CSS processing

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+ and npm
- Python 3.9+ (for backend development)
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/Abhijeet-077/linkedin-forge-AutoAgent.git
cd linkedin-forge-AutoAgent
```

### **2. Quick Launch**
```bash
# Windows
start.bat

# Manual start
# Terminal 1 - Frontend
cd Frontend
npm install
npm run dev

# Terminal 2 - Backend (optional for local development)
cd Backend
pip install -r requirements.txt
python working_server.py
```

### **3. Access Application**
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
linkedin-forge-AutoAgent/
├── 🎨 Frontend/                 # React TypeScript Application
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/              # Application pages
│   │   ├── lib/                # Utilities and API functions
│   │   ├── contexts/           # React contexts
│   │   └── hooks/              # Custom React hooks
│   ├── public/                 # Static assets
│   └── dist/                   # Build output
├── 🔧 Backend/                  # FastAPI Python Server
│   ├── api/                    # API endpoints
│   ├── working_server.py       # Main server file
│   └── requirements.txt        # Python dependencies
├── 📚 Documentation/
│   ├── README.md              # This file
│   └── DEPLOYMENT.md          # Deployment guide
└── 🚀 Deployment/
    ├── vercel.json            # Vercel configuration
    ├── package.json           # Root package configuration
    └── start.bat              # Quick start script
```

## 🌐 Deployment

### **Vercel Deployment (Recommended)**

The application is configured for **automatic deployment** via GitHub integration:

#### **🔄 Automatic Deployment**
1. **Connect Repository**: Link your GitHub repo to Vercel
2. **Auto-Deploy**: Push to `main` branch triggers deployment
3. **Live URL**: Get instant production URL

#### **⚙️ Manual Deployment**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### **🌍 Environment Variables**
Set in Vercel Dashboard (optional for mock mode):
```env
VITE_API_BASE_URL=https://your-backend-api.vercel.app
```

### **Local Development**
```bash
# Quick start
npm run dev

# Full development with backend
start.bat
```

## 🔧 Configuration

### **Frontend Configuration**
- **Vite Config**: `Frontend/vite.config.ts`
- **Tailwind**: `Frontend/tailwind.config.ts`
- **TypeScript**: `Frontend/tsconfig.json`

### **API Configuration**
- **Mock Mode**: Set `USE_MOCK_API = true` in `Frontend/src/lib/api.ts`
- **Production**: Set `USE_MOCK_API = false` for real backend integration

### **Build Configuration**
- **Build Command**: `cd Frontend && npm install && npm run build`
- **Output Directory**: `Frontend/dist`
- **Framework**: Vite (auto-detected)

## 📱 Screenshots

### **🎨 AI Content Pipeline**
> Intelligent content generation with real-time progress tracking

### **📊 Analytics Dashboard**
> Comprehensive metrics with engagement insights and growth trends

### **📅 Content Calendar**
> Smart scheduling with optimal posting time recommendations

### **👤 Profile Management**
> LinkedIn profile analysis with actionable recommendations

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/linkedin-forge-AutoAgent.git
cd linkedin-forge-AutoAgent

# Install dependencies
cd Frontend && npm install

# Start development
npm run dev
```

### **Contribution Guidelines**
1. **🔀 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **💾 Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **📤 Push** to branch (`git push origin feature/amazing-feature`)
5. **🔄 Open** a Pull Request

### **Code Standards**
- **TypeScript** for type safety
- **ESLint** for code quality
- **Prettier** for formatting
- **Conventional Commits** for commit messages

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter** for AI model access
- **Vercel** for seamless deployment
- **Radix UI** for accessible components
- **Tailwind CSS** for utility-first styling
- **React Community** for amazing ecosystem

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

[🐛 Report Bug](https://github.com/Abhijeet-077/linkedin-forge-AutoAgent/issues) • [✨ Request Feature](https://github.com/Abhijeet-077/linkedin-forge-AutoAgent/issues) • [💬 Discussions](https://github.com/Abhijeet-077/linkedin-forge-AutoAgent/discussions)

**Made with ❤️ by [Abhijeet](https://github.com/Abhijeet-077)**

</div>
