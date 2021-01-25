sample_hourly_forecasts = [
    {
        "dt": 1611522000,
        "temp": 277.59,
        "feels_like": 273.02,
        "pressure": 1024,
        "humidity": 90,
        "dew_point": 276.1,
        "uvi": 0,
        "clouds": 100,
        "visibility": 10000,
        "wind_speed": 4.37,
        "wind_deg": 56,
        "snow": {"1h": 30.65},
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04n",
            }
        ],
        "pop": 0.48,
    },
    {
        "dt": 1611525600,
        "temp": 278.2,
        "feels_like": 274.12,
        "pressure": 1024,
        "humidity": 86,
        "dew_point": 276.06,
        "uvi": 0,
        "clouds": 99,
        "visibility": 10000,
        "wind_speed": 3.66,
        "wind_deg": 57,
        "rain": {"1h": 30.65},
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04d",
            }
        ],
        "pop": 0.44,
    },
]

sample_current_forecast = {
    "dt": 1611524310,
    "sunrise": 1611524852,
    "sunset": 1611561882,
    "temp": 277.59,
    "feels_like": 275.46,
    "pressure": 1024,
    "humidity": 90,
    "dew_point": 276.1,
    "uvi": 0,
    "clouds": 100,
    "visibility": 10000,
    "wind_speed": 0.89,
    "wind_deg": 97,
    "wind_gust": 1.34,
    "weather": [
        {"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}
    ],
}

sample_daily_forecasts = [
    {
        "dt": 1611540000,
        "sunrise": 1611524852,
        "sunset": 1611561882,
        "temp": {
            "day": 281.95,
            "min": 277.59,
            "max": 282.92,
            "night": 278.95,
            "eve": 280.6,
            "morn": 278.66,
        },
        "feels_like": {"day": 277.62, "night": 275.57, "eve": 277.24, "morn": 274.2},
        "pressure": 1026,
        "humidity": 69,
        "dew_point": 276.7,
        "wind_speed": 4.15,
        "wind_deg": 66,
        "weather": [
            {"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}
        ],
        "clouds": 10,
        "pop": 1,
        "rain": 3.76,
        "uvi": 3.13,
    },
    {
        "dt": 1611626400,
        "sunrise": 1611611218,
        "sunset": 1611648343,
        "temp": {
            "day": 283.44,
            "min": 277.27,
            "max": 283.44,
            "night": 281.41,
            "eve": 281.65,
            "morn": 277.49,
        },
        "feels_like": {"day": 280.54, "night": 279.91, "eve": 279.67, "morn": 274.7},
        "pressure": 1026,
        "humidity": 58,
        "dew_point": 275.67,
        "wind_speed": 1.84,
        "wind_deg": 70,
        "weather": [
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}
        ],
        "clouds": 68,
        "pop": 0.56,
        "uvi": 3.09,
    },
]


def get_sample_one_call_response(
    hourly_forecasts=sample_hourly_forecasts,
    current_forecast=sample_current_forecast,
    daily_forecasts=sample_daily_forecasts,
):
    return {
        "lat": 35,
        "lon": 139,
        "timezone": "Asia/Tokyo",
        "timezone_offset": 32400,
        "current": current_forecast,
        "hourly": hourly_forecasts,
        "daily": daily_forecasts,
    }
