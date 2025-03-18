from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm_gemini(message):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message,
    )
    return response


def print_llm_gemini(message):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message,
    )
    print(response.text)


def list_files_in_directory(directory="."):
    """
    Lists all non-hidden files in the specified directory.

    Args:
        directory (str): The directory to list files from. Defaults to the current working directory.
    """
    try:
        files = [
            f
            for f in os.listdir(directory)
            if (not f.startswith(".") and not f.startswith("_"))
        ]
        for file in files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")
