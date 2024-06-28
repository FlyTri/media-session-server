import asyncio
from aiohttp import web
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as SessionManager
from datetime import datetime
import pytz

PlaybackStatus = [
    "Closed",
    "Opened",
    "Changing",
    "Stopped",
    "Playing",
    "Paused",
]


async def get_current_session(request):
    try:
        sessions = await SessionManager.request_async()
        current_session = sessions.get_current_session()
        metadata = await current_session.try_get_media_properties_async()
        playback_info = current_session.get_playback_info()
        timeline = current_session.get_timeline_properties()
        last_updated_time_timestamp = timeline.last_updated_time.timestamp()

        playing = playback_info.playback_status == PlaybackStatus.index("Playing")

        if playing:
            current_time_timestamp = datetime.now(pytz.utc).timestamp()
            position = (current_time_timestamp - last_updated_time_timestamp) + timeline.position.total_seconds()
        else:
            position = timeline.position.total_seconds()

        data = {
            "source": current_session.source_app_user_model_id,
            "title": metadata.title,
            "artist": metadata.artist,
            "album": metadata.album_title,
            "playing": playing,
            "position": int(position * 1000),
            "duration": timeline.end_time.seconds * 1000
        }

        return web.json_response(data)

    except Exception as e:
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)


async def handle_index(request):
    return web.Response(status=200, content_type='text/plain', text='')


async def main():
    app = web.Application()
    app.router.add_get('/current-session', get_current_session)
    app.router.add_get('/', handle_index)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8170)
    await site.start()

    print(f"HTTP server started at http://localhost:8170")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
