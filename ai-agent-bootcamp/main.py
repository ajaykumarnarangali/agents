import os
import sys
from dotenv import load_dotenv
from google.genai import types
from google import genai
from functions.get_file_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_the_function import call_function

load_dotenv()


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    system_prompt =( """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, analyze the task and decide which available tools are needed.

        Available tools:
        - get_files_info: Lists files and directories inside a specified directory.
        - get_file_content: Reads and returns the contents of a specified file.
        - write_file: Creates or overwrites a file with the provided content.
        - run_python_file: Executes a Python file and returns its output.

        Instructions:
        - Understand the user's request before taking action.
        - Use available tools when necessary.
        - Choose the appropriate tool based on the user's request.
        - Use get_files_info when the user asks to list or inspect directory contents.
        - Use get_file_content when the user asks to read, inspect, or understand a file's contents.
        - Use write_file when the user asks to create or modify a file.
        - Use run_python_file when the user asks to execute a Python file.
        - All paths provided to tools must be relative to the working directory.
        - When the user specifies a directory, pass its relative path as the directory argument.
        - When the user specifies a file, pass its relative path as the file_path argument.
        - If the user specifies a nested directory or file, include the complete relative path.
        - Use "." only when the user asks for the root working directory.
        - Never attempt to access files outside the working directory.
        - Do not assume file contents; inspect files when necessary.
        - Use tool results to decide the next action.
        - You may call multiple tools when needed.
        - Continue working until the requested task is completed.
        - If a tool returns an error, analyze it before deciding what to do next.
        - Do not claim that an operation succeeded unless the tool confirms it.
        - If the task cannot be completed, explain why.
        - Provide a clear and concise final response.
        """
    )

    client = genai.Client(api_key=api_key)

    args = sys.argv
    if len(args) < 2:
        print("Please provide a prompt.")
        return

    verbose_flag = False
    if len(args) == 3 and args[2] == "--verbose":
        verbose_flag = True

    prompt = args[1]
    messages: list[types.Content] = []
    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    max_loop=20
    for i in range(0,max_loop):
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )

        usage = response.usage_metadata
        if usage and verbose_flag:
            print("\nToken Usage:")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        elif verbose_flag:
            print("Token usage metadata is not available.")           

        messages.append(
            types.Content(
                role="model",
                parts=response.candidates[0].content.parts
            )
        )

        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose_flag)
                messages.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"result": result},
                            )
                        ],
                    )
                )
        else:
            print(response.text)
            return

       

if __name__ == "__main__":
    main()
