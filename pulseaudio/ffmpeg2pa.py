import shlex
from subprocess import PIPE, Popen

class AudioPlay(object):
    """
    Wraps a binary ffmpeg and pacat executable
    """
    def __init__(self, ffmpeg_exe_file, device_option, volume=65536):
        self._FfmpegProc = self._PacatProc = None
        self._FfmpegCmd = "%s  -hide_banner -loglevel panic -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16k -" %(ffmpeg_exe_file, '%s')
        self._PacatCmd = "pacat --format=s16le --rate=16000 --channels=1 %s %s" %(device_option, '%s')
        self._volume = volume

    def play(self, audiofile):
        volume_option = "--volume=%d" %(self._volume)
        FfmpegArgv = shlex.split(str(self._FfmpegCmd % (audiofile)))
        PacatArgv = shlex.split(str(self._PacatCmd) % (volume_option))

        if self._FfmpegProc is not None and self._FfmpegProc.poll() is None:
            self._FfmpegProc.terminate()
        if self._PacatProc is not None and self._PacatProc.poll() is None:
            self._PacatProc.terminate()

        self._FfmpegProc = Popen(FfmpegArgv, stdin=PIPE, stdout=PIPE)
        self._PacatProc = Popen(PacatArgv, stdin=self._FfmpegProc.stdout)

    def stop(self):
        if self._FfmpegProc is not None and self._FfmpegProc.poll() is None:
            self._FfmpegProc.stdin.write(b'q')
            self._FfmpegProc.stdin.flush()

    def set_volume(self, volume):
        self._volume = volume

    @property
    def volume(self):
        return self._volume

    @property
    def is_running(self):
        return self._PacatProc is not None and self._PacatProc.poll() is None
