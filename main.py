import asyncio
import base64

import aiohttp_cors
from aiohttp import web
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as SessionManager
from winsdk.windows.storage.streams import Buffer, InputStreamOptions


async def read_thumbnail(thumbnail):
    if not thumbnail:
        return None

    read = thumbnail.open_read_async()

    for _ in range(500):
        if read.status != 0:
            break
        await asyncio.sleep(0.01)

    if read.status == 0:
        return None

    buffer = Buffer(5 * 1024 * 1024)
    readable_stream = read.get_results()
    await readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)

    thumbnail_bytes = bytearray(buffer)
    thumbnail_base64 = base64.b64encode(thumbnail_bytes).decode("utf-8")
    return "data:image/png;base64," + thumbnail_base64


async def get_sessions(request):
    try:
        manager = await SessionManager.request_async()
        sessions = manager.get_sessions()
        data = {
            "size": sessions.size,
            "sessions": []
        }

        for session in sessions:
            metadata = await session.try_get_media_properties_async()
            playback_info = session.get_playback_info()
            timeline = session.get_timeline_properties()
            thumbnail = await read_thumbnail(metadata.thumbnail)

            data["sessions"].append({
                "source": session.source_app_user_model_id,
                "album": {
                    "artist": metadata.album_artist,
                    "title": metadata.album_title,
                    "track_count": metadata.album_track_count
                },
                "artist": metadata.artist,
                "genres": list(metadata.genres),
                "playback": {
                    "type": playback_info.playback_type,
                    "status": playback_info.playback_status,
                    "rate": playback_info.playback_rate,
                    "auto_repeat_mode": playback_info.auto_repeat_mode,
                    "is_shuffle_active": playback_info.is_shuffle_active,
                },
                "subtitle": metadata.subtitle,
                "title": metadata.title,
                "track_number": metadata.track_number,
                "thumbnail": thumbnail,
                "timeline": {
                    "position": timeline.position.total_seconds() * 1000,
                    "duration": timeline.end_time.total_seconds() * 1000,
                    "last_updated_time": timeline.last_updated_time.timestamp()
                }
            })

        return web.json_response(data)

    except Exception as error:
        error_message = {"error": str(error)}
        return web.json_response(error_message, status=500)


async def handle_index(request):
    return web.Response(status=200, content_type='text/plain', text='')


async def main():
    app = web.Application()
    app.router.add_get('/sessions', get_sessions)
    app.router.add_get('/', handle_index)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8170)
    await site.start()

    print(f"HTTP server started at http://localhost:8170")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
