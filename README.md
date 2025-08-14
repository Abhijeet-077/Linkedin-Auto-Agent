# 🚀 LinkedIn Auto Agent

<div align="center">

**AI-Powered LinkedIn Content Generation & Management Platform**

[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vite](https://img.shields.io/badge/Vite-5.4.19-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/Abhijeet-077/LinkedIn-Auto-Agent?style=for-the-badge)](https://github.com/Abhijeet-077/LinkedIn-Auto-Agent/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Abhijeet-077/LinkedIn-Auto-Agent?style=for-the-badge)](https://github.com/Abhijeet-077/LinkedIn-Auto-Agent/issues)

[🌟 Live Demo](https://linkedin-auto-agent.vercel.app) • [📖 Documentation](https://github.com/Abhijeet-077/LinkedIn-Auto-Agent/wiki) • [🐛 Report Bug](https://github.com/Abhijeet-077/LinkedIn-Auto-Agent/issues) • [💡 Request Feature](https://github.com/Abhijeet-077/LinkedIn-Auto-Agent/issues)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 Demo](#-demo)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🌐 Deployment](#-deployment)
- [🔧 Configuration](#-configuration)
- [📚 API Documentation](#-api-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Smart Content Creation**: Generate engaging LinkedIn posts using advanced AI algorithms
- **Topic-Based Generation**: Create content around specific topics and industries
- **Multiple Content Types**: Support for text posts, carousels, and visual content
- **Hashtag Optimization**: Automatic hashtag generation for maximum reach

### 📊 Analytics & Insights
- **Performance Tracking**: Monitor post engagement, reach, and growth metrics
- **Audience Analytics**: Understand your audience demographics and behavior
- **Optimal Timing**: AI-suggested best times to post for maximum engagement
- **Growth Insights**: Track follower growth and engagement trends

### 👤 Profile Optimization
- **Profile Analysis**: Comprehensive LinkedIn profile scoring and recommendations
- **Completeness Check**: Identify missing profile elements that impact visibility
- **SEO Optimization**: Keyword suggestions for better profile discoverability
- **Professional Branding**: Tips for building a strong personal brand

### 🎯 Outreach Management
- **Campaign Creation**: Design and manage LinkedIn outreach campaigns
- **Template Library**: Pre-built message templates for different scenarios
- **Response Tracking**: Monitor campaign performance and response rates
- **Contact Management**: Organize and track your professional network

### 📅 Content Scheduling
- **Smart Scheduling**: Schedule posts for optimal engagement times
- **Content Calendar**: Visual calendar view of your content pipeline
- **Bulk Scheduling**: Schedule multiple posts in advance
- **Auto-Publishing**: Seamless integration with LinkedIn's publishing API

### 🔧 Advanced Features
- **Multi-Account Support**: Manage multiple LinkedIn profiles
- **Team Collaboration**: Share access with team members
- **Custom Branding**: White-label solution for agencies
- **API Integration**: RESTful API for custom integrations

## 🎯 Demo

### 🖥️ Screenshots

<div align="center">

| Dashboard | Content Generation | Analytics |
|-----------|-------------------|-----------|
| ![Dashboard](https://via.placeholder.com/300x200?text=Dashboard) | ![Content](https://via.placeholder.com/300x200?text=Content+Gen) | ![Analytics](https://via.placeholder.com/300x200?text=Analytics) |

| Profile Analysis | Outreach | Scheduling |
|-----------------|----------|------------|
| ![Profile](https://via.placeholder.com/300x200?text=Profile) | ![Outreach](https://via.placeholder.com/300x200?text=Outreach) | ![Schedule](https://via.placeholder.com/300x200?text=Schedule) |

</div>

### 🌐 Live Demo
- **Frontend Demo**: [https://linkedin-auto-agent.vercel.app](https://linkedin-auto-agent.vercel.app)
- **API Documentation**: [https://linkedin-auto-agent-api.vercel.app/docs](https://linkedin-auto-agent-api.vercel.app/docs)

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18.3.1 with TypeScript
- **Build Tool**: Vite 5.4.19 for fast development and building
- **UI Library**: Tailwind CSS + Shadcn/ui components
- **State Management**: React Query for server state management
- **Routing**: React Router v6 for client-side routing
- **Animations**: Framer Motion for smooth animations
- **Charts**: Recharts for data visualization

### Backend
- **Framework**: FastAPI 0.100.0+ (Python)
- **Server**: Uvicorn ASGI server
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **CORS**: Configured for cross-origin requests
- **Validation**: Pydantic for request/response validation

### Development & Deployment
- **Package Manager**: npm/yarn for frontend, pip for backend
- **Version Control**: Git with GitHub
- **CI/CD**: GitHub Actions for automated deployment
- **Hosting**: Vercel for full-stack deployment
- **Static Hosting**: GitHub Pages for frontend-only deployment

## 🚀 Quick Start

### 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

### ⚡ One-Click Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/LinkedIn-Auto-Agent.git
   cd LinkedIn-Auto-Agent
   ```

2. **Start both servers:**
   ```bash
   # Windows
   start.bat

   # macOS/Linux
   chmod +x start.sh && ./start.sh
   ```

### 🔧 Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Backend Setup
```bash
cd Backend
pip install -r requirements.txt
python working_server.py
```

#### Frontend Setup
```bash
cd Frontend
npm install
npm run dev
```

</details>

### 🌐 Access Your Application

Once both servers are running, access your application at:

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Frontend** | [http://localhost:8080](http://localhost:8080) | Main application interface |
| 🔧 **Backend API** | [http://localhost:8000](http://localhost:8000) | REST API endpoints |
| 📚 **API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive API documentation |

### 🧪 Test the Setup

Run the deployment test to verify everything is working:
```bash
# Windows
test-deployment.bat

# macOS/Linux
chmod +x test-deployment.sh && ./test-deployment.sh
```

## 📁 Project Structure

```
LinkedIn-Auto-Agent/
├── 📁 Frontend/                 # React + TypeScript frontend
│   ├── 📁 src/
│   │   ├── 📁 components/       # Reusable UI components
│   │   ├── 📁 pages/           # Application pages
│   │   ├── 📁 lib/             # Utilities and API calls
│   │   ├── 📁 hooks/           # Custom React hooks
│   │   └── 📄 main.tsx         # Application entry point
│   ├── 📁 public/              # Static assets
│   ├── 📄 package.json         # Dependencies and scripts
│   ├── 📄 vite.config.ts       # Vite configuration
│   └── 📄 tailwind.config.ts   # Tailwind CSS configuration
├── 📁 Backend/                  # FastAPI Python backend
│   ├── 📁 api/                 # API route handlers
│   ├── 📄 working_server.py    # Main FastAPI application
│   ├── 📄 requirements.txt     # Python dependencies
│   └── 📄 vercel.json          # Vercel deployment config
├── 📁 .github/
│   └── 📁 workflows/           # GitHub Actions CI/CD
├── 📄 start.bat               # Windows startup script
├── 📄 start.sh                # Unix startup script
├── 📄 test-deployment.bat     # Windows test script
├── 📄 vercel.json             # Vercel configuration
└── 📄 README.md               # Project documentation
```

## 🌐 Deployment

### 🚀 Vercel (Recommended)

Deploy the full-stack application to Vercel with one command:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to production
vercel --prod
```

**Environment Variables for Vercel:**
```env
VITE_API_BASE_URL=https://your-app.vercel.app
VITE_USE_MOCK_API=false
```

### 📄 GitHub Pages

Deploy frontend-only version to GitHub Pages:

1. **Enable GitHub Pages** in repository settings
2. **Push to main branch** - automatic deployment via GitHub Actions
3. **Access at**: `https://username.github.io/LinkedIn-Auto-Agent/`

### 🐳 Docker Deployment

<details>
<summary>Click to expand Docker instructions</summary>

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual containers
docker build -t linkedin-agent-frontend ./Frontend
docker build -t linkedin-agent-backend ./Backend
```

</details>

## 🔧 Configuration

### 🌍 Environment Variables

#### Frontend (.env)
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK_API=false
VITE_DEBUG=true

# Optional: Analytics
VITE_GA_TRACKING_ID=your_google_analytics_id
```

#### Backend (.env)
```env
# Optional: AI API Keys for enhanced features
OPENROUTER_API_KEY=your_openrouter_key
HUGGINGFACE_TOKEN=your_huggingface_token

# Optional: Database (for production)
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### ⚙️ Customization

- **Branding**: Update colors and logos in `Frontend/src/lib/constants.ts`
- **API Endpoints**: Modify endpoints in `Backend/working_server.py`
- **UI Components**: Customize components in `Frontend/src/components/`

## 📚 API Documentation

### 🔗 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/pipeline/generate` | Generate content |
| `GET` | `/api/v1/analytics` | Get analytics data |
| `GET` | `/api/v1/profile/analysis` | Profile analysis |
| `GET` | `/api/v1/outreach/campaigns` | Get campaigns |
| `POST` | `/api/v1/outreach/campaigns` | Create campaign |

### 📖 Interactive Documentation

Visit [http://localhost:8000/docs](http://localhost:8000/docs) when running locally for full interactive API documentation.

### 🔧 Example API Usage

```javascript
// Generate LinkedIn content
const response = await fetch('/api/v1/pipeline/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: 'AI in Business' })
});

const result = await response.json();
console.log(result.content);
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details

### 💡 Suggesting Features

1. **Check the roadmap** to see if it's already planned
2. **Use the feature request template**
3. **Explain the use case** and potential impact

### 🔧 Development Workflow

1. **Fork the repository**
   ```bash
   git fork https://github.com/Abhijeet-077/LinkedIn-Auto-Agent.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   npm test                    # Frontend tests
   python -m pytest          # Backend tests
   ./test-deployment.bat      # Integration tests
   ```

5. **Submit a pull request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Include screenshots for UI changes

### 📝 Code Style

- **Frontend**: ESLint + Prettier configuration
- **Backend**: Black + isort for Python formatting
- **Commits**: Follow [Conventional Commits](https://conventionalcommits.org/)

## 🗺️ Roadmap

### 🚧 Current Development
- [ ] Real LinkedIn API integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app (React Native)

### 🔮 Future Plans
- [ ] AI-powered audience analysis
- [ ] Automated A/B testing
- [ ] Integration with other social platforms
- [ ] Enterprise features and SSO

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 LinkedIn Auto Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

<div align="center">

**Created with ❤️ by [Abhijeet](https://github.com/Abhijeet-077)**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Abhijeet-077)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/abhijeet-077)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/abhijeet_077)

</div>

## 🙏 Acknowledgments

- **React Team** for the amazing React framework
- **FastAPI** for the high-performance Python web framework
- **Vercel** for seamless deployment platform
- **Tailwind CSS** for the utility-first CSS framework
- **Shadcn/ui** for beautiful, accessible components
- **OpenAI** for AI capabilities inspiration
- **LinkedIn** for the platform that inspired this tool

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Abhijeet-077/LinkedIn-Auto-Agent&type=Date)](https://star-history.com/#Abhijeet-077/LinkedIn-Auto-Agent&Date)

---

<div align="center">

**If you found this project helpful, please consider giving it a ⭐!**

[🔝 Back to Top](#-linkedin-auto-agent)

</div>

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
