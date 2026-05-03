from openai.types.beta.assistant_stream_event import ThreadRunCancelled
from pyexpat import model
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL= os.getenv("OPENROUTER_BASE_URL")

client = OpenAI(base_url=OPENROUTER_BASE_URL,api_key=OPENROUTER_API_KEY)

INFORMATION_CONTEXT="""
<INFORMATION_CONTEXT>
Miki Bookstore is located at Banten.
We have local and international books collection.
Open Everyday from 10.00 to 19.00 WIB.
Answer nicely and warmly
</INFORMATION_CONTEXT>
"""

SYSTEM_PROMPT=f"""
<INFORMATION_CONTEXT>
You are a customer service for Miki BookStore.
Only answer based on this information context:
{INFORMATION_CONTEXT}

When you don't have the information, answer it politley.
</SYSTEM_PROMPT>
"""

messages=[
    {"role":"system","content": "SYSTEM_PROMPT"},
    ]

while True:
    user_input=input("User: ")
    user_message={"role": "user", "content":user_input}
    messages.append(user_message)

    completion=client.chat.completions.create(model="google/gemini-3.1-flash-lite-preview",messages=messages)  # ty:ignore[invalid-argument-type]

    final_output=completion.choices[0].message.content or ""
    print(final_output)
    messages.append({"role": "assistant","content":final_output})