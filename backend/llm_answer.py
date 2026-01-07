import google.generativeai as genai
import os

if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def generate_answer(question, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful and conversational AI assistant. 
Your primary source of information is the provided Context from a YouTube video.
Always prioritize the Context.

If the answer is found in the Context, answer using that information.
If the answer is NOT found in the Context, use your general knowledge to provide a helpful answer, but briefly mention that this information comes from outside the video.

Do not say "I don't know" unless the question is completely nonsensical.

Context:
{context}

Question:
{question}
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text
