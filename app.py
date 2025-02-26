from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
import argparse
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals

# ✅ Check for API Key to prevent errors
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Error: Missing GROQ_API_KEY. Please set your API key in the environment variables.")

def main():
    parser = argparse.ArgumentParser(description="Generate a video from a topic.")
    parser.add_argument("topic", type=str, help="The topic for the video")
    args = parser.parse_args()

    topic = args.topic
    audio_file = "audio_tts.wav"
    video_server = "pexel"

    print(f"🎬 Generating script for topic: {topic}...")
    script_text = generate_script(topic)

    if not script_text:
        print("⚠️ Error: Failed to generate script. Exiting.")
        return

    print("\n✅ Script Generated:\n", script_text)

    print("\n🔊 Generating voice-over audio...")
    asyncio.run(generate_audio(script_text, audio_file))

    print("\n📝 Generating timed captions...")
    captions = generate_timed_captions(audio_file)

    print("\n🔍 Finding relevant background videos...")
    search_terms = getVideoSearchQueriesTimed(script_text, captions)
    print("🔎 Video Search Terms:", search_terms)

    background_video_urls = None
    if search_terms:
        background_video_urls = generate_video_url(search_terms, video_server)
        print("\n🎥 Selected Background Videos:", background_video_urls)
    else:
        print("\n⚠️ No suitable background videos found.")

    # ✅ Merge empty intervals to ensure smooth video transitions
    background_video_urls = merge_empty_intervals(background_video_urls)

    if background_video_urls:
        print("\n🎬 Rendering Final Video...")
        final_video = get_output_media(audio_file, captions, background_video_urls, video_server)
        print("\n✅ Video Successfully Created:", final_video)
    else:
        print("\n⚠️ No video generated.")

if __name__ == "__main__":
    main()
