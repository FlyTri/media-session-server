import asyncio

import aiohttp_cors
from aiohttp import web
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as SessionManager


async def spotify():
    manager = await SessionManager.request_async()
    current = manager.get_current_session()

    if current.source_app_user_model_id == "Spotify.exe":
        return current
    else:
        return None


async def get_session(request):
    session = await spotify()

    if session:
        metadata = await session.try_get_media_properties_async()
        playback_info = session.get_playback_info()
        timeline = session.get_timeline_properties()

        return web.json_response({
            "title": metadata.title,
            "artist": metadata.artist,
            "album": {
                "artist": metadata.album_artist,
                "title": metadata.album_title,
                "track_count": metadata.album_track_count
            },
            "playback": {
                "status": playback_info.playback_status,
                "auto_repeat_mode": playback_info.auto_repeat_mode,
                "is_shuffle_active": playback_info.is_shuffle_active,
            },
            "timeline": {
                "position": timeline.position.total_seconds() * 1000,
                "duration": timeline.end_time.total_seconds() * 1000,
                "last_updated_time": timeline.last_updated_time.timestamp()
            }
        })
    else:
        return web.json_response({"message": "not_found"}, status=404)


async def toggle_play_pause(request):
    session = await spotify()

    if session:
        session.try_toggle_play_pause_async()

    return web.Response(status=204)


async def seek(request: web.Request):
    time = request.query.get("time", "0")

    if not time.isnumeric():
        time = "0"

    session = await spotify()

    if session:
        await session.try_change_playback_position_async(int(time) * 10000)

    return web.Response(status=204)


async def rewind(request):
    session = await spotify()

    if session:
        await session.try_rewind_async()

    return web.Response(status=204)


async def fast_forward(request):
    session = await spotify()

    if session:
        await session.try_fast_forward_async()

    return web.Response(status=204)


async def handle_index(request):
    return web.Response(status=200, content_type="text/plain")


async def main():
    app = web.Application()
    app.router.add_get("/spotify", get_session)
    app.router.add_get("/toggle", toggle_play_pause)
    app.router.add_get("/seek", seek)
    app.router.add_get("/rewind", rewind)
    app.router.add_get("/fast_forward", fast_forward)
    app.router.add_get("/", handle_index)

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
    site = web.TCPSite(runner, "localhost", 8170)
    await site.start()

    print("HTTP server started at http://localhost:8170")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
