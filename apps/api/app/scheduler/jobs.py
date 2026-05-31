from apscheduler.schedulers.background import BackgroundScheduler

_scheduler: BackgroundScheduler | None = None


def configure_scheduler() -> BackgroundScheduler:
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.start(paused=True)
    _scheduler = scheduler
    return scheduler

