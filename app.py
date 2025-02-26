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

# ✅ Ensure API key is set
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Error: Missing GROQ_API_KEY. Please set your API key in the environment variables.")

# ✅ AI-Powered Topic Generator
def generate_topic():
    print("\n🤖 Generating a viral topic using AI...")
    client = OpenAI(api_key=GROQ_API_KEY)  # Use OpenAI API for topic generation
    prompt = (
        "Generate a highly engaging, viral YouTube topic that sparks curiosity. "
        "It should be emotional, mysterious, or shocking to attract massive views."
    )

    response = client.completions.create(model="gpt-4", prompt=prompt, max_tokens=50)
    topic = response.choices[0].text.strip()

    if not topic:
        topic = "The Most Mysterious Unsolved Disappearance Ever"  # Fallback topic
        print("⚠️ Failed to generate topic. Using default:", topic)
    
    print("🎯 AI-Generated Topic:", topic)
    return topic

def main():
    # 🔹 Step 1: AI Generates the Topic
    topic = generate_topic()
    audio_file = "audio_tts.wav"
    video_server = "pexel"

    # 🔹 Step 2: AI Generates the Script
    print(f"\n🎬 Generating script for: {topic}...")
    script_text = generate_script(topic)

    if not script_text:
        print("⚠️ Error: Failed to generate script. Exiting.")
        return

    print("\n✅ Script Generated:\n", script_text)

    # 🔹 Step 3: Generate AI Voiceover
    print("\n🔊 Generating voice-over audio...")
    asyncio.run(generate_audio(script_text, audio_file))

    # 🔹 Step 4: Generate Timed Captions
    print("\n📝 Generating timed captions...")
    captions = generate_timed_captions(audio_file)

    # 🔹 Step 5: Search for Relevant Background Videos
    print("\n🔍 Finding background videos...")
    search_terms = getVideoSearchQueriesTimed(script_text, captions)
    print("🔎 Video Search Terms:", search_terms)

    background_video_urls = None
    if search_terms:
        background_video_urls = generate_video_url(search_terms, video_server)
        print("\n🎥 Selected Background Videos:", background_video_urls)
    else:
        print("\n⚠️ No suitable background videos found.")

    # 🔹 Step 6: Merge empty intervals for smooth transitions
    background_video_urls = merge_empty_intervals(background_video_urls)

    # 🔹 Step 7: Render Final Video
    if background_video_urls:
        print("\n🎬 Rendering Final Video...")
        final_video = get_output_media(audio_file, captions, background_video_urls, video_server)
        print("\n✅ Video Successfully Created:", final_video)
    else:
        print("\n⚠️ No video generated.")

if __name__ == "__main__":
    main()
