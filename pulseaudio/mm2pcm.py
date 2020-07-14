"""Change the multimedia to PCM, using ffmpeg."""
import asyncio
from haffmpeg.core import HAFFmpeg

class PCMStream(HAFFmpeg):
    """Implement a audio stream of the multimedia file."""

    async def PCMStreamReader(self, input_source: str
        ) -> asyncio.StreamReader:
        """Open FFmpeg process as pcm audio stream,
        and return the stream reader.
        """
        await self.open(cmd=[],
                        input_source=input_source,
                        output="-acodec pcm_s16le -f s16le -ac 1 -ar 16k -"
                        )
        return await self.get_reader()
