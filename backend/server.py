from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Import local modules
from models import *
from database import database
from ai_service import ai_service

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect_to_mongo()
    print("Connected to MongoDB")
    
    # Initialize some mock data
    await initialize_mock_data()
    
    yield
    
    # Shutdown
    await database.close_mongo_connection()
    print("Disconnected from MongoDB")

# Create the main app
app = FastAPI(lifespan=lifespan, title="Ocean Hazard Reporting Platform", version="1.0.0")

# Create API router
api_router = APIRouter(prefix="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize mock data
async def initialize_mock_data():
    """Initialize the system with mock data for demonstration"""
    try:
        # Create admin user if not exists
        admin_user = await database.get_user_by_username("admin")
        if not admin_user:
            admin = User(
                username="admin",
                email="admin@oceanhazard.com",
                role=UserRole.ADMIN,
                full_name="System Administrator",
                verified=True
            )
            await database.create_user(admin)
            print("Created admin user")

        # Create some mock social media posts
        mock_posts = [
            SocialMediaPost(
                platform="twitter",
                post_id="mock_tweet_1",
                content="Unusual high waves observed near Marina Beach Chennai. Fishermen advised to stay away. #ChennaiWeather #MarineAlert",
                author="Local Fisher",
                author_handle="@chennai_fisher",
                location=Location(latitude=13.0522, longitude=80.2613, city="Chennai", state="Tamil Nadu"),
                created_at=datetime.utcnow() - timedelta(hours=2),
                hashtags=["#ChennaiWeather", "#MarineAlert"],
                engagement_metrics={"likes": 45, "retweets": 23, "comments": 12}
            ),
            SocialMediaPost(
                platform="facebook",
                post_id="mock_fb_1",
                content="Oil spill spotted off Goa coast. Marine life seems affected. Authorities should take immediate action!",
                author="Environmental Activist",
                author_handle="@goa_environment",
                location=Location(latitude=15.2993, longitude=74.1240, city="Panaji", state="Goa"),
                created_at=datetime.utcnow() - timedelta(hours=5),
                hashtags=["#OilSpill", "#Goa", "#MarinePollution"],
                engagement_metrics={"likes": 156, "shares": 89, "comments": 34}
            ),
            SocialMediaPost(
                platform="youtube",
                post_id="mock_yt_1",
                content="Tsunami warning issued for Kerala coast. All coastal residents must evacuate immediately. This is not a drill!",
                author="Kerala Disaster Management",
                author_handle="@kerala_disaster",
                location=Location(latitude=10.8505, longitude=76.2711, city="Kochi", state="Kerala"),
                created_at=datetime.utcnow() - timedelta(minutes=30),
                hashtags=["#TsunamiAlert", "#Kerala", "#Emergency"],
                engagement_metrics={"likes": 892, "shares": 567, "comments": 234}
            )
        ]

        for post in mock_posts:
            try:
                await database.create_social_media_post(post)
            except:
                pass  # Skip if already exists

        # Create some mock hazard reports
        mock_reports = [
            HazardReport(
                title="High Waves at Juhu Beach",
                description="Observed unusually high waves at Juhu Beach. Waves reaching 8-10 feet high. Many people still in water despite warnings.",
                hazard_type=HazardType.HIGH_WAVES,
                severity=HazardSeverity.HIGH,
                location=Location(latitude=19.1076, longitude=72.8262, city="Mumbai", state="Maharashtra"),
                reporter_id="citizen_1",
                reporter_name="Ravi Kumar",
                status=ReportStatus.VERIFIED,
                contact_info="9876543210",
                tags=["waves", "beach", "safety"]
            ),
            HazardReport(
                title="Marine Debris Accumulation",
                description="Large amounts of plastic and fishing nets washed ashore. Affecting turtle nesting sites.",
                hazard_type=HazardType.DEBRIS,
                severity=HazardSeverity.MEDIUM,
                location=Location(latitude=11.9416, longitude=79.8083, city="Pondicherry", state="Pondicherry"),
                reporter_id="citizen_2",
                reporter_name="Priya Sharma",
                status=ReportStatus.PENDING,
                contact_info="priya.sharma@email.com",
                tags=["debris", "pollution", "marine_life"]
            )
        ]

        for report in mock_reports:
            try:
                await database.create_hazard_report(report)
            except:
                pass  # Skip if already exists

        print("Mock data initialized successfully")
        
    except Exception as e:
        print(f"Error initializing mock data: {e}")

# Authentication dependency (simplified for demo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # For demo purposes, return a mock user
    # In production, validate JWT token here
    return User(
        id="current_user_id",
        username="demo_user",
        email="demo@example.com",
        role=UserRole.CITIZEN,
        full_name="Demo User"
    )

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.OFFICIAL]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# User management endpoints
@api_router.post("/auth/register", response_model=User)
async def register_user(user_data: UserCreate):
    # Check if user already exists
    existing_user = await database.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create new user (password handling simplified for demo)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        full_name=user_data.full_name,
        organization=user_data.organization,
        role=user_data.role
    )
    
    created_user = await database.create_user(new_user)
    return created_user

@api_router.post("/auth/login")
async def login_user(login_data: UserLogin):
    user = await database.get_user_by_username(login_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Password verification simplified for demo
    await database.update_user_last_login(user.id)
    
    return {
        "access_token": "mock_jwt_token",
        "token_type": "bearer",
        "user": user
    }

# Hazard report endpoints
@api_router.post("/reports", response_model=HazardReport)
async def create_report(
    report_data: HazardReportCreate,
    current_user: User = Depends(get_current_user)
):
    # Create new hazard report
    new_report = HazardReport(
        title=report_data.title,
        description=report_data.description,
        hazard_type=report_data.hazard_type,
        severity=report_data.severity,
        location=report_data.location,
        reporter_id=current_user.id,
        reporter_name=current_user.full_name,
        contact_info=report_data.contact_info,
        language=report_data.language,
        tags=report_data.tags
    )
    
    # Perform AI analysis on the report
    try:
        ai_analysis = await ai_service.analyze_text_for_hazards(
            f"{report_data.title} {report_data.description}",
            report_data.language
        )
        new_report.ai_analysis = ai_analysis.dict()
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
    
    created_report = await database.create_hazard_report(new_report)
    
    # Generate alert if high severity
    if report_data.severity in [HazardSeverity.HIGH, HazardSeverity.CRITICAL]:
        alert_message = await ai_service.generate_alert_message(
            report_data.hazard_type,
            report_data.severity,
            report_data.location.city or "Unknown location"
        )
        
        alert = Alert(
            title=f"High Severity Hazard Alert",
            message=alert_message,
            alert_type="hazard_detected",
            severity=report_data.severity,
            location=report_data.location,
            source_type="citizen_report",
            source_id=created_report.id,
            target_roles=[UserRole.OFFICIAL, UserRole.ADMIN]
        )
        await database.create_alert(alert)
    
    return created_report

@api_router.get("/reports", response_model=List[HazardReport])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    hazard_type: Optional[HazardType] = None,
    severity: Optional[HazardSeverity] = None,
    status: Optional[ReportStatus] = None,
    current_user: User = Depends(get_current_user)
):
    filters = {}
    if hazard_type:
        filters["hazard_type"] = hazard_type.value
    if severity:
        filters["severity"] = severity.value
    if status:
        filters["status"] = status.value
    
    reports = await database.get_hazard_reports(skip, limit, filters)
    return reports

@api_router.get("/reports/{report_id}", response_model=HazardReport)
async def get_report(report_id: str, current_user: User = Depends(get_current_user)):
    report = await database.get_hazard_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@api_router.put("/reports/{report_id}/verify")
async def verify_report(
    report_id: str,
    verification_data: Dict[str, str],
    admin_user: User = Depends(get_admin_user)
):
    update_data = {
        "status": ReportStatus.VERIFIED.value,
        "verified_by": admin_user.id,
        "verified_at": datetime.utcnow(),
        "verification_notes": verification_data.get("notes", "")
    }
    
    success = await database.update_hazard_report(report_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {"message": "Report verified successfully"}

@api_router.get("/reports/nearby/{latitude}/{longitude}")
async def get_nearby_reports(
    latitude: float,
    longitude: float,
    radius: float = 10.0,
    current_user: User = Depends(get_current_user)
):
    reports = await database.get_reports_near_location(latitude, longitude, radius)
    return reports

# Social media endpoints
@api_router.get("/social-media", response_model=List[SocialMediaPost])
async def get_social_media_posts(
    skip: int = 0,
    limit: int = 50,
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    posts = await database.get_social_media_posts(skip, limit, platform)
    return posts

@api_router.post("/social-media/analyze")
async def analyze_social_media_batch(admin_user: User = Depends(get_admin_user)):
    """Analyze all unanalyzed social media posts"""
    posts = await database.get_social_media_posts(limit=100)
    analyzed_count = 0
    
    for post in posts:
        if not post.ai_analysis:
            try:
                analysis = await ai_service.analyze_text_for_hazards(post.content)
                analysis_dict = analysis.dict()
                
                # Update hazard relevance score
                post.hazard_relevance_score = analysis.confidence_score if analysis.hazard_detected else 0.0
                post.sentiment_score = analysis.sentiment_score
                
                await database.update_social_media_post_analysis(post.id, analysis_dict)
                analyzed_count += 1
                
                # Create alert for high-confidence hazard detection
                if analysis.hazard_detected and analysis.confidence_score > 0.7:
                    alert = Alert(
                        title="Social Media Hazard Detection",
                        message=f"Potential hazard detected on {post.platform}: {post.content[:100]}...",
                        alert_type="social_media_detection",
                        severity=analysis.severity_prediction or HazardSeverity.MEDIUM,
                        location=post.location,
                        source_type="social_media",
                        source_id=post.id,
                        target_roles=[UserRole.OFFICIAL, UserRole.ADMIN]
                    )
                    await database.create_alert(alert)
                
            except Exception as e:
                logger.error(f"Failed to analyze post {post.id}: {e}")
    
    return {"analyzed_posts": analyzed_count}

# Alert endpoints
@api_router.get("/alerts", response_model=List[Alert])
async def get_alerts(current_user: User = Depends(get_current_user)):
    alerts = await database.get_active_alerts(current_user.role)
    return alerts

@api_router.post("/alerts/{alert_id}/deactivate")
async def deactivate_alert(
    alert_id: str,
    admin_user: User = Depends(get_admin_user)
):
    success = await database.deactivate_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deactivated successfully"}

# Dashboard endpoints
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    stats = await database.get_dashboard_stats()
    return stats

@api_router.get("/dashboard/trends")
async def get_trend_analysis(
    days: int = 7,
    current_user: User = Depends(get_current_user)
):
    # Get recent data
    start_date = datetime.utcnow() - timedelta(days=days)
    
    reports = await database.get_hazard_reports(
        filters={"created_at": {"$gte": start_date}}
    )
    social_posts = await database.get_social_media_posts(limit=200)
    
    # Generate AI-powered trend analysis
    trends = await ai_service.generate_trend_analysis(reports, social_posts)
    
    return {
        "analysis_period_days": days,
        "start_date": start_date,
        "end_date": datetime.utcnow(),
        "total_reports": len(reports),
        "total_social_posts": len(social_posts),
        "trends": trends
    }

# Map data endpoints
@api_router.get("/map/hazards")
async def get_map_hazards(
    hazard_type: Optional[HazardType] = None,
    severity: Optional[HazardSeverity] = None,
    current_user: User = Depends(get_current_user)
):
    """Get hazard data formatted for map display"""
    filters = {}
    if hazard_type:
        filters["hazard_type"] = hazard_type.value
    if severity:
        filters["severity"] = severity.value
    
    reports = await database.get_hazard_reports(limit=500, filters=filters)
    
    # Format for map display
    map_data = []
    for report in reports:
        map_data.append({
            "id": report.id,
            "title": report.title,
            "description": report.description[:200] + "..." if len(report.description) > 200 else report.description,
            "hazard_type": report.hazard_type.value,
            "severity": report.severity.value,
            "status": report.status.value,
            "latitude": report.location.latitude,
            "longitude": report.location.longitude,
            "address": report.location.address,
            "city": report.location.city,
            "created_at": report.created_at.isoformat(),
            "reporter_name": report.reporter_name,
            "tags": report.tags
        })
    
    return map_data

# Translation endpoint
@api_router.post("/translate")
async def translate_text(
    text: str = Form(...),
    target_language: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    translated = await ai_service.translate_text(text, target_language)
    return {"translated_text": translated}

# File upload endpoint (simplified)
@api_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # For demo purposes, just return file info
    # In production, save to cloud storage
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
        "message": "File upload functionality - would save to cloud storage in production"
    }

# Include router in app
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Ocean Hazard Reporting Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }
