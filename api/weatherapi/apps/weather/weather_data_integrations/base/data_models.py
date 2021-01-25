import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from weatherapi.apps.weather.models import ForecastSpan, WeatherForecasts

LOG = logging.getLogger(__name__)


@dataclass
class WeatherForecast:
    lon: Decimal
    lat: Decimal
    timezone: str
    timestamp: datetime
    temp: Decimal
    pressure: Decimal
    humidity: int
    clouds: int
    wind_speed: Decimal
    wind_deg: int
    rain: Decimal
    snow: Decimal
    status: str
    detailed_status: str
    weather_code: int
    weather_icon_name: str
    forecast_span: ForecastSpan
    dew_point: Decimal
    heat_index: Optional[Decimal] = None
    visibility_distance: Optional[Decimal] = None
    utc_offset: Optional[int] = None
    uvi: Optional[Decimal] = None
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    feels_like: Optional[Decimal] = None
    wind_gust: Optional[Decimal] = None

    def to_weather_forecast_record(self) -> WeatherForecasts:
        return WeatherForecasts(
            lon=self.lon,
            lat=self.lat,
            timestamp=self.timestamp,
            forecast_span=self.forecast_span.value,
            weather_desc_main=self.status,
            timezone=self.timezone,
            temperature=self.temp,
            pressure=self.pressure,
            humidity=self.humidity,
            wind_speed=self.wind_speed,
            visibility=self.visibility_distance,
            uvi=self.uvi,
            misc={
                "clouds": self.clouds,
                "wind_deg": self.wind_deg,
                "rain": self.rain,
                "snow": self.snow,
                "detailed_status": self.detailed_status,
                "weather_code": self.weather_code,
                "weather_icon_name": self.weather_icon_name,
                "dew_point": self.dew_point,
                "heat_index": self.heat_index,
                "utc_offset": self.utc_offset,
                "sunrise": self.sunrise,
                "sunset": self.sunset,
                "feels_like": self.feels_like,
                "wind_gust": self.wind_gust,
            },
        )

    def __str__(self):
        return f"{self.lon}, {self.lat}, {self.timestamp}, {self.forecast_span.value}"
