import requests


def get_weather(city):

    coordinates = {
        "Chennai": (13.0827, 80.2707),
        "Coimbatore": (11.0168, 76.9558),
        "Bengaluru": (12.9716, 77.5946),
        "Mumbai": (19.0760, 72.8777),
        "Delhi": (28.6139, 77.2090)
    }

    if city not in coordinates:
        return "City not supported by the weather tool."

    latitude, longitude = coordinates[city]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,weather_code"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "city": city,
        "temperature": current["temperature_2m"],
        "weather_code": current["weather_code"]
    }