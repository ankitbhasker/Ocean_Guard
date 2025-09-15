import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
from models import AIAnalysisResult, HazardType, HazardSeverity, SocialMediaPost, HazardReport

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        self.chat_client = None
        self.initialize_client()

    def initialize_client(self):
        """Initialize the LLM client for AI analysis"""
        self.chat_client = LlmChat(
            api_key=self.api_key,
            session_id="ocean-hazard-analysis",
            system_message="""You are an expert marine and coastal hazard detection AI. 
            Analyze text content to identify ocean-related hazards, assess severity, and extract relevant information.
            
            Your analysis should focus on:
            1. Detecting ocean hazards: tsunamis, high waves, marine life anomalies, pollution, oil spills, coastal erosion, unusual weather, debris
            2. Assessing severity levels: low, medium, high, critical
            3. Extracting location information
            4. Performing sentiment analysis
            5. Identifying key phrases and trends
            6. Supporting multiple languages (Hindi, English, Bengali, Tamil, etc.)
            
            Always respond with structured JSON data for analysis results."""
        ).with_model("openai", "gpt-4o-mini")

    async def analyze_text_for_hazards(self, text: str, language: str = "en") -> AIAnalysisResult:
        """Analyze text content for ocean hazard detection"""
        try:
            prompt = f"""
            Analyze the following text for ocean and coastal hazards. The text is in language: {language}
            
            Text to analyze: "{text}"
            
            Please provide analysis in the following JSON format:
            {{
                "hazard_detected": boolean,
                "hazard_types": ["tsunami_warning", "high_waves", "unusual_marine_life", "water_pollution", "oil_spill", "coastal_erosion", "unusual_weather", "debris", "other"],
                "severity_prediction": "low|medium|high|critical",
                "location_mentioned": "extracted location or null",
                "sentiment": "positive|negative|neutral",
                "sentiment_score": float between -1 and 1,
                "confidence_score": float between 0 and 1,
                "key_phrases": ["list", "of", "key", "phrases"],
                "language": "detected language code"
            }}
            
            Focus on marine and coastal hazards. Be conservative in hazard detection to avoid false positives.
            """
            
            user_message = UserMessage(text=prompt)
            response = await self.chat_client.send_message(user_message)
            
            # Parse JSON response
            try:
                analysis_data = json.loads(response)
                
                # Map hazard types to enum values
                hazard_types = []
                for hazard in analysis_data.get("hazard_types", []):
                    try:
                        hazard_types.append(HazardType(hazard))
                    except ValueError:
                        continue
                
                # Map severity
                severity = None
                if analysis_data.get("severity_prediction"):
                    try:
                        severity = HazardSeverity(analysis_data["severity_prediction"])
                    except ValueError:
                        pass
                
                return AIAnalysisResult(
                    text=text,
                    hazard_detected=analysis_data.get("hazard_detected", False),
                    hazard_types=hazard_types,
                    severity_prediction=severity,
                    location_mentioned=analysis_data.get("location_mentioned"),
                    sentiment=analysis_data.get("sentiment", "neutral"),
                    sentiment_score=float(analysis_data.get("sentiment_score", 0.0)),
                    confidence_score=float(analysis_data.get("confidence_score", 0.5)),
                    key_phrases=analysis_data.get("key_phrases", []),
                    language=analysis_data.get("language", language)
                )
                
            except json.JSONDecodeError:
                # Fallback analysis if JSON parsing fails
                return AIAnalysisResult(
                    text=text,
                    hazard_detected=False,
                    hazard_types=[],
                    sentiment="neutral",
                    sentiment_score=0.0,
                    confidence_score=0.1,
                    key_phrases=[],
                    language=language
                )
                
        except Exception as e:
            print(f"AI Analysis error: {e}")
            return AIAnalysisResult(
                text=text,
                hazard_detected=False,
                hazard_types=[],
                sentiment="neutral",
                sentiment_score=0.0,
                confidence_score=0.0,
                key_phrases=[],
                language=language
            )

    async def generate_trend_analysis(self, reports: List[HazardReport], 
                                    social_posts: List[SocialMediaPost]) -> Dict[str, Any]:
        """Generate trend analysis from reports and social media data"""
        try:
            # Prepare data summary for analysis
            report_summary = {
                "total_reports": len(reports),
                "hazard_types": [report.hazard_type.value for report in reports],
                "severities": [report.severity.value for report in reports],
                "recent_descriptions": [report.description[:200] for report in reports[:10]]
            }
            
            social_summary = {
                "total_posts": len(social_posts),
                "platforms": [post.platform for post in social_posts],
                "recent_content": [post.content[:200] for post in social_posts[:10]]
            }
            
            prompt = f"""
            Analyze the following ocean hazard data and generate insights:
            
            Reports Summary: {json.dumps(report_summary)}
            Social Media Summary: {json.dumps(social_summary)}
            
            Please provide trend analysis in JSON format:
            {{
                "trending_keywords": ["list of trending keywords"],
                "emerging_patterns": ["list of emerging patterns"],
                "risk_assessment": "low|medium|high|critical",
                "regional_hotspots": ["list of areas with high activity"],
                "recommendations": ["list of actionable recommendations"],
                "confidence_level": float between 0 and 1
            }}
            """
            
            user_message = UserMessage(text=prompt)
            response = await self.chat_client.send_message(user_message)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "trending_keywords": [],
                    "emerging_patterns": [],
                    "risk_assessment": "low",
                    "regional_hotspots": [],
                    "recommendations": [],
                    "confidence_level": 0.1
                }
                
        except Exception as e:
            print(f"Trend analysis error: {e}")
            return {
                "trending_keywords": [],
                "emerging_patterns": [],
                "risk_assessment": "low",
                "regional_hotspots": [],
                "recommendations": [],
                "confidence_level": 0.0
            }

    async def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        try:
            prompt = f"""
            Translate the following text to {target_language}:
            
            Text: "{text}"
            
            Provide only the translation, no additional text.
            """
            
            user_message = UserMessage(text=prompt)
            response = await self.chat_client.send_message(user_message)
            return response.strip()
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    async def generate_alert_message(self, hazard_type: HazardType, 
                                   severity: HazardSeverity, 
                                   location: str) -> str:
        """Generate appropriate alert message for hazard"""
        try:
            prompt = f"""
            Generate a clear, urgent alert message for the following ocean hazard:
            
            Hazard Type: {hazard_type.value}
            Severity: {severity.value}
            Location: {location}
            
            The message should be:
            - Clear and actionable
            - Appropriate for the severity level
            - Include safety recommendations
            - Be under 200 characters
            - Suitable for both citizens and officials
            """
            
            user_message = UserMessage(text=prompt)
            response = await self.chat_client.send_message(user_message)
            return response.strip()
            
        except Exception as e:
            print(f"Alert generation error: {e}")
            return f"Ocean hazard alert: {hazard_type.value} reported in {location}. Severity: {severity.value}. Please stay alert and follow local guidelines."

# Global AI service instance
ai_service = AIService()
