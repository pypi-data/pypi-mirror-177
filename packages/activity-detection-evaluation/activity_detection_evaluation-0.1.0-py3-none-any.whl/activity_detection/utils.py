import subprocess
import librosa


def get_content_duration(filepath: str, data_type: str):
    if data_type == "audio":
        librosa.get_duration(filename=filepath)
    elif data_type == "video":
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                filepath,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    else:
        raise ValueError(f"Invalid data type specified: {data_type}")
    return float(result.stdout)
