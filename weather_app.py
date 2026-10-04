import requests

print("=== Weather App ===")

city = input("Enter city name: ").strip()

if not city:
    print("Error: City name cannot be empty.")
else:
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "results" not in data:
                print("Error: City not found.")
            else:
                location = data["results"][0]

                latitude = location["latitude"]
                longitude = location["longitude"]
                city_name = location["name"]

                weather_url = "https://api.open-meteo.com/v1/forecast"

                weather_params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                    "temperature_unit": "celsius",
                    "wind_speed_unit": "ms"
                }

                weather_response = requests.get(
                    weather_url,
                    params=weather_params,
                    timeout=10
                )

                if weather_response.status_code == 200:
                    weather = weather_response.json()
                    current = weather["current"]

                    temperature_c = current["temperature_2m"]
                    temperature_f = (temperature_c * 9 / 5) + 32
                    humidity = current["relative_humidity_2m"]
                    wind_speed = current["wind_speed_10m"]
                    weather_code = current["weather_code"]

                    print("\n=== Weather Information ===")
                    print(f"City: {city_name}")
                    print(f"Temperature: {temperature_c:.1f} °C")
                    print(f"Temperature: {temperature_f:.1f} °F")
                    print(f"Humidity: {humidity}%")
                    print(f"Weather Code: {weather_code}")
                    print(f"Wind Speed: {wind_speed:.1f} m/s")

                else:
                    print("Error: Unable to fetch weather data.")

        else:
            print("Error: Unable to find city.")

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")

    except requests.exceptions.RequestException:
        print("Error: Network problem.")