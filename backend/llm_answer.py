import os
from groq import Groq

# Configure Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192", # Strong reasoning model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error gathering answer: {e}"
