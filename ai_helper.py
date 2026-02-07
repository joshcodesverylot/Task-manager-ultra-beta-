from dotenv import load_dotenv, find_dotenv
from google import genai
import os


filepath = find_dotenv()
load_dotenv(filepath)
api_key = os.getenv("API_KEY")


client = genai.Client(api_key=api_key)

def categorize_tasks(task_text):
    prompt = f"Categorize this task into one word (e.g., Work, Personal, Health, Chores): '{task_text}'"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return response.text.strip()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    task = "Do the laundry"
    print(f"Task: {task}")
    print(f"Response: {categorize_tasks(task)}")