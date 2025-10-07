# Ticketmaster Event Notifier

A simple Python script that checks Ticketmaster daily for new events in your area and sends notifications via [ntfy](https://ntfy.sh).

## Features

- 🎫 Automatically fetches new events from Ticketmaster API
- 📍 Configurable location and search radius
- 🔔 Push notifications via ntfy (self-hosted or ntfy.sh)
- ⏰ Scheduled daily checks at 12:00 PM
- 🐳 Docker support with built-in cron
- 🎭 Customizable event genres

## Prerequisites

- Ticketmaster API key (free at [developer.ticketmaster.com](https://developer.ticketmaster.com))
- ntfy server (use [ntfy.sh](https://ntfy.sh) or self-host)

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings:
```env
# Ticketmaster API
API_KEY=your_ticketmaster_api_key

# Search configuration
CITY_NAME=Nice
COUNTRY_CODE=FR
GEO_POINT=43.7102,7.2620
SEARCH_RADIUS=40
EVENT_GENRE_ID=KnvZfZ7vAe1

# Ntfy notification
NTFY_URL=https://ntfy.sh/your_unique_topic
```

### Finding Your Location

Get coordinates for your city:
- Use [Google Maps](https://maps.google.com) → Right-click → Copy coordinates
- Format: `latitude,longitude` (e.g., `43.7102,7.2620` for Nice)

### Event Genre IDs

Common Ticketmaster genre IDs:
- `KnvZfZ7vAe1` - Comedy/Stand-up shows
- `KZFzniwnSyZfZ7v7nJ` - Music
- `KZFzniwnSyZfZ7v7na` - Arts & Theatre
- `KZFzniwnSyZfZ7v7nn` - Film
- `KZFzniwnSyZfZ7v7n1` - Sports

**Finding Genre IDs:**

Use the Ticketmaster Classifications API to get all available genre IDs:
```bash
curl "https://app.ticketmaster.com/discovery/v2/classifications.json?apikey=YOUR_API_KEY"
```

This returns a JSON with all segments, genres, and subgenres along with their IDs. Genre IDs are international and work across all countries.

## Deployment

### Option 1: Docker (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker logs -f notif-app

# Stop
docker-compose down
```

The container runs continuously with cron executing the script daily at 12:00 PM.

### Option 2: Cron Job

```bash
# Install dependencies
pip install -r requirements.txt

# Test run
python main.py

# Add to crontab
crontab -e
```

Add this line:
```
0 12 * * * cd /path/to/notif-show && python3 main.py
```

## How It Works

1. Script runs daily at 12:00 PM
2. Fetches events that went on sale yesterday
3. Filters duplicates by event name
4. Sends formatted notification for each new event via ntfy
5. Logs execution results

## Logs

**Docker:**
```bash
docker logs -f notif-app
# or
cat logs/notif-show.log
```

**Cron:**
Check your system logs or redirect output in crontab:
```
0 12 * * * cd /path/to/notif-show && python3 main.py >> /var/log/notif-show.log 2>&1
```

## Receiving Notifications

### Using ntfy.sh (Public)
1. Install [ntfy app](https://ntfy.sh) on your phone
2. Subscribe to your topic URL

### Self-Hosted ntfy
1. Follow [ntfy installation guide](https://docs.ntfy.sh/install/)
2. Use your server URL in `.env`

## Troubleshooting

**No notifications received:**
- Check your ntfy subscription is active
- Verify `NTFY_URL` in `.env`
- Test manually: `curl -d "Test" YOUR_NTFY_URL`

**No events found:**
- Check your Ticketmaster API key is valid
- Verify `GEO_POINT` coordinates are correct
- Try increasing `SEARCH_RADIUS`

**Docker container exits:**
- Check logs: `docker logs notif-app`
- Verify `.env` file exists and is valid

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
