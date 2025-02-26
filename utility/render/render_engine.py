import tempfile
from moviepy.editor import CompositeVideoClip, VideoFileClip, AudioFileClip, TextClip
import requests

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    visual_clips = []
    temp_files = []

    try:
        for (t1, t2), video_url in background_video_data:
            with tempfile.NamedTemporaryFile(delete=False) as temp_video:
                temp_files.append(temp_video.name)
                download_file(video_url, temp_video.name)
                video_clip = VideoFileClip(temp_video.name).set_start(t1).set_end(t2)
                visual_clips.append(video_clip)

        # Add audio and captions
        audio_clip = AudioFileClip(audio_file_path)
        for (t1, t2), text in timed_captions:
            text_clip = TextClip(text, fontsize=100, color="white").set_start(t1).set_end(t2).set_position("center")
            visual_clips.append(text_clip)

        video = CompositeVideoClip(visual_clips)
        video = video.set_audio(audio_clip)
        video.write_videofile(OUTPUT_FILE_NAME, codec="libx264", fps=24)
    
    finally:
        # Cleanup temporary files
        for temp_file in temp_files:
            os.remove(temp_file)
    
    return OUTPUT_FILE_NAME
