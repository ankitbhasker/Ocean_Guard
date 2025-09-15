from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class UserRole(str, Enum):
    CITIZEN = "citizen"
    OFFICIAL = "official"
    RESEARCHER = "researcher"
    ADMIN = "admin"

class HazardType(str, Enum):
    TSUNAMI_WARNING = "tsunami_warning"
    HIGH_WAVES = "high_waves"
    UNUSUAL_MARINE_LIFE = "unusual_marine_life"
    WATER_POLLUTION = "water_pollution"
    OIL_SPILL = "oil_spill"
    COASTAL_EROSION = "coastal_erosion"
    UNUSUAL_WEATHER = "unusual_weather"
    DEBRIS = "debris"
    OTHER = "other"

class HazardSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ReportStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    INVESTIGATING = "investigating"

class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "India"

class MediaFile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_type: str  # image, video, audio
    file_path: str
    file_size: Optional[int] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    phone: Optional[str] = None
    role: UserRole = UserRole.CITIZEN
    full_name: Optional[str] = None
    organization: Optional[str] = None
    verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: Optional[str] = None
    full_name: Optional[str] = None
    organization: Optional[str] = None
    role: UserRole = UserRole.CITIZEN

class UserLogin(BaseModel):
    username: str
    password: str

class HazardReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    hazard_type: HazardType
    severity: HazardSeverity
    location: Location
    reporter_id: str
    reporter_name: Optional[str] = None
    media_files: List[MediaFile] = []
    status: ReportStatus = ReportStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    verification_notes: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    language: str = "en"
    tags: List[str] = []
    contact_info: Optional[str] = None

class HazardReportCreate(BaseModel):
    title: str
    description: str
    hazard_type: HazardType
    severity: HazardSeverity
    location: Location
    contact_info: Optional[str] = None
    language: str = "en"
    tags: List[str] = []

class SocialMediaPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    platform: str  # twitter, facebook, youtube, instagram
    post_id: str
    content: str
    author: str
    author_handle: str
    location: Optional[Location] = None
    created_at: datetime
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    engagement_metrics: Dict[str, int] = {}  # likes, shares, comments
    ai_analysis: Optional[Dict[str, Any]] = None
    hazard_relevance_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    language: str = "en"
    hashtags: List[str] = []
    mentions: List[str] = []

class AIAnalysisResult(BaseModel):
    text: str
    hazard_detected: bool
    hazard_types: List[HazardType] = []
    severity_prediction: Optional[HazardSeverity] = None
    location_mentioned: Optional[str] = None
    sentiment: str  # positive, negative, neutral
    sentiment_score: float = Field(..., ge=-1, le=1)
    confidence_score: float = Field(..., ge=0, le=1)
    key_phrases: List[str] = []
    language: str
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)

class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    message: str
    alert_type: str  # hazard_detected, trend_alert, system_alert
    severity: HazardSeverity
    location: Optional[Location] = None
    affected_area_radius: Optional[float] = None  # in kilometers
    source_type: str  # citizen_report, social_media, ai_detection
    source_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    target_roles: List[UserRole] = []
    metadata: Dict[str, Any] = {}

class TrendAnalysis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    analysis_period_start: datetime
    analysis_period_end: datetime
    location: Optional[Location] = None
    hazard_types_frequency: Dict[HazardType, int] = {}
    trending_keywords: List[str] = []
    sentiment_distribution: Dict[str, float] = {}
    total_reports: int
    verified_reports: int
    social_media_posts: int
    ai_confidence_average: float
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    insights: List[str] = []

class DashboardStats(BaseModel):
    total_reports: int
    verified_reports: int
    pending_reports: int
    active_alerts: int
    social_media_posts_analyzed: int
    users_count: int
    reports_last_24h: int
    most_common_hazard: Optional[HazardType] = None
    average_response_time: Optional[float] = None  # in hours
    regional_distribution: Dict[str, int] = {}
