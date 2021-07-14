import os
import subprocess
from . import FSIZE_TARGET

# 新しい fpath を返す
def trimming_video_to_8MB(fname: str) -> str:
    target_name = fname

    while os.path.getsize(target_name) > FSIZE_TARGET:
        fsize = os.path.getsize(target_name)
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", target_name],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        current_duration:int = int(float(result.stdout.decode("utf-8").strip()))
        print("current duration: ", current_duration)

        target_duration_f: float = float(FSIZE_TARGET) / fsize * current_duration
        target_duration:int = int(target_duration_f)
        new_file_name = target_name.split(".")[0] + "-trimmed" + ".mp4"
        # [ffmpegで変換の際に大量に出る標準出力をログレベル指定ですっきりする - /var/www/yatta47.log](https://yatta47.hateblo.jp/entry/2015/03/03/231204)
        subprocess.run(["ffmpeg", "-y", "-i", target_name, "-t", str(target_duration), "-loglevel", "24", "-c", "copy", new_file_name])
        if "-trimmed" in target_name:
            os.remove(target_name)
        target_name = new_file_name
    one_trimmed = fname.split(".")[0] + "-trimmed" + ".mp4"
    os.rename(new_file_name, one_trimmed)
    return one_trimmed