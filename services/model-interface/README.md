# model-interface

Defines replaceable contracts for future AI and geospatial models.

No disaster workflow should depend directly on a vendor model. The application should call stable interfaces here so Sentinel, Google Earth Engine, or custom ML models can be swapped without rewriting API or UI logic.

Runtime implementation currently lives in `apps/api/app/services/model_interface`.

