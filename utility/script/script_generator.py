import os
import json
from openai import OpenAI  # Moved to top for clarity

# Initialize client outside function to avoid repeated setup
if len(os.environ.get("GROQ_API_KEY", "")) > 30:
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    model = "mixtral-8x7b-32768"
else:
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
    model = "gpt-4o"

def generate_script(topic):
    prompt = """[Your existing prompt here]"""  # Keep your original prompt
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    
    # Improved JSON parsing
    content = response.choices[0].message.content
    try:
        return json.loads(content)["script"]
    except json.JSONDecodeError:
        json_str = content[content.find('{'):content.rfind('}')+1]
        return json.loads(json_str)["script"]
