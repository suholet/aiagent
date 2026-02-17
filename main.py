import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def call_model(client, model_name, messages):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
        )
    return response

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
    
    for _ in range(20):
        # call the model, handle responses, etc.
        response = call_model(client, model_name, messages)

        if response.usage_metadata is None:
            raise RuntimeError("Problem with Gemini API call")
        
        for candidate in response.candidates:
            messages.append(candidate.content)

        prompt_token = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_token}")
            print(f"Response tokens: {response_tokens}")

        function_calls = response.function_calls

        if function_calls != None:
            function_results = []

            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                
                if len(function_call_result.parts) == 0:
                    raise Exception("Error: empty function_call_result.parts")
                
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Error: function_response is None")
                
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Error: function_response.response is None")
                
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print("Final response:")
            print(response.text)
            return

    print("Something went wrong. No final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
