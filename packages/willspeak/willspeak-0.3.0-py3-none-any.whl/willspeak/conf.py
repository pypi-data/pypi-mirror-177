from pydantic import BaseModel


class Settings(BaseModel):
    appname: str
    timeout: float = 0.1
    port: int = 9999
    volume: int = 100
    rate: int = 4
    chunk: int = 4096
    speak_timeout = 10_000
