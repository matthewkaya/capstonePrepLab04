class WeatherRecord:
    """Represents one hourly weather record."""

    def __init__(
        self,
        time: str,
        temperature: float | int | None,
        precipitation: float | int | None,
    ) -> None:
        self.time: str = time

        self.temperature: float | int | None = (
            temperature if isinstance(temperature, (int, float)) else None
        )

        self.precipitation: float | int | None = (
            precipitation if isinstance(precipitation, (int, float)) else None
        )

    def __str__(self) -> str:
        return f"{self.time}: {self.temperature} C, {self.precipitation} mm"
