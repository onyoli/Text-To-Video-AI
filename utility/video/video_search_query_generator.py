import os
import json
import re
from openai import OpenAI
from utility.utils import log_response, LOG_TYPE_GPT

# Initialize client
client = None
model = None

if len(os.environ.get("GROQ_API_KEY", "")) > 30:
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        model = "llama3-70b-8192"
    except ImportError:
        pass  # Fallback to OpenAI
else:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        model = "gpt-4o"
    else:
        raise EnvironmentError("Missing OpenAI or Groq API key.")

def getVideoSearchQueriesTimed(script, captions_timed):
    """
    Generate timed video search queries based on the script and captions.
    """
    end = captions_timed[-1][0][1]
    try:
        out = [[[0, 0], ""]]
        while out[-1][0][1] != end:
            content = call_openai(script, captions_timed).replace("'", '"')
            try:
                out = json.loads(content)
            except json.JSONDecodeError:
                content = fix_json(content.replace("```json", "").replace("```", ""))
                out = json.loads(content)
        return out
    except Exception as e:
        print(f"Error in response: {e}")
        return None

def call_openai(script, captions_timed):
    """
    Call OpenAI to generate search queries.
    """
    user_content = f"Script: {script}\nTimed Captions: {captions_timed}"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ]
    )
    text = response.choices[0].message.content.strip()
    log_response(LOG_TYPE_GPT, script, text)
    return text

def fix_json(json_str):
    """
    Fix common JSON formatting issues.
    """
    json_str = json_str.replace("’", "'")
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")
    json_str = json_str.replace('"you didn"t"', '"you didn\'t"')
    return json_str

def merge_empty_intervals(segments):
    """
    Merge intervals with no video URLs.
    """
    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j-1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            i = j
        else:
            merged.append([interval, url])
            i += 1
    return merged
