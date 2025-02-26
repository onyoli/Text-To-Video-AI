from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
import random

def generate_random_topic():
    """Uses AI to generate a trending, attention-grabbing YouTube video topic."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    topics = [
        "The Most Mysterious Places on Earth",
        "10 Unsolved Paranormal Cases That Will Give You Chills",
        "What Happened to Flight 370? The Disappearance Explained",
        "The Dark Truth Behind the Bermuda Triangle",
        "Real-Life Encounters with Ghosts – True Stories",
        "The Secret Underground Bunkers No One Talks About",
        "AI Predictions: Will Robots Take Over the World?",
        "Time Travel: Science Fiction or Secret Reality?",
        "The Most Haunted Places You Can Visit Today",
        "UFO Sightings the Government Can’t Explain"
    ]

    # Random fallback topic
    default_topic = random.choice(topics)

    try:
        response = client.completions.create(
            model="gpt-4",
            prompt="Give me a viral YouTube video topic about mysteries, paranormal events, or unsolved cases.",
            max_tokens=20
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("⚠️ OpenAI API failed, using a random topic instead.")
        return default_topic

if __name__ == "__main__":
    SAMPLE_TOPIC = generate_random_topic()
    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    print(f"🎥 **Generating video for topic:** {SAMPLE_TOPIC}")

    response = generate_script(SAMPLE_TOPIC)
    print("📝 Generated script:", response)

    asyncio.run(generate_audio(response, SAMPLE_FILE_NAME))

    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print("📝 Generated captions:", timed_captions)

    search_terms = getVideoSearchQueriesTimed(response, timed_captions)
    print("🔍 Search queries for video clips:", search_terms)

    background_video_urls = None
    if search_terms is not None:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        print("🎬 Background video URLs:", background_video_urls)
    else:
        print("⚠️ No background video found")

    background_video_urls = merge_empty_intervals(background_video_urls)

    if background_video_urls is not None:
        video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        print("✅ Final video generated:", video)
    else:
        print("⚠️ No final video generated")
