# Aegis Earth - Future Roadmap

## Sprint 2: Provider Integrations
- **Google Earth Engine Integration**: Full authentication flow and engine pipeline replacement.
- **Sentinel Hub Connectors**: True satellite metadata parsing utilizing OAuth2 flows.
- **Real-Time WebSockets**: Live pushing of active alerts to the frontend Dashboard to negate manual polling.

## Sprint 3: Advanced Hazard Models
- **Cyclone Tracking**: Implement geospatial storm tracking models calculating potential impact vectors.
- **Landslide Prediction**: Integrating heavy precipitation models with topographical elevation schemas.
- **Drought Monitoring**: Long-term temporal analysis over a sliding 120-day timeframe to detect soil moisture depletion.

## Sprint 4: Machine Learning Pipelines
- Swap out the heuristic Risk Threshold Rule engines with an isolated PyTorch inference microservice.
- Connect direct drone video feeds for micro-level resolution intelligence gathering.

## Post-MVP Architecture Upgrades
- **Kubernetes Migration**: Shift the standard Docker Compose system to highly available K8s pods.
- **Mobile Application**: Launch a specialized React Native app focusing purely on the `AlertFeed` system for ground operators.
