from typing import List, Dict, Any, Optional
from app.core.fusion.models import AggregationHierarchy

class GeoAggregationEngine:
    """
    Handles scaling from local hazards up to district, state, continental, and global Intelligence summaries.
    Preserves parent-child lineage.
    """
    
    HIERARCHY_LEVELS = ["local", "district", "state", "country", "continental", "global"]

    def aggregate_regions(self, child_assessments: List[Dict[str, Any]], target_level: str, parent_region_id: str) -> Dict[str, Any]:
        """
        Aggregates multiple child assessments into a single parent assessment.
        """
        if not child_assessments:
            return {}
            
        total_score = 0.0
        max_score = 0.0
        
        for child in child_assessments:
            score = child.get("fused_score", 0.0)
            total_score += score
            if score > max_score:
                max_score = score
                
        # Simple rollup logic: heavily weight the maximum hotspot, but also factor in spread.
        # This prevents a massive region with one tiny fire from being marked "low" on average.
        avg_score = total_score / len(child_assessments)
        rolled_up_score = (max_score * 0.7) + (avg_score * 0.3)
        
        hierarchy = AggregationHierarchy(
            level=target_level,
            region_id=parent_region_id,
            parent_region_id=self._get_parent_level_id(target_level, parent_region_id)
        )
        
        return {
            "fused_score": rolled_up_score,
            "aggregation_hierarchy": hierarchy.model_dump(),
            "child_count": len(child_assessments),
            "max_hotspot_score": max_score
        }
        
    def _get_parent_level_id(self, current_level: str, current_region_id: str) -> Optional[str]:
        # In a real geospatial system, this maps exactly to a boundary DB.
        # For MVP we return a mock parent ID.
        try:
            idx = self.HIERARCHY_LEVELS.index(current_level)
            if idx + 1 < len(self.HIERARCHY_LEVELS):
                parent_level = self.HIERARCHY_LEVELS[idx + 1]
                return f"{parent_level}-parent-of-{current_region_id}"
        except ValueError:
            pass
        return None

geo_aggregation_engine = GeoAggregationEngine()
