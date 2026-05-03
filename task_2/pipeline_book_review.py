import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL= os.getenv("OPENROUTER_BASE_URL")

client = OpenAI(base_url=OPENROUTER_BASE_URL,api_key=OPENROUTER_API_KEY)

class Event(BaseModel):
    title: str
    author: str
    genre: str
    recommendation: str

#raw information topic
def generate_book_content(user_input):
    completion = client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[
            {"role": "user", "content": user_input},
            {"role": "system", "content": "You are a book reviewer. Make it 3-4 sentences, comprehensive and informative"}
        ],
        max_tokens=1000
    )
    return completion.choices[0].message.content

#summary from the raw information
def summarize_book_content(raw_information):
    completion=client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[
            {"role": "user", "content": f"summarize this {raw_information}"}],
        max_tokens=500
    )
    return completion.choices[0].message.content

#extract summary information into bullet points
def extract_information(book_summary):
    completion=client.chat.completions.parse(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[
            {"role": "user", "content": book_summary},
            {"role": "system", "content": "Extract the information based on book summary"}
        ],
        max_tokens=500,
        response_format=Event
    )
    return completion.choices[0].message.parsed


if __name__ == "__main__":
    user_input = input("Input Book Title: ")

    about_book=generate_book_content(user_input)
    print(f"About the book: \n{about_book}")

    summary_book=summarize_book_content(about_book)
    print(f"\nSummary: \n{summary_book}")

    key_points = extract_information(summary_book)
    print(f"\n{key_points}")
