import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["cod"] == 200:
            return data
        else:
            return "Unexpected response format."
    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400: return "Bad request:\nPlease check your input"
            case 401: return "Unauthorized:\nInvalid API key"
            case 403: return "Forbidden:\nAccess is denied"
            case 404: return "Not found:\nCity not found"
            case 500: return "Internal Server Error:\nPlease try again later"
            case 502: return "Bad Gateway:\nInvalid response from the server"
            case 503: return "Service Unavailable:\nServer is down"
            case 504: return "Gateway Timeout:\nNo response from the server"
            case _: return f"HTTP error occurred:\n{http_error}"
    except requests.exceptions.ConnectionError:
        return "Connection Error:\nCheck your internet connection"
    except requests.exceptions.Timeout:
        return "Timeout Error:\nThe request timed out"
    except requests.exceptions.TooManyRedirects:
        return "Too many Redirects:\nCheck the URL"
    except requests.exceptions.RequestException as req_error:
        return f"Request Error:\n{req_error}"