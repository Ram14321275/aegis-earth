class CachePolicy:
    DEFAULT_TTL_SECONDS = 21600  # 6 hours

    TTL_SEARCH_RESULTS = 3600  # 1 hour
    TTL_ANALYSIS_RESULTS = 21600  # 6 hours
    TTL_RISK_ASSESSMENTS = 21600  # 6 hours
    TTL_VISUALIZATION_OUTPUTS = 3600  # 1 hour
    TTL_HISTORICAL = 86400  # 24 hours

class TTLPolicyEngine:
    @staticmethod
    def get_dynamic_ttl(hazard_type: str, severity: str, region_stability: str = "stable") -> int:
        """
        Calculates dynamic TTLs based on disaster tiers and severity.
        """
        severity = severity.upper()
        region_stability = region_stability.lower()

        # Historical change-detection results
        if region_stability == "historical":
            return CachePolicy.TTL_HISTORICAL
            
        # Hazard Severity Based TTLs
        if severity == "CRITICAL":
            return 600  # 10 minutes (5-15m range)
        elif severity == "HIGH":
            return 2700  # 45 minutes (30-60m range)
        elif severity == "MODERATE":
            return 9000  # 2.5 hours (2-3h range)
        elif severity == "LOW":
            return CachePolicy.DEFAULT_TTL_SECONDS  # 6 hours
            
        return CachePolicy.DEFAULT_TTL_SECONDS

ttl_policy_engine = TTLPolicyEngine()
