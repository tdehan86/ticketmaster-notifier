import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ticketmaster API configuration
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

# Search configuration
CITY_NAME = os.getenv("CITY_NAME", "Paris")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", "FR")
GEO_POINT = os.getenv("GEO_POINT", "48.8566,2.3522")
SEARCH_RADIUS = os.getenv("SEARCH_RADIUS", "40")
EVENT_GENRE_ID = os.getenv("EVENT_GENRE_ID", "KnvZfZ7vAe1")

# Ntfy configuration
NTFY_URL = os.getenv("NTFY_URL")


def fetch_events():
    """Fetch events from Ticketmaster API for the configured location."""
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    params = {
        "apikey": API_KEY,
        "locale": "*",
        "city": CITY_NAME,
        "countryCode": COUNTRY_CODE,
        "onsaleOnStartDate": yesterday,
        "genreId": EVENT_GENRE_ID,
        "geoPoint": GEO_POINT,
        "radius": SEARCH_RADIUS,
        "unit": "km",
        "size": 100,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if "_embedded" in data:
            events = data["_embedded"]["events"]

            # Remove duplicates based on event name
            seen = set()
            filtered_events = []

            for event in events:
                name = event["name"]
                if name not in seen:
                    seen.add(name)
                    filtered_events.append(event)

            return filtered_events

    return []


def generate_message(event):
    """Generate a formatted message for an event."""
    event_name = event.get("name", "Name not available")
    venue_name = "Venue not available"

    if "_embedded" in event and "venues" in event["_embedded"]:
        venue_name = event["_embedded"]["venues"][0].get("name", "Venue not available")

    event_url = event.get("url", "Link not available")
    event_date = event["dates"]["start"].get("localDate", "Date unknown")
    event_time = event["dates"]["start"].get("localTime", "")

    if event_time:
        event_date += f" at {event_time}"

    genre = "Genre not available"
    if "classifications" in event and event["classifications"]:
        genre_name = event["classifications"][0]["genre"].get("name", "")
        subgenre_name = event["classifications"][0]["subGenre"].get("name", "")
        if genre_name and subgenre_name:
            genre = f"{genre_name}/{subgenre_name}"

    message = (
        f"🎭 {event_name}\n"
        f"🕒 Date and time: {event_date}\n"
        f"📍 Venue: {venue_name}\n"
        f"📚 Genre: {genre}\n"
        f"🔗 More info: {event_url}"
    )

    return message


def send_notification(message):
    """Send a notification via ntfy."""
    if not NTFY_URL:
        print("Error: NTFY_URL is not configured in the .env file")
        return False

    try:
        response = requests.post(
            NTFY_URL,
            data=message.encode('utf-8'),
            headers={
                "Title": "New Ticketmaster Event",
                "Priority": "default",
                "Tags": "ticket,calendar"
            }
        )

        if response.status_code == 200:
            print(f"✓ Notification sent successfully (status: {response.status_code})")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Error sending notification: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Exception while sending: {e}")
        return False


def main():
    """Main function."""
    print(f"🔍 Searching for events in {CITY_NAME} ({COUNTRY_CODE})...")

    events = fetch_events()

    if events:
        print(f"✓ {len(events)} event(s) found")

        for event in events:
            message = generate_message(event)
            send_notification(message)
            print(f"  → {event['name']}")
    else:
        print("ℹ No new events found")


if __name__ == "__main__":
    main()
