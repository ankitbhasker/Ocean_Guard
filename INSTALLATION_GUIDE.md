# 🌊 Ocean Hazard Platform - Installation Guide

## 📁 Complete Project Structure

```
ocean-hazard-platform/
├── README.md                 # Main project documentation
├── INSTALLATION_GUIDE.md     # This installation guide
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── package.json             # Project metadata and scripts
├── setup.py                 # Automated setup script
├── docker-compose.yml       # Docker configuration
├── start-backend.sh         # Linux/Mac backend startup script
├── start-frontend.sh        # Linux/Mac frontend startup script
├── start-backend.bat        # Windows backend startup script
├── start-frontend.bat       # Windows frontend startup script
├── backend/
│   ├── server.py            # FastAPI main application
│   ├── models.py            # Pydantic data models
│   ├── database.py          # MongoDB operations
│   ├── ai_service.py        # AI/NLP service integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   ├── .env                 # Environment variables (auto-created)
│   └── Dockerfile           # Docker configuration
└── frontend/
    ├── public/
    │   ├── index.html       # HTML template
    │   ├── manifest.json    # PWA manifest
    │   └── favicon.ico      # Site icon
    ├── src/
    │   ├── components/      # React components
    │   │   ├── Navbar.js           # Navigation component
    │   │   ├── LoginForm.js        # Authentication form
    │   │   ├── Dashboard.js        # Main dashboard
    │   │   ├── MapView.js          # Interactive map
    │   │   ├── ReportForm.js       # Hazard reporting form
    │   │   ├── SocialMediaAnalytics.js  # Social media analysis
    │   │   ├── AlertsPanel.js      # Alert management
    │   │   └── ReportsManager.js   # Report management
    │   ├── App.js           # Main React application
    │   ├── App.css          # Application styles
    │   ├── index.js         # React entry point
    │   └── index.css        # Global styles
    ├── package.json         # Node.js dependencies
    ├── tailwind.config.js   # Tailwind CSS configuration
    ├── postcss.config.js    # PostCSS configuration
    ├── craco.config.js      # Create React App configuration
    ├── .env.example         # Environment template
    ├── .env                 # Environment variables (auto-created)
    └── Dockerfile           # Docker configuration
```

## 🚀 Installation Options

### Option 1: Quick Setup (Recommended)

**For Linux/Mac:**
```bash
# Clone or download the project
cd ocean-hazard-platform

# Run automated setup
python setup.py

# Start backend (Terminal 1)
./start-backend.sh

# Start frontend (Terminal 2)  
./start-frontend.sh
```

**For Windows:**
```cmd
# Clone or download the project
cd ocean-hazard-platform

# Run automated setup
python setup.py

# Start backend (Command Prompt 1)
start-backend.bat

# Start frontend (Command Prompt 2)
start-frontend.bat
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8+ (recommended: 3.11)
- Node.js 18+ 
- Yarn package manager
- MongoDB (local or cloud)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Setup environment
cp .env.example .env

# Start backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Setup environment
cp .env.example .env

# Start frontend
yarn start
```

### Option 3: Docker Setup

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Backend Environment (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ocean_hazard_db
CORS_ORIGINS=*
EMERGENT_LLM_KEY=sk-emergent-6C726E321B0C704Eb5
```

### Frontend Environment (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🌐 Access Points

After successful installation:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **MongoDB**: mongodb://localhost:27017

## 🧪 Testing the Installation

### Backend API Test
```bash
# Health check
curl http://localhost:8001/api/health

# Dashboard stats
curl -H "Authorization: Bearer mock_jwt_token" http://localhost:8001/api/dashboard/stats
```

### Frontend Test
1. Open http://localhost:3000
2. Login with any username/password
3. Navigate through all sections:
   - Dashboard ✅
   - Report Hazard ✅
   - Map View ✅
   - Social Analytics ✅
   - Alerts ✅
   - Reports ✅

## 🐳 Database Setup

### Option 1: Local MongoDB
```bash
# Install MongoDB Community Edition
# Start MongoDB service
mongod --dbpath /path/to/your/db

# The application will auto-create collections
```

### Option 2: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/atlas
2. Create cluster
3. Get connection string
4. Update `MONGO_URL` in backend/.env

### Option 3: Docker MongoDB
```bash
# Start MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:7

# Update connection string if needed
```

## 🎯 Features Available

After installation, you'll have access to:

**✅ Core Features:**
- Citizen hazard reporting with geolocation
- Interactive dashboard with real-time statistics
- OpenStreetMap integration with hazard markers
- AI-powered social media analytics
- Multi-language support (9 languages)
- Alert management system
- Report verification workflow

**✅ Technical Features:**
- RESTful API with 15+ endpoints
- MongoDB with geospatial indexing
- AI integration with Emergent LLM
- Responsive web design
- Real-time data updates
- Role-based access control

## 🔍 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check if MongoDB is running
mongosh  # Should connect successfully

# Check port 8001 is free
lsof -i :8001  # Should show no processes
```

**Frontend won't start:**
```bash
# Check Node.js version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
yarn install

# Check port 3000 is free
lsof -i :3000  # Should show no processes
```

**Dependencies issues:**
```bash
# Backend dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Frontend dependencies  
cd frontend
yarn cache clean
yarn install --force
```

**Environment variables:**
- Ensure `.env` files exist in both `backend/` and `frontend/`
- Check that MONGO_URL points to running MongoDB instance
- Verify REACT_APP_BACKEND_URL matches backend server URL

### Getting Help

1. Check the console logs for error messages
2. Verify all prerequisites are installed
3. Ensure MongoDB is running and accessible
4. Check firewall settings for ports 3000, 8001, 27017
5. Review the README.md for additional configuration options

## 📱 Mobile/Responsive Testing

The platform is fully responsive. Test on:
- Desktop (1920x1080+)
- Tablet (768x1024)
- Mobile (375x667)

## 🏆 Production Deployment

For production deployment:

1. **Environment Setup:**
   - Set production MongoDB URI
   - Configure proper CORS origins
   - Set secure secret keys
   - Use environment-specific .env files

2. **Build Process:**
   ```bash
   # Frontend production build
   cd frontend && yarn build
   
   # Backend optimization
   cd backend && pip install gunicorn
   ```

3. **Deployment Options:**
   - Cloud platforms (AWS, GCP, Azure)
   - Container orchestration (Kubernetes)
   - Traditional VPS hosting
   - Serverless deployment

## 📊 Next Steps

After successful installation:

1. **Explore the Dashboard** - View real-time statistics and charts
2. **Create Test Reports** - Use the Report Hazard form
3. **Check the Map** - View hazard locations and markers  
4. **Test AI Features** - Run social media analysis
5. **Review API Docs** - Visit http://localhost:8001/docs
6. **Customize Configuration** - Update .env files as needed

---

**🌊 Ready to monitor ocean hazards and keep our coastlines safe!**

For additional support, refer to the main README.md or create an issue in the project repository.
