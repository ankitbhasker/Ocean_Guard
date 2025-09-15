# 🌊 Ocean Hazard Reporting Platform

A comprehensive ocean hazard monitoring and social media analytics platform built for Smart India Hackathon (SIH25039).

## 🎯 Features

- **Citizen Hazard Reporting**: Real-time ocean hazard reporting with geolocation
- **Interactive Dashboard**: Statistics, charts, and analytics
- **Map Visualization**: OpenStreetMap integration with hazard markers
- **AI-Powered Social Media Analytics**: NLP-based hazard detection
- **Alert Management**: Real-time alert system for authorities
- **Multi-language Support**: Hindi, English, Bengali, Tamil, and more

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python) + MongoDB + AI Integration
- **Frontend**: React + Tailwind CSS + Chart.js + Leaflet Maps
- **AI**: Emergent LLM (GPT-4o-mini) for NLP processing
- **Database**: MongoDB with geospatial indexing

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (local or cloud)
- Yarn package manager

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update MongoDB connection string if needed

5. **Run the backend**:
   ```bash
   python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   yarn install
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update `REACT_APP_BACKEND_URL` if needed

4. **Run the frontend**:
   ```bash
   yarn start
   ```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 📁 Project Structure

```
ocean-hazard-platform/
├── backend/
│   ├── models.py          # Pydantic models
│   ├── database.py        # MongoDB operations
│   ├── ai_service.py      # AI/NLP service
│   ├── server.py          # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── frontend/
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.js       # Main application
│   │   ├── App.css      # Styles
│   │   └── index.js     # Entry point
│   ├── package.json     # Node dependencies
│   └── .env            # Environment variables
└── README.md           # This file
```

## 🔧 Configuration

### Backend Environment Variables (.env)

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ocean_hazard_db
CORS_ORIGINS=*
EMERGENT_LLM_KEY=your_emergent_llm_key_here
```

### Frontend Environment Variables (.env)

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🧪 Testing

### Backend API Testing

```bash
# Health check
curl http://localhost:8001/api/health

# Get dashboard stats
curl -H "Authorization: Bearer mock_jwt_token" http://localhost:8001/api/dashboard/stats

# Get reports
curl -H "Authorization: Bearer mock_jwt_token" http://localhost:8001/api/reports
```

### Frontend Testing

1. Open http://localhost:3000
2. Navigate through all sections:
   - Dashboard
   - Report Hazard
   - Map View
   - Social Analytics
   - Alerts
   - Reports

## 🤖 AI Features

The platform uses Emergent LLM integration for:
- **Hazard Detection**: Analyzing text for ocean-related threats
- **Sentiment Analysis**: Processing social media content
- **Multi-language Support**: Understanding content in Indian languages
- **Trend Analysis**: Generating insights and recommendations

## 📊 Database Schema

### Hazard Reports
- Title, description, hazard type, severity
- Geolocation with coordinates
- Reporter information and contact details
- AI analysis results and verification status

### Social Media Posts
- Platform, content, author information
- Engagement metrics and hashtags
- AI analysis with confidence scores
- Hazard relevance scoring

### Users & Alerts
- Role-based user management
- Real-time alert system
- Notification targeting by user roles

## 🔒 Authentication

The demo uses mock authentication. Any username/password combination will work for testing purposes.

For production deployment:
- Implement proper JWT authentication
- Add password hashing and validation
- Set up user registration and email verification

## 🌍 Deployment

### Backend Deployment

1. **Prepare for production**:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Environment setup**:
   - Set production MongoDB URI
   - Configure CORS origins
   - Set secure secret keys

3. **Deploy options**:
   - Docker containerization
   - Cloud platforms (AWS, GCP, Azure)
   - Traditional VPS hosting

### Frontend Deployment

1. **Build for production**:
   ```bash
   yarn build
   ```

2. **Deploy options**:
   - Static hosting (Netlify, Vercel)
   - CDN deployment
   - Traditional web hosting

## 🎯 API Endpoints

### Core Endpoints

- `GET /api/health` - Health check
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/reports` - Get hazard reports
- `POST /api/reports` - Create new report
- `GET /api/map/hazards` - Map data
- `GET /api/social-media` - Social media posts
- `GET /api/alerts` - Active alerts

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

## 🏆 SIH25039 Compliance

This platform addresses all requirements from Smart India Hackathon problem statement SIH25039:

✅ **Crowdsourced Reporting**: Citizen-based hazard reporting system  
✅ **Social Media Analytics**: AI-powered content analysis  
✅ **Real-time Monitoring**: Live dashboard and statistics  
✅ **Geographic Visualization**: Interactive map with hazard markers  
✅ **Multi-language Support**: Support for Indian languages  
✅ **Integration Ready**: APIs for INCOIS system integration  
✅ **Alert System**: Automated alerts for high-severity hazards  

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Built for Smart India Hackathon 2025 - Problem Statement SIH25039

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

---

**Made with ❤️ for ocean safety and marine conservation** 🌊

