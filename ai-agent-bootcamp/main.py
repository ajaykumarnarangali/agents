import os
import sys
from dotenv import load_dotenv
from google.genai import types
from google import genai

load_dotenv()


def main():
    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    args = sys.argv
    if len(args) < 2:
        print("Please provide a prompt.")
        return

    prompt = args[1]
    messages: list[types.Content] = []
    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=messages
    )

    usage = response.usage_metadata
    if usage:
        print("\nToken Usage:")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    else:
        print("Token usage metadata is not available.")

    print(response.text)


if __name__ == "__main__":
    main()
