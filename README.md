# `⊞` [Media Session Server](https://learn.microsoft.com/en-us/uwp/api/windows.media.control)

> [!IMPORTANT]  
> When an executable file created with PyInstaller is flagged as a virus, it's often a false positive due to the bundled files. You can resolve this by adding the executable to the antivirus whitelist or running the original Python script directly.

## [Download](https://nightly.link/FlyTri/media-session-server/workflows/build/main/Executable)

## Endpoints

> Default port is `8170` 

| Method | URL         |
|--------|-------------|
| `GET`  | `/sessions` |

### `GET` `/sessions`

Example response:

```json5
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
                "type": 1, // Nullable
                // | 0 | Unknown  | The media type is unknown.
                // | 1 | Music    | The media type is audio music. 
                // | 2 | Video    | The media type is video.
                // | 3 | Image    | The media type is an image.
                // https://learn.microsoft.com/en-us/uwp/api/windows.media.control.globalsystemmediatransportcontrolssessionplaybackstatus#fields
                "status": 4, 
                // | 0 | Closed   | The media is closed.
                // | 1 | Opened   | The media is opened.
                // | 2 | Changing | The media is changing.
                // | 3 | Stopped  | The media is stopped.
                // | 4 | Playing  | The media is playing.
                // | 5 | Paused   | The media is paused.
                // https://learn.microsoft.com/en-us/uwp/api/windows.media.control.globalsystemmediatransportcontrolssessionplaybackstatus#fields
                "rate": null,
                "auto_repeat_mode": 2, // Nullable
                // | 0 | None     | No repeating.
                // | 1 | Track    | Repeat the current track.
                // | 2 | List     | Repeat the current list of tracks.
                // https://learn.microsoft.com/en-us/uwp/api/windows.media.mediaplaybackautorepeatmode#fields
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
        "..."
    ]
}
```
