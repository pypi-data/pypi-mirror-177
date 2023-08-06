# Standard lib
import asyncio

# Third party
from aiohttp import web

# Allow for route decorators
routes = web.RouteTableDef()


# Functions
######################################################################

def create_full_url(request: web.Request, path: str) -> str:
    """Create a full absolute url using request to build the url."""
    return f"{request.scheme}://{request.host}{path}"


# Views
######################################################################

@routes.get("/")
async def api_root(request: web.Request):
    """
    This is the api root. It should list the urls to all the api endpoints.

    Endpoints:
        * /speak: Convert text to speach and respond with a raw wav file.
        * /settings: Get/set TTS engine parameters.
        * /voices: Get list of all available voices.
    """
    data = dict(
        speak=create_full_url(request, "/speak"),
        stop=create_full_url(request, "/stop"),
        settings=create_full_url(request, "/settings"),
        voices=create_full_url(request, "/voices"),
    )
    return web.json_response(data)


@routes.get("/voices")
async def get_voices(request: web.Request):
    """
    Return list of all available voices.
    """
    engine = request.app["tts_engine"]
    data = []
    for voice in engine.get_voices():
        voice_dict = voice.asdict_shallow()
        voice_dict["url"] = create_full_url(request, f"/voices/{voice_dict['id']}")
        data.append(voice_dict)
    return web.json_response(data)


@routes.get("/voices/{id}")
async def get_voice(request: web.Request):
    """
    Return details about slected voice.
    """
    engine = request.app["tts_engine"]
    voice_id = request.match_info["id"]

    for voice in engine.get_voices():
        # Do the check as strings, as the voice ID can be a string
        if str(voice.id) == str(voice_id):
            voice_dict = voice.asdict_shallow()
            voice_dict["url"] = create_full_url(request, f"/voices/{voice_dict['id']}")
            return web.json_response(voice_dict)

    message = f"No voice found matching ID: {voice_id}"
    return web.json_response({"error": message}, status=404)


@routes.view("/settings")
class Settings(web.View):
    async def get(self):
        """
        Return the current settings values.

        Settings:
            * rate: The current speaking rate.
            * volume: The current speaking volume.
            * voice: The currently selected voice.
        """
        engine = self.request.app["tts_engine"]
        voice_dict = engine.voice.asdict_shallow()
        voice_dict["url"] = create_full_url(self.request, f"/voices/{voice_dict['id']}")

        data = dict(
            rate=engine.rate,
            volume=engine.volume,
            voice=voice_dict,
        )

        return web.json_response(data)

    async def put(self):
        """
        Change any or all of the tts settings.
        """
        engine = self.request.app["tts_engine"]
        req_data = await self.request.json()

        if "rate" in req_data:
            engine.rate = req_data["rate"]
        if "volume" in req_data:
            engine.volume = req_data["volume"]
        if "voice" in req_data:
            voice_id = req_data["voice"]
            try:
                engine.voice = voice_id
            except ValueError as e:
                return web.json_response({"error": str(e)}, status=400)

        # Return the full settings response with changes
        return await self.get()


@routes.view("/speak")
class Speak(web.View):
    """
    Convert any given text into speach.

    The text can be given by using url params, or by using the request body.
    The url param to use is called 'text', the value needs to be url encoded.
    When sending the text using the body it can just be a plain text post request.
    The response will be a raw wave file.

    Support for other response types are planned.
    """
    EOF = object()

    async def get(self):
        """Handle text from url params."""
        if "text" not in self.request.query:
            message = "Missing required url parameter: text"
            return web.json_response({"error": message}, status=400)

        texts = self.request.query.getall("text")
        text = " ".join(texts)
        return await self.speak(text)

    async def post(self):
        """Handel text from post request."""
        if not self.request.can_read_body:
            message = "Missing required text body"
            return web.json_response({"error": message}, status=400)

        text = await self.request.text()
        return await self.speak(text)

    async def speak(self, text: str):
        """Convert text into speach."""
        loop = asyncio.get_running_loop()
        resp = web.StreamResponse()
        await resp.prepare(self.request)

        def callback(audio_chunk: bytes):
            # Be careful here, this code is synchronous, no async here
            coroutine = resp.write(audio_chunk)
            asyncio.run_coroutine_threadsafe(coroutine, loop).result()

        # Call TTS engine in another thread as the call is a blocking call
        engine = self.request.app["tts_engine"]
        stream = engine.create_memory_stream()
        await loop.run_in_executor(None, engine.raw_speak, stream, callback, text)

        # Finalize response
        await resp.write_eof()
        return resp


@routes.get("/stop")
async def stop_speak(request: web.Request):
    engine = request.app["tts_engine"]
    engine.stop()
    return web.json_response(status=204)


# Async Setup
######################################################################

@web.middleware
async def http_404_middleware(request, handler):
    """
    Middleware that converts a 404 page
    not found error into a json response.
    """
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.reason
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({"error": message})


async def setup_tt_engine(app):
    """Initialize TTS engine."""
    from willspeak.tts.sapi5.local import TTSClient
    engine = TTSClient(server_mode=True)
    app["tts_engine"] = engine


def start(addr: str, port: int):
    """Start the async http sapi5 api server."""
    middlewares = [http_404_middleware]
    app = web.Application(middlewares=middlewares)
    app.add_routes(routes)
    app.on_startup.append(setup_tt_engine)
    web.run_app(app, host=addr, port=port)
