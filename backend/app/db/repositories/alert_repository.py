from app.db.models.alert import Alert
from app.db.repositories.base_repository import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    pass


alert_repo = AlertRepository(Alert)
