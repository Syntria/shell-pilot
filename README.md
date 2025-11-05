# Shell Pilot

Shell Pilot is a lightweight, command-line AI assistant powered by Google's Gemini model. It acts as a coding agent, allowing you to interact with your local file system, execute code, and modify files using natural language.

## ⚠️ Important Security Notice

This project is a proof-of-concept and a learning tool. It does **not** have all the security and safety features of a production-grade application. While it includes basic sandboxing to prevent file system access outside of a designated working directory, it is still possible for the AI model to generate and execute code that could have unintended consequences.

**Use this tool with precaution.** It is best suited for small, trusted projects. Do not run it in an environment with sensitive data. The user is responsible for all actions performed by the agent.

**Shell Pilot operates directly within your current terminal directory.** For your safety and to prevent unintended actions, **always ensure you are in the intended project directory** before invoking `shell-pilot`.

## Features

- **Natural Language Interface:** Interact with your file system using plain English.
- **Function Calling:** Leverages the Gemini model's function calling capabilities to perform actions.
- **File System Operations:** List, read, and write files.
- **Code Execution:** Run Python scripts in a sandboxed directory and see their output.

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Syntria/shell-pilot.git
    cd shell-pilot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    # On Windows, use: .\.venv\Scripts\activate
    ```

3.  **Install the project and its dependencies:**
    ```bash
    pip install .
    ```
    *(This command reads the `pyproject.toml` file and installs the necessary packages.)*

4.  **Set up your API Key:**
    - Go to https://aistudio.google.com/app/api-keys and create a API key
    - Create a `.env` file in the root of the project.
    - Add your Gemini API key to the file:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

## Usage

The script is run from the command line, taking a prompt in quotes as its main argument.

### Verbose Mode

For transparency, you can use the `--verbose` (or `-v`) flag after the prompt to see the token usage.

### Example: Fixing a Bug

Shell Pilot can be used to diagnose and fix bugs in your code.

You can instruct Shell Pilot to fix it with a single prompt:

```bash
sp "fix the bug: 3 + 7 * 2 shouldn't be 20"
