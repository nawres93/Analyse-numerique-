from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self):
        self.repository = AnalyticsRepository()

    async def get_analytics(self):

        engagement = await self.repository.get_monthly_engagement()

        usage = await self.repository.get_usage()

        insights = await self.repository.get_quiz_statistics()

        return {
            "engagement": engagement,
            "usage": usage,
            "insights": insights,
        }