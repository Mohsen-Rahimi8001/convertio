import ffmpeg


def reverse_video(file_path, output_path):
    
    try:
        (
            ffmpeg
            .input(file_path)
            .output(output_path, vf='reverse', af='areverse')
            .run(overwrite_output=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print("FFmpeg error:", e.stderr.decode())
        raise e
