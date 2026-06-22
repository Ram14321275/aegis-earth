class CachePolicy:
    DEFAULT_TTL_SECONDS = 21600  # 6 hours (reduced from 24h)

    TTL_SEARCH_RESULTS = 3600  # 1 hour
    TTL_ANALYSIS_RESULTS = 21600  # 6 hours
    TTL_RISK_ASSESSMENTS = 21600  # 6 hours
    TTL_VISUALIZATION_OUTPUTS = 3600  # 1 hour

class TTLPolicyEngine:
    @staticmethod
    def get_dynamic_ttl(hazard_type: str, severity: str, region_stability: str = "stable") -> int:
        """
        Calculates dynamic TTLs based on disaster tiers.
        """
        severity = severity.upper()
        region_stability = region_stability.lower()
        
        # 1. Critical Disaster Zones: 5-15 minutes
        if severity == "CRITICAL" or region_stability == "active_emergency":
            return 900 # 15 minutes
            
        # 2. Urban Monitoring: 1-3 hours
        if region_stability == "urban_monitoring":
            return 3600 # 1 hour
            
        # 3. Stable Environmental Regions: 6-12 hours
        if region_stability == "stable":
            return CachePolicy.DEFAULT_TTL_SECONDS # 6 hours
            
        # 4. Historical Archives: 24h+
        if region_stability == "historical":
            return 86400 # 24 hours
            
        return CachePolicy.DEFAULT_TTL_SECONDS

ttl_policy_engine = TTLPolicyEngine()
