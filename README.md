# Media Sessions Server

## [Download](https://nightly.link/FlyTri/media-sessions-server/workflows/build/main/Executable)

## Endpoints

> Default port is `8170` 

| Method | URL         |
|--------|-------------|
| `GET`  | `/sessions` |

### `/sessions`

Example response:

```json
{
    "size": 2,
    "sessions": [
        {
            "source": "Spotify.exe",
            "album": {
                "artist": "Imagine Dragons",
                "title": "Mercury - Acts 1 & 2",
                "track_count": 0
            },
            "artist": "Imagine Dragons",
            "genres": [],
            "playback": {
                "type": 1,
                "status": 4,
                "rate": null,
                "auto_repeat_mode": 2,
                "is_shuffle_active": false
            },
            "subtitle": "",
            "title": "Waves",
            "track_number": 9,
            "thumbnail": "iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAYAAAB5fY51AAAgAE...",
            "timeline": {
                "position": 166439,
                "duration": 225431,
                "last_updated_time": 1719634209.901196
            }
        },
        {
            "source": "Chrome",
            "album": {
                "artist": "",
                "title": "",
                "track_count": 0
            },
            "artist": "Rick Astley",
            "genres": [],
            "playback": {
                "type": 1,
                "status": 5,
                "rate": 0,
                "auto_repeat_mode": null,
                "is_shuffle_active": null
            },
            "subtitle": "",
            "title": "Rick Astley - Never Gonna Give You Up (Official Music Video) ",
            "track_number": 0,
            "thumbnail": "iVBORw0KGgoAAAANSUhEUgAAAJYAAABUCAIAAADvQ1kKAAAgAE...",
            "timeline": {
                "position": 120317.508,
                "duration": 212061,
                "last_updated_time": 1719634209.36543
            }
        }
    ]
}
```