from typing import List

class LineageBuilder:
    @staticmethod
    def build_path(parent_lineage: str, new_event_id: str) -> str:
        """
        Builds a deterministic lineage path string.
        Format: parent1->parent2->new_event
        """
        if not parent_lineage:
            return new_event_id
        return f"{parent_lineage}->{new_event_id}"

    @staticmethod
    def verify_path(lineage: str, events: List[str]) -> bool:
        """
        Verifies if the lineage matches the sequence of event IDs.
        """
        expected = "->".join(events)
        return expected == lineage
