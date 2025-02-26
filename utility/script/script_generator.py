import os
from openai import OpenAI
import json

# Initialize client based on environment variables
if len(os.environ.get("GROQ_API_KEY", "")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
else:
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = """[Your prompt here]"""  # Keep your existing prompt

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except json.JSONDecodeError:
        json_start = content.find('{')
        json_end = content.rfind('}')
        if json_start == -1 or json_end == -1:
            raise ValueError("No valid JSON found.")
        script = json.loads(content[json_start:json_end+1])["script"]
    return script
