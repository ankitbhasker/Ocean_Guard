from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict, Any
from models import *
import os
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    async def connect_to_mongo(self):
        self.client = AsyncIOMotorClient(os.environ['MONGO_URL'])
        self.db = self.client[os.environ['DB_NAME']]
        
        # Create indexes for better performance
        await self.create_indexes()

    async def close_mongo_connection(self):
        if self.client:
            self.client.close()

    async def create_indexes(self):
        # Create geospatial index for location-based queries
        await self.db.hazard_reports.create_index([("location.latitude", 1), ("location.longitude", 1)])
        await self.db.hazard_reports.create_index("created_at")
        await self.db.hazard_reports.create_index("hazard_type")
        await self.db.hazard_reports.create_index("severity")
        await self.db.hazard_reports.create_index("status")
        
        await self.db.social_media_posts.create_index("created_at")
        await self.db.social_media_posts.create_index("platform")
        await self.db.social_media_posts.create_index("hazard_relevance_score")
        
        await self.db.users.create_index("username", unique=True)
        await self.db.users.create_index("email", unique=True)
        
        await self.db.alerts.create_index("created_at")
        await self.db.alerts.create_index("is_active")

    # User operations
    async def create_user(self, user: User) -> User:
        await self.db.users.insert_one(user.dict())
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user_data = await self.db.users.find_one({"username": username})
        return User(**user_data) if user_data else None

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        user_data = await self.db.users.find_one({"id": user_id})
        return User(**user_data) if user_data else None

    async def update_user_last_login(self, user_id: str):
        await self.db.users.update_one(
            {"id": user_id},
            {"$set": {"last_login": datetime.utcnow()}}
        )

    # Hazard report operations
    async def create_hazard_report(self, report: HazardReport) -> HazardReport:
        await self.db.hazard_reports.insert_one(report.dict())
        return report

    async def get_hazard_reports(self, skip: int = 0, limit: int = 100, 
                               filters: Dict[str, Any] = None) -> List[HazardReport]:
        query = filters or {}
        cursor = self.db.hazard_reports.find(query).skip(skip).limit(limit).sort("created_at", -1)
        reports = []
        async for report_data in cursor:
            reports.append(HazardReport(**report_data))
        return reports

    async def get_hazard_report_by_id(self, report_id: str) -> Optional[HazardReport]:
        report_data = await self.db.hazard_reports.find_one({"id": report_id})
        return HazardReport(**report_data) if report_data else None

    async def update_hazard_report(self, report_id: str, update_data: Dict[str, Any]) -> bool:
        result = await self.db.hazard_reports.update_one(
            {"id": report_id},
            {"$set": {**update_data, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def get_reports_near_location(self, latitude: float, longitude: float, 
                                      radius_km: float = 10) -> List[HazardReport]:
        # Simple distance calculation for demo (in production use proper geospatial queries)
        reports = await self.get_hazard_reports()
        nearby_reports = []
        for report in reports:
            # Simple distance calculation (not accurate, for demo only)
            lat_diff = abs(report.location.latitude - latitude)
            lon_diff = abs(report.location.longitude - longitude)
            if lat_diff <= 0.1 and lon_diff <= 0.1:  # Roughly 10km
                nearby_reports.append(report)
        return nearby_reports

    # Social media operations
    async def create_social_media_post(self, post: SocialMediaPost) -> SocialMediaPost:
        await self.db.social_media_posts.insert_one(post.dict())
        return post

    async def get_social_media_posts(self, skip: int = 0, limit: int = 100,
                                   platform: Optional[str] = None) -> List[SocialMediaPost]:
        query = {"platform": platform} if platform else {}
        cursor = self.db.social_media_posts.find(query).skip(skip).limit(limit).sort("created_at", -1)
        posts = []
        async for post_data in cursor:
            posts.append(SocialMediaPost(**post_data))
        return posts

    async def update_social_media_post_analysis(self, post_id: str, analysis: Dict[str, Any]) -> bool:
        result = await self.db.social_media_posts.update_one(
            {"id": post_id},
            {"$set": {"ai_analysis": analysis}}
        )
        return result.modified_count > 0

    # Alert operations
    async def create_alert(self, alert: Alert) -> Alert:
        await self.db.alerts.insert_one(alert.dict())
        return alert

    async def get_active_alerts(self, user_role: Optional[UserRole] = None) -> List[Alert]:
        query = {"is_active": True}
        if user_role:
            query["$or"] = [
                {"target_roles": {"$in": [user_role]}},
                {"target_roles": {"$size": 0}}
            ]
        
        cursor = self.db.alerts.find(query).sort("created_at", -1)
        alerts = []
        async for alert_data in cursor:
            alerts.append(Alert(**alert_data))
        return alerts

    async def deactivate_alert(self, alert_id: str) -> bool:
        result = await self.db.alerts.update_one(
            {"id": alert_id},
            {"$set": {"is_active": False}}
        )
        return result.modified_count > 0

    # Dashboard stats
    async def get_dashboard_stats(self) -> DashboardStats:
        total_reports = await self.db.hazard_reports.count_documents({})
        verified_reports = await self.db.hazard_reports.count_documents({"status": "verified"})
        pending_reports = await self.db.hazard_reports.count_documents({"status": "pending"})
        active_alerts = await self.db.alerts.count_documents({"is_active": True})
        social_media_posts = await self.db.social_media_posts.count_documents({})
        users_count = await self.db.users.count_documents({})
        
        # Reports in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        reports_last_24h = await self.db.hazard_reports.count_documents({
            "created_at": {"$gte": yesterday}
        })
        
        # Most common hazard type
        pipeline = [
            {"$group": {"_id": "$hazard_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        most_common = await self.db.hazard_reports.aggregate(pipeline).to_list(1)
        most_common_hazard = most_common[0]["_id"] if most_common else None
        
        return DashboardStats(
            total_reports=total_reports,
            verified_reports=verified_reports,
            pending_reports=pending_reports,
            active_alerts=active_alerts,
            social_media_posts_analyzed=social_media_posts,
            users_count=users_count,
            reports_last_24h=reports_last_24h,
            most_common_hazard=most_common_hazard,
            regional_distribution={}
        )

# Global database instance
database = Database()
