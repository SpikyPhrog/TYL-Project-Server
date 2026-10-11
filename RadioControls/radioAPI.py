import asyncio
import telnetlib3

class RadioTelnetManager:
    def __init__(self, host="127.0.0.1", port=1234):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.lock = asyncio.Lock()

        self.currentTrack = {
            "artist" : "",
            "title" : "",
            "filename" : ""
        }


    async def ensure_connected(self):
        if self.writer is None or self.writer.is_closing():
            await self.connect()

    async def connect(self):
        self.reader, self.writer = await telnetlib3.open_connection(self.host, self.port, encoding="utf-8")
        await asyncio.sleep(0.1)

        print("Connected To RadioTelnet")

    async def command(self, command : str):
        async with self.lock:
            self.writer.write(command + "\n")
            await self.writer.drain()

            lines = []

            while True:
                line = await self.reader.readline()
                if not line:
                    raise ConnectionError(
                        "Connection Closed"
                    )
                line = line.rstrip("\r\n")

                if line == "END":
                    break

                lines.append(line)

            return "\n".join(lines)

    async def close(self):
        if self.writer:
            self.writer.close()
            self.writer = None
            self.reader = None

    async def skip(self):
        return await self.command("music.skip")

    async def currently_playing(self):
        on_air = await self.command("request.on_air")
        # Split the string and add spaces back as separate elements
        IDs = [part if part.strip() else " " for part in on_air.split(" ")]
        songID = 0

        for i in range(len(IDs)):
            if 0 <= i <= 23:
                songID = IDs[i]
                break

        metadata_raw = await self.command(f"request.metadata {songID}")

        metadata = self.parse_metadata(metadata_raw)

        return {
            "artist" : metadata.get("artist", ""),
            "title" : metadata.get("title", ""),
            "filename" : metadata.get("filename", ""),
        }

    def parse_metadata(self, metadata:str) ->dict:
        result = {}

        for line in metadata.splitlines():
            line = line.strip()

            if "=" not in line:
                continue

            key, value = line.split("=" , 1)

            value = value.strip().strip('"')
            result[key] = value

            return result