import logging
import ee
from app.core.config import get_settings

logger = logging.getLogger(__name__)

class GEEAuthenticator:
    _authenticated = False
    _initialized = False

    @classmethod
    def authenticate_and_initialize(cls) -> bool:
        """
        Authenticates with Google Earth Engine using a Service Account and initializes the SDK.
        Returns True if successful, False otherwise.
        """
        if cls._initialized:
            return True

        settings = get_settings()
        
        if not settings.gee_project_id:
            logger.warning("GEE_PROJECT_ID not set. Running in degraded/mock mode.")
            return False

        try:
            # If a service account is provided with a key file
            if settings.gee_service_account and settings.gee_private_key_path:
                logger.info(f"Authenticating GEE using Service Account: {settings.gee_service_account}")
                credentials = ee.ServiceAccountCredentials(
                    settings.gee_service_account, 
                    settings.gee_private_key_path
                )
                ee.Initialize(credentials=credentials, project=settings.gee_project_id)
            else:
                # Fallback to default application credentials if key is missing but project is present
                logger.info("Authenticating GEE using Default Credentials")
                ee.Initialize(project=settings.gee_project_id)

            cls._authenticated = True
            cls._initialized = True
            logger.info("Successfully initialized Google Earth Engine SDK")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Google Earth Engine SDK: {str(e)}")
            return False

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls._authenticated
