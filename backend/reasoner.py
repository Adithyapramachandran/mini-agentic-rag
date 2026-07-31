import google.generativeai as genai

from backend.config import GEMINI_API_KEY

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def decide(query, context):

    with open(
        "prompts/reasoner_v2.txt",
        "r",
        encoding="utf-8"
    ) as f:

        prompt_template = f.read()

    prompt = f"""
{prompt_template}

Question:
{query}

Context:
{context}
"""

    response = model.generate_content(
        prompt
    )

    return response.text.strip()