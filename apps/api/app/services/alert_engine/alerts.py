from app.schemas.intelligence import AlertItem, DisasterSignal


def generate_alerts(signals: list[DisasterSignal]) -> list[AlertItem]:
    alerts: list[AlertItem] = []

    for index, signal in enumerate(signals, start=1):
        if signal.risk in {"high", "critical"}:
            title = "Flood watch recommended" if signal.type == "flood" else "Wildfire watch recommended"
            alerts.append(
                AlertItem(
                    id=f"alert-{index}",
                    severity=signal.risk,
                    title=title,
                    message=f"{signal.type.title()} indicators require operational monitoring for the selected area.",
                )
            )

    return alerts

