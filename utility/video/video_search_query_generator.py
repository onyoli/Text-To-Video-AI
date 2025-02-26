from openai import OpenAI
import os
import json
import re
from utility.utils import log_response, LOG_TYPE_GPT

# Initialize client
client = None
model = None

if len(os.environ.get("GROQ_API_KEY", "")) > 30:
    try:
        from groq import Groq
        model = "llama3-70b-8192"
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    except ImportError:
        pass  # Fallback to OpenAI
else:
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")
    if OPENAI_API_KEY:
        model = "gpt-4o"
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        raise EnvironmentError("Missing OpenAI or Groq API key.")

# Rest of the code remains the same...
