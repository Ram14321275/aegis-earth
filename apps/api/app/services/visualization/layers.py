from app.schemas.intelligence import EvidenceLayer


def build_evidence_layers() -> list[EvidenceLayer]:
    return [
        EvidenceLayer(
            id="base-map",
            label="Operational Map",
            type="map",
            description="Coordinate resolved base layer with terrain and urban context.",
        ),
        EvidenceLayer(
            id="risk-heat",
            label="Risk Heat Map",
            type="heatmap",
            description="Composite flood and wildfire intensity layer for operator triage.",
        ),
        EvidenceLayer(
            id="change-diff",
            label="Difference Map",
            type="difference",
            description="Before vs after satellite evidence slot for Sentinel-1 and Sentinel-2 outputs.",
        ),
    ]

