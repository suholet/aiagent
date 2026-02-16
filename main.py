import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

def main():
    parser = argparse.ArgumentParser(description="AI Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Now we can access `args.user_prompt`
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key is None:
        raise RuntimeError("Can't load API key")
    
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash"
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0
        ),
)

    if response.usage_metadata is None:
        raise RuntimeError("Problem with Gemini API call")
    
    prompt_token = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_tokens}")
    print(response.text)


if __name__ == "__main__":
    main()
