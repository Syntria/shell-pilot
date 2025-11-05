import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.functions.get_files_info import get_files_info, schema_get_files_info
from src.functions.get_file_content import get_file_content, schema_get_file_content
from src.functions.run_python_file import run_python_file, schema_run_python_file
from src.functions.write_file import schema_write_file, write_file

def call_function(function_call_part, verbose=False) -> types.Content:

    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_call_part.args["working_directory"] = "./"

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args}")

    else:
        print(f" - Calling function: {function_call_part.name}")


    function_to_run_name = function_call_part.name


    if function_to_run_name not in function_dict:

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_to_run_name,
                    response={"error": f"Unknown function: {function_to_run_name}"},
                )
            ],
        )

    else:
            function_to_run = function_dict[function_to_run_name]


            function_result  = function_to_run(**function_call_part.args)

            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_to_run_name,
                        response={"result": function_result},
                    )
                ],
            )

def main():

    model_name = 'gemini-2.5-flash'
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite filesd

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    """


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    max_loop_count = 20


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    parser = argparse.ArgumentParser(description="Lightweight Gemini CLI ")

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "prompt",
        help="The prompt"
    )

    args = parser.parse_args()


    if args.prompt:

        user_prompt = sys.argv[1]

        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        for count in range(max_loop_count):

            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions]
                ),
            )


            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)


            if not response.function_calls:
                print(response.text)
                return

            for function_call in response.function_calls:

                function_call_result = call_function(function_call, args.verbose)

                messages.append(function_call_result)
                
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")


                


            if args.verbose:
                if response.usage_metadata:
                    print("User Prompt: " + user_prompt)
                    print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
                    print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

        print("exiting loop")




if __name__ == "__main__":
    main()



