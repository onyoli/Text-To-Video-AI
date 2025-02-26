from groq import Groq
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

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_topic():
    """Generate a random topic using Groq's LLM (e.g., Mixtral or LLaMA)"""
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": "Generate a random interesting topic for a short video."}],
        model="mixtral-8x7b-32768",  # Or "llama2-70b-4096"
        temperature=0.7,
        max_tokens=50
    )
    return response.choices[0].message.content.strip()

async def main():
    # Always generate a topic using AI
    SAMPLE_TOPIC = generate_topic()
    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    print(f"Generated Topic: {SAMPLE_TOPIC}")

    # Step 1: Generate script
    response = generate_script(SAMPLE_TOPIC)
    print("Script:", response)

    # Step 2: Generate audio from script
    await generate_audio(response, SAMPLE_FILE_NAME)

    # Step 3: Generate timed captions from audio
    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print("Captions:", timed_captions)

    # Step 4: Generate search terms for background videos
    search_terms = getVideoSearchQueriesTimed(response, timed_captions)
    print("Search Terms:", search_terms)

    # Step 5: Fetch background video URLs
    background_video_urls = None
    if search_terms:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        print("Video URLs:", background_video_urls)
    else:
        print("No background video")

    # Step 6: Merge empty intervals in video URLs
    background_video_urls = merge_empty_intervals(background_video_urls)

    # Step 7: Render final video
    if background_video_urls:
        video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        print("Output Video:", video)
    else:
        print("No video generated")

if __name__ == "__main__":
    asyncio.run(main())
